
# Simple database for TONedu bot
import json
import os

class SimpleDB:
    def __init__(self):
        self.users_file = "users.json"
        self.tutors_file = "tutors.json"
        self.payments_file = "payments.json"
        
        # Initialize files if they don't exist
        for file in [self.users_file, self.tutors_file, self.payments_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)
    
    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user(self, user_id, user_data):
        users = self.load_data(self.users_file)
        users[str(user_id)] = user_data
        self.save_data(self.users_file, users)
    
    def get_user(self, user_id):
        users = self.load_data(self.users_file)
        return users.get(str(user_id))
    
    def add_tutor_application(self, user_id, application_data):
        tutors = self.load_data(self.tutors_file)
        tutors[str(user_id)] = application_data
        self.save_data(self.tutors_file, tutors)
    
    def get_pending_tutors(self):
        tutors = self.load_data(self.tutors_file)
        return {k: v for k, v in tutors.items() if v.get('status') == 'pending'}
    
    def approve_tutor(self, user_id):
        tutors = self.load_data(self.tutors_file)
        if str(user_id) in tutors:
            tutors[str(user_id)]['status'] = 'approved'
            self.save_data(self.tutors_file, tutors)
    
    def add_payment(self, user_id, payment_data):
        payments = self.load_data(self.payments_file)
        payments[f"{user_id}_{len(payments)}"] = payment_data
        self.save_data(self.payments_file, payments)
