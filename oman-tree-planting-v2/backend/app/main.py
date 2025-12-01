"""
FastAPI Backend - REST API للمنصة
يوفر endpoints للتنبؤ والـ chatbot والبيانات
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from backend.app.ml_model import predictor
from backend.app.chatbot import chatbot

# تهيئة FastAPI
app = FastAPI(
    title="منصة زراعة الأشجار الذكية - عُمان",
    description="نظام ذكي لتحليل نجاح زراعة الأشجار في محافظات عمان",
    version="2.0.0"
)

# تفعيل CORS للواجهة الأمامية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PredictionRequest(BaseModel):
    governorate: str
    season: str
    tree_name: str
    rainfall: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pH: Optional[float] = None
    organic_matter: Optional[float] = None
    soil_type: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

# Health Check
@app.get("/")
async def root():
    return {
        "status": "active",
        "message": "منصة زراعة الأشجار الذكية - عُمان",
        "version": "2.0.0",
        "endpoints": {
            "predict": "/api/predict",
            "chat": "/api/chat",
            "trees": "/api/trees",
            "governorates": "/api/governorates",
            "seasonal_advice": "/api/seasonal-advice"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ml_model": "loaded", "chatbot": "active"}

# Prediction Endpoint
@app.post("/api/predict")
async def predict_success(request: PredictionRequest):
    """
    التنبؤ بنجاح زراعة شجرة معينة
    """
    try:
        # بناء المعايير المخصصة
        custom_params = {}
        if request.rainfall is not None:
            custom_params['rainfall'] = request.rainfall
        if request.temperature is not None:
            custom_params['temperature_avg'] = request.temperature
        if request.humidity is not None:
            custom_params['humidity'] = request.humidity
        if request.pH is not None:
            custom_params['pH'] = request.pH
        if request.organic_matter is not None:
            custom_params['organic_matter'] = request.organic_matter
        if request.soil_type is not None:
            custom_params['soil_type'] = request.soil_type
        
        # الحصول على التنبؤ
        result = predictor.predict_success(
            governorate=request.governorate,
            season=request.season,
            tree_name=request.tree_name,
            custom_params=custom_params if custom_params else None
        )
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Chatbot Endpoint
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    التفاعل مع Chatbot الذكي
    """
    try:
        response = chatbot.get_response(
            user_message=request.message,
            context=request.context
        )
        
        return {
            "success": True,
            "data": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get All Trees
@app.get("/api/trees")
async def get_all_trees():
    """
    الحصول على قائمة بجميع الأشجار
    """
    try:
        trees = predictor.get_all_trees()
        return {
            "success": True,
            "count": len(trees),
            "data": trees
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Specific Tree
@app.get("/api/trees/{tree_name}")
async def get_tree_info(tree_name: str):
    """
    الحصول على معلومات شجرة محددة
    """
    try:
        tree = predictor._get_tree_info(tree_name)
        if not tree:
            raise HTTPException(status_code=404, detail="الشجرة غير موجودة")
        
        return {
            "success": True,
            "data": tree
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Governorates
@app.get("/api/governorates")
async def get_all_governorates():
    """
    الحصول على قائمة بجميع المحافظات
    """
    try:
        governorates = predictor.get_all_governorates()
        return {
            "success": True,
            "count": len(governorates),
            "data": governorates
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Seasonal Advice
@app.get("/api/seasonal-advice/{governorate}/{season}")
async def get_seasonal_advice(governorate: str, season: str):
    """
    الحصول على نصائح موسمية لمحافظة معينة
    """
    try:
        advice = chatbot.get_seasonal_advice(governorate, season)
        return {
            "success": True,
            "data": {
                "governorate": governorate,
                "season": season,
                "advice": advice
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Tree Recommendations
@app.get("/api/recommendations/{governorate}/{season}")
async def get_recommendations(governorate: str, season: str, limit: int = 5):
    """
    الحصول على توصيات الأشجار لمحافظة وموسم
    """
    try:
        recommendations = chatbot.get_tree_recommendation(governorate, season)
        return {
            "success": True,
            "data": recommendations[:limit]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Climate Data
@app.get("/api/climate/{governorate}/{season}")
async def get_climate_data(governorate: str, season: str):
    """
    الحصول على البيانات المناخية
    """
    try:
        climate = predictor._get_season_data(governorate, season)
        if not climate:
            raise HTTPException(status_code=404, detail="بيانات غير متوفرة")
        
        return {
            "success": True,
            "data": climate
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch Prediction
@app.post("/api/predict/batch")
async def batch_predict(requests: List[PredictionRequest]):
    """
    تنبؤات متعددة دفعة واحدة
    """
    try:
        results = []
        for req in requests:
            custom_params = {}
            if req.rainfall is not None:
                custom_params['rainfall'] = req.rainfall
            if req.temperature is not None:
                custom_params['temperature_avg'] = req.temperature
            
            result = predictor.predict_success(
                governorate=req.governorate,
                season=req.season,
                tree_name=req.tree_name,
                custom_params=custom_params if custom_params else None
            )
            results.append(result)
        
        return {
            "success": True,
            "count": len(results),
            "data": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Statistics
@app.get("/api/statistics")
async def get_statistics():
    """
    إحصائيات المنصة
    """
    try:
        trees = predictor.get_all_trees()
        governorates = predictor.get_all_governorates()
        
        return {
            "success": True,
            "data": {
                "total_trees": len(trees),
                "total_governorates": len(governorates),
                "seasons": 4,
                "tree_types": {
                    "دائمة الخضرة": len([t for t in trees if "دائمة" in t.get('type', '')]),
                    "نفضية": len([t for t in trees if "نفضية" in t.get('type', '')]),
                    "نخيل": len([t for t in trees if "نخيل" in t.get('type', '')]),
                    "صحراوية": len([t for t in trees if "صحراوية" in t.get('type', '')])
                }
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 تشغيل Backend Server...")
    print("📡 API Docs: http://localhost:8000/docs")
    print("🔍 ReDoc: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
