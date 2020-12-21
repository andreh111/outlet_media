
from django.http.response import HttpResponse
import json
from datetime import datetime

def ajax_response(data, allow_cross_domain=False):
    """ 
    Formats json data as a proper ajax response
    """
    
    response = HttpResponse(json.dumps(data, ensure_ascii=False, default=json_default_fn), content_type='application/json')
    if allow_cross_domain:
        response["Access-Control-Allow-Origin"] = "*"  
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"  
        response["Access-Control-Max-Age"] = "1000"  
        response["Access-Control-Allow-Headers"] = "Origin, X-Titanium-Id, Content-Type, Accept"
    return response

def json_default_fn(obj):
    """
    default function to handle complex types while dumping to JSON. Below is list of handled types. it is used as part of the json.dumps(default=tools.json_default_fn)
        - datetime: if it has isoformat, it calls d.isoformat()
    """
    
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        obj
        
def parse_dtt(dtt_str):
    """
    @param param: 2018-06-22T13:00:00
    """
    return datetime.strptime(dtt_str, "%Y-%m-%dT%H:%M:%S")

def parse_dt(dt_str):
    """
    @param param: 2018-06-22T13:00:00
    """
    return datetime.strptime(dt_str, "%Y-%m-%d")

def get_media_url(media_path):
    
    return "https://s3.eu-central-1.amazonaws.com/simpleoutlet/uploads/%s" % (media_path, )