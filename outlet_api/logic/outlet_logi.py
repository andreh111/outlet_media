from outletapp.models import Outlet, Contract, Wallunit
import logging
import uuid
from akkarmedia import tools

log = logging.getLogger(__name__)


def get_all_outlets():
    return Outlet.objects.all()


def outlet_dto(outlet):
    outlet_media = outlet.medias.first()
    wall_units = Wallunit.objects.filter(outlet=outlet).all()

    wall_unit_list = []
    for w in wall_units:

        tmp_w = {"brand": w.brand_id, "wall_unit_type": w.wall_unit_type_id}

        w_image = w.medias.first()
        if w_image and w_image.path:
            tmp_w['image_url'] = tools.get_media_url(w_image.path)

        wall_unit_list.append(tmp_w)

    outlet_dict = {
        "name": outlet.name,
        "location": outlet.location,
        "size": outlet.size_id,
        "estimation": outlet.estimated_sales_id,
        "lat": outlet.lat,
        "lng": outlet.long,
        "brands": wall_unit_list,
        "brand": 0,  # outlet.brand_id,  #TODO
        "retail": outlet.is_retail,
        "pick_time": 0,
        "competitor_brand": 0,
    }

    if outlet_media and outlet_media.path:
        outlet_dict['image_url'] = tools.get_media_url(outlet_media.path)

    contract = Contract.objects.filter(outlet=outlet).first()
    if contract:
        outlet_dict['contract'] = {
            "amount": contract.amount,
            "from_dt": contract.from_dt,
            "to_dt": contract.to_dt,
            "payment": contract.payment_id,
            "remark": contract.remark_id,
            "renewal": contract.renewable
        }

    return outlet_dict


def add_outlet(name, location, size_id, estimation_id, brand_id, retail, pick_time, competitor_brand_id, lat, lng, user,
               brands):
    """
    @param name: <string>, the name of the outlet
    @param location: <string>, The location name of this outlet
    @param size_id: <int> the primary key of the models.Size model to assign to this outlet
    @param estimation_id: <int> the primary key of the models.EstimatedSales model to assign to this outlet 
    @param brand_id: <int> the primary key of the models.Brand model to assign to this outlet
    @param retail: <boolean> if retail or not
    @param pick_time: <int> the primary key of the models.Brand model to assign to this outlet
    @param competitor_brand_id: <int> the primary key of the models.CompetitorBrand model to assign to this outlet
    @param lat: <double> the latitutde coordinate of this outlet
    @param lng: <double> the longitude coordinate of this outlet
    @param user: the User object who added this outlet
    """

    outlet = None
    try:
        outlet = Outlet()

        outlet.code = str(uuid.uuid4())
        outlet.name = name
        outlet.location = location
        outlet.estimation_id = estimation_id
        outlet.size_id = size_id
        outlet.brand_id = brand_id
        outlet.retail = retail
        outlet.pick_time = pick_time
        outlet.competitor_brand_id = competitor_brand_id
        outlet.lat = lat
        outlet.long = lng
        outlet.user = user

        outlet.save()

        wall_units = []

        for b in brands:
            try:
                w = Wallunit.objects.create(outlet=outlet, wall_unit_type_id=b.get('wall_unit_type'),
                                            brand_id=b.get('brand'))
                wall_units.append(w)
            except:
                log.error("Error occured while adding wall unit type for outlet %s", outlet)

    except:
        log.error("Not able to create the outlet added by %s", user, exc_info=1)

    return outlet, wall_units


def create_outlet_contract(outlet, amount, from_dt, to_dt, payment, remark, renewal):
    """
    @param outlet: the models.Outlet object
    @param amount: <int>, the primary key fo the models.Amount
    @param from_dt: <String> representing a datetime object
    @param to_dt: <String> representing a datetime object 
    @param payment: <int>, the primary key fo the models.PaymentType
    @param remark: <int>, the primary key fo the models.Remark
    @param renewal: <boolean> if is renewal or not
    """

    outlet_contract = None
    try:
        outlet_contract = Contract()

        outlet_contract.amount_id = amount
        outlet_contract.from_dt = tools.parse_dt(from_dt)
        outlet_contract.to_dt = tools.parse_dt(to_dt)
        outlet_contract.payment_id = payment
        outlet_contract.renewal = renewal
        outlet_contract.remark_id = remark

        outlet_contract.save()

    except:
        log.error("Not able to create a contract for the outlet %s", outlet, exc_info=1)

    return outlet_contract
