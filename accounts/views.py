# render : will load a html page
# redirect : will redirect the user to specify html pages based on completed activity
from django.shortcuts import render, redirect

# django inbuilt auth functions that return true or false based on the process
# login rerturns True if user is currently logged in 
#logout returns True if the user successfully logs out
# authenticate returns True if the user provides correct credentials for a login process
from django.contrib.auth import login, logout, authenticate

# returns True or false if the user is logged in or not and allow execution of a function based on that result
from django.contrib.auth.decorators import login_required

# message alerts : notifications
from django.contrib import messages

#require the configured form views for the password reset process
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

# only load views when required : reverse_lazy
from django.urls import reverse_lazy

#import form files from your apps forms.py
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm

# Create your views here.
## registration / sign_ups
def register_view(request):
    #check if user is already logged in
    # django always maintains our user object
    if request.user.is_authenticated:
        #if  user is already authenticated take them to dashboard
        return redirect('media_assets:dashboard')
    
    # check the type of request method
    # when submitting the form the request is POST
    # when viewing tha form the request is default GET
    if request.method == 'POST':
        #create the form reference for registration from forms.py
        form = UserRegistrationForm(request.POST)
        # if all form inputs are filled we then save details to the db
        # form.is_valid checks if all the form fields are filled correctly
        if form.is_valid():
            user = form.save() ## save() submits details to our db
            login(request,user) ## saving  our login state for the use 
            messages.success(request, f'welcome {user.username} Your account has been created')

            # redirect user to our dashboard
            return redirect('media_assets:dashboard')
    else: 
        form = UserRegistrationForm()# default get process
    
    return render(request, 'accounts/register.html', {'form': form})

## login / sign_in
def login_view(request):
    #check if user is already logged in
    if request.user.is_authenticated:
        return redirect('media_assets:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        # check if the fields are filled correctly
        if form.is_valid():
            # pic up our username and password from the form
            username = form.cleaned_data.get('username') # cleaned_data is a dictionary of the form data that has been validated and cleaned by the form's validation process.
            password = form.cleaned_data.get('password')
            # use method authenticate to check if the provided credentials are correct
            user = authenticate(request, username=username, password=password) # authenticate checks if the provided credentials are correct and returns a user object if they are valid, or None if they are not.
            if user is not None:
                login(request, user) # login function takes the request object and the authenticated user object as arguments and logs the user in by creating a session for them.
                messages.success(request, f'welcome back {user.username} You have successfully logged in')
                return redirect('media_assets:dashboard')

    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html',{'form': form})

## logout / sign_out
@login_required # this decorator ensures that only authenticated users can access the logout view. If an unauthenticated user tries to access this view, they will be redirected to the login page.
# decorator returns true i.e. only if the user is logged in
def logout_view(request):
    logout(request) # logout function takes the request object as an argument and logs the user out by clearing their session data. 
    messages.info(request, f'You have successfully logged out.')
    return redirect('accounts:login')

# user profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        # request.Post picks up text data
        # request.FILES picks up file/media data
        # instance=request.user ensures that we are updating the current user's profile
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save() #updates the user profile
            messages.success(request, f"Your profile has been updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts:profile.html', {'form': form})

# view for password reset
# django provides inbuilt views for password reset process but we can also customise them to fit our needs
class CustomPasswordResetView(PasswordResetView):
    # interface change for password reset form
    template_name = 'accounts/password_reset.html' # specify the template for password reset form
    email_template_name = 'accounts/password_reset_email.html' # specify the template for the password reset email
    success_url = reverse_lazy('accounts:password_reset_done') # specify the url to redirect to after successful password reset request 

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html' # specify the template for password reset confirmation form
    success_url = reverse_lazy('accounts:password_reset_complete') # specify the url to redirect to after successful password reset confirmation 
