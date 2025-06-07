"""Daily Bitcoin forecast using OpenAI GPT and live price data."""

from __future__ import annotations

import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import openai


COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"


def fetch_price_history(days: int = 30) -> pd.DataFrame:
    """Fetch historical prices and volume from CoinGecko."""
    params = {"vs_currency": "usd", "days": days}
    resp = requests.get(COINGECKO_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
    df = prices.merge(volumes, on="timestamp")
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("date", inplace=True)
    df.drop(columns="timestamp", inplace=True)
    return df


def extract_features(df: pd.DataFrame) -> dict[str, float]:
    """Compute trend and volatility features from price data."""
    df = df.copy()
    df["return"] = df["price"].pct_change()
    df["trend"] = df["return"].rolling(3).mean()
    df["volatility"] = df["return"].rolling(7).std() * np.sqrt(7)

    latest = df.iloc[-1]
    return {
        "price": float(latest["price"]),
        "volume": float(latest["volume"]),
        "trend": float(latest["trend"]),
        "volatility": float(latest["volatility"]),
    }


def forecast_with_gpt(features: dict[str, float]) -> str:
    """Query OpenAI GPT-4 with the computed features."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = openai.OpenAI(api_key=api_key)

    prompt = (
        "Du bist ein Krypto-Analyst. Basierend auf folgenden Daten zu Bitcoin:\n"
        f"Aktueller Preis: {features['price']:.2f} USD\n"
        f"24h-Volumen: {features['volume']:.2f}\n"
        f"Kurzfristiger Trend (3-Tage): {features['trend']:.4f}\n"
        f"7-Tage-Volatilität: {features['volatility']:.4f}\n\n"
        "Gib eine kurze Prognose zum BTC-Kurs f\xFCr die n\xE4chsten 1, 2 und 3 Tage."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def run_forecast() -> None:
    data = fetch_price_history()
    features = extract_features(data)
    result = forecast_with_gpt(features)
    print("=== Bitcoin Forecast (1-3 Tage) ===")
    print(result)


if __name__ == "__main__":
    run_forecast()

