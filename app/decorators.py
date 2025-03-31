from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Role

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role and current_user.role != Role.ADMIN:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required(Role.ADMIN)(f)