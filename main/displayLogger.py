import subprocess
import sys

# subprocess.run('powershell.exe Get-Item *')
p = subprocess.Popen(["powershell.exe"], stdout=sys.stdout)
p.communicate()