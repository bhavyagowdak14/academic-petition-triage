from app.agents.petition_intake_agent import validate_petition
from app.agents.evidence_assessment_agent import assess_evidence
from app.agents.rule_analysis_agent import analyze_petition


def test_valid_petition():
    petition = {
        "student_id": "STU001",
        "petition_type": "Attendance Condonation",
        "semester": 3,
        "reason": "Medical emergency caused absence.",
        "attendance_percentage": 78.5,
        "supporting_evidence": "medical_certificate.pdf",
    }

    result = validate_petition(petition)

    assert result["status"] == "valid"
    assert result["missing_fields"] == []


def test_missing_evidence():
    petition = {
        "supporting_evidence": None,
    }

    result = assess_evidence(petition)

    assert result["status"] == "evidence_missing"
    assert result["verified"] is False


def test_evidence_indicated():
    petition = {
        "supporting_evidence": "medical_certificate.pdf",
    }

    result = assess_evidence(petition)

    assert result["status"] == "evidence_indicated"
    assert result["verified"] is False


def test_attendance_condonation_review():
    petition = {
        "student_id": "STU002",
        "petition_type": "Attendance Condonation",
        "semester": 3,
        "reason": (
            "I was absent due to a medical emergency "
            "and request consideration of my attendance shortage."
        ),
        "attendance_percentage": 78.5,
        "supporting_evidence": "medical_certificate.pdf",
    }

    clauses = [
        {
            "text": (
                "A student is required to secure a minimum "
                "attendance of 85 % in each registered course."
            )
        },
        {
            "text": (
                "If attendance falls below 85 %, a shortage up to "
                "a maximum of 10 % may be condoned by the "
                "Vice-Chancellor on valid grounds such as medical "
                "reasons. All such cases shall be supported by "
                "valid documentary evidence."
            )
        },
    ]

    result = analyze_petition(petition, clauses)

    assert (
        result["assessment"]
        == "potentially_eligible_for_condonation_review"
    )
    assert result["final_decision"] == "pending_human_review"