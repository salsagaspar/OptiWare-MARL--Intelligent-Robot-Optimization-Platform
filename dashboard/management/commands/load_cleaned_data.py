import os
import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import Robot, Zone, MaintenanceLog, TaskAssignment, SensorReading

class Command(BaseCommand):
    help = 'Load cleaned data CSV files into SQLite database'

    def handle(self, *args, **options):
        self.stdout.write("Starting to load cleaned data...")

        # 1. Load Zones
        self.stdout.write("Loading Zones...")
        df_zones = pd.read_csv('cleaned_data/ds3_warehouse_zones_dim.csv')
        df_zones['zone_id'] = df_zones['zone_id'].astype(str)
        df_zones = df_zones.drop_duplicates(subset=['zone_id'])
        zones_to_create = []
        for _, row in df_zones.iterrows():
            zones_to_create.append(Zone(
                zone_id=row['zone_id'],
                zone_name=row['zone_name'],
                zone_type=row['zone_type'],
                area_sqm=row['area_sqm'],
                capacity_units=row['capacity_units'],
                current_occupancy_pct=row['current_occupancy_pct'],
                zone_status=row['zone_status']
            ))
        Zone.objects.all().delete()
        Zone.objects.bulk_create(zones_to_create)
        self.stdout.write(f"Loaded {len(zones_to_create)} zones.")

        # 2. Load Robots
        self.stdout.write("Loading Robots...")
        df_robots = pd.read_csv('cleaned_data/ds1_robots_dim.csv')
        df_robots['robot_id'] = df_robots['robot_id'].astype(str)
        df_robots = df_robots.drop_duplicates(subset=['robot_id'])
        robots_to_create = []
        for _, row in df_robots.iterrows():
            robots_to_create.append(Robot(
                robot_id=row['robot_id'],
                serial_number=row['serial_number'],
                model=row['model'],
                manufacturer=row['manufacturer'],
                robot_type=row['robot_type'],
                manufacture_date=pd.to_datetime(row['manufacture_date']).date() if pd.notnull(row['manufacture_date']) else None,
                installation_date=pd.to_datetime(row['installation_date']).date() if pd.notnull(row['installation_date']) else None,
                operational_status=row['operational_status'],
                max_payload_kg=row['max_payload_kg'],
                max_speed_mps=row['max_speed_mps'],
                battery_capacity_wh=row['battery_capacity_wh'],
                total_operational_hours=row['total_operational_hours']
            ))
        Robot.objects.all().delete()
        Robot.objects.bulk_create(robots_to_create)
        self.stdout.write(f"Loaded {len(robots_to_create)} robots.")

        # Get valid IDs as strings
        valid_robot_ids = set(Robot.objects.values_list('robot_id', flat=True))
        valid_zone_ids = set(Zone.objects.values_list('zone_id', flat=True))

        # 3. Load Maintenance Logs
        self.stdout.write("Loading Maintenance Logs...")
        df_maint = pd.read_csv('cleaned_data/ds2_maintenance_logs_fact.csv')
        df_maint['robot_id'] = df_maint['robot_id'].astype(str)
        df_maint = df_maint[df_maint['robot_id'].isin(valid_robot_ids)]
        df_maint = df_maint.drop_duplicates(subset=['log_id'])
        
        maint_to_create = []
        for _, row in df_maint.iterrows():
            maint_to_create.append(MaintenanceLog(
                log_id=row['log_id'],
                robot_id=row['robot_id'],
                technician_id=row['technician_id'],
                maintenance_date=pd.to_datetime(row['maintenance_date']).date() if pd.notnull(row['maintenance_date']) else None,
                maintenance_type=row['maintenance_type'],
                duration_hours=row['duration_hours'],
                parts_replaced=row['parts_replaced'] if pd.notnull(row['parts_replaced']) else "",
                total_cost_usd=row['total_cost_usd'],
                downtime_hours=row['downtime_hours'],
                completion_status=row['completion_status'],
                recurrence_count=row['recurrence_count'],
                inspection_passed=row['inspection_passed']
            ))
        MaintenanceLog.objects.all().delete()
        MaintenanceLog.objects.bulk_create(maint_to_create)
        self.stdout.write(f"Loaded {len(maint_to_create)} maintenance logs.")

        # 4. Load Task Assignments (Limit to 5000 rows to speed up and keep database lightweight)
        self.stdout.write("Loading Task Assignments (Subset)...")
        df_tasks = pd.read_csv('cleaned_data/ds3_task_assignments_fact.csv', nrows=10000)
        df_tasks['robot_id'] = df_tasks['robot_id'].astype(str)
        df_tasks['zone_id'] = df_tasks['zone_id'].astype(str)
        df_tasks = df_tasks[df_tasks['robot_id'].isin(valid_robot_ids) & df_tasks['zone_id'].isin(valid_zone_ids)]
        df_tasks = df_tasks.drop_duplicates(subset=['task_id'])
        # Limit to 5000 rows after filtering
        df_tasks = df_tasks.head(5000)
        
        tasks_to_create = []
        for _, row in df_tasks.iterrows():
            tasks_to_create.append(TaskAssignment(
                task_id=row['task_id'],
                robot_id=row['robot_id'],
                zone_id=row['zone_id'],
                assigned_at=pd.to_datetime(row['assigned_at']) if pd.notnull(row['assigned_at']) else None,
                started_at=pd.to_datetime(row['started_at']) if pd.notnull(row['started_at']) else None,
                completed_at=pd.to_datetime(row['completed_at']) if pd.notnull(row['completed_at']) else None,
                task_type=row['task_type'],
                priority=row['priority'],
                status=row['status'],
                items_count=row['items_count'],
                distance_m=row['distance_m'],
                time_taken_min=row['time_taken_min']
            ))
        TaskAssignment.objects.all().delete()
        TaskAssignment.objects.bulk_create(tasks_to_create)
        self.stdout.write(f"Loaded {len(tasks_to_create)} task assignments.")

        # 5. Load Sensor Readings (Limit to 5000 rows)
        self.stdout.write("Loading Sensor Readings (Subset)...")
        df_readings = pd.read_csv('cleaned_data/ds5_sensor_readings_fact.csv', nrows=10000)
        df_readings['robot_id'] = df_readings['robot_id'].astype(str)
        df_readings['zone_id'] = df_readings['zone_id'].astype(str)
        df_readings = df_readings[df_readings['robot_id'].isin(valid_robot_ids) & df_readings['zone_id'].isin(valid_zone_ids)]
        df_readings = df_readings.drop_duplicates(subset=['reading_id'])
        df_readings = df_readings.head(5000)
        
        readings_to_create = []
        for _, row in df_readings.iterrows():
            readings_to_create.append(SensorReading(
                reading_id=row['reading_id'],
                sensor_id=row['sensor_id'],
                robot_id=row['robot_id'],
                timestamp=pd.to_datetime(row['timestamp']) if pd.notnull(row['timestamp']) else None,
                reading_type=row['reading_type'],
                value=row['value'],
                unit=row['unit'],
                alert_triggered=row['alert_triggered'],
                alert_level=row['alert_level'] if pd.notnull(row['alert_level']) else None,
                zone_id=row['zone_id']
            ))
        SensorReading.objects.all().delete()
        SensorReading.objects.bulk_create(readings_to_create)
        self.stdout.write(f"Loaded {len(readings_to_create)} sensor readings.")

        self.stdout.write(self.style.SUCCESS("All cleaned data loaded successfully!"))
