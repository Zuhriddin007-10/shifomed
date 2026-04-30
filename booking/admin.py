from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Doctor, Appointment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'doctor_count', 'description')
    search_fields = ('name',)

    def doctor_count(self, obj):
        count = obj.doctors.count()
        return format_html('<b style="color:#1D9E75">{}</b> ta shifokor', count)
    doctor_count.short_description = "Shifokorlar soni"


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'work_start', 'work_end', 'slot_duration')
    list_filter = ('department',)
    search_fields = ('name', 'bio')

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('name', 'department', 'bio', 'image')
        }),
        ('Ish vaqti', {
            'fields': ('work_start', 'work_end', 'slot_duration')
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone_number', 'doctor', 'date', 'time_slot', 'colored_status', 'created_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient_name', 'phone_number', 'doctor__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    ordering = ('-date', 'time_slot')

    def colored_status(self, obj):
        colors = {
            'pending': '#FFA500',
            'confirmed': '#1D9E75',
            'cancelled': '#E74C3C',
        }
        labels = {
            'pending': 'Kutmoqda',
            'confirmed': 'Tasdiqlangan',
            'cancelled': 'Bekor qilingan',
        }
        color = colors.get(obj.status, '#999')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:12px">{}</span>',
            color, label
        )
    colored_status.short_description = "Holat"


admin.site.site_header = "ShifoMed Boshqaruv Paneli"
admin.site.site_title = "ShifoMed Admin"
admin.site.index_title = "Xush kelibsiz, ShifoMed!"
