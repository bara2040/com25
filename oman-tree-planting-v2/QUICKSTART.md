# 🚀 دليل التشغيل السريع - منصة زراعة الأشجار الذكية

## ⚡ التشغيل في 3 خطوات

### 1️⃣ فك الضغط وتثبيت المتطلبات

```bash
# فك ضغط الملف
tar -xzf oman-tree-planting-complete.tar.gz
cd oman-tree-planting-v2

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 2️⃣ تشغيل المنصة

**الطريقة السريعة (موصى بها):**
```bash
chmod +x run.sh
./run.sh
```

**أو تشغيل يدوي:**
```bash
# Terminal 1 - Backend
cd oman-tree-planting-v2
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd oman-tree-planting-v2
streamlit run frontend/streamlit_app.py --server.port 8501
```

### 3️⃣ افتح المنصة

- **الواجهة الرئيسية**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

---

## 📊 المميزات

✅ **15 نوع شجرة عمانية**  
✅ **11 محافظة (تغطية كاملة)**  
✅ **4 فصول مع بيانات دقيقة**  
✅ **Chatbot ذكي (120+ سؤال/جواب)**  
✅ **نموذج ML بدقة > 85%**  
✅ **بيانات رسمية 2023-2024**

---

## 🎯 استخدام سريع

### تحليل نجاح الزراعة

1. افتح http://localhost:8501
2. اختر "📊 تحليل الزراعة" من القائمة
3. اختر المحافظة (مثلاً: مسقط)
4. اختر الموسم (مثلاً: الخريف)
5. اختر الشجرة (مثلاً: اللبان)
6. اضغط "تحليل"

### استخدام Chatbot

1. اختر "💬 Chatbot الذكي" من القائمة
2. اكتب سؤالك (مثلاً: "متى أزرع النخيل؟")
3. احصل على إجابة فورية

### استخدام API مباشرة

```bash
# تنبؤ نجاح الزراعة
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "governorate": "مسقط",
    "season": "autumn",
    "tree_name": "اللبان"
  }'

# Chatbot
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ما هي أفضل الأشجار لعمان؟"
  }'

# قائمة الأشجار
curl "http://localhost:8000/api/trees"

# قائمة المحافظات
curl "http://localhost:8000/api/governorates"
```

---

## 🌍 النشر على خادم عام

### على خادم Linux

```bash
# 1. نقل الملف إلى الخادم
scp oman-tree-planting-complete.tar.gz user@your-server.com:~/

# 2. على الخادم
ssh user@your-server.com
tar -xzf oman-tree-planting-complete.tar.gz
cd oman-tree-planting-v2

# 3. تثبيت وتشغيل
pip3 install -r requirements.txt
./run.sh

# 4. افتح المنافذ
# 8000 للـ Backend API
# 8501 للـ Frontend
```

### باستخدام Gunicorn (Production)

```bash
# تثبيت Gunicorn
pip install gunicorn

# تشغيل Backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  backend.app.main:app --bind 0.0.0.0:8000

# تشغيل Frontend (في terminal آخر)
streamlit run frontend/streamlit_app.py \
  --server.address 0.0.0.0 --server.port 8501
```

---

## 🐛 حل المشاكل

### المشكلة: Backend لا يعمل
```bash
# تحقق من السجل
cat backend.log

# تحقق من المنفذ
lsof -i :8000

# إيقاف العملية إذا كانت معلقة
pkill -f uvicorn
```

### المشكلة: Frontend لا يعمل
```bash
# تحقق من Streamlit
streamlit --version

# إعادة تثبيت
pip install --upgrade streamlit
```

### المشكلة: خطأ في النموذج ML
```bash
# إعادة تدريب النموذج
cd backend/app
python3 -c "from ml_model import predictor; predictor.train_initial_model(); predictor.save_model('../models/')"
```

---

## 📞 الدعم

- **التوثيق الكامل**: راجع `README.md`
- **API Docs**: http://localhost:8000/docs
- **دليل النشر**: `docs/DEPLOYMENT.md`
- **دليل المستخدم**: `docs/USER_GUIDE.md`

---

## 🎉 نصائح للاستخدام الأمثل

1. **استخدم البيانات التلقائية أولاً**: البيانات المملوءة تلقائياً دقيقة ومن مصادر رسمية

2. **جرّب المحافظات المختلفة**: كل محافظة لها خصائص مناخية فريدة

3. **استكشف Chatbot**: يمكنه الإجابة على أكثر من 120 سؤال عن الزراعة

4. **استخدم API للتطبيقات الخارجية**: API RESTful كامل متاح على المنفذ 8000

5. **قارن بين الفصول**: جرّب نفس الشجرة في فصول مختلفة لرؤية الفرق

---

<div align="center">

**🌳 بالتوفيق في رحلة الزراعة!**

[![Made in Oman](https://img.shields.io/badge/Made%20in-Oman-green?style=for-the-badge)](https://oman.om)

</div>
