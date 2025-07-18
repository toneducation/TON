
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Load token from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Admin user ID (your actual Telegram user ID)
ADMIN_ID = "5276938671"

# Platform wallet for donations and payments
PLATFORM_WALLET = "0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11"

# Languages
LANGUAGES = {
    'en': {
        'welcome': "👋 Welcome to TONedu — Learn Smarter with AI & Real Tutors!\n\n📚 Whether you're looking for instant AI help or 1-on-1 sessions with expert teachers, we've got you covered.\n\n🔹 Learn any subject\n🔹 Pay easily with TON crypto\n🔹 Get matched with verified tutors\n🔹 Secure lesson management system\n\n👇 Choose how you'd like to begin:",
        'become_student': "📘 Become a Student",
        'become_tutor': "🎓 Become a Tutor",
        'admin_panel': "🛠 Admin Panel",
        'contact_admin': "📞 Contact Admin",
        'earn_ton': "💰 Earn TON",
        'language': "🌐 Language",
        'donate': "💖 Donate",
        'my_lessons': "📚 My Lessons",
        'audio_share': "🎵 Audio Share"
    },
    'ru': {
        'welcome': "👋 Добро пожаловать в TONedu — Учитесь умнее с ИИ и реальными преподавателями!\n\n📚 Независимо от того, ищете ли вы мгновенную помощь ИИ или индивидуальные занятия с экспертными преподавателями, мы поможем вам.\n\n🔹 Изучайте любой предмет\n🔹 Легко платите криптовалютой TON\n🔹 Найдите проверенных преподавателей\n🔹 Безопасная система управления уроками\n\n👇 Выберите, как вы хотите начать:",
        'become_student': "📘 Стать студентом",
        'become_tutor': "🎓 Стать преподавателем",
        'admin_panel': "🛠 Панель администратора",
        'contact_admin': "📞 Связаться с администратором",
        'earn_ton': "💰 Заработать TON",
        'language': "🌐 Язык",
        'donate': "💖 Пожертвовать",
        'my_lessons': "📚 Мои уроки",
        'audio_share': "🎵 Аудио обмен"
    },
    'uz': {
        'welcome': "👋 TONedu'ga xush kelibsiz — AI va haqiqiy o'qituvchilar bilan aqlliroq o'rganing!\n\n📚 Tezkor AI yordamini yoki ekspert o'qituvchilar bilan 1-ga-1 darslarni qidirayotgan bo'lsangiz, sizga yordam beramiz.\n\n🔹 Har qanday fanni o'rganing\n🔹 TON kripto bilan oson to'lang\n🔹 Tekshirilgan o'qituvchilar bilan tanishing\n🔹 Xavfsiz dars boshqaruv tizimi\n\n👇 Qanday boshlashni tanlang:",
        'become_student': "📘 Talaba bo'lish",
        'become_tutor': "🎓 O'qituvchi bo'lish",
        'admin_panel': "🛠 Admin panel",
        'contact_admin': "📞 Admin bilan bog'lanish",
        'earn_ton': "💰 TON ishlab topish",
        'language': "🌐 Til",
        'donate': "💖 Xayriya",
        'my_lessons': "📚 Mening darslarim",
        'audio_share': "🎵 Audio almashish"
    }
}

# Store user data
user_data = {}
user_states = {}
pending_tutors = {}
approved_tutors = {}
payments_history = {}
referrals = {}
active_lessons = {}
lesson_complaints = {}
audio_messages = {}

# Load data from files
def load_data():
    global user_data, pending_tutors, approved_tutors, payments_history, referrals, active_lessons, lesson_complaints, audio_messages
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
    except:
        user_data = {}
    
    try:
        with open('pending_tutors.json', 'r') as f:
            pending_tutors = json.load(f)
    except:
        pending_tutors = {}
    
    try:
        with open('approved_tutors.json', 'r') as f:
            approved_tutors = json.load(f)
    except:
        approved_tutors = {
            "teacher_1": {
                "name": "Sarah Johnson",
                "subject": "English",
                "experience": "3 Years",
                "price": "2 TON",
                "wallet": "UQA3iD3eId0aXX4mm82bTO6kozmZJaz42tsNh1ZoAIuQUfsF",
                "bio": "Certified English teacher with Cambridge certification",
                "rating": 4.8,
                "reviews": 45
            },
            "teacher_2": {
                "name": "Maria Rodriguez",
                "subject": "Mathematics",
                "experience": "5 Years",
                "price": "1.5 TON",
                "wallet": "UQA3iD3eId0aXX4mm82bTO6kozmZJaz42tsNh1ZoAIuQUfsF",
                "bio": "Advanced Mathematics specialist with PhD",
                "rating": 4.9,
                "reviews": 67
            }
        }
    
    try:
        with open('payments_history.json', 'r') as f:
            payments_history = json.load(f)
    except:
        payments_history = {}
    
    try:
        with open('referrals.json', 'r') as f:
            referrals = json.load(f)
    except:
        referrals = {}
    
    try:
        with open('active_lessons.json', 'r') as f:
            active_lessons = json.load(f)
    except:
        active_lessons = {}
    
    try:
        with open('lesson_complaints.json', 'r') as f:
            lesson_complaints = json.load(f)
    except:
        lesson_complaints = {}
    
    try:
        with open('audio_messages.json', 'r') as f:
            audio_messages = json.load(f)
    except:
        audio_messages = {}

# Save data to files
def save_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=2)
    with open('pending_tutors.json', 'w') as f:
        json.dump(pending_tutors, f, indent=2)
    with open('approved_tutors.json', 'w') as f:
        json.dump(approved_tutors, f, indent=2)
    with open('payments_history.json', 'w') as f:
        json.dump(payments_history, f, indent=2)
    with open('referrals.json', 'w') as f:
        json.dump(referrals, f, indent=2)
    with open('active_lessons.json', 'w') as f:
        json.dump(active_lessons, f, indent=2)
    with open('lesson_complaints.json', 'w') as f:
        json.dump(lesson_complaints, f, indent=2)
    with open('audio_messages.json', 'w') as f:
        json.dump(audio_messages, f, indent=2)

