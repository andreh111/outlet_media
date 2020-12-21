from django.urls.conf import path
from akkarmedia import tools
from outlet_api.logic import users_logic
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_user_tracking(request):
    
    d = request.POST
    
    user = users_logic.get_access_user_by_username(d.get('author_username'))
    if user:
        _ = users_logic.add_user_tracking(user, json.loads(d.get('tracking', '[]')))
        response = {'status': 'SUCCESS'}
    else:
        response = {'status': 'FAIL', 'message': 'INVALID_USER'}
    
    return tools.ajax_response(response)
    

urls = [
    path('update_tracking', add_user_tracking)
]