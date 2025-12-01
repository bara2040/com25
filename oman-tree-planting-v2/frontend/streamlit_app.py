"""
Streamlit Frontend - واجهة المستخدم الرئيسية
واجهة تفاعلية كاملة مع دعم Chatbot وتحليل موسمي
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# تكوين الصفحة
st.set_page_config(
    page_title="منصة زراعة الأشجار الذكية - عُمان",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للتصميم العماني
st.markdown("""
<style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        background-color: #d32f2f;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .success-box {
        background-color: #4caf50;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    .warning-box {
        background-color: #ff9800;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    .error-box {
        background-color: #f44336;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# عنوان المنصة
st.title("🌳 منصة زراعة الأشجار الذكية - سلطنة عُمان")
st.markdown("### نظام ذكي لتحليل نجاح زراعة الأشجار مع دعم الفصول الأربعة 🌦️")

# API URL
API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/d/dd/Flag_of_Oman.svg", width=200)
    st.markdown("## القائمة الرئيسية")
    
    page = st.radio(
        "اختر الصفحة:",
        ["🏠 الصفحة الرئيسية", "📊 تحليل الزراعة", "💬 Chatbot الذكي", "🌲 قاعدة بيانات الأشجار", "📈 الإحصائيات"]
    )
    
    st.markdown("---")
    st.markdown("### معلومات المنصة")
    st.info("""
    **النسخة:** 2.0.0
    
    **المميزات:**
    - ✅ تحليل موسمي (4 فصول)
    - ✅ بيانات رسمية (2023-2024)
    - ✅ Chatbot ذكي (120+ سؤال)
    - ✅ 17 نوع شجرة عمانية
    - ✅ 11 محافظة
    - ✅ نموذج ML متقدم
    """)

# الحصول على البيانات من API
@st.cache_data
def get_trees():
    try:
        response = requests.get(f"{API_URL}/api/trees")
        if response.status_code == 200:
            return response.json()['data']
    except:
        return []
    return []

@st.cache_data
def get_governorates():
    try:
        response = requests.get(f"{API_URL}/api/governorates")
        if response.status_code == 200:
            return response.json()['data']
    except:
        return []
    return []

def get_prediction(governorate, season, tree_name, custom_params=None):
    try:
        payload = {
            "governorate": governorate,
            "season": season,
            "tree_name": tree_name
        }
        if custom_params:
            payload.update(custom_params)
        
        response = requests.post(f"{API_URL}/api/predict", json=payload)
        if response.status_code == 200:
            return response.json()['data']
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
    return None

def get_chat_response(message, context=None):
    try:
        payload = {"message": message, "context": context}
        response = requests.post(f"{API_URL}/api/chat", json=payload)
        if response.status_code == 200:
            return response.json()['data']
    except Exception as e:
        st.error(f"خطأ في Chatbot: {e}")
    return None

# الصفحة الرئيسية
if page == "🏠 الصفحة الرئيسية":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌲 عدد الأشجار", "17 نوع", "+3 جديد")
    with col2:
        st.metric("🏛️ المحافظات", "11 محافظة", "100% تغطية")
    with col3:
        st.metric("🌦️ البيانات", "2023-2024", "رسمية")
    
    st.markdown("---")
    
    st.markdown("## 🎯 مرحباً بك في المنصة!")
    st.info("""
    هذه المنصة تستخدم الذكاء الاصطناعي لمساعدتك في:
    
    1. **تحليل نجاح الزراعة**: اكتشف أفضل الأشجار لمحافظتك وموسمك
    2. **نظام الفصول الأربعة**: بيانات دقيقة لكل موسم (ربيع، صيف، خريف، شتاء)
    3. **Chatbot ذكي**: اسأل أي سؤال عن الزراعة والأشجار
    4. **توصيات مخصصة**: نصائح عملية بناءً على بياناتك
    5. **بيانات رسمية**: من هيئة الطيران المدني والبنك الدولي
    """)
    
    st.markdown("### 🌟 ابدأ الآن")
    st.success("اختر **📊 تحليل الزراعة** من القائمة الجانبية لبدء التحليل")
    
    # عرض أمثلة
    st.markdown("### 📸 أمثلة من المنصة")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### تحليل موسمي دقيق")
        st.info("""
        - اختر المحافظة (مسقط، ظفار، الباطنة...)
        - اختر الموسم (ربيع، صيف، خريف، شتاء)
        - البيانات تُملأ تلقائياً من قاعدة 2023-2024
        - احصل على نسبة نجاح دقيقة
        """)
    
    with col2:
        st.markdown("#### Chatbot ذكي")
        st.info("""
        - أكثر من 120 سؤال وجواب
        - نصائح موسمية مخصصة
        - معلومات عن الأشجار العمانية
        - إجابات فورية 24/7
        """)

