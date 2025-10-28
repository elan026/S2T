import streamlit as st
import os
from datetime import datetime
import requests
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av
import numpy as np
import queue
import threading
import time

# Language options mapping for LibreTranslate
LANG_OPTIONS = {
    "English (India)": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Bengali": "bn"
}

def main():
    st.set_page_config(page_title="Speech to Text", layout="centered")
    st.title("Speech to Text")
    st.markdown("""
    <style>
        .stTextArea textarea {height: 200px !important;}
    </style>
    """, unsafe_allow_html=True)

    # Language selector
    lang_display = st.selectbox(
        "Select Language",
        list(LANG_OPTIONS.keys()),
        index=0
    )
    lang_code = LANG_OPTIONS[lang_display]

    st.info("Paste your transcript below. Optionally, translate it to the selected language.")

    transcript_text = st.text_area("Transcript Text", "", key="transcript")

    translate = st.button("Translate Transcript")
    translated_text = transcript_text

    if translate and transcript_text.strip():
        try:
            response = requests.post(
                "https://libretranslate.de/translate",
                json={
                    "q": transcript_text,
                    "source": "auto",
                    "target": lang_code
                },
                headers={"Content-Type": "application/json"}
            )
            if response.ok:
                translated_text = response.json().get("translatedText", transcript_text)
                st.success("Translation successful!")
            else:
                st.error("Translation failed.")
        except Exception as e:
            st.error(f"Translation error: {e}")

    st.text_area("Translated Transcript", translated_text, key="translated", height=200)

    if st.button("Download Transcript"):
        if translated_text.strip():
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join("downloads", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(translated_text)
            with open(filepath, "rb") as f:
                st.download_button(
                    label="Click to Download",
                    data=f,
                    file_name=filename,
                    mime="text/plain"
                )
        else:
            st.warning("Please enter some transcript text before downloading.")

    st.info("You can upload an audio file (wav, mp3, m4a) to transcribe using Whisper via Hugging Face.")
    uploaded_audio = st.file_uploader("Upload Audio File for Speech Recognition", type=["wav", "mp3", "m4a"])
    transcript_from_audio = ""
    if uploaded_audio is not None:
        st.audio(uploaded_audio, format="audio/wav")
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing audio using Whisper (Hugging Face)..."):
                try:
                    files = {"file": uploaded_audio}
                    response = requests.post(
                        "https://api-inference.huggingface.co/models/openai/whisper-large-v2",
                        headers={"accept": "application/json"},
                        files=files
                    )
                    if response.ok:
                        result = response.json()
                        transcript_from_audio = result.get("text", "")
                        st.success("Transcription complete!")
                        st.text_area("Transcript from Audio", transcript_from_audio, height=150)
                    else:
                        st.error(f"Transcription failed: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.header("🎤 Real-time Speech-to-Text (Microphone)")
    st.write("Start the microphone and get real-time transcript below.")

    transcript_placeholder = st.empty()
    audio_queue = queue.Queue()
    transcript_result = ""

    # Define AudioProcessor class for streamlit-webrtc
    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.buff = b""
        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            audio = frame.to_ndarray()
            self.buff += audio.tobytes()
            audio_queue.put(self.buff)
            return frame

    def transcribe_audio_stream():
        nonlocal transcript_result
        while True:
            if not audio_queue.empty():
                audio_bytes = audio_queue.get()
                # Send to Whisper via Hugging Face
                try:
                    response = requests.post(
                        "https://api-inference.huggingface.co/models/openai/whisper-large-v2",
                        headers={"accept": "application/json"},
                        files={"file": ("audio.wav", audio_bytes, "audio/wav")}
                    )
                    if response.ok:
                        result = response.json()
                        transcript_result = result.get("text", "")
                        transcript_placeholder.text_area("Real-time Transcript", transcript_result, height=150)
                    else:
                        transcript_placeholder.error(f"Transcription failed: {response.text}")
                except Exception as e:
                    transcript_placeholder.error(f"Error: {e}")
            time.sleep(2)

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDRECV,
        audio_receiver_size=256,
        video_receiver_size=0,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    if webrtc_ctx.state.playing:
        threading.Thread(target=transcribe_audio_stream, daemon=True).start()

    st.markdown("<footer style='text-align:center; color:#888; margin-top:2em;'>© Created by Elango and Team</footer>", unsafe_allow_html=True)

main()