import os
from pypdf import PdfReader
from api.config import CV_PATH

_cache = {"mtime": 0, "text": ""}

def get_cv_text() -> str:
    mtime = os.path.getmtime(CV_PATH)
    if mtime != _cache["mtime"]:
        reader = PdfReader(CV_PATH)
        _cache["text"] = "\n".join(p.extract_text() or "" for p in reader.pages)
        _cache["mtime"] = mtime
    return _cache["text"]