import os

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, folder):
    if not allowed_file(file.filename):
        return None, "Invalid file type"

    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, file.filename)
    file.save(path)

    return path, None
