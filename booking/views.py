from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Department, Doctor, Appointment
from datetime import datetime, timedelta, date

def home(request):
    departments = Department.objects.all()
    top_doctors = Doctor.objects.all()[:4]
    return render(request, 'booking/home.html', {
        'departments': departments,
        'top_doctors': top_doctors
    })

def doctor_list(request):
    department_id = request.GET.get('department')
    if department_id:
        doctors = Doctor.objects.filter(department_id=department_id)
    else:
        doctors = Doctor.objects.all()
    return render(request, 'booking/doctor_list.html', {'doctors': doctors})

def generate_time_slots(start_time, end_time, duration):
    slots = []
    current_time = datetime.combine(date.today(), start_time)
    end_dt = datetime.combine(date.today(), end_time)
    while current_time + timedelta(minutes=duration) <= end_dt:
        slots.append(current_time.time())
        current_time += timedelta(minutes=duration)
    return slots

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    selected_date_str = request.GET.get('date', date.today().isoformat())
    try:
        selected_date = date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = date.today()

    if selected_date < date.today():
        selected_date = date.today()

    all_slots = generate_time_slots(doctor.work_start, doctor.work_end, doctor.slot_duration)
    booked_appointments = Appointment.objects.filter(doctor=doctor, date=selected_date)
    booked_times = [appt.time_slot for appt in booked_appointments]

    available_slots = []
    for slot in all_slots:
        is_past = False
        if selected_date == date.today():
            if slot < timezone.now().time():
                is_past = True
        if not is_past and slot not in booked_times:
            available_slots.append(slot)

    dates_list = [(date.today() + timedelta(days=i)) for i in range(14)]

    return render(request, 'booking/doctor_detail.html', {
        'doctor': doctor,
        'selected_date': selected_date,
        'dates_list': dates_list,
        'available_slots': available_slots
    })

def book_appointment(request, doctor_id):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        selected_date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        symptoms = request.POST.get('symptoms', '')

        if not all([selected_date, time_slot, patient_name, phone_number]):
            return redirect(f"/doctor/{doctor_id}/?error=Missing+fields")

        try:
            Appointment.objects.create(
                doctor=doctor,
                patient_name=patient_name,
                phone_number=phone_number,
                symptoms=symptoms,
                date=selected_date,
                time_slot=time_slot
            )
            return redirect('booking_success')
        except Exception as e:
            return redirect(f"/doctor/{doctor_id}/?error=Slot+already+booked")

    return redirect('home')

def booking_success(request):
    return render(request, 'booking/success.html')
