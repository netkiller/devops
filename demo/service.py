import calendar
import datetime

begin = "2017-11-15"
end = "2018-04-23"


def monthlist(begin, end):
    begin = datetime.datetime.strptime(begin, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")

    result = []
    while True:
        if begin.month == 12:
            next = begin.replace(year=begin.year+1, month=1, day=1)
        else:
            next = begin.replace(month=begin.month+1, day=1)
        if next > end:
            break

        day = calendar.monthrange(begin.year, begin.month)[1]
        # print()
        # print(datetime.datetime.date())
        result.append((begin.strftime("%Y-%m-%d"),
                      begin.replace(day=day).strftime("%Y-%m-%d")))
        begin = next
    result.append((begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
    return result


lists = monthlist(begin, end)
print(lists)
for (b, e) in lists:
    print(b, e)
