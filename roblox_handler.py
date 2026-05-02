import requests

class RobloxSession:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = requests.Session()
        self.username = None
        self.user_id = None
        
    def authenticate(self):
        """Authenticate using .ROBLOSECURITY cookie"""
        self.session.cookies.set('.ROBLOSECURITY', self.cookie, domain='.roblox.com')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.roblox.com/'
        }
        
        try:
            resp = self.session.get(
                'https://users.roblox.com/v1/users/authenticated',
                headers=headers,
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                self.username = data.get('name')
                self.user_id = data.get('id')
                return True
        except:
            pass
        
        return False
    
    def get_username(self):
        return self.username
