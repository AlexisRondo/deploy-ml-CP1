# Deploy de Modelo de Machine Learning — Coluna Vertebral

API REST para classificação de problemas ortopédicos na coluna vertebral.

Disciplina: **Disruptive Architectures: IoT, IA & Generative AI** — FIAP ADS 2TDSPS  
Professor: André Tritiack

---

## Sobre o modelo

Dataset: Centre Médico-Chirurgical de Réadaptation des Massues (Lyon, França)  
310 registros com 6 atributos biomecânicos.

**Algoritmos treinados:**
- Random Forest — acurácia: **82.80%** ← modelo utilizado
- KNN — acurácia: 78.49%

**Classes de saída (coluna `diagnostic`):**
- `0` → Disk Hernia
- `1` → Normal
- `2` → Spondylolisthesis

---

## Estrutura do projeto
```
deploy_ml/
├── modelo.pkl                       # Modelo Random Forest serializado
├── inference.py                     # API Flask
├── requirements.txt                 # Dependências
├── Dockerfile                       # Container da aplicação
├── notebook_coluna_vertebral.ipynb  # Notebook de treinamento
├── questao_01.csv                   # Dataset
└── README.md
```

---

## Etapa 1 — Executar localmente
```bash
pip install -r requirements.txt
python inference.py
```

A API estará disponível em `http://localhost:8000`.

---

## Etapa 2 — Testar no Postman

**Método:** `POST`  
**URL:** `http://localhost:8000/predict`  
**Body:** raw → JSON
```json
[
  {
    "V1": 63.03,
    "V2": 22.55,
    "V3": 39.61,
    "V4": 40.48,
    "V5": 98.67,
    "V6": -0.25
  }
]
```

**Resposta esperada:**
```json
{
  "predicao": [0]
}
```

Também é possível verificar o status da API via `GET`:

**Método:** `GET`  
**URL:** `http://localhost:8000/`  

---

## Etapa 3 — Build e execução com Docker
```bash
# Construir a imagem
docker build -t modelo .

# Executar o container
docker run -p 8000:8000 modelo
```

Testar novamente no Postman com a mesma requisição acima.

---

## Etapa 4 — Deploy na nuvem (Azure App Service)

### Pré-requisitos
- [Azure CLI](https://docs.microsoft.com/pt-br/cli/azure/install-azure-cli) instalado
- Conta Azure ativa

### Comandos
```bash
# Login
az login

# Criar resource group (Brazil South — região disponível para Azure for Students FIAP)
az group create --name rg-spine-api --location brazilsouth

# Criar App Service Plan (free tier)
az appservice plan create --name plan-spine-api --resource-group rg-spine-api --sku F1 --is-linux

# Criar Web App com Python 3.11
az webapp create --resource-group rg-spine-api --plan plan-spine-api --name spine-disorder-api --runtime "PYTHON:3.11"

# Configurar startup
az webapp config set --resource-group rg-spine-api --name spine-disorder-api --startup-file "gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 1 inference:app"

# Habilitar instalação automática de dependências durante o deploy
az webapp config appsettings set --resource-group rg-spine-api --name spine-disorder-api --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true WEBSITES_PORT=8000

# Empacotar (Windows PowerShell)
Compress-Archive -Path inference.py,modelo.pkl,requirements.txt -DestinationPath deploy.zip -Force

# Fazer deploy
az webapp deploy --resource-group rg-spine-api --name spine-disorder-api --src-path deploy.zip --type zip --clean true
```

### Testar após o deploy
```bash
curl -X POST https://spine-disorder-api.azurewebsites.net/predict \
  -H "Content-Type: application/json" \
  -d '[{"V1": 63.03, "V2": 22.55, "V3": 39.61, "V4": 40.48, "V5": 98.67, "V6": -0.25}]'
```

**Resposta esperada:**
```json
{
  "predicao": [0]
}
```

---

## Fluxo completo
```
Treinar modelo (notebook)
      ↓
Salvar modelo (.pkl)
      ↓
Criar API Flask (inference.py)
      ↓
Testar localmente (Postman)
      ↓
Criar imagem Docker
      ↓
Executar container
      ↓
Deploy na nuvem (Azure)
      ↓
Consumir API via HTTP
```

---

## Referências

- Flask Documentation: https://flask.palletsprojects.com/
- Scikit-learn — Model Persistence: https://scikit-learn.org/stable/model_persistence.html
- Docker Documentation: https://docs.docker.com/
- Postman Learning Center: https://learning.postman.com/
