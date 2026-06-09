from humanward_ai.safe_sharing import classify_sharing, SharingDecision

def test_public_safe_content():
    result = classify_sharing("This is a public standards alignment summary.")
    assert result.decision == SharingDecision.PUBLIC_SAFE

def test_private_restricted_for_personal_data():
    result = classify_sharing("Contains phone number and date of birth.")
    assert result.decision == SharingDecision.PRIVATE_RESTRICTED

def test_dangerous_restricted_for_misuse():
    result = classify_sharing("This includes an exploit chain and malware details.")
    assert result.decision == SharingDecision.DANGEROUS_RESTRICTED

def test_controlled_review_for_red_team():
    result = classify_sharing("This red-team model failure needs review.")
    assert result.decision == SharingDecision.CONTROLLED_REVIEW
