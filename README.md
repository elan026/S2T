# Speech-to-Text Web Application

## Overview
This is a **Speech-to-Text Web Application** that supports real-time speech recognition in **9+ Indian languages**, including Hindi, Tamil, Telugu, Kannada, and more. It allows users to transcribe their speech, view the live text output, and download the transcript as a **.docx** file.

## Features
- **Supports Multiple Indian Languages** (English, Hindi, Tamil, Telugu, Kannada, etc.)
- **Real-Time Speech Recognition** using Web Speech API
- **Start & Stop Recording Buttons** for user control
- **Live Transcription Display** in a text area
- **Download Transcript** as a .docx file
- **Responsive & Interactive UI** with a modern design

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Speech Recognition:** Web Speech API
- **File Handling:** Python-Docx

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repository/speech-to-text-webapp.git
cd speech-to-text-webapp
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application
```bash
python app.py
```

### 5. Open in Browser
Go to `http://127.0.0.1:5000` in your web browser.

## Usage
1. **Select a Language** from the dropdown menu.
2. Click **Start Recording** to begin transcription.
3. Speak into your microphone, and the text will appear in real time.
4. Click **Stop Recording** when finished.
5. Click **Download Transcript** to save your speech as a .docx file.

## Supported Languages
- **English (India)** (`en-IN`)
- **Hindi** (`hi-IN`)
- **Tamil** (`ta-IN`)
- **Telugu** (`te-IN`)
- **Kannada** (`kn-IN`)
- **Malayalam** (`ml-IN`)
- **Gujarati** (`gu-IN`)
- **Marathi** (`mr-IN`)
- **Punjabi** (`pa-IN`)
- **Bengali** (`bn-IN`)

## File Structure
```
Create a Virtual Environment

Speech-to-Text-WebApp/
│── downloads/static/
│   ├── styles.css  # CSS for styling
│── templates/
│   ├── index.html  # Frontend UI
│── uploads/        # Stores downloaded transcripts
│── app.py          # Flask backend
│── requirements.txt # Required dependencies
│── README.md       # Documentation
```

## Dependencies
Ensure you have the following Python packages installed:
```bash
Flask
python-docx
```

## License
This project is licensed under the MIT License.

## Contributing
Feel free to fork this repository and submit pull requests.

## Author
[Elango Kandhasamy]https://github.com/elan026



