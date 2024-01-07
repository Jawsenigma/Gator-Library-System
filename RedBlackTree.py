from BinaryMinHeap import BinaryMinHeap


class Book:
    def __init__(self, bookID=None, bookName=None, authorName=None, availabilityStatus=None):
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = None
        self.reservationHeap = BinaryMinHeap(20)

    # Define how two Book instances should be compared based on their bookID
    def __lt__(self, other):
        return self.bookID < other.bookID

    # Insert a reservation into the reservation heap of the book
    def insert_reservation(self, patronID, priority, timeOfReservation):
        self.reservationHeap.insert(patronID, priority, timeOfReservation)

    # Extract the minimum reservation from the reservation heap
    def extract_min_reservation(self):
        return self.reservationHeap.extract_min()

    # Check if the reservation heap is empty
    def is_reservation_empty(self):
        return self.reservationHeap.is_empty()


class RedBlackNode:
    def __init__(self):
        self.red = False
        self.parent = None
        self.Book = Book()
        self.left = None
        self.right = None


class RBTree:
    def __init__(self):
        self.nil = RedBlackNode()
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
        self.color_flip_counter = 0

    # Implement Red-Black Tree operations: Insert, Delete, FindClosestBook

    def insert(self, val):
        # Insert a value into the tree.
        inserted_node = RedBlackNode()
        inserted_node.parent = None
        inserted_node.Book = val
        inserted_node.left = self.nil
        inserted_node.right = self.nil
        inserted_node.red = True  # new node must be red

        self._insert_node(inserted_node)

    def _insert_node(self, inserted_node):
        # Insert a node into the tree.
        y = None
        x = self.root

        while x != self.nil:
            y = x
            if inserted_node.Book.bookID < x.Book.bookID:
                x = x.left
            else:
                x = x.right

        inserted_node.parent = y
        if y is None:
            self.root = inserted_node
        elif inserted_node.Book.bookID < y.Book.bookID:
            y.left = inserted_node
        else:
            y.right = inserted_node

        if inserted_node.parent is None:
            inserted_node.red = False
        elif inserted_node.parent.parent is not None:
            self.fix_insert(inserted_node)

    def delete(self, val):
        # Delete a value from the tree.
        z = self.find(val)
        if z == self.nil:
            return
        self._delete_node(z)

    def _delete_node(self, z):
        # Delete a node from the tree.
        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.replace_subtree(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.replace_subtree(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.red
            x = y.right

            if x is not self.nil:
                x.parent = y

            if y.parent == z:
                x.parent = y
            else:
                self.replace_subtree(y, y.right)
                y.right = z.right
                if y.right is not self.nil:
                    y.right.parent = y

            self.replace_subtree(z, y)
            y.left = z.left

            if y.left is not self.nil:
                y.left.parent = y

            y.red = z.red

        if not y_original_color:
            self.fix_delete(x)

    # Replace the subtree rooted at 'source_node' with the subtree rooted at 'replacement_node' during Red-Black Tree deletion.
    def replace_subtree(self, source_node, replacement_node):
        if source_node is not None and source_node.parent is None:
            self.root = replacement_node
        elif source_node is not None and source_node.parent is not None:
            if source_node == source_node.parent.left:
                source_node.parent.left = replacement_node
            else:
                source_node.parent.right = replacement_node
        if replacement_node is not None:
            replacement_node.parent = source_node.parent

    # Fix the tree structure after delete operation to maintain RB tree properties
    def fix_delete(self, deleted_node):
        while deleted_node != self.root and not deleted_node.red:
            if deleted_node.parent is not None:
                if deleted_node == deleted_node.parent.left:
                    sibling_node = deleted_node.parent.right
                    if sibling_node is not None:
                        if sibling_node.red:
                            sibling_node.red = False
                            deleted_node.parent.red = True
                            self.rotate_left(deleted_node.parent)
                            sibling_node = deleted_node.parent.right
                            self.color_flip_counter += 3

                        if not (sibling_node.left is not None and sibling_node.left.red) and not (
                                sibling_node.right is not None and sibling_node.right.red):
                            sibling_node.red = True
                            deleted_node = deleted_node.parent
                        else:
                            if not (sibling_node.right is not None and sibling_node.right.red):
                                if sibling_node.left is not None:
                                    sibling_node.left.red = False
                                sibling_node.red = True
                                self.rotate_right(sibling_node)
                                sibling_node = deleted_node.parent.right
                                self.color_flip_counter += 3

                            sibling_node.red = deleted_node.parent.red
                            deleted_node.parent.red = False
                            if sibling_node.right is not None:
                                sibling_node.right.red = False
                            self.rotate_left(deleted_node.parent)
                            deleted_node = self.root
                            self.color_flip_counter += 1

                else:
                    sibling_node = deleted_node.parent.left
                    if sibling_node is not None:
                        if sibling_node.red:
                            sibling_node.red = False
                            deleted_node.parent.red = True
                            self.rotate_right(deleted_node.parent)
                            sibling_node = deleted_node.parent.left
                            self.color_flip_counter += 3

                        if not (sibling_node.right is not None and sibling_node.right.red) and not (
                                sibling_node.left is not None and sibling_node.left.red):
                            sibling_node.red = True
                            deleted_node = deleted_node.parent
                        else:
                            if not (sibling_node.left is not None and sibling_node.left.red):
                                if sibling_node.right is not None:
                                    sibling_node.right.red = False
                                sibling_node.red = True
                                self.rotate_left(sibling_node)
                                sibling_node = deleted_node.parent.left
                                self.color_flip_counter += 3

                            sibling_node.red = deleted_node.parent.red
                            deleted_node.parent.red = False
                            if sibling_node.left is not None:
                                sibling_node.left.red = False
                            self.rotate_right(deleted_node.parent)
                            deleted_node = self.root
                            self.color_flip_counter += 1

            else:
                break

        if deleted_node is not None:
            deleted_node.red = False
            self.color_flip_counter += 1

    # Find the node with the minimum bookID in the subtree rooted at node x.
    def minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    # Find the requested book in the tree.
    def find(self, val):
        result = self._find_recursive(self.root, val)
        return result if result != self.nil else None

    def _find_recursive(self, node, val):

        if node == self.nil or val == node.Book.bookID:
            return node
        elif val < node.Book.bookID:
            return self._find_recursive(node.left, val)
        else:
            return self._find_recursive(node.right, val) if node != self.nil else self.nil

    # rotate left at node x
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is not None:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        elif x.parent is None:
            self.root = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is not None:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        elif x.parent is None:
            self.root = y
        y.right = x
        x.parent = y

    # Fix the Red-Black Tree properties after insertion to ensure that all properties are maintained.
    def fix_insert(self, new_node):
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left  # uncle
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent

                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_left(new_node.parent.parent)

            else:
                u = new_node.parent.parent.right  # uncle
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_right(new_node.parent.parent)

        self.root.red = False
        self.color_flip_counter += 2

    # Finds and returns a list of nodes representing books closest to the given bookID (targetID).
    def find_closest(self, targetID):
        closest_books = []
        self._find_closest_recursive(self.root, targetID, float('inf'), closest_books)
        return closest_books

    def _find_closest_recursive(self, node, targetID, closest_distance, closest_books):
        if node != self.nil:
            current_distance = abs(node.Book.bookID - targetID)

            if current_distance < closest_distance:
                closest_books.clear()  # Clear the list with a closer book
                closest_books.append(node)  # Update the list with the closer book
                closest_distance = current_distance
            elif current_distance == closest_distance:
                closest_books.append(node)  # Add another book at equidistance

            if targetID < node.Book.bookID:
                self._find_closest_recursive(node.left, targetID, closest_distance, closest_books)
            elif targetID > node.Book.bookID:
                self._find_closest_recursive(node.right, targetID, closest_distance, closest_books)
            else:
                # If targetID is equal to the current node's bookID, no need to traverse further
                return

    # Count of color flips that occurred during insertions and deletions.
    def color_flip_count(self):
        return self.color_flip_counter

    # To read value of book in tree in the correct order
    def in_order_traversal(self):
        return self._in_order_traversal_recursive(self.root)

    def _in_order_traversal_recursive(self, node):
        if node != self.nil:
            yield from self._in_order_traversal_recursive(node.left)
            yield node
            yield from self._in_order_traversal_recursive(node.right)