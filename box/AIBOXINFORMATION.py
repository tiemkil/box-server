# coding=gbk
import json
import time

import pandas as pd
from kubernetes import client, config

import requests

config.load_kube_config(config_file=r"config/viewer.yml")
v1 = client.CoreV1Api()

class AIboxinformation(object):
    '''
    打印保存盒子信息和配置
    '''

    def __init__(self, nodeid, token):
        self.nodeid = nodeid
        self.url_info = "https://cloud.meijingdata.com/iot-edge-server/admin/api/v1/edge-nodes/" + self.nodeid

        self.nodeinfo_dict = {}
        # self.lastdata_dict = {}
        self.payload = {}
        self.headers = {"Cookie": "Authorization={0}".format(token)}
        self.nodeinfo_dict["nodeid"] = nodeid
        self.wrongndoedic_flag = ''
        self.wrongndoe_flag = {"namespace": 'this node have no namespace',
                               "namespace": 'this node have no namespace',
                               "nodestatus": "read node status wrong",
                               "onlineTime": "not response",
                               "onlineTime": "read onlineTime is wrong",
                               "edgeConfig": "read edgeConfig is empty",
                               "edgeConfig": "get edgeConfig wrong",
                               "deviceConfig": "read deviceConfig wrong",
                               "最后一条数据": "none",
                               "最后一条数据上传时间": '',
                               "最后一条数据": "最后一条数据读取失败",
                               "最后一条数据上传时间": '最后一条数据上传时间读取失败',
                               "最后一张图片上传时间": "not response",
                                "picture_info":'',
                                "最后一张图片上传时间": "read picture_last_time wrong",
                                "picture_info":'none',
                               "24h数据上传量": "not response",
                               "24h数据上传量": "can not read datanum",
                               "siteCode": "siteCode is none, can not read this node info",
                               "nodestatus": "Unknown"}

    def get_aibox_info(self):
        response = requests.request("GET", self.url_info, headers=self.headers, data=self.payload)
        try:
            response_dict = json.loads(response.text)

            if response_dict:
                self.nodeinfo_dict["address"] = response_dict["address"]
                self.nodeinfo_dict["siteCode"] = response_dict["siteCode"]
                self.nodeinfo_dict["typeCode"] = response_dict["typeCode"]
                self.nodeinfo_dict["站点名称"] = response_dict["nodeName"]
            else:
                self.nodeinfo_dict["address"] = "can not read address"
                self.nodeinfo_dict["siteCode"] = "can not read siteCode"
                self.nodeinfo_dict["typeCode"] = "can not read typeCode"
                self.nodeinfo_dict["站点名称"] = response_dict["nodeName"]
        except Exception as e:
            self.nodeinfo_dict["address"] = "get aibox information wrong{0}".format(e)
            self.nodeinfo_dict["siteCode"] = "get aibox information wrong{0}".format(e)
            self.nodeinfo_dict["typeCode"] = "get aibox information wrong{0}".format(e)
            self.nodeinfo_dict["站点名称"] = response_dict["nodeName"]

    def get_node_status(self):
        node_list = v1.read_node(self.nodeid)
        temp = {}
        try:
            self.nodeinfo_dict["namespace"] = node_list.metadata.labels["box.meijingdata.com/namespace"]
        except Exception:
            self.nodeinfo_dict["namespace"] = 'this node have no namespace'

        try:
            self.nodeinfo_dict["nodestatus"] = node_list.status.conditions[0].status
            self.nodeinfo_dict["nodestatus_reason"] = node_list.status.conditions[0].reason
        except Exception as e:
            self.nodeinfo_dict["nodestatus"] = "read node status wrong{0}".format(e)
            self.nodeinfo_dict["nodestatus_reason"] = 'read node status wrong{0}'.format(e)

    def get_node_onlinetime(self):
        end_time = int(round(time.time() * 1000))
        start_time = end_time - 60 * 60 * 24 * 7
        url_online = "https://cloud.meijingdata.com/online-server/api/v1/online/details?end={0}&start={1}&nodeCode={2}".format(
            str(end_time), str(start_time), self.nodeid)
        try:
            response = requests.request("POST", url_online, headers=self.headers, data=self.payload)
            ONLINEtime_dict = json.loads(response.text)
            if ONLINEtime_dict:
                # len(ONLINEtime_dict)
                disconnect_count = len(ONLINEtime_dict) - 1
                onlineStartTime = int(ONLINEtime_dict[disconnect_count]["onlineStartTime"]) / 1000
                time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(onlineStartTime))

                self.nodeinfo_dict["onlineTime"] = {"断线次数": disconnect_count,
                                                    "在线开始时间": time_string
                                                    }
            else:
                self.nodeinfo_dict["onlineTime"] = "not response"
        except Exception as e:
            self.nodeinfo_dict["onlineTime"] = "read onlineTime is wrong{0}".format(e)

    def get_edgeConfig(self):
        self.url_edgeConfig = "https://cloud.meijingdata.com/iot-edge-server/api/v1/config/getConfig/" + \
                              self.nodeinfo_dict["siteCode"] \
                              + "?keys=edgeConfig&siteCode=" + self.nodeinfo_dict["siteCode"]
        response = requests.request("GET", self.url_edgeConfig, headers=self.headers, data=self.payload)

        try:
            node_edgeConfig_dict = json.loads(response.text)
            if node_edgeConfig_dict:
                temp = node_edgeConfig_dict[0]["configValue"]
                num = []
                for key in temp:
                    if type(temp[key]) is dict:
                        num.append(temp[key]["logName"])
                    else:
                        if key == "logName":
                            num.append(temp["logName"])
                        else:
                            pass

                self.nodeinfo_dict["edgeConfig"] = num
                #print(num)

            else:
                self.nodeinfo_dict["edgeConfig"] = "read edgeConfig is empty"
        except Exception as e:
            self.nodeinfo_dict["edgeConfig"] = "get edgeConfig wrong{0}".format(e)

    def get_deviceConfig(self):
        self.url_deviceConfig = "https://cloud.meijingdata.com/iot-edge-server/api/v1/config/getConfig/" \
                                + self.nodeinfo_dict["siteCode"] + "?keys=deviceConfig&siteCode=" + self.nodeinfo_dict[
                                    "siteCode"]
        response = requests.request("GET", self.url_deviceConfig, headers=self.headers, data=self.payload)
        temp = {}
        try:
            node_deviceConfig_dict = json.loads(response.text)

            self.nodeinfo_dict["deviceConfig"] = node_deviceConfig_dict
        except Exception as e:
            self.nodeinfo_dict["deviceConfig"] = "read deviceConfig wrong".format(e)

    def get_videoCode(self):
        self.url_videocode = "https://cloud.meijingdata.com/iot-manager-server/api/v1/video/list-by-site-codes?siteCodes={0}" \
            .format(self.nodeinfo_dict["siteCode"])
        response = requests.request("GET", self.url_videocode, headers=self.headers, data=self.payload)
        try:
            response = str(response.text)
            videoinfo_dict = json.loads(response)
            if videoinfo_dict:
                self.nodeinfo_dict["视频编码"] = videoinfo_dict[0]["videoCode"]
                    #{"videoCode": videoinfo_dict[0]["videoCode"],"videoType": videoinfo_dict[0]["videoTypeCode"]}
            else:
                self.nodeinfo_dict["视频编码"] = "have not videoinfo"
        except Exception as e:
            self.nodeinfo_dict["视频编码"] = "get videoCode wrong{0}".format(e)

    def get_siminfo(self):

        """
        ccid-->sim(13位)
        :return:
        """

    def get_picture_last_time(self):

        url_picture = "https://cloud.meijingdata.com/mcl-handle-server/api/v1/pictureHandle/getLastPicture?mn={0}".format(
            self.nodeinfo_dict["siteCode"])
        response = requests.request("POST", url_picture, headers=self.headers, data=self.payload)
        try:
            picture_dict = json.loads(response.text)
            if picture_dict:
                picture_time = picture_dict["createTime"]
                picture_lasttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(round(int(picture_time) / 1000)))
                picture_area = picture_dict["areaCode"]
                picture_configureType = picture_dict["configureTypeId"]
                self.nodeinfo_dict["最后一张图片上传时间"] = picture_lasttime
                self.nodeinfo_dict["picture_info"] = {"picture_area": picture_area,
                                                      "picture_configureType": picture_configureType}
            else:
                self.nodeinfo_dict["最后一张图片上传时间"] = "not response"
                self.nodeinfo_dict["picture_info"] = ''
        except Exception as e:
            self.nodeinfo_dict["最后一张图片上传时间"] = "read picture_last_time wrong".format(e)
            self.nodeinfo_dict["picture_info"] = 'none'.format(e)

    def get_last_data(self):

        lastdata_url = "https://cloud.meijingdata.com/iot-manager-server/api/v2/site-datas/latest-data-by-time-type?" \
                       "siteCodes={0}&timeType=realtime".format(self.nodeinfo_dict["siteCode"])
        response = requests.request("GET", lastdata_url, headers=self.headers, data=self.payload)
        try:
            lastdata = json.loads(response.text)
            if lastdata:
                temp = {}
                lastdata_dict = lastdata[0]
                if self.nodeinfo_dict["typeCode"] == "air_box":
                    if lastdata_dict["datas"]["data"]["others"]["a21026_qc"] != "IC":
                        temp.update({"SO2值":lastdata_dict["datas"]["data"]["v_a21026"]})
                    else:
                        temp.update({"SO2值": "NULL"})
                    if lastdata_dict["datas"]["data"]["others"]["a21004_qc"] != "IC":
                        temp.update({"NO2值": lastdata_dict["datas"]["data"]["v_a21004"]})
                    else:
                        temp.update({"NO2值": "NULL"})
                    if lastdata_dict["datas"]["data"]["others"]["a21005_qc"] != "IC":
                        temp.update({"CO值": lastdata_dict["datas"]["data"]["v_a21005"]})
                    else:
                        temp.update({"CO值": "NULL"})
                    if lastdata_dict["datas"]["data"]["others"]["a05024_qc"] != "IC":
                        temp.update({"O3值": lastdata_dict["datas"]["data"]["v_a05024"]})
                    else:
                        temp.update({"O3值": "NULL"})
                    temp.update({"AQI": lastdata_dict["datas"]["data"]["aqi"]})
                    if lastdata_dict["datas"]["data"]["others"]["a34004_qc"] != "IC":
                        temp.update({"PM2.5": lastdata_dict["datas"]["data"]["v_a34004"]})
                    else:
                        temp.update({"PM2.5": "NULL"})
                    if lastdata_dict["datas"]["data"]["others"]["a34002_qc"] != "IC":
                        temp.update({"PM10": lastdata_dict["datas"]["data"]["v_a34002"]})
                    else:
                        temp.update({"PM10": "NULL"})
                    t = round(int(lastdata_dict["datas"]["data"]["time"]) / 1000)
                    lastdata_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
                    self.nodeinfo_dict.update({"最后一条数据上传时间": lastdata_time})
                    self.nodeinfo_dict.update({"最后一条数据": temp})
                elif self.nodeinfo_dict["typeCode"] == "car_box":
                    if lastdata_dict["datas"]["data"]["a21026_qc"] != "IC":
                        temp.update({"SO2值": lastdata_dict["datas"]["data"]["a21026"]})
                    else:
                        temp.update({"SO2值": "NULL"})
                        self.nodeinfo_dict.update({"data_flag": "some data_flag is IC"})
                    if lastdata_dict["datas"]["data"]["a21004_qc"] != "IC":
                        temp.update({"NO2值": lastdata_dict["datas"]["data"]["a21004"]})
                    else:
                        temp.update({"NO2值": "NULL"})
                        self.nodeinfo_dict.update({"data_flag": "some data_flag is IC"})
                    if lastdata_dict["datas"]["data"]["a21005_qc"] != "IC":
                        temp.update({"CO值": lastdata_dict["datas"]["data"]["a21005"]})
                    else:
                        temp.update({"CO值": "NULL"})
                        self.nodeinfo_dict.update({"data_flag": "some data_flag is IC"})
                    if lastdata_dict["datas"]["data"]["a05024_qc"] != "IC":
                        temp.update({"O3值": lastdata_dict["datas"]["data"]["a05024"]})
                    else:
                        temp.update({"O3值": "NULL"})
                        self.nodeinfo_dict.update({"data_flag": "some data_flag is IC"})
                        temp.update({"AQI": lastdata_dict["datas"]["data"]["aqi"]})
                    if lastdata_dict["datas"]["data"]["a34004_qc"] != "IC":
                        temp.update({"PM2.5": lastdata_dict["datas"]["data"]["a34004"]})
                    else:
                        temp.update({"PM2.5值": "NULL"})
                    if lastdata_dict["datas"]["data"]["a34002_qc"] != "IC":
                        temp.update({"PM10": lastdata_dict["datas"]["data"]["a34002"]})
                    else:
                        temp.update({"PM10值": "NULL"})
                    t = round(int(lastdata_dict["datas"]["data"]["time"]) / 1000)
                    lastdata_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
                    self.nodeinfo_dict.update({"最后一条数据上传时间": lastdata_time})
                    self.nodeinfo_dict.update({"最后一条数据": temp})
                else:
                    self.nodeinfo_dict.update({"最后一条数据上传时间": "这不是一个空气盒子"})
                    self.nodeinfo_dict.update({"最后一条数据": "这不是一个空气盒子"})
            else:
                self.nodeinfo_dict.update({"最后一条数据": "none"})
                self.nodeinfo_dict.update({"最后一条数据上传时间": ''})
        except Exception as e:

            self.nodeinfo_dict.update({"最后一条数据": "最后一条数据读取失败:{0}".format(e)})
            self.nodeinfo_dict.update({"最后一条数据上传时间": '最后一条数据上传时间读取失败'})


    def get_24hdatanum(self):
        endtime = round(time.time() * 1000)
        starttime = endtime - 60 * 60 * 24 * 1000

        self.datanum_url = "https://cloud.meijingdata.com/iot-manager-server/api/v2/site-datas/{0}/minute-by-time?startTime={1}" \
                           "&endTime={2}&supplementDataByTime=false".format(self.nodeinfo_dict["siteCode"],
                                                                            str(starttime), str(endtime))

        response = requests.request("GET", self.datanum_url, headers=self.headers, data=self.payload)
        try:
            res = json.loads(response.text)
            if res:

                datanum = str(len(res))
                self.nodeinfo_dict.update({"24h数据上传量": datanum})
            else:
                self.nodeinfo_dict.update({"24h数据上传量": "not response"})
        except Exception as e:
            self.nodeinfo_dict.update({"24h数据上传量": "can not read datanum{0}".format(e)})

    def get_1h_negativedata(self):
        endtime = round(time.time() * 1000)
        starttime = endtime - 60 * 60 * 1000

        self.datanum_url = "https://cloud.meijingdata.com/iot-manager-server/api/v2/site-datas/{0}/minute-by-time?startTime={1}" \
                           "&endTime={2}&supplementDataByTime=false".format(self.nodeinfo_dict["siteCode"],
                                                                            str(starttime), str(endtime))

        response = requests.request("GET", self.datanum_url, headers=self.headers, data=self.payload)
        try:
            res = json.loads(response.text)
            if res:
                so2_negnum = []
                no2_negnum = []
                co_negnum = []
                o3_negnum = []
                upside_down_negnum = []
                temp = {}
                for datas in res:
                    so2 = datas["a21026"]
                    pass
                    if so2 <= 0:
                        so2_negnum.append(so2)
                    else:
                        pass
                    no2 = datas["a21004"]
                    if no2 <= 0:
                        no2_negnum.append(no2)
                    else:
                        pass
                    co = datas["a21005"]
                    if co <= 0:
                        co_negnum.append(co)
                    else:
                        pass
                    o3 = datas["a21005"]
                    if o3 <= 0:
                        o3_negnum.append(co)
                    else:
                        pass
                    pm_25 = datas["a34004"]
                    pm_10 = datas["a34002"]
                    if pm_25 > pm_10:
                        upside_down_negnum.append({pm_25: pm_10})
                    else:
                        pass

                temp.update({"so2-1h负值": len(so2_negnum)})
                temp.update({"co-1h负值": len(co_negnum)})
                temp.update({"no2-1h负值": len(no2_negnum)})
                temp.update({"o3-1h负值": len(o3_negnum)})
                temp.update({"颗粒物-1h倒挂": len(upside_down_negnum)})
                self.nodeinfo_dict.update({"1h负值": temp})

            else:
                self.nodeinfo_dict.update({"1h负值": "not response"})
        except Exception as e:
            self.nodeinfo_dict.update({"1h负值": "can not read datanum{0}".format(e)})

    def get_wrongndoedic_flag(self):
        for flag in self.wrongndoe_flag.items():
            if flag in self.nodeinfo_dict.items():
                self.wrongndoedic_flag = "some is not work right"
                break
            else:
                pass

    def get_nodeid_informationg(self):

        self.get_aibox_info()
        self.get_node_status()
        self.get_node_onlinetime()
        if self.nodeinfo_dict["siteCode"]:
            self.get_edgeConfig()
            self.get_deviceConfig()
            self.get_videoCode()
            self.get_picture_last_time()
            self.get_last_data()
            self.get_24hdatanum()
            self.get_wrongndoedic_flag()
            #self.get_1h_negativedata()#数据不上传负值，
        else:
            self.nodeinfo_dict.update({"siteCode": "siteCode is none, can not read this node info"})





