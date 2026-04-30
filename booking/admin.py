from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Doctor, Appointment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'description')
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'work_start', 'work_end', 'slot_duration')
    list_filter = ('department',)
    search_fields = ('name',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone_number', 'doctor', 'date', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient_name', 'phone_number')
    readonly_fields = ('created_at',)


admin.site.site_header = "ShifoMed Boshqaruv Paneli"
admin.site.site_title = "ShifoMed Admin"
admin.site.index_title = "Xush kelibsiz, ShifoMed!"
