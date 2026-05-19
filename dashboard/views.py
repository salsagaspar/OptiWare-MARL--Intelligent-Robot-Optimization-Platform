from django.shortcuts import render
from django.http import JsonResponse
from django.db import models
from django.db.models import Sum, Avg, Count
from django.views.decorators.csrf import csrf_exempt
from .models import Robot, Zone, MaintenanceLog, TaskAssignment, SensorReading
import json

def dashboard_home(request):
    # Summary Metrics
    total_robots = Robot.objects.count()
    active_robots = Robot.objects.filter(operational_status='Active').count()
    idle_robots = Robot.objects.filter(operational_status='Idle').count()
    maintenance_robots = Robot.objects.filter(operational_status='Maintenance').count()
    
    total_maint_cost = MaintenanceLog.objects.aggregate(total=Sum('total_cost_usd'))['total'] or 0.0
    total_downtime = MaintenanceLog.objects.aggregate(total=Sum('downtime_hours'))['total'] or 0.0
    total_tasks = TaskAssignment.objects.count()
    
    # Alert sensor counts
    total_alerts = SensorReading.objects.filter(alert_triggered=1).count()
    recent_alerts = SensorReading.objects.filter(alert_triggered=1).order_by('-timestamp')[:5]

    # Lists
    top_robots = Robot.objects.order_by('-total_operational_hours')[:5]
    top_zones = Zone.objects.order_by('-current_occupancy_pct')[:5]
    
    # Recent maintenance logs
    recent_maint = MaintenanceLog.objects.order_by('-maintenance_date')[:5]

    context = {
        'total_robots': total_robots,
        'active_robots': active_robots,
        'idle_robots': idle_robots,
        'maintenance_robots': maintenance_robots,
        'total_maint_cost': f"${total_maint_cost:,.2f}",
        'total_downtime': f"{total_downtime:,.1f} jam",
        'total_tasks': total_tasks,
        'total_alerts': total_alerts,
        'recent_alerts': recent_alerts,
        'top_robots': top_robots,
        'top_zones': top_zones,
        'recent_maint': recent_maint,
    }
    return render(request, 'dashboard/home.html', context)

def robot_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    robots = Robot.objects.all()
    if query:
        robots = robots.filter(robot_id__icontains=query) | robots.filter(model__icontains=query) | robots.filter(serial_number__icontains=query)
    if status_filter:
        robots = robots.filter(operational_status=status_filter)
        
    context = {
        'robots': robots,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/robot_list.html', context)

def rl_simulation(request):
    # Render interactive simulation page
    return render(request, 'dashboard/simulation.html')

def copilot_chat(request):
    return render(request, 'dashboard/copilot.html')

@csrf_exempt
def api_copilot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
        except:
            return JsonResponse({'reply': 'Format request tidak valid.'}, status=400)
            
        reply = ""
        # 1. Robot queries
        if 'robot' in user_message:
            if 'jumlah' in user_message or 'berapa' in user_message:
                tot = Robot.objects.count()
                act = Robot.objects.filter(operational_status='Active').count()
                idle = Robot.objects.filter(operational_status='Idle').count()
                maint = Robot.objects.filter(operational_status='Maintenance').count()
                reply = f"Saat ini terdapat total **{tot} robot** terdaftar. Status armada:\n- **Active**: {act} robot\n- **Idle**: {idle} robot\n- **Maintenance**: {maint} robot"
            elif 'aktif' in user_message:
                act_list = list(Robot.objects.filter(operational_status='Active').values_list('robot_id', flat=True)[:10])
                reply = f"Terdapat {Robot.objects.filter(operational_status='Active').count()} robot aktif. Berikut sampel 10 robot aktif: {', '.join(act_list)}."
            elif 'rusak' in user_message or 'maintenance' in user_message:
                maint_count = Robot.objects.filter(operational_status='Maintenance').count()
                if maint_count > 0:
                    maint_list = list(Robot.objects.filter(operational_status='Maintenance').values_list('robot_id', flat=True))
                    reply = f"Terdapat **{maint_count} robot** yang sedang dalam perbaikan (Maintenance): {', '.join(maint_list)}."
                else:
                    reply = "Bagus! Saat ini tidak ada robot yang berada dalam status Maintenance."
            else:
                top_r = Robot.objects.order_by('-total_operational_hours').first()
                reply = f"Untuk info robot, robot dengan jam kerja tertinggi adalah **{top_r.robot_id}** ({top_r.model}) dengan akumulasi **{top_r.total_operational_hours:,.1f} jam**."
                
        # 2. Maintenance / Cost queries
        elif 'biaya' in user_message or 'maintenance' in user_message or 'servis' in user_message or 'cost' in user_message:
            total_cost = MaintenanceLog.objects.aggregate(total=Sum('total_cost_usd'))['total'] or 0.0
            avg_cost = MaintenanceLog.objects.aggregate(avg=Avg('total_cost_usd'))['avg'] or 0.0
            reply = f"Berdasarkan database histori:\n- **Total Biaya Servis**: ${total_cost:,.2f} USD\n- **Rata-rata Biaya per Servis**: ${avg_cost:,.2f} USD\n- **Total Kejadian Servis**: {MaintenanceLog.objects.count()} kali."
            
        # 3. Sensor / Alert queries
        elif 'sensor' in user_message or 'alert' in user_message or 'alarm' in user_message:
            alerts = SensorReading.objects.filter(alert_triggered=1).count()
            recent = SensorReading.objects.filter(alert_triggered=1).order_by('-timestamp').first()
            if recent:
                reply = f"Ditemukan total **{alerts} alarm sensor** terpicu. Alarm sensor terakhir terpicu pada **{recent.timestamp.strftime('%Y-%m-%d %H:%M:%S')}** oleh Sensor **{recent.sensor_id}** pada Robot **{recent.robot_id}** dengan jenis pembacaan **{recent.reading_type}** bernilai **{recent.value} {recent.unit}**."
            else:
                reply = "Tidak ada alarm sensor yang terpicu dalam database."
                
        # 4. Zone queries
        elif 'zona' in user_message or 'zone' in user_message:
            high_occ = Zone.objects.order_by('-current_occupancy_pct').first()
            reply = f"Gudang Anda memiliki {Zone.objects.count()} zona. Zona terpadat saat ini adalah **{high_occ.zone_name}** ({high_occ.zone_id}) dengan kepadatan **{high_occ.current_occupancy_pct}%**."
            
        # 5. General greetings
        elif any(greet in user_message for greet in ['halo', 'hi', 'hello', 'selamat', 'pagi', 'siang', 'sore', 'malam']):
            reply = "Halo! Saya **Warehouse AI Copilot**. Saya dapat membantu Anda menanyakan status robot, analisis biaya pemeliharaan, status kepadatan zona gudang, maupun alarm sensor IoT secara real-time. Apa yang ingin Anda tanyakan?"
        else:
            reply = "Saya belum sepenuhnya memahami pertanyaan Anda. Coba tanyakan hal seperti:\n- *'Berapa jumlah robot aktif saat ini?'*\n- *'Berapa total biaya servis maintenance?'*\n- *'Tampilkan alarm sensor terbaru'* \n- *'Zona mana yang paling padat?'*"
            
        return JsonResponse({'reply': reply})
    return JsonResponse({'error': 'POST request required'}, status=400)
