from django.shortcuts import render, redirect
from .models import Table, MenuItem, Reservation
from .forms import ReservationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

def home(request):
    menu = MenuItem.objects.all()[:2]
    return render(request, 'booking/home.html', {'menu': menu})

def menu_selection(request):
    menu = MenuItem.objects.all()
    if request.method == 'POST':
        selected = request.POST.getlist('menu_items')
        if not selected:
            messages.warning(request, "Please select at least one menu item.")
            return redirect('menu_selection')
        # Collect quantities for each selected item
        quantities = {}
        for item_id in selected:
            qty = request.POST.get(f'quantity_{item_id}', '1')
            try:
                qty = int(qty)
            except ValueError:
                qty = 1
            quantities[item_id] = qty
        request.session['menu_items'] = selected
        request.session['menu_quantities'] = quantities
        return redirect('reservation_form')
    return render(request, 'booking/menu_selection.html', {'menu': menu})

def reservation_form(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Convert date and time to string for session serialization
            data = form.cleaned_data.copy()
            if 'date' in data:
                data['date'] = data['date'].isoformat()
            if 'time' in data:
                data['time'] = data['time'].isoformat()
            request.session['reservation_data'] = data
            return redirect('reservation_preview')
    else:
        form = ReservationForm()

    return render(request, 'booking/reservation_form.html', {'form': form})


def reservation_preview(request):
    reservation_data = request.session.get('reservation_data')
    selected_menu = request.session.get('menu_items', [])
    menu_quantities = request.session.get('menu_quantities', {})

    if not reservation_data:
        messages.error(request, "No reservation data found. Please fill the reservation form first.")
        return redirect('reservation_form')

    # Convert date and time back to Python objects for the form
    import datetime
    data = reservation_data.copy()
    if 'date' in data:
        data['date'] = datetime.date.fromisoformat(data['date'])
    if 'time' in data:
        data['time'] = datetime.time.fromisoformat(data['time'])

    menu_items = MenuItem.objects.filter(pk__in=selected_menu)
    # Attach quantity to each menu item for display
    menu_items_with_qty = []
    for item in menu_items:
        qty = menu_quantities.get(str(item.pk), 1)
        menu_items_with_qty.append({'item': item, 'quantity': qty})

    if request.method == 'POST':
        form = ReservationForm(data)
        if form.is_valid():
            reservation = form.save(commit=False)

            # Always assign or create a table for every booking (ignore capacity)
            table = Table.objects.first()
            if not table:
                table = Table.objects.create(number="1", capacity=10)
            reservation.table = table
            reservation.save()

            for item in menu_items:
                reservation.menu_items.add(item)

            # Send confirmation email
            try:
                send_mail(
                    'Table Booked!',
                    f'Dear {reservation.name}, your table has been successfully booked.',
                    settings.EMAIL_HOST_USER,
                    [reservation.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, "Reservation saved but email could not be sent.")

            # Clear session data after booking
            request.session.pop('reservation_data', None)
            request.session.pop('menu_items', None)

            return redirect('success')
        else:
            messages.error(request, "There was an error with your reservation data.")
            return redirect('reservation_form')

    return render(request, 'booking/preview.html', {
        'reservation': data,
        'menu_items': menu_items_with_qty,
    })


def booking_success(request):
    return render(request, 'booking/success.html')
