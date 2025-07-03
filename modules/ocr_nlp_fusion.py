import json
import os
import openai

# Assuming client is initialized globally or passed
# Make sure your OPENAI_API_KEY is set in your .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

def analyze_sentiment(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using gpt-4o as per your original code
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a highly analytical AI trained to perform sentiment analysis on financial news articles. Extract the sentiment (positive, negative, neutral) and a score (0-1), along with a concise reason."},
                {"role": "user", "content": f"Analyze the sentiment of the following news text:\n\n{text}\n\nProvide the output as a JSON object with 'label', 'score', and 'reason' fields."}
            ]
        )
        sentiment_data = json.loads(response.choices[0].message.content)
        sentiment_data['score'] = float(sentiment_data.get('score', 0.0))
        sentiment_data['reason'] = str(sentiment_data.get('reason', 'No reason provided.'))
        return sentiment_data
    except Exception as e:
        return {"error": f"Sentiment analysis failed: {e}"}

def fuse_sentiment_and_visual(visual_analysis_result, news_text, timestamp):
    """
    Fuses visual chart analysis and news sentiment to provide a comprehensive trade suggestion.
    """
    if not visual_analysis_result or "error" in visual_analysis_result:
        return {"error": "Invalid visual analysis result provided."}
    
    if news_text is None:
        news_text = "No news text provided."

    visual_details = visual_analysis_result.get('details', 'No detailed visual analysis provided.')
    visual_signal_type = visual_analysis_result.get('signal_type', 'N/A')
    visual_confidence = visual_analysis_result.get('confidence', 0.0)
    visual_strategy = visual_analysis_result.get('strategy', 'N/A')
    visual_risk_reward = visual_analysis_result.get('risk_reward', 'N/A')

    sentiment_data = analyze_sentiment(news_text) 

    if "error" in sentiment_data:
        return {"error": f"Sentiment analysis for fusion failed: {sentiment_data['error']}"}

    sentiment_label = sentiment_data.get('label', 'N/A')
    sentiment_score = sentiment_data.get('score', 0.0)
    sentiment_reason = sentiment_data.get('reason', 'No reason provided for sentiment.')

    # Construct the comprehensive prompt for the LLM
    prompt_messages = [
        {"role": "system", "content": """
            You are an expert financial analyst. Your role is to integrate candlestick chart analysis with news sentiment to provide actionable and well-reasoned trade suggestions.
            Your output MUST be a JSON object. Ensure all fields are present.
            Provide specific numerical guidance (e.g., price levels), using standard currency format (e.g., $100,000.00). Ensure proper spacing between numbers and words.
            Keep explanations concise and focused on the rationale. Do NOT fuse words or numbers together.
        """},
        {"role": "user", "content": f"""
            Analyze the following financial data and provide a trade suggestion:

            ---
            **Visual Chart Analysis:**
            - Signal Type: {visual_signal_type}
            - Confidence: {visual_confidence:.2f}
            - Suggested Strategy: {visual_strategy}
            - Risk/Reward: {visual_risk_reward}
            - Detailed Visual Observations: {visual_details}

            ---
            **News Sentiment Analysis:**
            - News Text: "{news_text}"
            - Sentiment Label: {sentiment_label}
            - Sentiment Score: {sentiment_score:.2f}
            - Sentiment Reason: {sentiment_reason}

            ---
            **Current Context:**
            - Timestamp: {timestamp}

            ---
            **Your Task:**
            Generate a detailed trade suggestion based on the fusion of the visual chart analysis and the news sentiment.
            The output should be a JSON object with the following keys and values:

            {{
                "trade_suggestion": "string (e.g., 'Buy', 'Sell', 'Hold', 'Monitor')",
                "overall_confidence": "float (0.0 to 1.0, reflecting your overall confidence in the suggestion)",
                "strategy": "string (e.g., 'Short-term bullish', 'Long-term bearish', 'Consolidation play')",
                "risk_reward": "string (e.g., 'High Risk / High Reward', 'Moderate Risk / Moderate Reward', 'Low Risk / Defined Reward')",
                "entry_point": "string (e.g., 'Around $X.XX' or 'Between $X.XX and $Y.YY', with brief reasoning)",
                "profit_targets": ["string (e.g., '$A.AA')", "string (e.g., '$B.BB')"],
                "support_levels": ["string (e.g., '$C.CC')"],
                "resistance_levels": ["string (e.g., '$D.DD')"],
                "stop_loss": "string (e.g., '$E.EE', with brief reasoning)",
                "rationale_summary": "string (A brief paragraph summarizing the overall rationale for the trade suggestion, considering both technicals and sentiment. Focus on the main contributing factors and market outlook. This should be concise and no more than 3-4 sentences.)"
            }}
            Ensure all numerical values are provided with proper spacing and currency symbols.
            """}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=prompt_messages,
            temperature=0.3 # Even lower temperature for more structured, less free-form text
        )
        fusion_output = json.loads(response.choices[0].message.content)

        # Basic validation and default values for new fields
        fusion_output['trade_suggestion'] = fusion_output.get('trade_suggestion', 'N/A')
        fusion_output['overall_confidence'] = float(fusion_output.get('overall_confidence', 0.0))
        fusion_output['strategy'] = fusion_output.get('strategy', 'N/A')
        fusion_output['risk_reward'] = fusion_output.get('risk_reward', 'N/A')
        
        # Ensure these fields exist and are strings/lists of strings
        fusion_output['entry_point'] = fusion_output.get('entry_point', 'N/A').strip()
        fusion_output['profit_targets'] = [str(x).strip() for x in fusion_output.get('profit_targets', [])]
        fusion_output['support_levels'] = [str(x).strip() for x in fusion_output.get('support_levels', [])]
        fusion_output['resistance_levels'] = [str(x).strip() for x in fusion_output.get('resistance_levels', [])]
        fusion_output['stop_loss'] = fusion_output.get('stop_loss', 'N/A').strip()
        fusion_output['rationale_summary'] = fusion_output.get('rationale_summary', 'No detailed rationale provided.').strip()
        
        # The 'details' field from previous versions is no longer directly generated by AI for table.
        # It's now constructed in app.py
        # You can keep this line or remove it if app.py fully transitions to the new fields.
        fusion_output['details'] = "" 

        return fusion_output
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response as JSON: {e}. Raw response: {response.choices[0].message.content}"}
    except Exception as e:
        return {"error": f"Fusion process failed: {e}"}