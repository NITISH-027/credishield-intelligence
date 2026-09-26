import re
import string

LEGAL_SUFFIXES = [
    r"\bprivate limited\b",
    r"\bpvt\.?\s*ltd\.?\b",
    r"\bpvt\b",
    r"\blimited\b",
    r"\bltd\.?\b",
    r"\bllp\b",
    r"\blimited liability partnership\b",
    r"\bopc\b",
    r"\bone person company\b",
    r"\bcorporation\b",
    r"\bcorp\.?\b",
    r"\binc\.?\b",
    r"\bincorporated\b",
    r"\bco\.?\b",
    r"\bcompany\b",
    r"\benterprise[s]?\b",
    r"\bindustr(y|ies)\b",
    r"\btechnolog(y|ies)\b",
    r"\bservices\b",
    r"\bsolutions\b",
    r"\bindia\b",
]

def normalize_company_name(name: str) -> str:
    """
    Normalizes company name for robust entity resolution matching.
    Strips Indian legal corporate forms (Pvt Ltd, Ltd, LLP), punctuation,
    casing, and redundant words.
    """
    if not name:
        return ""
    
    text = name.lower().strip()
    
    # Replace ampersands with 'and'
    text = re.sub(r"\s*&\s*", " and ", text)
    
    # Remove legal suffixes
    for suffix_pattern in LEGAL_SUFFIXES:
        text = re.sub(suffix_pattern, "", text, flags=re.IGNORECASE)
        
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Normalize whitespaces
    tokens = [t for t in text.split() if t]
    
    return " ".join(tokens)

def get_token_fingerprint(name: str) -> str:
    """
    Sorts distinctive tokens alphabetically to handle word order variations.
    e.g., 'ABC Manufacturing' vs 'Manufacturing ABC'
    """
    norm = normalize_company_name(name)
    tokens = sorted(list(set(norm.split())))
    return " ".join(tokens)

def normalize_cin(cin: str) -> str:
    """
    Normalizes Indian 21-digit Corporate Identity Number (CIN).
    Format: U/L + 5 digits + 2 state letters + 4 year digits + PTC/PLC/LLP + 6 registration digits.
    e.g. U72200MH2015PTC123456
    """
    if not cin:
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", cin).upper()

def normalize_gstin(gstin: str) -> str:
    """
    Normalizes 15-character GSTIN.
    """
    if not gstin:
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", gstin).upper()
