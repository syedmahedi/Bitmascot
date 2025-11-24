import os
import httpx

NEWSAPI_EVERYTHING = "https://newsapi.org/v2/everything"


async def fetch_news(query: dict, max_items: int = 5) -> list:
    """Fetch recent news using NewsAPI. Falls back to sample data when key missing."""
    key = os.getenv("NEWS_API_KEY")
    if not key:
        return [
            {"title": "Local event today", "summary": "Community meetup at 6 PM"},
            {"title": "Traffic alert", "summary": "Accident on Main St, expect delays"},
        ]

    q = query.get("city") or query.get("q") or "local"
    params = {"q": q, "apiKey": key, "pageSize": max_items, "sortBy": "publishedAt"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(NEWSAPI_EVERYTHING, params=params)
            resp.raise_for_status()
            data = resp.json()
            articles = []
            for a in data.get("articles", [])[:max_items]:
                articles.append({"title": a.get("title"), "summary": a.get("description")})
            return articles
        except Exception as e:
            return [{"title": "news_fetch_error", "summary": str(e)}]
