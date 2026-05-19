from flask import Flask, render_template, request, jsonify, send_file
from downloader import download_audio
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'No URL provided.'}), 400
        
    try:
        file_path = download_audio(url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("\nStarting SongSnatcher server on http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)
