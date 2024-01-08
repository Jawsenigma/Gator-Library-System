**GatorLibrary**  

**Problem Statement**  
Implement GatorLibrary, a fictional library management system, to efficiently manage books, patrons, and borrowing operations. The system uses a Red-Black tree for book management and Binary Min-Heaps for book reservations. Supported operations include print, insert, borrow, return, delete, find closest book, and color flip count in the Red-Black tree.

**Command To Run**  
Use the following command to run the project. Provide the input file as an argument.  
_python3 gatorLibrary.py <input_file>_

**Program Structure**  
The program is structured using a Red-Black Tree (RBT) and a Binary Min Heap.

**Red-Black Tree**    
**RedBlackNode**: Represents a node in the Red-Black Tree.  
**RBTree**: Implements the Red-Black Tree with methods like Insert, Delete, Find, Find Closest, Rotate Left, Rotate Right, and more.

**Binary Min Heap**  
**MinHeap**: Implements a Binary Min Heap with methods for insertion, extraction of minimum element, and building the heap.

**Gator Library Implementation**  
**GatorLibrary**: Manages books using a Red-Black Tree. Includes methods for inserting, printing, borrowing, returning, deleting, finding the closest book, and obtaining the color flip count.  
**Book**: Represents a book, including information like bookID, bookName, authorName, availabilityStatus, and borrower details.  
**Patron**: Represents a patron with a unique patronID.


**Implementation Details**  
The Gator Library system is implemented using classes such as RedBlackNode, RBTree, MinHeap, GatorLibrary, Book, and Patron. Each class has specific methods to perform various operations, ensuring efficient book management and patron interactions.

**How to Use**  
Run the program with the provided command, specifying an input file.
The program processes commands from the input file, executing operations like inserting books, printing details, borrowing, returning, deleting, finding the closest book, and obtaining color flip counts.
Output is written to an output file.
Feel free to explore the source code for more details on the implementation of each class and their methods.

For any issues or questions, please feel free to contact.






