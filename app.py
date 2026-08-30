import os
from flask import Flask, render_template, request, session, redirect
import security_rules
import storage
from dotenv import load_dotenv

load_dotenv()
from gemini_api import generate_security_advice

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- BUSINESS PROFILE ---------------- #

@app.route("/business", methods=["GET", "POST"])
def business():

    if request.method == "POST":

        session.clear()
        session["business_id"] = storage.new_business_id()

        session["business_profile"] = {
            "business_name": request.form["business_name"],
            "business_type": request.form["business_type"],
            "employee_count": request.form["employee_count"],
            "device_count": request.form["device_count"],
            "cloud_services": request.form.getlist("cloud_services"),
            "important_data": request.form.getlist("important_data"),
            "state": request.form.get("state", ""),
            "district": request.form.get("district", ""),
        }

        print("\n===== BUSINESS PROFILE =====")
        for key, value in session["business_profile"].items():
            print(f"{key}: {value}")

        return redirect("/assessment")

    return render_template("business_profile.html")


# ---------------- GUIDED ASSESSMENT ---------------- #

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "business_profile" not in session:
        return redirect("/business")

    if request.method == "POST":

        answers = {}
        for category, questions in security_rules.QUESTIONS.items():
            for q in questions:
                answers[q["id"]] = request.form.get(q["id"])

        session["answers"] = answers

        print("\n===== ASSESSMENT ANSWERS =====")
        for qid, ans in answers.items():
            print(f"{qid}: {ans}")

        return redirect("/report")

    return render_template(
        "assessment.html",
        categories=security_rules.QUESTIONS,
        category_labels=security_rules.CATEGORY_LABELS,
    )


# ---------------- REPORT (rule-based score + Gemini interpretation) ---------------- #

@app.route("/report")
def report():

    if "answers" not in session:
        return redirect("/assessment")

    business_profile = session.get("business_profile")
    answers = session.get("answers")

    # --- STEP 1: Rule-based scoring ---
    # This is the source of truth for the numerical score.
    scoring_result = security_rules.calculate_all_scores(answers)

    priority_findings = security_rules.build_priority_findings(
        scoring_result["category_scores"]
    )

    roadmap_buckets = security_rules.build_roadmap(
        scoring_result["category_scores"]
    )

    print("\n==============================")
    print("RULE-BASED SCORING RESULT")
    print("==============================")
    print(scoring_result)

    # --- STEP 2: Save the assessment immediately ---
    # Gemini is intentionally NOT called here.
    business_id = session.get("business_id")

    if business_id:
        storage.save_assessment(
            business_id,
            business_profile,
            scoring_result,
            None,
        )

    # --- STEP 3: Show the report immediately ---
    return render_template(
        "report.html",
        profile=business_profile,
        scoring=scoring_result,
        priority_findings=priority_findings,
        roadmap_buckets=roadmap_buckets,
        category_labels=security_rules.CATEGORY_LABELS,
        ai=None,
        ai_error=None,
        business_id=business_id,
    )


# ---------------- AI ADVICE API ---------------- #

@app.route("/api/ai-advice")
def ai_advice():

    if "answers" not in session:
        return {"error": "Assessment not found."}, 400

    business_profile = session.get("business_profile")
    answers = session.get("answers")

    # Calculate the same rule-based results.
    # Gemini only interprets these results.
    scoring_result = security_rules.calculate_all_scores(answers)

    priority_findings = security_rules.build_priority_findings(
        scoring_result["category_scores"]
    )

    roadmap_buckets = security_rules.build_roadmap(
        scoring_result["category_scores"]
    )

    assessment_context = {
        "category_scores": scoring_result["category_scores"],
        "overall_score": scoring_result["overall_score"],
        "overall_risk_level": scoring_result["overall_risk_level"],
        "priority_findings": [
            {"category": key, **data}
            for key, data in priority_findings
        ],
        "roadmap_buckets": {
            bucket: [
                {"category": key, **data}
                for key, data in items
            ]
            for bucket, items in roadmap_buckets.items()
        },
    }

    try:
        # Gemini runs here, AFTER the report page has already loaded.
        ai_advice = generate_security_advice(
            business_profile,
            assessment_context,
        )

        return {
            "success": True,
            "ai": ai_advice,
        }

    except Exception as e:
        print("\nGEMINI ERROR:", str(e))

        return {
            "success": False,
            "error": "AI advice is temporarily unavailable.",
        }, 200


# ---------------- REASSESSMENT ---------------- #

@app.route("/reassess")
def reassess():
    # Keep the business profile and business_id (so history stays linked),
    # but clear previous answers so they retake the assessment fresh.
    session.pop("answers", None)
    return redirect("/assessment")


@app.route("/history")
def history():
    business_id = session.get("business_id")
    if not business_id:
        return redirect("/business")

    full_history = storage.get_history(business_id)
    progress = storage.compare_progress(business_id)

    return render_template(
        "history.html",
        history=full_history,
        progress=progress,
        category_labels=security_rules.CATEGORY_LABELS,
        profile=session.get("business_profile"),
    )


if __name__ == "__main__":
    app.run(debug=True)
