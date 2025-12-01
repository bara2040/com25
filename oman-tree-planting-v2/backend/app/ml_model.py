"""
نموذج التعلم الآلي لتوقع نجاح زراعة الأشجار
يستخدم RandomForest و GradientBoosting مع بيانات عمانية حقيقية
"""

import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

class TreeSuccessPredictor:
    def __init__(self):
        self.rf_model = None
        self.gb_model = None
        self.scaler = StandardScaler()
        self.trees_db = self._load_trees_database()
        self.climate_db = self._load_climate_database()
        
    def _load_trees_database(self):
        """تحميل قاعدة بيانات الأشجار العمانية"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'oman_trees_database.json'
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_climate_database(self):
        """تحميل البيانات المناخية الموسمية للمحافظات"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'oman_seasonal_climate_data.json'
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def train_initial_model(self):
        """
        تدريب نموذج أولي بناءً على البيانات التاريخية
        يستخدم معايير متوافقة مع المناخ العماني
        """
        # بيانات تدريب أولية (سيتم توسيعها بالبيانات الحقيقية)
        X_train, y_train = self._generate_training_data()
        
        # تطبيع البيانات
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # تدريب Random Forest
        self.rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )
        self.rf_model.fit(X_train_scaled, y_train)
        
        # تدريب Gradient Boosting
        self.gb_model = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=7,
            random_state=42
        )
        self.gb_model.fit(X_train_scaled, y_train)
        
        return True
    
    def _generate_training_data(self):
        """
        توليد بيانات تدريب من قاعدة البيانات والمعايير العمانية
        """
        X = []
        y = []
        
        # تحويل أسماء الفصول من الإنجليزية إلى العربية
        season_mapping = {
            'spring': 'الربيع',
            'summer': 'الصيف',
            'autumn': 'الخريف',
            'winter': 'الشتاء'
        }
        
        # لكل محافظة وشجرة، نقوم بتوليد أمثلة تدريبية
        for gov_name_ar, gov_data in self.climate_db['governorates'].items():
            
            for season_en, season_ar in season_mapping.items():
                if season_ar not in gov_data:
                    continue
                    
                season_data_raw = gov_data[season_ar]
                
                # تحويل البيانات إلى الشكل المتوقع
                season_data = {
                    'rainfall': season_data_raw.get('rainfall_mm', 50),
                    'temperature_avg': season_data_raw.get('avg_temperature', 25),
                    'humidity': season_data_raw.get('humidity', 50),
                    'soil_type': season_data_raw.get('soil_type', 'رملية'),
                    'pH': season_data_raw.get('soil_ph', 7.5),
                    'organic_matter': season_data_raw.get('organic_matter', 2.0)
                }
                
                for tree in self.trees_db['trees']:
                    # حساب التوافق بناءً على المعايير
                    compatibility = self._calculate_compatibility(
                        tree, season_data
                    )
                    
                    # إنشاء مثال تدريبي
                    features = [
                        season_data['rainfall'],
                        season_data['temperature_avg'],
                        season_data['humidity'],
                        self._encode_soil_type(season_data['soil_type']),
                        season_data['pH'],
                        season_data['organic_matter'],
                        self._encode_season(season_en),
                        self._encode_tree_type(tree['type'])
                    ]
                    
                    X.append(features)
                    y.append(1 if compatibility >= 0.7 else 0)
        
        return np.array(X), np.array(y)
    
    def predict_success(self, governorate, season, tree_name, custom_params=None):
        """
        التنبؤ بنجاح زراعة شجرة معينة في محافظة وفصل محدد
        
        Args:
            governorate: اسم المحافظة
            season: الفصل (spring, summer, autumn, winter)
            tree_name: اسم الشجرة
            custom_params: معايير مخصصة (اختياري)
        
        Returns:
            dict: نسبة النجاح، التوصيات، ملاحظات الموسم
        """
        # الحصول على بيانات الموسم للمحافظة
        season_data = self._get_season_data(governorate, season)
        tree_info = self._get_tree_info(tree_name)
        
        if not season_data or not tree_info:
            return {
                'success_rate': 0,
                'recommendations': ['بيانات غير متوفرة'],
                'seasonal_notes': []
            }
        
        # استخدام المعايير المخصصة إذا وُجدت
        if custom_params:
            season_data.update(custom_params)
        
        # تحضير البيانات للتنبؤ
        features = np.array([[
            season_data['rainfall'],
            season_data['temperature_avg'],
            season_data['humidity'],
            self._encode_soil_type(season_data['soil_type']),
            season_data['pH'],
            season_data['organic_matter'],
            self._encode_season(season),
            self._encode_tree_type(tree_info['type'])
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        # التنبؤ باستخدام النماذج
        if self.rf_model and self.gb_model:
            rf_prob = self.rf_model.predict_proba(features_scaled)[0][1]
            gb_prob = self.gb_model.predict_proba(features_scaled)[0][1]
            success_rate = (rf_prob + gb_prob) / 2 * 100
        else:
            # حساب يدوي إذا لم يكن النموذج مدرباً
            success_rate = self._calculate_compatibility(tree_info, season_data) * 100
        
        # توليد التوصيات
        recommendations = self._generate_recommendations(
            tree_info, season_data, season, success_rate
        )
        
        # ملاحظات الموسم
        seasonal_notes = self._get_seasonal_notes(tree_name, season)
        
        return {
            'success_rate': round(success_rate, 1),
            'recommendations': recommendations,
            'seasonal_notes': seasonal_notes,
            'optimal_planting_time': self._get_optimal_planting_time(tree_name),
            'tree_info': tree_info,
            'climate_data': season_data
        }
    
    def _calculate_compatibility(self, tree, climate):
        """حساب التوافق بين الشجرة والمناخ"""
        score = 0.0
        weights = {
            'rainfall': 0.25,
            'temperature': 0.25,
            'humidity': 0.15,
            'pH': 0.15,
            'soil': 0.20
        }
        
        # معايير الأمطار
        rainfall = climate['rainfall']
        if tree['requirements']['rainfall_min'] <= rainfall <= tree['requirements']['rainfall_max']:
            score += weights['rainfall']
        elif abs(rainfall - tree['requirements']['rainfall_min']) < 50:
            score += weights['rainfall'] * 0.5
        
        # معايير درجة الحرارة
        temp = climate['temperature_avg']
        if tree['requirements']['temperature_min'] <= temp <= tree['requirements']['temperature_max']:
            score += weights['temperature']
        elif abs(temp - tree['requirements']['temperature_min']) < 10:
            score += weights['temperature'] * 0.6
        
        # معايير الرطوبة
        humidity = climate['humidity']
        if tree['requirements']['humidity_min'] <= humidity <= tree['requirements']['humidity_max']:
            score += weights['humidity']
        
        # معايير pH
        pH = climate['pH']
        if tree['requirements']['pH_min'] <= pH <= tree['requirements']['pH_max']:
            score += weights['pH']
        
        # نوع التربة
        if climate['soil_type'].lower() in [s.lower() for s in tree['requirements']['soil_types']]:
            score += weights['soil']
        
        return min(score, 1.0)
    
    def _get_season_data(self, governorate, season):
        """الحصول على بيانات الموسم للمحافظة"""
        season_mapping = {
            'spring': 'الربيع',
            'summer': 'الصيف',
            'autumn': 'الخريف',
            'winter': 'الشتاء'
        }
        
        season_ar = season_mapping.get(season, season)
        
        for gov_name_ar, gov_data in self.climate_db['governorates'].items():
            if gov_name_ar == governorate or gov_data.get('name_en', '').lower() == governorate.lower():
                if season_ar in gov_data:
                    raw_data = gov_data[season_ar]
                    return {
                        'rainfall': raw_data.get('rainfall_mm', 50),
                        'temperature_avg': raw_data.get('avg_temperature', 25),
                        'humidity': raw_data.get('humidity', 50),
                        'soil_type': raw_data.get('soil_type', 'رملية'),
                        'pH': raw_data.get('soil_ph', 7.5),
                        'organic_matter': raw_data.get('organic_matter', 2.0)
                    }
        return None
    
    def _get_tree_info(self, tree_name):
        """الحصول على معلومات الشجرة"""
        for tree in self.trees_db['trees']:
            if tree['name'] == tree_name or tree['name_en'].lower() == tree_name.lower():
                return tree
        return None
    
    def _encode_soil_type(self, soil_type):
        """ترميز نوع التربة"""
        soil_mapping = {
            'رملية': 1, 'sandy': 1,
            'طينية': 2, 'clay': 2,
            'صخرية': 3, 'rocky': 3,
            'جيرية': 4, 'calcareous': 4,
            'طميية': 5, 'loamy': 5
        }
        return soil_mapping.get(soil_type.lower(), 0)
    
    def _encode_season(self, season):
        """ترميز الفصل"""
        season_mapping = {'spring': 1, 'summer': 2, 'autumn': 3, 'winter': 4}
        return season_mapping.get(season, 0)
    
    def _encode_tree_type(self, tree_type):
        """ترميز نوع الشجرة"""
        type_mapping = {
            'شجرة دائمة الخضرة': 1,
            'شجرة نفضية': 2,
            'نخيل': 3,
            'شجرة صحراوية': 4,
            'شجرة جبلية': 5,
            'شجرة ساحلية': 6
        }
        return type_mapping.get(tree_type, 0)
    
    def _generate_recommendations(self, tree, climate, season, success_rate):
        """توليد التوصيات بناءً على التحليل"""
        recommendations = []
        
        if success_rate >= 80:
            recommendations.append(f"✅ موسم ممتاز لزراعة {tree['name']}")
        elif success_rate >= 60:
            recommendations.append(f"⚠️ موسم مقبول لزراعة {tree['name']} مع الرعاية الإضافية")
        else:
            recommendations.append(f"❌ يُنصح بتأجيل الزراعة إلى موسم أفضل")
        
        # توصيات بناءً على الأمطار
        if climate['rainfall'] < tree['requirements']['rainfall_min']:
            recommendations.append(f"💧 يُنصح بالري المنتظم (نقص أمطار: {tree['requirements']['rainfall_min'] - climate['rainfall']:.0f} مم)")
        
        # توصيات بناءً على درجة الحرارة
        if climate['temperature_avg'] > tree['requirements']['temperature_max']:
            recommendations.append("🌡️ استخدام شبكات التظليل في ساعات الذروة")
        
        # توصيات التسميد
        if climate['organic_matter'] < 2:
            recommendations.append("🌱 إضافة السماد العضوي (2-3 كجم لكل شجرة)")
        
        # توصيات pH
        if abs(climate['pH'] - 7) > 1:
            if climate['pH'] < 6:
                recommendations.append("⚗️ إضافة الجير لرفع حموضة التربة")
            elif climate['pH'] > 8:
                recommendations.append("⚗️ إضافة الكبريت لخفض قلوية التربة")
        
        return recommendations
    
    def _get_seasonal_notes(self, tree_name, season):
        """الحصول على ملاحظات الموسم للشجرة"""
        tree = self._get_tree_info(tree_name)
        if not tree:
            return []
        
        seasonal_tips = tree.get('seasonal_care', {})
        return seasonal_tips.get(season, [])
    
    def _get_optimal_planting_time(self, tree_name):
        """الحصول على أفضل وقت للزراعة"""
        tree = self._get_tree_info(tree_name)
        if not tree:
            return "غير محدد"
        return tree.get('optimal_planting_time', 'الخريف والشتاء')
    
    def get_all_trees(self):
        """الحصول على قائمة بجميع الأشجار"""
        return self.trees_db['trees']
    
    def get_all_governorates(self):
        """الحصول على قائمة بجميع المحافظات"""
        return list(self.climate_db['governorates'].keys())
    
    def save_model(self, path='models/'):
        """حفظ النموذج المدرب"""
        Path(path).mkdir(exist_ok=True)
        if self.rf_model:
            joblib.dump(self.rf_model, f'{path}rf_model.pkl')
        if self.gb_model:
            joblib.dump(self.gb_model, f'{path}gb_model.pkl')
        joblib.dump(self.scaler, f'{path}scaler.pkl')
        return True
    
    def load_model(self, path='models/'):
        """تحميل النموذج المحفوظ"""
        try:
            self.rf_model = joblib.load(f'{path}rf_model.pkl')
            self.gb_model = joblib.load(f'{path}gb_model.pkl')
            self.scaler = joblib.load(f'{path}scaler.pkl')
            return True
        except:
            return False

# تهيئة النموذج العام
predictor = TreeSuccessPredictor()

# محاولة تحميل نموذج محفوظ، وإلا تدريب نموذج جديد
if not predictor.load_model():
    print("⚙️ تدريب نموذج جديد...")
    predictor.train_initial_model()
    predictor.save_model()
    print("✅ اكتمل التدريب")
