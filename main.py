import sys
import os
from src.cad.autocad_client import AutoCADClient
from src.llm.llm_manager import LLMManager

def main():
    print("--- AutoCAD AI Assistant ---")
    
    cad = AutoCADClient()
    if not cad.connect():
        print("Could not connect to AutoCAD. Please make sure it is open.")
        # sys.exit(1) # Uncomment for production

    llm = LLMManager()
    
    print(f"[*] Configuration Loaded:")
    print(f"    - Model: {llm.model}")
    print(f"    - API URL: {llm.api_url or 'Ollama Default (localhost:11434)'}")
    print(f"    - CAD: AutoCAD (via COM)")
    
    while True:
        try:
            user_input = input("\n[CAD AI] > ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            print("Processing request...")
            tool_calls = llm.process_prompt(user_input)
            
            if not tool_calls:
                print("LLM did not identify any CAD commands.")
                continue
                
            print(f"Total steps to execute: {len(tool_calls)}")
            for i, call in enumerate(tool_calls, 1):
                func_name = call['function']['name']
                args = call['function']['arguments']
                
                print(f"[Step {i}/{len(tool_calls)}] Executing: {func_name}")
                
                try:
                    if func_name == 'draw_line':
                        cad.add_line(tuple(args['start']), tuple(args['end']))
                    elif func_name == 'draw_circle':
                        cad.add_circle(tuple(args['center']), args['radius'])
                    elif func_name == 'draw_point':
                        cad.add_point(tuple(args['point']))
                    elif func_name == 'draw_arc':
                        cad.add_arc(tuple(args['center']), args['radius'], args['start_angle'], args['end_angle'])
                    elif func_name == 'draw_spline':
                        cad.add_spline(args['points'])
                    elif func_name == 'trim_entities':
                        cad.trim()
                    else:
                        print(f"Unsupported command: {func_name}")
                except Exception as step_error:
                    print(f"Error in step {i}: {step_error}")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
