from datetime import datetime,timedelta
now_time = datetime.now()
# .replace(hour=0, minute=0, second=0, microsecond=0)
# 当月第一天

# 当前日期所在周的周一
week_start_time = now_time - timedelta(days=now_time.weekday(), hours=now_time.hour, minutes=now_time.minute,
                                    seconds=now_time.second)
# 当前日期所在周的周日
week_end_time = week_start_time + timedelta(days=6, hours=23, minutes=59, seconds=59)


one_time = now_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# 当前日期处于本月第几周
week_num = int(now_time.strftime('%W')) - int(one_time.strftime('%W')) 

print(int(now_time.strftime('%W')) ,int(one_time.strftime('%W')) )

print(now_time, one_time, week_num)