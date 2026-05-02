import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_elvebredd_values():
    """
    Scrape comprehensive pet values from elvebredd calculator
    Returns dict of {pet_name: value}
    """
    value_map = {}
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get('https://elvebredd.com/adopt-me-calculator', headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Method 1: Try to find JSON data embedded in page
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'petData' in script.string:
                # Extract JSON pet data if embedded
                match = re.search(r'petData\s*=\s*(\{.*?\}|\[.*?\])', script.string, re.DOTALL)
                if match:
                    pet_data = json.loads(match.group(1))
                    for pet in pet_data:
                        name = pet.get('name', '')
                        value = float(pet.get('value', 0))
                        if value >= 5:  # Filter out under 5
                            value_map[name] = value
                    return value_map
        
        # Method 2: Scrape from HTML table/divs
        # Inspect their actual HTML structure and adjust selectors
        pet_rows = soup.select('[class*="pet"]')  # Adjust selector based on actual page
        
        for row in pet_rows:
            name_elem = row.select_one('[class*="name"]')
            value_elem = row.select_one('[class*="value"], [class*="worth"]')
            
            if name_elem and value_elem:
                name = name_elem.get_text(strip=True)
                value_text = value_elem.get_text(strip=True)
                
                # Extract numeric value
                value_match = re.search(r'([\d.]+)', value_text)
                if value_match:
                    value = float(value_match.group(1))
                    if value >= 5:
                        value_map[name] = value
        
        # Method 3: Fallback to manually curated high-value pets
        if not value_map:
            value_map = build_fallback_values()
        
        return value_map
        
    except Exception as e:
        print(f"Elvebredd scrape error: {e}")
        return build_fallback_values()


def build_fallback_values():
    """
    Manually curated Adopt Me pet values (5+)
    Updated as of common trading values
    """
    return {
        # Mega Neon Legendaries
        'Mega Neon Shadow Dragon': 600.0,
        'Mega Neon Bat Dragon': 540.0,
        'Mega Neon Giraffe': 480.0,
        'Mega Neon Frost Dragon': 400.0,
        'Mega Neon Owl': 320.0,
        'Mega Neon Parrot': 280.0,
        'Mega Neon Evil Unicorn': 240.0,
        'Mega Neon Crow': 220.0,
        'Mega Neon Arctic Reindeer': 160.0,
        'Mega Neon Turtle': 140.0,
        'Mega Neon Kangaroo': 130.0,
        'Mega Neon Albino Monkey': 125.0,
        'Mega Neon Flamingo': 120.0,
        'Mega Neon Dalmatian': 115.0,
        'Mega Neon Lion': 110.0,
        'Mega Neon Monkey King': 105.0,
        'Mega Neon Blue Dog': 100.0,
        'Mega Neon Pink Cat': 95.0,
        'Mega Neon Hedgehog': 90.0,
        'Mega Neon Queen Bee': 85.0,
        'Mega Neon King Bee': 80.0,
        'Mega Neon Skele-Rex': 75.0,
        'Mega Neon Fury': 70.0,
        'Mega Neon Phoenix': 65.0,
        'Mega Neon Shark': 60.0,
        'Mega Neon Octopus': 58.0,
        'Mega Neon Golden Rat': 55.0,
        'Mega Neon Dodo': 52.0,
        'Mega Neon T-Rex': 50.0,
        
        # Neon Legendaries
        'Neon Shadow Dragon': 150.0,
        'Neon Bat Dragon': 135.0,
        'Neon Giraffe': 120.0,
        'Neon Frost Dragon': 100.0,
        'Neon Owl': 80.0,
        'Neon Parrot': 70.0,
        'Neon Evil Unicorn': 60.0,
        'Neon Crow': 55.0,
        'Neon Arctic Reindeer': 40.0,
        'Neon Turtle': 35.0,
        'Neon Kangaroo': 32.0,
        'Neon Albino Monkey': 31.0,
        'Neon Flamingo': 30.0,
        'Neon Dalmatian': 28.0,
        'Neon Lion': 27.0,
        'Neon Monkey King': 26.0,
        'Neon Blue Dog': 25.0,
        'Neon Pink Cat': 24.0,
        'Neon Hedgehog': 22.0,
        'Neon Queen Bee': 21.0,
        'Neon King Bee': 20.0,
        'Neon Skele-Rex': 18.0,
        'Neon Fury': 17.0,
        'Neon Phoenix': 16.0,
        'Neon Shark': 15.0,
        'Neon Octopus': 14.0,
        'Neon Golden Rat': 13.0,
        'Neon Dodo': 12.0,
        'Neon T-Rex': 11.0,
        'Neon Snow Owl': 10.0,
        'Neon Metal Ox': 9.0,
        'Neon Guardian Lion': 8.0,
        'Neon Cerberus': 7.0,
        'Neon Kitsune': 6.0,
        'Neon Robo Dog': 5.5,
        'Neon Griffin': 5.0,
        
        # Regular Legendaries
        'Shadow Dragon': 150.0,
        'Bat Dragon': 135.0,
        'Giraffe': 120.0,
        'Frost Dragon': 100.0,
        'Owl': 80.0,
        'Parrot': 70.0,
        'Evil Unicorn': 60.0,
        'Crow': 55.0,
        'Arctic Reindeer': 40.0,
        'Turtle': 35.0,
        'Kangaroo': 32.0,
        'Albino Monkey': 31.0,
        'Flamingo': 30.0,
        'Dalmatian': 28.0,
        'Lion': 27.0,
        'Monkey King': 26.0,
        'Blue Dog': 25.0,
        'Pink Cat': 24.0,
        'Hedgehog': 22.0,
        'Queen Bee': 21.0,
        'King Bee': 20.0,
        'Lavender Dragon': 18.0,
        'Diamond Ladybug': 17.0,
        'Skele-Rex': 16.0,
        'Frost Fury': 15.0,
        'Phoenix': 14.0,
        'Shark': 13.0,
        'Octopus': 12.0,
        'Golden Rat': 11.0,
        'Dodo': 10.0,
        'T-Rex': 9.0,
        'Snow Owl': 8.0,
        'Metal Ox': 7.0,
        'Guardian Lion': 6.5,
        'Cerberus': 6.0,
        'Kitsune': 5.5,
        'Robo Dog': 5.0,
        
        # High-value Ultra Rares
        'Elephant': 15.0,
        'Cow': 12.0,
        'Pig': 10.0,
        'Meerkat': 9.0,
        'Wild Boar': 8.0,
        'Rhino': 7.5,
        'Chicken': 7.0,
        'Platypus': 6.5,
        'Brown Bear': 6.0,
        'Llama': 5.5,
        'Turkey': 5.0,
    }


def get_pet_values(pets):
    """
    Enrich pet list with current trade values
    Filters out pets under 5 value
    """
    value_map = scrape_elvebredd_values()
    valued_pets = []
    
    for pet in pets:
        pet_name = pet.get('name', '')
        matched_value = 0
        matched_name = None
        
        # Fuzzy matching - check if any known pet is in the name
        for known_pet, value in value_map.items():
            if known_pet.lower() in pet_name.lower():
                if value > matched_value:  # Take highest match
                    matched_value = value
                    matched_name = known_pet
        
        # Only include if value >= 5
        if matched_value >= 5:
            pet['value'] = matched_value
            pet['matched_name'] = matched_name or pet_name
            pet['total'] = matched_value * pet.get('quantity', 1)
            valued_pets.append(pet)
    
    return valued_pets
