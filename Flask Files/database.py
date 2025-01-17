import json
import string
import random
from typing import Dict, Tuple, Optional, List
from config import Config

def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def load_database() -> Dict:
    """Load user data from JSON file."""
    try:
        with open(Config.JSON_DB_PATH, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: database file not found")
        return {'users': []}
    except json.JSONDecodeError:
        print("Error: invalid JSON format")
        return {'users': []}

def save_database(data: Dict) -> bool:
    """Save data to JSON file."""
    try:
        with open(Config.JSON_DB_PATH, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving database: {str(e)}")
        return False

def verify_username(input_username: str) -> Optional[Dict]:
    """Verify username exists in database."""
    data = load_database()
    return next((user for user in data['users'] if user['username'] == input_username), None)

def add_user(username: str, name: str) -> Tuple[bool, str]:
    """Add new user to database with unique QR string."""
    if not username or not name:
        return False, "Username and name are required"
    
    data = load_database()
    
    if any(user['username'] == username for user in data['users']):
        return False, "Username already exists"
    
    try:
        users = data['users']
        new_user_id = str(int(users[-1]["ID"]) + 1) if users else "1"
        qr_string = generate_random_string(32)
        
        data['users'].append({
            'username': username,
            'Name': name,
            'ID': new_user_id,
            'qr_string': qr_string
        })
        
        if save_database(data):
            return True, "User added successfully"
        return False, "Error saving user data"
    except Exception as e:
        return False, f"Error adding user: {str(e)}"
