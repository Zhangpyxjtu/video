# video
视频下载opencv应用
### 无SD卡视频下载

### 传入参数

自带参数
export edgenodeKey

填写的参数
PLATFORM_HARBOR_URL=101.206.211.217:8079/mec/
export url="http://101.206.211.217:8018/file/uploadfile?"
minutes  (整数)

### 摄像头参数
export user="admin"
export pwd="a123456789"
video_wide 和摄像头参数一致
video_high 和摄像头参数一致
fps  和摄像头参数一致
rtsp  :554/Streaming/Channels/102(子码流)或101(主码流)


### 数据库参数
application_name: 无SD卡视频下载
scene: 该协议实现无SD卡时使用rtsp进行视频录制上传

template_name: video-download-rtsp
template_desc: 使用rtsp下载视频

```json
{
    "commonVariable": [
        {
            "title": "harbor地址",
            "key": "PLATFORM_HARBOR_URL",
            "value": ""
        },      
        {
            "title": "接口地址",
            "key": "url",
            "value": ""
        },          
        {
            "title": "录制时间",
            "key": "minutes",
            "value": ""
        }
    ],
    "environmentVariable": [],
    "showVariable": []
}
```

helm --kubeconfig ~/.kube/config-unicom install --set-string PLATFORM_HARBOR_URL=101.206.211.217:8079/mec/,user="admin",pwd="a123456789",url="http://101.206.211.217:8018/file/uploadfile?",hostname=dell31312312313  video-download-rtsp ../charts/video-download-rtsp-arm64
rtsp:554/Streaming/Channels/102

mysql -h 192.168.31.121 --port 3307 -u root -p < db.sql
test
