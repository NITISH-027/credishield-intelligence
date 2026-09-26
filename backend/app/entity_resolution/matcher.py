import difflib
from typing import Dict, Any, List, Tuple
from .normalizer import normalize_company_name, get_token_fingerprint, normalize_cin, normalize_gstin
from ..schemas.entity import EntityMatchCandidate, EntityResolutionResult

def jaro_winkler_similarity(s1: str, s2: str) -> float:
    """
    Standard Jaro-Winkler similarity implementation.
    """
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    match1 = [False] * len1
    match2 = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if match2[j]:
                continue
            if s1[i] != s2[j]:
                continue
            match1[i] = True
            match2[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    transpositions = 0
    k = 0
    for i in range(len1):
        if not match1[i]:
            continue
        while not match2[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    transpositions //= 2
    jaro = (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0

    # Winkler prefix bonus (up to 4 chars)
    prefix = 0
    for i in range(min(4, min(len1, len2))):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    return jaro + prefix * 0.1 * (1.0 - jaro)

def calculate_token_overlap(s1: str, s2: str) -> float:
    toks1 = set(s1.split())
    toks2 = set(s2.split())
    if not toks1 or not toks2:
        return 0.0
    intersection = toks1.intersection(toks2)
    union = toks1.union(toks2)
    return len(intersection) / len(union)

def match_entities(query_name: str, candidate_record: Dict[str, Any], query_cin: str = None, query_gstin: str = None) -> Tuple[float, str, List[str]]:
    """
    Computes a multi-signal match confidence between search query and a buyer record.
    Returns: (confidence, status, match_signals)
    Status: MATCHED (>=0.88), LIKELY_MATCH (0.70-0.87), POSSIBLE_MATCH (0.50-0.69), UNRESOLVED (<0.50)
    """
    signals = []
    
    # 1. Deterministic Identifier Check (Gold Standard)
    if query_cin and candidate_record.get("cin"):
        if normalize_cin(query_cin) == normalize_cin(candidate_record.get("cin")):
            signals.append("Exact CIN (Corporate Identity Number) Match")
            return 1.0, "MATCHED", signals
            
    if query_gstin and candidate_record.get("gstin"):
        if normalize_gstin(query_gstin) == normalize_gstin(candidate_record.get("gstin")):
            signals.append("Exact GSTIN Match")
            return 1.0, "MATCHED", signals

    norm_query = normalize_company_name(query_name)
    norm_candidate = normalize_company_name(candidate_record.get("legal_name", ""))
    
    # Exact Normalized Name Match
    if norm_query and norm_query == norm_candidate:
        signals.append("Exact Normalized Legal Name Match")
        confidence = 0.95
        return confidence, "MATCHED", signals
        
    # Check historical/previous names
    for prev in candidate_record.get("previous_names") or []:
        if normalize_company_name(prev) == norm_query:
            signals.append(f"Matched Historical Legal Name: '{prev}'")
            return 0.92, "MATCHED", signals

    # 2. String Metrics
    jw = jaro_winkler_similarity(norm_query, norm_candidate)
    tok_overlap = calculate_token_overlap(norm_query, norm_candidate)
    difflib_ratio = difflib.SequenceMatcher(None, norm_query, norm_candidate).ratio()
    
    base_score = 0.5 * jw + 0.3 * tok_overlap + 0.2 * difflib_ratio
    signals.append(f"Name Jaro-Winkler: {jw:.2f}, Token Overlap: {tok_overlap:.2f}")

    # 3. Contextual Boosts (State, Trade Name, Suffixes)
    trade_name = candidate_record.get("trade_name")
    if trade_name and normalize_company_name(trade_name) in norm_query:
        base_score += 0.08
        signals.append(f"Trade name match: '{trade_name}'")
        
    confidence = min(0.99, max(0.0, base_score))
    
    # Categorization thresholds
    if confidence >= 0.88:
        status = "MATCHED"
    elif confidence >= 0.70:
        status = "LIKELY_MATCH"
    elif confidence >= 0.50:
        status = "POSSIBLE_MATCH"
    else:
        status = "UNRESOLVED"
        
    return round(confidence, 3), status, signals
