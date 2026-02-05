class Book:
    def __init__(self, title: str, author: str, isbn: str):
        # Create the instance variables for title, author, and isbn here
        self._title = title
        self._author = author
        self._isbn = isbn
        self.available = True  # Initially, the book is available

    @property
    def title(self):
        return self._title

    @property
    def isbn(self):
        return self._isbn

    def borrow_book(self):
        # Remove the pass and write code for this method
        # (borrowing a book changes its availability)
        self.available = False

    def return_book(self):
        # Remove the pass and write code for this method
        self.available = True

    def __str__(self):
        # Remove the pass and write code for this method
        #  (printing a book should display its title, author, and isbn)
        return f"Book({self._title}, {self._author}, {self._isbn}, {self.available=})"


class DigitalBook(Book):
    valid_compatibility = {"PDF", "Kindle", "Apple"}

    def __init__(self, title: str, author: str, isbn: str):
        # Call the superclass constructor with title, author, and isbn
        super().__init__(title, author, isbn)
        self.available = True  # Made explicit in case 'Book' behaviour is changed.
        self.compatibility = {"Kindle"}

    def borrow_book(self):
        # Don't remove the pass
        # (borrowing a digital book doesn't change its availability)
        pass

    def return_book(self):
        # Don't remove the pass (same as borrow_book)
        pass

    def __str__(self):
        # Remove the pass and write code for this method
        # (printing a digital book should also display its compatibility)
        return f"Book({self._title}, {self._author}, {self._isbn}, {self.compatibility=}, {self.available=}"


class Library:
    def __init__(self):
        self.books: list[Book] = []

    def add_book(self, book: Book):
        # Remove the pass and write code for this method
        self.books.append(book)

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                # Remove the pass and write code for this method
                # (check if the book is available, then call its borrow method)
                book.borrow_book()
                break

    def return_book(self, isbn):
        # Remove the pass and write code for this method, see borrow_book
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                break

    def __str__(self):
        # Remove the pass and write code for this method
        # (printing a library should display its books and their details)
        book_str = "\n".join(str(book) for book in self.books)
        return f"Library({book_str})"


def test_book():
    book = Book("Frankenstein", "Mary Shelley", "978-0486282114")
    # Try the methods of the Book class here and print the book object
    book.borrow_book()
    print(book)
    book.return_book()
    print(book)


def test_digital_book():
    digital_book = DigitalBook(
        "Orlando: A Biography", "Virginia Woolf", "978-0156031516"
    )
    # Try the methods here and print it
    digital_book.borrow_book()
    print(digital_book)
    digital_book.return_book()
    print(digital_book)


def test_library():
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
    book2 = Book("1984", "George Orwell", "978-0451524935")
    book3 = Book("Jane Eyre", "Charlotte Bronte", "978-0141441146")
    book4 = DigitalBook("1984", "George Orwell", "978-0451524935")

    library = Library()
    # Add the books to the library here and try borrowing and returning them
    # Remember to print the library object at each step
    library.add_book(book1)
    print(library)
    library.add_book(book2)
    print(library)
    library.add_book(book3)
    print(library)
    library.add_book(book4)
    print(library)
    library.borrow_book("978-0451524935")
    print(library)
    library.return_book("978-0451524935")
    print(library)


test_library()
