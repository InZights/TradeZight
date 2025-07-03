# modules/visual_analyzer.py
import os
import io
import base64
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ingest_and_analyze_visual(image_bytes, analysis_tool="OpenAI GPT-4o", image_mime_type="image/jpeg"):
    """
    Analyzes a visual input (chart image) to identify market signals using OpenAI GPT-4o.
    Adds optional overlay indicator descriptions and strategy suggestions.

    Args:
        image_bytes (bytes): The raw bytes of the image file.
        analysis_tool (str): The chosen analysis tool (default to GPT-4o).
        image_mime_type (str): The MIME type of the image (e.g., 'image/png', 'image/jpeg').

    Returns:
        dict: A dictionary containing the identified signal type, confidence, strategy, and details.
    """
    try:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:{image_mime_type};base64,{base64_image}"

        prompt = """
You are a financial trading assistant analyzing a candlestick chart.

Instructions:
1. Identify any known chart patterns (e.g., Bullish Engulfing, Doji, Head & Shoulders).
2. Analyze common indicators if visible (e.g., MACD crossover, RSI levels, Bollinger Bands).
3. Estimate a confidence score from 0.0 to 1.0.
4. Suggest a trading strategy based on the pattern.
5. Recommend risk/reward ratio and whether to wait for confirmation.

Output format:
Signal Type: <pattern>
Confidence: <score>
Strategy: <what a trader could do>
Risk/Reward: <R/R estimate or comment>
Details: <clear explanation of the pattern, trend, and volume context>
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a trading assistant that analyzes financial charts and recommends strategies."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ]
        )

        model_response = response.choices[0].message.content.strip()

        signal_type = "Unidentified"
        confidence = 0.0
        strategy = "None"
        risk_reward = "Not specified"
        details_text = model_response

        lines = model_response.split("\n")
        for line in lines:
            if line.lower().startswith("signal type:"):
                signal_type = line.split(":", 1)[1].strip()
            elif line.lower().startswith("confidence:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    confidence = 0.0
            elif line.lower().startswith("strategy:"):
                strategy = line.split(":", 1)[1].strip()
            elif line.lower().startswith("risk/reward:"):
                risk_reward = line.split(":", 1)[1].strip()
            elif line.lower().startswith("details:"):
                details_text = line.split(":", 1)[1].strip()
                remaining = lines[lines.index(line)+1:]
                if remaining:
                    details_text += "\n" + "\n".join(remaining).strip()
                break

        return {
            "signal_type": signal_type,
            "confidence": confidence,
            "strategy": strategy,
            "risk_reward": risk_reward,
            "details": details_text
        }

    except Exception as e:
        return {"error": f"Error using GPT-4o visual analysis: {str(e)}"}
