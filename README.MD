# AAI Server - AI Interview Platform Backend

Welcome to the backend of the **AAI (AI Interview Platform)**. This is a smart interview support platform that uses Artificial Intelligence to simulate and evaluate technical and soft skill interview sessions.

## Overview

The server is built on **FastAPI**, focusing on high performance and scalability. The system provides APIs to manage users, question banks, and most importantly, coordinates real-time AI interview sessions.

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** Prisma (Python Client)
- **Real-time Video/Audio:** Daily.co integration
- **AI Integration:** Processing transcripts and post-interview evaluation analysis

## Key Features

- **Interview Management:** Coordinates interview sessions by categories (Technical, Soft Skills).
- **Question Bank:** Stores and manages a diverse collection of interview questions.
- **Real-time Transcripts:** Records conversation content between the AI (Bot) and the candidate (User).
- **Evaluation Reports:** Automatically scores and provides detailed feedback after each interview session.
- **Artifacts Management:** Stores code snippets or technical data generated during the interview.

---

## Database Schema

![Database Schema](./diagrams/agent_interview.drawio.svg)

<details>
<summary><b>View Technical ER Diagram (Mermaid)</b></summary>

```mermaid
erDiagram
    User ||--o{ InterviewSession : "sessions"
    InterviewCategory ||--o{ QuestionBank : "questions"
    InterviewCategory ||--o{ InterviewSession : "sessions"
    InterviewSession ||--o{ Transcript : "transcripts"
    InterviewSession ||--o{ TechnicalArtifact : "artifacts"
    InterviewSession ||--o{ QuestionResponse : "responses"
    InterviewSession ||--o1 EvaluationReport : "report"
    QuestionBank ||--o{ QuestionResponse : "responses"

    User {
        String id PK
        String fullName
        String email
        String avatarUrl
        UserRole role
        DateTime createdAt
        DateTime updatedAt
    }

    InterviewCategory {
        String id PK
        String name
        String slug
        String systemPrompt
        String language
        DateTime createdAt
    }

    QuestionBank {
        String id PK
        String categoryId FK
        String questionText
        String expectedAnswer
        String difficulty
    }

    InterviewSession {
        String id PK
        String userId FK
        String categoryId FK
        String dailyRoomUrl
        SessionStatus status
        DateTime startTime
        DateTime endTime
        DateTime createdAt
    }

    Transcript {
        String id PK
        String sessionId FK
        String role
        String content
        Int latencyMs
        DateTime createdAt
    }

    TechnicalArtifact {
        String id PK
        String sessionId FK
        String language
        String codeContent
        String aiAnalysis
        DateTime createdAt
    }

    QuestionResponse {
        String id PK
        String sessionId FK
        String questionId FK
        String answer
        Float score
        String comment
    }

    EvaluationReport {
        String id PK
        String sessionId FK
        Float overallScore
        Float technicalScore
        Float softSkillScore
        String aiFeedback
        String recommendation
        DateTime createdAt
    }
```

</details>

## Installation & Running the Server

1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` file (Database URL).
3. Run the Server: `python -m app.main`
