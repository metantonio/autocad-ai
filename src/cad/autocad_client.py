import win32com.client
import pythoncom
import time
from array import array

class AutoCADClient:
    def __init__(self):
        self.app = None
        self.doc = None
        self.model_space = None

    def connect(self):
        """Connect to a running instance of AutoCAD using win32com."""
        prog_ids = [
            "AutoCAD.Application",
            "AutoCAD.Application.25",
            "AutoCAD.Application.24.1",
            "AutoCAD.Application.24",
            "AutoCAD.Application.23.1",
            "AutoCAD.Application.23",
            "AutoCAD.Application.22",
            "AutoCAD.Application.21",
            "AutoCAD.Application.20.1",
            "AutoCAD.Application.20",
        ]
        
        last_error = None
        for prog_id in prog_ids:
            try:
                print(f"[*] Trying to connect via '{prog_id}'...")
                # win32com.client.GetActiveObject is generally more robust for running apps
                self.app = win32com.client.GetActiveObject(prog_id)
                self.doc = self.app.ActiveDocument
                self.model_space = self.doc.ModelSpace
                print(f"[+] Successfully connected via '{prog_id}'.")
                return True
            except Exception as e:
                # print(f"    [-] Connection failed for '{prog_id}': {e}")
                last_error = e
                continue
        
        print(f"Error connecting to AutoCAD: {last_error}")
        print("Tip: Make sure AutoCAD is open and a drawing is active.")
        return False

    def _get_double_array(self, point):
        """Convert a point to a win32com-compatible double array."""
        if len(point) == 2:
            return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(point[0]), float(point[1]), 0.0))
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(point[0]), float(point[1]), float(point[2])))

    def add_line(self, start_point, end_point):
        """Add a line to the model space."""
        if not self.model_space: return None
        try:
            start = self._get_double_array(start_point)
            end = self._get_double_array(end_point)
            return self.model_space.AddLine(start, end)
        except Exception as e:
            print(f"Error in add_line: {e}")
            raise e

    def add_circle(self, center, radius):
        """Add a circle to the model space."""
        if not self.model_space: return None
        try:
            c = self._get_double_array(center)
            return self.model_space.AddCircle(c, float(radius))
        except Exception as e:
            print(f"Error in add_circle: {e}")
            raise e

    def add_point(self, point):
        """Add a point to the model space."""
        if not self.model_space: return None
        try:
            p = self._get_double_array(point)
            return self.model_space.AddPoint(p)
        except Exception as e:
            print(f"Error in add_point: {e}")
            raise e

    def add_arc(self, center, radius, start_angle, end_angle):
        """Add an arc to the model space."""
        if not self.model_space: return None
        try:
            c = self._get_double_array(center)
            return self.model_space.AddArc(c, float(radius), float(start_angle), float(end_angle))
        except Exception as e:
            print(f"Error in add_arc: {e}")
            raise e

    def add_spline(self, points):
        """Add a spline to the model space."""
        if not self.model_space: return None
        try:
            flattened = []
            for pt in points:
                if len(pt) == 2:
                    flattened.extend([float(pt[0]), float(pt[1]), 0.0])
                else:
                    flattened.extend([float(pt[0]), float(pt[1]), float(pt[2])])
            
            pts_array = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, flattened)
            start_tan = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            end_tan = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
            return self.model_space.AddSpline(pts_array, start_tan, end_tan)
        except Exception as e:
            print(f"Error in add_spline: {e}")
            raise e

    def create_layer(self, layer_name, color_index=7):
        """Create a new layer with a specific color (default: 7 - White/Black)."""
        try:
            if not self.doc: return None
            # Add method will return existing layer if it already exists
            layer = self.doc.Layers.Add(layer_name)
            layer.Color = int(color_index)
            print(f"[+] Layer '{layer_name}' created/updated with color {color_index}.")
            return layer
        except Exception as e:
            print(f"Error creating layer: {e}")
            return None

    def get_layers_info(self):
        """Retrieve a list of layers and their properties."""
        try:
            if not self.doc: return []
            layers_data = []
            layers = self.doc.Layers
            for i in range(layers.Count):
                layer = layers.Item(i)
                layers_data.append({
                    "name": layer.Name,
                    "is_on": layer.LayerOn,
                    "is_frozen": layer.Freeze,
                    "is_locked": layer.Lock,
                    "color": layer.Color
                })
            return layers_data
        except Exception as e:
            print(f"Error retrieving layers: {e}")
            return []

    def set_layer_status(self, layer_name, is_on):
        """Enable or disable a specific layer."""
        try:
            if not self.doc: return False
            layer = self.doc.Layers.Item(layer_name)
            layer.LayerOn = is_on
            return True
        except Exception as e:
            print(f"Error setting layer status: {e}")
            return False

    def trim(self):
        """Invoke the TRIM command."""
        self.send_command("_TRIM")

    def send_command(self, command):
        """Send a raw command to AutoCAD."""
        try:
            if self.doc:
                self.doc.SendCommand(f"{command} ")
                return True
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
        return False
