def main():
    import sys
    import os
    import json
    import shutil

    # Ensure .env exists
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        print("[*] .env file not found. Creating from .env.example...")
        shutil.copy(".env.example", ".env")

    try:
        from src.cad.autocad_client import AutoCADClient
        from src.llm.llm_manager import LLMManager
        import win32com.client
        import pythoncom
    except ImportError as e:
        print(f"\n[!] IMPORT ERROR: {e}")
        print("This usually means a library is missing from the compiled executable.")
        raise e

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
                    elif func_name == 'list_layers':
                        layers = cad.get_layers_info()
                        # Add a second LLM pass to explain the layers to the user
                        print(f"Retrieved {len(layers)} layers. Generating summary...")
                        summary_prompt = f"The user asked about layers. Here is the technical data of the layers: {json.dumps(layers)}. Please summarize this for the user in a friendly way, highlighting which ones are off or locked."
                        summary_response = llm.client.chat(
                            model=llm.model,
                            messages=[{'role': 'user', 'content': summary_prompt}]
                        )
                        print(f"\n[Layers Summary]:\n{summary_response['message']['content']}")
                    elif func_name == 'set_layer_status':
                        success = cad.set_layer_status(args['layer_name'], args['is_on'])
                        status_str = "ON" if args['is_on'] else "OFF"
                        if success:
                            print(f"[*] Layer '{args['layer_name']}' successfully turned {status_str}.")
                        else:
                            print(f"[!] Failed to turn {status_str} the layer '{args['layer_name']}'.")
                    elif func_name == 'create_layer':
                        color = args.get('color', 7)
                        cad.create_layer(args['layer_name'], color)
                        print(f"[*] Layer '{args['layer_name']}' created with color {color}.")
                    else:
                        print(f"Unsupported command: {func_name}")
                except Exception as step_error:
                    print(f"Error in step {i}: {step_error}")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("\n" + "="*50)
        print("CRITICAL ERROR DURING EXECUTION:")
        traceback.print_exc()
        print("="*50)
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        pass
