from typing import Any


VALID_GROUNDS = {
    "medical": "Medical reasons",
    "nss": "Participation in NSS activities",
    "ncc": "Participation in NCC activities",
    "red cross": "Participation in Red Cross activities",
    "sports": "University, State, National or International level sports",
    "cultural": "University, State, National or International level cultural activities",
}


def analyze_petition(
    petition: dict[str, Any],
    retrieved_clauses: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Produce a preliminary, evidence-based assessment.

    This function does not make the university's final decision.
    """

    attendance = petition.get("attendance_percentage")
    reason = (petition.get("reason") or "").lower()
    evidence = petition.get("supporting_evidence")

    # Locate the relevant regulations in retrieved text.
    clauses = [
    clause
    for clause in retrieved_clauses
    if any(
        keyword in clause.get("text", "").lower()
        for keyword in (
            "attendance",
            "condoned",
            "condonation",
            "85 %",
            "85%",
        )
    )
]

    base_rule_found = any(
        "85 %" in clause.get("text", "")
        or "85%" in clause.get("text", "")
        for clause in clauses
    )

    condonation_rule_found = any(
        "condon" in clause.get("text", "").lower()
        and (
            "10 %" in clause.get("text", "")
         or "10%" in clause.get("text", "")
        )
        for clause in clauses
    )

    if attendance is None:
        return {
            "assessment": "insufficient_information",
            "recommendation": "refer_to_human_review",
            "reasons": [
                "Attendance percentage was not provided."
            ],
            "final_decision": "pending_human_review",
        }

    if not base_rule_found or not condonation_rule_found:
        return {
            "assessment": "insufficient_regulatory_evidence",
            "recommendation": "refer_to_human_review",
            "reasons": [
                "The retrieved passages do not establish both "
                "the base attendance rule and the condonation provision."
            ],
            "final_decision": "pending_human_review",
        }

    if attendance >= 85:
        return {
            "assessment": "minimum_attendance_threshold_met",
            "recommendation": "continue_eligibility_checks",
            "reasons": [
                "The reported attendance meets the 85% minimum "
                "in the retrieved regulation."
            ],
            "final_decision": "pending_human_review",
        }

    shortfall = 85 - attendance

    valid_ground = next(
        (
            description
            for keyword, description in VALID_GROUNDS.items()
            if keyword in reason
        ),
        None,
    )

    if shortfall <= 10 and valid_ground and evidence:
        return {
            "assessment": "potentially_eligible_for_condonation_review",
            "recommendation": "refer_to_authorized_approval_process",
            "reasons": [
                f"Reported attendance: {attendance}%.",
                f"Shortfall from 85%: {shortfall:.2f} percentage points.",
                f"Reported ground: {valid_ground}.",
                "Supporting evidence has been indicated but has not "
                "been independently verified.",
                "Condonation requires the prescribed recommendations "
                "and approval by the authorized university authority.",
            ],
            "final_decision": "pending_human_review",
        }

    return {
        "assessment": "condonation_conditions_not_established",
        "recommendation": "refer_to_human_review",
        "reasons": [
            f"Reported attendance: {attendance}%.",
            f"Shortfall from 85%: {shortfall:.2f} percentage points.",
            "The available petition information does not establish "
            "all conditions for consideration under the condonation provision."
        ],
        "final_decision": "pending_human_review",
    }

