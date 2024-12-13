import json
import datetime

# File paths
BOOKS_FILE = "books.json"
LENDED_BOOKS_FILE = "lended_books.json"

# Load existing data from files
def load_books():
    try:
        with open(BOOKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def load_lended_books():
    try:
        with open(LENDED_BOOKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save books data to the JSON file
def save_books(books):
    with open(BOOKS_FILE, 'w') as file:
        json.dump(books, file, indent=4)

# Save lended books data to the JSON file
def save_lended_books(lended_books):
    with open(LENDED_BOOKS_FILE, 'w') as file:
        json.dump(lended_books, file, indent=4)

# Add new book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author(s): ")
    isbn = input("Enter ISBN: ")
    year = input("Enter publishing year: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    
    new_book = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "year": year,
        "price": price,
        "quantity": quantity
    }
    
    books = load_books()
    books.append(new_book)
    save_books(books)
    print(f"Book '{title}' added successfully.")

# View all books
def view_books():
    books = load_books()
    if books:
        for i, book in enumerate(books, start=1):
            print(f"{i}. {book['title']} by {book['author']}, ISBN: {book['isbn']}, Year: {book['year']}, Price: {book['price']}, Quantity: {book['quantity']}")
    else:
        print("No books available in the system.")

# Update book details
def update_book():
    view_books()
    book_index = int(input("Enter the book number to update: ")) - 1
    books = load_books()
    
    if 0 <= book_index < len(books):
        book = books[book_index]
        print("Leave empty to keep current value.")
        book['title'] = input(f"Enter new title (current: {book['title']}): ") or book['title']
        book['author'] = input(f"Enter new author(s) (current: {book['author']}): ") or book['author']
        book['isbn'] = input(f"Enter new ISBN (current: {book['isbn']}): ") or book['isbn']
        book['year'] = input(f"Enter new publishing year (current: {book['year']}): ") or book['year']
        book['price'] = float(input(f"Enter new price (current: {book['price']}): ") or book['price'])
        book['quantity'] = int(input(f"Enter new quantity (current: {book['quantity']}): ") or book['quantity'])
        
        save_books(books)
        print(f"Book '{book['title']}' updated successfully.")
    else:
        print("Invalid book number.")

# Remove a book
def remove_book():
    view_books()
    book_index = int(input("Enter the book number to remove: ")) - 1
    books = load_books()
    
    if 0 <= book_index < len(books):
        removed_book = books.pop(book_index)
        save_books(books)
        print(f"Book '{removed_book['title']}' removed successfully.")
    else:
        print("Invalid book number.")

# Lend a book
def lend_book():
    books = load_books()
    if not books:
        print("No books available to lend.")
        return
    
    book_title = input("Enter the title of the book to lend: ")
    book = next((b for b in books if b['title'].lower() == book_title.lower() and b['quantity'] > 0), None)
    
    if book:
        borrower_name = input("Enter borrower's name: ")
        borrower_phone = input("Enter borrower's phone number: ")
        due_date = datetime.datetime.now() + datetime.timedelta(days=14)
        due_date_str = due_date.strftime("%Y-%m-%d %H:%M:%S")
        
        lend_info = {
            "borrower_name": borrower_name,
            "borrower_phone": borrower_phone,
            "book_title": book_title,
            "due_date": due_date_str
        }
        
        lended_books = load_lended_books()
        lended_books.append(lend_info)
        save_lended_books(lended_books)
        
        # Update book quantity
        book['quantity'] -= 1
        save_books(books)
        
        print(f"Book '{book_title}' lent to {borrower_name}. Due date: {due_date_str}")
    else:
        print("There are not enough books available to lend.")

# Return a book
def return_book():
    lended_books = load_lended_books()
    if not lended_books:
        print("No books currently lent out.")
        return
    
    borrower_name = input("Enter borrower's name: ")
    book_title = input("Enter the title of the book being returned: ")
    
    lend_info = next((l for l in lended_books if l['borrower_name'].lower() == borrower_name.lower() and l['book_title'].lower() == book_title.lower()), None)
    
    if lend_info:
        # Remove the lend info
        lended_books.remove(lend_info)
        save_lended_books(lended_books)
        
        books = load_books()
        book = next(b for b in books if b['title'].lower() == book_title.lower())
        
        # Increase book quantity
        book['quantity'] += 1
        save_books(books)
        
        print(f"Book '{book_title}' returned successfully.")
    else:
        print("No record found for this book being lent.")

# Main menu
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Update Book")
        print("4. Remove Book")
        print("5. Lend Book")
        print("6. Return Book")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            update_book()
        elif choice == "4":
            remove_book()
        elif choice == "5":
            lend_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
