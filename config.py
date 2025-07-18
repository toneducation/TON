
# TONedu Bot Configuration

# Admin Configuration
ADMIN_ID = "YOUR_ADMIN_USER_ID"  # Replace with your actual Telegram user ID
ADMIN_USERNAME = "ezylof"

# Payment Configuration
PLATFORM_WALLET = "0x4a5BD1355da68eA9f256B8E6a3Cf735e10607E11"  # Your main wallet for donations
TEACHER_COMMISSION = 0.7  # Teachers get 70% of payment

# Bot Messages
WELCOME_MESSAGE = """
👋 Welcome to TONedu!

TONedu is a Telegram-based learning platform that connects students with verified tutors and AI-powered assistance. Users can pay for lessons using TON cryptocurrency, while tutors earn securely through the platform.

Choose your role to begin:
"""

TUTOR_APPLICATION_FORMAT = """
🎓 Tutor Application

Please send your application in this format:

Full Name: [Your full name]
Subject(s): [e.g., English, Math, Physics]
Experience (years): [e.g., 3]
Lesson Price (in TON): [e.g., 2 TON]
Your TON Wallet: [Your TON wallet address]
Bio: [Brief description of your teaching experience]

📝 Send all information in one message following the format above.
"""

# Sample Teachers (you can modify these)
SAMPLE_TEACHERS = {
    "teacher_1": {
        "name": "Sarah Johnson",
        "subject": "English",
        "experience": "3 Years",
        "price": "2 TON",
        "wallet": "EQD4a5BD1355da68eA9f256B8E6a3Cf735e10607E11",
        "bio": "Certified English teacher with Cambridge certification"
    },
    "teacher_2": {
        "name": "Maria Rodriguez", 
        "subject": "Mathematics",
        "experience": "5 Years",
        "price": "1.5 TON",
        "wallet": "EQD4a5BD1355da68eA9f256B8E6a3Cf735e10607E11",
        "bio": "Advanced Mathematics specialist with PhD"
    },
    "teacher_3": {
        "name": "Ahmed Hassan",
        "subject": "Physics", 
        "experience": "4 Years",
        "price": "2.5 TON",
        "wallet": "EQD4a5BD1355da68eA9f256B8E6a3Cf735e10607E11",
        "bio": "Physics PhD with hands-on teaching experience"
    }
}
