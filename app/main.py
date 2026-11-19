from fastapi import FastAPI
from pydantic import BaseModel
from src.abrams_model import calculate_abrams_features

app = FastAPI(
    title="Structural Concrete Strength & Quality Microservice",
    version="1.0.0",
    description="Inference API for Concrete Quality Prediction and Anomaly Detection"
)

class ConcreteMixInput(BaseModel):
    cement_kg_m3: float
    water_kg_m3: float
    fly_ash_kg_m3: float = 0.0
    slag_kg_m3: float = 0.0
    age_days: int = 28

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "concrete-quality-ai"}

@app.post("/predict-strength")
def predict_strength(mix: ConcreteMixInput):
    physics_features = calculate_abrams_features(
        water_kg=mix.water_kg_m3,
        cement_kg=mix.cement_kg_m3,
        fly_ash_kg=mix.fly_ash_kg_m3,
        slag_kg=mix.slag_kg_m3
    )
    # Calibrated estimation blended with physical model
    predicted_fck_mpa = physics_features['abrams_index'] * (mix.age_days / (4 + 0.85 * mix.age_days))
    
    return {
        "predicted_compressive_strength_mpa": round(predicted_fck_mpa, 2),
        "physics_parameters": physics_features,
        "conformance_status": "CONFORME" if predicted_fck_mpa >= 30.0 else "SUB_DIMENSIONADO"
    }
