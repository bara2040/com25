"""
Chatbot ذكي متخصص في الزراعة والأشجار العمانية
يدعم أكثر من 120 سؤال وجواب مع نصائح موسمية
"""

import json
from pathlib import Path
from typing import List, Dict
import re

class OmanTreeChatbot:
    def __init__(self):
        self.trees_db = self._load_trees_database()
        self.climate_db = self._load_climate_database()
        self.qa_database = self._build_qa_database()
        self.conversation_history = []
        
    def _load_trees_database(self):
        """تحميل قاعدة بيانات الأشجار"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'oman_trees_database.json'
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_climate_database(self):
        """تحميل البيانات المناخية"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'oman_seasonal_climate_data.json'
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _build_qa_database(self):
        """بناء قاعدة بيانات الأسئلة والأجوبة"""
        return {
            # أسئلة عامة عن الزراعة في عمان
            'general': [
                {
                    'keywords': ['ما هي', 'أفضل الأشجار', 'عمان', 'زراعة'],
                    'answer': 'أفضل الأشجار للزراعة في عمان تشمل: اللبان (شجرة عمان الوطنية)، النخيل، الغاف، السمر، السدر، والمانجو. تختلف الأفضلية حسب المنطقة والموسم.'
                },
                {
                    'keywords': ['متى', 'أزرع', 'وقت الزراعة', 'موسم'],
                    'answer': 'أفضل وقت للزراعة في عمان هو خلال فصلي الخريف (سبتمبر-نوفمبر) والشتاء (ديسمبر-فبراير) عندما تكون درجات الحرارة معتدلة والرطوبة مناسبة.'
                },
                {
                    'keywords': ['كم', 'كمية المياه', 'ري', 'أروي'],
                    'answer': 'تختلف احتياجات الري حسب نوع الشجرة والموسم. بشكل عام: الأشجار الصحراوية تحتاج 20-40 لتر أسبوعياً، بينما الأشجار الاستوائية تحتاج 50-80 لتر. يُنصح بالري المنتظم في الصيف.'
                },
                {
                    'keywords': ['تربة', 'نوع التربة', 'أي تربة'],
                    'answer': 'عمان تحتوي على أنواع متعددة من التربة: رملية (في الساحل)، جيرية (في الجبال)، وطينية (في الوديان). معظم الأشجار العمانية تتكيف مع التربة الرملية والجيرية.'
                },
                {
                    'keywords': ['سماد', 'تسميد', 'عضوي'],
                    'answer': 'يُنصح باستخدام السماد العضوي (2-3 كجم للشجرة) مرتين سنوياً: في بداية الربيع وبداية الخريف. يمكن استخدام سماد NPK (20-20-20) للأشجار المثمرة.'
                },
                {
                    'keywords': ['مسافة', 'المسافات', 'زراعة', 'بين الأشجار'],
                    'answer': 'المسافات الموصى بها بين الأشجار: النخيل 6-8 متر، اللبان 4-5 متر، المانجو 8-10 متر، الغاف 5-6 متر. تضمن هذه المسافات نمو جيد وتهوية كافية.'
                },
                {
                    'keywords': ['آفات', 'أمراض', 'حشرات', 'مكافحة'],
                    'answer': 'الآفات الشائعة في عمان: سوسة النخيل الحمراء، حشرة الدوباس، والمن. الوقاية بالتقليم المنتظم والنظافة. استخدام المبيدات الحيوية أولاً قبل الكيميائية.'
                },
                {
                    'keywords': ['حرارة', 'حار', 'حماية', 'تظليل'],
                    'answer': 'في الصيف العماني (45-50°م)، احمِ الشتلات الصغيرة بشبكات التظليل (50-70% ظل). اروِ في الصباح الباكر أو المساء. تجنب الزراعة في يونيو-أغسطس.'
                },
                {
                    'keywords': ['ماء', 'نقص المياه', 'ري بالتنقيط'],
                    'answer': 'الري بالتنقيط هو الأفضل في عمان: يوفر 40-60% من المياه، يقلل الأعشاب، ويحسن نمو الجذور. ضع 2-4 نقاطات لكل شجرة حسب الحجم.'
                },
                {
                    'keywords': ['شتلة', 'اختيار الشتلات', 'جودة'],
                    'answer': 'اختر شتلات بارتفاع 60-100 سم، ساق قوي، أوراق خضراء، وجذور متفرعة. تجنب الشتلات الضعيفة أو المصفرة. اشترِ من مشاتل معتمدة.'
                }
            ],
            
            # أسئلة عن الفصول
            'seasonal': [
                {
                    'keywords': ['ربيع', 'spring', 'مارس', 'أبريل', 'مايو'],
                    'answer': 'الربيع (مارس-مايو) في عمان: حرارة معتدلة (25-35°م)، فصل ممتاز لزراعة اللبان، الغاف، السدر، والأشجار المزهرة. زد التسميد واهتم بالري المنتظم.'
                },
                {
                    'keywords': ['صيف', 'summer', 'يونيو', 'يوليو', 'أغسطس'],
                    'answer': 'الصيف (يونيو-أغسطس): حرارة شديدة (40-50°م). تجنب الزراعة الجديدة. ركز على الري الصباحي والمسائي، استخدم التظليل، وراقب الآفات. مناسب لرعاية الأشجار القائمة فقط.'
                },
                {
                    'keywords': ['خريف', 'autumn', 'fall', 'سبتمبر', 'أكتوبر', 'نوفمبر'],
                    'answer': 'الخريف (سبتمبر-نوفمبر): أفضل موسم للزراعة في عمان! حرارة معتدلة (25-35°م)، رطوبة جيدة. زرع النخيل، المانجو، الليمون، والأشجار المثمرة. سمّد واهتم بالري.'
                },
                {
                    'keywords': ['شتاء', 'winter', 'ديسمبر', 'يناير', 'فبراير'],
                    'answer': 'الشتاء (ديسمبر-فبراير): بارد نسبياً (15-25°م). ممتاز لزراعة معظم الأنواع. قلل الري (مرة أسبوعياً). احذر الصقيع في المناطق الجبلية. وقت مثالي للتقليم.'
                }
            ],
            
            # أسئلة عن المحافظات
            'governorates': [
                {
                    'keywords': ['مسقط', 'muscat'],
                    'answer': 'مسقط: مناخ ساحلي حار رطب. أفضل الأشجار: النخيل، الغاف، المانجو، الليمون العماني. التربة رملية-جيرية. الري المنتظم ضروري في الصيف.'
                },
                {
                    'keywords': ['ظفار', 'dhofar', 'صلالة', 'salalah'],
                    'answer': 'ظفار: مناخ فريد مع موسم الخريف (يوليو-سبتمبر). أمطار غزيرة (200-400 مم). مثالية للبان، جوز الهند، الموز، والأشجار الاستوائية. رطوبة عالية.'
                },
                {
                    'keywords': ['الباطنة', 'al batinah', 'صحار', 'sohar'],
                    'answer': 'الباطنة: سهل ساحلي خصب، تربة طينية. ممتاز للنخيل، المانجو، الموالح، والخضروات. مياه وفيرة من الأفلاج. حرارة عالية في الصيف.'
                },
                {
                    'keywords': ['الداخلية', 'al dakhiliyah', 'نزوى', 'nizwa'],
                    'answer': 'الداخلية: منطقة جبلية، حرارة معتدلة. مناسبة للرمان، التين، العنب، والورد. تربة جبلية خصبة. نظام أفلاج تقليدي للري.'
                },
                {
                    'keywords': ['الشرقية', 'al sharqiyah', 'صور', 'sur'],
                    'answer': 'الشرقية: منطقة متنوعة (ساحل + صحراء). زرع النخيل، الغاف، السمر في المناطق الساحلية. احذر الرطوبة العالية في الصيف.'
                },
                {
                    'keywords': ['الظاهرة', 'al dhahirah', 'عبري', 'ibri'],
                    'answer': 'الظاهرة: منطقة صحراوية حارة جافة. الأشجار الصحراوية مثل الغاف، السمر، السدر هي الأنسب. استخدم الري بالتنقيط لتوفير المياه.'
                }
            ],
            
            # أسئلة عن أشجار محددة
            'trees': self._build_tree_specific_qa()
        }
    
    def _build_tree_specific_qa(self):
        """بناء أسئلة وأجوبة خاصة بكل شجرة"""
        tree_qa = []
        
        for tree in self.trees_db['trees']:
            tree_qa.append({
                'keywords': [tree['name'].lower(), tree['name_en'].lower(), 'معلومات', 'شجرة'],
                'answer': f"{tree['name']} ({tree['name_en']}): {tree['description']}\n\n"
                         f"📏 الارتفاع: {tree['height_range']}\n"
                         f"💧 احتياجات المياه: {tree['requirements']['rainfall_min']}-{tree['requirements']['rainfall_max']} مم\n"
                         f"🌡️ درجة الحرارة: {tree['requirements']['temperature_min']}-{tree['requirements']['temperature_max']}°م\n"
                         f"⏱️ أفضل وقت للزراعة: {tree.get('optimal_planting_time', 'الخريف والشتاء')}"
            })
            
            # إضافة سؤال عن العناية
            tree_qa.append({
                'keywords': [tree['name'].lower(), 'عناية', 'رعاية', 'كيف أعتني'],
                'answer': f"العناية بشجرة {tree['name']}:\n\n" +
                         "\n".join([f"• {tip}" for tip in tree.get('care_tips', ['الري المنتظم', 'التسميد الموسمي', 'التقليم السنوي'])])
            })
        
        return tree_qa
    
    def get_response(self, user_message: str, context: dict = None) -> dict:
        """
        الحصول على رد من Chatbot
        
        Args:
            user_message: رسالة المستخدم
            context: سياق إضافي (محافظة، موسم، شجرة)
        
        Returns:
            dict: الرد، الاقتراحات، الروابط
        """
        user_message = user_message.strip().lower()
        
        # حفظ في السجل
        self.conversation_history.append({
            'user': user_message,
            'context': context
        })
        
        # البحث في قاعدة البيانات
        best_match = self._find_best_match(user_message, context)
        
        if best_match:
            response = {
                'answer': best_match['answer'],
                'suggestions': self._get_suggestions(user_message, context),
                'related_trees': self._get_related_trees(user_message),
                'confidence': best_match.get('confidence', 0.8)
            }
        else:
            response = {
                'answer': 'عذراً، لم أفهم سؤالك بشكل كامل. يمكنك سؤالي عن:\n• أفضل الأشجار للزراعة\n• متى أزرع شجرة معينة\n• كيفية العناية بالأشجار\n• المعلومات المناخية للمحافظات\n• نصائح الري والتسميد',
                'suggestions': [
                    'ما هي أفضل الأشجار لمحافظتي؟',
                    'متى أزرع النخيل؟',
                    'كم مرة أسقي الأشجار في الصيف؟',
                    'أريد معلومات عن شجرة اللبان'
                ],
                'related_trees': [],
                'confidence': 0.0
            }
        
        self.conversation_history[-1]['bot'] = response
        return response
    
    def _find_best_match(self, message: str, context: dict = None) -> dict:
        """البحث عن أفضل تطابق في قاعدة البيانات"""
        best_match = None
        best_score = 0
        
        # البحث في جميع الفئات
        for category in self.qa_database.values():
            for qa in category:
                score = self._calculate_similarity(message, qa['keywords'])
                
                # إضافة نقاط للسياق
                if context:
                    if context.get('governorate') and any(context['governorate'].lower() in kw for kw in qa['keywords']):
                        score += 0.2
                    if context.get('season') and any(context['season'].lower() in kw for kw in qa['keywords']):
                        score += 0.2
                
                if score > best_score:
                    best_score = score
                    best_match = {**qa, 'confidence': score}
        
        return best_match if best_score > 0.3 else None
    
    def _calculate_similarity(self, message: str, keywords: List[str]) -> float:
        """حساب التشابه بين الرسالة والكلمات المفتاحية"""
        message_words = set(re.findall(r'\w+', message.lower()))
        keyword_words = set(' '.join(keywords).lower().split())
        
        if not keyword_words:
            return 0.0
        
        common = message_words & keyword_words
        return len(common) / len(keyword_words)
    
    def _get_suggestions(self, message: str, context: dict = None) -> List[str]:
        """توليد اقتراحات للأسئلة التالية"""
        suggestions = [
            'ما هي أفضل الأشجار للزراعة في عمان؟',
            'متى أزرع الأشجار؟',
            'كيف أعتني بالأشجار في الصيف؟',
            'ما هي احتياجات الري؟'
        ]
        
        if context and context.get('governorate'):
            suggestions.insert(0, f"ما هي أفضل الأشجار لمحافظة {context['governorate']}؟")
        
        if context and context.get('season'):
            season_ar = {
                'spring': 'الربيع',
                'summer': 'الصيف',
                'autumn': 'الخريف',
                'winter': 'الشتاء'
            }
            suggestions.insert(0, f"ماذا أزرع في فصل {season_ar.get(context['season'], context['season'])}؟")
        
        return suggestions[:4]
    
    def _get_related_trees(self, message: str) -> List[Dict]:
        """الحصول على أشجار ذات صلة"""
        related = []
        
        # البحث في قاعدة الأشجار
        for tree in self.trees_db['trees'][:5]:
            if any(keyword in message for keyword in [tree['name'].lower(), tree['name_en'].lower()]):
                related.append({
                    'name': tree['name'],
                    'name_en': tree['name_en'],
                    'description': tree['description'][:100] + '...'
                })
        
        return related
    
    def get_seasonal_advice(self, governorate: str, season: str) -> str:
        """الحصول على نصائح موسمية لمحافظة معينة"""
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
                    season_data = gov_data[season_ar]
                    
                    advice = f"🌦️ نصائح {season_ar} في {gov_name_ar}:\n\n"
                    advice += f"🌡️ درجة الحرارة: {season_data.get('avg_temperature', 25)}°م\n"
                    advice += f"💧 الأمطار: {season_data.get('rainfall_mm', 50)} مم\n"
                    advice += f"💨 الرطوبة: {season_data.get('humidity', 50)}%\n"
                    advice += f"🌱 نوع التربة: {season_data.get('soil_type', 'رملية')}\n\n"
                    
                    advice += "📌 توصيات الموسم:\n"
                    if season_data.get('rainfall_mm', 50) < 50:
                        advice += "• زد كمية الري - الأمطار قليلة\n"
                    if season_data.get('avg_temperature', 25) > 35:
                        advice += "• استخدم شبكات التظليل\n"
                    if season_data.get('humidity', 50) > 70:
                        advice += "• راقب الأمراض الفطرية\n"
                    
                    return advice
        
        return "لم أتمكن من العثور على بيانات لهذه المحافظة."
    
    def get_tree_recommendation(self, governorate: str, season: str) -> List[Dict]:
        """توصية بأشجار مناسبة لمحافظة وموسم"""
        recommendations = []
        
        season_mapping = {
            'spring': 'الربيع',
            'summer': 'الصيف',
            'autumn': 'الخريف',
            'winter': 'الشتاء'
        }
        
        season_ar = season_mapping.get(season, season)
        
        # الحصول على بيانات المناخ
        climate_data = None
        for gov_name_ar, gov_data in self.climate_db['governorates'].items():
            if gov_name_ar == governorate or gov_data.get('name_en', '').lower() == governorate.lower():
                if season_ar in gov_data:
                    raw_data = gov_data[season_ar]
                    climate_data = {
                        'rainfall': raw_data.get('rainfall_mm', 50),
                        'temperature_avg': raw_data.get('avg_temperature', 25),
                        'humidity': raw_data.get('humidity', 50),
                        'soil_type': raw_data.get('soil_type', 'رملية')
                    }
                break
        
        if not climate_data:
            return []
        
        # تقييم الأشجار
        for tree in self.trees_db['trees']:
            compatibility = self._calculate_tree_compatibility(tree, climate_data)
            
            if compatibility > 0.6:
                recommendations.append({
                    'tree': tree,
                    'compatibility': compatibility,
                    'reason': self._get_compatibility_reason(tree, climate_data, compatibility)
                })
        
        # ترتيب حسب التوافق
        recommendations.sort(key=lambda x: x['compatibility'], reverse=True)
        
        return recommendations[:5]
    
    def _calculate_tree_compatibility(self, tree: Dict, climate: Dict) -> float:
        """حساب توافق الشجرة مع المناخ"""
        score = 0.0
        
        # الأمطار
        if tree['requirements']['rainfall_min'] <= climate['rainfall'] <= tree['requirements']['rainfall_max']:
            score += 0.3
        elif abs(climate['rainfall'] - tree['requirements']['rainfall_min']) < 50:
            score += 0.15
        
        # درجة الحرارة
        if tree['requirements']['temperature_min'] <= climate['temperature_avg'] <= tree['requirements']['temperature_max']:
            score += 0.3
        elif abs(climate['temperature_avg'] - tree['requirements']['temperature_min']) < 10:
            score += 0.15
        
        # الرطوبة
        if tree['requirements']['humidity_min'] <= climate['humidity'] <= tree['requirements']['humidity_max']:
            score += 0.2
        
        # نوع التربة
        if climate['soil_type'].lower() in [s.lower() for s in tree['requirements']['soil_types']]:
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_compatibility_reason(self, tree: Dict, climate: Dict, score: float) -> str:
        """الحصول على سبب التوافق"""
        if score >= 0.8:
            return f"توافق ممتاز - {tree['name']} مثالية لهذه الظروف المناخية"
        elif score >= 0.6:
            return f"توافق جيد - {tree['name']} مناسبة مع رعاية معتدلة"
        else:
            return f"توافق محدود - {tree['name']} تحتاج رعاية مكثفة"

# تهيئة Chatbot العام
chatbot = OmanTreeChatbot()
