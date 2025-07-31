import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import threading

st.title("🎙️ Voice Chatbot")

# Initialize recognizer and TTS
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

def listen():
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        st.success("Recognizing...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        st.error("Could not understand audio.")
        return None
    except sr.RequestError:
        st.error("Speech recognition service error.")
        return None

def get_response_from_backend(text):
    try:
        response = requests.post("http://localhost:8000/chat", json={"message": text})
        return response.json().get("response", "No reply.")
    except requests.exceptions.RequestException as e:
        st.error(f"Backend error: {e}")
        return "Failed to get a response."

# Main interface
if st.button("Start Voice Chat"):
    user_text = listen()
    if user_text:
        st.text(f"🗣️ You said: {user_text}")
        response = get_response_from_backend(user_text)
        st.text(f"Bot : {response}")
        speak(response)
