def detect_strategy_ml(text, language="en"):
    """
    Simple rule-based + keyword strategy detection
    (ML-like behaviour for hackathon/demo)
    """

    if not text:
        return "No Strategy Defined"

    t = text.lower()

    # ---- Fake Gift / OTP Scam ----
    if any(k in t for k in [
        "otp", "one time password", "lottery",
        "gift", "prize", "congratulations", "reward",
        "केवाईसी", "इनाम", "लॉटरी", "उपहार"
    ]):
        return "Fake Gift / OTP Scam"

    # ---- Loan Fraud ----
    if any(k in t for k in [
        "loan", "instant loan", "processing fee",
        "emi", "interest rate", "credit score",
        "ऋण", "लोन", "किस्त"
    ]):
        return "Loan Fraud"

    # ---- Accident / Emergency Scam ----
    if any(k in t for k in [
        "accident", "hospital", "emergency",
        "urgent money", "medical",
        "दुर्घटना", "आपातकाल", "इलाज"
    ]):
        return "Accident Emergency Scam"

    return "No Strategy Defined"