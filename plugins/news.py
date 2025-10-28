"""
News Plugin for Nova
"""
import requests

def run(context):
    api_key = context.get("news_api_key")
    if not api_key:
        return "News API key not set. Add 'news_api_key' to plugins_config.yaml."
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            headlines = [a['title'] for a in data['articles'][:3]]
            return "News: " + "; ".join(headlines)
        else:
            return f"News API error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"News fetch error: {e}"
