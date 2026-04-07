# Insurance Price Predictor

Predict medical insurance charges based on patient demographics and health indicators using machine learning. Built with scikit-learn, FastAPI, and Streamlit.

## Demo

https://www.youtube.com/watch?v=p2njig6bH18


## How It Works

The model predicts insurance costs using features like age, BMI, smoking status, and region. 
Key insight from EDA were: **smoking status** is the dominant predictor, followed by **age**, and then, **BMI, but specifically for smokers**.

### Feature Engineering

- `smoker_bmi` — BMI only drives up costs for smokers (visible in scatter plots)
- `smoker_age` — older smokers face exponentially higher charges
- `age_squared` — insurance costs accelerate with age, not linearly
- Log-transformed target to handle right-skewed charge distribution

### Model Comparison

| Model | CV R² | Test R² | MAE | RMSE |
|-------|-------|---------|-----|------|
| **GradientBoosting** | 0.8128 | **0.8664** | **0.1835** | **0.3466** |
| XGBRegressor | 0.8197 | 0.8565 | 0.2074 | 0.3592 |
| LinearRegression | 0.8150 | 0.8564 | 0.2022 | 0.3592 |
| RandomForest | 0.8069 | 0.8498 | 0.1969 | 0.3675 |

Overall, none of the scores were particularly strong as the dataset only contained 1,338 samples with 7 features. Still, GradientBoosting performed best and was selected as the final model. The primary goal of this project was to practice building an end-to-end ML pipeline with FastAPI, Streamlit, and Docker.

## Tech Stack

- **ML**: scikit-learn, XGBoost, pandas, NumPy
- **API**: FastAPI, Pydantic (with computed fields for feature engineering)
- **Frontend**: Streamlit
- **Serialization**: Pickle

## Project Structure

```
├── app.py              # FastAPI backend with prediction endpoint
├── frontend.py         # Streamlit frontend
├── insurance.csv       # Dataset
├── main.ipynb          # EDA, feature engineering, model training
├── model.pkl           # Trained GradientBoosting model
├── pyproject.toml      # Project config
├── requirements.txt    # Dependencies
└── README.md
```

## Setup

### 1. Clone the repo

```bash
git clone YOUR_GITHUB_REPO_URL
cd insurance-cost-predictor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app:app --reload
```

### 4. Run the Streamlit app (in a separate terminal)

```bash
streamlit run frontend.py
```

The app will open at `http://localhost:8501`. Enter patient details and click **Predict Cost**.

## API Usage

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "sex": "male",
    "weight": 85,
    "height": 1.75,
    "children": 2,
    "smoker": "yes",
    "region": "northwest"
  }'
```

Response:

```json
{
  "predicted_amount": 38169.79
}
```

## Dataset

[Kaggle — Medical Cost Personal Dataset](https://www.kaggle.com/datasets/mirichoi0218/insurance) (1,338 rows, 7 features)

---
