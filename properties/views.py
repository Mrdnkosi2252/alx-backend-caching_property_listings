from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    
    
    properties_data = []
    for property in properties:
        properties_data.append({
            'title': property.title,
            'description': property.description,
            'price': float(property.price),  
            'location': property.location,
            'created_at': property.created_at.isoformat()  
        })
    
    
    return JsonResponse({
        'data': properties_data
    }, encoder=DecimalEncoder)