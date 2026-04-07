import re


def clean_text(raw_text):
    text = raw_text.strip()
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text


def get_multiline_input(prompt_message):
    print(prompt_message)
    print("=" * 50)
    print("Paste your text below. You can paste multiple lines.")
    print("When you are finished, type DONE on a new line and press Enter.")
    print("=" * 50)

    collected_lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().upper() == "DONE":
            break

        collected_lines.append(line)

    full_text = "\n".join(collected_lines)
    return full_text


def truncate_text(text, max_words=800):
    words = text.split()

    if len(words) <= max_words:
        return text

    truncated = " ".join(words[:max_words])
    truncated += "\n... [truncated for length]"

    return truncated


def extract_word_count(text):
    words = text.split()
    return len(words)


def read_from_file(file_path):
    import os

    file_path = file_path.strip().strip("'\"")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension not in (".txt", ".md", ".text"):
        raise ValueError(
            f"Unsupported file type: '{extension}'. "
            f"Please use a .txt file. You can copy-paste your resume "
            f"into a plain text file and try again."
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            raise ValueError("The file is empty. Please provide a file with content.")

        return content

    except UnicodeDecodeError:
        raise ValueError(
            "Could not read the file. It may contain special encoding. "
            "Please save it as a UTF-8 text file and try again."
        )
