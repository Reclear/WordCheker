from pathlib import Path

def load_words() -> list[str]:

    result = []
    file = Path("list.txt")

    if file.exists() is False:
        return result

    with file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.replace("\n","")
            result.append(line)
        f.close()

    return result