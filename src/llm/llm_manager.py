import json
import os
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMManager:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
        self.api_url = os.getenv("LLM_API_URL", 'http://localhost:11434')
        
        if self.api_url:
            # Cleanup URL if user pasted the endpoint instead of the base host
            self.api_url = self.api_url.strip().rstrip('/')
            for suffix in ['/api/generate', '/api/chat', '/api']:
                if self.api_url.endswith(suffix):
                    self.api_url = self.api_url[:-len(suffix)]
            
            self.client = ollama.Client(host=self.api_url)
        else:
            self.client = ollama

    def get_tool_definitions(self):
        return [
            {
                'type': 'function',
                'function': {
                    'name': 'draw_line',
                    'description': 'Draw a line in AutoCAD',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'start': {'type': 'array', 'items': {'type': 'number'}, 'description': '[x, y, z]'},
                            'end': {'type': 'array', 'items': {'type': 'number'}, 'description': '[x, y, z]'},
                        },
                        'required': ['start', 'end'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'draw_circle',
                    'description': 'Draw a circle in AutoCAD',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'center': {'type': 'array', 'items': {'type': 'number'}, 'description': '[x, y, z]'},
                            'radius': {'type': 'number'},
                        },
                        'required': ['center', 'radius'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'draw_point',
                    'description': 'Draw a point in AutoCAD',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'point': {'type': 'array', 'items': {'type': 'number'}, 'description': '[x, y, z]'},
                        },
                        'required': ['point'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'draw_arc',
                    'description': 'Draw an arc in AutoCAD',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'center': {'type': 'array', 'items': {'type': 'number'}, 'description': '[x, y, z]'},
                            'radius': {'type': 'number'},
                            'start_angle': {'type': 'number', 'description': 'Start angle in radians'},
                            'end_angle': {'type': 'number', 'description': 'End angle in radians'},
                        },
                        'required': ['center', 'radius', 'start_angle', 'end_angle'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'draw_spline',
                    'description': 'Draw a spline line in AutoCAD with optional start/end tangent angles.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'points': {
                                'type': 'array', 
                                'items': {'type': 'array', 'items': {'type': 'number'}}, 
                                'description': 'List of points [[x,y,z], [x,y,z], ...]'
                            },
                            'start_angle': {
                                'type': 'number', 
                                'description': 'Start tangent angle in degrees. Default is 15.',
                                'default': 15.0
                            },
                            'end_angle': {
                                'type': 'number', 
                                'description': 'End tangent angle in degrees. Default is 15.',
                                'default': 15.0
                            },
                        },
                        'required': ['points'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'trim_entities',
                    'description': 'Invoke the TRIM command in AutoCAD to clean up lines.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'list_layers',
                    'description': 'Get information about all layers in the drawing, including name, color, and status (on/off, frozen, locked).',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'set_layer_status',
                    'description': 'Enable or disable a specific layer by name.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'layer_name': {'type': 'string', 'description': 'The name of the layer to modify'},
                            'is_on': {'type': 'boolean', 'description': 'True to turn ON, False to turn OFF'},
                        },
                        'required': ['layer_name', 'is_on'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'create_layer',
                    'description': 'Create a new layer with a specific name and optional color.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'layer_name': {'type': 'string', 'description': 'The name of the new layer'},
                            'color': {
                                'type': 'integer', 
                                'description': 'AutoCAD Color Index (ACI). 1=Red, 2=Yellow, 3=Green, 4=Cyan, 5=Blue, 6=Magenta, 7=White/Black.',
                                'default': 7
                            },
                        },
                        'required': ['layer_name'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'rename_layer',
                    'description': 'Rename an existing AutoCAD layer.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'old_name': {'type': 'string', 'description': 'The current name of the layer'},
                            'new_name': {'type': 'string', 'description': 'The new name for the layer'},
                        },
                        'required': ['old_name', 'new_name'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'change_layer_color',
                    'description': 'Change the color of an existing AutoCAD layer.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'layer_name': {'type': 'string', 'description': 'The name of the layer'},
                            'color': {
                                'type': 'integer', 
                                'description': 'AutoCAD Color Index (ACI). 1=Red, 2=Yellow, 3=Green, 4=Cyan, 5=Blue, 6=Magenta, 7=White/Black.'
                            },
                        },
                        'required': ['layer_name', 'color'],
                    },
                },
            }
        ]

    def process_prompt(self, prompt):
        """Send prompt to LLM and get tool calls, encouraging sequential reasoning."""
        messages = [
            {
                'role': 'system', 
                'content': (
                    'You are an expert AutoCAD assistant. Use the provided tools to fulfill the user request. '
                    'IMPORTANT: If the user asks to draw a circle but does not provide the center coordinates or the radius, '
                    'DO NOT call the tool. Instead, respond with a polite text message asking the user for the missing information.'
                )
            },
            {'role': 'user', 'content': prompt}
        ]
        
        response = self.client.chat(
            model=self.model,
            messages=messages,
            tools=self.get_tool_definitions(),
        )
        
        message = response.get('message', {})
        content = message.get('content', '')
        tool_calls = message.get('tool_calls', [])
        
        # Fallback: if no structured tool calls, check if content looks like one
        if not tool_calls and content:
            stripped_content = content.strip()
            if stripped_content.startswith('{') and stripped_content.endswith('}'):
                try:
                    data = json.loads(stripped_content)
                    if 'name' in data and 'arguments' in data:
                        tool_calls = [{'function': data}]
                        content = "" # Clear content if it was actually a tool call
                except:
                    pass
            elif stripped_content.startswith('[') and stripped_content.endswith(']'):
                try:
                    data = json.loads(stripped_content)
                    if isinstance(data, list) and len(data) > 0:
                        potential_calls = []
                        for item in data:
                            if isinstance(item, dict) and 'name' in item and 'arguments' in item:
                                potential_calls.append({'function': item})
                        if potential_calls:
                            tool_calls = potential_calls
                            content = "" # Clear content
                except:
                    pass

        return tool_calls, content

if __name__ == "__main__":
    manager = LLMManager()
    calls = manager.process_prompt("Draw a line from 0,0 to 10,10 and a circle at 5,5 with radius 2")
    print(json.dumps(calls, indent=2))
