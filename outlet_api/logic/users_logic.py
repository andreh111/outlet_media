
from django.contrib.auth.models import User
from outletapp.models import TrackUser
from akkarmedia import tools


def access_user_dto(user):
    return {
        'username': user.username,
        'password': user.userprofile.local_password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.userprofile.phone,
        'profile_pic': tools.get_media_url(user.userprofile.profile_pic) if user.userprofile.profile_pic else None,
        'email': user.email
    }


def get_access_user_by_username(username):
    return User.objects.select_related("userprofile").filter(username=username, is_superuser=False,
                                                             is_staff=False).first()


def get_access_users():
    """
    Get all users that can access the app
    """

    return User.objects.select_related("userprofile").filter(is_superuser=False, is_staff=False).all()


def add_user_tracking(user, tracking_list):
    track_list = []

    for t in tracking_list:
        TrackUser(user=user, lat=t.get('lat'), long=t.get('long'), location_dt=t.get('location_dt'))

    if track_list:
        TrackUser.objects.bulk_create(track_list)

    return True