# Initialize data
load_data()

# Helper function to add main menu button
def add_menu_button(keyboard, user_lang="en"):
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    keyboard.append([InlineKeyboardButton("💖 Donate", callback_data="donate")])
    return keyboard

# Language selection
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 Choose your language / Выберите язык / Tilni tanlang:",
        reply_markup=reply_markup
    )

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if it's a callback query or direct message
    if hasattr(update, 'callback_query') and update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        username = update.callback_query.from_user.username or update.callback_query.from_user.first_name
        query = update.callback_query
    else:
        user_id = str(update.message.from_user.id)
        username = update.message.from_user.username or update.message.from_user.first_name
        query = None
    
    # Check for referral
    if context.args:
        referrer_id = context.args[0]
        if referrer_id != user_id and referrer_id in user_data:
            if user_id not in referrals:
                referrals[user_id] = {"referred_by": referrer_id, "date": str(datetime.now())}
                if referrer_id not in referrals:
                    referrals[referrer_id] = {"referrals": [], "total_earned": 0}
                referrals[referrer_id]["referrals"].append(user_id)
                save_data()
    
    # Initialize user data
    if user_id not in user_data:
        user_data[user_id] = {
            "username": username,
            "language": "en",
            "join_date": str(datetime.now()),
            "role": "student"
        }
        save_data()
    
    user_lang = user_data[user_id].get("language", "en")
    
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[user_lang]["become_student"], callback_data="become_student")],
        [InlineKeyboardButton(LANGUAGES[user_lang]["become_tutor"], callback_data="become_tutor")],
        [InlineKeyboardButton(LANGUAGES[user_lang]["my_lessons"], callback_data="my_lessons")],
        [InlineKeyboardButton(LANGUAGES[user_lang]["audio_share"], callback_data="audio_share")],
        [InlineKeyboardButton(LANGUAGES[user_lang]["earn_ton"], callback_data="earn_ton")]
    ]
    
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton(LANGUAGES[user_lang]["admin_panel"], callback_data="admin_panel")])
    
    keyboard.extend([
        [InlineKeyboardButton(LANGUAGES[user_lang]["contact_admin"], url="https://t.me/ezylof")],
        [InlineKeyboardButton(LANGUAGES[user_lang]["language"], callback_data="change_language")],
        [InlineKeyboardButton("💖 Donate", callback_data="donate"),
         InlineKeyboardButton("⚡ Quick Donate", callback_data="quick_donate")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(LANGUAGES[user_lang]["welcome"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(LANGUAGES[user_lang]["welcome"], reply_markup=reply_markup)

# Show donation information
async def show_donation_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if it's a callback query or direct message
    if hasattr(update, 'callback_query') and update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        query = update.callback_query
    else:
        user_id = str(update.message.from_user.id)
        query = None
    
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    donation_text = """
💖 **Support TONedu Platform!**

Your donations help us grow and improve our educational platform.

💰 **Easy Donation Process:**
1. Copy the wallet address below
2. Open your TON wallet app
3. Send any amount to the address
4. Help us build better education tools!

🔗 **Donation Wallet:** 
`0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11`

💡 **How donations help:**
• Platform development and maintenance
• Better features for students and teachers
• Improved security and performance
• 24/7 technical support

Every donation, no matter the size, makes a difference! 🚀

Thank you for supporting education! 🎓
    """
    
    keyboard = [
        [InlineKeyboardButton("📋 Copy Wallet Address", callback_data="copy_wallet")],
        [InlineKeyboardButton("💰 Quick Donate 1 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=1000000000")],
        [InlineKeyboardButton("💎 Quick Donate 5 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=5000000000")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(donation_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(donation_text, reply_markup=reply_markup, parse_mode='Markdown')

# Handle button callbacks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    # Initialize user data if not exists
    if user_id not in user_data:
        username = query.from_user.username or query.from_user.first_name
        user_data[user_id] = {
            "username": username,
            "language": "en",
            "join_date": str(datetime.now()),
            "role": "student"
        }
        save_data()
    
    if query.data.startswith("lang_"):
        lang = query.data.split("_")[1]
        user_data[user_id]["language"] = lang
        save_data()
        await query.edit_message_text(f"✅ Language changed to {lang.upper()}")
        await start(update, context)
        return
    
    if query.data == "change_language":
        keyboard = [
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Choose your language:", reply_markup=reply_markup)
        return
    
    if query.data == "main_menu":
        # Create a new update object for main menu
        new_update = Update(
            update_id=update.update_id,
            callback_query=query
        )
        await start(new_update, context)
        return
    
    if query.data == "donate":
        await show_donation_info(update, context)
        return
    
    if query.data == "copy_wallet":
        await query.answer("Wallet address copied! 📋\n0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11", show_alert=True)
        return
    
    if query.data == "quick_donate":
        await show_quick_donate(query, context)
        return
    
    if query.data == "become_student":
        await show_teachers(query, context)
    elif query.data == "become_tutor":
        await start_tutor_application(query, context)
    elif query.data == "my_lessons":
        await show_my_lessons(query, context)
    elif query.data == "audio_share":
        await show_audio_share(query, context)
    elif query.data == "earn_ton":
        await show_earn_ton(query, context)
    elif query.data == "admin_panel" and user_id == ADMIN_ID:
        await show_admin_panel(query, context)
    elif query.data.startswith("select_teacher_"):
        teacher_id = query.data.replace("select_teacher_", "")
        await show_teacher_details(query, context, teacher_id)
    elif query.data.startswith("pay_teacher_"):
        teacher_id = query.data.replace("pay_teacher_", "")
        await show_payment_info(query, context, teacher_id)
    elif query.data.startswith("confirm_payment_"):
        teacher_id = query.data.replace("confirm_payment_", "")
        await handle_payment_confirmation(query, context, teacher_id)
    elif query.data == "back_to_teachers":
        await show_teachers(query, context)
    elif query.data.startswith("rate_teacher_"):
        teacher_id = query.data.replace("rate_teacher_", "")
        await show_rating_options(query, context, teacher_id)
    elif query.data.startswith("rating_"):
        parts = query.data.split("_")
        teacher_id = parts[1]
        rating = int(parts[2])
        await handle_rating(query, context, teacher_id, rating)
    elif query.data.startswith("complete_lesson_"):
        lesson_id = query.data.replace("complete_lesson_", "")
        await complete_lesson(query, context, lesson_id)
    elif query.data.startswith("complain_teacher_"):
        lesson_id = query.data.replace("complain_teacher_", "")
        await file_complaint(query, context, lesson_id)
    
    # Admin panel callbacks
    elif user_id == ADMIN_ID:
        if query.data == "admin_new_applications":
            await show_new_applications(query, context)
        elif query.data == "admin_active_tutors":
            await show_active_tutors(query, context)
        elif query.data == "admin_payment_history":
            await show_payment_history(query, context)
        elif query.data == "admin_students_count":
            await show_students_count(query, context)
        elif query.data == "admin_broadcast":
            await start_broadcast(query, context)
        elif query.data == "admin_search_user":
            await start_user_search(query, context)
        elif query.data == "admin_earn_ton_game":
            await show_earn_ton_stats(query, context)
        elif query.data == "admin_active_lessons":
            await show_admin_active_lessons(query, context)
        elif query.data == "admin_complaints":
            await show_admin_complaints(query, context)
        elif query.data.startswith("approve_tutor_"):
            tutor_id = query.data.replace("approve_tutor_", "")
            await approve_tutor(query, context, tutor_id)
        elif query.data.startswith("reject_tutor_"):
            tutor_id = query.data.replace("reject_tutor_", "")
            await reject_tutor(query, context, tutor_id)
        elif query.data.startswith("pay_teacher_"):
            lesson_id = query.data.replace("pay_teacher_", "")
            await admin_pay_teacher(query, context, lesson_id)

# Show my lessons
async def show_my_lessons(query, context):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    my_lessons = [lesson for lesson_id, lesson in active_lessons.items() 
                  if lesson.get('student_id') == user_id or lesson.get('teacher_id') == user_id]
    
    if not my_lessons:
        keyboard = [
            [InlineKeyboardButton("📚 Browse Teachers", callback_data="become_student")],
            [InlineKeyboardButton("🎓 Become a Tutor", callback_data="become_tutor")]
        ]
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("""
📚 **No Active Lessons Yet**

You don't have any active lessons at the moment.

🎯 **Get Started:**
• Browse our qualified teachers
• Book your first lesson
• Start learning with TONedu!

Choose an option below to continue:
        """, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    lessons_text = "📚 **Your Active Lessons:**\n\n"
    keyboard = []
    
    for i, lesson in enumerate(my_lessons):
        if lesson.get('student_id') == user_id:
            # Student view
            teacher_name = lesson.get('teacher_name', 'Unknown Teacher')
            lessons_text += f"🎓 **Lesson {i+1}**\n"
            lessons_text += f"👨‍🏫 Teacher: {teacher_name}\n"
            lessons_text += f"📖 Subject: {lesson.get('subject', 'N/A')}\n"
            lessons_text += f"💰 Price: {lesson.get('price', 'N/A')}\n"
            lessons_text += f"📅 Started: {lesson.get('start_date', 'N/A')}\n"
            lessons_text += f"📋 Status: {lesson.get('status', 'active')}\n\n"
            
            lesson_id = lesson.get('lesson_id')
            keyboard.append([InlineKeyboardButton(f"✅ Complete Lesson {i+1}", callback_data=f"complete_lesson_{lesson_id}")])
            keyboard.append([InlineKeyboardButton(f"⚠️ Complain about Teacher", callback_data=f"complain_teacher_{lesson_id}")])
        
        elif lesson.get('teacher_id') == user_id:
            # Teacher view
            student_name = lesson.get('student_name', 'Unknown Student')
            lessons_text += f"📖 **Teaching Session {i+1}**\n"
            lessons_text += f"👨‍🎓 Student: {student_name}\n"
            lessons_text += f"📖 Subject: {lesson.get('subject', 'N/A')}\n"
            lessons_text += f"💰 Earnings: {lesson.get('teacher_earnings', 'N/A')}\n"
            lessons_text += f"📅 Started: {lesson.get('start_date', 'N/A')}\n"
            lessons_text += f"📋 Status: {lesson.get('status', 'active')}\n\n"
    
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(lessons_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show audio share
async def show_audio_share(query, context):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    audio_text = """
🎵 **Audio Share Center**

Share voice messages and audio materials with your tutors/students!

📋 **Features:**
• Send voice messages to your lesson partner
• Share audio explanations and materials
• Record pronunciation practice
• Exchange educational audio content

🎯 **How to use:**
1. Start an active lesson first
2. Record your voice message in Telegram
3. Send it in chat with the bot
4. Your lesson partner will receive it automatically

📝 **Note:** Audio sharing is only available for users with active lessons.
    """
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(audio_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show teachers
async def show_teachers(query, context):
    user_lang = user_data.get(str(query.from_user.id), {}).get("language", "en")
    keyboard = []
    teachers_text = "📚 **Available Teachers:**\n\n"
    
    for teacher_id, teacher in approved_tutors.items():
        rating_stars = "⭐" * int(teacher.get("rating", 0))
        teachers_text += f"👨‍🏫 **{teacher['name']}**\n"
        teachers_text += f"📖 Subject: {teacher['subject']}\n"
        teachers_text += f"✅ Experience: {teacher['experience']}\n"
        teachers_text += f"💰 Price: {teacher['price']} per lesson\n"
        teachers_text += f"{rating_stars} {teacher.get('rating', 0)} ({teacher.get('reviews', 0)} reviews)\n"
        teachers_text += f"📝 {teacher['bio']}\n\n"
        
        keyboard.append([InlineKeyboardButton(f"Select {teacher['name']}", callback_data=f"select_teacher_{teacher_id}")])
    
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(teachers_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show teacher details
async def show_teacher_details(query, context, teacher_id):
    user_lang = user_data.get(str(query.from_user.id), {}).get("language", "en")
    teacher = approved_tutors.get(teacher_id)
    if not teacher:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Teacher not found.", reply_markup=reply_markup)
        return
    
    rating_stars = "⭐" * int(teacher.get("rating", 0))
    details_text = f"""
👨‍🏫 **{teacher['name']}**
📖 Subject: {teacher['subject']}
✅ Experience: {teacher['experience']}
💰 Price: {teacher['price']} per lesson
{rating_stars} {teacher.get('rating', 0)} ({teacher.get('reviews', 0)} reviews)
📝 Bio: {teacher['bio']}

Ready to book a lesson?
    """
    
    keyboard = [
        [InlineKeyboardButton("💳 Pay & Book Lesson", callback_data=f"pay_teacher_{teacher_id}")],
        [InlineKeyboardButton("⭐ Rate Teacher", callback_data=f"rate_teacher_{teacher_id}")],
        [InlineKeyboardButton("⬅️ Back to Teachers", callback_data="back_to_teachers")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(details_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show payment info
async def show_payment_info(query, context, teacher_id):
    user_lang = user_data.get(str(query.from_user.id), {}).get("language", "en")
    teacher = approved_tutors.get(teacher_id)
    if not teacher:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Teacher not found.", reply_markup=reply_markup)
        return
    
    payment_text = f"""
💳 **Payment for {teacher['name']}**

💰 Amount: {teacher['price']}
📩 Send TON to Platform Wallet: 
`{PLATFORM_WALLET}`

⚠️ **Important Payment Process:**
1. Send exactly {teacher['price']} TON to the wallet above
2. After payment, click "Confirm Payment" below
3. Admin will verify payment within 1-2 hours
4. Once verified, you'll be connected with the teacher
5. After lesson completion and your approval, teacher receives 70% of payment

💡 **Security:** Your payment is held securely until lesson completion!

Copy the wallet address by tapping on it! 📋
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm Payment", callback_data=f"confirm_payment_{teacher_id}")],
        [InlineKeyboardButton("⬅️ Back to Teacher", callback_data=f"select_teacher_{teacher_id}")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(payment_text, reply_markup=reply_markup, parse_mode='Markdown')

# Handle payment confirmation
async def handle_payment_confirmation(query, context, teacher_id):
    user_id = str(query.from_user.id)
    username = query.from_user.username or query.from_user.first_name
    user_lang = user_data.get(user_id, {}).get("language", "en")
    teacher = approved_tutors.get(teacher_id)
    
    if not teacher:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Teacher not found.", reply_markup=reply_markup)
        return
    
    # Create lesson
    lesson_id = f"lesson_{len(active_lessons)}"
    teacher_earnings = float(teacher['price'].replace(' TON', '')) * 0.7
    
    active_lessons[lesson_id] = {
        "lesson_id": lesson_id,
        "student_id": user_id,
        "student_name": username,
        "teacher_id": teacher_id,
        "teacher_name": teacher['name'],
        "subject": teacher['subject'],
        "price": teacher['price'],
        "teacher_earnings": f"{teacher_earnings} TON",
        "start_date": str(datetime.now()),
        "status": "payment_pending",
        "payment_confirmed": False
    }
    
    # Store payment
    payment_id = f"payment_{len(payments_history)}"
    payments_history[payment_id] = {
        "payment_id": payment_id,
        "lesson_id": lesson_id,
        "user_id": user_id,
        "username": username,
        "teacher_id": teacher_id,
        "teacher_name": teacher['name'],
        "amount": teacher['price'],
        "date": str(datetime.now()),
        "status": "pending_verification"
    }
    save_data()
    
    # Notify admin
    admin_message = f"""
🔔 **NEW PAYMENT CONFIRMATION**

👤 Student: @{username} (ID: {user_id})
👨‍🏫 Teacher: {teacher['name']} (ID: {teacher_id})
💰 Amount: {teacher['price']}
📖 Subject: {teacher['subject']}
🆔 Lesson ID: {lesson_id}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Action Required:**
1. Verify payment in wallet: `{PLATFORM_WALLET}`
2. Connect student with teacher
3. Monitor lesson progress

Please verify the payment and activate the lesson.
    """
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='Markdown')
    except:
        pass
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"""
✅ **Payment Confirmation Received!**

🎓 **Lesson Details:**
• Teacher: {teacher['name']}
• Subject: {teacher['subject']}
• Amount: {teacher['price']}
• Lesson ID: `{lesson_id}`

📋 **Next Steps:**
1. Admin will verify your payment (1-2 hours)
2. You'll be connected with your teacher
3. Teacher will contact you to schedule the lesson
4. After lesson, confirm completion to release payment to teacher

⏰ **Payment held securely until lesson completion!**

Thank you for choosing TONedu! 🚀
    """, reply_markup=reply_markup, parse_mode='Markdown')

# Complete lesson
async def complete_lesson(query, context, lesson_id):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    if lesson_id not in active_lessons:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Lesson not found.", reply_markup=reply_markup)
        return
    
    lesson = active_lessons[lesson_id]
    
    if lesson.get('student_id') != user_id:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ You can only complete your own lessons.", reply_markup=reply_markup)
        return
    
    # Mark lesson as completed
    lesson['status'] = 'completed'
    lesson['completion_date'] = str(datetime.now())
    lesson['student_approved'] = True
    save_data()
    
    # Notify admin to pay teacher
    teacher_id = lesson.get('teacher_id')
    teacher = approved_tutors.get(teacher_id)
    
    admin_message = f"""
✅ **LESSON COMPLETED - PAYMENT RELEASE REQUEST**

🎓 Lesson ID: {lesson_id}
👤 Student: @{lesson.get('student_name')} approved lesson completion
👨‍🏫 Teacher: {lesson.get('teacher_name')}
💰 Teacher Payment Due: {lesson.get('teacher_earnings')}
📖 Subject: {lesson.get('subject')}
⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Action Required:** Release 70% payment to teacher's wallet
Teacher Wallet: {teacher.get('wallet') if teacher else 'Not found'}

Student has confirmed satisfactory lesson completion.
    """
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='Markdown')
    except:
        pass
    
    # Notify teacher
    try:
        await context.bot.send_message(
            chat_id=teacher_id,
            text=f"🎉 **Lesson Completed!**\n\nYour student @{lesson.get('student_name')} has approved the lesson completion. Payment will be processed by admin shortly!\n\nEarnings: {lesson.get('teacher_earnings')}"
        )
    except:
        pass
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"""
✅ **Lesson Completed Successfully!**

Thank you for confirming lesson completion! 

📋 **What happens next:**
• Teacher payment is being processed
• You can rate your teacher if you haven't already
• Your lesson record is saved in your history

🎓 **Ready for more lessons?**
Browse our teachers anytime to continue learning!
    """, reply_markup=reply_markup, parse_mode='Markdown')

# File complaint
async def file_complaint(query, context, lesson_id):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    user_states[user_id] = f"filing_complaint_{lesson_id}"
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("""
⚠️ **File a Complaint**

Please describe your issue with the teacher in detail. Our admin team will review your complaint and take appropriate action.

📝 **Send your complaint message now:**
(Include specific details about what went wrong)
    """, reply_markup=reply_markup, parse_mode='Markdown')

# Show earn TON section
async def show_earn_ton(query, context):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    user_referrals = referrals.get(user_id, {}).get("referrals", [])
    referral_count = len(user_referrals)
    
    earn_text = f"""
💰 **Earn TON by Inviting Friends!**

🎯 **Your Referral Stats:**
👥 Friends Invited: {referral_count}
💰 TON Earned: {referral_count // 5} TON

🎁 **Rewards:**
• 5 friends = 1 TON
• 10 friends = 2 TON (total)
• 15 friends = 3 TON (total)

🔗 **Your Referral Link:**
https://t.me/YourBotUsername?start={user_id}

📋 **How it works:**
1. Share your referral link with friends
2. When they join and use the bot, you get credit
3. Earn 1 TON for every 5 successful referrals!

Share your link and start earning! 🚀
    """
    
    keyboard = [
        [InlineKeyboardButton("🔗 Share Link", switch_inline_query=f"Join TONedu and earn crypto! https://t.me/YourBotUsername?start={user_id}")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(earn_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show rating options
async def show_rating_options(query, context, teacher_id):
    user_lang = user_data.get(str(query.from_user.id), {}).get("language", "en")
    teacher = approved_tutors.get(teacher_id)
    if not teacher:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Teacher not found.", reply_markup=reply_markup)
        return
    
    rating_text = f"⭐ **Rate {teacher['name']}:**\n\nHow would you rate your lesson experience?"
    
    keyboard = [
        [InlineKeyboardButton("⭐", callback_data=f"rating_{teacher_id}_1"),
         InlineKeyboardButton("⭐⭐", callback_data=f"rating_{teacher_id}_2"),
         InlineKeyboardButton("⭐⭐⭐", callback_data=f"rating_{teacher_id}_3")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data=f"rating_{teacher_id}_4"),
         InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data=f"rating_{teacher_id}_5")],
        [InlineKeyboardButton("⬅️ Back", callback_data=f"select_teacher_{teacher_id}")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(rating_text, reply_markup=reply_markup, parse_mode='Markdown')

# Handle rating
async def handle_rating(query, context, teacher_id, rating):
    user_lang = user_data.get(str(query.from_user.id), {}).get("language", "en")
    teacher = approved_tutors.get(teacher_id)
    if not teacher:
        keyboard = []
        keyboard = add_menu_button(keyboard, user_lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❌ Teacher not found.", reply_markup=reply_markup)
        return
    
    # Update teacher rating
    current_rating = teacher.get("rating", 0)
    current_reviews = teacher.get("reviews", 0)
    
    new_rating = ((current_rating * current_reviews) + rating) / (current_reviews + 1)
    teacher["rating"] = round(new_rating, 1)
    teacher["reviews"] = current_reviews + 1
    
    save_data()
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"✅ Thank you for rating {teacher['name']}! Your {rating}-star rating has been recorded.", reply_markup=reply_markup)

# Admin Panel
async def show_admin_panel(query, context):
    admin_text = """
🛠 **TONedu Admin Dashboard**

Welcome to the comprehensive admin control center!
    """
    
    keyboard = [
        [InlineKeyboardButton("📥 New Tutor Applications", callback_data="admin_new_applications")],
        [InlineKeyboardButton("👨‍🏫 Active Tutors", callback_data="admin_active_tutors")],
        [InlineKeyboardButton("💰 Payment History", callback_data="admin_payment_history")],
        [InlineKeyboardButton("📊 Students Count", callback_data="admin_students_count")],
        [InlineKeyboardButton("📚 Active Lessons", callback_data="admin_active_lessons")],
        [InlineKeyboardButton("⚠️ Complaints", callback_data="admin_complaints")],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🔍 Search User", callback_data="admin_search_user")],
        [InlineKeyboardButton("💰 Earn TON Stats", callback_data="admin_earn_ton_game")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show new applications
async def show_new_applications(query, context):
    if not pending_tutors:
        keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📋 No pending tutor applications.", reply_markup=reply_markup)
        return
    
    apps_text = "📥 **New Tutor Applications:**\n\n"
    keyboard = []
    
    for user_id, app in pending_tutors.items():
        user_info = user_data.get(user_id, {})
        username = user_info.get('username', 'Unknown')
        apps_text += f"👤 @{username} (ID: {user_id})\n"
        apps_text += f"📝 {app['application'][:150]}...\n\n"
        keyboard.append([
            InlineKeyboardButton(f"✅ Approve {username}", callback_data=f"approve_tutor_{user_id}"),
            InlineKeyboardButton(f"❌ Reject {username}", callback_data=f"reject_tutor_{user_id}")
        ])
    
    keyboard.append([InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(apps_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show active tutors
async def show_active_tutors(query, context):
    tutors_text = "👨‍🏫 **Active Tutors:**\n\n"
    
    for teacher_id, teacher in approved_tutors.items():
        # Find teacher's user data for nickname
        teacher_user_id = None
        for uid, user in user_data.items():
            if user.get('role') == 'tutor' and teacher.get('name') in str(user.get('username', '')):
                teacher_user_id = uid
                break
        
        nickname = f"@{user_data.get(teacher_user_id, {}).get('username', 'N/A')}" if teacher_user_id else "N/A"
        
        tutors_text += f"• **{teacher['name']}** {nickname}\n"
        tutors_text += f"  📖 {teacher['subject']} - 💰 {teacher['price']}\n"
        tutors_text += f"  ⭐ {teacher.get('rating', 0)} ({teacher.get('reviews', 0)} reviews)\n"
        tutors_text += f"  👤 User ID: {teacher_user_id or 'Unknown'}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(tutors_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show admin active lessons
async def show_admin_active_lessons(query, context):
    if not active_lessons:
        keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 No active lessons found.", reply_markup=reply_markup)
        return
    
    lessons_text = "📚 **Active Lessons Management:**\n\n"
    keyboard = []
    
    for lesson_id, lesson in active_lessons.items():
        student_username = lesson.get('student_name', 'Unknown')
        teacher_name = lesson.get('teacher_name', 'Unknown')
        status = lesson.get('status', 'unknown')
        
        lessons_text += f"🆔 **{lesson_id}**\n"
        lessons_text += f"👨‍🎓 Student: @{student_username}\n"
        lessons_text += f"👨‍🏫 Teacher: {teacher_name}\n"
        lessons_text += f"📖 Subject: {lesson.get('subject', 'N/A')}\n"
        lessons_text += f"💰 Amount: {lesson.get('price', 'N/A')}\n"
        lessons_text += f"📋 Status: {status}\n\n"
        
        if status == 'completed' and lesson.get('student_approved'):
            keyboard.append([InlineKeyboardButton(f"💸 Pay Teacher - {lesson_id}", callback_data=f"pay_teacher_{lesson_id}")])
    
    keyboard.append([InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(lessons_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show admin complaints
async def show_admin_complaints(query, context):
    if not lesson_complaints:
        keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("⚠️ No complaints found.", reply_markup=reply_markup)
        return
    
    complaints_text = "⚠️ **Student Complaints:**\n\n"
    
    for complaint_id, complaint in lesson_complaints.items():
        complaints_text += f"🆔 **{complaint_id}**\n"
        complaints_text += f"👤 Student: @{complaint.get('student_name', 'Unknown')}\n"
        complaints_text += f"📖 Lesson: {complaint.get('lesson_id', 'Unknown')}\n"
        complaints_text += f"📝 Complaint: {complaint.get('complaint_text', 'N/A')[:100]}...\n"
        complaints_text += f"📅 Date: {complaint.get('date', 'N/A')}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(complaints_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show payment history
async def show_payment_history(query, context):
    if not payments_history:
        keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("💰 No payment history found.", reply_markup=reply_markup)
        return
    
    history_text = "💰 **Recent Payments:**\n\n"
    
    for payment_id, payment in list(payments_history.items())[-10:]:
        history_text += f"• @{payment.get('username', 'Unknown')} - {payment.get('date', 'N/A')[:10]}\n"
        history_text += f"  💰 {payment.get('amount', 'N/A')} - 📋 {payment.get('status', 'N/A')}\n"
        history_text += f"  👨‍🏫 Teacher: {payment.get('teacher_name', 'N/A')}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(history_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show students count
async def show_students_count(query, context):
    students = [user for user in user_data.values() if user.get('role') == 'student']
    tutors = [user for user in user_data.values() if user.get('role') == 'tutor']
    
    # Show students with nicknames
    students_text = "📊 **Platform Statistics:**\n\n"
    students_text += f"👥 **Total Students:** {len(students)}\n"
    
    if students:
        students_text += "**Student List:**\n"
        for i, student in enumerate(students[:10]):  # Show first 10
            username = student.get('username', 'Unknown')
            join_date = student.get('join_date', 'N/A')[:10]
            students_text += f"{i+1}. @{username} (Joined: {join_date})\n"
        
        if len(students) > 10:
            students_text += f"... and {len(students) - 10} more\n"
    
    students_text += f"\n🎓 **Total Tutors:** {len(approved_tutors)}\n"
    students_text += f"💰 **Total Payments:** {len(payments_history)}\n"
    students_text += f"📚 **Active Lessons:** {len(active_lessons)}\n"
    students_text += f"🔗 **Total Referrals:** {len(referrals)}\n"
    students_text += f"⚠️ **Complaints:** {len(lesson_complaints)}\n\n"
    students_text += f"📈 **Growth this month:** +{len([u for u in user_data.values() if u.get('join_date', '')[:7] == str(datetime.now())[:7]])} users"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(students_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show earn TON stats
async def show_earn_ton_stats(query, context):
    stats_text = "💰 **Earn TON Game Statistics:**\n\n"
    
    for user_id, ref_data in referrals.items():
        if 'referrals' in ref_data:
            user_info = user_data.get(user_id, {})
            username = user_info.get('username', 'Unknown')
            referral_count = len(ref_data['referrals'])
            earnings = referral_count // 5
            
            stats_text += f"• @{username}: {referral_count} referrals, {earnings} TON earned\n"
    
    if len(stats_text) < 50:
        stats_text += "No referral activity yet."
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode='Markdown')

# Start tutor application
async def start_tutor_application(query, context):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    user_states[user_id] = "applying_as_tutor"
    
    keyboard = []
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("""
🎓 **Tutor Application**

Please send your application in this format:

**Full Name:** [Your full name]
**Subject(s):** [e.g., English, Math, Physics]
**Experience (years):** [e.g., 3]
**Lesson Price (in TON):** [e.g., 2 TON]
**Your TON Wallet:** [Your TON wallet address]
**Bio:** [Brief description of your teaching experience]

📝 Send all information in one message following the format above.
    """, reply_markup=reply_markup, parse_mode='Markdown')

# Handle user search from admin panel
async def handle_user_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    
    if user_states.get(user_id) == "searching_user":
        search_term = update.message.text.strip()
        found_users = []

        # Search in user_data for the user ID or username
        for uid, user in user_data.items():
            username = user.get("username", "")
            if username == search_term.replace("@", "") or uid == search_term:
                role = user.get("role", "student")
                join_date = user.get("join_date", "N/A")[:10]
                found_users.append(f"👤 **@{username}** (ID: {uid})\n📋 Role: {role}\n📅 Joined: {join_date}\n")

        if found_users:
            result_text = "🔍 **Search Results:**\n\n" + "\n".join(found_users)
        else:
            result_text = "❌ No user found with that username or ID."
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        user_states[user_id] = None  # Reset state

# Handle tutor application and other message types
async def handle_tutor_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    # Handle user search
    if user_states.get(user_id) == "searching_user":
        await handle_user_search(update, context)
        return
    
    # Handle complaint filing
    if user_states.get(user_id, "").startswith("filing_complaint_"):
        lesson_id = user_states[user_id].replace("filing_complaint_", "")
        complaint_text = update.message.text
        username = update.message.from_user.username or update.message.from_user.first_name
        
        complaint_id = f"complaint_{len(lesson_complaints)}"
        lesson_complaints[complaint_id] = {
            "complaint_id": complaint_id,
            "lesson_id": lesson_id,
            "student_id": user_id,
            "student_name": username,
            "complaint_text": complaint_text,
            "date": str(datetime.now()),
            "status": "pending"
        }
        save_data()
        
        # Notify admin
        admin_message = f"""
⚠️ **NEW STUDENT COMPLAINT**

👤 Student: @{username} (ID: {user_id})
📖 Lesson ID: {lesson_id}
📝 Complaint: {complaint_text}
⏰ Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Please review and take appropriate action.
        """
        
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='Markdown')
        except:
            pass
        
        await update.message.reply_text("""
✅ **Complaint Filed Successfully!**

Your complaint has been submitted to our admin team for review.

📋 **What happens next:**
1. Admin team will investigate the issue
2. We'll contact you within 24 hours
3. Appropriate action will be taken if needed

Thank you for your feedback! 🙏
        """, parse_mode='Markdown')
        
        user_states[user_id] = None
        return
    
    # Handle tutor application
    if user_states.get(user_id) == "applying_as_tutor":
        application_text = update.message.text
        username = update.message.from_user.username or update.message.from_user.first_name
        
        pending_tutors[user_id] = {
            "username": username,
            "application": application_text,
            "date": str(datetime.now()),
            "status": "pending"
        }
        
        # Update user role
        user_data[user_id]["role"] = "tutor_pending"
        save_data()
        
        # Notify admin
        admin_message = f"""
🎓 **NEW TUTOR APPLICATION**

👤 Applicant: @{username} (ID: {user_id})
⏰ Applied: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**APPLICATION DETAILS:**
{application_text}

Please review and approve/reject this application.
        """
        
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='Markdown')
        except:
            pass
        
        await update.message.reply_text("""
✅ **Application Submitted!**

Your tutor application has been received and sent to our admin team for review.

📋 **What happens next:**
1. Admin reviews your profile and qualifications
2. You'll be notified about approval status within 24-48 hours
3. Once approved, you can start receiving students
4. You'll earn 70% of lesson fees after completion

⏰ Review process typically takes 24-48 hours.

Thank you for wanting to be part of TONedu! 🎓
        """)
        
        user_states[user_id] = None
    
    elif user_states.get(user_id) == "broadcasting":
        # Handle broadcast message
        broadcast_text = update.message.text
        user_count = 0
        
        for uid in user_data.keys():
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 **Broadcast Message:**\n\n{broadcast_text}", parse_mode='Markdown')
                user_count += 1
            except:
                pass
        
        await update.message.reply_text(f"📢 Broadcast sent to {user_count} users!")
        user_states[user_id] = None
    
    # Handle voice messages for audio sharing
    elif update.message.voice:
        await handle_audio_message(update, context)

# Handle audio messages
async def handle_audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or update.message.from_user.first_name
    
    # Find active lessons for this user
    user_lessons = [lesson for lesson_id, lesson in active_lessons.items() 
                   if lesson.get('student_id') == user_id or lesson.get('teacher_id') == user_id]
    
    if not user_lessons:
        await update.message.reply_text("🎵 Audio sharing is only available for users with active lessons.")
        return
    
    # Store audio message
    audio_id = f"audio_{len(audio_messages)}"
    voice_file_id = update.message.voice.file_id
    
    audio_messages[audio_id] = {
        "audio_id": audio_id,
        "sender_id": user_id,
        "sender_name": username,
        "voice_file_id": voice_file_id,
        "date": str(datetime.now()),
        "lessons": [lesson.get('lesson_id') for lesson in user_lessons]
    }
    save_data()
    
    # Forward to lesson partners
    for lesson in user_lessons:
        partner_id = lesson.get('teacher_id') if lesson.get('student_id') == user_id else lesson.get('student_id')
        partner_name = lesson.get('teacher_name') if lesson.get('student_id') == user_id else lesson.get('student_name')
        
        if partner_id:
            try:
                await context.bot.send_voice(
                    chat_id=partner_id,
                    voice=voice_file_id,
                    caption=f"🎵 **Audio message from @{username}**\n📖 Lesson: {lesson.get('subject', 'N/A')}"
                )
            except:
                pass
    
    await update.message.reply_text("🎵 Audio message sent to your lesson partner(s)!")

# Admin functions
async def approve_tutor(query, context, tutor_id):
    if tutor_id in pending_tutors:
        app = pending_tutors[tutor_id]
        
        # Parse application
        app_lines = app['application'].split('\n')
        teacher_data = {
            "name": "New Teacher",
            "subject": "Various",
            "experience": "1 Year",
            "price": "2 TON",
            "wallet": "UQA3iD3eId0aXX4mm82bTO6kozmZJaz42tsNh1ZoAIuQUfsF",
            "bio": "Newly approved tutor",
            "rating": 5.0,
            "reviews": 0
        }
        
        # Try to parse application details
        for line in app_lines:
            if "name:" in line.lower():
                teacher_data["name"] = line.split(":", 1)[1].strip()
            elif "subject" in line.lower():
                teacher_data["subject"] = line.split(":", 1)[1].strip()
            elif "experience" in line.lower():
                teacher_data["experience"] = line.split(":", 1)[1].strip()
            elif "price" in line.lower():
                teacher_data["price"] = line.split(":", 1)[1].strip()
            elif "wallet" in line.lower():
                teacher_data["wallet"] = line.split(":", 1)[1].strip()
            elif "bio" in line.lower():
                teacher_data["bio"] = line.split(":", 1)[1].strip()
        
        # Add to approved tutors
        approved_tutors[f"teacher_{len(approved_tutors)}"] = teacher_data
        
        # Update user role
        user_data[tutor_id]["role"] = "tutor"
        
        del pending_tutors[tutor_id]
        save_data()
        
        # Notify tutor
        try:
            await context.bot.send_message(
                chat_id=tutor_id,
                text="🎉 **Congratulations!** Your tutor application has been approved! You can now start receiving students and earning TON!"
            )
        except:
            pass
        
        await query.edit_message_text(f"✅ Tutor @{app['username']} approved successfully!")

async def reject_tutor(query, context, tutor_id):
    if tutor_id in pending_tutors:
        app = pending_tutors[tutor_id]
        del pending_tutors[tutor_id]
        
        # Reset user role
        user_data[tutor_id]["role"] = "student"
        save_data()
        
        # Notify tutor
        try:
            await context.bot.send_message(
                chat_id=tutor_id,
                text="❌ Unfortunately, your tutor application was not approved. Please contact admin for more details or reapply with more information."
            )
        except:
            pass
        
        await query.edit_message_text(f"❌ Tutor @{app['username']} rejected.")

async def start_broadcast(query, context):
    user_id = str(query.from_user.id)
    user_states[user_id] = "broadcasting"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("""
📢 **Broadcast Message**

Send me the message you want to broadcast to all users.

This message will be sent to all registered users on the platform.
    """, reply_markup=reply_markup, parse_mode='Markdown')

async def start_user_search(query, context):
    user_id = str(query.from_user.id)
    user_states[user_id] = "searching_user"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Admin Panel", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("""
🔍 **Search User**

Send me a user ID or username to search for.

**Examples:** 
• `123456789` (User ID)
• `@username` (Username)
• `username` (Without @)
    """, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_pay_teacher(query, context, lesson_id):
    if lesson_id not in active_lessons:
        await query.edit_message_text("❌ Lesson not found.")
        return
    
    lesson = active_lessons[lesson_id]
    teacher_id = lesson.get('teacher_id')
    teacher = approved_tutors.get(teacher_id)
    
    if not teacher:
        await query.edit_message_text("❌ Teacher not found.")
        return
    
    # Mark payment as completed
    lesson['teacher_paid'] = True
    lesson['payment_date'] = str(datetime.now())
    save_data()
    
    # Notify teacher
    try:
        await context.bot.send_message(
            chat_id=teacher_id,
            text=f"💰 **Payment Received!**\n\nYou have been paid {lesson.get('teacher_earnings')} for lesson {lesson_id}.\n\nThank you for teaching on TONedu! 🎓"
        )
    except:
        pass
    
    await query.edit_message_text(f"✅ Teacher payment completed for lesson {lesson_id}!")

# Show quick donate options
async def show_quick_donate(query, context):
    user_id = str(query.from_user.id)
    user_lang = user_data.get(user_id, {}).get("language", "en")
    
    quick_donate_text = """
⚡ **Quick Donate to TONedu**

Support our educational platform instantly!

💰 **Choose your donation amount:**

🔗 **Wallet Address:** 
`0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11`

📱 **Instructions:**
1. Tap on any amount below
2. Your wallet app will open automatically
3. Confirm the transaction
4. Thank you for supporting education! 🎓
    """
    
    keyboard = [
        [InlineKeyboardButton("💎 1 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=1000000000&text=TONedu%20Donation%201%20TON")],
        [InlineKeyboardButton("💰 2 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=2000000000&text=TONedu%20Donation%202%20TON")],
        [InlineKeyboardButton("🚀 5 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=5000000000&text=TONedu%20Donation%205%20TON")],
        [InlineKeyboardButton("💎 10 TON", url="ton://transfer/0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11?amount=10000000000&text=TONedu%20Donation%2010%20TON")],
        [InlineKeyboardButton("📋 Copy Wallet Address", callback_data="copy_wallet")]
    ]
    keyboard = add_menu_button(keyboard, user_lang)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(quick_donate_text, reply_markup=reply_markup, parse_mode='Markdown')

# Show donation information via command
async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_donation_info(update, context)

# Main bot runner
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_selection))
    app.add_handler(CommandHandler("donate", donate_command))
    
    # Callback query handler
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Message handler for text, voice, and other content
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tutor_application))
    app.add_handler(MessageHandler(filters.VOICE, handle_tutor_application))
    
    print("🤖 TONedu BOT IS RUNNING...")
    print("🌐 Multi-language support: EN/RU/UZ")
    print("💰 Referral system active")
    print("🛠 Enhanced admin panel available")
    print("⭐ Rating system enabled")
    print("📚 Lesson management system active")
    print("🎵 Audio sharing enabled")
    print("💖 Donation system integrated")
    app.run_polling()

if __name__ == "__main__":
    main()
