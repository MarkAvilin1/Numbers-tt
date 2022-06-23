from sql_process.sql_processing import SQLProcessing
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order

sp = SQLProcessing()
sheet = sp.sheet
check = sp.check_equality()
idx = sp.data_getter().shape[0]


def home(request):
    if not check:
        sp.delete_all()
        sp.data_input()

    orders = Order.objects.all().order_by('id')
    paginator = Paginator(orders, per_page=4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders': page_obj
    }
    return render(request, 'home.html', context)


def create(request):
    form = OrderForm()
    rate = sp.get_currency_rate()
    pk = idx + 1
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_num = form.cleaned_data.get('order_num')
            price_usd = form.cleaned_data.get('price_usd')
            price_rub = form.cleaned_data.get('price_rub')
            delivery_time = form.cleaned_data.get('delivery_time')
            data4sheet = [pk, order_num, price_usd, delivery_time]
            data4table = Order(id=pk, order_num=order_num, price_usd=price_usd, price_rub=price_rub,
                               delivery_time=delivery_time)
            sp.sheet.insert_row(data4sheet, pk + 1)
            data4table.save()
            return redirect('/')
    context = {
        'form': form,
        'rate': rate,
    }
    return render(request, 'create.html', context)


def update(request, pk):
    data = Order.objects.get(id=pk)
    form = OrderForm(instance=data)
    rate = sp.get_currency_rate()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=data)
        if form.is_valid():
            order_num = form.cleaned_data.get('order_num')
            price_usd = form.cleaned_data.get('price_usd')
            delivery_time = form.cleaned_data.get('delivery_time')
            all_data = [pk, order_num, price_usd, delivery_time]
            sp.sheet.delete_row(pk + 1)
            sp.sheet.insert_row(all_data, pk + 1)
            form.save()
            return redirect('/')
    context = {
        'data': data,
        'form': form,
        'rate': rate,
    }
    return render(request, 'update.html', context)


def delete(request, pk):
    data = Order.objects.get(id=pk)
    if request.method == 'POST':
        sp.sheet.delete_row(pk + 1)
        data.delete()
        return redirect('/')
    context = {
        'data': data
    }
    return render(request, 'delete.html', context)
