from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os

with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    dados = request.json
    df = pd.DataFrame(dados)
    pred = modelo.predict(df)
    return jsonify({"predicao": pred.tolist()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
