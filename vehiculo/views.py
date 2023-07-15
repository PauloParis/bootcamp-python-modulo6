from django.shortcuts import render, redirect, get_object_or_404
from vehiculo.forms import VehiculoForm, RegisterUserForm

from vehiculo.models import VehiculosModel
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    if not request.user.has_perm('vehiculo.visualizar_catalogo'):
        return redirect('agregar')
    return render(request, 'index.html', {})



@login_required(login_url='/login/')
def agregar(request):
    if request.user.has_perm('vehiculo.add_vehiculosmodel'):
        if request.method == 'POST':
            formaVehiculo = VehiculoForm(request.POST)
            if formaVehiculo.is_valid():
                formaVehiculo.save()
                return redirect('listar')
        else:
            formaVehiculo = VehiculoForm()
        return render(request, 'add.html', {'formaVehiculo': formaVehiculo})
    return redirect('inicio')


@login_required(login_url='/login/')
def listar(request):
    if request.user.has_perm('vehiculo.visualizar_catalogo'):
        vehiculos = VehiculosModel.objects.order_by('id')
        for item in vehiculos:
            item.condicion = condiciones(item.precio)
        return render(request, 'list.html', {'vehiculos': vehiculos})
    else:
        return redirect('inicio')


def condiciones(precio):
     return 'Bajo' if precio <= 10000 else 'Medio' if precio <= 30000 else 'Alto'


@login_required(login_url='/login/')
def editar(request, id):
    if request.user.has_perm('vehiculo.visualizar_catalogo'):
        vehiculo = get_object_or_404(VehiculosModel, pk=id)
        if request.method == 'POST':
            formaVehiculo = VehiculoForm(request.POST, instance=vehiculo)
            if formaVehiculo.is_valid():
                formaVehiculo.save()
                return redirect('listar')
        else:
            formaVehiculo = VehiculoForm(instance=vehiculo)
        return render(request, 'edit.html', {'formaVehiculo': formaVehiculo})
    else:
        return redirect('inicio')


@login_required(login_url='/login/')
def eliminar(request, id):
    if request.user.has_perm('vehiculo.visualizar_catalogo'):
        vehiculo = get_object_or_404(VehiculosModel, pk=id)
        if vehiculo:
            vehiculo.delete()
        return redirect('listar')
    else:
        return redirect('inicio')



def register(request):
    if request.method == 'POST':
        formaUsuario = RegisterUserForm(request.POST)
        print(formaUsuario)
        if formaUsuario.is_valid():
            content_type = ContentType.objects.get_for_model(VehiculosModel)
            visualizar_catalogo = Permission.objects.get(codename='visualizar_catalogo', content_type=content_type)
            user = formaUsuario.save()
            user.user_permissions.add(visualizar_catalogo)
            messages.success(request, 'Registro Exitoso')
            return redirect('login')
        else:
            messages.error(request, 'Error registro, datos inválidos paso el post')
    formaUsuario = RegisterUserForm()
    context = {'register_form': formaUsuario}
    return render(request, 'login.html', context)



def login_View(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Iniciaste sesión como: {username}')
                return redirect('/')
            else:
                messages.error(request, 'Error de inicio de sesión, datos inválidos')
        else:
            messages.error(request, 'Error de inicio de sesión, datos inválidos')

    form = AuthenticationForm()
    context = {'login_form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'Se ha cerrado la sesión correctamente')
    return redirect('login')