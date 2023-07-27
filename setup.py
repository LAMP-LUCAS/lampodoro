import sys
import os
from cx_Freeze import setup, Executable

# Diretório onde estão as traduções
locale_dir = os.path.join(os.path.dirname(__file__), "locale")

# Informações sobre o aplicativo
build_exe_options = {
    "packages": ["os", "tkinter", "configparser", "gettext"],
    "include_files": [(locale_dir, "locale")]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executável a ser gerado
executables = [
    Executable("lampodoro.py", base=base)
]

# Configurações do setup
setup(
    name="Lampodoro",
    version="1.0",
    description="Gerenciador de tempos Pomodoro",
    options={"build_exe": build_exe_options},
    executables=executables
)
