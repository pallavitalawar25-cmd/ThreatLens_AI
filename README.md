# 🛡 ThreatLens

### Cybersecurity Readiness for Small Businesses

**Challenge:** Omni_CyberTech_2 — Affordable Cybersecurity Assessment for Small Businesses

---
# 🛡️ ThreatLens — Cybersecurity Readiness for Small Businesses

> An AI-assisted cybersecurity readiness assessment platform that helps small businesses understand their security gaps and prioritize practical improvements.

ThreatLens is designed for small businesses that may not have a dedicated cybersecurity team or the budget for expensive security assessments.

It combines **deterministic rule-based cybersecurity scoring** with **Google Gemini AI** to transform assessment responses into a clear cybersecurity readiness report, prioritized recommendations, and a 30/60/90-day improvement roadmap.

---

## 🎯 Problem

Small businesses increasingly depend on:

- Online services
- Cloud platforms
- Customer information
- Employee devices
- Digital payments
- E-commerce platforms

However, many small businesses do not have:

- Dedicated cybersecurity teams
- Specialized security expertise
- Large security budgets
- Continuous security monitoring
- A clear understanding of their biggest security weaknesses

This creates a practical problem:

> **Businesses know cybersecurity matters, but they often don't know where to start.**

---

## 💡 Solution

ThreatLens provides a guided cybersecurity readiness assessment specifically designed for small businesses.

The user enters basic business information and answers 20 security questions across 10 cybersecurity categories.

ThreatLens then:

1. Evaluates the responses using deterministic security rules.
2. Calculates category-level readiness scores.
3. Calculates an overall readiness score.
4. Classifies the overall risk level.
5. Identifies priority findings.
6. Uses Gemini AI to explain the results in plain language.
7. Provides practical recommended actions.
8. Generates a structured 30/60/90-day improvement roadmap.
9. Stores assessment snapshots for progress tracking.

---

## What it is

ThreatLens is an AI-assisted cybersecurity readiness assessment and
decision-support platform for small businesses. It helps a business owner
understand their security posture across 10 core areas, see what matters
most, and get a concrete 30/60/90-day plan — without needing an IT
background.

**What it is not:** penetration testing, vulnerability scanning, malware
detection, real-time threat monitoring, or a SOC/SIEM. It does not claim
any of these capabilities anywhere in the app or report.

## How scoring works (the important part)

Your readiness score is **never** calculated by AI. It's calculated by
fixed, deterministic rules in `security_rules.py`:

```
Assessment Answers (20 questions, 10 categories)
        ↓
Points per answer (A=0 ... D=3, fixed mapping)
        ↓
Category Score (0-100 per category)
        ↓
Weighted Overall Readiness Score (0-100)
        ↓
Risk Level (LOW ≥75, MEDIUM 50-74, HIGH <50)
```

Gemini receives these already-computed numbers and is explicitly
instructed not to change or invent any of them — its job is only to
explain the results in plain language, prioritize what to fix first, and
write the specific action items for the roadmap phases the app already
assigned.

## Architecture

```
Business Profile
        ↓
Guided Cybersecurity Assessment (20 questions)
        ↓
Rule-Based Risk Scoring          ← security_rules.py, deterministic
        ↓
Gemini AI Security Advisor       ← gemini_api.py, interprets only
        ↓
Risk Prioritization + 30/60/90-Day Roadmap
        ↓
Cybersecurity Readiness Report
        ↓
Reassessment & Progress Tracking ← storage.py, local JSON snapshot store
```

## Honest technical notes

- **No real database.** The original CareerCompass project never actually
  used MongoDB/Firebase despite mentioning them — it was 100% session-based
  with no persistence. To make reassessment/progress tracking real rather
  than faked, this project adds a local JSON file (`storage.py`) keyed by
  a per-business ID. This is a prototype-grade store, not production
  infrastructure — it won't survive a redeploy on most hosts and isn't
  safe for concurrent multi-tenant traffic. Swapping in MongoDB or
  Firebase later only requires rewriting the functions in `storage.py`;
  no call sites elsewhere need to change.
- **PDF export** is `window.print()`, same as the original project —
  `reportlab` was listed in the original `requirements.txt` but never
  actually used, so it's been dropped here rather than left as dead weight.
