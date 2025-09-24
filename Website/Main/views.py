from django.shortcuts import render, redirect

def homepage(request):
    if request.user.is_authenticated:
        if request.user.school:
            # Redirect or render the user's school homepage
            return render(request, 'schools/school_home.html', {'school': request.user.school})
        else:
            # User is logged in but has no school assigned
            return render(request, 'Main/homepage.html', {'message': 'You are not assigned to a school yet.'})
    else:
        return render(request, 'Main/homepage.html')
def site_home(request):
    return render(request, 'Main/homepage.html')