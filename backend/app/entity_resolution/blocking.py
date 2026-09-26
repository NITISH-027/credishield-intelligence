from typing import List, Set
from .normalizer import normalize_company_name, get_token_fingerprint

def generate_blocking_keys(name: str, state: str = None, cin: str = None) -> Set[str]:
    """
    Generates blocking keys inspired by record-linkage best practices.
    """
    keys = set()
    norm = normalize_company_name(name)
    tokens = norm.split()
    
    if tokens:
        # Key 1: First token
        keys.add(f"tok1:{tokens[0]}")
        # Key 2: First 4 chars of normalized name
        if len(norm) >= 3:
            keys.add(f"pref:{norm[:4]}")
        # Key 3: Token fingerprint prefix
        fingerprint = get_token_fingerprint(name)
        if fingerprint:
            keys.add(f"fp:{fingerprint[:6]}")
            
    # Key 4: State code if provided
    if state:
        keys.add(f"st:{state.lower()[:3]}")
        
    # Key 5: CIN prefix (ROC/State)
    if cin and len(cin) >= 8:
        keys.add(f"cin_roc:{cin[6:8]}")
        
    return keys
