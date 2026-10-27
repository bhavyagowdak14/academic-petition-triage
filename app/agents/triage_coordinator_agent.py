from typing import Any


def coordinate_triage(
    intake_result: dict[str, Any],
    rule_result: dict[str, Any],
    evidence_result: dict[str, Any],
) -> dict[str, Any]:
    """Combine agent outputs into a review-ready triage report."""

    if intake_result["status"] != "valid":
        assessment = "incomplete_petition"
        recommendation = "request_missing_information"

    else:
        assessment = rule_result.get(
            "assessment",
            "insufficient_regulatory_evidence",
        )
        recommendation = rule_result.get(
            "recommendation",
            "refer_to_human_review",
        )

    return {
        "workflow": "academic_petition_multi_agent_triage",
        "agent_results": {
            "intake": intake_result,
            "rule_analysis": rule_result,
            "evidence_assessment": evidence_result,
        },
        "assessment": assessment,
        "recommendation": recommendation,
        "final_decision": "pending_human_review",
        "human_review_required": True,
    }