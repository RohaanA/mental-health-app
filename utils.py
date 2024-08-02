import os
import json
from datetime import datetime
"""_summary_
This function is used to store user reports in their respective JSON files.
"""
def save_report(username, report):
    # Define the path for the user's JSON file
    file_path = os.path.join('stats', f'{username}.json')
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Read existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        # Initialize an empty list if file does not exist
        data = []
    
    # Append the new report with a timestamp
    timestamp = datetime.now().isoformat()
    data.append({
        'timestamp': timestamp,
        'report': report
    })
    
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_path(username):
    return os.path.join('stats', f'{username}.json')