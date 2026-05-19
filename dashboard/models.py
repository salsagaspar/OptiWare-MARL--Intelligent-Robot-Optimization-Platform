from django.db import models

class Zone(models.Model):
    zone_id = models.CharField(max_length=50, primary_key=True)
    zone_name = models.CharField(max_length=100)
    zone_type = models.CharField(max_length=100)
    area_sqm = models.FloatField(null=True, blank=True)
    capacity_units = models.IntegerField(null=True, blank=True)
    current_occupancy_pct = models.FloatField(null=True, blank=True)
    zone_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.zone_name} ({self.zone_id})"

class Robot(models.Model):
    robot_id = models.CharField(max_length=50, primary_key=True)
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    robot_type = models.CharField(max_length=100)
    manufacture_date = models.DateField(null=True, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    operational_status = models.CharField(max_length=50)
    max_payload_kg = models.FloatField(null=True, blank=True)
    max_speed_mps = models.FloatField(null=True, blank=True)
    battery_capacity_wh = models.FloatField(null=True, blank=True)
    total_operational_hours = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.model} - {self.robot_id}"

class MaintenanceLog(models.Model):
    log_id = models.CharField(max_length=50, primary_key=True)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='maintenance_logs')
    technician_id = models.CharField(max_length=50)
    maintenance_date = models.DateField(null=True, blank=True)
    maintenance_type = models.CharField(max_length=50)
    duration_hours = models.FloatField(null=True, blank=True)
    parts_replaced = models.TextField(null=True, blank=True)
    total_cost_usd = models.FloatField(null=True, blank=True)
    downtime_hours = models.FloatField(null=True, blank=True)
    completion_status = models.CharField(max_length=50)
    recurrence_count = models.IntegerField(default=0)
    inspection_passed = models.IntegerField(default=1)

    def __str__(self):
        return f"Log {self.log_id} - Robot {self.robot_id}"

class TaskAssignment(models.Model):
    task_id = models.CharField(max_length=50, primary_key=True)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='tasks')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='tasks')
    assigned_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=100)
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    items_count = models.IntegerField(null=True, blank=True)
    distance_m = models.FloatField(null=True, blank=True)
    time_taken_min = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Task {self.task_id} - Robot {self.robot_id}"

class SensorReading(models.Model):
    reading_id = models.CharField(max_length=50, primary_key=True)
    sensor_id = models.CharField(max_length=50)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, related_name='sensor_readings')
    timestamp = models.DateTimeField(null=True, blank=True)
    reading_type = models.CharField(max_length=50)
    value = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20)
    alert_triggered = models.IntegerField(default=0)
    alert_level = models.CharField(max_length=50, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='sensor_readings')

    def __str__(self):
        return f"Reading {self.reading_id} - Sensor {self.sensor_id}"
