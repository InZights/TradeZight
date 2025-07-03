# app.py
import streamlit as st
from dotenv import load_dotenv
import os
import datetime
import pytz # For timezone handling

# Assume these modules exist and are correctly implemented
from modules.visual_analyzer import ingest_and_analyze_visual
from modules.ocr_nlp_fusion import analyze_sentiment, fuse_sentiment_and_visual
from modules.chat_module import run_chatbot

# --- Constants and Configuration ---
APP_TITLE = "Multi-Modal Financial Analysis"
APP_ICON = "📈"
DEFAULT_LAYOUT = "wide"
DEFAULT_SIDEBAR_STATE = "expanded"
ANALYSIS_TOOL_NAME = "OpenAI GPT-4o"
PH_TIMEZONE = "Asia/Manila" # Philippines timezone

# --- Set Streamlit Page Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=DEFAULT_LAYOUT,
    initial_sidebar_state=DEFAULT_SIDEBAR_STATE
)

# --- Custom CSS for Streamlit Styling ---
# Consolidated and slightly refined CSS
st.markdown(f"""
    <style>
        /* General layout adjustments for main content */
        .main .block-container {{
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1rem; /* Adjust top padding for main content */
        }}

        /* Sidebar styling to match the goal image */
        [data-testid="stSidebar"] {{
            background-color: #0E1117; /* Dark background color from the image */
            color: #FAFAFA; /* Light text color */
            padding-top: 20px; /* Add some padding at the top */
            min-width: 350px; /* Adjust width as needed */
            width: 350px;
        }}

        /* Streamlit button default override (optional, for main content) */
        .stButton > button {{
            background-color: #4CAF50; /* Example button color */
            color: white;
            border-radius: 5px;
        }}

        /* Chat input box styling in the sidebar */
        [data-testid="stSidebar"] .stTextInput > div > div > input {{
            background-color: #262730; /* Darker background for input */
            color: #FAFAFA; /* Light text color for input */
            border: 1px solid #444; /* Subtle border */
            border-radius: 20px; /* Rounded corners for the input */
            padding: 10px 15px;
            padding-right: 40px; /* Space for the send icon */
        }}
        
        /* Remove the default label for the text_input in chat_input */
        [data-testid="stSidebar"] .stTextInput label {{
            display: none;
        }}

        /* Custom chat message bubbles for st.chat_message */
        .st-chat-message-container.st-chat-message-user {{
            background-color: transparent !important;
            justify-content: flex-end; /* Align user messages to the right */
            margin: 8px 0;
        }}
        .st-chat-message-container.st-chat-message-ai {{
            background-color: transparent !important;
            justify-content: flex-start; /* Align AI messages to the left */
            margin: 8px 0;
        }}

        /* Specific bubble styling - Adjusted for a more "boxed" look */
        .st-chat-message-container .st-chat-message-contents {{
            padding: 10px 15px;
            border-radius: 12px; /* Adjusted: Slightly less rounded for a boxier look */
            max-width: 80%; /* Limit bubble width */
            word-wrap: break-word;
            font-size: 0.95em;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); 
        }}
        
        .st-chat-message-container.st-chat-message-user .st-chat-message-contents {{
            background-color: #3C80F2; /* A shade of blue for user messages */
            color: white;
        }}

        .st-chat-message-container.st-chat-message-ai .st-chat-message-contents {{
            background-color: #444; /* Darker grey for bot messages */
            color: #FAFAFA;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }}

        /* For the "ChatGPT-like clone" header */
        .sidebar-header {{
            font-size: 2em;
            font-weight: bold;
            color: #FAFAFA;
            margin-bottom: 20px;
            padding-left: 1rem; /* Align with other content */
        }}

        /* For the Disclaimer expander and Detailed Fusion Summary expander */
        .stExpander {{
            border: none !important; /* Remove expander border */
            background-color: #262730; /* Darker background for the expander */
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .stExpander > div > div > p {{
            color: #FAFAFA; /* Text color for disclaimer */
        }}
        .stExpander > div > div > [data-testid="stExpanderChevron"] {{
            color: #FAFAFA; /* Chevron color */
        }}
        
        /* This targets the actual content area within any expander */
        .stExpander [data-testid="stExpanderContent"] {{
            padding: 15px; /* Add internal padding for better spacing around text */
            padding-top: 5px; /* Adjust top padding specifically for content */
        }}
        
        /* Style for paragraph text inside expander content */
        .stExpander [data-testid="stExpanderContent"] p {{
            font-size: 0.9em; /* Slightly smaller font size than default for body text */
            line-height: 1.6; /* Increase line height for better readability */
            margin-bottom: 0.8em; /* Space between paragraphs */
            word-wrap: break-word; /* Essential: Ensures long words/fused text breaks */
            overflow-wrap: break-word; /* Alternative for word-wrap */
            white-space: pre-wrap; /* Preserves whitespace and allows lines to wrap */
            color: #E0E0E0; /* Slightly lighter text for readability on dark background */
        }}

        /* If the AI uses markdown lists or strong/bold text, style them too */
        .stExpander [data-testid="stExpanderContent"] ul {{
            list-style-position: inside;
            padding-left: 1em;
            margin-bottom: 0.8em;
        }}
        .stExpander [data-testid="stExpanderContent"] li {{
            font-size: 0.9em;
            line-height: 1.6;
            color: #E0E0E0;
        }}
        .stExpander [data-testid="stExpanderContent"] strong {{
            color: #FFFFFF; /* Make bold text stand out more */
        }}

        /* NEW CSS for Markdown Tables inside expander */
        .stExpander [data-testid="stExpanderContent"] table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1em;
            margin-bottom: 1em;
        }}
        .stExpander [data-testid="stExpanderContent"] th,
        .stExpander [data-testid="stExpanderContent"] td {{
            border: 1px solid #333; /* Darker border for table cells */
            padding: 8px;
            text-align: left;
            color: #E0E0E0; /* Text color for table content */
        }}
        .stExpander [data-testid="stExpanderContent"] th {{
            background-color: #1A1A1A; /* Slightly darker background for headers */
            color: #FAFAFA;
            font-weight: bold;
        }}
    </style>
""", unsafe_allow_html=True)

