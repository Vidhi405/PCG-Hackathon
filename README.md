# AI-Driven Intelligent Ticketing – Enterprise ITSM


Modern enterprises handle large volumes of IT incidents and service requests across platforms like ServiceNow, Jira, Zendesk, and Freshservice. This project builds an AI-powered intelligent ticketing system that automates ticket classification, prioritization, routing, duplicate detection, 
and trend analysis. By leveraging machine learning and historical data, the system reduces manual triage, improves SLA compliance, identifies recurring issues, and continuously learns from human feedback to enhance IT operations efficiency.

---

## Table of contents
-[Overview](#overview)
-[Tech Stack](#techstack)
-[System Architecture](#systemarchitecture)
-[Use Case and Application](#usecaseandapplication)
-[How it Works?](#howitworks)
-[Contributors](#contributors)
-[How can you Contribute?](#howcanyoucontribute)


## Overview
This project was developed for the Pi-Hack-Za Hackathon 24-Hour Build Challenge. The solution is an AI‑driven ITSM assistant where a web frontend (HTML, CSS, JavaScript/TypeScript) lets users upload ticket CSVs and view routing, SLA risk, and duplicate insights. The backend is built with
FastAPI, which connects the UI to a machine‑learning pipeline using SentenceTransformer embeddings and RandomForest models to analyze tickets and return enriched results plus high‑level trends.


## Tech Stack

Frontend: HTML, CSS, JavaScript, TypeScript

Backend: Python, FastAPI, Pydantic

Machine Learning / NLP: scikit‑learn (RandomForest, DBSCAN, LabelEncoder), sentence‑transformers (all‑MiniLM‑L6‑v2), NumPy, pandas

Model Persistence: joblib

Dev / Infra: Uvicorn (ASGI server), CORS middleware for frontend–backend integration


## System Architecture

[ Browser UI ]
    HTML/CSS + JS/TS
          |
          |  HTTP (JSON)
          v
[ FastAPI Server ]
    Python + ML pipeline
          |
          v
[ Models & Data ]
  pandas / NumPy / NLP / RF


## Use Cases & Applications

-Enterprise IT Support Automation: Automatically classify, prioritize, and route IT tickets to reduce manual triage effort.
-SLA Risk Management: Predict potential SLA breaches and trigger early escalations to avoid penalties.
-Duplicate & Incident Reduction: Detect repeated issues and suggest knowledge base articles to prevent redundant tickets.
-Root-Cause & Trend Analysis: Identify recurring system failures, noisy alerts, and top issue drivers to enable proactive fixes.
-Operational Efficiency & Cost Reduction: Reduce resolution time (MTTR), improve team productivity, and optimize resource allocation.
-Continuous Learning Systems: Improve model accuracy over time using human feedback and corrections.


## How it Works?

-The user first feeds a csv file to the 
-JavaScript/TypeScript sends the file to the FastAPI /upload-dataset endpoint over HTTP as form-data/JSON.
-FastAPI reads the CSV into pandas, validates and cleans it, and builds features (priority encoding, impact score, embeddings, etc.) for each ticket.
-ML models (RandomForest for routing/SLA, DBSCAN for duplicates, SentenceTransformer for embeddings) run on these features and produce predictions and cluster IDs.
-FastAPI returns a JSON response with per-ticket outputs and aggregates, and the frontend uses this JSON to render tables, charts, and insights for the user.

## Contributors
-Jyotsna Mallena - ML Model
-Rashmeet Kaur - Frontend

## How to contribute?
We welcome contributions to improve the AI-Driven Intelligent Ticketing System!

### Contribution Guidelines
-Fork the repository
-Create a new branch (feature/your-feature-name)
-Commit your changes
-Push to your fork
-Open a Pull Request
