from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import SchoolForm
# Create your views here.
def create_school_view(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Main:homepage')  # redirect somewhere sensible
    else:
        form = SchoolForm()
    
    return render(request, 'schools/create_school.html', {'form': form})

def school_list_view(request):
    from .models import School
    schools = School.objects.all()
    return render(request, 'schools/school_list.html', {'schools': schools})

def school_detail_view(request, school_name):
    from .models import School
    school = School.objects.get(name=school_name)
    return render(request, 'schools/school_home.html', {'school': school})