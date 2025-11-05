import json

# Load the Bible JSON
with open("KJV.json", "r", encoding="utf-8") as file:
    data = json.load(file)

books = data["books"]

# --- Function to display all books ---
def list_books():
    print("=== LIST OF BIBLE BOOKS ===")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['name']}")

# --- Function to show all verses of a chapter ---
def show_chapter(book_index, chapter_index):
    book = books[book_index]
    book_name = book["name"]
    chapters = book["chapters"]

    if not (0 <= chapter_index < len(chapters)):
        print("❌ Chapter out of range!")
        return

    verses = chapters[chapter_index]
    print(f"\n📖 {book_name} Chapter {chapter_index + 1}")
    print("-" * 40)
    for i, verse_text in enumerate(verses, start=1):
        print(f"{i}. {verse_text}")
    print("-" * 40)
    print(f"Total verses: {len(verses)}")

# --- Function to search for a word or phrase ---
def search_verse(keyword):
    print(f"\n🔍 Searching for: '{keyword}' ...")
    results = []
    for book_index, book in enumerate(books):
        for chap_index, chapter in enumerate(book["chapters"], start=1):
            for verse_index, verse in enumerate(chapter, start=1):
                if keyword.lower() in verse.lower():
                    ref = f"{book['name']} {chap_index}:{verse_index}"
                    results.append((book_index, chap_index, ref, verse))
    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} result(s):\n")
    for i, (book_index, chap, ref, verse_text) in enumerate(results, start=1):
        print(f"{i}. {ref} - {verse_text[:100]}{'...' if len(verse_text)>100 else ''}")

    # Ask user if they want to open a book/chapter from the results
    open_choice = input("\nDo you want to open one of these results? (y/n): ").lower()
    if open_choice == 'y':
        list_books()
        book_choice = input("\nEnter the book number you want to open: ")
        if not book_choice.isdigit():
            print("❌ Invalid book number!")
            return
        book_index = int(book_choice) - 1
        book = books[book_index]
        print(f"\n✅ You selected: {book['name']}")
        print(f"This book has {len(book['chapters'])} chapters.")
        chapter_choice = input(f"Enter the chapter number (1 - {len(book['chapters'])}): ")
        if not chapter_choice.isdigit():
            print("❌ Invalid chapter number!")
            return
        chapter_index = int(chapter_choice) - 1
        show_chapter(book_index, chapter_index)

# --- Main Program Loop ---
def main():
    print("=== Terminal-Based Bible App ===")
    while True:
        print("\nOptions:")
        print("1. List all books")
        print("2. Search for a verse")
        print("3. Open a book and chapter")
        print("4. Quit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            list_books()

        elif choice == "2":
            keyword = input("Enter a word or phrase to search for: ").strip()
            if keyword:
                search_verse(keyword)
            else:
                print("❌ Please enter a keyword.")

        elif choice == "3":
            list_books()
            book_choice = input("\nEnter book number: ")
            if not book_choice.isdigit():
                print("❌ Invalid input!")
                continue
            book_index = int(book_choice) - 1
            if not (0 <= book_index < len(books)):
                print("❌ Book number out of range!")
                continue
            book = books[book_index]
            print(f"\n✅ You selected: {book['name']}")
            print(f"This book has {len(book['chapters'])} chapters.")
            chapter_choice = input(f"Enter chapter number (1 - {len(book['chapters'])}): ")
            if not chapter_choice.isdigit():
                print("❌ Invalid chapter!")
                continue
            chapter_index = int(chapter_choice) - 1
            show_chapter(book_index, chapter_index)

        elif choice == "4":
            print("👋 Exiting program. God bless!")
            break

        else:
            print("❌ Invalid choice! Please choose 1–4.")

# Hello Nard
