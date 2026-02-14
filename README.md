# AI-Driven Intelligent Ticketing – Enterprise ITSM


Modern enterprises handle large volumes of IT incidents and service requests across platforms like ServiceNow, Jira, Zendesk, and Freshservice. This project builds an AI-powered intelligent ticketing system that automates ticket classification, prioritization, routing, duplicate detection, 
and trend analysis. By leveraging machine learning and historical data, the system reduces manual triage, improves SLA compliance, identifies recurring issues, and continuously learns from human feedback to enhance IT operations efficiency.

---

## Table of contents
[Overview](#overview)
[Tech Stack](#techstack)



## Overview
This project was developed for the Pi-Hack-Za Hackathon 24-Hour Build Challenge. The solution is an AI‑driven ITSM assistant where a web frontend (HTML, CSS, JavaScript/TypeScript) lets users upload ticket CSVs and view routing, SLA risk, and duplicate insights. The backend is built with
FastAPI, which connects the UI to a machine‑learning pipeline using SentenceTransformer embeddings and RandomForest models to analyze tickets and return enriched results plus high‑level trends.


## Tech Stack

Frontend: HTML, CSS, JavaScript, TypeScript

Backend: Python, FastAPI, Pydantic

Machine Learning / NLP: scikit‑learn (RandomForest, DBSCAN, LabelEncoder), sentence‑transformers (all‑MiniLM‑L6‑v2), NumPy, pandas

Model Persistence: joblib

Dev / Infra: Uvicorn (ASGI server), CORS middleware for frontend–backend integration
