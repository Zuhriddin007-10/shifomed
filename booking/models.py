from django.db import models
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    work_start = models.TimeField(default='09:00:00')
    work_end = models.TimeField(default='17:00:00')
    slot_duration = models.IntegerField(default=30)

    def __str__(self):
        return f"Dr. {self.name} - {self.department.name}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    symptoms = models.TextField(blank=True, null=True)
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')

    def __str__(self):
        return f"{self.patient_name} with {self.doctor.name} on {self.date} at {self.time_slot}"
