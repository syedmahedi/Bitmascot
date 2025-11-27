import os
import asyncio
import json
import httpx

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


async def plan_with_rules(weather: dict, news: list) -> dict:
    recs = []
    desc = (weather.get("description") or "").lower()
    if "rain" in desc or "shower" in desc or "storm" in desc:
        recs.append("Carry an umbrella and prefer indoor activities.")
    elif "clear" in desc or "sun" in desc:
        recs.append("Great day for outdoor activities; consider a walk or exercise outside.")
    else:
        recs.append("Check details for weather-sensitive plans.")

    for item in news:
        t = (item.get("title") or "").lower()
        s = (item.get("summary") or "").lower()
        if "traffic" in t or "accident" in s or "road" in s:
            recs.append("Expect travel delays — leave earlier for appointments.")
            break

    return {"source": "rules", "recommendations": recs}


async def plan_with_openai(weather: dict, news: list) -> dict:
    """Call OpenAI ChatCompletion to generate recommendations.
    Falls back to rule-based if the OpenAI key is missing or the call fails.
    """
    key = os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return await plan_with_rules(weather, news)

    try:
        import openai

        openai.api_key = key
        system = "You are DayMate, an assistant that creates short, practical daily planning recommendations based on weather and local news. Provide 3 concise actionable suggestions."
        user = f"Weather: {json.dumps(weather)}\nNews: {json.dumps(news[:5])}"
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=300,
            n=1,
        )
        text = resp.choices[0].message.content.strip()
        # naive split into lines
        recs = [line.strip('- ').strip() for line in text.splitlines() if line.strip()]
        return {"source": "openai", "recommendations": recs, "raw": text}
    except Exception:
        return await plan_with_rules(weather, news)


async def generate_plan(weather: dict, news: list) -> dict:
    # prefer OpenAI if key present
    if os.getenv(OPENAI_API_KEY_ENV):
        return await plan_with_openai(weather, news)
    return await plan_with_rules(weather, news)
