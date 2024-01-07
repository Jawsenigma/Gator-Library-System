import time
import os
import sys
import argparse
import re
from RedBlackTree import RBTree
from RedBlackTree import Book

parser = argparse.ArgumentParser(description="Process an input file")
parser.add_argument("input_file", help="Path to the input file")
args = parser.parse_args()


def process_input_line(line, library, output_file):
    # Parse the input line and perform the corresponding operation

    if line.startswith('InsertBook'):
        # Parse arguments and perform the insert operation
        line = line.replace('InsertBook', 'insert_book')
        exec(f'library.{line}')

    elif line[:9] == 'PrintBook' and line[:10] != 'PrintBooks':
        # Parse arguments and perform the print operation
        bookID = eval(line[10:-1])
        book = library.books.find(bookID)
        library.print_book(book, bookID, output_file)

    elif line[:10] == 'PrintBooks':
        # Parse arguments and perform the print operation
        bookID1, bookID2 = map(int, line[11:-1].split(','))
        library.print_books(bookID1, bookID2, output_file)

    elif line.startswith('BorrowBook'):
        # Parse arguments and perform the borrow operation
        parts = line[11:-1].split(', ')
        patronID, bookID, patronPriority = map(eval, parts)
        library.borrow_book(patronID, bookID, patronPriority)

    elif line.startswith('ReturnBook'):
        # Parse arguments and perform the return operation
        parts = line[11:-1].split(', ')
        patronID, bookID = map(eval, parts)
        library.return_book(patronID, bookID, output_file)

    elif line.startswith('FindClosestBook'):
        # Parse arguments and perform the find closest book operation
        targetID = eval(line[16:-1])
        library.find_closest_book(targetID, output_file)

    elif line.startswith('DeleteBook'):
        # Parse arguments and perform the delete operation
        bookID = eval(line[11:-1])
        library.delete_book(bookID)

    elif line.startswith('ColorFlipCount'):
        # Perform the color flip count operation
        library.color_flip_count()


class Patron:
    def __init__(self, patronID):
        self.patronID = patronID


class gatorLibrary:
    def __init__(self):
        self.books = RBTree()

    def insert_book(self, bookID, bookName, authorName, availabilityStatus):
        # Add a new book to the library
        new_book = Book(bookID, bookName, authorName, availabilityStatus)
        self.books.insert(new_book)

    def print_book(self, book, bookID, output_file):
        if book is not None:
            availability_status = "Yes" if book.Book.availabilityStatus else "No"
            reservations = set(r[0] for r in book.Book.reservationHeap.Heap if r != 0 and r[0] != -1)
            reservations = list(reservations)
            output_file.write(f"BookID = {book.Book.bookID}\n"
                              f"Title = \"{book.Book.bookName}\"\n"
                              f"Author = \"{book.Book.authorName}\"\n"
                              f"Availability = \"{availability_status}\"\n"
                              f"BorrowedBy = {None if book.Book.borrowedBy is None else f'{book.Book.borrowedBy}'}\n"
                              f"Reservations = {reservations}\n\n")
        else:
            output_file.write(f"Book {bookID} not found in the library\n\n")

    def print_books(self, bookID1, bookID2, output_file):
        for book_node in self.books.in_order_traversal():
            book_id = book_node.Book.bookID
            if bookID1 <= book_id <= bookID2:
                self.print_book(book_node, book_id, output_file)

    def borrow_book(self, patronID, bookID, patronPriority):
        # Allow a patron to borrow a book
        book = self.books.find(bookID)
        if book and book.Book.availabilityStatus and book.Book.borrowedBy is None:
            # Book is available, and the patron doesn't have it already
            book.Book.availabilityStatus = False
            book.Book.borrowedBy = patronID
            output_file.write(f"Book {book.Book.bookID} Borrowed by Patron {patronID} \n\n")
        elif book:
            # Book is not available, add to the reservation heap
            book.Book.insert_reservation(patronID, patronPriority, time.time())
            output_file.write(f"Book {bookID} Reserved by Patron {patronID}\n\n")

    def return_book(self, patronID, bookID, output_file):
        book = self.books.find(bookID)
        if book is None:
            return
        if book and book.Book.borrowedBy == patronID:
            # Book is borrowed by the patron, return it
            book.Book.availabilityStatus = True
            book.Book.borrowedBy = None

            highest_priority_patronID = None

            # Assign the book to the highest priority patron in the reservation heap
            while not book.Book.is_reservation_empty():
                reservation = book.Book.extract_min_reservation()
                highest_priority_patronID = reservation[0]
                # Ensure the book is not returned to the same patron
                if highest_priority_patronID != patronID:
                    book.Book.borrowedBy = highest_priority_patronID
                    book.Book.availabilityStatus = False
                    break

            if highest_priority_patronID is not None:
                output_file.write(f"Book {book.Book.bookID} Returned by Patron {patronID}\n\n")
                output_file.write(f"Book {book.Book.bookID} Allotted to Patron {highest_priority_patronID}\n\n")
            else:
                output_file.write(f"Book {book.Book.bookID} Returned by Patron {patronID}\n\n")

    def delete_book(self, bookID):
        # Delete a book from the library
        book = self.books.find(bookID)
        if book:
            canceled_patron_ids = []
            # Notify patrons in the reservation list that the book is no longer available
            while not book.Book.reservationHeap.is_empty():
                reservation = book.Book.reservationHeap.extract_min()
                patronID = reservation[0]
                canceled_patron_ids.append(patronID)

            # Write a message for each canceled reservation
            if canceled_patron_ids:
                canceled_patron_ids_str = ', '.join(map(str, canceled_patron_ids))
                if len(canceled_patron_ids) < 2:
                    output_file.write(
                        f"Book {book.Book.bookID} is no longer available. Reservation made by Patron {canceled_patron_ids_str} has been cancelled!\n\n")
                else:
                    output_file.write(
                        f"Book {book.Book.bookID} is no longer available. Reservations made by Patrons {canceled_patron_ids_str} have been cancelled!\n\n")
            else:
                output_file.write(f"Book {book.Book.bookID} is no longer available\n\n")

            # Delete the book from the tree
            self.books.delete(bookID)

    def not_found(self, book, output_file):
        output_file.write(f"Book {book.Book.bookID} not found in the library\n\n")

    def find_closest_book(self, targetID, output_file):
        closest_books = self.books.find_closest(targetID)
        closest_books = sorted(closest_books, key=lambda x: x.Book.bookID)
        if closest_books:
            for books in (closest_books):
                self.print_book(books, books, output_file)
        else:
            output_file.write("No books found.\n")

    def color_flip_count(self):
        output_file.write(f"Color Flip Count: {self.books.color_flip_count()}\n\n")


library = gatorLibrary()
with open(args.input_file, "r") as input_file:
    input_base_name = os.path.splitext(os.path.basename(args.input_file))[0]

    # Use the base name in the output file name
    output1 = f"{input_base_name}_output_file.txt"
    with open(output1, "w") as output_file:
        for line in input_file:
            if line.strip().lower() == 'quit()':
                # Terminate the program when encountering "Quit"
                output_file.write("Program Terminated!!\n")
                sys.exit()
            process_input_line(line.strip(), library, output_file)