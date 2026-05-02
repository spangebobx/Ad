import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class RobloxSession:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = requests.Session()
        self.username = None
        self.user_id = None
        
    def authenticate(self):
        """Authenticate using .ROBLOSECURITY cookie"""
        self.session.cookies.set('.ROBLOSECURITY', self.cookie, domain='.roblox.com')
        
        # Verify authentication
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = self.session.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            self.username = data.get('name')
            self.user_id = data.get('id')
            return True
        return False
    
    def get_username(self):
        return self.username
    
    def launch_adopt_me(self):
        """Launch Adopt Me game in headless browser"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Inject cookie into browser
        driver.get('https://www.roblox.com')
        driver.add_cookie({
            'name': '.ROBLOSECURITY',
            'value': self.cookie,
            'domain': '.roblox.com'
        })
        
        # Navigate to Adopt Me
        driver.get('https://www.roblox.com/games/920587237/Adopt-Me')
        time.sleep(3)  # Wait for page load
        
        return driver
