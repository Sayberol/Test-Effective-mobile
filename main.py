from library import Library, BookDto

def command_list():
    """
    Возвращает строку со списком команд.
    """
    command_list = [
        "help:          Отображает список команд",
        "add:           Добавить книгу",
        "delete:        Удалить книгу",
        "find:          Найти книгу",
        "show:          Отобразить все книги",
        "update_status: Изменить статус книги",
        "exit:          Выход",
    ]

    command_list_string = f"\nСписок доступных команд:\n"
    for command in command_list:
        command_list_string += f"{command}\n"

    return command_list_string

def print_book(book: BookDto):
    print(f"ID: {book.id}\nАвтор: {book.author}\nНазвание книги: {book.title}\nГод: {book.year}\nСтатус: {book.status}\n")

def main():
    library = Library()

    print(command_list())

    while True:

        choice = input("Введите команду: ")
        try:
            match choice:
                    case "add":
                        title = input("Название книги: ")
                        author = input("Автор книги: ")
                        year = int(input("Год издания: "))
                        book_id = library.add_book(title, author, year)
                        print(f"Книга сохранена с ID: {book_id}")
                    case "delete":
                        book_id = int(input("ID книги: "))
                        library.delete_book(book_id)
                        print("Книга удалена")
                    case "find":
                        book_id = int(input("ID книги: "))
                        found_book = library.get_book_by_id(book_id)
                        print_book(found_book)
                    case "show":
                        all_books = library.get_all_books()
                        if not all_books:
                            print("Книги отсутствют")
                        for book in all_books:
                            print_book(book)
                    case "update_status":
                        book_id = int(input("ID книги: "))
                        new_status = library.update_book_status(book_id)
                        print(f"Новый статус: {new_status}")
                    case "exit":
                        break
                    case "help":
                        print(command_list())
                    case _:
                        print("Неверная команда.")
        except Exception as e:
            print(f"Ошибка: {e}")
if __name__ == "__main__":
    main()