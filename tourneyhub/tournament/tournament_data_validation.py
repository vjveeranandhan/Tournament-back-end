from datetime import datetime

def validate_api_data(data):
    required_fields = ['title', 'description', 'date', 'time', 'address', 'registrationFees', 'firstPrice', 'secondPrice', 'numOfTeams']
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    
    for field in ['title', 'description', 'address', 'registrationFees', 'numOfTeams']:
        if not data.get(field):
            return f"Field '{field}' cannot be null or empty"

    for field in ['firstPrice', 'secondPrice']:
        try:
            value = int(data.get(field))
            if value <= 0:
                return f"Field '{field}' must be a positive integer"
        except (TypeError, ValueError):
            return f"Field '{field}' must be an integer"

    try:
        event_date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        if event_date <= datetime.now():
            return "Field 'date' must be greater than today's date"
    except ValueError:
        return "Field 'date' must be in YYYY-MM-DD format"

    return "Validation passed"

api_data = {
    'title': 'Event Title',
    'description': 'Event Description',
    'date': '2024-08-15',
    'time': None,
    'address': '123 Event Street',
    'registrationFees': '100',
    'firstPrice': '500',
    'secondPrice': '300',
    'numOfTeams': '10'
}

result = validate_api_data(api_data)
print(result)
