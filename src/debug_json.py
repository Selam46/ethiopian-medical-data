import os
from pathlib import Path

def debug_json():
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    # Construct path to JSON file
    json_path = project_root / "data" / "raw" / "messages" / "scrape_20250204_012338.json"
    
    print(f"Looking for file at: {json_path}")
    
    if json_path.exists():
        print("\nFile found! Reading contents...")
        with open(json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nFirst 200 characters of file:")
            print("-" * 50)
            print(content[:200])
            print("-" * 50)
            print(f"\nTotal file size: {len(content)} characters")
    else:
        print(f"\nError: File not found at {json_path}")
        print("\nAvailable files in messages directory:")
        messages_dir = project_root / "data" / "raw" / "messages"
        if messages_dir.exists():
            for file in messages_dir.glob("*"):
                print(f"- {file.name}")
        else:
            print(f"Messages directory not found at: {messages_dir}")

if __name__ == "__main__":
    debug_json() 