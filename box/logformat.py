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
                "���ݿⱨ��": ["(JDBC.*?)\n", "(DataSource.*?)\n"]
            }
            for key, value in error_dict.items():
                for errorlog in value:
                    if re.findall(errorlog, error_log):
                        error_list.append(key)
            if error_list:
                self.format_log.update({"��־����error": error_list})
            else:
                unkonwerror = re.findall("(error.*?)\n", self.podlog, flags=re.IGNORECASE)
                temp = []
                [temp.append(i) for i in unkonwerror if i not in temp]
                self.format_log.update({"��־����error": "���޷�ʶ��Ĵ���{0}".format(temp)})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class AIR_server(LogDeal):

    def get_format_log(self):

        MqttCron_log = '���͵�������ϢΪ��{(.*?)}'
        MqttReceiveService_log = 'mqtt����ͼƬ����ͨ��--��ǰtopicΪ��(.*?)\n'
        DataService_log = '�����ƶ˵�topicΪ��(.*?)\n'
        try:
            MqttCron_pod_log = re.findall(MqttCron_log, self.podlog)
            if MqttCron_pod_log:
                self.format_log.update({"app_MqttCron": "����������Ϣ����"})
            else:
                self.format_log.update({"app_MqttCron": "����������Ϣlog missing"})

            MqttReceiveService_pod_log = re.findall(MqttReceiveService_log, self.podlog)
            if MqttReceiveService_pod_log:
                self.format_log.update({"app_MqttReceiveService": "ͼƬ��������"})
            else:
                self.format_log.update({"app_MqttReceiveService": "ͼƬ����log missing"})
            DataService_pod_log = re.findall(DataService_log, self.podlog)
            if DataService_pod_log:
                self.format_log.update({"app_DataService": "���ݷ����ƶ�����"})
            else:
                self.format_log.update({"app_DataService": "���ݷ����ƶ�log missing"})

        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Edge_watchdog(LogDeal):

    def get_format_log(self):
        try:
            LET_signal_pod_log = re.findall("CSQ:(.*?)\n", self.podlog)
            if LET_signal_pod_log:
                self.format_log.update({"�ź�ֵ": LET_signal_pod_log[-1]})
            else:
                self.format_log.update({"�ź�ֵ": "�ź�ֵ log missing"})
            LET_CCID_pod_log = re.findall("CCID:(.*?)\n", self.podlog)
            if LET_CCID_pod_log:
                self.format_log.update({"CCID��": LET_CCID_pod_log[-1]})
            else:
                self.format_log.update({"CCID��": "CCID��log missing"})
            cameraip_pod_log = re.findall("(box.*?)\n", self.podlog)
            if cameraip_pod_log:
                temp = cameraip_pod_log[-2:]
                if "box can reach camera ip 192.168.1.10" in temp or "box can reach camera ip 192.168.0.10" in temp:
                    self.format_log.update({"����ͷip": "�����ҵ�����ͷ"})
                else:
                    self.format_log.update({"����ͷip": "�Ҳ�������ͷ"})
            else:
                self.format_log.update({"����ͷip": "����ͷip log missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Sensor_data_collect(LogDeal):

    def get_format_log(self):
        try:
            camera_mqttup_log = re.findall("(ͼƬ.*?����)", self.podlog)
            camera_sensor_log1 = re.findall("(���.*?��ͼ�ɹ�)", self.podlog)
            camera_sensor_log2 = re.findall("(ͼƬ.*?�ɹ�)", self.podlog)
            if camera_mqttup_log and (camera_sensor_log1 or camera_sensor_log2):
                self.format_log.update({"ͼƬ��־": "ͼƬ�ɼ�����"})
            else:
                self.format_log.update({"ͼƬ��־": "ͼƬlog missing"})
            airbox_log = re.findall("air_box.py(.*?)\n", self.podlog)
            datatime_log = re.findall("(ʱ���Ϊ.*?),", self.podlog)
            #alarm_log = re.findall("(������.*?)\n", self.podlog)
            if airbox_log:
                self.format_log.update({"airbox_log": "�������� �ɼ�����"})
                self.format_log.update({"ʱ���": datatime_log[-1]})
                #self.format_log.update({"������": alarm_log[-1]})
            else:
                self.format_log.update({"airbox_log": "�������ݲɼ�log missing"})  # �жϴ������ݲɼ�
            # format_pod_log = {"ͼƬ": camera_log[-4:], "airbox_log": airbox_log[-4:]}
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Rod_traffic(LogDeal):
    def get_format_log(self):

        try:
            road_traffic_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if road_traffic_log:
                self.format_log.update({"��ͨʶ��": "��ͨӵ��ʶ������"})
            else:
                self.format_log.update({"��ͨʶ��": "��ͨӵ��ʶ��δ������Ϣ"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Baresoil_recognition(LogDeal):

    def get_format_log(self):

        try:
            baresoil_recognition_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if baresoil_recognition_log:
                self.format_log.update({"��������": "��������ʶ������"})
            else:
                self.format_log.update({"��������": "��������ʶ��δ������Ϣ"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Fire_somke(LogDeal):

    def get_format_log(self):

        try:
            baresoil_recognition_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if baresoil_recognition_log:
                self.format_log.update({"ȼ��ʶ��": "ȼ��ʶ������"})
            else:
                self.format_log.update({"ȼ��ʶ��": "ȼ��ʶ��δ������Ϣ"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Outdoor_barbecue(LogDeal):

    def get_format_log(self):

        try:
            outdoor_barbecue_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if outdoor_barbecue_log:
                self.format_log.update({"�����տ�": "�����տ�ʶ������"})
            else:
                self.format_log.update({"�����տ�": "�����տ�ʶ��δ������Ϣ"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})

class Build_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_build_server_reslog = re.findall("(����Ӳ��.*?)\n", self.podlog)
            meijing_build_server_fileuplog = re.findall("(�ļ��ϴ��ɹ�.*?)\n", self.podlog)
            if meijing_build_server_reslog and meijing_build_server_fileuplog:
                self.format_log.update({"build-server": "�����ڱ���������"})
            else:
                self.format_log.update({"build-server": "�����ڱ�δ���ջ��ϴ�����log missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Car_air_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_car_air_server_picup = re.findall("(�ϴ��ƶ�ͼƬ��ossKeyΪ.*?)\n", self.podlog)
            meijing_car_air_server_res = re.findall("(���ձ�Ե������.*?)\n", self.podlog)
            if meijing_car_air_server_picup and meijing_car_air_server_res:
                self.format_log.update({"���ط���": "���ط���������"})
            else:
                self.format_log.update({"���ط���": "���ط���δ���ջ��ϴ�����log missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})





class Shaoxing_cars_movebox(LogDeal):
    def get_format_log(self):

        try:
            shaoxing_cars_movebox_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if shaoxing_cars_movebox_log:
                self.format_log.update({"���˳���ģ��": "���˳���ģ������"})
            else:
                self.format_log.update({"���˳���ģ��": "���˳���ģ��δ������Ϣlog missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})


class Airtight_transportation(LogDeal):

    def get_format_log(self):

        try:
            airtight_transportation_log = re.findall("(��Ϣ����.*?)\n", self.podlog)
            if airtight_transportation_log:
                self.format_log.update({"���˳���ģ��": "���˳���ģ������"})
            else:
                self.format_log.update({"���˳���ģ��": "���˳���ģ��δ������Ϣlog missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})

class Muck_screen_web(LogDeal):

    def get_format_log(self):

        try:
            meijing_muck_screen_web_log = re.findall("(Upgrade success.*?)\n", self.podlog)
            if meijing_muck_screen_web_log:
                self.format_log.update({"��������Ļ": "��ʼ���ɹ�"})
            else:
                self.format_log.update({"��������Ļ": "��������Ļ��ʼ��������log missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})

class Slagcar_server(LogDeal):

    def get_format_log(self):

        try:
            meijing_slagcar_server_log1 = re.findall("(������ʵʱ���ݲ���ɹ�.*?)\n", self.podlog)
            meijing_slagcar_server_log2 = re.findall("(�뼶�����ݷ��ͳɹ�.*?)\n", self.podlog)

            if meijing_slagcar_server_log1 and meijing_slagcar_server_log2:
                self.format_log.update({"����������": "��������������"})
            else:
                self.format_log.update({"����������": "�����������쳣log missing"})
        except Exception as e:
            self.format_log.update({"��־����error": "��־��������{0}".format(e)})

