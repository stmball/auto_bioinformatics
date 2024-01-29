import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--icon=icon.ico',
    'src/main.py',
])

