# security_rules.py
#
# THIS FILE IS THE SOURCE OF TRUTH FOR SCORING.
# Gemini never calculates a number here — it only receives the output
# of these functions and explains/prioritizes it in plain language.
#
# Structure mirrors opt_mapper.py's trait_map, but instead of mapping an
# answer to a list of trait labels, each answer maps to a POINT VALUE
# (0-3) that feeds directly into a deterministic score.

# ---------------------------------------------------------------------------
# CATEGORIES
# ---------------------------------------------------------------------------
# 10 categories, each weighted equally (10 points each = 100 total).
# Change CATEGORY_WEIGHTS if you want some categories to matter more
# (e.g. weight Backup & Recovery or MFA higher — both are common root
# causes of small-business breaches).

CATEGORY_WEIGHTS = {
    "authentication": 10,
    "access_control": 10,
    "password_practices": 10,
    "mfa": 10,
    "backup_recovery": 10,
    "device_security": 10,
    "data_protection": 10,
    "employee_awareness": 10,
    "cloud_security": 10,
    "incident_preparedness": 10,
}

CATEGORY_LABELS = {
    "authentication": "Authentication",
    "access_control": "Access Control",
    "password_practices": "Password Practices",
    "mfa": "Multi-Factor Authentication",
    "backup_recovery": "Backup & Recovery",
    "device_security": "Device Security",
    "data_protection": "Data Protection",
    "employee_awareness": "Employee Security Awareness",
    "cloud_security": "Cloud Security",
    "incident_preparedness": "Incident Preparedness",
}

# ---------------------------------------------------------------------------
# QUESTION BANK
# ---------------------------------------------------------------------------
# 2 plain-language questions per category = 20 total.
# Each option A-D is worth 0-3 points (3 = best practice, 0 = weakest).
# question ids are formatted "<category>_1" / "<category>_2".

