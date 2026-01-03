# test_gitignore.py
import os
from pathlib import Path

def test_gitignore():
    """Test if .gitignore file exists and works"""
    
    print("=" * 60)
    print("Testing .gitignore Configuration")
    print("=" * 60)
    
    # Check if .gitignore exists
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        print("✓ .gitignore file exists")
        
        # Read .gitignore content
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        # Check for important entries
        important_items = [
            '.env',
            '__pycache__/',
            'venv/',
            '*.log',
            '*.db'
        ]
        
        print("\nChecking important entries:")
        for item in important_items:
            if item in content:
                print(f"✓ {item} is ignored")
            else:
                print(f"✗ {item} is NOT ignored (add it!)")
        
        print(f"\nTotal lines in .gitignore: {len(content.splitlines())}")
        
    else:
        print("✗ .gitignore file NOT found!")
        print("Create it using: notepad .gitignore")
    
    # Check if .env exists and should be ignored
    env_path = Path('.env')
    if env_path.exists():
        print("\n✓ .env file exists (should be ignored by Git)")
    else:
        print("\n⚠ .env file not found (you need to create it)")
    
    print("=" * 60)

if __name__ == "__main__":
    test_gitignore()