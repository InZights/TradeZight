# TradeZight: Multi-Modal Financial Analysis AI

## Fusing Visuals & Sentiment for Smarter Trade Decisions

![TradeZight App Screenshot - Placeholder](https://placehold.co/800x450/0E1117/FAFAFA?text=TradeZight+App+Screenshot)
*(Replace this placeholder with an actual screenshot or GIF of your running app!)*

## 🚀 Project Overview

TradeZight is an AI-powered Streamlit application designed to empower traders and investors with comprehensive, data-driven insights. In today's volatile financial markets, making informed decisions requires synthesizing vast amounts of information. TradeZight addresses this challenge by intelligently fusing two critical data streams: **candlestick chart analysis** and **financial news sentiment**.

The app provides actionable trade suggestions, complete with precise numerical guidance (entry points, profit targets, support/resistance, stop-losses), all presented in a clear, easy-to-digest tabular format. A dedicated AI chatbot is also integrated to answer specific trading-related questions based on the generated analysis.

## ✨ Features

* **Visual Chart Analysis:** Upload a candlestick chart (PNG, JPG, JPEG) and let AI analyze its patterns, trends, and key signals (e.g., Bullish Engulfing, MACD Crossover, RSI indicators).
* **News Sentiment Analysis:** Input relevant financial news text, and the AI will analyze its sentiment (Positive, Negative, Neutral) and provide a confidence score and reasoning.
* **Multi-Modal Fusion:** The core innovation! TradeZight intelligently combines insights from both visual chart analysis and news sentiment to generate a holistic trade suggestion.
* **Actionable Numerical Guidance:** The fusion summary provides concrete numbers for:
    * Suggested Entry Points/Ranges
    * Potential Profit Targets
    * Key Support Levels
    * Key Resistance Levels
    * Recommended Stop-Loss Levels
* **Concise Rationale:** Each trade suggestion is accompanied by a brief, clear explanation of the contributing factors from both technical and fundamental (sentiment) perspectives.
* **AI Trading Assistant Chatbot:** A dedicated sidebar chatbot allows users to ask follow-up questions about the analysis, trade strategies, or market conditions, receiving context-aware responses.
* **Persistent Results:** Analysis results are stored in session state, preventing redundant API calls and ensuring a smooth user experience even across app reruns.

## 🛠️ Installation and Setup

### Prerequisites

* Python 3.8+
* An OpenAI API Key (`sk-proj-...`)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/TradeZight.git](https://github.com/your-username/TradeZight.git)
    cd TradeZight
    ```
    *(Replace `https://github.com/your-username/TradeZight.git` with your actual repository URL)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    * **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up your OpenAI API Key:**
    Create a file named `.env` in the root directory of your project (where `app.py` is located) and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    **Important:** Replace `"your_openai_api_key_here"` with your actual key. Do not share this file publicly.

## ▶️ How to Run

After completing the setup:

1.  **Ensure your virtual environment is activated.**
2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    This will open the app in your default web browser.

## 💡 Usage

1.  **Upload a Candlestick Chart:** In the "1. Visual Chart Analysis" section, use the file uploader to upload a PNG, JPG, or JPEG image of a candlestick chart.
2.  **Analyze Chart:** Click the "Analyze Chart" button. The AI will process the image and display its technical signal breakdown.
3.  **Enter News Text:** In the "2. News & Sentiment Analysis" section, type or paste relevant financial news article text.
4.  **Analyze Sentiment:** Click the "Analyze Sentiment" button. The AI will analyze the text and provide its sentiment label, score, and reason.
5.  **Perform Fusion:** Once both visual and sentiment analyses are complete and free of errors, the "Perform Fusion" button in the "3. Multi-Modal Fusion & Trade Suggestion" section will become active. Click it to get the comprehensive trade suggestion.
6.  **Review Detailed Summary:** Expand the "Detailed Fusion Summary" to view the tabular breakdown of entry points, targets, support/resistance, stop-loss, and the overall rationale.
7.  **Chat with TradeZight:** Use the "Ask TradeZight" chatbot in the sidebar to ask follow-up questions about the analysis or general trading concepts.

## ⚠️ Disclaimer

This application is an AI-powered financial analysis tool. The trade suggestions and information provided are for informational purposes only and do not constitute financial advice. Always conduct your own thorough research, exercise due diligence, and consult with a professional financial advisor before making any investment decisions. The developers are not liable for any financial losses incurred from using this application.

## 🤝 Credits

Developed by Jefferson Macasarte

## 📄 License

This project is open-sourced under the MIT License. See the `LICENSE` file for more details.
*(You'll need to create a `LICENSE` file in your repository if you want to include this. A simple MIT license file can be found online.)*
