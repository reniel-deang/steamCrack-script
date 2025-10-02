import base64
import zipfile
import shutil
import os
from pathlib import Path
import requests
import subprocess
import sys

# psutil is optional; used only for process inspection (no killing).
try:
    import psutil
except Exception:
    psutil = None

# Optional: read-only Steam path from registry (Windows only)
def get_steam_path_from_registry():
    try:
        import winreg
    except Exception:
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ) as key:
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            return steam_path
    except Exception:
        return None


class Main:
    """
    Python equivalent of the C# Main class.
    Methods:
      - UnZip(fileName, extract_dir)
      - DownloadManifest(appid)
      - DeleteLUA(appid)
      - ManifestResponse(url, path, appid)
      - CheckForExist(appid)
      - Base64ToFileConverter.SaveBase64AsBinaryFile
    """

    def __init__(self):
        # sandbox root for safe operations
        self.sandbox_root = Path.cwd() / "sandbox_inspect"
        self.sandbox_root.mkdir(exist_ok=True)

        # safe targets (instead of Steam locations)
        self.sandbox_depotcache = self.sandbox_root / "config" / "depotcache"
        self.sandbox_stplugin = self.sandbox_root / "config" / "stplug-in"
        self.sandbox_depotcache.mkdir(parents=True, exist_ok=True)
        self.sandbox_stplugin.mkdir(parents=True, exist_ok=True)

    def UnZip(self, fileName: str, extract_dir: str) -> None:
        """
        Equivalent to C# UnZip: creates directory if needed and extracts the zip.
        Note: extraction ignores entries with path traversal to be safe.
        """
        extract_dir_path = Path(extract_dir)
        if not extract_dir_path.exists():
            extract_dir_path.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(fileName, "r") as zf:
                safe_members = []
                for member in zf.namelist():
                    # prevent path traversal or absolute paths
                    if os.path.isabs(member) or ".." in Path(member).parts:
                        print(f"[UnZip] Skipping suspicious entry: {member}")
                        continue
                    safe_members.append(member)
                zf.extractall(extract_dir_path, members=safe_members)
        except zipfile.BadZipFile:
            print(f"[UnZip] Bad zip file: {fileName}")
        except FileNotFoundError:
            print(f"[UnZip] File not found: {fileName}")
        except Exception as e:
            # original C# had empty catch; here we at least log.
            print(f"[UnZip] Exception during extraction: {e}")

    def DownloadManifest(self, appid: str) -> None:
        """
        Equivalent to C# DownloadManifest.
        - Check remote existence
        - Download to working dir (./{appid}.zip)
        - Extract, look for files, and perform "StartAdd" logic
        - WARNING: All Steam-modifying lines are commented out and replaced with sandbox ops.
        """
        steam_auto_add = SteamAutoAdd()

        # In C# they call: if (!this.CheckForExist(appid)) { ... } -- note bool inversion in original decompiled code.
        # Here we'll treat CheckForExist to return True if exists; if it does not exist, we abort.
        if not self.CheckForExist(appid):
            # remote zip missing -> stop
            print(f"[DownloadManifest] {appid}.zip not found on remote. Aborting.")
            return

        url = f""
        selectedPath = "./"

        # download the zip into current directory
        self.ManifestResponse(url, selectedPath, appid)

        zip_local = Path(selectedPath) / f"{appid}.zip"
        extract_dir = Path(selectedPath) / appid

        # extract
        self.UnZip(str(zip_local), str(extract_dir))

        game_path = str(extract_dir)

        # Inspect Steam processes -- original C# kills them. We WILL NOT kill processes.
        # We'll only detect and print their status.
        steam_processes = []
        if psutil:
            for proc in psutil.process_iter(["name", "pid"]):
                try:
                    if proc.info["name"] and proc.info["name"].lower().startswith("steam"):
                        steam_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        else:
            # fallback: use 'tasklist' on Windows for detection (no killing)
            try:
                if sys.platform.startswith("win"):
                    output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq steam.exe"], stderr=subprocess.DEVNULL, text=True)
                    if "steam.exe" in output.lower():
                        steam_processes = ["steam.exe (detected)"]
            except Exception:
                pass

        if not steam_processes:
            print("[DownloadManifest] Steam not running (or not detected).")
        else:
            print("[DownloadManifest] Steam detected: (NO ACTION TAKEN)")
            # DANGEROUS: original C# killed the processes:
            # foreach (Process proc in steamProcesses) { proc.Kill(); }
            # foreach (Process proc2 in steamProcesses) { proc2.WaitForExit(); }
            # Those lines are intentionally commented out below:
            #
            # >>> DANGEROUS — COMMENTED OUT <<<
            # for proc in steam_processes:
            #     try:
            #         proc.kill()
            #     except Exception as e:
            #         print("Failed to kill process:", e)
            #
            # for proc in steam_processes:
            #     try:
            #         proc.wait(timeout=30)
            #     except Exception:
            #         pass
            #
            # END DANGEROUS

        # Process extracted files using SteamAutoAdd logic, but move files to sandbox instead of Steam.
        steam_auto_add.StartAdd(game_path, sandbox_depot=self.sandbox_depotcache, sandbox_lua=self.sandbox_stplugin)

        # Cleanup similarly to C# but sandboxed (only delete local zip and extracted folder from working dir)
        try:
            if zip_local.exists():
                zip_local.unlink()
                print(f"[DownloadManifest] Deleted local zip: {zip_local}")
        except Exception as e:
            print("[DownloadManifest] Failed to delete zip:", e)

        # Delete extracted directory safely
        try:
            if extract_dir.exists() and extract_dir.is_dir():
                shutil.rmtree(extract_dir)
                print(f"[DownloadManifest] Deleted extracted folder: {extract_dir}")
        except Exception as e:
            print("[DownloadManifest] Failed to delete extracted folder:", e)

        # DANGEROUS: original C# performs Steam folder modifications:
        # File.Delete(Settings1.Default.SteamPath + "hid.dll");
        # Directory.CreateDirectory(Settings1.Default.SteamPath);
        # File.Copy("hid.dll", Path.Combine(Settings1.Default.SteamPath ?? "", "hid.dll"), true);
        # MessageBox.Show("Game or App ID added in library successfully, steam restarted.", "Steam Games Tool");
        #
        # Those are commented out. Below we log what would have been done.
        steam_path = get_steam_path_from_registry() or "<SteamPath not found>"
        print("[DownloadManifest] (SAFE MODE) Would have replaced hid.dll in SteamPath:", steam_path)
        print("[DownloadManifest] (SAFE MODE) Steam-modifying lines are intentionally disabled in this educational script.")

    def DeleteLUA(self, appid: str) -> None:
        """
        Equivalent to C# DeleteLUA: deletes a specific lua file in Steam config/stplug-in/<appid>.lua
        In this safe translation we will not touch Steam's folder. Instead we delete the corresponding file
        in sandbox_inspect/config/stplug-in/<appid>.lua, which mimics the same file layout.
        """
        # original path: Settings1.Default.SteamPath + "config\\stplug-in\\" + appid + ".lua"
        sandbox_lua_path = self.sandbox_stplugin / f"{appid}.lua"
        try:
            if sandbox_lua_path.exists():
                sandbox_lua_path.unlink()
                print(f"[DeleteLUA] Deleted sandbox lua: {sandbox_lua_path}")
            else:
                print(f"[DeleteLUA] Sandbox lua file not found: {sandbox_lua_path}")
        except Exception as e:
            print(f"[DeleteLUA] Exception while deleting: {e}")

        # In C# they show a MessageBox and then kill/start Steam. We will only display a message.
        print("[DeleteLUA] (SAFE MODE) Not restarting Steam. Steam restart code is commented out.")

        # DANGEROUS — commented out: killing and starting Steam
        # try:
        #     steam_processes = [p for p in psutil.process_iter(['name']) if p.info['name'] and p.info['name'].lower().startswith('steam')]
        #     if steam_processes:
        #         for p in steam_processes:
        #             p.kill()
        #         for p in steam_processes:
        #             p.wait()
        #     steam_exe = os.path.join(Settings1.Default.SteamPath, "steam.exe")
        #     subprocess.Popen([steam_exe])
        # except Exception as ex:
        #     print("Error:", ex)

    def ManifestResponse(self, url: str, path: str, appid: str) -> None:
        """
        Equivalent to C# ManifestResponse: download the file url -> path/appid.zip using requests.
        """
        if not url:
            return
        path_filename = Path(path) / f"{appid}.zip"
        try:
            path_filename.parent.mkdir(parents=True, exist_ok=True)
            # streaming download
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(path_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print(f"[ManifestResponse] Downloaded {url} to {path_filename}")
        except Exception as e:
            print(f"[ManifestResponse] Download error: {e}")

    def CheckForExist(self, appid: str) -> bool:
        """
        Equivalent to C# CheckForExist: sends a HEAD request to the S3 url and returns True if 200 OK.
        """
        url = f""
        try:
            r = requests.head(url, allow_redirects=True, timeout=10)
            if r.status_code == 200:
                return True
            else:
                print("[CheckForExist] App ID doesn't exist. HTTP:", r.status_code, r.reason)
                return False
        except requests.RequestException as ex:
            # In the C#, they inspect WebException.Response; here we just print.
            print(f"[CheckForExist] Request exception: {ex}")
            return False

    class Base64ToFileConverter:
        @staticmethod
        def SaveBase64AsBinaryFile(base64String: str, filePath: str) -> bool:
            """
            Decode base64 and save to file. Matches C# behavior. Returns True on success.
            """
            try:
                fileBytes = base64.b64decode(base64String)
                Path(filePath).parent.mkdir(parents=True, exist_ok=True)
                with open(filePath, "wb") as f:
                    f.write(fileBytes)
                print("[Base64ToFileConverter] File successfully saved to:", filePath)
                return True
            except (base64.binascii.Error, ValueError) as e:
                print("[Base64ToFileConverter] Invalid Base64 string:", e)
                return False
            except Exception as e:
                print("[Base64ToFileConverter] Error saving file:", e)
                return False


class SteamAutoAdd:
    """
    Python equivalent of SteamAutoAdd class.
    The original moves .manifest files into Steam's config\\depotcache and .lua files into config\\stplug-in,
    then restarts Steam. Those destructive actions are commented out. Instead we move files into sandbox folders.
    """

    @staticmethod
    def MoveManifests(manifest: str, dir_name: str, sandbox_depot: Path):
        """
        Original: moves manifest into Settings1.Default.SteamPath/config/depotcache
        SAFE: move into sandbox_depot (passed in)
        """
        src = Path(manifest)
        sandbox_depot.mkdir(parents=True, exist_ok=True)
        dest = sandbox_depot / src.name
        try:
            # Overwrite semantics similar to File.Move(manifest, destinationPath, true) in original
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"[MoveManifests] Moved {src} -> {dest} (sandbox)")
        except Exception as e:
            print(f"[MoveManifests] Error moving manifest: {e}")

    @staticmethod
    def MoveLuas(lua: str, dir_name: str, sandbox_lua: Path):
        """
        Original: moves lua into Settings1.Default.SteamPath/config/stplug-in
        SAFE: move into sandbox_lua
        """
        src = Path(lua)
        sandbox_lua.mkdir(parents=True, exist_ok=True)
        dest = sandbox_lua / src.name
        try:
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"[MoveLuas] Moved {src} -> {dest} (sandbox)")
        except Exception as e:
            print(f"[MoveLuas] Error moving lua: {e}")

    @staticmethod
    def RestartSteam():
        """
        Original: kills steam processes and starts steam.exe from Settings1.Default.SteamPath
        DANGEROUS: commented out in this educational script.
        We implement a READ-ONLY detection that reports status but does not act.
        """
        try:
            # Detect steam processes (report only)
            found = False
            if psutil:
                for p in psutil.process_iter(["name", "pid"]):
                    try:
                        if p.info["name"] and p.info["name"].lower().startswith("steam"):
                            print(f"[RestartSteam] Detected Steam process: pid={p.pid}, name={p.info['name']}")
                            found = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            else:
                print("[RestartSteam] psutil not available; process inspection skipped.")

            if not found:
                print("[RestartSteam] Steam not running (no action taken).")
            else:
                print("[RestartSteam] (SAFE MODE) Steam restart code is commented out to avoid destructive behavior.")

            # DANGEROUS — COMMENTED OUT: code that would kill processes and restart steam.exe
            # try:
            #     for p in psutil.process_iter(['name']):
            #         if p.info['name'] and p.info['name'].lower().startswith('steam'):
            #             p.kill()
            #     steam_exe = Path(Settings1.Default.SteamPath) / "steam.exe"
            #     subprocess.Popen([str(steam_exe)])
            # except Exception as ex:
            #     print("Error restarting Steam:", ex)

        except Exception as ex:
            print("[RestartSteam] Error:", ex)

    def StartAdd(self, path_name: str, sandbox_depot: Path, sandbox_lua: Path):
        """
        Equivalent to C# StartAdd:
         - Look for files in path_name
         - If none found, look inside a single subdirectory
         - Process files via ProcessFiles
         - In original they would call RestartSteam() if files are processed; here we only call the safe RestartSteam() which is non-destructive.
        """
        fullPath = Path("./") / path_name
        files = [str(p) for p in fullPath.glob("*") if p.is_file()]
        found = self.ProcessFiles(files, sandbox_depot, sandbox_lua)
        if not found:
            subDirs = [p for p in fullPath.iterdir() if p.is_dir()]
            if len(subDirs) == 1:
                subDir = subDirs[0]
                subFiles = [str(p) for p in subDir.glob("*") if p.is_file()]
                self.ProcessFiles(subFiles, sandbox_depot, sandbox_lua)
                SteamAutoAdd.RestartSteam()  # safe-mode: only reports

    def ProcessFiles(self, files: list, sandbox_depot: Path, sandbox_lua: Path) -> bool:
        """
        Iterate files, move .lua -> sandbox_lua, .manifest -> sandbox_depot.
        Return True if any were found.
        """
        anyFound = False
        for file in files:
            extension = Path(file).suffix.lower()
            if extension == ".lua":
                print(f"[ProcessFiles] Found lua: {file}")
                SteamAutoAdd.MoveLuas(file, "", sandbox_lua)
                anyFound = True
            elif extension == ".manifest":
                print(f"[ProcessFiles] Found manifest: {file}")
                SteamAutoAdd.MoveManifests(file, "", sandbox_depot)
                anyFound = True
        return anyFound


# === Example usage / test harness ===
if __name__ == "__main__":
    m = Main()

    # Put an example appid here to test the safe flow; it will download if available.
    test_appid = "12345"
    print("SteamPath (read-only):", get_steam_path_from_registry() or "<not found>")

    # Demonstrate CheckForExist (safe)
    exists = m.CheckForExist(test_appid)
    print(f"[Main] CheckForExist({test_appid}) -> {exists}")

    # If you want to test the full safe DownloadManifest flow, uncomment the line below.
    # NOTE: It will download the zip (if present) and perform sandbox moves, but it will NOT touch Steam.
    # m.DownloadManifest(test_appid)

    # Demonstrate SaveBase64AsBinaryFile (safe)
    sample_b64 = base64.b64encode(b"hello world").decode("ascii")
    sample_out = str(m.sandbox_root / "sample.bin")
    Main.Base64ToFileConverter.SaveBase64AsBinaryFile(sample_b64, sample_out)
    print("[Main] Saved sample base64 to:", sample_out)

    print("\nEducational conversion complete. Review the code and the comments to map actions to the original C#.")
