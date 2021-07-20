import json
import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import matplotlib.pyplot as plt
from pyecharts import Bar


#方法：打印输出结果
def pr_out(car_list):
    if len(car_list) == 0:
        if (station_op != "中国海洋大学"):
            print('无符合搜索条件的班车')

    k = 0
    for car_i in range(len(car_list)):
        k += 1
        print('_' * 100)
        print('第', k, '辆车')
        print('_' * 100)

        for e in range(46):
            car_match(e, car_list[car_i][e])


#方法：匹配对应的表头
def car_match(car_i, Info):
    if car_i == 3:
        car_t = '车号'
    elif car_i == 6:
        Info = dic_rename[Info]
        car_t = '出发点'
    elif car_i == 7:
        Info = dic_rename[Info]
        car_t = '目的地'
    elif car_i == 8:
        car_t = '出发时间'
    elif car_i == 9:
        car_t = '到站时间'
    elif car_i == 10:
        car_t = '历时'
    elif car_i == 21:
        car_t = '高级软卧'
    elif car_i == 23:
        car_t = '软卧一等卧'
    elif car_i == 24:
        car_t = '软座'
    elif car_i == 26:
        car_t = '无座'
    elif car_i == 28:
        car_t = '硬卧二等卧'
    elif car_i == 29:
        car_t = '硬坐'
    elif car_i == 30:
        car_t = '二等座/二等包座'
    elif car_i == 31:
        car_t = '一等座'
    elif car_i == 32:
        car_t = '商务座'
    elif car_i == 33:
        car_t = '动卧'
    else:
        return

    if Info == '':
        Info = '---'
    print(car_t, ':', Info)
    return


#爬取符合条件的站点信息
def get_info(url):
    global car_list
    car_list = []

    #判断输入是否合法
    if url == -1:
        return

    #动态爬取班次信息
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'cookie':
        '_uab_collina=160009096166163658684735; JSESSIONID=6345A6EA1FC2AC1A66100F744D635F51; RAIL_EXPIRATION=1600357189610; RAIL_DEVICEID=qraGMPdDZZJcVTeKSEfGP-pl8NjcnfdpVmOBCS1RFsCxVgVn5YCZONhmyh0u0RHhXDyiUcP_lD9VJy4QcFAI8Bn7pjIYi54mhF6O8GNaRVJsYh8_XT9PBok6ksd1YxVE8CxeJ8Vym6vNjvEMJ2PXYexb98vUVNxL; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2020-09-16; _jc_save_toDate=2020-09-16; BIGipServerpool_passport=233636362.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=468713994.38945.0000'
    }
    data2 = requests.get(url, headers=headers).content.decode("utf-8")
    data3 = data2.split('|')

    #生成car_list包含所有符合条件的车次信息

    for data_info_key in range(int((len(data3) - 1) / 46)):
        car_info = []
        for car_i in range(46):
            car_info.append(data3[car_i + 46 * data_info_key])
        car_list.append(car_info)


#方法：检测输入是否合法
def check_station(op, ed, time):
    flag = 1
    if (op not in all_name):
        flag = 0
    if (ed not in all_name):
        flag = 0
    if (len(time) != 10):
        flag = 0
    return flag


#爬取所有站名
def station_name():
    header = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    url1 = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
    r1 = requests.get(url1, headers=header).content
    html1 = str(r1, 'utf-8')
#输出站点信息的列表，和对应缩写的双向字典
    global dic_name
    global all_name
    global dic_rename
    dic_name = {}
    all_name = []
    dic_rename = {}

    html1_results = html1.split('|')
    for i in range(len(html1_results)):
        if i % 5 == 1:
            a = html1_results[i]
            all_name.append(html1_results[i])
        if i % 5 == 2:
            b = html1_results[i]
        if i % 4 == 3:
            dic_name[a] = b
            dic_rename[b] = a


#方法：录入条件信息
def station_writein():
    global station_op
    #station_op = input('请输入你的起始站点：')
    #station_ed = input('请输入你的终点站点：')
    #time = input('请输入日期时间（按照格式年—月—日）：')
    station_op = '青岛'
    station_ed = '北京'
    time = '2020-09-18'

    if (not check_station(station_op, station_ed, time)):
        if (station_op == "中国海洋大学"):
            print('\n'.join([''.join([('Love'[(x-y) % len('Love')] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))

        else:
            print('你输入的信息有误')
        return -1
        
#url的字符串拼接
    Url1 = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="
    Url2 = "&leftTicketDTO.from_station="
    Url3 = "&leftTicketDTO.to_station="
    Url4 = "&purpose_codes=ADULT"
    Url = Url1 + time + Url2 + dic_name[station_op] + Url3 + dic_name[
        station_ed] + Url4
    return Url

def printing_1():
    car_fast = 0
    car_other =0

    # 这两行代码解决 plt 中文显示的问题
    for num in car_list:
        if num[3][0] in ['G','C','D']:
            car_fast += 1
            car_fast_time = num[10]
        else:
            car_slow_time = num[10]
    car_other = len(car_list)-car_fast
        
    #plt.rcParams['font.sans-serif'] = ['SimHei']
    #plt.rcParams['axes.unicode_minus'] = False

    X_car = ('动车\n历时:'+car_fast_time,'其他列车\n历时:'+car_slow_time)
    y_number = [car_fast,car_other]

    #plt.bar(X_car, y_number)
    #plt.title('动车非动车统计图')

    #plt.show()

    bar = Bar ('动车非动车统计图','历时图')
    bar.add('数量',X_car,y_number)


def printing_2():
    mor = 0
    mid = 0
    aft = 0
    nig = 0

    # 这两行代码解决 plt 中文显示的问题
    for num in car_list:
        time_1 = int(num[9][0]+num[9][1])
        if  time_1 <6 and time_1 >= 0 :
            mor += 1
        if  time_1 <12 and time_1 >= 6:
            mid += 1
        if  time_1 <18 and time_1 >= 12 :
            aft += 1
        if  time_1 <24 and time_1 >= 18 :
            nig += 1

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    X_time = ('00:00-06:00','06:00-12:00','12:00-18:00','18:00-24:00')
    y_number = [mor,mid,aft,nig]

    plt.bar(X_time, y_number)
    plt.title('动车非动车统计图')

    plt.show()

#main()函数
def main():

    station_name()
    get_info(station_writein())
    pr_out(car_list)
    printing_1()
    #printing_2()
    

if __name__ == "__main__":
    main()

