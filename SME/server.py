from flask import Flask, request, jsonify, render_template, send_file
from services.document_service import DocumentService
import os
from app_config import GENERATED_FOLDER

app = Flask(__name__)
doc_service = DocumentService()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({
            "type": "text",
            "response": "❌ No message received."
        })

    try:
        result = doc_service.process(message)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "type": "text",
            "response": f"⚠️ Error: {str(e)}"
        })

@app.route("/switch", methods=["POST"])
def switch_personality():
    data = request.json
    new_mode = data.get("mode", "").upper()

    if new_mode not in ["HR", "ADMIN"]:
        return jsonify({"response": "❌ Invalid mode. Choose HR or Admin."}), 400

    doc_service.switch_personality(new_mode)
    return jsonify({"response": f"✅ Switched to {new_mode} mode."})

@app.route("/download/<path:filename>")
def download_file(filename):
    full_path = os.path.join(GENERATED_FOLDER, filename)
    return send_file(full_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
