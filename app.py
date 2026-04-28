"""
FarmDoctor AI — Standalone Streamlit App (Cloud Sync Fix)
"""
import os
import gdown

MODEL_PATH = "Backend/plant_disease_model.h5"
FILE_ID = "https://drive.google.com/file/d/1lL5puuUz-KOaOZRlvwFwI0iK_eHFL_Mn/view?usp=drive_link"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    os.makedirs("Backend", exist_ok=True)
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)
import streamlit as st
import json
import os
import sys
import uuid
import pandas as pd
import random
from datetime import datetime

# Path to backend directory for data storage
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Backend")

from Backend.groq_llm import get_groq_response, get_disease_cure_response
from Backend.image import predict_disease
from Backend.knowledge import knowledge_base
# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌿 FarmDoctor AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1a5e1f 0%, #2d8a34 50%, #43a047 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(26, 94, 31, 0.3);
    }
    .hero-banner h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .hero-banner p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f7f0 100%);
        border: 1px solid #e0e8e0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a5e1f;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #555;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Severity Badge */
    .severity-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        color: white;
    }

    /* Disease Info Card */
    .disease-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8faf8 100%);
        border: 1px solid #e0e8e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Chat Messages */
    .chat-user {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #43a047;
    }
    .chat-bot {
        background: linear-gradient(135deg, #f5f5f5, #eeeeee);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1a5e1f;
    }

    /* Sidebar Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3e1f 0%, #2d5a34 100%);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #888;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Session Initialization ─────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"


# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 FarmDoctor AI")
    st.markdown("---")

    page = st.radio(
        "Navigate to:",
        ["🏠 Home", "💬 AI Chatbot", "🔬 Disease Detection", "📈 Market Prices"],
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        "FarmDoctor AI is an intelligent agricultural assistant "
        "that helps farmers with crop disease identification, "
        "treatment recommendations, and farming best practices."
    )
    st.markdown("---")
    st.markdown("##### Made with ❤️ for Indian Farmers")


# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "🏠 Home":
    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <h1>🌿 FarmDoctor AI</h1>
        <p>Your Intelligent Agricultural Assistant — Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">AI Chatbot</div>
            <div class="feature-desc">
                Ask any farming question — crop advice, soil health,
                pest control, government schemes, and more.
                Powered by Groq LLM.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">Disease Detection</div>
            <div class="feature-desc">
                Upload a photo of your plant leaf and get instant
                AI-powered disease diagnosis with treatment
                recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Knowledge Base</div>
            <div class="feature-desc">
                Access detailed information about 38 crop diseases,
                including symptoms, pesticides, and prevention
                strategies.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Stats
    st.markdown("### 📊 Platform Features")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Crop Diseases", "38", help="Number of diseases in our database")
    with stat_col2:
        st.metric("Crops Covered", "14", help="Including tomato, potato, apple, corn, grape & more")
    with stat_col3:
        st.metric("AI Model", "Llama 3.3", help="Powered by Groq's fast LLM inference")
    with stat_col4:
        st.metric("Detection Model", "MobileNetV2", help="Transfer learning on PlantVillage dataset")

    # How to Use
    st.markdown("### 🚀 How to Use")
    st.markdown("""
    1. **💬 AI Chatbot** — Navigate to the chatbot page and type your farming question
    2. **🔬 Disease Detection** — Upload a clear photo of an affected leaf for AI analysis
    3. **📋 Get Results** — Receive instant disease diagnosis, treatment, and prevention tips
    """)

    st.markdown("""
    <div class="footer">
        FarmDoctor AI v1.0 • Built for Indian Farmers • AI-Powered Agricultural Assistance
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHATBOT PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "💬 AI Chatbot":
    st.markdown("## 💬 FarmDoctor AI Chatbot")

    # Language selector
    lang_col1, lang_col2 = st.columns([3, 1])
    with lang_col1:
        st.markdown("Ask me anything about farming, crops, diseases, soil, weather, or government schemes!")
    with lang_col2:
        language = st.selectbox(
            "🌐 Language",
            ["English", "Hindi", "Telugu", "Kannada", "Tamil", "Marathi"],
            key="chat_language",
            help="Choose your preferred language for responses",
        )

    # Localized labels per language
    _LANG_LABELS = {
        "Hindi": {
            "placeholder": "अपना कृषि प्रश्न यहाँ टाइप करें...",
            "thinking": "🌱 सोच रहा हूँ...",
        },
        "Telugu": {
            "placeholder": "మీ వ్యవసాయ ప్రశ్నను ఇక్కడ టైప్ చేయండి...",
            "thinking": "🌱 ఆలోచిస్తోంది...",
        },
        "Kannada": {
            "placeholder": "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ...",
            "thinking": "🌱 ಯೋಚಿಸುತ್ತಿದೆ...",
        },
        "Tamil": {
            "placeholder": "உங்கள் விவசாய கேள்வியை இங்கே டைப் செய்யுங்கள்...",
            "thinking": "🌱 யோசிக்கிறது...",
        },
        "Marathi": {
            "placeholder": "तुमचा शेतीविषयक प्रश्न इथे टाइप करा...",
            "thinking": "🌱 विचार करत आहे...",
        },
    }
    labels = _LANG_LABELS.get(language, {})
    chat_placeholder = labels.get("placeholder", "Type your farming question here...")
    thinking_text = labels.get("thinking", "🌱 Thinking...")

    st.markdown("---")

    # Chat history display
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👨‍🌾"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🌿"):
                st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input(chat_placeholder):
        # Display user message
        with st.chat_message("user", avatar="👨‍🌾"):
            st.markdown(prompt)

        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Get response
        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner(thinking_text):
                try:
                    # Standalone Cloud Mode: Call Groq directly
                    answer = get_groq_response(
                        query=prompt,
                        chat_history=st.session_state.chat_history[:-1],
                        language=language,
                    )
                except Exception as e:
                    answer = (
                        f"⚠️ Error: {str(e)}\n\n"
                        f"**To fix:**\n"
                        f"If you are on Streamlit Cloud, make sure you've added the `GROQ_API_KEY` to the **Secrets** section."
                    )

                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Chat Actions (Clear, Save, Load)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    history_file = os.path.join(backend_dir, "chat_history.json")

    with col1:
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                try:
                    # Also delete the saved file if it exists
                    if os.path.exists(history_file):
                        os.remove(history_file)
                except Exception:
                    pass
                st.rerun()

    with col2:
        if st.session_state.chat_history:
            if st.button("💾 Save Chat History", type="primary", use_container_width=True):
                try:
                    with open(history_file, 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=4)
                    st.success("Chat history saved successfully!")
                except Exception as e:
                    st.error(f"Failed to save history: {e}")

    with col3:
        if os.path.exists(history_file):
            if st.button("📂 Load Chat History", type="secondary", use_container_width=True):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        st.session_state.chat_history = json.load(f)
                    st.success("Chat history loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load history: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# DISEASE DETECTION PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "🔬 Disease Detection":
    st.markdown("## 🔬 Plant Disease Detection")
    st.markdown("Upload a photo of a plant leaf to detect diseases and get treatment recommendations.")

    # Language selector for AI Cure
    _det_lang_col1, _det_lang_col2 = st.columns([3, 1])
    with _det_lang_col2:
        detection_language = st.selectbox(
            "🌐 AI Cure Language",
            ["English", "Hindi", "Telugu", "Kannada", "Tamil", "Marathi"],
            key="detection_language",
            help="Language for the AI-generated treatment plan",
        )
    st.markdown("---")

    # Upload section
    col_upload, col_info = st.columns([1, 1])

    with col_upload:
        st.markdown("### 📸 Upload Leaf Image")
        uploaded_file = st.file_uploader(
            "Choose a clear photo of the affected leaf",
            type=["jpg", "jpeg", "png", "webp"],
            help="For best results, take a clear, well-lit photo of a single leaf",
        )

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    with col_info:
        st.markdown("### 📋 Tips for Best Results")
        st.info("""
        📌 **How to take a good photo:**
        - Use natural daylight (avoid flash)
        - Focus on a single affected leaf
        - Include both healthy and diseased areas
        - Keep the image sharp and in focus
        - Avoid shadows on the leaf
        """)

        st.markdown("### 🌱 Supported Crops")
        st.markdown("""
        Apple • Blueberry • Cherry • Corn • Grape • Orange  
        Peach • Pepper • Potato • Raspberry • Soybean  
        Squash • Strawberry • Tomato • Many more...
        """)

    # Analyze button
    if uploaded_file is not None:
        st.markdown("---")
        if st.button("🔍 Analyze Leaf", type="primary", use_container_width=True):
            with st.spinner("🔬 Analyzing image with AI..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    # Standalone Cloud Mode: Call prediction directly
                    result = predict_disease(image_bytes)

                    if result.get("error"):
                        st.error(f"❌ {result['message']}")
                    else:
                        # Store results in session_state so they persist across reruns
                        st.session_state.last_analysis_result = result
                        info = result.get("disease_info")
                        st.session_state.last_disease_info = info
                        if info:
                            parts = result["class_name"].split("__")
                            st.session_state.last_crop_name = parts[0].replace("_", " ").strip() if parts else "Unknown Crop"
                        else:
                            st.session_state.last_crop_name = result.get("class_name", "Unknown").split("__")[0]
                        # Clear any previous AI cure response
                        st.session_state.pop("last_cure_response", None)

                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

    # ── Display stored analysis results (persists across reruns) ──────────
    if "last_analysis_result" in st.session_state:
        result = st.session_state.last_analysis_result
        info = st.session_state.last_disease_info
        crop_name = st.session_state.last_crop_name

        st.success(f"✅ Analysis Complete — Confidence: **{result['confidence']}%**")
        if 'debug_index' in result:
            st.caption(f"Raw Model Prediction Index: {result['debug_index']}")

        if info:
            # Explicit Crop and Disease Info
            st.markdown(f"### 🌾 Crop Identified: **{crop_name}**")
            st.markdown(f"### 🦠 Disease Detected: **{info['display_name']}**")

            severity = info.get("severity", "Unknown")
            severity_colors = {
                "None": "#28a745",
                "Low": "#90EE90",
                "Moderate": "#FFA500",
                "High": "#FF4500",
                "Very High": "#DC143C",
                "Unknown": "#808080",
            }
            color = severity_colors.get(severity, "#808080")
            st.markdown(
                f'<span class="severity-badge" style="background:{color}">'
                f"Severity: {severity}</span>",
                unsafe_allow_html=True,
            )

            # Description
            st.markdown(f"**📝 Description:** {info['description']}")
            st.markdown("---")

            # Make Pesticides and Prevention explicit, not hidden in tabs
            col_treat, col_prev = st.columns(2)

            with col_treat:
                st.markdown("### 💊 Pesticides & Treatment")
                if info.get("pesticides"):
                    for pesticide in info.get("pesticides", []):
                        search_query = pesticide.replace(" ", "+")
                        amazon_link = f"https://www.amazon.in/s?k={search_query}+pesticide"
                        st.markdown(f"- {pesticide} &nbsp; [🛒 Buy Now]({amazon_link})")
                else:
                    st.markdown("- No chemical treatment required.")

            with col_prev:
                st.markdown("### 🛡️ Prevention Tips")
                if info.get("prevention"):
                    for tip in info.get("prevention", []):
                        st.markdown(f"- {tip}")
                else:
                    st.markdown("- Keep plant healthy.")

            st.markdown("### 🔍 Symptoms")
            with st.expander("View Symptoms", expanded=False):
                for symptom in info.get("symptoms", []):
                    st.markdown(f"- {symptom}")
        else:
            st.info(f"Detected class: **{result['class_name']}**")

        # ── AI-Powered Cure Section (now outside the Analyze button block) ──
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Treatment Plan")
        st.markdown("Get a **detailed, personalized treatment plan** generated by AI based on the diagnosis above.")

        if st.button("🤖 Get AI Treatment Plan", type="primary", use_container_width=True):
            with st.spinner("🧠 Generating detailed treatment plan..."):
                try:
                    cure_info = info if info else {}
                    cure_response = get_disease_cure_response(
                        crop_name=crop_name,
                        disease_name=cure_info.get("display_name", result.get("class_name", "Unknown")),
                        severity=cure_info.get("severity", "Unknown"),
                        symptoms=cure_info.get("symptoms", []),
                        pesticides=cure_info.get("pesticides", []),
                        prevention=cure_info.get("prevention", []),
                        language=detection_language,
                    )
                    st.session_state.last_cure_response = cure_response
                except Exception as cure_err:
                    st.error(f"⚠️ Could not generate AI treatment plan: {str(cure_err)}")

        # Display cached AI cure response
        if "last_cure_response" in st.session_state:
            st.markdown(st.session_state.last_cure_response)

    # ── Complete Crop & Disease Reference ─────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌾 Complete Crop Disease & Pesticide Reference")
    st.markdown("Browse all **14 crops** and **38 disease classes** with recommended pesticides and prevention tips.")

    # Organize by crop name - Use all available diseases in the knowledge base
    all_diseases = knowledge_base.get_all_disease_names()
    crops = {}
    for class_name in all_diseases:
        parts = class_name.split("__")
        crop = parts[0].replace("_", " ").strip()
        if crop not in crops:
            crops[crop] = []
        crops[crop].append(class_name)

    # Crop emoji mapping (Expanded)
    crop_emojis = {
        "Apple": "🍎", "Blueberry": "🫐", "Cherry (including sour)": "🍒",
        "Corn (maize)": "🌽", "Grape": "🍇", "Orange": "🍊",
        "Peach": "🍑", "Pepper bell": "🫑", "Potato": "🥔",
        "Raspberry": "🫐", "Soybean": "🫘", "Squash": "🎃",
        "Strawberry": "🍓", "Tomato": "🍅",
        "Rice": "🌾", "Wheat": "🌾", "Cotton": "☁️",
        "Groundnut": "🥜", "Sugarcane": "🎋", "Chilli": "🌶️",
        "Mango": "🥭", "Banana": "🍌", "Onion": "🧅",
        "Mustard": "🌼", "Turmeric": "🧂"
    }

    # Quick stats
    total_diseases = len([c for c in all_diseases if "healthy" not in c.lower()])
    st.markdown(
        f"**📊 Coverage:** `{len(crops)}` crops • `{total_diseases}` diseases • `{len(all_diseases)}` total entries"
    )

    # Search / filter
    search_crop = st.text_input("🔍 Search crops:", placeholder="e.g., Rice, Wheat, Tomato, Mango...")

    for crop_name, disease_list in sorted(crops.items()):
        # Apply search filter
        if search_crop and search_crop.lower() not in crop_name.lower():
            continue

        emoji = crop_emojis.get(crop_name, "🌱")
        diseases = [c for c in disease_list if "healthy" not in c.lower()]
        healthy = [c for c in disease_list if "healthy" in c.lower()]

        with st.expander(f"{emoji} **{crop_name}** — {len(diseases)} disease(s)", expanded=False):

            # Show healthy status (only if it's in the ML model)
            if healthy:
                st.success(f"✅ **Healthy {crop_name}** is included in our detection model")
            elif crop_name in ["Rice", "Wheat", "Cotton", "Groundnut", "Sugarcane", "Chilli", "Mango", "Banana", "Onion", "Mustard", "Turmeric"]:
                st.info(f"ℹ️ **{crop_name}** is available in the knowledge base (manual identification)")

            if not diseases:
                st.info(f"No diseases recorded for {crop_name} — only healthy detection available.")
                continue

            # Show each disease
            for class_name in diseases:
                info = knowledge_base.get_disease_info(class_name)
                if not info:
                    continue

                disease_name = info.get("display_name", class_name)
                severity = info.get("severity", "Unknown")
                severity_colors = {
                    "None": "#28a745", "Low": "#90EE90",
                    "Moderate": "#FFA500", "High": "#FF4500",
                    "Very High": "#DC143C", "Unknown": "#808080",
                }
                color = severity_colors.get(severity, "#808080")

                st.markdown(f"#### 🦠 {disease_name}")
                st.markdown(
                    f'<span class="severity-badge" style="background:{color}">'
                    f'Severity: {severity}</span>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"*{info.get('description', '')}*")

                tab1, tab2, tab3 = st.tabs([
                    f"🔍 Symptoms",
                    f"💊 Pesticides & Treatment",
                    f"🛡️ Prevention",
                ])

                with tab1:
                    for s in info.get("symptoms", []):
                        st.markdown(f"• {s}")

                with tab2:
                    st.markdown("**Recommended Pesticides / Treatments:**")
                    for idx, p in enumerate(info.get("pesticides", []), 1):
                        search_query = p.replace(" ", "+")
                        amazon_link = f"https://www.amazon.in/s?k={search_query}+pesticide"
                        st.markdown(f"**{idx}.** {p} &nbsp; [🛒 Buy Now]({amazon_link})")

                with tab3:
                    for t in info.get("prevention", []):
                        st.markdown(f"• {t}")

                st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# MARKET PRICES PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "📈 Market Prices":
    st.markdown("## 📈 Real-Time Market Prices (Mandi Rates)")
    st.markdown("Check the latest agricultural commodity prices across different states and markets to sell your crops at the best price.")
    st.markdown("---")
    
    # State selection
    states = ["Maharashtra", "Karnataka", "Andhra Pradesh", "Telangana", "Punjab", "Gujarat"]
    selected_state = st.selectbox("📍 Select State:", states)
    
    # Crop search
    crop_search = st.text_input("🔍 Search Crop:", placeholder="e.g., Tomato, Cotton, Wheat...")
    
    # Simulated Mandi Data (Realistic for demonstration)
    # In a real production app, this would be fetched from data.gov.in APIs
    
    # Generate realistic dummy data
    today = datetime.now().strftime("%d %b %Y")
    
    # Use local Random instance so prices stay consistent within a day for same inputs
    # without mutating the global random state
    rng = random.Random(f"{today}_{selected_state}_{crop_search}")
    
    commodity_list = ["Tomato", "Potato", "Onion", "Cotton", "Wheat", "Rice", "Soybean", "Maize", "Green Gram", "Red Gram", "Chilli"]
    markets_by_state = {
        "Maharashtra": ["Pune", "Nashik", "Nagpur", "APMC Mumbai"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Belagavi"],
        "Andhra Pradesh": ["Guntur", "Kurnool", "Anantapur", "Vijayawada"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam"],
        "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
        "Gujarat": ["Ahmedabad", "Surat", "Rajkot", "Vadodara"]
    }
    
    mandi_data = []
    
    # Ensure the searched crop is included if there's a search term
    crops_to_show = commodity_list.copy()
    if crop_search and crop_search.title() not in crops_to_show:
        crops_to_show.insert(0, crop_search.title())
         
    for market in markets_by_state[selected_state]:
        # Pick 4-6 random crops for this market
        market_crops = rng.sample(crops_to_show, min(rng.randint(4, 6), len(crops_to_show)))
        
        # Force include searched crop if provided
        if crop_search and crop_search.title() not in market_crops:
            market_crops[0] = crop_search.title()
            
        for crop in market_crops:
            if crop_search and crop_search.lower() not in crop.lower():
                continue
                
            # Base price logic
            base_price = 1000
            if "Tomato" in crop: base_price = rng.randint(1500, 3500)
            elif "Cotton" in crop: base_price = rng.randint(6000, 8000)
            elif "Wheat" in crop: base_price = rng.randint(2200, 2600)
            elif "Onion" in crop: base_price = rng.randint(1200, 4500)
            else: base_price = rng.randint(1500, 5000)
            
            min_p = int(base_price * 0.9)
            max_p = int(base_price * 1.1)
            model_p = int((min_p + max_p) / 2)
            
            mandi_data.append({
                "Commodity (Crop)": f"🌾 {crop}",
                "Market Center": market,
                "Min Price (₹/Quintal)": min_p,
                "Max Price (₹/Quintal)": max_p,
                "Modal Price (₹/Quintal)": model_p,
                "Date": today
            })
            
    if mandi_data:
        df = pd.DataFrame(mandi_data)
        
        # Display as a clean dataframe
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True,
            column_config={
                "Min Price (₹/Quintal)": st.column_config.NumberColumn(format="₹ %d"),
                "Max Price (₹/Quintal)": st.column_config.NumberColumn(format="₹ %d"),
                "Modal Price (₹/Quintal)": st.column_config.NumberColumn(format="₹ %d", help="Most common trading price"),
            }
        )
        
        # Show some trends
        st.markdown("### 📊 Price Insights")
        avg_price = df["Modal Price (₹/Quintal)"].mean()
        highest_price = df.loc[df["Modal Price (₹/Quintal)"].idxmax()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Average crop price** across {selected_state} today is **₹{int(avg_price)}/Quintal**.")
        with col2:
            st.success(f"**Highest paying market** for {highest_price['Commodity (Crop)']} is **{highest_price['Market Center']}** at **₹{highest_price['Max Price (₹/Quintal)']}**.")
             
        st.markdown("*Note: This is simulated data for demonstration purposes based on typical Indian market price ranges.*")
    else:
        st.warning(f"No market data found currently for '{crop_search}' in {selected_state}.")
