# Academic Regulation and Student Petition Triage Service

An evidence-based academic petition triage service that helps assess student petitions against university regulations using semantic search, rule analysis, evidence assessment, and a multi-agent workflow.

The system retrieves relevant regulatory passages and generates a structured preliminary assessment to support authorized university officers. **It does not make final approval or rejection decisions. All petitions requiring a decision remain subject to human review.**

---

## Table of Contents

* [Project Overview](#project-overview)
* [Problem Statement](#problem-statement)
* [Objectives](#objectives)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [System Workflow](#system-workflow)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [Installation and Setup](#installation-and-setup)
* [Running with Docker](#running-with-docker)
* [API Documentation](#api-documentation)
* [Example Petition Request](#example-petition-request)
* [Understanding the Output](#understanding-the-output)
* [Automated Testing](#automated-testing)
* [Monitoring and Logging](#monitoring-and-logging)
* [Screenshots](#screenshots)
* [Limitations](#limitations)
* [Future Enhancements](#future-enhancements)
* [Ethical Considerations](#ethical-considerations)
* [Author](#author)

---

## Project Overview

Academic institutions receive petitions from students for various academic circumstances, including attendance shortages, medical issues, and requests for regulatory exceptions.

Manually reviewing each petition against lengthy academic regulations can be time-consuming. Important clauses, eligibility conditions, supporting documents, and approval procedures must be considered before an authorized officer can make a decision.

The **Academic Regulation and Student Petition Triage Service** addresses this challenge by retrieving relevant regulation passages and organizing the available information into a structured preliminary assessment.

The system uses semantic search to find potentially relevant regulatory clauses and a multi-agent workflow to validate petition inputs, analyze applicable rules, assess the status of supporting evidence, and coordinate the resulting assessment.

The application is exposed through a REST API built with FastAPI and can be run using Docker.

### Project Scope

The current implementation focuses on academic petition triage, particularly attendance-condonation scenarios supported by the available regulation corpus and implemented rules.

It is intended to assist human reviewers, not replace university authorities.

---

## Problem Statement

Students submit academic petitions that must be assessed against institutional regulations and supporting evidence.

Manual assessment can involve:

* Locating the applicable academic regulation.
* Checking attendance requirements and condonation conditions.
* Identifying the grounds stated in the petition.
* Determining whether supporting evidence has been indicated.
* Identifying the appropriate approval process.
* Preparing a consistent summary for human review.

The proposed service helps organize these tasks through semantic retrieval, rule-based analysis, evidence assessment, and structured reporting.

---

## Objectives

1. Accept and validate academic petition information.
2. Search university regulation passages using semantic similarity.
3. Identify relevant rules and conditions for preliminary assessment.
4. Evaluate petition details against the implemented rules.
5. Identify whether supporting evidence has been indicated.
6. Produce a structured triage assessment and recommendation.
7. Preserve human oversight for official decisions.
8. Record monitoring events for petition-analysis operations.
9. Provide a containerized API that can be tested and extended.

---

## Key Features

### 1. Petition Intake and Validation

The API accepts petition details, including:

* Student identifier.
* Petition type.
* Semester.
* Reason for the petition.
* Attendance percentage, when applicable.
* Supporting evidence information.

Pydantic models validate the incoming request, including required fields and attendance-percentage constraints.

### 2. Semantic Regulation Search

The application processes the available regulation document into text chunks and searches for passages relevant to a submitted petition.

The retrieval service uses:

* Sentence Transformers for text embeddings.
* `sentence-transformers/all-MiniLM-L6-v2` as the embedding model.
* FAISS for similarity-based retrieval.
* Regulation source information and page metadata to help identify relevant passages.

The retrieved passages provide regulatory context for the preliminary assessment.

### 3. Rule Analysis

The rule-analysis component evaluates petition information against implemented academic rules.

For supported attendance-condonation scenarios, it can consider:

* The stated attendance percentage.
* The attendance requirement identified in the regulation.
* The stated reason for the petition.
* Potentially applicable condonation grounds.
* The presence of relevant regulatory passages.
* Whether further review is necessary.

The current implementation includes deterministic Python logic for supported rule-analysis scenarios.

### 4. Evidence Assessment

The evidence-assessment component considers the supporting evidence information supplied with a petition.

The system distinguishes between evidence being indicated and evidence being authenticated.

**An indicated medical certificate or other supporting document is not automatically considered verified.**

### 5. Multi-Agent Triage Workflow

The application organizes the assessment into separate components:

* Petition intake.
* Rule analysis.
* Evidence assessment.
* Triage coordination.

These components produce a structured preliminary assessment. The workflow should not be interpreted as a collection of independently operating autonomous AI agents or as an official university decision-making system.

### 6. Human Review

The service preserves a human-review requirement.

Its preliminary assessment can help an authorized reviewer understand the relevant regulation, petition circumstances, evidence status, and suggested next steps.

The service does not grant condonation or officially approve or reject petitions.

### 7. Monitoring and Logging

The application records petition-analysis events, including the analysis status and relevant summary information.

These logs help developers inspect execution and diagnose problems during testing.

### 8. Docker Support

The project includes a Dockerfile and Docker Compose configuration to simplify application startup and provide a consistent runtime environment.

---

## System Architecture

```text
+----------------------------------+
|          Student / Client        |
+----------------------------------+
                 |
                 v
+----------------------------------+
|          FastAPI REST API        |
|     Request Validation           |
+----------------------------------+
                 |
                 v
+----------------------------------+
|       Petition Intake Agent      |
+----------------------------------+
                 |
                 v
+----------------------------------+
|   Semantic Regulation Retrieval  |
|                                  |
|  Sentence Transformers           |
|  FAISS Similarity Search         |
|  Regulation Text and Metadata    |
+----------------------------------+
                 |
                 v
+----------------------------------+
|        Rule Analysis Agent       |
+----------------------------------+
                 |
                 v
+----------------------------------+
|      Evidence Assessment Agent   |
+----------------------------------+
                 |
                 v
+----------------------------------+
|        Triage Coordinator        |
+----------------------------------+
                 |
                 v
+----------------------------------+
|     Structured Triage Report     |
+----------------------------------+
                 |
                 v
+----------------------------------+
|      Authorized Human Review     |
+----------------------------------+

Monitoring Service records analysis events.
```

The architecture describes the application's logical processing flow. The individual components operate within the implemented application; the diagram does not imply that the system makes independent official decisions.

---

## System Workflow

The following sequence illustrates how a petition is processed.

```text
1. Student submits a petition
             |
             v
2. API validates the input
             |
             v
3. Petition Intake Agent processes
   the submitted information
             |
             v
4. Semantic search retrieves
   relevant regulation passages
             |
             v
5. Rule Analysis Agent examines
   applicable conditions
             |
             v
6. Evidence Assessment Agent
   evaluates indicated evidence
             |
             v
7. Triage Coordinator organizes
   the assessment
             |
             v
8. Structured preliminary report
   is returned by the API
             |
             v
9. Authorized human review
```

The retrieved regulatory passages provide context for the assessment. The final outcome remains the responsibility of the authorized university authority.

---

## Technology Stack

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| Python                | Main programming language           |
| FastAPI               | REST API development                |
| Pydantic              | Request validation and schemas      |
| Sentence Transformers | Text embedding generation           |
| `all-MiniLM-L6-v2`    | Semantic embedding model            |
| FAISS                 | Similarity-based vector retrieval   |
| LangGraph             | Workflow-related dependency         |
| PyPDF                 | PDF text extraction                 |
| Docker                | Application containerization        |
| Docker Compose        | Container startup and configuration |
| Pytest                | Automated testing                   |
| Python logging        | Monitoring and event logging        |

The table includes technologies declared by the project. The exact role and extent of use of each dependency should be verified against the current implementation.

---

## Project Structure

```text
academic-petition-triage/
│
├── app/
│   ├── agents/
│   │   ├── evidence_assessment_agent.py
│   │   ├── petition_intake_agent.py
│   │   ├── rule_analysis_agent.py
│   │   └── triage_coordinator_agent.py
│   │
│   ├── api/
│   ├── evaluation/
│   ├── ingestion/
│   │   └── ingest_regulations.py
│   │
│   ├── schemas/
│   │   └── petition.py
│   │
│   ├── services/
│   │   ├── monitoring_service.py
│   │   ├── petition_service.py
│   │   └── regulation_search.py
│   │
│   ├── tools/
│   └── main.py
│
├── corpus/
│   ├── processed/
│   │   ├── regulation_chunks.json
│   │   └── regulation_metadata.json
│   │
│   └── regulations/
│       └── vtu_2025_regulations.pdf
│
├── tests/
│   ├── test_api.py
│   └── test_petition_agents.py
│
├── screenshots/
│   ├── swagger-ui.png
│   ├── petition-analysis.png
│   └── test-results.png
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

The `screenshots/` directory is intended for demonstration images. Create it and add the images before expecting them to appear in this README.

---

## Prerequisites

Before running the project, install:

* Python 3.11 or a compatible Python version.
* Git.
* Docker Desktop with Docker Compose support, if using Docker.
* Internet access on the first run if the embedding model must be downloaded.

The application uses Sentence Transformers and FAISS, so initial model loading and embedding-index creation may take some time.

---

## Installation and Setup

### Option 1: Run Locally with Python

#### Step 1: Clone the repository

```powers
```
