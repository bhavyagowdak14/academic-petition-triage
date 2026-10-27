# Academic Regulation and Student Petition Triage Service

## 1. Project Overview

The Academic Petition Triage Service is an evidence-based application that helps organize and analyze academic petitions using official university regulations.

The system retrieves relevant regulatory passages, checks petition information against identified rules, assesses whether supporting evidence has been indicated, and prepares a structured recommendation for authorized human review.

**The system does not make final university decisions.** All final decisions remain with authorized university officers.

## 2. Key Features

* Petition submission and input validation.
* Retrieval-Augmented Generation (RAG)-style semantic retrieval over regulatory documents.
* Semantic embeddings generated using Sentence Transformers.
* Similarity search using FAISS.
* Rule-based attendance and condonation analysis.
* Evidence-reference assessment.
* Multi-agent workflow orchestration.
* Source passages returned for reviewer inspection.
* Structured monitoring logs.
* FastAPI endpoints and interactive Swagger documentation.
* Docker-based deployment.
* Automated unit and API tests.

## 3. Architecture

The workflow consists of the following components:

1. **Petition Intake Agent:** Checks whether required petition information is present.
2. **Regulation Retrieval:** Searches the processed VTU regulation corpus for relevant passages.
3. **Rule Analysis Agent:** Evaluates the reported attendance, stated reason, and available regulatory evidence.
4. **Evidence Assessment Agent:** Identifies whether supporting evidence has been indicated. It does not independently authenticate documents.
5. **Triage Coordinator:** Combines agent outputs into a structured triage report.
6. **Monitoring Service:** Records workflow events and outcomes.

The FastAPI application exposes the workflow through HTTP endpoints. Docker packages the application and its dependencies into a container.

## 4. Technology Stack

* Python 3.11
* FastAPI
* Pydantic
* Sentence Transformers
* FAISS
* PyPDF
* Pytest
* Docker
* Docker Compose

## 5. Project Structure

```text
academic-petition-triage/
├── app/
│   ├── agents/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── corpus/
│   ├── regulations/
│   └── processed/
├── logs/
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## 6. Running the Application with Docker

Ensure Docker Desktop is running.

Build the image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

Check container status:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs --tail 100 petition-api
```

Stop the application:

```bash
docker compose down
```

## 7. API Endpoints

| Method | Endpoint             | Purpose                                      |
| ------ | -------------------- | -------------------------------------------- |
| GET    | `/`                  | Application status                           |
| GET    | `/health`            | Health check                                 |
| POST   | `/petitions/submit`  | Submit a petition                            |
| POST   | `/petitions/analyze` | Analyze a petition and return triage results |

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## 8. Example Analysis Request

```json
{
  "student_id": "STU002",
  "petition_type": "Attendance Condonation",
  "semester": 3,
  "reason": "I was absent due to a medical emergency and request consideration of my attendance shortage.",
  "attendance_percentage": 78.5,
  "supporting_evidence": "medical_certificate.pdf"
}
```

The evidence filename is a reference supplied by the requester. Its presence does not mean that the file exists, is authentic, or has been verified.

## 9. Testing

Run the automated test suite:

```bash
python -m pytest tests -v
```

The current test suite contains eight passing tests covering petition validation, evidence handling, rule analysis, API responses, and invalid attendance input.

These results demonstrate the tested behaviors; they do not establish regulatory correctness for every possible petition.

## 10. Monitoring

Workflow events are recorded as structured JSON lines in:

`logs/petition_monitoring.log`

The Docker deployment uses a named volume for application logs.

## 11. Limitations and Human Oversight

* The current rule-analysis implementation uses deterministic Python logic.
* Semantic retrieval may return irrelevant or incomplete passages.
* Evidence references are not independently authenticated.
* Retrieval and analysis require broader evaluation before production use.
* Regulatory changes require the corpus and index to be updated.
* The service provides triage recommendations, not official decisions.
* Final decisions remain with authorized university officers.

## 12. Future Improvements

* Broader evaluation of retrieval precision and recall.
* More comprehensive regulatory rule coverage.
* Evidence document upload and validation.
* Improved monitoring dashboards and performance metrics.
* Authentication, authorization, and privacy controls.
* Automated detection of outdated regulatory documents.
* Additional integration and end-to-end tests.
