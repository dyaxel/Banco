from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ClienteForm, CuentaForm, TransaccionForm, TransferenciaForm, FiltrarForm
from Administracion.models import Cliente, Cuenta, Transaccion
from decimal import Decimal
from django.contrib import messages


def registrar_cliente(request):

    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_clientes')

    return render(request, 'registro_clientes.html', {'form': form})


def registrar_cuenta(request):

    form = CuentaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_cuentas')

    return render(request, 'registro_cuentas.html', {'form': form})


def registrar_transaccion(request):

    form = TransaccionForm(request.POST or None)

    if form.is_valid():
        form.save()
        
        info = form.cleaned_data
        trans = Cuenta.objects.get(numero_cuenta=info['cuenta'])
        
        

        if info['tipo'] == 'retiro':
            retirar = Cuenta.objects.get(numero_cuenta=trans)
            retirar.saldo = retirar.saldo - Decimal(info['monto'])
            retirar.save()
        else:
            depositar = Cuenta.objects.get(numero_cuenta=trans)
            depositar.saldo = depositar.saldo + Decimal(info['monto'])
            depositar.save()
        
        messages.success(request,"Transacción Exitosa")
        return redirect('registrar_transaccion')
    
    else:
        return render(request, 'registro_transaccion.html', {'form':form})

    #if form.is_valid():
     #   form.save()
      #  return redirect('registrar_transaccion')

    #return render(request, 'registro_transaccion.html', {'form': form})

def consultas(request):
    return render(request, 'consultas.html')


def ver_clientes(request):
    
    lista_clientes = Cliente.objects.all().order_by('dpi')
    
    return render(request, 'clientes.html',{'clientes':lista_clientes})

def ver_cuentas(request, cliente_dpi):
    
    cuentas = Cuenta.objects.filter(cliente=cliente_dpi)
    
    return render(request, 'cuentas.html',{'cuentas':cuentas})


def realizar_transferencia(request):
    
    
    form = TransferenciaForm(request.POST or None)


    if form.is_valid():
        info = form.cleaned_data
        retirar = Cuenta.objects.get(numero_cuenta=info['de_cuenta'])
        depositar = Cuenta.objects.get(numero_cuenta=info['a_cuenta'])

        retiro = Transaccion.objects.create(
                cuenta = retirar,
                tipo = "retiro",
                monto = info["monto"],
                descripcion = info["descripcion"]
            )
        
        deposito = Transaccion.objects.create(
                cuenta = depositar,
                tipo = "deposito",
                monto = info["monto"],
                descripcion = info["descripcion"]
        )
        
        retirar.saldo = retirar.saldo - Decimal(info['monto'])
        retirar.save()

        depositar.saldo = depositar.saldo + Decimal(info['monto'])
        depositar.save()
        
        messages.success(request,"Transacción Exitosa")
        return redirect('realizar_transferencia')
    
    else:
        return render(request, 'transferencias.html', {'form':form})
    
def ver_transacciones(request, cuenta_numero_cuenta):
    
    transferencias = Transaccion.objects.filter(cuenta=cuenta_numero_cuenta)
    
    return render(request, 'ver_transferencias.html',{'transferencias':transferencias,'numero_cuenta':cuenta_numero_cuenta})

def filtrar_fecha(request, numero_cuenta):
    
    fecha_buscar = request.GET["dato"]
    fecha = Transaccion.objects.filter(fecha__date=fecha_buscar,cuenta=numero_cuenta)
    return render(request, 'ver_transferencias.html',{'transferencias':fecha,'numero_cuenta':numero_cuenta})
    
    #fecha = Transaccion.objects.filter(fecha=tr_fecha)
    
    #return redirect('ver_transacciones', {'transferencias':fecha})