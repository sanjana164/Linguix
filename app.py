from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get("text")
    src = data.get("src_lang", "auto")
    tgt = data.get("tgt_lang", "en")

    translated = GoogleTranslator(source=src, target=tgt).translate(text)
    english = GoogleTranslator(source=src, target="en").translate(text)

    return jsonify({
        "translated": translated,
        "english": english,
        "time_ms": 100,
        "model": "google-translator"
    })

if __name__ == "__main__":
    app.run(debug=True)