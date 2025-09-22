import os

drive = "./vfs"

def safe_path(path):
    abs_path = os.path.realpath(os.path.join(drive, path))
    if not abs_path.startswith(os.path.realpath(drive)):
        raise ValueError(f"Illegal path -> {path}")
    return abs_path
def get_path(path):
    os.makedirs("vfs", exist_ok=True)
    
    path = path.replace("vfs:", "")
    safe_p = safe_path(path)

    if not os.path.exists(safe_p):
        raise FileNotFoundError(f"Could not find file -> {path}")
    
    if os.path.isfile(safe_p):
        return [{"name":path, "type":"file"}]
    
    entries = []
    for entry in os.listdir(safe_p):
        file_type = "directory" if os.path.isdir(os.path.join(safe_p, entry)) else "file"

        entries.append({"name":entry,"type":file_type})
    return entries

