from django.shortcuts import render,redirect
from .models import Outlet,UserProfile,Contract,TrackUser,Media
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import *
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from _datetime import datetime
from akkarmedia import media
from outlet_api.views import outlet
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# from django.core.files.storage import FileSystemStorage




@login_required(login_url='/accounts/login')
def home(request):
    #Upon signing in , if the user is not an admin , log him out and notify him 
    if not (request.user.is_staff) or (not request.user.is_superuser):      
        logout(request)
        return HttpResponse("Invalid login,You are not an admin . ")
    
    #if the user is an admin
    else:
        outlets_count = Outlet.objects.count()
        users_count = UserProfile.objects.count()
        contracts_count = Contract.objects.count()
        outlets = Outlet.objects.all()
        first4 = Outlet.objects.all()[0:4]
        return render(request,'dashboard.html',{'outlets_count':outlets_count,'users_count':users_count,'contracts_count':contracts_count,'outlets':outlets,'first4':first4})

@login_required(login_url='/accounts/login')
def outlets(request):
    out = Outlet.objects.all()
    return render(request, 'outlets.html',{'outlets':out})

@login_required(login_url='/accounts/login')
def users(request):
    all_users = UserProfile.objects.all()
    users_count = UserProfile.objects.count()

    return render(request, 'users.html',{'users':all_users,'users_count':users_count})

@login_required(login_url='/accounts/login')
def tracking(request):
    """
    Track a user within a time range in a specific date
    
    @param sel: the selected user to be tracked 
    @param notfound:returned as 1 if there is no records for the user in the selected range,as None if already found 
    """
    users = UserProfile.objects.all()
    sel = None
    notfound = None
    if request.method == 'POST':
        sel = request.POST['sel']
    if sel and sel != "select":
        date = request.POST['date1']
        track = TrackUser.objects.filter(user__username=sel ,location_dt__date=date,location_dt__time__gte=request.POST['time1'],location_dt__time__lte=request.POST['time2'])
        #if there are records available 
        if track:
            return render(request, 'tracking.html',{'track':track,'users':users})
        #if no records found
        else:
            notfound = 1
            return render(request, 'tracking.html',{'track':track,'users':users,'notfound':notfound})
    
    return render(request, 'tracking.html',{'users':users})




@login_required(login_url='/accounts/login')
def profile(request,username=None):    
    """
    visit a user profile, two post forms , upload a profile image and edit password
    @param username:the username of the user to visit profile, if no username is given , land the user in his profile 
    
    """
    #if a username is given , get the user , unless he's an admin or a superadmin , in this case visiting is profile isn't permitted
    if username and ((not User.objects.get(username=username).is_staff) or (not User.objects.get(username=username).is_superuser)):
#       host is the user to visit profile  
        host = User.objects.get(username=username)
    else:
        #if the username is None , the host is the logged in user himself
        host = request.user
    #errs are the errors in the password change form 
    errs=None
    if request.method == 'POST':
        #if the change password form is involved
        if "savepass" in request.POST:
            form = PasswordChangeForm(host, request.POST)
            if form.is_valid():
                #save the new password in the local_password field
                host.userprofile.local_password=form.cleaned_data.get('new_password1')
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
            
            else:
                errs = form.error_messages
        #if post the upload image is the involved
        else:
            file = request.FILES['profileup']
            pr = UserProfile.objects.get(user=host)
            pr.profile_pic=media.upload_to_s3(file, 'uploads/profile-pictures')[1]
            pr.save()
            form = PasswordChangeForm(host)
    else:
        form = PasswordChangeForm(host)

    return render(request, 'profile.html', {'form': form,'errs':errs,'host':host})


@login_required(login_url='/accounts/login')
def reports(request):
    return render(request,'reports.html')



@login_required(login_url='/accounts/login')
def signup(request):
    """
    Add a user
    
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.userprofile.mobile = form.cleaned_data.get('mobile')
            user.userprofile.local_password=form.cleaned_data.get('password1')
            user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/accounts/login')
def single_outlet(request,code=None):
    outlet= Outlet.objects.get(code = code)    
    return render(request,'single_outlet.html',{'outlet':outlet})
# @login_required(login_url='/accounts/login')
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.UserProfile.mobile = 123
#     user.save()



# def write_pdf_view(request):
#     doc = SimpleDocTemplate("/tmp/somefilename.pdf")
#     styles = getSampleStyleSheet()
#     Story = [Spacer(1,2*inch)]
#     style = styles["Normal"]
#     for i in range(100):
#        bogustext = ("This is Paragraph number %s.  " % i) * 20
#        p = Paragraph(bogustext, style)
#        Story.append(p)
#        Story.append(Spacer(1,0.2*inch))
#     doc.build(Story)
# 
#     fs = FileSystemStorage("/tmp")
#     with fs.open("somefilename.pdf") as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#         return response
# 
#     return response
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    