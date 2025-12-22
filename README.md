# AutoCAD & Revit AI Assistant

This project provides a bridge between LLMs (via Ollama or other providers) and CAD software (AutoCAD and/or Revit). Use natural language to draw and manipulate CAD entities directly.

## Features
- **AutoCAD Integration**: Draw points, lines, circles, arcs, and splines via COM automation.
- **LLM-Driven**: Powered by Ollama tool-calling for intelligent intent parsing.
- **Portable**: Can be compiled into a single `.exe` for easy distribution.

## Installation (Virtual Environment)

To ensure a clean installation, it is recommended to use a Python virtual environment.

1. **Clone or download** the repository.
2. **Open a terminal** (PowerShell or CMD) in the project root directory.
3. **Create the virtual environment**:
   ```powershell
   python -m venv venv
   ```
4. **Activate the environment**:
   - **PowerShell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **CMD**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
5. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Prerequisites
- **AutoCAD**: Must be installed and running during script execution.
- **Ollama**: Must be installed and reachable (default: `localhost:11434`). Ensure you have a model pulled (e.g., `ollama pull llama3`).

## Usage

1. Launch AutoCAD and open a drawing.
2. Run the assistant:
   ```powershell
   python main.py
   ```
3. Type your requests in the prompt, for example:
   - *"Draw a circle at 0,0 with radius 10."*
   - *"Draw a line from 0,0,0 to 50,50,0."*

## Building the Executable

To generate a standalone `.exe`:
```powershell
python build_scripts/build_app.py
```
The executable will be located in the `dist/` folder.

### Configuration with .exe
The compiled `.exe` will look for a `.env` file in the **same directory** where it is being executed. 
- If no `.env` file is found, the assistant will fall back to its internal defaults:
    - **OLLAMA_MODEL**: `llama3`
    - **LLM_API_URL**: `http://localhost:11434`
- You can copy your `.env` file into the `dist/` folder alongside the `CAD_AI_Assistant.exe` to customize its behavior.

## Project Structure
- `src/cad/`: CAD connectors (AutoCAD COM).
- `src/llm/`: LLM management and tool definitions.
- `build_scripts/`: PyInstaller configuration.
- `main.py`: Interactive CLI entry point.
- `requirements.txt`: Project dependencies.
