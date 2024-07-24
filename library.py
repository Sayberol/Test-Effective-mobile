from abc import ABC, abstractmethod
import json, os

STATUS_IN_STOCK = "в наличии"
STATUS_GIVEN = "выдана"

class BookDto:
    def __init__(self, id, title, author, year, status):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }
    

class LibraryRepository(ABC):

    @abstractmethod
    def get_all_books(self) -> list[BookDto]:
        """
        Возвращает список всех книг.
        """
        pass

    @abstractmethod
    def overwrite_all_books(self, books: list[BookDto]):
        """
        Перезаписать все книги.
        """
        pass


class LibraryRepositoryLocalFile(LibraryRepository):
    def is_json_file_empty(self, file_path)-> bool:

        try:
            with open(file_path, "r") as f:
                json.load(f)
            return False
        except json.JSONDecodeError:
            return True
        
    def get_all_books(self)-> list[BookDto]:
        """
        Raises:
            FileExistsError
        """
        if not os.path.exists("data.json"):
            raise FileNotFoundError("Файл data.json не найден")
        
        if self.is_json_file_empty("data.json"):
            return []

        with open("data.json", "r") as file:
            books_dict = json.load(file)

        books_dto = []
        for book_dict in books_dict:
            books_dto.append(BookDto(*book_dict.values()))
        return books_dto


    def overwrite_all_books(self, books: list[BookDto]):
        """
        Raises:
            FileExistsError
        """

        books_dict = []
        for book in books:
            books_dict.append(book.to_dict())

        books_json = json.dumps(books_dict, indent=4)

        with open("data.json", "w") as f:
            f.write(books_json)

            
class Library():
    def __init__(self, repository: LibraryRepository = LibraryRepositoryLocalFile()):
        self._repository = repository

    def get_all_books(self) -> list[BookDto]:
        """
        Возвращает список всех книг.

        Raises:
            FileExistsError
        """
        return self._repository.get_all_books()
        
    def get_book_by_id(self, book_id: int) -> BookDto:
        """
        Возвращает книгу по ID.

        Raises:
            KeyError, FileExistsError
        """
        books = self.get_all_books()

        for book in books:
            if book.id == book_id:
                return book
        raise KeyError(f"Книга с таким ID: {book_id} не найдена")
    
    def add_book(self, title: str, author: str, year: int)-> int:
        """
        Добавляет новую книгу в файл

        Raises:
            ValueError, FileExistsError
        """

        if not title or not author or not year:
            raise ValueError("Неверные данные книги: Отсутствуют необходимые поля.")
        
        books = self.get_all_books()

        # Генерация уникального ID
        if not books:
            next_id = 1
        else:
            next_id = max(book.id for book in books) + 1

        books.append(BookDto(next_id, title, author, year, status=STATUS_IN_STOCK))

        self._repository.overwrite_all_books(books)

        return next_id
    
    def update_book_status(self, book_id: int):
        """
        Изменить книгу в файле

        Raises:
            KeyError, FileExistsError
        """

        books = self.get_all_books()

        for book in books:
            if book.id == book_id:
                if book.status == STATUS_IN_STOCK:
                    book.status = STATUS_GIVEN
                else:
                    book.status = STATUS_IN_STOCK
                self._repository.overwrite_all_books(books)
                return book.status
        raise KeyError(f"Книга с таким ID: {book_id} не найдена")

    def delete_book(self, book_id: int):
        """
        Удалить книгу из файла
        Raises:
            KeyError, FileExistsError
        """
        
        books = self.get_all_books()

        book_to_delete = None
        for book in books:
            if book.id == book_id:
                book_to_delete = book
                break

        if not book_to_delete:
            raise KeyError(f"Книга с таким ID: {book_id} не найдена")
        
        books.remove(book_to_delete)

        self._repository.overwrite_all_books(books)
            