QUESTIONS = {

    "authentication": [
        {
            "id": "authentication_1",
            "text": "How do employees log in to your business systems (email, files, software)?",
            "options": {
                "A": "Everyone shares one or two generic logins",
                "B": "Most people have their own login, but a few share accounts",
                "C": "Everyone has their own individual login",
                "D": "Everyone has their own login, and we review/remove unused accounts regularly",
            },
        },
        {
            "id": "authentication_2",
            "text": "When someone leaves the company, what happens to their account access?",
            "options": {
                "A": "We usually forget or deal with it 'eventually'",
                "B": "We remove access within a few weeks",
                "C": "We remove access within a few days",
                "D": "We remove access the same day, following a checklist",
            },
        },
    ],

    "access_control": [
        {
            "id": "access_control_1",
            "text": "Can every employee access every file and system, or only what their role needs?",
            "options": {
                "A": "Everyone can access everything",
                "B": "Mostly open, with a couple of restricted folders",
                "C": "Access is limited by role for most systems",
                "D": "Access is strictly limited by role and reviewed periodically",
            },
        },
        {
            "id": "access_control_2",
            "text": "Do you know exactly who currently has admin/owner-level access to your key accounts?",
            "options": {
                "A": "No idea — it's grown organically over time",
                "B": "We have a rough idea",
                "C": "Yes, we keep a list but don't review it often",
                "D": "Yes, and we review admin access regularly",
            },
        },
    ],

    "password_practices": [
        {
            "id": "password_practices_1",
            "text": "How do employees typically create and store passwords?",
            "options": {
                "A": "Simple passwords, often reused across accounts",
                "B": "Passwords vary but are written down or stored in unencrypted notes",
                "C": "Employees use their own unique passwords",
                "D": "Employees use unique passwords generated/stored in a password manager",
            },
        },
        {
            "id": "password_practices_2",
            "text": "Do you enforce any password requirements (length, complexity, expiration)?",
            "options": {
                "A": "No requirements at all",
                "B": "We ask people to use 'good' passwords but don't enforce it",
                "C": "Systems enforce minimum length/complexity",
                "D": "Systems enforce strong password rules company-wide",
            },
        },
    ],

    "mfa": [
        {
            "id": "mfa_1",
            "text": "Is multi-factor authentication (MFA / two-factor login) enabled on your important accounts (email, banking, cloud storage)?",
            "options": {
                "A": "Not enabled anywhere",
                "B": "Enabled on one or two accounts only",
                "C": "Enabled on most important accounts",
                "D": "Enabled on all important accounts, required for everyone",
            },
        },
        {
            "id": "mfa_2",
            "text": "If MFA is enabled, is it required or optional for employees?",
            "options": {
                "A": "We don't use MFA",
                "B": "Optional — up to each employee",
                "C": "Required for admins/owners only",
                "D": "Required for everyone on every important account",
            },
        },
    ],

    "backup_recovery": [
        {
            "id": "backup_recovery_1",
            "text": "How is your important business data backed up?",
            "options": {
                "A": "It isn't backed up",
                "B": "Backed up occasionally/manually by someone remembering to do it",
                "C": "Backed up automatically on a regular schedule",
                "D": "Backed up automatically, on a schedule, with a copy stored offsite/separately",
            },
        },
        {
            "id": "backup_recovery_2",
            "text": "Have you ever actually tested restoring data from a backup?",
            "options": {
                "A": "No, and we're not sure our backups would even work",
                "B": "No, but we assume they'd work",
                "C": "We've tested it once or twice",
                "D": "We test restores on a regular schedule",
            },
        },
    ],

    "device_security": [
        {
            "id": "device_security_1",
            "text": "Are company computers/phones protected with antivirus/security software and kept updated?",
            "options": {
                "A": "No security software, updates are ignored",
                "B": "Some devices have protection, updates are inconsistent",
                "C": "Most devices are protected and mostly kept updated",
                "D": "All devices are protected and updates are enforced automatically",
            },
        },
        {
            "id": "device_security_2",
            "text": "Are laptops/phones used for work protected if lost or stolen (screen lock, encryption, remote wipe)?",
            "options": {
                "A": "No protections in place",
                "B": "Just a basic screen lock, nothing else",
                "C": "Screen lock plus encryption on most devices",
                "D": "Screen lock, encryption, and remote wipe capability on all devices",
            },
        },
    ],

    "data_protection": [
        {
            "id": "data_protection_1",
            "text": "How is sensitive data (customer info, payment details, employee records) stored?",
            "options": {
                "A": "Mixed in with everything else, no special protection",
                "B": "Somewhat separated but not encrypted",
                "C": "Stored in access-controlled systems",
                "D": "Stored encrypted, in access-controlled systems, with limited exposure",
            },
        },
        {
            "id": "data_protection_2",
            "text": "When you share sensitive files (with clients, vendors, etc.), how is that usually done?",
            "options": {
                "A": "Plain email attachments, no protection",
                "B": "Email, sometimes password-protected",
                "C": "Shared through a secure file-sharing platform",
                "D": "Secure file-sharing platform with access expiration/tracking",
            },
        },
    ],

    "employee_awareness": [
        {
            "id": "employee_awareness_1",
            "text": "Have employees received any training on spotting phishing emails or scams?",
            "options": {
                "A": "No training at all",
                "B": "An informal chat once, nothing structured",
                "C": "A one-time formal training session",
                "D": "Regular/recurring security awareness training",
            },
        },
        {
            "id": "employee_awareness_2",
            "text": "If an employee suspects a phishing email or scam, do they know what to do?",
            "options": {
                "A": "No, there's no guidance",
                "B": "They'd probably ask a coworker informally",
                "C": "There's a general expectation to report it to someone",
                "D": "There's a clear, known process for reporting it",
            },
        },
    ],

    "cloud_security": [
        {
            "id": "cloud_security_1",
            "text": "What cloud services does your business rely on (email, storage, accounting, CRM, etc.), and are they configured with security in mind?",
            "options": {
                "A": "We use cloud tools but haven't reviewed their security settings",
                "B": "Default settings, never really reviewed",
                "C": "We've reviewed and adjusted settings on our main tools",
                "D": "Settings are reviewed regularly and locked down (sharing limits, login alerts, etc.)",
            },
        },
        {
            "id": "cloud_security_2",
            "text": "Do you know exactly what data is stored in each cloud service you use?",
            "options": {
                "A": "No clear picture",
                "B": "A rough idea for the main ones",
                "C": "Yes, for most services",
                "D": "Yes, we keep an inventory of what's stored where",
            },
        },
    ],

    "incident_preparedness": [
        {
            "id": "incident_preparedness_1",
            "text": "If your business had a security incident today (ransomware, data breach, account takeover), would you know what to do first?",
            "options": {
                "A": "No idea — we'd be figuring it out from scratch",
                "B": "We'd probably call our IT person/vendor and hope for the best",
                "C": "We have a rough plan in our heads",
                "D": "We have a written incident response plan the team knows about",
            },
        },
        {
            "id": "incident_preparedness_2",
            "text": "Do you know who to contact (legal, customers, authorities) if customer data were exposed?",
            "options": {
                "A": "No idea",
                "B": "We'd figure it out at the time",
                "C": "We have a general sense of who to contact",
                "D": "We have contacts/obligations documented in advance",
            },
        },
    ],
}

