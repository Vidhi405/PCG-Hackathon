# core.py

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

# Base directory = folder where core.py is
BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = Path(
    r"C:\\Users\\vidhi\\OneDrive\\Desktop\\Important stuff\\Projects\\pcghack\\enterprise_final_itsm_dataset.csv"
)

# Where to save trained models / indices
MODELS_DIR = BASE_DIR / "models_artifacts"
MODELS_DIR.mkdir(exist_ok=True, parents=True)

RANDOM_STATE = 42

# Column names from the CSV header[file:1]
TEXT_COL = "description"
ID_COL = "ticket id"

TARGET_PRIORITY = "priority_encoded"
TARGET_ROUTING = "assigned_group"
TARGET_SLA_BREACH = "sla_breach_flag"

NUM_FEATURES = [
    "impact_score",
    "urgency_score",
    "risk_score",
    "affected_users",
    "resolution_hours",
]

def load_data() -> pd.DataFrame:
    """Load the ITSM tickets dataset."""
    df = pd.read_csv(DATA_PATH)
    # We ignore 'status' and assume tickets are resolved.[file:1]
    return df

def split_targets(df: pd.DataFrame):
    """
    Split into train/test for:
    - priority (encoded)
    - routing (assigned_group)
    - SLA breach flag
    """
    X = df[[TEXT_COL] + NUM_FEATURES]
    y_pr = df[TARGET_PRIORITY]
    y_rt = df[TARGET_ROUTING]
    y_sla = df[TARGET_SLA_BREACH]

    return train_test_split(
        X,
        y_pr,
        y_rt,
        y_sla,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y_pr,
    )

def build_preprocessor():
    """Shared TF‑IDF + numeric scaler transformer."""
    text_tf = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 1),
        min_df=5,
    )
    num_tf = Pipeline([
        ("scaler", StandardScaler())
    ])

    pre = ColumnTransformer(
        transformers=[
            ("text", text_tf, TEXT_COL),
            ("num", num_tf, NUM_FEATURES),
        ]
    )
    return pre
