#from cv2 import cv2
import cv2 
import os
import json
import requests
import time
# import sensecam_discovery
import base64
import datetime
import threading
import subprocess as sp
#import ffmpeg

#获取环境变量
edgenodeKey = os.environ.get("edgenodeKey")
# fps =  os.environ.get("fps")
# print(fps)
url = os.environ.get("url")
print(url)
# rtsp_addr = os.environ.get("rtsp")
minutes = os.environ.get("minutes")
seconds = float(minutes)*60
print(seconds)
#解析出endpoints
endpointsBase64 = os.environ.get("endpoints")
endpoints = base64.b64decode(endpointsBase64).decode("utf-8")
endpointsObjs = json.loads(endpoints)



class videodown (threading.Thread):
    def __init__(self,threadID,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.counter=counter
    def run(self):
        endpointsObjs = json.loads(endpoints)
        endpointsObj = endpointsObjs[self.counter]
        camera_id = endpointsObj["key"]
        id = endpointsObj["id"]
        video_name = id+'.mp4'
        variableObj = json.loads(endpointsObj["variable"])
        user = variableObj["user"]
        print(user)
        pwd = variableObj["pwd"]
        print(pwd)
        #video_w = variableObj["video_wide"]
        #print(video_w)
        #video_h = variableObj["video_high"]
        #print(video_h)
        #fps = variableObj["fps"]
        #print(fps)
        rtsp_addr = variableObj["rtsp"]
        print(rtsp_addr)
        #print(fps)
        rtsps,SerialNumber,ips = discover()
        print(rtsps,SerialNumber,ips)
        print("ips: ", ips)
        for ip in ips:
            #rtsps = discover_rtsp()
            for rtsp in rtsps:
                if (camera_id in rtsp):
                    #创建VideoWriter类对象
                    while True:
                        print('download')
                        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                        fourcc = cv2.VideoWriter_fourcc(*'X264')
                        cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+rtsp+rtsp_addr)
                        video_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                        video_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        print(int(video_w),int(video_h),int(fps))
                        out = cv2.VideoWriter(video_name,fourcc, int(fps), (int(video_w),int(video_h)))
                        #cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+ip+":554/Streaming/Channels/102")
                        download_time = int(fps)*int(seconds)
                        for i in range(download_time):
                            ret, frame = cap.read()
                            if ret==True:
                                out.write(frame)					#保存帧
                            else:
                                # cap.release()
                                cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+rtsp+rtsp_addr)
                                #ret, frame = cap.read()
                        cap.release() 
                        out.release()
                        try:
                            fsize = os.path.getsize('./'+video_name)
                            print(fsize)
                            curr_time = datetime.datetime.now()
                            time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
                            print(time_str)
                            url_id = url+'id='+id
                            print(url_id)
                            data = {
                                'fileSize':fsize,
                                'startTime':time_str,
                                'duration':minutes
                            }
                            name = './'+video_name
                            file1 = open(name,"rb")
                            files = {
                            'multipartFile':(file1)
                            }
                            backend_req(url_id,data,files)
                        except Exception as e:
                            print(e)
                        #cv2.destroyAllWindows()
                        out.release()
                        cap.release()  
                        file1.close()          
                        print('remove')
                        path = video_name
                        os.remove(path)

def backend_req(url_id,data,files):
    response = requests.post(url_id, data=data,files=files)
    print(response.text)
    print(response.status_code)

def discover():
    command = ['timeout -s SIGKILL 5 avahi-browse -a --resolve']
    p = sp.Popen(command,  shell=True,stdout=sp.PIPE)
    str1 = 'hostname'
    str2 = 'address'
    list_address = []
    list_num = []
    list_ip = []
    for line in p.stdout.readlines():
        line = bytes.decode(line)
        # print(line)
        if (str1 in line):
            address = line[15:-2]
            # print(address,type(address),type(list_address))
            list_address.append(address)
            # print(list_address)
            num = line[15:-8]
            # print(num,type(num),type(list_num))
            list_num.append(num)
            # print(list_num)
        if (str2 in line):
            ip = line[14:-2]
            list_ip.append(ip)
            # print(ip)
    rtsp = list(set(list_address))
    rtsp.sort(key=list_address.index)
    SerialNumber = list(set(list_num))
    SerialNumber.sort(key = list_num.index)
    ips = list(set(list_ip))
    ips.sort(key = list_ip.index)
    return rtsp,SerialNumber,ips

while True:
    command_srevice = ['systemctl status avahi-daemon.service']
    p1 = sp.Popen(command_srevice,shell = True)
    threadLock = threading.Lock()
    threads = []
    threadID = 1
    for i in range(len(endpointsObjs)):
        thread = videodown(threadID,i)
        thread.start()
        threads.append(thread)
        threadID += 1
    for t in threads:
        t.join()
        print('exit')
