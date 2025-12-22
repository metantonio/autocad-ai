import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
WALKTHROUGH_PATH = os.getenv("WALKTHROUGH_PATH")
CHANGELOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "changelog.md")

def update_changelog():
    """Appends the content of walkthrough.md to changelog.md with a timestamp."""
    if not os.path.exists(WALKTHROUGH_PATH):
        print(f"Error: Walkthrough artifact not found at {WALKTHROUGH_PATH}")
        return

    with open(WALKTHROUGH_PATH, "r", encoding="utf-8") as f:
        walkthrough_content = f.read()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n## Update - {timestamp}\n\n"
    
    mode = "a" if os.path.exists(CHANGELOG_PATH) else "w"
    
    with open(CHANGELOG_PATH, mode, encoding="utf-8") as f:
        f.write(header)
        f.writelines(walkthrough_content)
    
    print(f"Successfully updated changelog.md at {CHANGELOG_PATH}")

if __name__ == "__main__":
    update_changelog()
