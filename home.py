import json

# --- Load the Bible JSON ---
with open("KJV.json", "r", encoding="utf-8") as file:
    data = json.load(file)

books = data["books"]

# --- Function to display all books ---
def list_books(show_only=False):
    print("\n=== LIST OF BIBLE BOOKS ===")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['name']}")
    if show_only:
        return

    choice = input("\nEnter a book number to view its chapters (or press Enter to go back): ").strip()
    if not choice:
        return
    if not choice.isdigit():
        print("❌ Invalid input! Please enter a number.")
        return

    book_index = int(choice) - 1
    if not (0 <= book_index < len(books)):
        print("❌ Book number out of range!")
        return

    book = books[book_index]
    print(f"\n✅ You selected: {book['name']}")
    print(f"This book has {len(book['chapters'])} chapters.")
    chap_choice = input(f"Enter a chapter number (1–{len(book['chapters'])}): ").strip()
    if not chap_choice.isdigit():
        print("❌ Invalid input!")
        return

    chapter_index = int(chap_choice) - 1
    show_chapter(book_index, chapter_index)

# --- Function to show all verses of a chapter ---
def show_chapter(book_index, chapter_index):
    book = books[book_index]
    book_name = book["name"]
    chapters = book["chapters"]

    if not (0 <= chapter_index < len(chapters)):
        print("❌ Chapter out of range!")
        return

    print(f"\n📖 {book_name} Chapter {chapter_index + 1}")
    print("-" * 40)

    chapter = chapters[chapter_index]
    # Detect structure type
    if isinstance(chapter, list):
        # Old format: list of verse strings
        for i, verse_text in enumerate(chapter, start=1):
            print(f"{i}. {verse_text}")
        total_verses = len(chapter)

    elif isinstance(chapter, dict) and "verses" in chapter:
        # New format: dict with "verses"
        for v in chapter["verses"]:
            verse_num = v.get("verse", 0)
            verse_text = v.get("text", "")
            print(f"{verse_num}. {verse_text}")
        total_verses = len(chapter["verses"])

    else:
        print("⚠️ Unknown chapter format.")
        return

    print("-" * 40)
    print(f"Total verses: {total_verses}")

# --- Function to search for a word or phrase ---
def search_verse(keyword):
    print(f"\n🔍 Searching for: '{keyword}' ...")
    results = []

    for book_index, book in enumerate(books):
        for chap_index, chapter in enumerate(book["chapters"], start=1):
            # Detect format
            if isinstance(chapter, list):
                for verse_index, verse_text in enumerate(chapter, start=1):
                    if keyword.lower() in verse_text.lower():
                        ref = f"{book['name']} {chap_index}:{verse_index}"
                        results.append((book_index, chap_index, verse_index, ref, verse_text))
            elif isinstance(chapter, dict) and "verses" in chapter:
                for v in chapter["verses"]:
                    verse_text = v.get("text", "")
                    verse_num = v.get("verse", 0)
                    if keyword.lower() in verse_text.lower():
                        ref = f"{book['name']} {chap_index}:{verse_num}"
                        results.append((book_index, chap_index, verse_num, ref, verse_text))

    if not results:
        print("No results found.")
        return

    print(f"\nFound {len(results)} result(s):\n")
    for i, (book_index, chap, verse_num, ref, verse_text) in enumerate(results, start=1):
        print(f"{i}. {ref} - {verse_text[:100]}{'...' if len(verse_text)>100 else ''}")

    open_choice = input("\nEnter the number of the verse you want to open (or press Enter to cancel): ").strip()
    if not open_choice:
        return
    if not open_choice.isdigit():
        print("❌ Invalid number!")
        return

    choice = int(open_choice)
    if not (1 <= choice <= len(results)):
        print("❌ Number out of range!")
        return

    book_index, chap_index, verse_num, ref, verse_text = results[choice - 1]
    print(f"\n✅ You chose: {ref}")
    print(f"→ \"{verse_text}\"\n")
    show_chapter(book_index, chap_index - 1)

# --- Main Program Loop ---
def main():
    print("=== Terminal-Based Bible App ===")
    while True:
        print("\nOptions:")
        print("1. List all books")
        print("2. Search for a verse")
        print("3. Open a book and chapter")
        print("4. Quit")

        choice = input("\nEnter your choice (1–4): ").strip()

        if choice == "1":
            list_books()  # Now interactive

        elif choice == "2":
            keyword = input("Enter a word or phrase to search for: ").strip()
            if keyword:
                search_verse(keyword)
            else:
                print("❌ Please enter a keyword.")

        elif choice == "3":
            list_books(show_only=True)
            book_choice = input("\nEnter book number: ").strip()
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
            chapter_choice = input(f"Enter chapter number (1–{len(book['chapters'])}): ").strip()
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

# --- Run the program ---
if __name__ == "__main__":
    main()
