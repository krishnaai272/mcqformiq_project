def validate_form(data):
    errors = []
    if not data.get("name"):
        errors.append("Name is required.")
    if data.get("age") and (data["age"] < 0 or data["age"] > 120):
        errors.append("Invalid age.")
    if "fever" in data.get("symptoms", "").lower():
        temp = data.get("temperature")
        if temp is not None and temp < 98:
            errors.append("Fever present but temperature too low (<98°F). Please double-check.")
    return errors