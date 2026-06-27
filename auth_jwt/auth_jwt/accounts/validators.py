import re

def validate_password_strength(password):
    """
    Valida que la contraseña tenga al menos 8 caracteres
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    # Opcional: validar que tenga al menos una mayúscula, un número y un carácter especial
    # if not re.search(r'[A-Z]', password):
    #     return False, "La contraseña debe contener al menos una mayúscula"
    # if not re.search(r'[0-9]', password):
    #     return False, "La contraseña debe contener al menos un número"
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, ""