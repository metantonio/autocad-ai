import comtypes.client
import time

class AutoCADClient:
    def __init__(self):
        self.app = None
        self.doc = None
        self.model_space = None

    def connect(self):
        """Connect to a running instance of AutoCAD, trying multiple ProgIDs."""
        prog_ids = [
            "AutoCAD.Application",      # Generic
            "AutoCAD.Application.25",   # AutoCAD 2024
            "AutoCAD.Application.24.1", # AutoCAD 2022
            "AutoCAD.Application.24",   # AutoCAD 2021
            "AutoCAD.Application.23.1", # AutoCAD 2020
            "AutoCAD.Application.23",   # AutoCAD 2019
            "AutoCAD.Application.22",   # AutoCAD 2018
            "AutoCAD.Application.21",   # AutoCAD 2017
            "AutoCAD.Application.20.1", # AutoCAD 2016
            "AutoCAD.Application.20",   # AutoCAD 2015
        ]
        
        last_error = None
        for prog_id in prog_ids:
            try:
                print(f"Trying to connect via {prog_id}...")
                self.app = comtypes.client.GetActiveObject(prog_id)
                self.doc = self.app.ActiveDocument
                self.model_space = self.doc.ModelSpace
                print(f"Successfully connected to AutoCAD via {prog_id}.")
                return True
            except Exception as e:
                last_error = e
                continue
        
        print(f"Error connecting to AutoCAD: {last_error}")
        print("Tip: Make sure AutoCAD is open and a drawing is active.")
        return False

    def add_line(self, start_point, end_point):
        """Add a line to the model space."""
        if not self.model_space:
            return None
        # points are tuples (x, y, z)
        return self.model_space.AddLine(comtypes.automation.VARIANT(start_point), 
                                        comtypes.automation.VARIANT(end_point))

    def add_circle(self, center, radius):
        """Add a circle to the model space."""
        if not self.model_space:
            return None
        return self.model_space.AddCircle(comtypes.automation.VARIANT(center), radius)

    def add_point(self, point):
        """Add a point to the model space."""
        if not self.model_space:
            return None
        return self.model_space.AddPoint(comtypes.automation.VARIANT(point))

    def add_arc(self, center, radius, start_angle, end_angle):
        """Add an arc to the model space."""
        if not self.model_space:
            return None
        return self.model_space.AddArc(comtypes.automation.VARIANT(center), radius, start_angle, end_angle)

    def add_spline(self, points):
        """Add a spline to the model space from a list of points."""
        try:
            if not self.model_space:
                return None
            flattened_points = [p for pt in points for p in pt]
            start_tan = comtypes.automation.VARIANT([0.0, 0.0, 0.0])
            end_tan = comtypes.automation.VARIANT([0.0, 0.0, 0.0])
            return self.model_space.AddSpline(comtypes.automation.VARIANT(flattened_points), start_tan, end_tan)
        except Exception as e:
            print(f"Error adding spline: {e}")
            return None

    def get_layers_info(self):
        """Retrieve a list of layers and their properties."""
        try:
            if not self.doc:
                return []
            
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

    def trim(self):
        """Invoke the TRIM command in AutoCAD. 
        Note: Trim usually requires interactive selection, but we can send command strings.
        """
        print("Sending TRIM command to AutoCAD...")
        self.send_command("_TRIM")

    def send_command(self, command):
        """Send a raw command to AutoCAD."""
        try:
            if self.doc:
                # Use \r to simulate Enter
                self.doc.SendCommand(f"{command} ")
                return True
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
        return False

if __name__ == "__main__":
    client = AutoCADClient()
    if client.connect():
        # Example: Draw a simple line
        client.add_line((0, 0, 0), (10, 10, 0))
        client.add_circle((5, 5, 0), 2.5)
