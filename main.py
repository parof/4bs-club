import json
from typing import Optional
from enum import Enum
from tabulate import tabulate

class Status(Enum):
    READ = "read"
    NEXT = "next"
    READING = "reading"

    @classmethod
    def from_string(cls, status_string: str) -> 'Status':
        for status in cls:
            if status.value == status_string:
                return status
        raise ValueError(f"'{status_string}' is not a valid {cls.__name__}")

class Rating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    @classmethod
    def from_int(cls, r: int) -> 'Rating':
        if not isinstance(r, int):
            raise ValueError(f"Values for {cls.__name__} must be integers")
        if not 1 <= r <= 5:
            raise ValueError(f"'{r}' is not a valid {cls.__name__}")
        else:
            match r:
                case 1: return cls.ONE
                case 2: return cls.TWO
                case 3: return cls.THREE
                case 4: return cls.FOUR
                case 5: return cls.FIVE
        raise ValueError('Unreachable')

    def __str__(self):
        return '⭐' * self.value + '🌑' * (5 - self.value)

class BookClubEntry:
    def __init__(self, title: str, author: str, genre: str, proposed_by: str, link: str, session: Optional[str], status: Status, rating: Optional[Rating]):
        self.title = title
        self.author = author
        self.genre = genre
        self.proposed_by = proposed_by
        self.link = link
        self.session = session
        self.status = status
        self.rating = rating

    def __str__(self):
        return f"{self.title} by {self.author} ({self.genre}) - Proposed by {self.proposed_by} - Status: {self.status.value} - Session : {self.session if self.session else 'No Session'} - {self.rating.name if self.rating else 'No rating'} [{self.link}]"

class Library:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: BookClubEntry):
        self.entries.append(entry)

    def __str__(self):
        return '\n'.join(str(entry) for entry in self.entries)

    @staticmethod
    def from_json(file_path: str):
        # Open the JSON file and load the data
        with open(file_path, 'r') as file:
            data = json.load(file)

        if isinstance(data, list):
            library = Library()
            for record in data:
                try:
                    title = record['title']
                    author = record['author']
                    genre = record['genre']
                    proposed_by = record['proposed_by']
                    link = record['link']
                    session = record['session'] if 'session' in record else None
                    status = Status.from_string(record['status'])
                    rating = Rating.from_int(record['rating']) if 'rating' in record else None
                    library.add_entry(BookClubEntry(title, author, genre, proposed_by, link, session, status, rating))
                except KeyError as e:
                    raise KeyError(f"KeyError: Missing key {e} in record {record}")
            return library
        else:
            raise ValueError("Invalid JSON format. Expected a list of records.")


    def headers(self):
        headers = ["Title", "Author", "Genre", "Proposed By", "Status", "Session", "Rating", "Link"]
        return headers

    def table(self):
        table = []
        for entry in self.entries:
            table.append([
                entry.title,
                entry.author,
                entry.genre,
                entry.proposed_by,
                entry.status.value,
                entry.session if entry.session else "No Session",
                entry.rating if entry.rating else "No rating",
                entry.link
            ])
        return table

    def print_library(self) -> None:
        print(tabulate(self.table(), self.headers(), tablefmt="fancy_grid"))

    def print_library_to_markdown(self, path: str) -> None:
        table_format = "pipe"
        markdown_table = tabulate(self.table(), self.headers(), tablefmt=table_format)

        # Write the Markdown table to the file
        with open(path, "w") as file:
            file.write(markdown_table)


if __name__ == "__main__":
    path = 'entries.json'
    entries = Library.from_json(path)
    entries.print_library()
    entries.print_library_to_markdown("library.md")
