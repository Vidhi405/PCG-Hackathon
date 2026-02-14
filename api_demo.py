# api_demo.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from core import TEXT_COL
from ticket_understanding import summarize, extract_entities, detect_missing_info, find_duplicates
from autonomous_prioritization import load_autonomous_prioritization
from smart_routing import load_smart_routing, explain_routing
from pattern_detection import recurring_incidents, noisy_alert_sources, top_drivers
from proactive_insights import forecast_trend, recommend_actions, suggest_kb_article
from feedback_loop import log_feedback

app = FastAPI(title="ITSM AI Demo")

priority_model, risk_model, sla_model = load_autonomous_prioritization()
routing_model = load_smart_routing()

class TicketIn(BaseModel):
    ticket_id: str = "NEW"
    description: str
    affected_users: int = 1
    impact_score: float = 0.0
    urgency_score: float = 0.0
    risk_score: float = 0.0
    resolution_hours: float = 0.0

class FeedbackIn(BaseModel):
    ticket_id: str
    model_output: dict
    human_correction: dict

@app.post("/predict")
def predict(ticket: TicketIn):
    x = {
        TEXT_COL: [ticket.description],
        "affected_users": [ticket.affected_users],
        "impact_score": [ticket.impact_score],
        "urgency_score": [ticket.urgency_score],
        "risk_score": [ticket.risk_score],
        "resolution_hours": [ticket.resolution_hours],
    }

    summary = summarize(ticket.description)
    entities = extract_entities(ticket.description)
    missing = detect_missing_info(ticket.description)
    duplicates = find_duplicates(ticket.description)

    pr = priority_model.predict(x)[0]
    pr_conf = float(max(priority_model.predict_proba(x)[0]))

    group = routing_model.predict(x)[0]
    group_conf = float(max(routing_model.predict_proba(x)[0]))
    routing_reason = explain_routing(ticket.description, group)

    risk = float(risk_model.predict(x)[0])
    sla_prob = float(sla_model.predict_proba(x)[0][1])

    kb = suggest_kb_article(ticket.description)

    audit = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary,
        "priority": {"value": int(pr), "confidence": pr_conf},
        "routing": {"group": group, "confidence": group_conf, "reason": routing_reason},
        "risk_score": risk,
        "sla_breach_probability": sla_prob,
        "duplicates": duplicates,
        "entities": entities,
        "missing_info_flags": missing,
        "suggested_kb": kb,
    }

    return {
        "ticket_id": ticket.ticket_id,
        "summary": summary,
        "priority": int(pr),
        "routing_group": group,
        "sla_breach_prob": sla_prob,
        "risk_score": risk,
        "duplicates": duplicates,
        "entities": entities,
        "missing_info_flags": missing,
        "suggested_kb": kb,
        "audit_trail": audit,
    }

@app.get("/insights")
def insights():
    return {
        "recurring_incidents": recurring_incidents(),
        "noisy_alert_sources": noisy_alert_sources(),
        "top_drivers": top_drivers(),
        "trend_forecast": forecast_trend(),
        "recommended_actions": recommend_actions(),
    }

@app.post("/feedback")
def feedback(fb: FeedbackIn):
    log_feedback(fb.ticket_id, fb.model_output, fb.human_correction)
    return {"status": "recorded"}
