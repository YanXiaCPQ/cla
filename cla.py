import json
import requests
from pathlib import Path
from enum import Enum, unique

@unique
class Month(Enum):
    Jan = "正月"
    Feb = "二月"
    Mar = "三月"
    Apr = "四月"
    May = "五月"
    Jun = "六月"
    Jul = "七月"
    Aug = "八月"
    Sep = "九月"
    Oct = "十月"
    Nov = "十一月"
    Dec = "十二月"
Month_list = ["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
Month_list2 = ["閏正月","閏二月","閏三月","閏四月","閏五月","閏六月","閏七月","閏八月","閏九月","閏十月","閏十一月","閏十二月"]

def dowmload(begin, end):
    for i in range(begin, end):
        try:
            url = "https://www.hko.gov.hk/tc/gts/time/calendar/text/files/T{}c.txt".format(str(i))
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            html = res.text
            with open(Path('.').resolve().joinpath('./rowdata/{}.txt'.format(str(i))), 'w') as f:
                f.write(html)
        except Exception as e:
            print(e)
            print(i)


def processAndSave(begin, end):
    cla = dict()
    for i in range(begin, end):
        with open(Path('.').resolve().joinpath('./rowdata/{}.txt'.format(str(i))), 'r') as f:
            tmp = f.readlines()
            header_date = tmp[2]
            list_date = tmp[3:]

        header_date = header_date.split()
        gregoriana = header_date[0]
        lunar = header_date[1]

        tmpMonth=list()

        for date in list_date:
            tmp = date.split()
            if len(tmp)==0:
                continue
            if tmp[1].find('月') != -1:
                tmpMonth.append(tmp[1])

        month_begin = list(set(Month_list).difference(set(tmpMonth)))
        if len(month_begin) != 0:
            month = month_begin[0]
        else:
            month = tmpMonth[0]

        for date in list_date:
            tmp = date.split()
            if len(tmp)==0:
                continue
            if tmp[1].find('月') == -1:
                tmp[1] = Month_list[Month_list.index(month)] + tmp[1] + '日'
            else:
                tmp[1]= tmp[1] + '初一日'
                try:
                    month = Month_list[Month_list.index(month)]
                except:
                    month = Month_list[Month_list2.index(month)]
            cla[tmp[0]] = tmp[1]
    
    with open(Path('.').resolve().joinpath('./data.dict'), 'w') as f:
        f.write(str(cla))


begin = 2020
end = 2101
#dowmload(begin,end)
processAndSave(begin,end)

