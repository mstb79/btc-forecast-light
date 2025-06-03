import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_forecast(data):
    prompt = f"""
Du bist ein quantitativer Krypto-Analyst. Basierend auf folgenden Daten:
- Aktueller BTC-Preis: {data['price']} USD
- Handelsvolumen: {data['volume']}
- Twitter-Stimmung: {data['twitter_sentiment']}
- Nachrichtenlage: {data['news_sentiment']}
- Miner-Abflüsse: {data['miner_outflows']}
- Makrolage: {data['macro']}

Gib mir eine Einschätzung:
1. Wahrscheinlichkeit, dass BTC morgen steigt (>1 %)
2. Wahrscheinlichkeit, dass BTC morgen fällt (>1 %)
3. Trendrichtung (↗️ / → / ↘️)
4. Kurze Begründung in 1–2 Sätzen
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