- **Gemini model name** (`gemini-3.5-flash`) was carried over from the
  original project's `gemini_api.py`. Verify it's valid for your API key
  before relying on it in a live demo.

## Tech stack

- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Backend:** Python, Flask
- **AI:** Google Gemini API
- **Storage:** local JSON file (prototype-grade — see note above)
- **Deployment:** Render (gunicorn)

## Project Structure

```
ThreatLens/
│
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── business_profile.html
│   ├── assessment.html
│   ├── report.html
│   └── history.html
│
├── data/                  ← assessments.json created at runtime
├── app.py                 ← routes
├── security_rules.py      ← deterministic scoring engine (the core logic)
├── gemini_api.py           ← Gemini integration (interpretation only)
├── storage.py              ← lightweight persistence for reassessment
├── requirements.txt
├── Procfile
├── .env.example
└── README.md
```

## Setup

```bash
git clone <your-repo-url>
cd ThreatLens
pip install -r requirements.txt
cp .env.example .env   # then fill in GEMINI_API_KEY
python app.py
```

Open `http://127.0.0.1:5000`.

## Implementation order this was built in

1. `security_rules.py` — data model + deterministic scoring
2. `gemini_api.py` — AI interpretation layer
3. `storage.py` — reassessment persistence
4. `app.py` — routes wiring it together
5. Templates + orange/white styling
6. End-to-end smoke tests (scoring engine, full request flow, Gemini-failure
   fallback, all-worst-case-answers edge case) — all passing


### 🏢 Business Profiling

ThreatLens collects basic business information including:

- Business name
- Business type
- Employee count
- Device count
- Cloud services used
- Sensitive information handled
- State
- District

---

### 📋 Guided Cybersecurity Assessment

The assessment evaluates 10 cybersecurity readiness categories:

1. Authentication
2. Access Control
3. Password Practices
4. Multi-Factor Authentication
5. Backup & Recovery
6. Device Security
7. Data Protection
8. Employee Security Awareness
9. Cloud Security
10. Incident Preparedness

The current assessment contains **20 questions**.

---

### 📊 Rule-Based Risk Scoring

ThreatLens uses deterministic application logic to calculate:

- Category scores
- Overall readiness score
- Risk levels
- Priority findings
- Roadmap categories

The numerical score is calculated by the application's rule engine rather than by the AI model.

This keeps the scoring process consistent and reproducible.

---

### 🤖 AI-Powered Security Guidance

Google Gemini acts as an advisory layer.

The AI does **not** calculate or modify the numerical security score.

Instead, it interprets the already-calculated assessment results and generates:

- Overall security summary
- Plain-language explanations
- Priority finding explanations
- Recommended security actions
- 30-day guidance
- 60-day guidance
- 90-day guidance

---

### 🛣️ 30/60/90-Day Security Roadmap

ThreatLens converts identified weaknesses into a phased improvement plan.

#### First 30 Days

Focus on immediate and high-priority security improvements.

#### Next 60 Days

Strengthen security practices and address remaining important gaps.

#### Next 90 Days

Establish longer-term security improvements and improve overall readiness.

The roadmap helps small businesses improve progressively instead of attempting to implement every security improvement at once.

---

### 📈 Progress Tracking

ThreatLens supports reassessment and progress tracking.

Users can:

- Reassess their business
- Store assessment snapshots
- View assessment history
- Compare progress over time
- Track changes in readiness scores

---

### 📄 Readiness Report

After completing the assessment, ThreatLens generates a cybersecurity readiness report containing:

- Overall readiness score
- Risk classification
- Business profile
- Category scores
- Priority findings
- Recommended actions
- 30/60/90-day roadmap
- AI-generated security guidance

The report can also be printed or saved as a PDF through the browser.

---

# 🧠 System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │   Small Business    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Business Profile   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Guided Assessment   │
                    │    20 Questions     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Rule-Based Scoring  │
                    │                     │
                    │ Category Scores     │
                    │ Overall Score       │
                    │ Risk Levels         │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Priority Findings│        │ 30/60/90 Roadmap │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Google Gemini    │
                    │  AI Interpretation   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Cybersecurity       │
                    │ Readiness Report    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Assessment History  │
                    │ & Progress Tracking │
                    └─────────────────────┘
