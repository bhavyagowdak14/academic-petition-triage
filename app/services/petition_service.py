from app.agents.petition_intake_agent import validate_petition
from app.agents.rule_analysis_agent import analyze_petition
from app.agents.evidence_assessment_agent import assess_evidence
from app.agents.triage_coordinator_agent import coordinate_triage
from app.services.regulation_search import RegulationSearch
from app.services.monitoring_service import log_workflow_event


_regulation_search = None


def get_regulation_search():
    global _regulation_search

    if _regulation_search is None:
        _regulation_search = RegulationSearch()

    return _regulation_search


def analyze_submitted_petition(petition: dict) -> dict:
    """Run the multi-agent triage workflow with monitoring."""

    petition_id = str(petition.get("student_id", "unknown"))

    try:
        # Agent 1: Validate petition information.
        intake_result = validate_petition(petition)

        # Agent 2: Assess whether supporting evidence is indicated.
        evidence_result = assess_evidence(petition)

        # Stop if required information is missing.
        if intake_result["status"] != "valid":
            result = coordinate_triage(
                intake_result=intake_result,
                rule_result={
                    "assessment": "insufficient_information",
                    "recommendation": "refer_to_human_review",
                    "reasons": [
                        "Required petition information is missing."
                    ],
                },
                evidence_result=evidence_result,
            )

            result["reasons"] = [
                "Required petition information is missing."
            ]
            result["evidence"] = []

            log_workflow_event(
                event="petition_analysis",
                petition_id=petition_id,
                status="incomplete",
                details={
                    "assessment": result["assessment"],
                    "missing_fields": intake_result["missing_fields"],
                },
            )

            return result

        # Agent 3: Retrieve relevant regulatory passages.
        searcher = get_regulation_search()

        query = (
            "Academic attendance regulations and condonation provisions. "
            f"Petition type: {petition.get('petition_type', '')}. "
            f"Attendance: {petition.get('attendance_percentage', 'not provided')}. "
            f"Reason: {petition.get('reason', '')}. "
            "Find the minimum attendance rule, permitted shortage, "
            "valid grounds, documentary evidence, and approval authority."
        )

        retrieved_clauses = searcher.search(query, top_k=12)

        # Agent 4: Analyze the petition against retrieved clauses.
        rule_result = analyze_petition(
            petition=petition,
            retrieved_clauses=retrieved_clauses,
        )

        # Agent 5: Coordinate the agent results.
        result = coordinate_triage(
            intake_result=intake_result,
            rule_result=rule_result,
            evidence_result=evidence_result,
        )

        result["reasons"] = rule_result.get("reasons", [])

        # Attach source passages for reviewer inspection.
        result["evidence"] = [
            {
                "source": clause["source"],
                "page": clause["page"],
                "chunk_id": clause["chunk_id"],
                "text": clause["text"],
                "similarity": clause["similarity"],
            }
            for clause in retrieved_clauses
        ]

        # Log the completed analysis without recording the full petition.
        log_workflow_event(
            event="petition_analysis",
            petition_id=petition_id,
            status="success",
            details={
                "assessment": result["assessment"],
                "recommendation": result["recommendation"],
                "retrieved_clause_count": len(retrieved_clauses),
            },
        )

        return result

    except Exception as exc:
        # Record the error, then allow the API to handle it.
        log_workflow_event(
            event="petition_analysis",
            petition_id=petition_id,
            status="error",
            details={
                "error_type": type(exc).__name__,
            },
        )
        raise