# Flatten point values: every option A-D maps to a fixed point value
# regardless of category, so the meaning of "picking C" is consistent
# across the whole assessment.
OPTION_POINTS = {"A": 0, "B": 1, "C": 2, "D": 3}
MAX_POINTS_PER_QUESTION = 3

# ---------------------------------------------------------------------------
# RISK THRESHOLDS (0-100 scale, explainable and defined in one place)
# ---------------------------------------------------------------------------
RISK_THRESHOLDS = {
    "LOW": 75,      # score >= 75  -> LOW risk / strong readiness
    "MEDIUM": 50,   # 50 <= score < 75 -> MEDIUM risk
    # anything below 50 -> HIGH risk
}


def get_risk_level(score):
    """Deterministic mapping from a 0-100 score to a risk label."""
    if score >= RISK_THRESHOLDS["LOW"]:
        return "LOW"
    if score >= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "HIGH"


def calculate_category_score(category, answers):
    """
    answers: dict of question_id -> 'A'/'B'/'C'/'D'
    Returns a 0-100 score for a single category, based on its 2 questions.
    """
    questions = QUESTIONS[category]
    total_possible = len(questions) * MAX_POINTS_PER_QUESTION
    total_earned = 0

    for q in questions:
        answer = answers.get(q["id"])
        total_earned += OPTION_POINTS.get(answer, 0)

    if total_possible == 0:
        return 0

    return round((total_earned / total_possible) * 100)


def calculate_all_scores(answers):
    """
    answers: dict of question_id -> 'A'/'B'/'C'/'D' (all 20 questions)

    Returns:
    {
        "category_scores": {category: {"score": int, "label": str, "risk_level": str}, ...},
        "overall_score": int,
        "overall_risk_level": str,
    }
    """
    category_scores = {}
    weighted_sum = 0
    total_weight = sum(CATEGORY_WEIGHTS.values())

    for category in QUESTIONS:
        score = calculate_category_score(category, answers)
        category_scores[category] = {
            "score": score,
            "label": CATEGORY_LABELS[category],
            "risk_level": get_risk_level(score),
        }
        weighted_sum += score * CATEGORY_WEIGHTS[category]

    overall_score = round(weighted_sum / total_weight) if total_weight else 0

    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "overall_risk_level": get_risk_level(overall_score),
    }


def build_priority_findings(category_scores, top_n=5):
    """
    Returns the weakest categories, sorted ascending by score, capped at top_n.
    This is what "Priority Findings" on the report/dashboard is built from —
    always derived from real scores, never invented.
    """
    ranked = sorted(
        category_scores.items(),
        key=lambda item: item[1]["score"]
    )
    return ranked[:top_n]


def build_roadmap(category_scores):
    """
    Rule-based 30/60/90-day bucketing driven purely by category scores:
      - Weakest categories (lowest scores) -> 30 days
      - Middle -> 60 days
      - Strongest (but not yet at LOW risk) -> 90 days
    Categories already at LOW risk are left out of the roadmap entirely,
    since they don't need near-term action.

    Returns {"30_days": [...], "60_days": [...], "90_days": [...]}
    each item is (category_key, category_data).
    """
    ranked = sorted(category_scores.items(), key=lambda item: item[1]["score"])
    needs_action = [item for item in ranked if item[1]["risk_level"] != "LOW"]

    roadmap = {"30_days": [], "60_days": [], "90_days": []}
    n = len(needs_action)

    if n == 0:
        return roadmap

    # Split into thirds, weakest categories first.
    third = max(1, round(n / 3))
    roadmap["30_days"] = needs_action[:third]
    roadmap["60_days"] = needs_action[third:third * 2]
    roadmap["90_days"] = needs_action[third * 2:]

    return roadmap
