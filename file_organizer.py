from os import walk, rename, remove
from os.path import splitext, join, isdir

DEFAULT_EXTS = {
    r"C:\Users\shana\Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".svg",
    },
    r"C:\Users\shana\Music": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    r"C:\Users\shana\Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    r"C:\Users\shana\Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".ppt",
        ".pptx",
        ".xls",
        ".xlsx",
        ".odt",
        ".zip",
    },
    r"C:\Users\shana\Downloads": "",
}

exts = {}


def user():
    while True:
        raw = (
            input(
                f"Paths and its extensions\nb - break, q - exit, d - defualt folders\n: "
            )
            .strip()
            .lower()
        )
        if raw == "q":
            exit()
        elif raw == "b":
            return exts
        elif raw == "d":
            return DEFAULT_EXTS
        try:
            path, extension = raw.split(":")
            if not isdir(path):
                print("Invalid path")
                continue
            extension = set(map(str.strip, extension.split()))
            exts[path.strip()] = extension
            continue
        except ValueError:
            print("Invalid format.")
            continue


def organize(exten):
    nfiles = 0
    for folder in exten:

        for root, _, files in walk(folder):
            for file in files:
                ext = splitext(file)[1].lower()

                for folders, extension in exten.items():
                    if ext in extension:
                        if folder != folders:
                            try:
                                rename(
                                    join(root, file),
                                    join(folders, file),
                                )
                            except FileExistsError:
                                remove(join(root, file))

                            nfiles += 1
                            break

    print(f"Done! Location of {nfiles} was changed.")


organize(user())
