# coding=gbk
import re


class LogDeal(object):
    def __init__(self, podlog):
        self.podlog = podlog
        self.format_log = {}

    def get_format_log(self):
        self.format_log = {"test":"test"}


class ERROR_deal(LogDeal):

    def get_format_log(self):
        try:
            error_list = []
            error_log1 = str(re.findall("(error.*?)\n", self.podlog, flags=re.IGNORECASE))
            error_log2 = str(re.findall("(Failed.*?)\n", self.podlog))
            error_log = error_log1 + error_log2
            error_dict = {
                "数据库报错": ["(JDBC.*?)\n", "(DataSource.*?)\n"]
            }
            for key, value in error_dict.items():
                for errorlog in value:
                    if re.findall(errorlog, error_log):
                        error_list.append(key)
            if error_list:
                self.format_log.update({"日志报错error": error_list})
            else:
                unkonwerror = re.findall("(error.*?)\n", self.podlog, flags=re.IGNORECASE)
                temp = []
                [temp.append(i) for i in unkonwerror if i not in temp]
                self.format_log.update({"日志报错error": "暂无法识别的错误{0}".format(temp)})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class AIR_server(LogDeal):

    def get_format_log(self):

        MqttCron_log = '发送的心跳消息为：{(.*?)}'
        MqttReceiveService_log = 'mqtt消费图片数据通道--当前topic为：(.*?)\n'
        DataService_log = '发送云端的topic为：(.*?)\n'
        try:
            MqttCron_pod_log = re.findall(MqttCron_log, self.podlog)
            if MqttCron_pod_log:
                self.format_log.update({"app_MqttCron": "发送心跳信息正常"})
            else:
                self.format_log.update({"app_MqttCron": "发送心跳信息log missing"})

            MqttReceiveService_pod_log = re.findall(MqttReceiveService_log, self.podlog)
            if MqttReceiveService_pod_log:
                self.format_log.update({"app_MqttReceiveService": "图片接收正常"})
            else:
                self.format_log.update({"app_MqttReceiveService": "图片接收log missing"})
            DataService_pod_log = re.findall(DataService_log, self.podlog)
            if DataService_pod_log:
                self.format_log.update({"app_DataService": "数据发送云端正常"})
            else:
                self.format_log.update({"app_DataService": "数据发送云端log missing"})

        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Edge_watchdog(LogDeal):

    def get_format_log(self):
        try:
            LET_signal_pod_log = re.findall("CSQ:(.*?)\n", self.podlog)
            if LET_signal_pod_log:
                self.format_log.update({"信号值": LET_signal_pod_log[-1]})
            else:
                self.format_log.update({"信号值": "信号值 log missing"})
            LET_CCID_pod_log = re.findall("CCID:(.*?)\n", self.podlog)
            if LET_CCID_pod_log:
                self.format_log.update({"CCID号": LET_CCID_pod_log[-1]})
            else:
                self.format_log.update({"CCID号": "CCID号log missing"})
            cameraip_pod_log = re.findall("(box.*?)\n", self.podlog)
            if cameraip_pod_log:
                temp = cameraip_pod_log[-2:]
                if "box can reach camera ip 192.168.1.10" in temp or "box can reach camera ip 192.168.0.10" in temp:
                    self.format_log.update({"摄像头ip": "可以找到摄像头"})
                else:
                    self.format_log.update({"摄像头ip": "找不到摄像头"})
            else:
                self.format_log.update({"摄像头ip": "摄像头ip log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Sensor_data_collect(LogDeal):

    def get_format_log(self):
        try:
            camera_mqttup_log = re.findall("(图片.*?代理)", self.podlog)
            camera_sensor_log1 = re.findall("(相机.*?存图成功)", self.podlog)
            camera_sensor_log2 = re.findall("(图片.*?成功)", self.podlog)
            if camera_mqttup_log and (camera_sensor_log1 or camera_sensor_log2):
                self.format_log.update({"图片日志": "图片采集正常"})
            else:
                self.format_log.update({"图片日志": "图片log missing"})
            airbox_log = re.findall("air_box.py(.*?)\n", self.podlog)
            datatime_log = re.findall("(时间戳为.*?),", self.podlog)
            #alarm_log = re.findall("(报警码.*?)\n", self.podlog)
            if airbox_log:
                self.format_log.update({"airbox_log": "串口数据 采集正常"})
                self.format_log.update({"时间戳": datatime_log[-1]})
                #self.format_log.update({"报警码": alarm_log[-1]})
            else:
                self.format_log.update({"airbox_log": "串口数据采集log missing"})  # 判断串口数据采集
            # format_pod_log = {"图片": camera_log[-4:], "airbox_log": airbox_log[-4:]}
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Rod_traffic(LogDeal):
    def get_format_log(self):

        try:
            road_traffic_log = re.findall("(消息发布.*?)\n", self.podlog)
            if road_traffic_log:
                self.format_log.update({"交通识别": "交通拥堵识别正常"})
            else:
                self.format_log.update({"交通识别": "交通拥堵识别未发布消息"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Baresoil_recognition(LogDeal):

    def get_format_log(self):

        try:
            baresoil_recognition_log = re.findall("(消息发布.*?)\n", self.podlog)
            if baresoil_recognition_log:
                self.format_log.update({"裸土覆盖": "裸土覆盖识别正常"})
            else:
                self.format_log.update({"裸土覆盖": "裸土覆盖识别未发布消息"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Fire_somke(LogDeal):

    def get_format_log(self):

        try:
            baresoil_recognition_log = re.findall("(消息发布.*?)\n", self.podlog)
            if baresoil_recognition_log:
                self.format_log.update({"燃烟识别": "燃烟识别正常"})
            else:
                self.format_log.update({"燃烟识别": "燃烟识别未发布消息"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Outdoor_barbecue(LogDeal):

    def get_format_log(self):

        try:
            outdoor_barbecue_log = re.findall("(消息发布.*?)\n", self.podlog)
            if outdoor_barbecue_log:
                self.format_log.update({"户外烧烤": "户外烧烤识别正常"})
            else:
                self.format_log.update({"户外烧烤": "户外烧烤识别未发布消息"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})

class Build_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_build_server_reslog = re.findall("(接收硬件.*?)\n", self.podlog)
            meijing_build_server_fileuplog = re.findall("(文件上传成功.*?)\n", self.podlog)
            if meijing_build_server_reslog and meijing_build_server_fileuplog:
                self.format_log.update({"build-server": "工地哨兵工作正常"})
            else:
                self.format_log.update({"build-server": "工地哨兵未接收或上传数据log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Car_air_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_car_air_server_picup = re.findall("(上传云端图片的ossKey为.*?)\n", self.podlog)
            meijing_car_air_server_res = re.findall("(接收边缘端数据.*?)\n", self.podlog)
            if meijing_car_air_server_picup and meijing_car_air_server_res:
                self.format_log.update({"车载服务": "车载服务工作正常"})
            else:
                self.format_log.update({"车载服务": "车载服务未接收或上传数据log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})





class Shaoxing_cars_movebox(LogDeal):
    def get_format_log(self):

        try:
            shaoxing_cars_movebox_log = re.findall("(消息发布.*?)\n", self.podlog)
            if shaoxing_cars_movebox_log:
                self.format_log.update({"绍兴车载模型": "绍兴车载模型正常"})
            else:
                self.format_log.update({"绍兴车载模型": "绍兴车载模型未发布消息log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})


class Airtight_transportation(LogDeal):

    def get_format_log(self):

        try:
            airtight_transportation_log = re.findall("(消息发布.*?)\n", self.podlog)
            if airtight_transportation_log:
                self.format_log.update({"绍兴车载模型": "绍兴车载模型正常"})
            else:
                self.format_log.update({"绍兴车载模型": "绍兴车载模型未发布消息log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})

class Muck_screen_web(LogDeal):

    def get_format_log(self):

        try:
            meijing_muck_screen_web_log = re.findall("(Upgrade success.*?)\n", self.podlog)
            if meijing_muck_screen_web_log:
                self.format_log.update({"渣土车屏幕": "初始化成功"})
            else:
                self.format_log.update({"渣土车屏幕": "渣土车屏幕初始化有问题log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})

class Slagcar_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_slagcar_server_log1 = re.findall("(传感器实时数据插入成功.*?)\n", self.podlog)
            meijing_slagcar_server_log2 = re.findall("(秒级别数据发送成功.*?)\n", self.podlog)

            if meijing_slagcar_server_log1 and meijing_slagcar_server_log2:
                self.format_log.update({"渣土车服务": "渣土车服务正常"})
            else:
                self.format_log.update({"渣土车服务": "渣土车服务异常log missing"})
        except Exception as e:
            self.format_log.update({"日志解析error": "日志解析出错{0}".format(e)})

