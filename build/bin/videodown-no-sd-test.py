from cv2 import cv2
#import cv2 
from onvif import ONVIFCamera
import os
import json
from requests_toolbelt import MultipartEncoder
import requests
import time
import sensecam_discovery
import base64
import datetime
import threading

#print(cv2.__version__)
fps = 10
minutes = 1
#video_name = 'outputtest.avi'
# video_wide = 2560
# video_high = 1920
# user = 'admin'
# pwd = 'a123456789'
# #获取环境变量
url = 'http://101.206.211.217:8018/file/uploadfile?'
# edgenodeKey = os.environ.get("edgenodeKey")
# fps =  os.environ.get("fps")
# print(fps)
# url = os.environ.get("url")
# print(url)
# minutes = os.environ.get("minutes")
#seconds = os.environ.get("seconds")
seconds = float(minutes)*60
print(seconds)
# #video_name = os.environ.get("name")
#video_name = 'out.avi'
# print(video_name)
# video_wide = os.environ.get("video_wide")
# print(video_wide)
# video_high = os.environ.get("video_high")
# print(video_high)
# user = os.environ.get("user")
# pwd = os.environ.get("pwd")
# endpointsBase64 = os.environ.get("endpoints")
# # url = os.environ.get("url")
# # camera_id = os.environ.get("id")
# id='10101111'
# #camera_id = 'DS-IPC-T12H-IA20200714AACHE59206192'
camera_id = 'DS-2CD3955FWD-IWS20200630AACH244564882'
endpointsBase64 = 'W3siYWdyZWVtZW50Ijoib252aWYiLCJ1cGxvYWRWYXJpYWJsZSI6IntcIklQQ1wiOiBcIkRTLUlQQy1UMTJILUlBXCJ9IiwibmFtZSI6ImhrMDAxIiwidmFyaWFibGUiOiJ7XCJ1c2VyXCI6XCJhZG1pblwiLFwicHdkXCI6XCJhMTIzNDU2Nzg5XCIsXCJ2aWRlb193aWRlXCI6XCI2NDBcIixcInZpZGVvX2hpZ2hcIjpcIjM2MFwiLFwiZnBzXCI6XCIxMFwiLFwicnRzcFwiOlwiOjU1NC9TdHJlYW1pbmcvQ2hhbm5lbHMvMTAyXCJ9IiwiaWQiOiIxMzA2NTUxNDIxMzM1NzY5MDg5IiwidHlwZSI6IuaRhOWDj+WktCIsImJyYW5kIjoiSElLVklTSU9OIiwia2V5IjoiRFMtSVBDLVQxMkgtSUEyMDIwMDcxNEFBQ0hFNTkyMDYxOTIifV0='
endpoints = base64.b64decode(endpointsBase64).decode("utf-8")
endpointsObjs = json.loads(endpoints)
endpoints_len = len(endpointsObjs)
print(endpoints_len)

# # 解析出camera_id
# endpoints = base64.b64decode(endpointsBase64).decode("utf-8")
# endpointsObjs = json.loads(endpoints)
# endpointsObj = endpointsObjs[0]
# camera_id = endpointsObj["key"]
# #解析出url所需id
# endpoints = base64.b64decode(endpointsBase64).decode("utf-8")
# endpointsObjs = json.loads(endpoints)
# endpointsObj = endpointsObjs[0]
# id = endpointsObj["id"]
# url_id = url+'id='+id
# print(url_id)

# 后端请求
# def backend_req(data,files):
#     response = requests.post(url_id, data=data,files=files)
#     print(response.text)
#     print(response.status_code)

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
        #variable = endpointsObj["variable"]
        variableObj = json.loads(endpointsObj["variable"])
        user = variableObj["user"]
        print(user)
        pwd = variableObj["pwd"]
        print(pwd)
        video_w = variableObj["video_wide"]
        print(video_w)
        video_h = variableObj["video_high"]
        print(video_h)
        ips = sensecam_discovery.discover()
        print("ips: ", ips)
        for ip in ips:
            cam = ONVIFCamera(ip, 80, user, pwd, './wsdl')
            maun = cam.devicemgmt.GetDeviceInformation()
            cameraid = maun.SerialNumber
            if cameraid==camera_id:
                #创建VideoWriter类对象
                while True:
                    print('download')
                    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                    cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+ip+":554/Streaming/Channels/102")
                    video_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    video_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    print(video_w,video_h,fps)
                    out = cv2.VideoWriter(video_name,fourcc, int(fps), (int(video_w),int(video_h)))                   
                    download_time = int(fps)*int(seconds)
                    print(download_time)
                    for i in range(download_time):
                        # print(i)
                        #cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+ip+":554/Streaming/Channels/1")
                        ret, frame = cap.read()
                        if ret==True:
                            out.write(frame)					#保存帧
                            #cap.release() 
                            # cv2.imshow(frame)
                            # cv2.waitKey(1)
                        else:
                            # pass
                            # cap.release() 
                            cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+ip+":554/Streaming/Channels/102")
                            # ret, frame = cap.read()
                            #print('video error')
                    out.release()
                    cap.release() 
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
                        video_name = './'+video_name
                        file1 = open(video_name,"rb")
                        files = {
                        'multipartFile':(file1)
                        }
                        backend_req(url_id,data,files)
                        #time.sleep(int(seconds))
                    except Exception as e:
                        print(e)
                    cv2.destroyAllWindows()
                    # out.release()
                    # cap.release()  
                    file1.close() 
                    print('over')         
                    time.sleep(20)
                    # path = video_name
                    # os.remove(path)
def backend_req(url_id,data,files):
    response = requests.post(url_id, data=data,files=files)
    print(response.text)
    print(response.status_code)

while True:
    # 获取ip
    ips = sensecam_discovery.discover()
    print("ips: ", ips)
    #for ip in ips:
        #cap = cv2.VideoCapture("rtsp://"+user+":"+pwd+"@"+ip+":554/Streaming/Channels/1")
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
