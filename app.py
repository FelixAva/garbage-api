# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from pathlib import Path

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Ajusta aquí la ruta absoluta al public de tu React app ---
# partiendo de donde está este archivo:
BASE_DIR = Path(__file__).resolve().parent
REACT_PUBLIC = (BASE_DIR / '..' / 'garbage-web' / 'public').resolve()
SAMPLES_DIR = REACT_PUBLIC / 'samples'

@app.route('/api/samples/<category>', methods=['GET'])
def get_samples(category):
    base = SAMPLES_DIR / category
    if not base.is_dir():
        return jsonify({"urls": []}), 200

    files = sorted(f for f in os.listdir(base) if f.lower().endswith(('.jpg','jpeg','png')))
    # construimos rutas relativas para que React las sirva desde /samples/...
    urls = [f'/samples/{category}/{fname}' for fname in files]
    return jsonify({"urls": urls}), 200

@app.route('/api/upload-samples', methods=['POST'])
def upload_samples():
    category = request.form.get('category')
    photos   = request.files.getlist('photos')

    if not category or not photos:
        return jsonify({"error": "Falta categoría o archivos"}), 400

    dest = SAMPLES_DIR / category
    os.makedirs(dest, exist_ok=True)

    # calcular siguiente índice
    existing = sorted(f for f in os.listdir(dest) if f.startswith(category))
    nums = []
    for f in existing:
        name, ext = os.path.splitext(f)
        idx = name.replace(category, '')
        if idx.isdigit(): nums.append(int(idx))
    next_idx = max(nums) + 1 if nums else 1

    saved = []
    for file in photos:
        filename = f"{category}{next_idx}.jpg"
        file.save(str(dest / filename))
        saved.append(f'/samples/{category}/{filename}')
        next_idx += 1

    return jsonify({"saved": len(saved), "urls": saved}), 200

if __name__ == "__main__":
    app.run(debug=True)
