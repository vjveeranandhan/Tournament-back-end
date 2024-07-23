import re
from .models import CustomUser

def validate_user_data(data):
    try:
        print("# Minimum password length")
        min_length = 8
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        
        if 'first_name' in data:
            if data['first_name'] is None:
                return False, "First name should not be Null!"
        
        if 'last_name' in data:
            if data['last_name'] is None:
                return False, "Last nmae should not be Null!"
        
        if 'email' in data:
            if data['email'] is not None:
                if CustomUser.objects.filter(email= data['email']).exists():
                    return False, "Email alrady exists!"
            else:
                return False, "Email should not be Null!"
            data['username'] = data['email']
        else:
            print("Email is missing")
            return False, "Email is missing!"
        
        if 'phone' in data:
            if data['phone'] is not None:
                if CustomUser.objects.filter(phone= data['phone']).exists():
                    return False, "Phone number alrady exists!"
            else:
                return False, "Phone Number should not be Null!"
        else:
            return False, "Phone number is missing!"
        
        if 'dateofbirth' in data:
            if data['dateofbirth'] is None:
                return False, "Date of Birth is missing!"
        
        if len(data['password']) < min_length:
            return False, f"Password must be at least {min_length} characters long."
        
        if not re.match(regex, data['password']):
            return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        
        if data['password'] != data['confirm_password']:
            return False, "Passwords do not match."
        
        return True, "Valid."
    except:
        return False, "Something went wrong. Please Try agan later."
