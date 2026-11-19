"""Desktop + Start Menu shortcuts that open the app with no console window."""
import os
import subprocess
import sys
from pathlib import Path

from .util import ROOT

PS = r"""
$ws = New-Object -ComObject WScript.Shell
foreach ($dir in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) {
  if (-not $dir) { continue }
  $s = $ws.CreateShortcut((Join-Path $dir 'Peanut Clipper.lnk'))
  $s.TargetPath = '{target}'
  $s.Arguments = '-m clipper launch'
  $s.WorkingDirectory = '{root}'
  $s.IconLocation = '{icon},0'
  $s.Description = 'Peanut Clipper - make Shorts from streams'
  $s.Save()
  Write-Output $dir
}
"""


def make_shortcuts():
    if os.name != "nt":
        return []
    exe = Path(sys.executable)
    target = exe.with_name("pythonw.exe")
    if not target.exists():
        target = exe
    icon = ROOT / "assets" / "peanut.ico"
    esc = lambda p: str(p).replace("'", "''")  # noqa: E731
    script = PS.replace("{target}", esc(target)).replace("{root}", esc(ROOT)).replace("{icon}", esc(icon))
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
                       capture_output=True, text=True)
    return [line.strip() for line in r.stdout.splitlines() if line.strip()]
