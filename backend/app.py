from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import os
from collections import Counter

# ---------- Service Imports ----------
from services.file_parser import read_file
from services.nlp_engine import extract_entities
from services.language_detector import detect_language
from services.strategy_detector import detect_strategy_ml
from services.pattern_analyzer import detect_crime_patterns
from services.charts import generate_charts
from services.strategy_pattern_detector import detect_same_strategy_across_locations
# ------------------------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- Helper ----------
def safe_first(value):
    if isinstance(value, list) and len(value) > 0:
        return value[0]
    return None


# ---------- Routes ----------

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "MCIAP Backend Running"
    })


@app.route("/upload-ui")
def upload_ui():
    return render_template("upload.html")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/upload", methods=["POST"])
def upload_files():

    files = request.files.getlist("files")

    file_names = []
    languages = []
    records = []

    # ---------- File Processing ----------
    for file in files:
        if not file or file.filename == "":
            continue

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_names.append(file.filename)

        content = read_file(file_path)

        lang = detect_language(content)
        languages.append(lang)

        entities = extract_entities(content)

        phones = entities.get("phones", [])
        vehicles = entities.get("vehicles", [])
        ips = entities.get("ips", [])
        states = entities.get("states", [])
        crimes = entities.get("crimes", [])

        strategy = detect_strategy_ml(content, lang)

        records.append({
            "file": file.filename,
            "state": safe_first(states),
            "phone": safe_first(phones),
            "vehicle": safe_first(vehicles),
            "ip": safe_first(ips),
            "crime": safe_first(crimes) or "Cyber Fraud",
            "strategy": strategy
        })

    # ---------- Repeated Identifier Logic (FINAL & CORRECT) ----------
    phones_all = [r["phone"] for r in records if r["phone"]]
    vehicles_all = [r["vehicle"] for r in records if r["vehicle"]]
    ips_all = [r["ip"] for r in records if r["ip"]]

    repeated_phones = [k for k, v in Counter(phones_all).items() if v > 1]
    repeated_vehicles = [k for k, v in Counter(vehicles_all).items() if v > 1]
    repeated_ips = [k for k, v in Counter(ips_all).items() if v > 1]

    # ---------- Charts ----------
    charts = generate_charts(records) if records else None

    # ---------- Strategy Patterns ----------
    strategy_alerts = detect_same_strategy_across_locations(records)

    # ---------- Render Dashboard ----------
    return render_template(
        "dashboard.html",
        files=file_names,
        records=records,
        languages=languages,
        repeated_phones=repeated_phones,
        repeated_vehicles=repeated_vehicles,
        repeated_ips=repeated_ips,
        charts=charts,
        strategy_alerts=strategy_alerts
    )



# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

    # http://127.0.0.1:5000/upload-ui


    # Hello world