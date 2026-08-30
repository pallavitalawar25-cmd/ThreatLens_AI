# storage.py
#
# IMPORTANT: CareerCompass AI did not actually use MongoDB or Firebase
# despite them being mentioned as target stack — the whole app was
# session-only, with zero persistence. To support reassessment/progress
# tracking honestly, this file adds the SIMPLEST thing that actually
# works: a local JSON file, keyed by a business_id stored in the
# session cookie.
#
# This is NOT a production database. It won't survive a redeploy on
# most hosts (including Render's ephemeral filesystem), and it isn't
# safe for concurrent multi-user traffic. It's enough to make
# reassessment real (not faked) for a hackathon prototype.
#
# To make this production-real: swap the functions below for MongoDB
# (pymongo) or Firebase (firebase-admin) calls — the call sites in
# app.py won't need to change.

import json
import os
import uuid
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "assessments.json")


def _load_all():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def new_business_id():
    return uuid.uuid4().hex[:12]


def save_assessment(business_id, business_profile, scoring_result, ai_advice):
    """
    Appends one assessment snapshot to this business's history.
    Returns the full updated history list for this business.
    """
    data = _load_all()
    history = data.get(business_id, [])

    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "business_profile": business_profile,
        "overall_score": scoring_result["overall_score"],
        "overall_risk_level": scoring_result["overall_risk_level"],
        "category_scores": scoring_result["category_scores"],
        "ai_advice": ai_advice,
    }

    history.append(snapshot)
    data[business_id] = history
    _save_all(data)

    return history


def get_history(business_id):
    data = _load_all()
    return data.get(business_id, [])


def get_latest(business_id):
    history = get_history(business_id)
    return history[-1] if history else None


def compare_progress(business_id):
    """
    Returns a simple diff between the two most recent assessments, or
    None if there's only one (or zero) on record.
    """
    history = get_history(business_id)
    if len(history) < 2:
        return None

    previous, latest = history[-2], history[-1]

    category_deltas = {}
    for category, latest_data in latest["category_scores"].items():
        prev_score = previous["category_scores"].get(category, {}).get("score", 0)
        category_deltas[category] = {
            "label": latest_data["label"],
            "previous_score": prev_score,
            "current_score": latest_data["score"],
            "delta": latest_data["score"] - prev_score,
        }

    return {
        "previous_overall": previous["overall_score"],
        "current_overall": latest["overall_score"],
        "overall_delta": latest["overall_score"] - previous["overall_score"],
        "category_deltas": category_deltas,
        "previous_date": previous["timestamp"],
        "current_date": latest["timestamp"],
    }
