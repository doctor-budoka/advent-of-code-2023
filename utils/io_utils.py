def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_file_by_line(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()