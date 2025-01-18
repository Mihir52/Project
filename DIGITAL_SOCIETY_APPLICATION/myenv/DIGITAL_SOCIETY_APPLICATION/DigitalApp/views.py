from django.views.generic import TemplateView,View
from . models import *
from django.shortcuts import render,redirect
import random,string,os

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

class SignupView(TemplateView):
    template_name = "signup.html"

    def sendsignup_email(self, email):
        try : 

            """Send OTP email to the user."""
            subject = "DIGITAL SOCIETY APPLICATION"
            message = "Thank you for signing up....!!!"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
        
        except Exception as e:
            print(e)

    def post(self, request):
        try :
            user = User.objects.get(email = request.POST['email'])
            msg = "Already Registered..!!!!"
            return render(request, self.template_name, {'msg':msg})
        except:
            user = User.objects.create(
                    usertype = request.POST['usertype'],
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['pswd']
                    
            )
            Userprofile.objects.create(
                user = user
            )

            self.sendsignup_email(request.POST['email'])
            msg = "Sign Up Successfully..!!!"
            return render(request, self.template_name, {'s_msg':msg})

    def get(self, request):
        return render(request, self.template_name)
    

class ForgotpasswordView(TemplateView):
    template_name = "forgotpassword.html"

    def generateotp(self):
        otp = ''.join(random.choices(string.digits, k=6)) 
        return otp
    
    def sendotp_email(self, otp, email):
        try : 

            """Send OTP email to the user."""
            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

        except Exception as e:
            print(e)

    
    def post(self,request):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            otp = self.generateotp()

            print(otp)

            request.session['otp'] = otp
            request.session['email'] = email

            self.sendotp_email(otp,email)
            msg = "OTP has been sent to your email. Please check your inbox."
            return render(request, 'verifyotp.html', {'msg':msg})
        
        except:
            msg = "No user found with that email."
            return render(request, self.template_name, {'msg':msg})

    def get(self,request):
        return render(request, self.template_name)
    
class VerifyotpView(TemplateView):
    template_name = "verifyotp.html"
    
    def post(self, request):
        email = request.session['email']
        otp = request.session['otp']
        uotp = request.POST['otp']

        if otp == uotp:
            return redirect('resetpassword')
        else:
            msg="INVALID OTP..!!!"
            return render(request, self.template_name, {'msg':msg})
        
    def get_context_data(self, request):
        return render(request, self.template_name)
        
class ResetpasswordView(TemplateView):
    template_name = "resetpassword.html"

    def post(self,request):
        email = request.session['email']

        if request.POST['pass'] == request.POST['cpass']:
            user = User.objects.get(email=email)
            user.password = request.POST['pass']
            user.save()

            del request.session['otp']
            del request.session['email']
        
            msg = "Your password has been reset successfully."
            return render(request, 'signup.html', {'s_msg':msg})
        else:
            msg = "Passwords Do Not Match."
            return render(request, self.template_name, {'msg':msg})
            

    def get(self, request):
        return render(request, self.template_name)


class LoginView(TemplateView):
    template_name = "signup.html"  

    def post(self, request):
        try:
            user = User.objects.get(email = request.POST['email'])

            if user.password == request.POST['pswd']:
                request.session['email']=user.email

                try:
                    user_profile = Userprofile.objects.get(user=user)
                    if user_profile.profile:
                        request.session['profile'] = user_profile.profile.url
                except:
                    pass 

                return redirect('index')
            else:
                msg = "Invalid Password...."
                return render(request, self.template_name, {'msg': msg})
        except:
            msg = "Email not registered..!!"
            return render(request, self.template_name, {'msg': msg})

    def get(self, request):
        return render(request, self.template_name)


class IndexView(TemplateView): 
    template_name = "index.html" 

    def get(self, request):
        return render(request, self.template_name, {'profile': request.session.get('profile', None)})

