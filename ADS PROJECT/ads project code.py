# importing the libararies required
import sys
import time
import heapq

class MinHeapNode:
    def __init__(self, patronID, priority, timestamp):
        self.patronID = patronID
        self.priority = priority
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority
    
# gator library consists of books that has id, name, author name, availability status , who borrowed, and who are in queue
class BookNode:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None, reservationHeap=None):
        # intializing
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        if reservationHeap is None:
            self.reservationHeap = []
        else:
            self.reservationHeap = reservationHeap

class ReadBlacktreeNode:
    def __init__(self, bookNode,minheapNode):
        self.bookNode = bookNode
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1  # 1=red , 0 = black
        self.min_heap_node = minheapNode
        
class RedBlackTree:
    def __init__(self):
        self.nil = ReadBlacktreeNode(None,None)
        self.root = self.nil
        self.ColorFlipCount = 0
        self.nil.left = None
        self.nil.right = None
        self.nil.color = 0

    # Functions for help like left rotation and right rotation
    def Left_Rotation(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    # Right rotation in Red-Black Tree
    def Right_Rotation(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    # insertion of nodes
    def Insert(self, z):
        
        y = self.nil
        x = self.root

        while x != self.nil:
            y = x
            if z.bookNode.bookID < x.bookNode.bookID:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y == self.nil:
            self.root = z
        elif z.bookNode.bookID < y.bookNode.bookID:
            y.left = z
        else:
            y.right = z

        z.left = self.nil
        z.right = self.nil
        z.color = 'RED'
        self.insert_fixup(z)
        if z != self.root:
            self.ColorFlipCount += 1


    def insert_fixup(self, z):
        while z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                    self.ColorFlipCount += 1
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.Left_Rotation(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self.Right_Rotation(z.parent.parent)
                    self.ColorFlipCount += 2
            else:
                y = z.parent.parent.left
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                    self.ColorFlipCount += 1
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.Right_Rotation(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self.Left_Rotation(z.parent.parent)
                    self.ColorFlipCount += 2

        self.root.color = 'BLACK'
    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent != z:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self.delete_fixup(x)  
            if x != self.nil and x != self.root:
                self.ColorFlipCount -= 1


    def delete_fixup(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.Left_Rotation(x.parent)
                    w = x.parent.right
                    self.ColorFlipCount += 1
                if w.left.color == 'BLACK' and w.right.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.right.color == 'BLACK':
                        w.left.color = 'BLACK'
                        w.color = 'RED'
                        self.Right_Rotation(w)
                        w = x.parent.right
                        self.ColorFlipCount += 1
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.right.color = 'BLACK'
                    self.Left_Rotation(x.parent)
                    self.ColorFlipCount += 1
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.Right_Rotation(x.parent)
                    w = x.parent.left
                    self.ColorFlipCount += 1
                if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                    self.ColorFlipCount += 1
                else:
                    if w.left.color == 'BLACK':
                        w.right.color = 'BLACK'
                        w.color = 'RED'
                        self.Left_Rotation(w)
                        w = x.parent.left
                        self.ColorFlipCount += 1
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.left.color = 'BLACK'
                    self.Right_Rotation(x.parent)
                    x = self.root
                    self.ColorFlipCount += 1

        x.color = 'BLACK'
        if x != self.nil and x.color == 'BLACK':
            self.ColorFlipCount += 1
        if x.parent != self.nil and x.parent.color == 'BLACK':
            self.ColorFlipCount += 1

    def tree_minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x
    def rb_transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
   

    def FindClosestBook(self, targetID):
        # Closest book checking
        current_node = self.root
        closest_book = None

        while current_node != self.nil:
            if current_node.bookNode.bookID == targetID:
                return current_node

            if closest_book is None or abs(current_node.bookNode.bookID - targetID) < abs(closest_book.bookNode.bookID - targetID):
                closest_book = current_node

            if targetID < current_node.bookNode.bookID:
                current_node = current_node.left
            else:
                current_node = current_node.right

        return closest_book

class GatorLibrary:
    def __init__(self):
        self.red_black_tree = RedBlackTree()
        self.reservation_limit = 20
    #inserting all the deatils and checking if the book is available or borrowed by someone
    def InsertBook(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None, reservationHeap=None):
        if availabilityStatus != "Yes" and availabilityStatus != "No":
            print("Availability status should be 'Yes' or 'No'. Defaulting to 'Yes'.")
            availabilityStatus = "Yes"
        timestamp = time.time()  
        minheap_node = MinHeapNode(patronID=None, priority=None, timestamp=timestamp)
        new_book = BookNode(bookID, bookName, authorName, availabilityStatus, borrowedBy, reservationHeap)
        new_node = ReadBlacktreeNode(new_book, minheap_node)
        self.red_black_tree.Insert(new_node)
    
    # function to check if the book is borrowed by someone
    def BorrowBook(self, patronID, bookID, patronPriority):
        node = self.FindClosestBook(bookID)
        if node and node.bookNode.bookID == bookID:
            book = node.bookNode
            if book.availabilityStatus:
                book.availabilityStatus = False
                book.borrowedBy = patronID
                print(f"Book {bookID} borrowed by Patron {patronID}")
            else:
                reserved_patrons = [res[2].patronID for res in book.reservationHeap]
                if patronID in reserved_patrons:
                    print(f"Book {bookID} borrowed by Patron {patronID}")
                    index = reserved_patrons.index(patronID)
                    _, _, reservation = book.reservationHeap.pop(index)
                    book.availabilityStatus = False
                    book.borrowedBy = patronID
                    print(f"Book {bookID} allotted to Patron {patronID}")
                else:
                    new_reservation = (patronPriority, time.time(), MinHeapNode(patronID, patronPriority, time.time()))
                    heapq.heappush(book.reservationHeap, new_reservation)
                    print(f"Book {bookID} reserved by Patron {patronID}")
        else:
            print(f"Book {bookID} not found in the library")

    def ReturnBook(self, patronID, bookID):
        node = self.FindClosestBook(bookID)
        if node and node.bookNode.bookID == bookID:
            book = node.bookNode
            if not book.availabilityStatus and book.borrowedBy == patronID:
                book.availabilityStatus = True
                book.borrowedBy = None
                if book.reservationHeap:
                    reserved_patrons = [res[2].patronID for res in book.reservationHeap]
                    if patronID in reserved_patrons:
                        _, _, reservation = heapq.heappop(book.reservationHeap)
                        book.availabilityStatus = False
                        book.borrowedBy = reservation.patronID
                        print(f"Book {bookID} allotted to Patron {reservation.patronID}")
                    else:
                        print(f"Book {bookID} returned by Patron {patronID}")
                        while book.reservationHeap:
                            _, _, reservation = heapq.heappop(book.reservationHeap)
                            if reservation.patronID in reserved_patrons:
                                book.availabilityStatus = False
                                book.borrowedBy = reservation.patronID
                                print(f"Book {bookID} allotted to Patron {reservation.patronID}")
                                break
                        else:
                            book.availabilityStatus = True
                            print(f"Book {bookID} returned by Patron {patronID}")
                else:
                    print(f"Book {bookID} returned by Patron {patronID}")
            else:
                print(f"Book {bookID} is not borrowed by Patron {patronID} or not found")
        else:
            closest_book = self.FindClosestBook(bookID)
            if closest_book and closest_book.bookNode.bookID != bookID:
                closest_book = closest_book.bookNode
                print(f"BookID = {closest_book.bookID}")
                print(f"Title = {closest_book.bookName}")
                print(f"Author = {closest_book.authorName}")
                print(f"Availability = {'Yes' if closest_book.availabilityStatus else 'No'}")
                print(f"BorrowedBy = {closest_book.borrowedBy if closest_book.borrowedBy else 'None'}")
                print(f"Reservations = {closest_book.reservationHeap}")
                print(f"Book {bookID} not found in the library")

    
    # Checks the closest book for the given ID and print the details of that book
    def FindClosestBook(self, targetID, print_details=False):
        current_node = self.red_black_tree.root
        closest_book = None
        min_diff = float('inf')  

        while current_node != self.red_black_tree.nil:
            if current_node.bookNode.bookID == targetID:
                if print_details:
                    self.PrintBook(targetID)
                return current_node
            if abs(current_node.bookNode.bookID - targetID) < min_diff:   #  closest book is identified based on comparison of book IDs
                min_diff = abs(current_node.bookNode.bookID - targetID)
                closest_book = current_node
            if targetID < current_node.bookNode.bookID: #Traversing left or right based on the target ID
                current_node = current_node.left
            else:
                current_node = current_node.right
        if closest_book is None:                      #Checking  if the target ID is smaller than the smallest book ID
            closest_book = self.red_black_tree.root
            if print_details:
                self.PrintBook(closest_book.bookNode.bookID)
            return closest_book
        if closest_book and print_details:           # Check what details need to be printed for the book closest found
            self.PrintBook(closest_book.bookNode.bookID)

        return closest_book
    
    # implenmenattaion of delete book function based on given book ID
    def DeleteBook(self, bookID, print_details=False):
        node = self.FindClosestBook(bookID, print_details=print_details)
        if node and node.bookNode.bookID == bookID:
            book = node.bookNode
            self.red_black_tree.delete(node)
            if book.reservationHeap:
                reserved_patrons = [res[2].patronID for res in book.reservationHeap]
                for _, _, reservation in book.reservationHeap:
                    print(f"Notifying Patron {reservation.patronID}: The book {bookID} is no longer available")
                book.reservationHeap = []
                print(f"Book {bookID} is deleted from the library. Reservations made by Patrons {', '.join(map(str, reserved_patrons))} have been cancelled!")
            else:
                print(f"Book {bookID} is deleted from the library.")
#             if print_details:
#                 self.PrintBook(bookID)
        else:
            print(f"Book {bookID} not found in the library")
    

    # Calculates the color flip count
    def ColorFlipCount(self):
        return self.red_black_tree.ColorFlipCount
        
    

# printing deatails of the books based on given ID
    def PrintBook(self, bookID):
        # Implementation of PrintBook method
        node = self.red_black_tree.FindClosestBook(bookID)
        if node and node.bookNode.bookID == bookID:
            book = node.bookNode
            print(f"BookID = {book.bookID}")
            print(f"Title = {book.bookName}")
            print(f"Author = {book.authorName}")
            print(f"Availability = {'Yes' if book.availabilityStatus else 'No'}")
            print(f"BorrowedBy = {book.borrowedBy if book.borrowedBy else 'None'}")
            print(f"Reservations = {[res[2].patronID for res in book.reservationHeap]}")
        else:
            print(f"Book {bookID} not found in the Library")

    # print all the books that are in the given range of ID's
    def PrintBooks(self, bookID1, bookID2):
        for bookID in range(bookID1, bookID2 + 1):
            node = self.FindClosestBook(bookID)
            if node and node.bookNode.bookID == bookID:
                self.PrintBook(bookID)
    
    # call of the program
    def Quit(self):
        print("Program Terminated")
    

#main function
if __name__ == "__main__":
    input_file_path = 'INPUT.txt'  
    output_file_path = 'OUTPUT.txt' 

    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    with open(output_file_path, 'w') as output_file:
        original_stdout = sys.stdout  
        sys.stdout = output_file  # Redirect stdout to the output file

        library = GatorLibrary()

        # Process each line of input from the file
        for line in lines:
            command = line.strip()
            try:
                exec(f"library.{command}")
                
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
            # exec(command)

        sys.stdout = original_stdout  # Restore original stdout
    
    print("Output Sent to", output_file_path)