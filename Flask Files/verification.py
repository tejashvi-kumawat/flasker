from flask import Flask, request, jsonify
import json

app = Flask(__name__)

json_file = 'sample.json'

@app.route('/verify_qr', methods=['POST'])
def verify_qr():
    """Handles QR code verification."""
    data = request.get_json()  # Get the QR code string from the client
    
    if not data:
        print("No data received in the request.")
        return jsonify({"status": "error", "message": "No data received"}), 400

    qr_string = data.get('qr_string')
    
    if not qr_string:
        print("QR string is missing.")
        return jsonify({"status": "error", "message": "QR string not provided"}), 400
    
    try:
        # Open the JSON file and search for the QR code
        with open(json_file, 'r') as file:
            users_data = json.load(file)
        
        print(f"Users data: {users_data}")  # Debugging output to check if data is being loaded properly
        
        # Search for the user by the QR string
        user_found = False
        for user in users_data["users"]:
            if user["qr_string"] == qr_string:
                user_found = True
                if user.get("verified", False):
                    print(f"User with QR code {qr_string} is already verified.")
                    return jsonify({"status": "already_verified", "message": "User already verified"})
                
                # Mark the user as verified
                user["verified"] = True
                print(f"User with QR code {qr_string} verified.")
                
                # Write the updated data back to the JSON file
                with open(json_file, 'w') as file:
                    json.dump(users_data, file, indent=4)
                
                return jsonify({"status": "verified", "message": "QR Code Verification Successful"})
        
        if not user_found:
            print(f"QR Code {qr_string} not found in the data.")
            return jsonify({"status": "not_found", "message": "QR Code not found"}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Error verifying QR code"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)