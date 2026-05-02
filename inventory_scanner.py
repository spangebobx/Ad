import requests
import time

def scan_adopt_me_inventory(roblox_session):
    """
    Comprehensive Adopt Me inventory scan
    Uses multiple methods to catch all pets
    """
    user_id = roblox_session.user_id
    pets = []
    
    # Method 1: Game passes (some pets stored here)
    pets.extend(scan_game_passes(roblox_session, user_id))
    
    # Method 2: Collectibles inventory
    pets.extend(scan_collectibles(roblox_session, user_id))
    
    # Method 3: Badge holders (sometimes pet ownership tracked via badges)
    pets.extend(scan_badges(roblox_session, user_id))
    
    # Deduplicate
    seen = set()
    unique_pets = []
    for pet in pets:
        key = (pet['name'], pet['id'])
        if key not in seen:
            seen.add(key)
            unique_pets.append(pet)
    
    return unique_pets


def scan_game_passes(session, user_id):
    """Scan game passes inventory"""
    url = f'https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles'
    params = {'assetType': 'GamePass', 'sortOrder': 'Asc', 'limit': 100}
    
    pets = []
    try:
        resp = session.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get('data', []):
                if 'adopt me' in item.get('name', '').lower():
                    pets.append({
                        'name': item.get('name'),
                        'id': item.get('assetId'),
                        'quantity': item.get('quantity', 1)
                    })
    except:
        pass
    
    return pets


def scan_collectibles(session, user_id):
    """Scan collectibles inventory (primary method for Adopt Me)"""
    url = f'https://inventory.roblox.com/v2/users/{user_id}/inventory'
    params = {'assetTypes': 'All', 'limit': 100}
    
    pets = []
    try:
        resp = session.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get('data', []):
                name = item.get('name', '')
                # Filter for pet-like items
                pet_keywords = ['dragon', 'unicorn', 'owl', 'parrot', 'turtle', 
                               'kangaroo', 'frost', 'shadow', 'bat', 'giraffe',
                               'evil', 'crow', 'arctic', 'monkey', 'flamingo',
                               'dalmatian', 'lion', 'hedgehog', 'bee', 'cat',
                               'dog', 'elephant', 'cow', 'pig', 'neon', 'mega']
                
                if any(keyword in name.lower() for keyword in pet_keywords):
                    pets.append({
                        'name': name,
                        'id': item.get('assetId'),
                        'quantity': 1
                    })
    except:
        pass
    
    return pets


def scan_badges(session, user_id):
    """Scan badge inventory for pet ownership markers"""
    url = f'https://badges.roblox.com/v1/users/{user_id}/badges'
    params = {'limit': 100}
    
    pets = []
    try:
        resp = session.session.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            for badge in data.get('data', []):
                name = badge.get('name', '')
                if 'adopt me' in name.lower() and ('pet' in name.lower() or 'hatch' in name.lower()):
                    # Extract pet name from badge
                    pets.append({
                        'name': name,
                        'id': badge.get('id'),
                        'quantity': 1
                    })
    except:
        pass
    
    return pets
