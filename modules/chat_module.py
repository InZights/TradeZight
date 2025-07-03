# modules/chat_module.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_chatbot(user_input, context_data):
    # Safely retrieve data from context_data.
    # If a key is missing OR its value is None, default to an empty dictionary.
    # This prevents 'NoneType' object has no attribute 'get' errors.
    visual = context_data.get("visual_analysis")
    if visual is None:
        visual = {} # Ensure it's an empty dict if the session state value was None

    sentiment = context_data.get("sentiment_analysis")
    if sentiment is None:
        sentiment = {} # Ensure it's an empty dict if the session state value was None
        
    fusion_result = context_data.get("fusion_result")
    if fusion_result is None:
        fusion_result = {} # Also handle fusion_result if it can be None

    news_input = context_data.get("news_input", "") # Default to empty string if not present

    # Safely get values from visual analysis, defaulting to 'N/A' or 0.0 if not present
    signal_type = visual.get("signal_type", "N/A")
    confidence = visual.get("confidence", 0.0)
    strategy = visual.get("strategy", "N/A")
    risk_reward = visual.get("risk_reward", "N/A")
    details = visual.get("details", "N/A")

    # Safely get values from sentiment analysis, defaulting to 'N/A' or 0.0 if not present
    sentiment_label = sentiment.get("label", "N/A")
    sentiment_score = sentiment.get("score", 0.0)
    sentiment_reason = sentiment.get("reason", "N/A")

    # Safely get values from fusion result
    fusion_suggestion = fusion_result.get("trade_suggestion", "N/A")
    fusion_overall_confidence = fusion_result.get("overall_confidence", 0.0)
    fusion_strategy = fusion_result.get("strategy", "N/A")
    fusion_risk_reward = fusion_result.get("risk_reward", "N/A")
    fusion_details = fusion_result.get("details", "N/A")


    # Construct context summary
    context_summary = f"""
Current Analysis Context:

Visual Signal: {signal_type}
Visual Confidence: {confidence:.2f}
Visual Strategy: {strategy}
Visual Risk/Reward: {risk_reward}
Visual Details: {details}

Sentiment: {sentiment_label}
Sentiment Score: {sentiment_score:.2f}
Sentiment Reason: {sentiment_reason}

---
Overall Multi-Modal Fusion Result:
Trade Suggestion: {fusion_suggestion}
Overall Confidence: {fusion_overall_confidence:.2f}
Suggested Strategy (Fusion): {fusion_strategy}
Risk/Reward (Fusion): {fusion_risk_reward}
Fusion Details: {fusion_details}
---

User News Input: {news_input[:500]}
"""
    # Ensure no explicit "None" strings appear in the prompt for cleaner AI interaction
    context_summary = context_summary.replace("None", "N/A").strip()


    prompt = f"""
You are TradeZight, a highly intelligent and helpful AI trading assistant. Your primary goal is to provide precise, actionable, and informed responses based on the provided financial analysis context (visual chart analysis, news sentiment analysis, and the multi-modal fusion result).

**Guidelines for your responses:**
1.  **Prioritize Fusion Result:** If a "Overall Multi-Modal Fusion Result" is available in the context, use it as the primary basis for trade suggestions and insights.
2.  **Combine Insights:** When providing suggestions, briefly mention how the visual and sentiment analyses contributed to the fusion result.
3.  **Actionable Advice:** If the user asks for trade timing, confirmation, or strategy, give a precise suggestion (e.g., "Consider a long position," "Look for entry at X," "Avoid trading for now").
4.  **Stay in Domain:** Only answer questions directly related to trading (stocks, crypto, forex, commodities, etc.) and the provided financial data.
5.  **Professional Tone:** Maintain a professional, objective, and helpful tone.
6.  **Decline Irrelevant Questions:** If a question is unrelated to trading or the provided financial context, politely decline to answer by saying, "My purpose is to assist with financial trading analysis based on the provided data. Please ask a question related to trading."
7.  **No Financial Advice Disclaimer:** Always include a small disclaimer at the end of your trading-related answers: "(This is for informational purposes only and not financial advice. Always do your own research.)"

**Current Chart & News Context:**
{context_summary}

**User Question:**
{user_input}
"""

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are TradeZight, a financial trading advisor. Always adhere to the guidelines provided."},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Chatbot Error: {str(e)}\n\nPlease ensure your OpenAI API key is correctly set and you have an active internet connection."