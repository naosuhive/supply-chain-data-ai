from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Supply Chain Data AI API",
    description="AI-powered supply chain analytics and prediction API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    product_id: str
    quantity: Optional[int] = None
    location: Optional[str] = None

class PredictionResponse(BaseModel):
    product_id: str
    predicted_demand: float
    confidence: float
    recommendations: List[str]

@app.get("/")
async def root():
    return {
        "message": "Supply Chain Data AI API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict/demand", response_model=PredictionResponse)
async def predict_demand(request: PredictionRequest):
    try:
        predicted_demand = 100.0
        confidence = 0.85
        recommendations = [
            "Maintain current inventory levels",
            "Monitor seasonal trends"
        ]
        
        return PredictionResponse(
            product_id=request.product_id,
            predicted_demand=predicted_demand,
            confidence=confidence,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/inventory")
async def get_inventory_analytics():
    return {
        "total_products": 0,
        "low_stock_items": 0,
        "overstock_items": 0,
        "turnover_rate": 0.0
    }

@app.get("/analytics/supply-chain")
async def get_supply_chain_analytics():
    return {
        "average_lead_time": 0,
        "on_time_delivery_rate": 0.0,
        "supplier_performance": {}
    }

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True
    )
