from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('icon', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctors/')),
                ('work_start', models.TimeField(default='09:00:00')),
                ('work_end', models.TimeField(default='17:00:00')),
                ('slot_duration', models.IntegerField(default=30)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='booking.department')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('time_slot', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='booking.doctor')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('doctor', 'date', 'time_slot')},
        ),
    ]
