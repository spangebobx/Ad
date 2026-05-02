from flask import Flask, render_template, request, jsonify
import threading
from roblox_handler import RobloxSession
from inventory_scanner import scan_adopt_me_inventory
from value_fetcher import get_pet_values
import queue

app = Flask(__name__)

# Global state
active_sessions = []
results_cache = {}
task_queue = queue.Queue()
MAX_CONCURRENT = 2

def process_account(cookie):
    """Process single account: login -> launch -> scan -> value lookup"""
    try:
        session = RobloxSession(cookie)
        if not session.authenticate():
            return {"error": "Authentication failed", "cookie": cookie[:20] + "..."}
        
        username = session.get_username()
        pets = scan_adopt_me_inventory(session)
        
        # Enrich with values from elvebredd
        valued_pets = get_pet_values(pets)
        
        return {
            "username": username,
            "pets": valued_pets,
            "total_value": sum(p.get("value", 0) for p in valued_pets)
        }
    except Exception as e:
        return {"error": str(e), "cookie": cookie[:20] + "..."}

def worker():
    """Background worker to process accounts with max 2 concurrent"""
    while True:
        cookie = task_queue.get()
        if cookie is None:
            break
        
        result = process_account(cookie)
        results_cache[cookie] = result
        task_queue.task_done()

# Start worker threads
for _ in range(MAX_CONCURRENT):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    """Endpoint to submit cookies for scanning"""
    data = request.json
    cookies = data.get('cookies', [])
    
    # Clear previous results
    results_cache.clear()
    
    # Queue all cookies
    for cookie in cookies:
        task_queue.put(cookie.strip())
    
    return jsonify({"status": "queued", "count": len(cookies)})

@app.route('/results', methods=['GET'])
def results():
    """Fetch current results"""
    return jsonify(list(results_cache.values()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
