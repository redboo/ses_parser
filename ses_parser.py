import gzip
import os
import re
import shutil


def create_filename(name: str) -> str:
    counter, filename = 0, f"{name}.md"
    while os.path.exists(os.path.join("dist", filename)):
        counter += 1
        filename = f"{name}({counter}).md"
    return filename


def parse_ses(file_path: str, output_dir: str = "dist"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    with open(file_path, "r", encoding="utf-8") as f:
        write = False
        prev_file = ""

        for line in f:
            line = line.strip().replace("- ", "").rstrip("-")
            if line.endswith(","):
                line += " "

            if not line:
                continue

            if line == "А":
                write = True
                continue

            if line.startswith("НАСЕЛЁННЫЕ МОСКВА ы ©"):
                break

            if write:
                if match := re.search(r"^(?![А-Я](\.)? )[А-Я\-]+(?:\s[А-Я\-]+)*(?=[ ,]|\.\.)+", line):
                    upper = match.group()
                    title = upper.lower()
                    row = line.replace(upper, title).replace("- ", "-")
                    prev_file = file_name = create_filename(title.replace(" ", "_"))
                    with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
                        f.write(row)
                else:
                    with open(os.path.join(output_dir, prev_file), "a", encoding="utf-8") as f:
                        f.write(line.rstrip("-") if line.endswith("-") else line)


if __name__ == "__main__":
    file_path = "ses.txt"
    file_gz_path = f"{file_path}.gz"
    if not os.path.exists(file_path):
        if os.path.exists(file_gz_path):
            with gzip.open(file_gz_path, "rb") as f_in, open(file_path, "wb") as f_out:
                f_out.write(f_in.read())
        else:
            exit(f"File '{file_path}' not found")

    parse_ses(file_path)
