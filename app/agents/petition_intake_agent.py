from typing import Any


REQUIRED_FIELDS = [
    "student_id",
    "petition_type",
    "semester",
    "reason",
]


def validate_petition(petition: dict[str, Any]) -> dict[str, Any]:
    """Check whether the petition contains the minimum required information."""

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if petition.get(field) is None
        or (
            isinstance(petition.get(field), str)
            and not petition[field].strip()
        )
    ]

    if missing_fields:
        return {
            "agent": "petition_intake_agent",
            "status": "incomplete",
            "missing_fields": missing_fields,
            "message": "The petition is missing required information.",
        }

    return {
        "agent": "petition_intake_agent",
        "status": "valid",
        "missing_fields": [],
        "message": "The petition contains the required fields.",
    }