# صفحة التحليل
elif page == "📊 تحليل الزراعة":
    st.markdown("## 📊 تحليل نجاح الزراعة - نظام موسمي متقدم")
    
    # تحميل البيانات
    trees = get_trees()
    governorates = get_governorates()
    
    if not trees or not governorates:
        st.error("⚠️ تأكد من تشغيل Backend Server أولاً!")
        st.code("cd backend && python -m uvicorn app.main:app --reload", language="bash")
        st.stop()
    
    # نموذج الإدخال
    col1, col2 = st.columns(2)
    
    with col1:
        selected_gov = st.selectbox(
            "🏛️ اختر المحافظة:",
            governorates,
            help="اختر المحافظة التي تريد الزراعة فيها"
        )
        
        selected_tree = st.selectbox(
            "🌳 اختر الشجرة:",
            [t['name'] for t in trees],
            help="اختر نوع الشجرة المراد زراعتها"
        )
    
    with col2:
        season_map = {
            "🌸 الربيع (مارس - مايو)": "spring",
            "☀️ الصيف (يونيو - أغسطس)": "summer",
            "🍂 الخريف (سبتمبر - نوفمبر)": "autumn",
            "❄️ الشتاء (ديسمبر - فبراير)": "winter"
        }
        
        selected_season_ar = st.selectbox(
            "🌦️ اختر الموسم:",
            list(season_map.keys()),
            help="اختر الموسم المراد الزراعة فيه"
        )
        selected_season = season_map[selected_season_ar]
        
        use_custom = st.checkbox(
            "⚙️ استخدام معايير مخصصة",
            help="تجاوز البيانات التلقائية وإدخال قيم مخصصة"
        )
    
    st.markdown("---")
    
    # المعايير المخصصة
    custom_params = None
    if use_custom:
        st.markdown("### ⚙️ المعايير المخصصة")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rainfall = st.number_input("💧 الأمطار (مم)", min_value=0.0, max_value=500.0, value=100.0)
            temperature = st.number_input("🌡️ درجة الحرارة (°م)", min_value=0.0, max_value=50.0, value=25.0)
        
        with col2:
            humidity = st.number_input("💨 الرطوبة (%)", min_value=0.0, max_value=100.0, value=50.0)
            pH = st.number_input("⚗️ pH التربة", min_value=4.0, max_value=9.0, value=7.0)
        
        with col3:
            organic_matter = st.number_input("🌱 المادة العضوية (%)", min_value=0.0, max_value=10.0, value=2.0)
            soil_type = st.selectbox("🪨 نوع التربة", ["رملية", "طينية", "صخرية", "جيرية", "طميية"])
        
        custom_params = {
            "rainfall": rainfall,
            "temperature": temperature,
            "humidity": humidity,
            "pH": pH,
            "organic_matter": organic_matter,
            "soil_type": soil_type
        }
    
    # زر التحليل
    if st.button("🔍 تحليل نجاح الزراعة", type="primary", use_container_width=True):
        with st.spinner("جاري التحليل..."):
            result = get_prediction(selected_gov, selected_season, selected_tree, custom_params)
            
            if result:
                # عرض نسبة النجاح
                success_rate = result['success_rate']
                
                if success_rate >= 80:
                    st.markdown(f'<div class="success-box">✅ نسبة النجاح: {success_rate}% - ممتاز!</div>', unsafe_allow_html=True)
                elif success_rate >= 60:
                    st.markdown(f'<div class="warning-box">⚠️ نسبة النجاح: {success_rate}% - مقبول</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-box">❌ نسبة النجاح: {success_rate}% - غير مناسب</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # التوصيات
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📋 التوصيات")
                    for rec in result['recommendations']:
                        st.markdown(f"- {rec}")
                    
                    st.markdown("### ⏰ أفضل وقت للزراعة")
                    st.info(result['optimal_planting_time'])
                
                with col2:
                    st.markdown("### 📝 ملاحظات الموسم")
                    if result['seasonal_notes']:
                        for note in result['seasonal_notes']:
                            st.markdown(f"- {note}")
                    else:
                        st.warning("لا توجد ملاحظات موسمية خاصة")
                
                # البيانات المناخية
                st.markdown("---")
                st.markdown("### 🌦️ البيانات المناخية للموسم")
                
                climate = result['climate_data']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💧 الأمطار", f"{climate['rainfall']} مم")
                with col2:
                    st.metric("🌡️ الحرارة", f"{climate['temperature_avg']}°م")
                with col3:
                    st.metric("💨 الرطوبة", f"{climate['humidity']}%")
                with col4:
                    st.metric("⚗️ pH", climate['pH'])
                
                # رسم بياني للمقارنة
                st.markdown("---")
                st.markdown("### 📊 تحليل بصري")
                
                fig = go.Figure()
                
                fig.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=success_rate,
                    title={'text': "نسبة النجاح"},
                    delta={'reference': 70},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkgreen"},
                        'steps': [
                            {'range': [0, 60], 'color': "lightgray"},
                            {'range': [60, 80], 'color': "lightyellow"},
                            {'range': [80, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)

# صفحة Chatbot
elif page == "💬 Chatbot الذكي":
    st.markdown("## 💬 Chatbot الذكي - مساعدك الزراعي الشخصي")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 أنت: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">🤖 المساعد: {message["content"]}</div>', unsafe_allow_html=True)
    
    # أمثلة سريعة
    st.markdown("### 💡 أمثلة سريعة:")
    examples_col1, examples_col2, examples_col3 = st.columns(3)
    
    with examples_col1:
        if st.button("ما هي أفضل الأشجار لعمان؟"):
            user_message = "ما هي أفضل الأشجار لعمان؟"
            st.session_state.messages.append({"role": "user", "content": user_message})
            response = get_chat_response(user_message)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
            st.rerun()
    
    with examples_col2:
        if st.button("متى أزرع النخيل؟"):
            user_message = "متى أزرع النخيل؟"
            st.session_state.messages.append({"role": "user", "content": user_message})
            response = get_chat_response(user_message)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
            st.rerun()
    
    with examples_col3:
        if st.button("نصائح الري في الصيف"):
            user_message = "كيف أروي الأشجار في الصيف؟"
            st.session_state.messages.append({"role": "user", "content": user_message})
            response = get_chat_response(user_message)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
            st.rerun()
    
    # Chat input
    user_input = st.chat_input("اكتب سؤالك هنا...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("جاري التفكير..."):
            response = get_chat_response(user_input)
            
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                st.rerun()

# صفحة قاعدة البيانات
elif page == "🌲 قاعدة بيانات الأشجار":
    st.markdown("## 🌲 قاعدة بيانات الأشجار العمانية")
    
    trees = get_trees()
    
    if trees:
        st.success(f"📊 إجمالي الأشجار: {len(trees)} نوع")
        
        # فلتر حسب النوع
        tree_types = list(set([t.get('type', 'غير محدد') for t in trees]))
        selected_type = st.selectbox("🔍 فلترة حسب النوع:", ["الكل"] + tree_types)
        
        # عرض الأشجار
        filtered_trees = trees if selected_type == "الكل" else [t for t in trees if t.get('type') == selected_type]
        
        for tree in filtered_trees:
            with st.expander(f"🌳 {tree['name']} ({tree['name_en']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**الوصف:** {tree['description']}")
                    st.markdown(f"**النوع:** {tree.get('type', 'غير محدد')}")
                    st.markdown(f"**الارتفاع:** {tree['height_range']}")
                
                with col2:
                    st.markdown("**المتطلبات:**")
                    reqs = tree['requirements']
                    st.markdown(f"- 💧 الأمطار: {reqs['rainfall_min']}-{reqs['rainfall_max']} مم")
                    st.markdown(f"- 🌡️ الحرارة: {reqs['temperature_min']}-{reqs['temperature_max']}°م")
                    st.markdown(f"- 💨 الرطوبة: {reqs['humidity_min']}-{reqs['humidity_max']}%")
                    st.markdown(f"- ⚗️ pH: {reqs['pH_min']}-{reqs['pH_max']}")

# صفحة الإحصائيات
elif page == "📈 الإحصائيات":
    st.markdown("## 📈 إحصائيات المنصة")
    
    try:
        response = requests.get(f"{API_URL}/api/statistics")
        if response.status_code == 200:
            stats = response.json()['data']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌲 إجمالي الأشجار", stats['total_trees'])
            with col2:
                st.metric("🏛️ المحافظات", stats['total_governorates'])
            with col3:
                st.metric("🌦️ الفصول", stats['seasons'])
            with col4:
                st.metric("📊 أنواع الأشجار", len(stats['tree_types']))
            
            # رسم بياني دائري
            st.markdown("---")
            st.markdown("### 🥧 توزيع أنواع الأشجار")
            
            fig = px.pie(
                values=list(stats['tree_types'].values()),
                names=list(stats['tree_types'].keys()),
                title="توزيع أنواع الأشجار في قاعدة البيانات"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"خطأ في جلب الإحصائيات: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌳 منصة زراعة الأشجار الذكية - سلطنة عُمان 2024</p>
    <p>تم تطويرها بـ ❤️ باستخدام Python, FastAPI, Streamlit, و ML</p>
</div>
""", unsafe_allow_html=True)
