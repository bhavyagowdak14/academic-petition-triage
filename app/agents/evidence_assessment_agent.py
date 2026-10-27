from typing import Any


def assess_evidence(petition: dict[str, Any]) -> dict[str, Any]:
    """Assess whether evidence is indicated, without claiming to verify it."""

    evidence = petition.get("supporting_evidence")

    if isinstance(evidence, str):
        evidence = evidence.strip()

    if evidence:
        return {
            "agent": "evidence_assessment_agent",
            "status": "evidence_indicated",
            "evidence_reference": evidence,
            "verified": False,
            "message": (
                "Supporting evidence has been indicated, "
                "but its authenticity and validity have not been verified."
            ),
        }

    return {
        "agent": "evidence_assessment_agent",
        "status": "evidence_missing",
        "evidence_reference": None,
        "verified": False,
        "message": (
            "No supporting evidence was indicated. "
            "An authorized reviewer should assess whether evidence is required."
        ),
    }