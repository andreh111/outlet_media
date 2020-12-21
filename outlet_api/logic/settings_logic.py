from outletapp.models import Size, EstimatedSales, WallUnitType, PaymentType,WallUnitBrand,Remark

def get_sizes():
    
    return Size.objects.filter().all()

def get_estimated_sales():
    
    return EstimatedSales.objects.filter().all()

def get_wall_unit_types():
    
    return WallUnitType.objects.filter().all()

def get_payment_types():
    
    return PaymentType.objects.filter().all()

def get_wall_unit_brands():
    return WallUnitBrand.objects.filter().all()

def get_remarks():
    return Remark.objects.filter().all();

def settings_dto(s):
    
    return {
        'name': s.text,
        'id': s.id,
    }

def settings_dtw(s):
    return {
        'name': s.name,
        'id': s.id
    }