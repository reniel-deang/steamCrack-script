import requests
import os
import shutil
import zipfile
from pathlib import Path
from dotenv import dotenv_values

def url_exists_head(url, timeout=10):
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException as e:
        print("HEAD request failed:", e)
        return False

def download_file(url, dest_path, chunk_size=8192):
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        return True
    except requests.RequestException as e:
        print("Download failed:", e)
        return False

def safe_extract_zip(zip_path, extract_to):
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_to)
        return True
    except zipfile.BadZipFile as e:
        print("Bad zip file:", e)
        return False
    except Exception as e:
        print("Extraction error:", e)
        return False

def find_files_by_ext(root_dir, extensions):
    root_dir = Path(root_dir)
    found = []
    for p in root_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            found.append(p)
    return found

def move_files_to_folder(files, target_folder):
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)
    moved = []
    for f in files:
        dest = target_folder / f.name
        # In the safe script we avoid overwriting unless user permits; here we overwrite
        try:
            shutil.move(str(f), str(dest))
            moved.append(dest)
        except Exception as e:
            print(f"Failed to move {f} -> {dest}: {e}")
    return moved

if __name__ == "__main__":
    # Example usage (replace appid and host as needed)

    appid = "240"
    host = "" # need for env
    url = f"{host}/{appid}.zip"

    # if not url_exists_head(url):
    #     print(f"{url} not found (HEAD returned non-200).")
    # else:
    #     local_zip = Path.cwd() / f"{appid}.zip"
    #     print("Downloading...", url)
    #     if download_file(url, local_zip):
    #         print("Downloaded to", local_zip)
    #         extract_dir = Path.cwd() / "extracted" / appid
    #         if safe_extract_zip(local_zip, extract_dir):
    #             print("Extracted to:", extract_dir)
    #             # Look for .lua and .manifest in the extracted folder
    #             found = find_files_by_ext(extract_dir, extensions={".lua", ".manifest"})
    #             print(f"Found {len(found)} files: {[str(x) for x in found]}")
    #             # Move them to user-specified safe folders (not Steam)
    #             lua_target = Path.cwd() / "collected_luas"
    #             manifest_target = Path.cwd() / "collected_manifests"
    #             lua_files = [f for f in found if f.suffix.lower() == ".lua"]
    #             manifest_files = [f for f in found if f.suffix.lower() == ".manifest"]
    #             moved_luas = move_files_to_folder(lua_files, lua_target)
    #             moved_manifests = move_files_to_folder(manifest_files, manifest_target)
    #             print("Moved LUA files:", moved_luas)
    #             print("Moved manifest files:", moved_manifests)
    #         else:
    #             print("Extraction failed.")
    #     else:
    #         print("Download failed.")
