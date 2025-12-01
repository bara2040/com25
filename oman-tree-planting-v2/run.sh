#!/bin/bash

# سكريبت تشغيل المنصة الكاملة
# يقوم بتشغيل Backend (FastAPI) و Frontend (Streamlit) معاً

echo "🚀 بدء تشغيل منصة زراعة الأشجار الذكية - عُمان"
echo "=================================================="

# التحقق من تثبيت المتطلبات
echo "📦 التحقق من المتطلبات..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python غير مثبت! قم بتثبيت Python 3.8+ أولاً"
    exit 1
fi

# تثبيت المتطلبات إذا لم تكن مثبتة
echo "📥 تثبيت المتطلبات (إذا لزم الأمر)..."
pip install -q --no-input -r requirements.txt

# التأكد من وجود البيانات
if [ ! -f "data/oman_trees_database.json" ]; then
    echo "❌ قاعدة بيانات الأشجار غير موجودة!"
    exit 1
fi

# إنشاء مجلد النماذج
mkdir -p backend/models

# تدريب النموذج إذا لم يكن موجوداً
if [ ! -f "backend/models/rf_model.pkl" ]; then
    echo "🤖 تدريب نموذج ML للمرة الأولى..."
    cd backend/app
    python3 -c "from ml_model import predictor; predictor.train_initial_model(); predictor.save_model('../models/')"
    cd ../..
    echo "✅ اكتمل تدريب النموذج"
fi

echo ""
echo "🎯 تشغيل الخوادم..."
echo "=================================================="

# تشغيل Backend في الخلفية
echo "📡 تشغيل Backend API (FastAPI)..."
cd backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# انتظار بدء Backend
sleep 3

# التحقق من تشغيل Backend
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ فشل تشغيل Backend!"
    cat backend.log
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend يعمل على http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"

# تشغيل Frontend
echo ""
echo "🌐 تشغيل Frontend (Streamlit)..."
cd frontend
streamlit run streamlit_app.py --server.port 8501 &
FRONTEND_PID=$!
cd ..

# انتظار بدء Streamlit
sleep 5

echo ""
echo "=================================================="
echo "✅ المنصة تعمل بنجاح!"
echo "=================================================="
echo ""
echo "🌐 الروابط:"
echo "  • Frontend: http://localhost:8501"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo ""
echo "📝 السجلات:"
echo "  • Backend: backend.log"
echo "  • Frontend: في Terminal الحالي"
echo ""
echo "⏹️  لإيقاف المنصة، اضغط Ctrl+C"
echo ""

# انتظار حتى يتم إيقاف Streamlit
wait $FRONTEND_PID

# تنظيف عند الإيقاف
echo ""
echo "⏹️  إيقاف الخوادم..."
kill $BACKEND_PID 2>/dev/null
echo "✅ تم إيقاف المنصة بنجاح"
