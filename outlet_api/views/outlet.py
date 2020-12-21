from django.urls.conf import path
import json
from outlet_api.logic import outlet_logi, users_logic
from akkarmedia import tools, media
from django.views.decorators.csrf import csrf_exempt
import logging
from outletapp.models import Media

log = logging.getLogger(__name__)

@csrf_exempt
def sync(request):
    
    outlet_data_str = request.POST.get('outlet_data')
    author_username = request.POST.get('author_username')
    outlet_image_file = request.FILES.get('outlet_image_file')
    brand_image_1 = request.FILES.get('brand_image_1')
    brand_image_2 = request.FILES.get('brand_image_2')
    
    response = {'status': 'FAIL', 'message': 'MISSING_DATA'}
    
    if outlet_data_str:
        od = json.loads(outlet_data_str)
        
        user = users_logic.get_access_user_by_username(author_username)
        if user:
            
            outlet, wall_units = outlet_logi.add_outlet(od.get('name'), od.get('location'), od.get('size'), od.get('estimation'), od.get('brand'), 
                                            od.get('retail'), od.get('pick_time'), od.get('competitor_brand'), od.get('lat'), od.get('lng'), user)
            
            if outlet:
                c_data = od.get('contract', {})
                
                contract = outlet_logi.create_outlet_contract(outlet, c_data.get('amount'), c_data.get('from_dt'), c_data.get('to_dt'), c_data.get('payment'), c_data.get('remark'), c_data.get('renewal')) 
                
                if outlet_image_file:
                    outlet_image_path, _ = media.upload_to_s3(outlet_image_file, 'uploads/outlets')
                    outlet.medias.add(Media.objects.create(path=outlet_image_path))
                    
                if brand_image_1:
                    wall_unit_1 = wall_units[0] if len(wall_units) == 2 else None
                    if wall_unit_1:
                        brand_image_1_path, brand_image_1_link = media.upload_to_s3(brand_image_1, 'uploads/outlets')
                        wall_unit_1.medias.append(Media.objects.create(path=brand_image_1_path))
                        
                if brand_image_2:
                    wall_unit_2 = wall_units[1] if len(wall_units) == 2 else None
                    if wall_unit_2:
                        brand_image_2_path, brand_image_2_link = media.upload_to_s3(brand_image_2, 'uploads/outlets')
                        wall_unit_2.medias.append(Media.objects.create(path=brand_image_2_path))
                    
                
                outlet.save()
            
            response = {'status': 'SUCCESS'}
            
        else:
            response = {'status': 'FAIL', 'message': 'INVALID_USER'}
    
    return tools.ajax_response(response)

def all_outlets(request):
    
    outlets = outlet_logi.get_all_outlets()
    
    response = {'status': 'SUCCESS', 'payload': list(map(lambda outlet: outlet_logi.outlet_dto(outlet), outlets))}
    
    return tools.ajax_response(response)

urls = [
    path('sync', sync),
    path('all', all_outlets) 
]