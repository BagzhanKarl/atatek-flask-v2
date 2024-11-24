import os
import uuid

from werkzeug.utils import secure_filename

def save_file(file, upload_folder):
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        print(f"File saved to {file_path}")
        return unique_filename
    return None