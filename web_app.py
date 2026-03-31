import streamlit as st
import database
import importlib
importlib.reload(database)
import dateparser
from datetime import datetime

st.set_page_config(page_title="Smart To-Do", page_icon="✨", layout="wide")

# Manage success animations
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# Add custom CSS to make it "premium"
st.markdown("""
<style>
div[data-testid="stMetricValue"] {
    font-size: 2.8rem;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

TRANSLATIONS = {
    "en": {
        "title": "✨ Smart To-Do Dashboard",
        "subtitle": "Your premium, intelligent task manager.",
        "add_task": "➕ New Task",
        "desc_label": "Task Description*",
        "desc_placeholder": "Schedule meeting for Friday...",
        "due_label": "Smart Date (Type naturally!)",
        "due_placeholder": "e.g. tomorrow at 5pm",
        "priority": "Priority Level",
        "add_btn": "Create Task",
        "success": "Task perfectly scheduled!",
        "error_date": "Could not understand date:",
        "tab_pending": "📋 Pending Actions",
        "tab_completed": "✅ Completed Mastery",
        "no_pending": "You're all caught up! Amazing job. 🏖️",
        "no_completed": "No tasks completed yet. Let's get to work! 💪",
        "language": "Language / भाषा",
        "search": "🔍 Filter your active tasks...",
        "metrics_total": "Total Active",
        "metrics_done": "Completed",
        "metrics_overdue": "Overdue"
    },
    "hi": {
        "title": "✨ स्मार्ट टू-डू डैशबोर्ड",
        "subtitle": "आपका प्रीमियम, बुद्धिमान कार्य प्रबंधक।",
        "add_task": "➕ नया कार्य",
        "desc_label": "कार्य का विवरण*",
        "desc_placeholder": "जैसे कि बैठक शेड्यूल करें...",
        "due_label": "स्मार्ट तिथि (कुछ भी टाइप करें!)",
        "due_placeholder": "जैसे कल शाम 5 बजे",
        "priority": "प्राथमिकता स्तर",
        "add_btn": "कार्य बनाएं",
        "success": "कार्य सफलतापूर्वक जोड़ा गया!",
        "error_date": "तारीख समझ नहीं सका:",
        "tab_pending": "📋 लंबित कार्य",
        "tab_completed": "✅ पूर्ण किए गए कार्य",
        "no_pending": "आपका कोई कार्य लंबित नहीं है! मज़े करें। 🏖️",
        "no_completed": "अभी तक कोई कार्य पूरा नहीं हुआ है। 💪",
        "language": "भाषा / Language",
        "search": "🔍 अपने कार्य खोजें...",
        "metrics_total": "कुल सक्रिय",
        "metrics_done": "पूरा किया",
        "metrics_overdue": "अतिदेय"
    },
    "fr": {
        "title": "✨ Tableau de Bord Smart To-Do",
        "subtitle": "Votre gestionnaire de tâches intelligent et premium.",
        "add_task": "➕ Nouvelle Tâche",
        "desc_label": "Description de la Tâche*",
        "desc_placeholder": "Planifier une réunion pour vendredi...",
        "due_label": "Date Intelligente (Saisie naturelle!)",
        "due_placeholder": "ex. demain à 17h",
        "priority": "Niveau de Priorité",
        "add_btn": "Créer une Tâche",
        "success": "Tâche parfaitement programmée!",
        "error_date": "Impossible de comprendre la date:",
        "tab_pending": "📋 Actions en Attente",
        "tab_completed": "✅ Maîtrise Terminée",
        "no_pending": "Vous êtes à jour! Excellent travail. 🏖️",
        "no_completed": "Aucune tâche terminée pour le moment. Au travail! 💪",
        "language": "Langue / Language",
        "search": "🔍 Filtrer vos tâches actives...",
        "metrics_total": "Total Actif",
        "metrics_done": "Terminé",
        "metrics_overdue": "En Retard"
    },
    "de": {
        "title": "✨ Smart To-Do Dashboard",
        "subtitle": "Ihr intelligenter Premium-Aufgabenmanager.",
        "add_task": "➕ Neue Aufgabe",
        "desc_label": "Aufgabenbeschreibung*",
        "desc_placeholder": "Meeting für Freitag planen...",
        "due_label": "Smart Datum (Natürlich tippen!)",
        "due_placeholder": "z.B. morgen um 17 Uhr",
        "priority": "Prioritätsstufe",
        "add_btn": "Aufgabe Erstellen",
        "success": "Aufgabe perfekt geplant!",
        "error_date": "Datum konnte nicht verstanden werden:",
        "tab_pending": "📋 Ausstehende Aktionen",
        "tab_completed": "✅ Abgeschlossene Meisterschaft",
        "no_pending": "Sie sind auf dem neuesten Stand! Tolle Arbeit. 🏖️",
        "no_completed": "Noch keine Aufgaben abgeschlossen. An die Arbeit! 💪",
        "language": "Sprache / Language",
        "search": "🔍 Filtern Sie Ihre aktiven Aufgaben...",
        "metrics_total": "Gesamt Aktiv",
        "metrics_done": "Abgeschlossen",
        "metrics_overdue": "Überfällig"
    },
    "bn": {
        "title": "✨ স্মার্ট টু-ডু ড্যাশবোর্ড",
        "subtitle": "আপনার প্রিমিয়াম টাস্ক ম্যানেজার।",
        "add_task": "➕ নতুন কাজ",
        "desc_label": "কাজের বিবরণ*",
        "desc_placeholder": "যেমন আগামীকাল বাজার...",
        "due_label": "স্মার্ট তারিখ",
        "due_placeholder": "আগামীকাল বিকাল ৫টায়",
        "priority": "অগ্রাধিকার",
        "add_btn": "কাজ যোগ করুন",
        "success": "কাজ সফলভাবে যোগ করা হয়েছে!",
        "error_date": "তারিখ বুঝতে পারলাম না:",
        "tab_pending": "📋 মুলতুবি কাজ",
        "tab_completed": "✅ সম্পন্ন কাজ",
        "no_pending": "কোনো কাজ বাকি নেই! 🏖️",
        "no_completed": "কোনো কাজ সম্পন্ন হয়নি। 💪",
        "language": "ভাষা / Language",
        "search": "🔍 কাজ খুঁজুন...",
        "metrics_total": "সক্রিয় কাজ",
        "metrics_done": "সম্পন্ন",
        "metrics_overdue": "মেয়াদোত্তীর্ণ"
    },
    "ta": {
        "title": "✨ ஸ்மார்ட் டாஷ்போர்டு",
        "subtitle": "உங்கள் அறிவார்ந்த மேலாளர்.",
        "add_task": "➕ புதிய பணி",
        "desc_label": "பணி விளக்கம்*",
        "desc_placeholder": "கூட்டத்தை திட்டமிடு...",
        "due_label": "ஸ்மார்ட் தேதி",
        "due_placeholder": "நாளை மாலை 5 மணி",
        "priority": "முன்னுரிமை",
        "add_btn": "உருவாக்கு",
        "success": "பணி வெற்றிகரமாக முடிந்தது!",
        "error_date": "தேதியை அறிய முடியவில்லை:",
        "tab_pending": "📋 நிலுவை பணிகள்",
        "tab_completed": "✅ முடிந்த பணிகள்",
        "no_pending": "பணிகள் எதுவும் இல்லை! 🏖️",
        "no_completed": "எந்தப் பணியும் முடிக்கப்படவில்லை. 💪",
        "language": "மொழி / Language",
        "search": "🔍 தேடுங்கள்...",
        "metrics_total": "மொத்தம்",
        "metrics_done": "முடிந்தது",
        "metrics_overdue": "தாமதம்"
    },
    "mr": {
        "title": "✨ स्मार्ट टू-डू डॅशबोर्ड",
        "subtitle": "तुमचा प्रीमियम, बुद्धिमान टास्क मॅनेजर.",
        "add_task": "➕ नवीन कार्य जोडा",
        "desc_label": "कार्याचे वर्णन*",
        "desc_placeholder": "उदा. उद्यासाठी मीटिंग...",
        "due_label": "स्मार्ट तारीख",
        "due_placeholder": "उदा. उद्या संध्याकाळी 5 वाजता",
        "priority": "प्राधान्य पातळी",
        "add_btn": "कार्य तयार करा",
        "success": "कार्य यशस्वीरित्या जोडले!",
        "error_date": "तारीख समजू शकलो नाही:",
        "tab_pending": "📋 प्रलंबित कामे",
        "tab_completed": "✅ पूर्ण झालेली कामे",
        "no_pending": "कोणतेही प्रलंबित काम नाही! मजेत राहा. 🏖️",
        "no_completed": "अद्याप कोणतेही काम पूर्ण झालेले नाही. 💪",
        "language": "भाषा / Language",
        "search": "🔍 आपली कामे शोधा...",
        "metrics_total": "एकूण सक्रिय",
        "metrics_done": "पूर्ण",
        "metrics_overdue": "थकबाकी"
    },
    "kn": {
        "title": "✨ ಸ್ಮಾರ್ಟ್ ಕಾರ್ಯ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "subtitle": "ನಿಮ್ಮ ಪ್ರೀಮಿಯಂ, ಬುದ್ಧಿವಂತ ಕಾರ್ಯ ನಿರ್ವಾಹಕ.",
        "add_task": "➕ ಹೊಸ ಕಾರ್ಯ",
        "desc_label": "ಕಾರ್ಯದ ವಿವರಣೆ*",
        "desc_placeholder": "ಉದಾ. ನಾಳೆ ಸಭೆ...",
        "due_label": "ಸ್ಮಾರ್ಟ್ ದಿನಾಂಕ",
        "due_placeholder": "ಉದಾ. ನಾಳೆ ಸಂಜೆ 5 ಕ್ಕೆ",
        "priority": "ಆದ್ಯತೆ",
        "add_btn": "ಕಾರ್ಯ ರಚಿಸಿ",
        "success": "ಕಾರ್ಯವನ್ನು ಸೇರಿಸಲಾಗಿದೆ!",
        "error_date": "ದಿನಾಂಕ ಅರ್ಥವಾಗಲಿಲ್ಲ:",
        "tab_pending": "📋 ಬಾಕಿ ಇರುವ ಕಾರ್ಯಗಳು",
        "tab_completed": "✅ ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯಗಳು",
        "no_pending": "ಯಾವುದೇ ಕಾರ್ಯಗಳಿಲ್ಲ! 🏖️",
        "no_completed": "ಯಾವುದೇ ಕಾರ್ಯ ಪೂರ್ಣಗೊಂಡಿಲ್ಲ. 💪",
        "language": "ಭಾಷೆ / Language",
        "search": "🔍 ಕಾರ್ಯಗಳನ್ನು ಹುಡುಕಿ...",
        "metrics_total": "ಒಟ್ಟು ಸಕ್ರಿಯ",
        "metrics_done": "ಪೂರ್ಣಗೊಂಡಿದೆ",
        "metrics_overdue": "ಬಾಕಿ ಉಳಿದಿದೆ"
    },
    "te": {
        "title": "✨ స్మార్ట్ టాస్క్ డాష్‌బోర్డ్",
        "subtitle": "మీ ప్రీమియం, తెలివైన టాస్క్ మేనేజర్.",
        "add_task": "➕ కొత్త పని",
        "desc_label": "పని వివరణ*",
        "desc_placeholder": "ఉదా. రేపు సమావేశం...",
        "due_label": "స్మార్ట్ తేదీ",
        "due_placeholder": "ఉదా. రేపు సాయంత్రం 5 గంటలకు",
        "priority": "ప్రాధాన్యత",
        "add_btn": "టాస్క్ సృష్టించండి",
        "success": "టాస్క్ జోడించబడింది!",
        "error_date": "తేదీ అర్థం కాలేదు:",
        "tab_pending": "📋 పెండింగ్‌లో పనులు",
        "tab_completed": "✅ పూర్తయిన పనులు",
        "no_pending": "పెండింగ్ పనులు లేవు! జాలీగా ఉండండి. 🏖️",
        "no_completed": "ఇంకా ఏమి పూర్తి కాలేదు. 💪",
        "language": "భాష / Language",
        "search": "🔍 వెతకండి...",
        "metrics_total": "మొత్తం",
        "metrics_done": "పూర్తయింది",
        "metrics_overdue": "ఆలస్యం"
    },
    "ml": {
        "title": "✨ സ്മാർട്ട് ഡാഷ്ബോർഡ്",
        "subtitle": "നിങ്ങളുടെ പ്രീമിയം ടാസ്ക് മാനേജർ.",
        "add_task": "➕ പുതിയ ടാസ്ക്",
        "desc_label": "ടാസ്ക് വിവരണം*",
        "desc_placeholder": "ഉദാ. നാളത്തെ മീറ്റിംഗ്...",
        "due_label": "സ്മാർട്ട് തീയതി",
        "due_placeholder": "ഉദാ. നാളെ 5 മണിക്ക്",
        "priority": "മുൻഗണന",
        "add_btn": "സൃഷ്ടിക്കുക",
        "success": "ടാസ്ക് ചേർത്തു!",
        "error_date": "തീയതി മനസ്സിലാക്കാൻ കഴിഞ്ഞില്ല:",
        "tab_pending": "📋 ശേഷിക്കുന്നവ",
        "tab_completed": "✅ പൂർത്തിയായവ",
        "no_pending": "ടാസ്ക്കുകളൊന്നുമില്ല! 🏖️",
        "no_completed": "ടാസ്ക്കുകൾ പൂർത്തിയായിട്ടില്ല. 💪",
        "language": "ഭാഷ / Language",
        "search": "🔍 തിരയുക...",
        "metrics_total": "സജീവമായവ",
        "metrics_done": "പൂർത്തിയായി",
        "metrics_overdue": "വൈകിയത്"
    },
    "it": {
        "title": "✨ Dashboard Smart To-Do",
        "subtitle": "Il tuo gestore di attività intelligente e premium.",
        "add_task": "➕ Nuova Attività",
        "desc_label": "Descrizione Attività*",
        "desc_placeholder": "es. Pianifica riunione...",
        "due_label": "Data Intelligente (Scrivi naturalmente!)",
        "due_placeholder": "es. domani alle 17",
        "priority": "Priorità",
        "add_btn": "Crea Attività",
        "success": "Attività aggiunta con successo!",
        "error_date": "Impossibile comprendere la data:",
        "tab_pending": "📋 Attività in Sospeso",
        "tab_completed": "✅ Attività Completate",
        "no_pending": "Nessuna attività in sospeso! 🏖️",
        "no_completed": "Nessuna attività completata. 💪",
        "language": "Lingua / Language",
        "search": "🔍 Cerca attività...",
        "metrics_total": "Totale Attive",
        "metrics_done": "Completate",
        "metrics_overdue": "In Ritardo"
    },
    "es": {
        "title": "✨ Panel de Tareas Inteligente",
        "subtitle": "Tu gestor de tareas premium.",
        "add_task": "➕ Nueva Tarea",
        "desc_label": "Descripción de la Tarea*",
        "desc_placeholder": "Ej. Reunión el viernes...",
        "due_label": "Fecha Inteligente (¡Escribe naturalmente!)",
        "due_placeholder": "ej. mañana a las 5pm",
        "priority": "Prioridad",
        "add_btn": "Crear Tarea",
        "success": "¡Tarea programada!",
        "error_date": "No se pudo entender la fecha:",
        "tab_pending": "📋 Tareas Pendientes",
        "tab_completed": "✅ Tareas Completadas",
        "no_pending": "¡No tienes tareas! 🏖️",
        "no_completed": "Aún no hay tareas completadas. 💪",
        "language": "Idioma / Language",
        "search": "🔍 Buscar tareas...",
        "metrics_total": "Total Activas",
        "metrics_done": "Completadas",
        "metrics_overdue": "Atrasadas"
    },
    "ja": {
        "title": "✨ スマート To-Do ダッシュボード",
        "subtitle": "あなたのプレミアムなタスクマネージャー。",
        "add_task": "➕ 新しいタスク",
        "desc_label": "タスクの説明*",
        "desc_placeholder": "例：明日の会議...",
        "due_label": "スマートな日付",
        "due_placeholder": "例：明日の午後5時",
        "priority": "優先度",
        "add_btn": "タスクを作成",
        "success": "タスクが追加されました！",
        "error_date": "日付が理解できません:",
        "tab_pending": "📋 保留中のタスク",
        "tab_completed": "✅ 完了したタスク",
        "no_pending": "保留中のタスクはありません！ 🏖️",
        "no_completed": "まだ完了したタスクはありません。 💪",
        "language": "言語 / Language",
        "search": "🔍 タスクを検索...",
        "metrics_total": "合計アクティブ",
        "metrics_done": "完了",
        "metrics_overdue": "期限切れ"
    },
    "zh": {
        "title": "✨ 智能待办事项仪表板",
        "subtitle": "您的高级智能任务管理器。",
        "add_task": "➕ 新任务",
        "desc_label": "任务描述*",
        "desc_placeholder": "例如：明天开会...",
        "due_label": "智能日期（自然输入！）",
        "due_placeholder": "例如：明天下午5点",
        "priority": "优先级",
        "add_btn": "创建任务",
        "success": "任务已完美安排！",
        "error_date": "无法理解日期：",
        "tab_pending": "📋 待办事项",
        "tab_completed": "✅ 已完成任务",
        "no_pending": "您没有待办事项！🏖️",
        "no_completed": "尚未完成任何任务。💪",
        "language": "语言 / Language",
        "search": "🔍 搜索任务...",
        "metrics_total": "总计活动",
        "metrics_done": "已完成",
        "metrics_overdue": "已逾期"
    }
}

# Sidebar controls
with st.sidebar:
    lang_map = {"English": "en", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "বাংলা (Bengali)": "bn", "தமிழ் (Tamil)": "ta", "తెలుగు (Telugu)": "te", "ಕನ್ನಡ (Kannada)": "kn", "മലയാളം (Malayalam)": "ml", "Français (French)": "fr", "Deutsch (German)": "de", "Italiano (Italian)": "it", "Español (Spanish)": "es", "日本語 (Japanese)": "ja", "中文 (Chinese)": "zh"}
    with st.expander("🌐 Interface Language", expanded=False):
        selected_lang_name = st.selectbox("Select Language", list(lang_map.keys()), label_visibility="collapsed")
    lang = lang_map[selected_lang_name]
    t = TRANSLATIONS[lang]

    with st.expander(t["add_task"], expanded=True):
        with st.form("add_task_form", clear_on_submit=True):
            desc = st.text_input(t["desc_label"], placeholder=t["desc_placeholder"])
            notes = st.text_area("📝 Extra Notes / Description (Optional)")
            image_file = st.file_uploader("🖼️ Attach Image (Optional)", type=["jpg", "png", "jpeg"])
            audio_file = st.audio_input("🎙️ Record Voice Note (Optional)")
            due = st.text_input(t["due_label"], placeholder=t["due_placeholder"])
            priority = st.selectbox(t["priority"], ["High", "Medium", "Low"], index=1)
            submitted = st.form_submit_button(t["add_btn"], use_container_width=True)
            
            if submitted and desc:
                import os
                import time
                img_path = None
                if image_file:
                    os.makedirs("uploads", exist_ok=True)
                    img_path = f"uploads/img_{int(time.time())}_{image_file.name}"
                    with open(img_path, "wb") as f:
                        f.write(image_file.getbuffer())
                        
                aud_path = None
                if audio_file:
                    os.makedirs("uploads", exist_ok=True)
                    aud_path = f"uploads/aud_{int(time.time())}.wav"
                    with open(aud_path, "wb") as f:
                        f.write(audio_file.getbuffer())
                
                GLOBAL_LANGS = ['en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur', 'fr', 'de', 'it', 'es', 'ja', 'zh']
                due_date = None
                if due:
                    parsed = dateparser.parse(due, languages=GLOBAL_LANGS)
                    if parsed:
                        due_date = parsed.strftime("%Y-%m-%d %H:%M")
                    else:
                        st.error(f"{t['error_date']} {due}")
                
                if not due or due_date:
                    database.add_task(desc, due_date, priority, notes=notes, image_path=img_path, audio_path=aud_path)
                    st.toast(t["success"], icon="🚀")
                    st.rerun()

    with st.expander("⏰ Native Alarms", expanded=False):
        st.caption("Starts a lightweight tracker to send Windows Toast Notifications when tasks are due.")
        if st.button("Launch Background Alarms", use_container_width=True):
            import sys
            import subprocess
            # Open a new external Windows terminal so the alarms keep running independent of the Streamlit web app
            subprocess.Popen([sys.executable, "main.py", "daemon"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            st.toast("Alarm Tracker Launched in a new window!", icon="⏰")

c_title, c_settings = st.columns([0.8, 0.2])
with c_title:
    st.title(t["title"])
    st.markdown(f"*{t['subtitle']}*")

with c_settings:
    st.write("")
    with st.popover("⚙️ Settings", use_container_width=True):
        THEMES = {
            "Auto / System Default": "",
            "Midnight Purple (Dark)": """
                <style>
                [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
                [data-testid="stSidebar"] { background-color: #0f0c29; }
                [data-testid="stHeader"] { background-color: transparent; }
                .stMarkdown p, .stMarkdown span, label, div[data-testid="stMetricLabel"], .st-emotion-cache-1wivap2 { color: #fdfdfd !important; }
                h1, h2, h3, h4, .stMarkdown h4 { color: #f8c291 !important; }
                div[data-testid="stMetricValue"] { color: #f8c291 !important; }
                </style>
            """,
            "Ocean Depth (Dark)": """
                <style>
                [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0b0c10, #1f2833); }
                [data-testid="stSidebar"] { background-color: #0b0c10; border-right: 1px solid #45a29e; }
                [data-testid="stHeader"] { background-color: transparent; }
                .stMarkdown p, .stMarkdown span, label, div[data-testid="stMetricLabel"], .st-emotion-cache-1wivap2 { color: #c5c6c7 !important; }
                h1, h2, h3, h4, .stMarkdown h4 { color: #45a29e !important; }
                div[data-testid="stMetricValue"] { color: #66fcf1 !important; }
                </style>
            """,
            "Forest Whisper (Light)": """
                <style>
                [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #dce35b, #45b649); }
                [data-testid="stSidebar"] { background-color: #e8f5e9; }
                [data-testid="stHeader"] { background-color: transparent; }
                .stMarkdown p, .stMarkdown span, label, div[data-testid="stMetricLabel"], .st-emotion-cache-1wivap2 { color: #000000 !important; }
                h1, h2, h3, h4, .stMarkdown h4 { color: #1b5e20 !important; }
                div[data-testid="stMetricValue"] { color: #1b5e20 !important; }
                </style>
            """,
            "Hacker Matrix (Dark)": """
                <style>
                [data-testid="stAppViewContainer"] { background-color: #000000; }
                [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #00ff00; }
                [data-testid="stHeader"] { background-color: transparent; }
                .stMarkdown p, .stMarkdown span, label, div[data-testid="stMetricLabel"], .st-emotion-cache-1wivap2 { color: #00ff00 !important; font-family: "Courier New", Courier, monospace !important; }
                h1, h2, h3, h4, .stMarkdown h4 { color: #00ff00 !important; font-family: "Courier New", Courier, monospace !important; }
                div[data-testid="stMetricValue"] { color: #00ff00 !important; }
                button { border: 1px solid #00ff00 !important; color: #00ff00 !important; }
                </style>
            """
        }
        selected_theme = st.selectbox("🎨 App Theme", list(THEMES.keys()))
        if THEMES[selected_theme]:
            st.markdown(THEMES[selected_theme], unsafe_allow_html=True)

# Database Calls
all_pending = database.get_tasks("Pending")
all_completed = database.get_tasks("Completed")

# Smart Overdue check
def get_due_status(date_str):
    if not date_str:
        return ""
    try:
        due = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        now = datetime.now()
        diff = due - now
        if diff.total_seconds() < 0:
            return "overdue"
        elif diff.days == 0:
            return "today"
        else:
            return f"in {diff.days} days"
    except:
        return ""

overdue_count = sum(1 for p in all_pending if get_due_status(p['due_date']) == "overdue")

# Premium Metrics Panel
m1, m2, m3 = st.columns(3)
m1.metric(t["metrics_total"], len(all_pending), delta="-0" if not all_pending else None)
m2.metric(t["metrics_done"], len(all_completed), delta=f"+{len(all_completed)}")
m3.metric(t["metrics_overdue"], overdue_count, delta=f"{overdue_count} critical" if overdue_count else None, delta_color="inverse")

st.divider()

@st.dialog("🎉 Task Completed!")
def complete_task_dialog(task_id, description):
    st.write(f"Awesome job finishing: **{description}**")
    remark = st.text_input("Add a 1-line remark about this (optional):", placeholder="e.g. Finished quicker than expected!")
    if st.button("Save & Complete", use_container_width=True):
        database.complete_task(task_id, remark=remark)
        st.session_state.show_balloons = True
        st.rerun()

# Search and Tabs
search_query = st.text_input(t["search"])

tabs = st.tabs([f"{t['tab_pending']} ({len(all_pending)})", f"{t['tab_completed']} ({len(all_completed)})"])

with tabs[0]:
    # Filter pending
    display_pending = all_pending
    if search_query:
        display_pending = [p for p in all_pending if search_query.lower() in p['description'].lower()]
        
    if not display_pending:
        st.info(t["no_pending"])
    else:
        for p_task in display_pending:
            status = get_due_status(p_task['due_date'])
            status_badge = ""
            if status == "overdue":
                status_badge = "🔥 **OVERDUE**"
            elif status == "today":
                status_badge = "⏳ **Due Today**"
            elif status:
                status_badge = f"⏱️ *{status}*"
                
            color = "red" if p_task['priority'] == 'High' else "orange" if p_task['priority'] == 'Medium' else "green"
            
            # Using Streamlit 1.30+ Native visual containers
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.2, 0.2])
                with c1:
                    # Added a bit of margin layout workaround
                    st.write("")
                    if st.button("✅", key=f"done_{p_task['id']}", help="Mark Complete"):
                        complete_task_dialog(p_task['id'], p_task['description'])
                with c2:
                    st.markdown(f"#### {p_task['description']}")
                    try:
                        if p_task.get('notes'):
                            st.info(p_task['notes'])
                        if p_task.get('image_path'):
                            st.image(p_task['image_path'], use_container_width=True)
                        if p_task.get('audio_path'):
                            st.audio(p_task['audio_path'])
                    except Exception as media_err:
                        pass
                        
                    with st.expander("✏️ Add / Edit Media & Notes"):
                        with st.form(f"edit_media_{p_task['id']}", clear_on_submit=False):
                            n_notes = st.text_area("Update Notes", value=p_task['notes'] if p_task.get('notes') else "")
                            n_img = st.file_uploader("Upload New Image", type=["jpg", "png", "jpeg"], key=f"img_{p_task['id']}")
                            n_aud = st.audio_input("Record New Audio", key=f"aud_{p_task['id']}")
                            if st.form_submit_button("Save Changes", use_container_width=True):
                                final_img = p_task.get('image_path')
                                if n_img:
                                    import os, time
                                    os.makedirs("uploads", exist_ok=True)
                                    final_img = f"uploads/img_{int(time.time())}_{n_img.name}"
                                    with open(final_img, "wb") as f:
                                        f.write(n_img.getbuffer())
                                final_aud = p_task.get('audio_path')
                                if n_aud:
                                    import os, time
                                    os.makedirs("uploads", exist_ok=True)
                                    final_aud = f"uploads/aud_{int(time.time())}.wav"
                                    with open(final_aud, "wb") as f:
                                        f.write(n_aud.getbuffer())
                                database.edit_task_media(p_task['id'], notes=n_notes, image_path=final_img, audio_path=final_aud)
                                st.rerun()

                with c3:
                    if p_task['due_date']:
                        st.markdown(f"🗓️ {p_task['due_date']}<br>{status_badge}", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"**Priority:**<br>:{color}[**{p_task['priority']}**]", unsafe_allow_html=True)

with tabs[1]:
    if not all_completed:
        st.info(t["no_completed"])
    else:
        for c_task in all_completed:
            with st.container(border=True):
                c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
                with c1:
                    st.write("")
                    if st.button("🗑️", key=f"del_{c_task['id']}", help="Permamently Delete"):
                        database.delete_task(c_task['id'])
                        st.rerun()
                with c2:
                    st.markdown(f"#### ~~{c_task['description']}~~")
                    if c_task.get('completion_remark'):
                        st.success(f"**Remark:** {c_task['completion_remark']}")
                        
                    with st.expander("✏️ Edit Completion Remark"):
                        with st.form(f"edit_remark_{c_task['id']}", clear_on_submit=False):
                            new_remark = st.text_input("Update your completion remark:", value=c_task.get('completion_remark', ''))
                            if st.form_submit_button("Save Remark", use_container_width=True):
                                database.edit_completion_remark(c_task['id'], new_remark)
                                st.toast("Remark updated flawlessly!", icon="✨")
                                st.rerun()

                    try:
                        if c_task.get('notes'):
                            st.caption(c_task['notes'])
                        if c_task.get('image_path'):
                            st.image(c_task['image_path'], width=100)
                        if c_task.get('audio_path'):
                            st.audio(c_task['audio_path'])
                    except Exception as media_err:
                        pass
                with c3:
                    st.caption(c_task.get('due_date', "No date"))
