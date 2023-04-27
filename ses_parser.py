import os
import re
import shutil


def create_filename(name, counter=0):
    filename = f"{name}.md"
    if counter > 0:
        filename = f"{name}_({counter}).md"
    if os.path.exists(os.path.join("dist", filename)):
        return create_filename(name, counter + 1)
    return filename


def parse_ses(file_path, output_dir="dist", limit=None):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    with open(file_path, "r", encoding="utf-8") as f:
        write = False
        i = 0
        prev_file = ""
        for line in f:
            line = line.strip().replace("- ", "").rstrip("-")
            if line.endswith(","):
                line += " "
            if not line:
                continue
            if line == "А":
                write = True
                i += 1
                continue
            if line.startswith("НАСЕЛЁННЫЕ МОСКВА ы ©"):
                break
            if write:
                if match := re.search(r"^(?![А-Я](\.)? )[А-Я-]+(\s[А-Я-]+)*(?=[ \,]|\.\.)+", line):
                    upper = match.group()
                    title = upper.lower()
                    row = line.replace(upper, title).replace("- ", "-")
                    prev_file = file_name = create_filename(title.replace(" ", "_"))
                    with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
                        f.write(row)
                else:
                    with open(os.path.join(output_dir, prev_file), "a", encoding="utf-8") as f:
                        if prev_file and line.endswith("-"):
                            line = line[:-1]
                        f.write(line)
                i += 1
            if limit and i == limit:
                break


if __name__ == "__main__":
    if not os.path.exists("ses.txt"):
        if os.path.exists("ses.txt.gz"):
            import gzip

            with gzip.open("ses.txt.gz", "rb") as f_in:
                with open("ses.txt", "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            import sys

            print("File 'ses.txt' not found")
            sys.exit(1)

    parse_ses("ses.txt")
