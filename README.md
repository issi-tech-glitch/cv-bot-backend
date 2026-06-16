# cv-bot-backend

Backend for the CV chatbot on my freelancer website. Visitors can chat with an AI assistant called Pia that knows my background, skills, and work history — essentially a conversational version of my CV.

I work as a Data and Automation Freelancer, and a lot of potential clients land on my site without knowing exactly what I do or whether I'm the right fit for their project. Instead of just having a static CV page, this gives them a way to ask specific questions and get answers right away.

## How it works

The backend is a small FastAPI app. On startup it reads my CV from a PDF file and loads the text into the system prompt alongside instructions for how Pia should behave. Every chat request streams the response back token by token so the frontend feels snappy.

The assistant runs on Gemini 2.5 Flash via Google's OpenAI-compatible API. It has two tools available:

- **record_user_details** — if someone wants to get in touch, Pia asks for their email and stores it
- **record_unknown_question** — if a question can't be answered from the CV, it gets logged so I can fill the gap

Pia responds in whatever language the user writes in (defaults to German if ambiguous).

## Stack

- Python 3.12
- FastAPI + Uvicorn
- Google Gemini 2.5 Flash (via OpenAI-compatible endpoint)
- pypdf for CV text extraction
- uv for dependency management

## Setup

```bash
cp .env.example .env   # add your GOOGLE_API_KEY
uv sync
uv run uvicorn api.main:app --reload
```

Put your CV as `cv/cv.pdf` or set `CV_PATH` in `.env` to point somewhere else.

The chat endpoint is `POST /api/chat` and expects `{ "messages": [...] }` in OpenAI message format.
