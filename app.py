from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize translation pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        src_lang = data.get('src_lang', 'en')
        tgt_lang = data.get('tgt_lang', 'fr')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        start_time = time.time()

        # Load appropriate model for the language pair
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        try:
            translator = pipeline("translation", model=model_name)
        except:
            # Fallback to a default model if specific pair not available
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

        # Translate using transformers
        result = translator(text, max_length=512)

        end_time = time.time()
        time_ms = int((end_time - start_time) * 1000)

        return jsonify({
            'translated': result[0]['translation_text'],
            'time_ms': time_ms,
            'model': model_name
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)