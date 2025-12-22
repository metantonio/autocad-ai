

## Update - 2025-12-22 15:37:41

# Walkthrough: AutoCAD AI Assistant

I have implemented a tool that allows you to control AutoCAD using natural language through an LLM (Ollama).

## Project Structure
- [README.md](file:///c:/Repositorios/autocad-ai/README.md): Main documentation and setup guide.
- [main.py](file:///c:/Repositorios/autocad-ai/main.py): Entry point and command orchestrator.
- [src/cad/autocad_client.py](file:///c:/Repositorios/autocad-ai/src/cad/autocad_client.py): Handles the COM connection to AutoCAD and drawing functions.
- [src/llm/llm_manager.py](file:///c:/Repositorios/autocad-ai/src/llm/llm_manager.py): Manages Ollama interaction and tool/function definitions.
- [build_scripts/build_app.py](file:///c:/Repositorios/autocad-ai/build_scripts/build_app.py): Script to generate the `.exe` using PyInstaller.

## Implemented Features
- **Project Structure & Docs**: Added `README.md` and virtual environment setup instructions.
- **AutoCAD Connection**: Automatically detects and connects to a running instance of AutoCAD.
- **Natural Language Drawing**: You can ask the AI to "draw a line from 0,0 to 100,100" or "draw a circle in the center".
- **Dynamic Tool Calling**: The LLM parses user intent into specific CAD function calls.
- **Portability**: Ready to be compiled into a single `.exe`.

## How to Run
### 1. Setup Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
### 2. Launch AutoCAD & Ollama
Ensure AutoCAD is open and Ollama is running with your preferred model.
### 3. Start Assistant
```powershell
python main.py
```
4. **Build Executable**:
   ```bash
   python build_scripts/build_app.py
   ```

## Video Demonstration
> [!NOTE]
> Below is a conceptual representation of how the tool interacts with AutoCAD.

````carousel
```python
# AutoCAD Connector Logic
def add_line(self, start_point, end_point):
    return self.model_space.AddLine(start_point, end_point)
```
<!-- slide -->
```json
# LLM Tool Definition
{
  "name": "draw_line",
  "parameters": { ... }
}
```
````
