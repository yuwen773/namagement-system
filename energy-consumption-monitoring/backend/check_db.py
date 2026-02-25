import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energy_monitoring.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.energy.models import EnergyData
from apps.devices.models import Device, EnergyType
from apps.buildings.models import Campus, Building, Floor, Room
from apps.accounts.models import UserProfile
from apps.alarms.models import Alarm, AlarmRule
from apps.system.models import Bill, RechargeRecord, Notice, OperationLog
from django.db.models import Count, Min, Max
from django.db import connection
from django.contrib.auth.models import User
import json

result = {}

# 1. All em_ table counts
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        AND table_name LIKE 'em_%'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cursor.fetchall()]

table_counts = {}
with connection.cursor() as cursor:
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        table_counts[table] = count
result['table_counts'] = table_counts

# 2. Energy data by type
energy_by_type = list(EnergyType.objects.annotate(
    data_count=Count('devices__energy_data')
).values('code', 'name', 'data_count'))
result['energy_data_by_type'] = energy_by_type

# 3. Energy data time range
time_range = EnergyData.objects.aggregate(
    min_time=Min('timestamp'),
    max_time=Max('timestamp')
)
result['energy_data_time_range'] = {
    'min_time': str(time_range['min_time']) if time_range['min_time'] else None,
    'max_time': str(time_range['max_time']) if time_range['max_time'] else None
}

# 4. Data by year
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT YEAR(timestamp) as year, COUNT(*) as count
        FROM em_energy_data
        GROUP BY YEAR(timestamp)
        ORDER BY year
    """)
    result['energy_data_by_year'] = [
        {'year': row[0], 'count': row[1]}
        for row in cursor.fetchall()
    ]

# 5. Building hierarchy
result['buildings'] = {
    'campuses': Campus.objects.count(),
    'buildings': Building.objects.count(),
    'floors': Floor.objects.count(),
    'rooms': Room.objects.count()
}

# 6. Devices by type
devices_by_type = list(Device.objects.values('energy_type__code').annotate(
    count=Count('id')
).values_list('energy_type__code', 'count'))
result['devices_by_type'] = dict(devices_by_type)
result['devices_total'] = Device.objects.count()

# 7. Devices with data count
device_list = []
for d in Device.objects.all():
    data_count = EnergyData.objects.filter(device=d).count()
    device_list.append({
        'id': d.id,
        'device_id': d.device_id,
        'name': d.name,
        'energy_type': d.energy_type.code,
        'data_count': data_count
    })
result['devices'] = device_list

# 8. Campus building summary
campus_list = []
for c in Campus.objects.all():
    building_count = Building.objects.filter(campus=c).count()
    campus_list.append({
        'id': c.id,
        'name': c.name,
        'code': c.code,
        'capacity': c.capacity,
        'building_count': building_count
    })
result['campuses'] = campus_list

# 9. Users
user_list = []
for u in User.objects.all():
    try:
        profile = u.profile
        user_list.append({
            'id': u.id,
            'username': u.username,
            'role': profile.role,
            'phone': profile.phone
        })
    except:
        user_list.append({
            'id': u.id,
            'username': u.username,
            'role': 'NO_PROFILE'
        })
result['users'] = user_list
result['users_total'] = User.objects.count()

# 10. Alarms
alarm_list = []
for a in Alarm.objects.all():
    alarm_list.append({
        'id': a.id,
        'device': a.device.device_id,
        'alarm_type': a.alarm_type,
        'status': a.status,
        'alarm_time': str(a.alarm_time),
        'alarm_value': str(a.alarm_value) if a.alarm_value else None
    })
result['alarms'] = alarm_list

# 11. Alarm rules
rule_list = []
for r in AlarmRule.objects.all():
    rule_list.append({
        'id': r.id,
        'name': r.name,
        'energy_type': r.energy_type.code,
        'threshold_value': str(r.threshold_value),
        'is_active': r.is_active
    })
result['alarm_rules'] = rule_list

print(json.dumps(result, indent=2, ensure_ascii=False))
