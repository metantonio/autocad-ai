import PyInstaller.__main__
import os

def build():
    # Set environment variables for PyInstaller if needed
    os.environ['PYINSTALLER_ISOLATED_PYTHON'] = '0'

    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--console',
        '--name=CAD_AI_Assistant',
        '--collect-all=comtypes',
        '--collect-all=ollama',
        '--collect-all=pydantic',
        '--collect-all=python-dotenv',
        '--hidden-import=comtypes.gen',
        '--hidden-import=comtypes.automation',
        '--hidden-import=comtypes.typeinfo',
        '--hidden-import=win32com',
        '--hidden-import=src.cad.autocad_client',
        '--hidden-import=src.llm.llm_manager',
    ])

if __name__ == "__main__":
    build()