class ProfileView(TemplateView): 
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            user = User.objects.get(email=self.request.session['email'])
            user_profile = Userprofile.objects.get(user=user)  
            context["user"] = user
            context["profile"] = user_profile if user_profile.profile else None 
            return context
        except Exception as e:
            print(e)

    def post(self, request):
        user = User.objects.get(email=self.request.session['email'])
        user_profile = Userprofile.objects.get(user=user)

        user_profile.fname = request.POST['fname']
        user_profile.sname = request.POST['sname']
        if request.POST['mobile'] == '0' or request.POST['mobile'] == '':
            user_profile.mobile = user_profile._meta.get_field('mobile').get_default()
        else:
            user_profile.mobile = request.POST['mobile']
        user_profile.address = request.POST['address']
        
        try:
            user_profile.profile = request.FILES['profile_picture']
            request.session['profile'] = user_profile.profile.url
            user_profile.save()
        except:
            pass
        
        user_profile.save()
        user.save()

        return redirect('profile')

class S_membersView(TemplateView): 
    template_name = "s_members.html"

    def get_context_data(self, **kwargs):
        # Fetch all users along with their profiles using select_related
        members = User.objects.all()
        
        # Create a list to store user profiles as context
        member_profiles = []
        for member in members:
            # Use `userprofile_set` to access related profiles
            profile = member.userprofile_set.first()  # Get the first associated profile (if exists)
            member_profiles.append({
                'user': member,
                'profile': profile
            })

        context = super().get_context_data(**kwargs)
        context['members'] = member_profiles  # Add member profiles to context
        return context
    
    def get(self, request, *args, **kwargs):
        # Fetch the context from get_context_data and pass it to render
        context = self.get_context_data(**kwargs)

        # You can also add additional context here if necessary, like profile from session
        context['profile'] = request.session.get('profile', None)

        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user

        # Render the template with the updated context
        return render(request, self.template_name, context)

class S_watchmenView(TemplateView): 
    template_name = "s_watchmen.html"

    def get_context_data(self, **kwargs):
        
        members = User.objects.all()

        member_profiles = []
        for member in members:
            profile = member.userprofile_set.first()  
            member_profiles.append({
                'user': member,
                'profile': profile
            })

        context = super().get_context_data(**kwargs)
        context['members'] = member_profiles  
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['profile'] = request.session.get('profile', None)
        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user
        return render(request, self.template_name, context)
    