```

---

# 🔐 Rule-First AI Architecture

ThreatLens follows a **rule-first, AI-second** approach.

The AI model is not responsible for determining the numerical risk score.

```text
Assessment Answers
        ↓
Deterministic Security Rules
        ↓
Verified Category Scores
        ↓
Overall Readiness Score
        ↓
Priority Findings + Roadmap
        ↓
Gemini AI Interpretation
        ↓
Plain-Language Security Guidance
```

This separation ensures that AI-generated content does not arbitrarily change the numerical assessment results.

---

# 🛡️ Security Boundaries

ThreatLens is a **cybersecurity readiness assessment and advisory platform**.

It does NOT perform:

- Penetration testing
- Vulnerability scanning
- Malware detection
- CVE detection
- Real-time threat monitoring
- SOC/SIEM operations
- Automated incident response

ThreatLens evaluates user-provided information and provides readiness guidance based on the assessment results.

---

# 🛠️ Technology Stack

## Backend

- Python
- Flask
- Google Gemini API

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

## Application Logic

- Python rule-based scoring engine
- Flask sessions
- Assessment history storage

## Deployment

- GitHub
- Render
- Gunicorn

---

# 📁 Project Structure

```text
ThreatLens/
│
├── app.py
├── gemini_api.py
├── security_rules.py
├── storage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── business_profile.html
│   ├── assessment.html
│   ├── report.html
│   └── history.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ThreatLens
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

**Never commit the `.env` file to GitHub.**

## 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🌐 Deployment

ThreatLens can be deployed as a Python web service using Render.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
gunicorn app:app
```

## Required Environment Variables

```text
GEMINI_API_KEY
SECRET_KEY
```

Environment variables should be configured through the hosting platform rather than committed to the repository.

---

# 🔄 Application Flow

```text
Business Profile
       ↓
20 Security Questions
       ↓
Rule-Based Evaluation
       ↓
Category Scores
       ↓
Overall Readiness Score
       ↓
Risk Classification
       ↓
Priority Findings
       ↓
AI Explanations
       ↓
Recommended Actions
       ↓
30/60/90-Day Roadmap
       ↓
Assessment History
```

---

# 📊 Example Output

A completed assessment produces a report containing:

```text
Overall Readiness Score
        ↓
Risk Level
        ↓
Category Score Breakdown
        ↓
Priority Findings
        ↓
Recommended Actions
        ↓
30-Day Plan
        ↓
60-Day Plan
        ↓
90-Day Plan
```

The actual score depends on the answers provided by the business.

---

# 🎯 Intended Users

ThreatLens is primarily designed for:

- Small businesses
- Local retailers
- Small e-commerce businesses
- Service businesses
- Startups
- Organizations without dedicated cybersecurity teams

---

# 🚧 Current Limitations

ThreatLens is a cybersecurity readiness assessment tool and is not a replacement for a professional cybersecurity assessment.

The current system:

- Relies on user-provided information
- Uses predefined assessment questions
- Uses deterministic scoring rules
- Provides advisory recommendations
- Does not actively inspect infrastructure
- Does not perform penetration testing
- Does not perform vulnerability scanning
- Does not provide continuous threat monitoring

---

# 🔮 Future Enhancements

Potential future improvements include:

- Industry-specific assessment profiles
- Compliance-oriented guidance
- Security policy templates
- Security awareness training modules
- Evidence/document upload
- Multi-user business accounts
- Persistent cloud database
- Advanced progress analytics
- Integration with optional security assessment tools
- More detailed cybersecurity maturity tracking

---

# 🏆 Project Vision

ThreatLens aims to make cybersecurity readiness:

**Understandable → Actionable → Affordable**

Instead of overwhelming small businesses with technical security terminology, ThreatLens converts assessment responses into a practical improvement plan that businesses can understand and follow.

---

# 👩‍💻 Project

**ThreatLens — Cybersecurity Readiness for Small Businesses**

Built as a cybersecurity-focused project demonstrating:

- Cybersecurity readiness assessment
- Rule-based risk scoring
- Generative AI
- Flask web development
- Frontend development
- Security-focused product design
- Progress tracking

---

# ⚠️ Disclaimer

ThreatLens provides cybersecurity readiness guidance based on user-provided assessment information.

It should not be considered a complete security audit, penetration test, vulnerability assessment, or professional cybersecurity certification.