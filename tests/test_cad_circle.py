from src.cad.autocad_client import AutoCADClient
import sys

def test_circle():
    print("Testing AutoCAD Circle creation...")
    cad = AutoCADClient()
    if not cad.connect():
        print("Could not connect to AutoCAD.")
        return

    try:
        center = (0.0, 0.0, 0.0)
        radius = 5.0
        print(f"Attempting to draw circle at {center} with radius {radius}...")
        circle = cad.add_circle(center, radius)
        if circle:
            print("SUCCESS: Circle created successfully.")
        else:
            print("FAILURE: Circle object is None.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_circle()
