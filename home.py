import json
import random
from collections import deque

# --- Load the Bible JSON ---
with open("KJV.json", "r", encoding="utf-8") as file:
    data = json.load(file)

books = data["books"]

# --- Search History (Queue) ---
search_history = deque(maxlen=10)

def add_to_history(keyword):
    search_history.append(keyword)

def show_history():
    print("\n📜 Search History:")
    if not search_history:
        print("No searches yet.")
    else:
        for i, keyword in enumerate(search_history, start=1):
            print(f"{i}. {keyword}")

# --- Bookmarks (Hash Table / Dict) ---
bookmarks = {}

def add_bookmark(ref, verse_text):
    bookmarks[ref] = verse_text
    print(f"✅ Bookmarked {ref}!")

def show_bookmarks():
    print("\n📌 Bookmarked Verses:")
    if not bookmarks:
        print("No bookmarks yet.")
        return
    for ref, verse_text in bookmarks.items():
        print(f"{ref} - {verse_text[:100]}{'...' if len(verse_text) > 100 else ''}")

# --- Display all books ---
def list_books():
    print("\n=== LIST OF BIBLE BOOKS ===")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['name']}")

# --- Display a chapter (all verses) ---
def show_chapter(book_index, chapter_index):
    book = books[book_index]
    book_name = book["name"]
    chapters = book["chapters"]

    if not (0 <= chapter_index < len(chapters)):
        print("❌ Chapter out of range!")
        return

    chapter = chapters[chapter_index]
    verses = chapter["verses"]

    print(f"\n📖 {book_name} Chapter {chapter['chapter']}")
    print("-" * 40)
    for verse in verses:
        print(f"{verse['verse']}. {verse['text']}")
    print("-" * 40)
    print(f"Total verses: {len(verses)}")

# --- Display a single verse ---
def show_verse(book_index, chapter_index, verse_index):
    book = books[book_index]
    chapter = book["chapters"][chapter_index]
    verses = chapter["verses"]

    if not (0 <= verse_index < len(verses)):
        print("❌ Verse out of range!")
        return

    verse = verses[verse_index]
    ref = f"{book['name']} {chapter['chapter']}:{verse['verse']}"
    print(f"\n📖 {ref} - {verse['text']}")
    return ref, verse['text']

# --- Search verses ---
def search_verse(keyword):
    print(f"\n🔍 Searching for: '{keyword}' ...")
    add_to_history(keyword)
    results = []
    for book_index, book in enumerate(books):
        for chap_index, chapter in enumerate(book["chapters"], start=1):
            for verse_obj in chapter["verses"]:
                verse_text = verse_obj["text"]
                verse_num = verse_obj["verse"]
                if keyword.lower() in verse_text.lower():
                    ref = f"{book['name']} {chapter['chapter']}:{verse_num}"
                    results.append((book_index, chap_index, ref, verse_text))
    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} result(s):\n")
    for i, (book_index, chap, ref, verse_text) in enumerate(results, start=1):
        print(f"{i}. {ref} - {verse_text[:100]}{'...' if len(verse_text) > 100 else ''}")

    # Ask user if they want to open a book/chapter from results
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

# --- Verse of the Day ---
def verse_of_the_day():
    book = random.choice(books)
    chapter = random.choice(book["chapters"])
    verse = random.choice(chapter["verses"])
    print(f"\n📖 Verse of the Day: {book['name']} {chapter['chapter']}:{verse['verse']}")
    print(verse["text"])

# --- Main Program Loop ---
def main():
    print("=== Terminal-Based Bible App ===")
    while True:
        print("\nOptions:")
        print("1. List all books")
        print("2. Search for a verse")
        print("3. Open a book, chapter, and verse")
        print("4. Verse of the Day")
        print("5. Show search history")
        print("6. Show bookmarks")
        print("7. Quit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":
            list_books()

        elif choice == "2":
            keyword = input("Enter a word or phrase to search for: ").strip()
            if keyword:
                search_verse(keyword)
            else:
                print("❌ Please enter a keyword.")

        elif choice == "3":
            # --- Select Book ---
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

            # --- Select Chapter ---
            print(f"This book has {len(book['chapters'])} chapters.")
            chapter_choice = input(f"Enter chapter number (1 - {len(book['chapters'])}): ")
            if not chapter_choice.isdigit():
                print("❌ Invalid chapter!")
                continue
            chapter_index = int(chapter_choice) - 1
            if not (0 <= chapter_index < len(book['chapters'])):
                print("❌ Chapter out of range!")
                continue
            chapter = book["chapters"][chapter_index]
            print(f"This chapter has {len(chapter['verses'])} verses (1 - {len(chapter['verses'])})")

            # --- Select Verse ---
            verse_choice = input(f"Enter verse number (1 - {len(chapter['verses'])}): ")
            if not verse_choice.isdigit():
                print("❌ Invalid verse!")
                continue
            verse_index = int(verse_choice) - 1
            ref, verse_text = show_verse(book_index, chapter_index, verse_index)

            # --- Ask to Bookmark ---
            bookmark_choice = input("\nDo you want to bookmark this verse? (y/n): ").lower()
            if bookmark_choice == 'y':
                add_bookmark(ref, verse_text)

        elif choice == "4":
            verse_of_the_day()

        elif choice == "5":
            show_history()

        elif choice == "6":
            show_bookmarks()

        elif choice == "7":
            print("👋 Exiting program. God bless!")
            break

        else:
            print("❌ Invalid choice! Please choose 1–7.")

# --- Run the program ---
if __name__ == "__main__":
    main()
