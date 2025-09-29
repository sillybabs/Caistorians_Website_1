from .forms import SchoolForm, HistoricalImageFormSet, AlumniHighlightFormSet
from django.shortcuts import render, redirect
from .models import School

# Create your views here.
def create_school_view(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        historical_formset = HistoricalImageFormSet(request.POST, request.FILES, queryset=School.objects.none())
        alumni_formset = AlumniHighlightFormSet(request.POST, request.FILES, queryset=School.objects.none())

        if form.is_valid() and historical_formset.is_valid() and alumni_formset.is_valid():
            school = form.save()

            # Save historical images
            for hform in historical_formset:
                if hform.cleaned_data and not hform.cleaned_data.get('DELETE', False):
                    hist = hform.save(commit=False)
                    hist.school = school
                    hist.save()

            # Save alumni highlights
            for aform in alumni_formset:
                if aform.cleaned_data and not aform.cleaned_data.get('DELETE', False):
                    alum = aform.save(commit=False)
                    alum.school = school
                    alum.save()

            return redirect('Main:homepage')

    else:
        form = SchoolForm()
        historical_formset = HistoricalImageFormSet(queryset=School.objects.none())
        alumni_formset = AlumniHighlightFormSet(queryset=School.objects.none())

    return render(request, 'schools/create_school.html', {
        'form': form,
        'historical_formset': historical_formset,
        'alumni_formset': alumni_formset,
    })

def school_list_view(request):
    from .models import School
    schools = School.objects.all()
    return render(request, 'schools/school_list.html', {'schools': schools})

def school_detail_view(request, school_name):
    from .models import School
    school = School.objects.get(name=school_name)
    return render(request, 'schools/school_home.html', {'school': school})



from django.shortcuts import get_object_or_404, render, redirect
from .models import School
from .forms import EditSchoolForm, HistoricalImageFormSet, AlumniHighlightFormSet

def edit_school_view(request, school_id):
    school = get_object_or_404(School, id=school_id)

    if request.method == "POST":
        form = EditSchoolForm(request.POST, request.FILES, instance=school)
        historical_formset = HistoricalImageFormSet(request.POST, request.FILES, instance=school)
        alumni_formset = AlumniHighlightFormSet(request.POST, request.FILES, instance=school)

        if form.is_valid() and historical_formset.is_valid() and alumni_formset.is_valid():
            form.save()
            historical_formset.save()
            alumni_formset.save()
            return redirect('Main:homepage')  # or school detail page
    else:
        form = EditSchoolForm(instance=school)
        historical_formset = HistoricalImageFormSet(instance=school)
        alumni_formset = AlumniHighlightFormSet(instance=school)

    context = {
        'form': form,
        'historical_formset': historical_formset,
        'alumni_formset': alumni_formset,
        'school': school
    }
    return render(request, 'schools/edit_school.html', context)
