from . import app
from .auth import current_user, user_signed_in

@app.context_processor
def inject_current_user():
    return {'current_user': current_user}


@app.context_processor
def inject_user_signed_in():
    return {'user_signed_in': user_signed_in}
