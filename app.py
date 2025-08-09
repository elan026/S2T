from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    transcript_text = request.form.get('transcript_text', '')
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Generate filename with timestamp
    filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join('downloads', filename)
    
    # Save transcript to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    
    # Send file to user
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
#hii