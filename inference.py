from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)
model = None

def get_model():
    global model
    if model is None:
        print("Carregando modelo...")
        with open("modelo.pkl", "rb") as f:
            model = pickle.load(f)
        print("Modelo carregado!")
    return model

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "mensagem": "API funcionando"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        dados = request.get_json()

        if dados is None:
            return jsonify({"erro": "Nenhum JSON enviado."}), 400

        if isinstance(dados, dict):
            df = pd.DataFrame([dados])
        elif isinstance(dados, list):
            df = pd.DataFrame(dados)
        else:
            return jsonify({"erro": "Envie um objeto JSON ou uma lista de objetos."}), 400

        modelo = get_model()
        pred = modelo.predict(df)

        return jsonify({"predicao": pred.tolist()})

    except Exception as e:
        return jsonify({
            "erro": "Erro ao processar previsão.",
            "detalhes": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
