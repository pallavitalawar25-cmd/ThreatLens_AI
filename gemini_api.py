# gemini_api.py
#
# Same client setup pattern as CareerCompass's gemini_api.py.
# The critical difference: Gemini is given the ALREADY-CALCULATED scores
# and is explicitly instructed not to invent or re-score anything.

import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"timeout": 30000}
)

# NOTE: preserved from the original project's model string. Verify this
# is a valid/available model name for your API key before relying on it —
# swap for a confirmed model (e.g. "gemini-2.0-flash") if this errors out.
MODEL_NAME = "gemini-3.6-flash"


SECURITY_ADVISOR_PROMPT = """
You are ThreatLens AI, a cybersecurity readiness advisor for small businesses.

You are given a business's profile and the results of a cybersecurity
readiness assessment. The numerical scores below have ALREADY been
calculated by rule-based application logic. You must NOT invent, change,
recalculate, or contradict any score or risk level given to you.

Your job is ONLY to:
1. Explain what the results mean in plain, non-technical language.
2. Prioritize which weaknesses matter most, using the priority findings
   provided (do not invent new weaknesses that weren't assessed).
3. Give specific, practical recommendations for each weak category.
4. Write short, plain-language content for the 30/60/90-day roadmap
   buckets that were already assigned by the application (do not move
   categories between buckets).
5. Write an overall plain-language summary.

IMPORTANT RULES:
- Do NOT state or imply any overall score or category score other than
  the ones provided to you.
- Do NOT claim capabilities this product does not have: no penetration
  testing, no vulnerability scanning, no malware/CVE detection, no
  real-time threat monitoring, no SOC/SIEM. This is a readiness
  assessment and advisory tool only.
- Do NOT fabricate statistics, breach examples, or certifications.
- Base every recommendation on the categories and scores actually given.

Return ONLY valid JSON. Do NOT use markdown. Do NOT use ```json.
Do NOT write any explanation before or after the JSON.
The response MUST start with { and end with }

Use EXACTLY this JSON structure:

{
  "category_explanations": {
    "<category_key>": "plain-language explanation of this category's result and why it matters"
  },
  "priority_findings": [
    {
      "category": "<category_key>",
      "why_it_matters": "plain-language explanation of the risk",
      "recommended_actions": ["action 1", "action 2", "action 3"]
    }
  ],
  "roadmap": {
    "30_days": {
      "summary": "one sentence framing this phase",
      "action_items": ["action 1", "action 2"]
    },
    "60_days": {
      "summary": "one sentence framing this phase",
      "action_items": ["action 1", "action 2"]
    },
    "90_days": {
      "summary": "one sentence framing this phase",
      "action_items": ["action 1", "action 2"]
    }
  },
  "overall_summary": "2-4 sentence plain-language summary of the business's security readiness and what to focus on first"
}
"""


def generate_security_advice(business_profile, assessment_results):
    """
    business_profile: dict from the business profile form
    assessment_results: dict returned by security_rules.calculate_all_scores(),
                         plus priority_findings and roadmap already computed

    Returns parsed JSON (dict) from Gemini, or raises on failure — the
    caller is responsible for deciding what to show the user if Gemini
    is unavailable (the rule-based score/report can still stand on its own).
    """
    prompt = f"""
{SECURITY_ADVISOR_PROMPT}

Business Profile:
{business_profile}

Assessment Results (already calculated, do not change any numbers):
{assessment_results}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    text = response.text
    text = text.replace("```json", "").replace("```", "").strip()

    import json
    return json.loads(text)
