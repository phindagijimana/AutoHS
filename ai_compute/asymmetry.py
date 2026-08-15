"""Hippocampal asymmetry calculations for AutoHS."""

LEFT_HS_THRESHOLD = -0.070839747728063
RIGHT_HS_THRESHOLD = 0.046915816971433


def calculate_asymmetry_index(left_volume: float, right_volume: float) -> float:
    """AI = (L - R) / (L + R)."""
    denom = left_volume + right_volume
    if denom == 0:
        return 0.0
    return round((left_volume - right_volume) / denom, 4)


def classify_laterality(asymmetry_index: float, threshold: float = 0.05) -> str:
    if asymmetry_index > threshold:
        return "Left > Right"
    if asymmetry_index < -threshold:
        return "Right > Left"
    return "Symmetric"


def classify_hs_laterality(asymmetry_index: float) -> str:
    if asymmetry_index > RIGHT_HS_THRESHOLD:
        return "Left-dominant (Right HS suspected)"
    if asymmetry_index < LEFT_HS_THRESHOLD:
        return "Right-dominant (Left HS suspected)"
    return "Balanced (No HS)"


def build_metrics(left_mm3: float, right_mm3: float) -> dict:
    ai = calculate_asymmetry_index(left_mm3, right_mm3)
    return {
        "left_hippocampus_mm3": round(left_mm3, 2),
        "right_hippocampus_mm3": round(right_mm3, 2),
        "asymmetry_index": ai,
        "laterality": classify_laterality(ai),
        "hs_classification": classify_hs_laterality(ai),
        "left_hs_threshold": LEFT_HS_THRESHOLD,
        "right_hs_threshold": RIGHT_HS_THRESHOLD,
    }
