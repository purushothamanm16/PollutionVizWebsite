from fastapi import APIRouter, Query
from ai.ai_logic import ask_groq
from ai.utils import calculate_overall_aqi

router = APIRouter()

@router.get("/help")
async def help_info():
    return {
        "help": """Clarity is an AI assistant that explains pollution data and health risks to citizens, policymakers, and students. It suggests actions, predicts policy impacts, creates quizzes, and simulates urban planning scenarios to promote pollution awareness and healthier communities."""
    }

@router.get("/explain")
async def explain_pollution(pollutant: str):
    prompt = (
        f"Explain the pollutant '{pollutant}'. "
        "Respond strictly in this JSON format:\n\n"
        "{\n"
        '  "object": "What is {pollutant}?",\n'
        '  "causes": ["Cause 1", "Cause 2", "Cause 3"],\n'
        '  "effects": ["Effect 1", "Effect 2", "Effect 3"]\n'
        "}\n"
        "Do not include any extra text or explanation outside the JSON."
    ).replace("{pollutant}", pollutant)
    return ask_groq(prompt)

import json
from fastapi import HTTPException

@router.get("/predict_policy")
async def predict_policy(policy: str, location: str, pm25: float, pm10: float, no2: float, co: float, o3: float):
    old_aqi = calculate_overall_aqi(pm25, pm10, no2, co, o3)

    prompt = f"""
You are Clarity, an AI model that predicts the outcome of pollution-control policies.

Inputs:
- Policy: {policy}
- Location: {location}
- Current AQI: {old_aqi}
- Pollutant measures: PM2.5={pm25}, PM10={pm10}, NO2={no2}, CO={co}, O3={o3}

Return ONLY a valid JSON object with EXACT keys and data types as shown below.

All string values must be enclosed in double quotes.
For rupee values (estimated_cost_rupees, healthcare_savings_rupees), include units like "100Cr".
For health_benefits, return exactly "high" or "low" as a string.
For total_population, return a **number only**, not a string.

Do NOT include any comments or extra text.

Example JSON format:

{{
  "effects_of_policy": ["Effect 1", "Effect 2", "Effect 3"],
  "efficiency_ratio": 0.0,
  "old_aqi": {old_aqi},
  "new_aqi": 0.0,
  "aqi_improvement_percent": 0.0,
  "old_pollutants": {{
    "pm25": {pm25},
    "pm10": {pm10},
    "no2": {no2},
    "co": {co},
    "o3": {o3}
  }},
  "new_pollutants": {{
    "pm25": 0.0,
    "pm10": 0.0,
    "no2": 0.0,
    "co": 0.0,
    "o3": 0.0
  }},
  "health_benefits": "high",
  "estimated_cost_rupees": "0",
  "timeline_months": 0,
  "short_term_steps": ["Step 1", "Step 2", "Step 3"],
  "medium_term_steps": ["Step 1", "Step 2", "Step 3"],
  "long_term_steps": ["Step 1", "Step 2", "Step 3"],
  "total_population": 0,
  "total_benefited": 0,
  "urban_percent": 0.0,
  "rural_percent": 0.0,
  "respiratory_cases_reduction_percent": 0.0,
  "healthcare_savings_rupees": "0",
  "quality_of_life_increase_percent": 0.0,
  "life_expectancy": "+0 years"
}}

Do not include any other explanation or text.
"""

    return ask_groq(prompt)


@router.get("/compare_locations")
async def compare_locations(location1: str, location2: str, pm25_1: float, pm10_1: float, pm25_2: float, pm10_2: float):
    prompt = f"""
You are Clarity.
Compare pollution health impact between:
- {location1}: PM2.5={pm25_1}, PM10={pm10_1}
- {location2}: PM2.5={pm25_2}, PM10={pm10_2}
Give 2-line difference summary.
Return as {{"comparison": "..."}}
"""
    return ask_groq(prompt)

@router.get("/health_risks")
async def health_risks(pm25: float, pm10: float, no2: float, co: float, o3: float):
    aqi = calculate_overall_aqi(pm25, pm10, no2, co, o3)
    prompt = f"""
You are Clarity.
AQI: {aqi}
Pollutants: PM2.5={pm25}, PM10={pm10}, NO2={no2}, CO={co}, O3={o3}
Give health risk summary per group in this JSON:
{{
  "children": "...",
  "adults": "...",
  "elderly": "..."
}}
"""
    return ask_groq(prompt)

debug_policy_suggestions = False

@router.get("/suggest_policies")
async def suggest_policies(location: str, aqi: int, pm25: float, pm10: float, no2: float, co: float, o3: float):
    prompt = f"""
You are Clarity, a narrow AI assistant for pollution policy.
Suggest 3 effective policies based on the following context:
Location: {location}
AQI: {aqi}
Pollutant levels:
- PM2.5: {pm25}
- PM10: {pm10}
- NO2: {no2}
- CO: {co}
- O3: {o3}

Respond only with a JSON array:
["Policy 1", "Policy 2", "Policy 3"]
"""
    return ask_groq(prompt) if not debug_policy_suggestions else ["Plant trees", "Ban diesel", "Promote cycling"]

@router.get("/citizen_actions")
async def citizen_actions(pm25: float, pm10: float, no2: float, co: float, o3: float):
    prompt = f"""
You are Clarity, an AI assistant for pollution awareness.

Given current pollutant levels (units: CO and NO2 in ppb; O3, PM10, PM2.5 in µg/m³):
- PM2.5: {pm25}
- PM10: {pm10}
- NO2: {no2}
- CO: {co}
- O3: {o3}

Suggest 5 simple, practical actions citizens can take right now to reduce their exposure and protect their health.

Return a JSON array of action strings only.
"""
    return ask_groq(prompt)

@router.get("/daily_tip")
async def daily_tip():
    prompt = """
You are Clarity, an AI assistant that gives short, actionable tips or facts about pollution.

Give one daily pollution-related tip or fact that is:
- Easy to understand
- Practical or educational
- No more than 2 sentences

Respond as plain text.
"""
    result = ask_groq(prompt)
    return {"tip": result if isinstance(result, str) else str(result)}

@router.get("/myth_buster")
async def myth_buster(claim: str):
    prompt = f"""
You are Clarity, an AI myth-buster for pollution.

Analyze the following claim and respond whether it's True or False, followed by a short explanation.

Claim: "{claim}"

Respond in JSON format:
{{
  "verdict": "True" or "False",
  "explanation": "..."
}}
"""
    return ask_groq(prompt)

@router.get("/reduce_pollution_plan")
async def reduce_pollution_plan(goal: str, location: str):
    prompt = f"""
You are Clarity, an AI assistant helping design pollution-reduction strategies.

Goal: {goal}
Location: {location}

Give a 3-point actionable plan that can help achieve this goal. Be realistic and location-aware.

Respond in JSON format:
{{
  "goal": "{goal}",
  "location": "{location}",
  "plan": ["Step 1", "Step 2", "Step 3"]
}}
"""
    return ask_groq(prompt)