# --- App Initialization ---
load_dotenv()

# Initialize session state variables using .setdefault() for conciseness
st.session_state.setdefault('visual_analysis_result', None)
st.session_state.setdefault('sentiment_analysis_result', None)
st.session_state.setdefault('fusion_result', None) # This will now store structured data
st.session_state.setdefault('uploaded_image_display', None)
st.session_state.setdefault('news_text_input', "") # For persisting the news input
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault('last_analyzed_image_id', None) # To track the last analyzed image

# Function to get current time in PH timezone
def get_ph_current_time():
    ph_tz = pytz.timezone(PH_TIMEZONE)
    now_ph = datetime.datetime.now(ph_tz)
    return now_ph.strftime("%Y-%m-%d %H:%M:%S %Z%z")

# Update timestamp in session state
st.session_state.current_time_ph = get_ph_current_time()

# --- Main Application Content ---
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("Upload a candlestick chart and provide relevant news to generate a trade suggestion.")

col1, col2 = st.columns(2)

# Column 1: Visual Chart Analysis
with col1:
    st.header("1. Visual Chart Analysis")
    uploaded_image = st.file_uploader("Upload a Candlestick Chart (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], key="chart_uploader")

    if uploaded_image:
        # Display the uploaded image immediately for visual feedback
        st.session_state.uploaded_image_display = uploaded_image.getvalue()
        st.image(st.session_state.uploaded_image_display, caption="Uploaded Chart", use_column_width=True)

        # Add the Analyze Chart button, disabled if no image is uploaded
        analyze_chart_button_clicked = st.button("Analyze Chart", key="analyze_chart_button", disabled=(uploaded_image is None))

        # Logic to trigger visual analysis when button is clicked AND it's a new or unanalyzed image
        if analyze_chart_button_clicked: # Button click takes precedence
            if uploaded_image.file_id != st.session_state.last_analyzed_image_id:
                with st.spinner(f"Analyzing the chart..."):
                    image_bytes = uploaded_image.getvalue()
                    image_mime_type = uploaded_image.type
                    visual_signal = ingest_and_analyze_visual(image_bytes, analysis_tool=ANALYSIS_TOOL_NAME, image_mime_type=image_mime_type)
                    
                    st.session_state.visual_analysis_result = visual_signal
                    st.session_state.last_analyzed_image_id = uploaded_image.file_id # Store the ID of the newly analyzed image
                    st.rerun() # Rerun to immediately display results
            else:
                st.info("Chart already analyzed. Displaying cached results.")

        # Display visual analysis results if available (persists across reruns)
        if st.session_state.visual_analysis_result:
            visual_signal = st.session_state.visual_analysis_result
            if "error" not in visual_signal:
                st.success("Visual analysis complete!" if analyze_chart_button_clicked and uploaded_image.file_id == st.session_state.last_analyzed_image_id else "Visual analysis results available.")
                st.subheader("Visual Signal Breakdown")
                st.write(f"**Signal Type:** `{visual_signal.get('signal_type', 'N/A')}`")
                st.write(f"**Confidence:** `{visual_signal.get('confidence', 0.0):.2f}`")
                st.write(f"**Suggested Strategy:** `{visual_signal.get('strategy', 'N/A')}`")
                st.write(f"**Risk/Reward:** `{visual_signal.get('risk_reward', 'N/A')}`")
                with st.expander("Detailed Analysis"):
                    st.markdown(str(visual_signal.get('details', 'No details.')))
            else:
                st.error(f"Visual Analysis Error: {visual_signal['error']}")
        elif uploaded_image: # If an image is uploaded but no analysis result yet
            st.info("Click 'Analyze Chart' to process the uploaded image.")
    else: # No image uploaded at all
        st.info("Upload an image to begin visual analysis.")
        # Clear visual state if no image is present
        st.session_state.visual_analysis_result = None
        st.session_state.last_analyzed_image_id = None


# Column 2: News & Sentiment Analysis
with col2:
    st.header("2. News & Sentiment Analysis")
    news_text_input = st.text_area("Enter relevant news article text:", key="news_text_input_area", height=300,
                                   value=st.session_state.news_text_input)

    final_text_for_sentiment = news_text_input
    
    # Analyze Sentiment button logic - ONLY runs the analysis, not the display
    if st.button("Analyze Sentiment", key="analyze_sentiment_button"):
        if final_text_for_sentiment.strip():
            with st.spinner("Analyzing sentiment..."):
                sentiment_result = analyze_sentiment(final_text_for_sentiment)
                st.session_state.sentiment_analysis_result = sentiment_result
        else:
            st.warning("Please enter news text to analyze sentiment.")

    # Display sentiment results persistently, outside the button block
    if st.session_state.sentiment_analysis_result: # Check if analysis has been performed
        sentiment_result = st.session_state.sentiment_analysis_result # Get the cached result
        if "error" in sentiment_result:
            st.error(f"Sentiment Analysis Error: {sentiment_result['error']}")
        else:
            st.success("Sentiment analysis complete!") 
            st.subheader("Sentiment Breakdown")
            st.markdown(f"**Sentiment:** `{sentiment_result.get('label', 'N/A')}`")
            st.markdown(f"**Score:** `{sentiment_result.get('score', 0.0):.2f}`")
            with st.expander("Sentiment Reason"):
                st.markdown(str(sentiment_result.get("reason", "No reason provided.")))
    elif news_text_input.strip() and not st.session_state.sentiment_analysis_result:
        st.info("Click 'Analyze Sentiment' to process the news text.")


st.markdown("---")
st.header("3. Multi-Modal Fusion & Trade Suggestion")

# Determine if fusion can proceed (prerequisites met)
can_fuse = (
    st.session_state.visual_analysis_result is not None and
    st.session_state.sentiment_analysis_result is not None and
    "error" not in st.session_state.visual_analysis_result and
    "error" not in st.session_state.sentiment_analysis_result
)

# Add the Perform Fusion button, disabled if prerequisites are not met
perform_fusion_button_clicked = st.button("Perform Fusion", key="perform_fusion_button", disabled=not can_fuse)

# Logic to trigger fusion when button is clicked
if perform_fusion_button_clicked and can_fuse:
    current_visual_id = st.session_state.last_analyzed_image_id
    current_news_hash = hash(st.session_state.news_text_input) 

    # Only perform fusion if inputs changed or it hasn't run for current inputs
    if st.session_state.fusion_result is None or \
       st.session_state.fusion_result.get('last_visual_id') != current_visual_id or \
       st.session_state.fusion_result.get('last_news_hash') != current_news_hash:
        with st.spinner("Fusing insights and generating suggestion..."):
            fusion_result = fuse_sentiment_and_visual(
                st.session_state.visual_analysis_result,
                final_text_for_sentiment,
                timestamp=st.session_state.current_time_ph
            )
            fusion_result['last_visual_id'] = current_visual_id
            fusion_result['last_news_hash'] = current_news_hash
            st.session_state.fusion_result = fusion_result
            st.rerun() # Rerun to immediately display results
    else:
        st.info("Fusion already performed for current visual and news data. Displaying cached results.")

# Display fusion result if available (always display if in session state)
if st.session_state.fusion_result and "error" not in st.session_state.fusion_result:
    fusion_result = st.session_state.fusion_result 
    st.success("Fusion complete!" if perform_fusion_button_clicked else "Fusion results available.")
    st.markdown(f"### **Trade Suggestion: {fusion_result.get('trade_suggestion', 'Hold')}**")
    st.markdown(f"**Confidence:** `{fusion_result.get('overall_confidence', 0.0):.2f}`")
    st.markdown(f"**Strategy:** `{fusion_result.get('strategy', 'N/A')}`")
    st.markdown(f"**Risk/Reward:** `{fusion_result.get('risk_reward', 'N/A')}`")
    
    with st.expander("Detailed Fusion Summary"):
        # Construct the Markdown table from the structured fusion_result
        entry = fusion_result.get('entry_point', 'N/A')
        
        # Join list items with proper comma and space
        targets = ", ".join(fusion_result.get('profit_targets', [])) if fusion_result.get('profit_targets') else 'N/A'
        support = ", ".join(fusion_result.get('support_levels', [])) if fusion_result.get('support_levels') else 'N/A'
        resistance = ", ".join(fusion_result.get('resistance_levels', [])) if fusion_result.get('resistance_levels') else 'N/A'
        
        stop_loss = fusion_result.get('stop_loss', 'N/A')
        rationale = fusion_result.get('rationale_summary', 'No detailed rationale provided.').strip()

        # Build the markdown table string
        table_markdown = f"""
| Metric           | Value                                     |
| :--------------- | :---------------------------------------- |
| **Entry Point** | {entry}                                   |
| **Targets** | {targets}                                 |
| **Support** | {support}                                 |
| **Resistance** | {resistance}                              |
| **Stop-Loss** | {stop_loss}                               |
"""
        st.markdown(table_markdown)
        st.markdown(f"**Rationale:** {rationale}") # Display rationale below the table

elif st.session_state.fusion_result and "error" in st.session_state.fusion_result:
     st.error(f"Fusion Error: {st.session_state.fusion_result['error']}")
elif can_fuse: # If prerequisites met but fusion not yet performed
    st.info("Click 'Perform Fusion' to combine visual and sentiment insights.")
else:
    st.info("Complete both visual and sentiment analysis steps without errors to enable fusion.")


# --- SIDEBAR: Chatbot for Trading Assistance ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">Ask TradeZight 📊</div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ Disclaimer"):
        st.write("""
            This is an AI-powered financial analysis tool. The trade suggestions are for informational purposes only and do not constitute financial advice. Always conduct your own research and consult with a professional financial advisor before making any investment decisions.
        """)

    # Container for chat messages to enable scrolling independently of the input
    chat_messages_container = st.container(height=500) 
    
    with chat_messages_container:
        # Display chat messages using st.chat_message
        for user_msg, bot_msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("ai"):
                st.write(bot_msg)

    # Chat input at the very bottom of the sidebar
    user_question = st.chat_input("Message TradeZight", key="sidebar_chat_input_unique")

    if user_question:
        # Prepare context for the chatbot
        chart_data = {
            "visual_analysis": st.session_state.visual_analysis_result,
            "sentiment_analysis": st.session_state.sentiment_analysis_result,
            "news_input": st.session_state.news_text_input,
            "fusion_result": st.session_state.fusion_result 
        }
        
        reply = run_chatbot(user_question, chart_data)
        st.session_state.chat_history.append((user_question, reply))
        st.rerun() # Rerun to update the chat history display immediately and clear input


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Jefferson Macasarte")
st.sidebar.markdown(f"Current Time (PH): {st.session_state.current_time_ph}")