import json
import os
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMManager:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
        self.api_url = os.getenv("LLM_API_URL")
        
        if self.api_url:
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
                    'description': 'Draw a spline line in AutoCAD',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'points': {
                                'type': 'array', 
                                'items': {'type': 'array', 'items': {'type': 'number'}}, 
                                'description': 'List of points [[x,y,z], [x,y,z], ...]'
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
            }
        ]

    def process_prompt(self, prompt):
        """Send prompt to LLM and get tool calls, encouraging sequential reasoning."""
        messages = [
            {
                'role': 'system', 
                'content': 'You are an expert AutoCAD assistant. When a user asks for a complex task, '
                           'generate all the necessary tool calls in the correct logical order '
                           '(e.g., draw a rectangle before trimming it).'
            },
            {'role': 'user', 'content': prompt}
        ]
        
        response = self.client.chat(
            model=self.model,
            messages=messages,
            tools=self.get_tool_definitions(),
        )
        return response['message'].get('tool_calls', [])

if __name__ == "__main__":
    manager = LLMManager()
    calls = manager.process_prompt("Draw a line from 0,0 to 10,10 and a circle at 5,5 with radius 2")
    print(json.dumps(calls, indent=2))
