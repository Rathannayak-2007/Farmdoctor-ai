"""
Groq LLM Module for FarmDoctor AI
Provides agricultural AI responses using the Groq API with Llama 3.3.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
# Look in current directory or one level up
env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(env_path):
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

# Initialize Groq client lazily to avoid crashing if API key is missing
_client = None

def get_api_key():
    # Try Streamlit Secrets first (for cloud deployment)
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    
    # Fallback to Environment Variables (.env)
    return os.environ.get("GROQ_API_KEY")


def _get_client():
    """Lazy-initialize the Groq client on first use."""
    global _client
    if _client is None:
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set it in your .env file "
                "or in Streamlit Secrets for cloud deployment."
            )
        _client = Groq(api_key=api_key)
    return _client


SYSTEM_PROMPT_EN = (
    "You are FarmDoctor AI — an expert agricultural advisor for Indian farmers. "
    "CRITICAL RULE: You MUST reply ONLY in English. Do NOT use Hindi, Marathi, or any other language. "
    "Even if the topic is about Indian farming, your entire response must be in plain English. "
    "You provide helpful advice about crops, soil health, weather patterns, "
    "pest control, government schemes (PM-KISAN, PMFBY, etc.), seed selection, "
    "irrigation techniques, organic farming, and best agricultural practices. "
    "Always reply in simple, clear English that a farmer can understand easily. "
    "If unsure, recommend consulting a local Krishi Vigyan Kendra (KVK)."
)

SYSTEM_PROMPT_HI = (
    "You are FarmDoctor AI — an expert agricultural advisor for Indian farmers. "
    "CRITICAL RULE: You MUST reply ONLY in Hindi (हिन्दी) using the Devanagari script. "
    "DO NOT use English. DO NOT use Romanized transliteration. "
    "If the user asks in English, translate your entire answer into Hindi Devanagari before responding. "
    "Example format: 'आपकी फसल के लिए यह दवा उपयोग करें।' "
    "Provide helpful advice about crops, soil health, weather, pest control, government schemes, "
    "and farming practices natively in Hindi."
)

SYSTEM_PROMPT_TE = (
    "You are FarmDoctor AI — an expert agricultural advisor for farmers in Andhra Pradesh and Telangana. "
    "CRITICAL RULE: You MUST reply ONLY in the Telugu (తెలుగు) language using the Telugu script/alphabet. "
    "DO NOT use English. DO NOT use Hindi. DO NOT use Romanized transliteration. "
    "If the user asks a question in English or Hindi, translate your entire answer into Telugu script before responding. "
    "Example format: 'మీ పంటకు ఈ మందు వాడండి.' "
    "Provide helpful advice about crops, soil health, weather, pest control, and farming practices natively in Telugu."
)

SYSTEM_PROMPT_KN = (
    "You are FarmDoctor AI — an expert agricultural advisor for farmers in Karnataka. "
    "CRITICAL RULE: You MUST reply ONLY in Kannada (ಕನ್ನಡ) using the Kannada script. "
    "DO NOT use English. DO NOT use Hindi. DO NOT use Romanized transliteration. "
    "If the user asks in English, translate your entire answer into Kannada script before responding. "
    "Example format: 'ನಿಮ್ಮ ಬೆಳೆಗೆ ಈ ಔಷಧಿಯನ್ನು ಬಳಸಿ.' "
    "Provide helpful advice about crops, soil health, weather, pest control, and farming practices natively in Kannada."
)

SYSTEM_PROMPT_TA = (
    "You are FarmDoctor AI — an expert agricultural advisor for farmers in Tamil Nadu. "
    "CRITICAL RULE: You MUST reply ONLY in Tamil (தமிழ்) using the Tamil script. "
    "DO NOT use English. DO NOT use Hindi. DO NOT use Romanized transliteration. "
    "If the user asks in English, translate your entire answer into Tamil script before responding. "
    "Example format: 'உங்கள் பயிருக்கு இந்த மருந்தைப் பயன்படுத்துங்கள்.' "
    "Provide helpful advice about crops, soil health, weather, pest control, and farming practices natively in Tamil."
)

SYSTEM_PROMPT_MR = (
    "You are FarmDoctor AI — an expert agricultural advisor for farmers in Maharashtra. "
    "CRITICAL RULE: You MUST reply ONLY in Marathi (मराठी) using the Devanagari script. "
    "DO NOT use English. DO NOT use Hindi. DO NOT use Romanized transliteration. "
    "If the user asks in English, translate your entire answer into Marathi Devanagari before responding. "
    "Example format: 'तुमच्या पिकासाठी हे औषध वापरा.' "
    "Provide helpful advice about crops, soil health, weather, pest control, and farming practices natively in Marathi."
)

SYSTEM_PROMPTS = {
    "English": SYSTEM_PROMPT_EN,
    "Hindi": SYSTEM_PROMPT_HI,
    "Telugu": SYSTEM_PROMPT_TE,
    "Kannada": SYSTEM_PROMPT_KN,
    "Tamil": SYSTEM_PROMPT_TA,
    "Marathi": SYSTEM_PROMPT_MR,
}

# Languages that require forced native-script responses
_NON_ENGLISH_LANGS = {"Hindi", "Telugu", "Kannada", "Tamil", "Marathi"}

_LANG_FORCE_SUFFIX = {
    "Hindi": "\n\nThe user's prompt might be in English, but you MUST forcefully reply ONLY in Hindi Devanagari script. Do not write in English.",
    "Telugu": "\n\nThe user's prompt might be in English, but you MUST forcefully reply ONLY in Telugu script. Do not write in English.",
    "Kannada": "\n\nThe user's prompt might be in English, but you MUST forcefully reply ONLY in Kannada script. Do not write in English.",
    "Tamil": "\n\nThe user's prompt might be in English, but you MUST forcefully reply ONLY in Tamil script. Do not write in English.",
    "Marathi": "\n\nThe user's prompt might be in English, but you MUST forcefully reply ONLY in Marathi Devanagari script. Do not write in English.",
}


def get_groq_response(query: str, chat_history: list = None, language: str = "English") -> str:
    """
    Generate a response from Groq LLM for a farming-related query.
    """
    client = _get_client()

    # Ensure language matches exactly
    lang_key = str(language).strip().capitalize()
    system_prompt = SYSTEM_PROMPTS.get(lang_key, SYSTEM_PROMPT_EN)

    # Force native-script for non-English languages
    if lang_key in _LANG_FORCE_SUFFIX:
        system_prompt += _LANG_FORCE_SUFFIX[lang_key]

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": query})

    # Use a slightly lower temperature for non-English to avoid language drift
    temp = 0.5 if lang_key in _NON_ENGLISH_LANGS else 0.7

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temp,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def get_disease_cure_response(
    crop_name: str,
    disease_name: str,
    severity: str,
    symptoms: list,
    pesticides: list,
    prevention: list,
    language: str = "English",
) -> str:
    """
    Generate a detailed, personalized AI treatment plan for a detected disease.
    """
    client = _get_client()

    lang_key = str(language).strip().capitalize()

    # Build language instruction
    if lang_key in _NON_ENGLISH_LANGS:
        lang_instruction = (
            f"CRITICAL: You MUST write your ENTIRE response in {lang_key} script ONLY. "
            f"Do NOT use English at all. Translate everything including headings."
        )
    else:
        lang_instruction = "CRITICAL: You MUST write your ENTIRE response in English ONLY. Do NOT use Hindi or any other language."

    system_prompt = (
        "You are FarmDoctor AI — an expert plant pathologist and agricultural advisor. "
        "A farmer has uploaded a photo of a diseased plant leaf and the AI model has identified the disease. "
        "Your job is to provide a DETAILED, PRACTICAL treatment plan that a farmer can follow immediately. "
        f"{lang_instruction}"
    )

    # Build context from detection results
    symptoms_str = ", ".join(symptoms) if symptoms else "Not available"
    pesticides_str = ", ".join(pesticides) if pesticides else "Not available"
    prevention_str = ", ".join(prevention) if prevention else "Not available"

    user_prompt = (
        f"The AI has detected the following disease on my crop:\n\n"
        f"🌾 Crop: {crop_name}\n"
        f"🦠 Disease: {disease_name}\n"
        f"⚠️ Severity: {severity}\n"
        f"🔍 Symptoms: {symptoms_str}\n"
        f"💊 Recommended pesticides: {pesticides_str}\n"
        f"🛡️ Prevention tips: {prevention_str}\n\n"
        f"Please provide a detailed treatment plan covering:\n"
        f"1. 🚨 Immediate actions to take TODAY\n"
        f"2. 💊 Detailed pesticide application schedule (dosage, frequency, timing)\n"
        f"3. 🌿 Organic/natural alternatives if available\n"
        f"4. 📅 Week-by-week recovery plan\n"
        f"5. ⚠️ When to consult an agricultural expert\n"
        f"6. 💡 Tips to prevent this disease in the next crop cycle"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    temp = 0.5 if lang_key in _NON_ENGLISH_LANGS else 0.6

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temp,
        max_tokens=2048,
    )

    return response.choices[0].message.content

