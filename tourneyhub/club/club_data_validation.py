import re
from .models import Club
from user_manager.models import CustomUser

def validate_club_data(data, activity):
    phone_number_pattern = r'^[6-9]\d{9}$'
    phone_number_regex = re.compile(phone_number_pattern)
    try:
        if activity == 'fetch-club':
            if CustomUser.objects.filter(id= data['user_id']).first():
                club = Club.objects.filter(created_by= data['user_id']).first()
                if club:
                    return True, club
                return False, "Club not found"
            else:
                return False, "Invalid user"
        else:
            if data['user_id']:
                if CustomUser.objects.filter(id= data['user_id']).first():
                    if Club.objects.filter(created_by= data['user_id']).exists():
                        return False, "Only one club is allowed for a person"
                else:
                    return False, "Invalid user"
            if activity == 'club-update':
                if 'id' not in data:
                    return False, "club id missing!"
            if 'club_name' in data:
                if data['club_name'] is None:
                    return False, "Club name should not be Null!"
            if 'description' in data:
                if data['description'] is None:
                    return False, "Description should not be Null!"
            if 'country' in data:
                if data['country'] is None:
                    return False, "Country should not be Null!"
            if 'state' in data:
                if data['state'] is None:
                    return False, "State should not be Null!"
            if 'district' in data:
                if data['district'] is None:
                    return False, "District should not be Null!"
            if 'email' in data:
                if data['email'] is not None:
                    if activity == 'club-update':
                        if Club.objects.filter(email= data['email'] ).exclude(id=data['id']).exists():
                            return False, "Email alrady exists!"
                    else:
                        if Club.objects.filter(email= data['email'] ).exists():
                            return False, "Email alrady exists!"
                else:
                    return False, "Email should not be Null!"
            else:
                return False, "Email is missing!"
            if 'phone' in data:
                if data['phone'] is not None:
                    if activity == 'club-update':
                        if phone_number_regex.match(data['phone']):
                            if Club.objects.filter(phone= data['phone']).exclude(id=data['id']).exists():
                                return False, "Phone number alrady exists!"
                        else:
                            return False, "Invalid phone number!"
                        
                    else:
                        if Club.objects.filter(phone= data['phone']).exists():
                            return False, "Phone number alrady exists!"
                else:
                    return False, "Phone Number should not be Null!"
            else:
                return False, "Phone number is missing!"
        
        return True, "Valid."
    except:
        return False, "Something went wrong. Please Try agan later."
