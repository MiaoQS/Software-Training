import requests
from bs4 import BeautifulSoup
import re
import sys


def main():
    header = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    url1="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
    r1=requests.get(url1,headers=header).content
    html1=str(r1,'utf-8')
    data = BeautifulSoup(html1)


if __name__ == "__main__":
    main()