from flask import Flask, request, render_template, jsonify
from summarizer import extract_article_text, summarize_text
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Get API_KEY from .env
API_KEY = os.getenv("API_KEY")

@app.before_request
def require_api_key():
    if request.path == '/summarize':
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
    else:  # GET
        url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    text, title = extract_article_text(url)
    if not text:
        return jsonify({'error': 'Failed to extract article'}), 500

    sentence_list, best_sentences = summarize_text(text)
    return render_template("summary.html", title=title, sentences=sentence_list, best_sentences=best_sentences)

if __name__ == '__main__':
    app.run(debug=True)
