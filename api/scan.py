from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from roblox_handler import RobloxSession
from inventory_scanner import scan_adopt_me_inventory
from value_fetcher import get_pet_values

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse request body
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)
        
        cookies = data.get('cookies', [])
        results = []
        
        # Process each cookie (max 10 to avoid timeout)
        for cookie in cookies[:10]:
            try:
                session = RobloxSession(cookie.strip())
                if not session.authenticate():
                    results.append({
                        "error": "Authentication failed",
                        "cookie": cookie[:20] + "..."
                    })
                    continue
                
                username = session.get_username()
                pets = scan_adopt_me_inventory(session)
                valued_pets = get_pet_values(pets)
                
                results.append({
                    "username": username,
                    "pets": valued_pets,
                    "total_value": sum(p.get("value", 0) for p in valued_pets)
                })
            except Exception as e:
                results.append({
                    "error": str(e),
                    "cookie": cookie[:20] + "..."
                })
        
        self.wfile.write(json.dumps(results).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
