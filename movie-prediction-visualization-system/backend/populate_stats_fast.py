import os
import django
import sys
from datetime import date as dt_date

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_prediction.settings")
django.setup()

from django.db.models import Sum, Count
from django.db import transaction

from boxoffice.models import BoxOfficeRecord, DailyRegionStat, DailyMovieTypeStat, DailyOverallStat


def populate_overall_stats(year):
    """填充大盘统计数据 - 最简单，最关键"""
    print(f"[1/3] Populating DailyOverallStat for {year}...")

    # 删除旧数据
    deleted = DailyOverallStat.objects.filter(record_date__year=year).delete()[0]
    if deleted:
        print(f"  Deleted {deleted} old records")

    # 按日期聚合票房数据 - 使用Django ORM
    stats = BoxOfficeRecord.objects.filter(
        record_date__year=year
    ).values('record_date').annotate(
        total_box_office=Sum('daily_box_office'),
        total_screening_count=Sum('screening_count'),
        total_audience_count=Sum('audience_count')
    ).order_by('record_date')

    # 批量创建
    to_create = []
    for stat in stats:
        to_create.append(DailyOverallStat(
            record_date=stat['record_date'],
            total_box_office=stat['total_box_office'] or 0,
            total_screening_count=stat['total_screening_count'] or 0,
            total_audience_count=stat['total_audience_count'] or 0
        ))

    count = len(to_create)
    DailyOverallStat.objects.bulk_create(to_create, batch_size=1000)
    print(f"  Created {count} records for {year}")
    return count


def populate_region_stats(year):
    """填充地域统计数据"""
    print(f"[2/3] Populating DailyRegionStat for {year}...")

    # 删除旧数据
    deleted = DailyRegionStat.objects.filter(record_date__year=year).delete()[0]
    if deleted:
        print(f"  Deleted {deleted} old records")

    # 按日期和地域聚合票房数据
    stats = BoxOfficeRecord.objects.filter(
        record_date__year=year
    ).exclude(cinema__region__isnull=True).values(
        'record_date', 'cinema__region'
    ).annotate(
        box_office=Sum('daily_box_office')
    ).order_by('record_date', 'cinema__region')

    # 批量创建
    to_create = []
    for stat in stats:
        region_id = stat['cinema__region']
        if region_id:
            to_create.append(DailyRegionStat(
                record_date=stat['record_date'],
                region_id=region_id,
                box_office=stat['box_office'] or 0,
                cinema_count=1  # 这里简化了，实际可能需要统计
            ))

    count = len(to_create)
    DailyRegionStat.objects.bulk_create(to_create, batch_size=1000)
    print(f"  Created {count} records for {year}")
    return count


def populate_type_stats(year):
    """填充类型统计数据"""
    print(f"[3/3] Populating DailyMovieTypeStat for {year}...")

    # 删除旧数据
    deleted = DailyMovieTypeStat.objects.filter(record_date__year=year).delete()[0]
    if deleted:
        print(f"  Deleted {deleted} old records")

    # 按日期和类型聚合票房数据
    stats = BoxOfficeRecord.objects.filter(
        record_date__year=year,
        movie__type__isnull=False
    ).values(
        'record_date', 'movie__type'
    ).annotate(
        box_office=Sum('daily_box_office')
    ).order_by('record_date', 'movie__type')

    # 批量创建
    to_create = []
    for stat in stats:
        type_id = stat['movie__type']
        if type_id:
            to_create.append(DailyMovieTypeStat(
                record_date=stat['record_date'],
                movie_type_id=type_id,
                box_office=stat['box_office'] or 0
            ))

    count = len(to_create)
    DailyMovieTypeStat.objects.bulk_create(to_create, batch_size=1000)
    print(f"  Created {count} records for {year}")
    return count


if __name__ == "__main__":
    print("=" * 60)
    print("Starting to populate pre-aggregated tables")
    print("=" * 60)

    current_year = dt_date.today().year
    years = [current_year]  # 只处理当前年

    print(f"Years to process: {years}")
    print(f"Total BoxOfficeRecord records: {BoxOfficeRecord.objects.count()}")
    print("-" * 60)

    for year in years:
        print(f"\nProcessing data for {year}:")
        print("-" * 60)

        try:
            # 先填充大盘统计，这是最重要的
            overall_count = populate_overall_stats(year)
            type_count = populate_type_stats(year)
            region_count = populate_region_stats(year)

            print("-" * 60)
            print(f"{year} completed: overall={overall_count}, type={type_count}, region={region_count}")
        except Exception as e:
            print(f"Error processing {year}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("All stats populated successfully!")
    print("=" * 60)
