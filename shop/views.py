from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Medicine
from shop.forms import MedicineForm


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

@login_required
def edit_medicine(request, medicine_id):
    medicine = Medicine.objects.get(id=medicine_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'edit_medicine.html', {'form': form})

@login_required
def delete_medicine(request, medicine_id):
    medicine = Medicine.objects.get(id=medicine_id)
    medicine.delete()
    return redirect('medicine_list')

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    print(medicines)
    return render(request, 'medicine_list.html', {'medicines': medicines})

@login_required
def search_medicine(request):
    query = request.GET.get('p')
    medicines = Medicine.objects.filter( name__icontains=query)
    return render(request, 'medicine_list.html', {'medicines': medicines,'query':query})



from django.shortcuts import render, redirect
from django.contrib.auth import  login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('medicine_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')