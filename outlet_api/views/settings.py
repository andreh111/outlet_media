
from django.urls.conf import path
from akkarmedia import tools
from outlet_api.logic import users_logic, settings_logic
from outlet_api.common.constants import ResponseStatus

def get_application_settings(request):
    
    response = {
        'status': ResponseStatus.SUCCESS,
        'message': '',
        'payload': {
            'users': list(map(lambda u: users_logic.access_user_dto(u), users_logic.get_access_users())),
            'sizes': list(map(lambda s: settings_logic.settings_dto(s), settings_logic.get_sizes())),
            'estimated_sales': list(map(lambda s: settings_logic.settings_dto(s), settings_logic.get_estimated_sales())),
            'wall_unit_types': list(map(lambda s: settings_logic.settings_dto(s), settings_logic.get_wall_unit_types())),
            'payment_types': list(map(lambda s: settings_logic.settings_dto(s), settings_logic.get_payment_types())),
            'wall_unit_brands': list(map(lambda s: settings_logic.settings_dtw(s), settings_logic.get_wall_unit_brands())),
            'remarks': list(map(lambda s: settings_logic.settings_dto(s), settings_logic.get_remarks())),
        }
    }
    
    return tools.ajax_response(response)
    
urls = [
    path('app_settings', get_application_settings)
]