class UpdatememberView(TemplateView):
    template_name = "updatemember.html"

    def get_context_data(self, pk, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            user = User.objects.get(pk=pk)
            user_profile = Userprofile.objects.get(user=user)  
            context["member"] = user
            context["memberprofile"] = user_profile if user_profile.profile else None
            print(context) 
            return context
        except Exception as e:
            print(e)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user_profile = Userprofile.objects.get(user=user)

        user_profile.fname = request.POST['fname']
        user_profile.sname = request.POST['sname']
        if request.POST['mobile'] == '0' or request.POST['mobile'] == '':
            user_profile.mobile = user_profile._meta.get_field('mobile').get_default()
        else:
            user_profile.mobile = request.POST['mobile']
        user_profile.address = request.POST['address']
        
        try:
            user_profile.profile = request.FILES['profile_picture']
            user_profile.save()
        except:
            pass
        
        user_profile.save()
        user.save()

        if user.usertype == "member":
            return redirect('s_members')  
        elif user.usertype == "watchman":
            return redirect('s_watchmen') 
        
    def get(self, request, *args, **kwargs):
        
        context = self.get_context_data(**kwargs)
        
        context['profile'] = request.session.get('profile', None)

        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user

        return render(request, self.template_name, context)
    
class DeletememberView(View):

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        userprofile = Userprofile.objects.get(user=user)
        if userprofile and userprofile.profile: 
            if os.path.isfile(userprofile.profile.path): 
                os.remove(userprofile.profile.path)
        user.delete()
        if user.usertype == "member":
            return redirect('s_members')  
        elif user.usertype == "watchman":
            return redirect('s_watchmen') 
    

class NoticeView(TemplateView): 
    template_name = "notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice = Notice.objects.all()
        context['notices'] = notice
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['profile'] = request.session.get('profile', None)

        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user

        return render(request, self.template_name, context)


class CreatenoticeView(TemplateView):
    template_name = "createnotice.html"

    def post(self, request):
        Notice.objects.create(
            noticename = request.POST['noticename'],
            noticedescription = request.POST['noticedescription']
        )
        return redirect('notice') 
    
    def get(self, request):
        return render(request, self.template_name, {'profile': request.session.get('profile', None),'user': User.objects.get(email=request.session['email'])})
    
class UpdatenoticeView(TemplateView):
    template_name = "updatenotice.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        notice = Notice.objects.get(pk=pk)
        
        context['notice'] = notice
        return context
    
    def post(self, request, pk):
        notice = Notice.objects.get(pk=pk)
        notice.noticename = request.POST['noticename']
        notice.noticedescription = request.POST['noticedescription']

        notice.save()
        return redirect('notice')
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['profile'] = request.session.get('profile', None)
        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user
        return render(request, self.template_name, context)
    
class DeletenoticeView(View):

    def get(self, request, pk):

        notice = Notice.objects.get(pk=pk)

        notice.delete()

        return redirect('notice')


class EventView(TemplateView):
    template_name = "event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.all()
        context['events'] = events
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['profile'] = request.session.get('profile', None)
        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user
        return render(request, self.template_name, context)


class CreateeventView(TemplateView):
    template_name = "createevent.html"

    def post(self, request):
        Event.objects.create(
            eventname = request.POST['eventname'],
            eventdescription = request.POST['eventdescription'],
            date = request.POST['date'],
            time = request.POST['time']
        )
        return redirect('event') 
    
    def get(self, request):
        return render(request, self.template_name, {'profile': request.session.get('profile', None), 'user': User.objects.get(email=request.session['email'])})
    
class UpdateeventView(TemplateView):
    template_name = "updateevent.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=pk)
        
        context['event'] = event
        context['date'] = event.date.strftime('%Y-%m-%d')
        context['time'] = event.time.strftime('%H:%M') 
        return context
    
    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.eventname = request.POST['eventname']
        event.eventdescription = request.POST['eventdescription']
        event.date = request.POST['date']
        event.time = request.POST['time']

        event.save()
        return redirect('event')
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['profile'] = request.session.get('profile', None)
        user = User.objects.get(email=self.request.session['email'])
        context['user'] = user

        return render(request, self.template_name, context)

class DeleteeventView(View):

    def get(self, request, pk):

        event = Event.objects.get(pk=pk)

        event.delete()

        return redirect('event')

class ChangepasswordView(TemplateView):
    template_name = "changepassword.html"

    def post(self, request):
        email = request.session['email']
        user = User.objects.get(email=email)
        print(user)
        if request.POST['oldpass'] == user.password:
            if request.POST['newpass'] == request.POST['cpass']:
                user.password = request.POST['newpass']
                user.save()

                del request.session['email']
            
                msg = "Your password has been Change successfully."
                return render(request, 'signup.html', {'s_msg':msg})
            else:
                msg = "Passwords Do Not Match."
                return render(request, self.template_name, {'msg':msg})
        else:
            msg = "Incorrect old Password..!!"
            return render(request, self.template_name, {'msg':msg})
            
    def get(self, request):
        return render(request, self.template_name)


class SignoutView(TemplateView):
     def get(self, request, *args, **kwargs):
        if 'profile' in request.session:
            del request.session['profile']
        del request.session['email']  
        return redirect('login') 
     
class DeleteuseraccountView(View):
    def get(self, request):

        user = User.objects.get(email=request.session['email'])

        userprofile = Userprofile.objects.get(user=user)
        if userprofile and userprofile.profile: 
            if os.path.isfile(userprofile.profile.path): 
                os.remove(userprofile.profile.path)
        user.delete()

        return redirect('signup')