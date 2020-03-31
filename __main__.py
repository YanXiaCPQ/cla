#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import argparse
from pathlib import Path
from ast import literal_eval
from datetime import datetime, timedelta

_SOLAR_ = 'solar'
_LUNAR_ = 'lunar'

dbirthday={
    _SOLAR_:{
        'B':'3月340日'
    },
    _LUNAR_:{
	'D':'三月初八日'
    }
}

def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', metavar='CONF_DIR', default=default_configure_dir, help='Specify configure file')
    return parser.parse_args(sys.argv[1:])


def notice(title):
    api = ''
    params = {
        "text":title
    }
    req = requests.get(api,params = params)


def checkdate():
    with open(Path('.').resolve().joinpath('./server/controllers/data.dict'), 'r') as f:
        dClaData = literal_eval(f.read())
    
    year=datetime.now().strftime("%Y")
    today = datetime.now().strftime("%m月%d日")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m月%d日")
    dyear = dClaData[year]
    
    for type_cla, value in dbirthday.items():
        for name, birthday in value.items():
            if type_cla == _SOLAR_:
                if len(birthday) == 5:
                    birthday = '0'+birthday
                if birthday == today:
                    notice(name + '今天新历生日啦 ==>' + birthday)
                elif birthday == tomorrow:
                    notice(name + '明天新历生日啦 ==>' + birthday)
            elif type_cla == _LUNAR_:
                record_birthday = birthday
                tmpdyear = {v : k for k, v in dyear.items()}
                birthday = tmpdyear[birthday][5:]
                print(birthday)
                if len(birthday) == 5:
                    birthday = '0' + birthday                
                if birthday == today:
                    notice(name + '今天阴历生日啦 ' + record_birthday)
                elif birthday == tomorrow:
                    notice(name + '明天阴历生日啦 ' + record_birthday)



if __name__ == '__main__':
    checkdate()

    
