"""Hippocampal asymmetry calculations for AutoHS."""

LATERALITY_THRESHOLD = 0.05
LEFT_HS_THRESHOLD = -0.070839747728063
RIGHT_HS_THRESHOLD = 0.046915816971433


def threshold_guide() -> str:
    """Interpretation rules for NeuroInsight-AutoHS (AutoHS pipeline step 2)."""
    return (
        f"Volume laterality (threshold ±{LATERALITY_THRESHOLD}):\n"
        f"• Left > Right if AI > {LATERALITY_THRESHOLD}\n"
        f"• Right > Left if AI < {-LATERALITY_THRESHOLD}\n"
        f"• Symmetric if {-LATERALITY_THRESHOLD} ≤ AI ≤ {LATERALITY_THRESHOLD}\n"
        f"\nHS classification:\n"
        f"• Left HS (Right-dominant) if AI < {LEFT_HS_THRESHOLD:.12f}\n"
        f"• Right HS (Left-dominant) if AI > {RIGHT_HS_THRESHOLD:.12f}\n"
        f"• No HS (Balanced) otherwise"
    )


def calculate_asymmetry_index(left_volume: float, right_volume: float) -> float:
    """AI = (L - R) / (L + R)."""
    denom = left_volume + right_volume
    if denom == 0:
        return 0.0
    return round((left_volume - right_volume) / denom, 4)


def classify_laterality(
    asymmetry_index: float, threshold: float = LATERALITY_THRESHOLD
) -> str:
    if asymmetry_index > threshold:
        return "Left > Right"
    if asymmetry_index < -threshold:
        return "Right > Left"
    return "Symmetric"


def classify_hs_laterality(asymmetry_index: float) -> str:
    if asymmetry_index > RIGHT_HS_THRESHOLD:
        classification = "Left-dominant (Right HS suspected)"
    elif asymmetry_index < LEFT_HS_THRESHOLD:
        classification = "Right-dominant (Left HS suspected)"
    else:
        classification = "Balanced (No HS)"

    thresholds_info = (
        f"Thresholds:\n\n"
        f"• Left HS (Right-dominant) if AI < {LEFT_HS_THRESHOLD:.12f}\n"
        f"• Right HS (Left-dominant) if AI > {RIGHT_HS_THRESHOLD:.12f}\n"
        f"• No HS (Balanced) otherwise."
    )
    return f"{classification}\n\n{thresholds_info}"


def build_metrics(left_mm3: float, right_mm3: float) -> dict:
    ai = calculate_asymmetry_index(left_mm3, right_mm3)
    return {
        "left_hippocampus_mm3": round(left_mm3, 2),
        "right_hippocampus_mm3": round(right_mm3, 2),
        "asymmetry_index": ai,
        "laterality": classify_laterality(ai),
        "laterality_threshold": LATERALITY_THRESHOLD,
        "hs_classification": classify_hs_laterality(ai),
        "left_hs_threshold": LEFT_HS_THRESHOLD,
        "right_hs_threshold": RIGHT_HS_THRESHOLD,
        "interpretation": threshold_guide(),
    }
