import os
import pygrib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import paramiko
import math

year = 2019 # 2019 or 2020 or 2021
area_list = ['chubu', 'chugoku', 'hokkaido',
             'hokuriku', 'kansai', 'kyushu',
             'okinawa', 'shikoku', 'tohoku', 'tokyo']

if year == 2020: # うるう年
    tNum = 8784
else:
    tNum = 8760

if year==2019 or year==2021:
    Day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
else:
    Day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    
# べき法則
def beki(wind_0,height_0,height_hub,n=7.0):
    wind_hub = wind_0 * (height_hub/height_0)**(1/n)
    return wind_hub

# 設置個所データの読み込み
WPplace = {}
for area in area_list:
    WPplace[area] = pd.read_excel('WPplace_'+area+'.xlsx', header=0, index_col=0)
    print(WPplace[area])
    
wind_speed = {}
for area in area_list:
    wind_speed[area] = pd.DataFrame(np.zeros((tNum,len(WPplace[area]))))    

#Date/Time list definition
date_time = []

t=0

#Loop to get wind data at WPplace long and lat and calculate wind hub for every hour in a year
for m in range(12):
    for d in range(Day[m]):
        # paramikoでpokemasにssh接続
        hostname = '133.72.91.174'
        username = 'pokemas'
        password = 'negiken4679'
        port = 22

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname,port,username,password)
        ## DLするファイルのディレクトリ設定とDL
        # 1月1日は前年12月31日1500(UTC)～1月1日1400(UTC)まで
        for h in range(24):
            yn = str(year)
            if h < 9: # UTCをJSTに読み替える
                hn = str(h+15)
            elif h < 19:
                hn = '0' + str(h-9)
            else:
                hn = str(h-9)
            
            if d==0:
                if h<9:
                    if m==0:
                        mn = '12'
                        dn = '31'
                        yn = str(year-1)
                    elif m<10:
                        mn = '0'+str(m)
                        dn = str(Day[m-1])
                    else:
                        mn = str(m)
                        dn = str(Day[m-1])
                else:
                    if m<9:
                        mn = '0'+str(m+1)
                        dn = '01'
                    else:
                        mn = str(m+1)
                        dn = '01'                        
            else:
                if h<9:
                    if d<10:
                        dn = '0'+str(d)
                    else:
                        dn = str(d)
                else:
                    if d<9:
                        dn = '0'+str(d+1)
                    else:
                        dn = str(d+1)
                
            sftp = ssh.open_sftp()
            dirname = '/home/LAB/53-共有データセット/GPVデータ/LA'+yn+'_'+mn
            sftp.chdir(dirname) # ディレクトリをcdする
            
            file_name = 'LANAL_'+yn+mn+dn+hn+'.grb2' # DLするファイル名の指定
            
            # 欠損した客観解析データの代わりにGPV-MSMの予報データを使う
            if year==2019 and mn=='02' and dn=='05':
                if hn=='00' or hn=='01' or hn=='02':
                    dirname = '/home/LAB/53-共有データセット/GPVデータ/'
                    sftp.chdir(dirname) # ディレクトリをcdする
                    file_name = 'Z__C_RJTD_20190205000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin'
            
            sftp.get(file_name,'/home/LAB/GMAN/'+file_name) # pokemasから自サーバにDL

        ssh.close() # ssh接続を切断

        grbs = {}
        point_data = {}
        wind_hub = {}
        

        for h in range(24):
            yn = str(year)
            if h < 9: # UTCをJSTに読み替える
                hn = str(h+15)
            elif h < 19:
                hn = '0' + str(h-9)
            else:
                hn = str(h-9)
            
            if d==0:
                if h<9:
                    if m==0:
                        mn = '12'
                        dn = '31'
                        yn = str(year-1)
                    elif m<10:
                        mn = '0'+str(m)
                        dn = str(Day[m-1])
                    else:
                        mn = str(m)
                        dn = str(Day[m-1])
                else:
                    if m<9:
                        mn = '0'+str(m+1)
                        dn = '01'
                    else:
                        mn = str(m+1)
                        dn = '01'                        
            else:
                if h<9:
                    if d<10:
                        dn = '0'+str(d)
                    else:
                        dn = str(d)
                else:
                    if d<9:
                        dn = '0'+str(d+1)
                    else:
                        dn = str(d+1)
                        
            file_name = 'LANAL_'+yn+mn+dn+hn+'.grb2' # 開くファイル名の指定
            date_time.append(yn + '-' + mn + '-' + dn + ' ' + hn + ':00') #Adding to the date and time list
            
            if year==2019 and mn=='02' and dn=='05':
                if hn=='00' or hn=='01' or hn=='02':
                    file_name = 'Z__C_RJTD_20190205000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin'
                    print(yn+mn+dn+hn)
                    grbs[h] = pygrib.open(file_name) # grib2データの読み込み
                else:
                    print(yn+mn+dn+hn) 
                    grbs[h] = pygrib.open(file_name) # grib2データの読み込み
                    os.remove(file_name) # 読み込んだファイルの消去
            else:
                print(yn+mn+dn+hn) 
                grbs[h] = pygrib.open(file_name) # grib2データの読み込み
                os.remove(file_name) # 読み込んだファイルの消去

            # # GRIB2ファイルの中身を表示する
            # for grb in grbs[h]:
            #     print(grb)

            # 観測値を取得する
            # uv座標系，uが横，vが縦
            # u-wind:西風が正, v-wind:南風が正
            if year==2019 and mn=='02' and dn=='05':
                if hn=='00':
                    uwind0 = grbs[h].select(parameterName='u-component of wind', forecastTime=0)[0]
                    values_u, lats_u, lons_u = uwind0.data()
                    vwind0 = grbs[h].select(parameterName='v-component of wind', forecastTime=0)[0]
                    values_v, lats_v, lons_v = vwind0.data()
                    values = np.sqrt(np.power(values_u,2) + np.power(values_v,2))
                elif hn=='01':
                    uwind0 = grbs[h].select(parameterName='u-component of wind', forecastTime=1)[0]
                    values_u, lats_u, lons_u = uwind0.data()
                    vwind0 = grbs[h].select(parameterName='v-component of wind', forecastTime=1)[0]
                    values_v, lats_v, lons_v = vwind0.data()
                    values = np.sqrt(np.power(values_u,2) + np.power(values_v,2))
                elif hn=='02':
                    uwind0 = grbs[h].select(parameterName='u-component of wind', forecastTime=2)[0]
                    values_u, lats_u, lons_u = uwind0.data()
                    vwind0 = grbs[h].select(parameterName='v-component of wind', forecastTime=2)[0]
                    values_v, lats_v, lons_v = vwind0.data()
                    values = np.sqrt(np.power(values_u,2) + np.power(values_v,2))
                else:
                    uwind0 = grbs[h].select(parameterName='u-component of wind', forecastTime=0)[0]
                    values_u, lats_u, lons_u = uwind0.data()
                    vwind0 = grbs[h].select(parameterName='v-component of wind', forecastTime=0)[0]
                    values_v, lats_v, lons_v = vwind0.data()
                    values = np.sqrt(np.power(values_u,2) + np.power(values_v,2))
            else:
                uwind0 = grbs[h].select(parameterName='u-component of wind', forecastTime=0)[0]
                values_u, lats_u, lons_u = uwind0.data()
                vwind0 = grbs[h].select(parameterName='v-component of wind', forecastTime=0)[0]
                values_v, lats_v, lons_v = vwind0.data()
                values = np.sqrt(np.power(values_u,2) + np.power(values_v,2))
                
            # print(values)
            # 指定した緯度経度に最も近いメッシュのインデックスを探索
            for area in area_list:
                for place in range(len(WPplace[area])):
                    lat_point = float(WPplace[area].iat[place,2])
                    lon_point = float(WPplace[area].iat[place,3])
                    diff_lonlats = abs((lats_u-lat_point)/lat_point)**2 + abs((lons_u-lon_point)/lon_point)**2
                    idx = np.unravel_index(np.argmin(diff_lonlats), diff_lonlats.shape)
                    print(idx)
                    print('lat='+str(lats_u[idx])+'lon='+str(lons_u[idx])) # 指定したメッシュの緯度・経度
                    point_data[h,place] = values[idx]
                    print('wind speed='+str(point_data[h,place]))
                    
                    # 風速データを指定したハブ高さに変換（べき法則）
                    height_0 = 10
                    height_hub = 80
                    wind_hub = beki(point_data[h,place],height_0,height_hub)
                    print('wind_hub = '+str(wind_hub))
                    
                    #wind_hub calculation results into wind_speed data frame
                    wind_speed[area].iat[t, place] = wind_hub
                  
            t += 1

#Setting df index to 'Date/Time' and outputting df to csv           
for area in area_list:  
    wind_speed[area]['Date/Time'] = date_time
    wind_speed[area] = wind_speed[area].set_index('Date/Time')
    wind_speed[area].index = pd.to_datetime(wind_speed[area].index) 
    print('wind_speed=')
    print(wind_speed[area].head)
    wind_speed[area].to_csv('wind_speed-'+area+str(year)+'.csv')