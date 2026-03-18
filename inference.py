from flask import Flask, request, jsonify
import pickle
import pandas as pd

with open("modelo.pkl", "rb") as f:
    model = pickle.load(f)
    
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    dados  = request.json
    df = pd.DataFrame(dados)
    pred = model.predict(df)
    return jsonify({"predicao": pred.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)