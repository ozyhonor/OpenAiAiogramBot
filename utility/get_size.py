import os


def get_readable_size(file):
    file_size_bytes = os.path.getsize(file)

    if file_size_bytes < 1024:
        return f"{file_size_bytes} B"
    elif file_size_bytes < 1024 * 1024:
        file_size_kb = file_size_bytes / 1024
        return f"{file_size_kb:.2f} KB"
    else:
        file_size_mb = file_size_bytes / (1024 * 1024)
        return f"{file_size_mb:.2f} MB"
