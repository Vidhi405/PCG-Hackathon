# train_all.py
from autonomous_prioritization import train_autonomous_prioritization
from smart_routing import train_smart_routing
from ticket_understanding import build_duplicate_index
from core import load_data

if __name__ == "__main__":
    df = load_data()
    train_autonomous_prioritization()
    train_smart_routing()
    build_duplicate_index()
    print("All models and indices trained.")
