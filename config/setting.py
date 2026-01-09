import os

# 基础配置
BASE_URL = os.getenv("BASE_URL", "http://10.100.0.184:11080")
API = os.getenv("API", "api")
USERNAME = os.getenv("TEST_USERNAME", "caoqin")
PASSWORD = os.getenv("TEST_PASSWORD", "caoqin@123")

#常用的参数
PROVINCE = os.getenv("Province", "HeBei")
PROVINCE_CODE = os.getenv("PROVINCE_CODE", "130000")
FILTER_PARAMS = os.getenv("FILTER_PARAMS", {"param":{"targetTypes":["RADAR","AIS_A","AIS_B","BDS","CCTV","RADAR_AIS_A","RADAR_AIS_B","RADAR_BDS","RADAR_CCTV","AIS_A_BDS","AIS_B_BDS","RADAR_AIS_A_BDS","RADAR_AIS_B_BDS","CCTV_AIS","USV","BWC","PES","SRS"],"shipTypes":["1","2","4","3","10","5","8","9"],"lengthRange":[{"minValue":0,"maxValue":20},{"minValue":20,"maxValue":80},{"minValue":80,"maxValue":120},{"minValue":120,"maxValue":10000}],"speedRange":[{"minValue":0,"maxValue":1},{"minValue":1,"maxValue":10},{"minValue":10,"maxValue":20},{"minValue":20,"maxValue":120}],"areaList":[],"stateList":["1","2"],"registryList":["1","2","3","0"],"provinceList":[f"{PROVINCE}"],"fixedType":["1","3","2","4","5","6"],"showFuseBds":True,"fileds":["targetId","idLink","mmsi","state","latitude","longitude","course","heading","speed","len","shipType","sClass","lastTm","shipName","vesselName","nationality","displacement","duration","province","bdsTargetId","hidden","terminal","destination","rangeMaxDistance","staticAisName","markName","colorStyle","violationFlag","approachFlag","extendMessage","fixedType","imo","callSign"]}})

PROVINCE_BDS = os.getenv("Province", "ShanDong")
PROVINCE_CODE_BDS = os.getenv("PROVINCE_CODE", "370000")
FILTER_PARAMS_BDS = os.getenv("FILTER_PARAMS", {"param":{"targetTypes":["RADAR","AIS_A","AIS_B","BDS","CCTV","RADAR_AIS_A","RADAR_AIS_B","RADAR_BDS","RADAR_CCTV","AIS_A_BDS","AIS_B_BDS","RADAR_AIS_A_BDS","RADAR_AIS_B_BDS","CCTV_AIS","USV","BWC","PES","SRS"],"shipTypes":["1","2","4","3","10","5","8","9"],"lengthRange":[{"minValue":0,"maxValue":20},{"minValue":20,"maxValue":80},{"minValue":80,"maxValue":120},{"minValue":120,"maxValue":10000}],"speedRange":[{"minValue":0,"maxValue":1},{"minValue":1,"maxValue":10},{"minValue":10,"maxValue":20},{"minValue":20,"maxValue":120}],"areaList":[],"stateList":["1","2"],"registryList":["1","2","3","0"],"provinceList":[f"{PROVINCE_BDS}"],"fixedType":["1","3","2","4","5","6"],"showFuseBds":True,"fileds":["targetId","idLink","mmsi","state","latitude","longitude","course","heading","speed","len","shipType","sClass","lastTm","shipName","vesselName","nationality","displacement","duration","province","bdsTargetId","hidden","terminal","destination","rangeMaxDistance","staticAisName","markName","colorStyle","violationFlag","approachFlag","extendMessage","fixedType","imo","callSign"]}})



# 报告路径
REPORT_DIR = "reports"
SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")
TRACE_DIR = os.path.join(REPORT_DIR, "traces")
LOG_DIR = os.path.join(REPORT_DIR, "logs")

# 确保目录存在
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(TRACE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)