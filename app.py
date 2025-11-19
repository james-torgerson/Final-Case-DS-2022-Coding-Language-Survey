from datetime import datetime, timezone
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pydantic import ValidationError
from models import SurveySubmission, StoredSurveyRecord
from storage import append_json_line
import hashlib

app = Flask(__name__, static_folder='frontend')

CORS(app, resources={r"/v1/*": {"origins": "*"}})

def hash_string(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

@app.route("/", methods=["GET"])
def index():
    """Serve the main HTML page."""
    return send_from_directory(app.static_folder, 'index.html') 

@app.route("/health", methods=["GET"])
def ping():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })

@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "detail": "Body must be application/json"}), 400
        
    try:
        submission = SurveySubmission(**payload)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": "Please complete all fields before submitting"}), 422
    
    email_normalized = submission.email.strip().lower()
    email_hash = hash_string(email_normalized)

    hour_stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    submission_id = submission.submission_id or hash_string(email_normalized + hour_stamp)

    record = StoredSurveyRecord(
        name=submission.name,
        submission_id=submission_id,
        email_hash=email_hash,
        role=submission.role,
        languages=submission.languages,
        proficiencies=submission.proficiencies,
        received_at=datetime.now(timezone.utc),
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or "")
    )
    append_json_line(record.dict())
    return jsonify({"status": "ok"}), 201
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)