from langchain_gigachat.chat_models import GigaChat
from pathlib import Path
import logging
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
logging.basicConfig(level=logging.DEBUG)


def generate_neuro_texts(
    author: str,
    root_dir: Path | str,
    desired_size: int,
    n_books: int,
    prompt: str,
    series_list: list[str],
    intermediate_files: Path | str | None,
) -> None:

    for series in series_list:
        series_folder = Path(root_dir, f"{series}_txt")
        series_folder.mkdir(exist_ok=True)

        for _ in range(n_books):
            logging.info(f"Current_book: {_}")
            current_size = 0
            indx = 0
            book_content = []
            while current_size < desired_size:
                giga = GigaChat(
                    credentials=API_KEY,
                    verify_ssl_certs=False,
                )

                try:
                    resp = giga.invoke(prompt)
                except Exception as e:
                    logging.warning(e)
                    continue

                current_size += len(resp.content)
                fragment_name = f"{author}_{series}_{indx}.txt"
                if intermediate_files is not None:
                    with open(
                        Path(Path(intermediate_files), fragment_name), "w"
                    ) as file:
                        file.write(resp.content)

                indx += 1
                book_content.append(resp.content)
                logging.info(current_size)

                time.sleep(1)

            full_book_text = " ".join(book_content)
            book_number = str(
                get_latest_number_of_generated_book(Path(series_folder)) + 1
            )
            if len(book_number) < 2:
                book_number = "0" + book_number
            book_name = f"{author}_{series}_{book_number}.txt"

            with open(Path(series_folder, book_name), "w") as file:
                file.write(full_book_text)

            print(f"Saved book to {str(Path(series_folder, book_name))}")


def get_latest_number_of_generated_book(path_to_dir: Path) -> int:
    list_of_files = [
        int(p.name.split("_")[-1].split(".")[0]) for p in path_to_dir.iterdir()
    ]
    if not list_of_files:
        return -1
    return max(list_of_files)


if __name__ == "__main__":
    author = "DontsovaDaria"
    root_dir = "/home/team/text_input/DD_txt"
    desired_size = 500000
    n_books = 2
    prompt = "Сгенерируй текст в стиле Дарьи Донцовой максимального размера. Отправь только результат генерации"
    series_list = ["Neuro_Dontsova"]

    generate_neuro_texts(author, root_dir, desired_size, n_books, prompt, series_list)
