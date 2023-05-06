# coding=gbk
import json
import re
import time
import box.logformat as logformat
import pandas as pd
from kubernetes import client, config
import requests
from requests.auth import HTTPDigestAuth

config.load_kube_config(config_file=r"config/viewer.yml")
v1 = client.CoreV1Api()

def get_format_log(obj):
    obj.get_format_log()

class AIboxPodLog(object):
    def __init__(self):
        self.node_list = []
        self.node_pod_dict = {}
        self.namespace_list = ["yining-kongqi"]
        self.namespace_pod_dict = {}
        self.ccid_dict = {}
        self.podlog_dict = {}
        self.log_flag = {}

    def get_pod_log(self, podname, namespace):
        try:
            pod_log = v1.read_namespaced_pod_log(name=podname, namespace=namespace,
                                                 pretty=True, tail_lines=200, _request_timeout=2)
            if pod_log.__contains__("error") or pod_log.__contains__("ERROR"):
                app_error = logformat.ERROR_deal(pod_log)
                get_format_log(app_error)
                pod_log = app_error.format_log
                self.log_flag.update({podname: "应用日志中存在报错"})
            else:
                self.log_flag.update({podname: "日志读取正常"})

        except Exception as e:
            pod_log = {"应用日志读取报错error：{0}".format(e)}
            self.log_flag.update({podname: "应用日志读取出现报错"})

        return pod_log

    def get_format_podlog(self, podname, namespace):
        pod_info = v1.read_namespaced_pod(podname, namespace)
        format_pod_log = {}
        if pod_info.metadata.labels["app"] == 'meijing-edge-watchdog':
            self.log_flag.update({podname: "看门狗日志"})
            try:
                pod_log = v1.read_namespaced_pod_log(name=podname, namespace=namespace,
                                                     pretty=True, tail_lines=200, _request_timeout=2)
                app = logformat.Edge_watchdog(pod_log)
                get_format_log(app)
                format_pod_log = app.format_log
                self.ccid_dict.update({podname: format_pod_log["CCID号"]})
                # return format_pod_log

            except Exception as e:
                format_pod_log = "读取应用类型报错 error：{0}".format(e)

        else:
            pod_log = self.get_pod_log(podname, namespace)
            if str(pod_log).__contains__("error"):
                format_pod_log = pod_log

            else:
                try:
                    pod_type = pod_info.metadata.labels["app"]
                    if pod_type == 'meijing-air-server':
                        app = logformat.AIR_server(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'meijing-edge-watchdog':
                        app = logformat.Edge_watchdog(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log
                        self.ccid_dict.update({podname: format_pod_log["CCID号"]})

                    elif pod_type == 'sensor-data-collect':
                        app = logformat.Sensor_data_collect(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'road-traffic':
                        app = logformat.Rod_traffic(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'baresoil-recognition':
                        app = logformat.Baresoil_recognition(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'fire-smoke':
                        app = logformat.Fire_somke(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'outdoor-barbecue':
                        app = logformat.Outdoor_barbecue(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'meijing-build-server':
                        app = logformat.Build_server(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'meijing-car-air-server':
                        app = logformat.Car_air_server(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'shaoxing-cars-movebox':
                        app = logformat.Shaoxing_cars_movebox(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'meijing-muck-screen-web':
                        app = logformat.Muck_screen_web(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    elif pod_type == 'meijing-slagcar-server':
                        app = logformat.Slagcar_server(pod_log)
                        get_format_log(app)
                        format_pod_log = app.format_log

                    else:
                        format_pod_log = {"pod_log": "can not deal this is pod yet!"}  #
                except Exception as e:
                    format_pod_log = "读取应用类型报错 error：{0}".format(e)

        return format_pod_log

    def get_node_pod_dict(self):
        nodes = v1.list_node().items

        for node in nodes:
            pod_list = []
            pod_dict = {}
            if "box.meijingdata.com/namespace" in node.metadata.labels:
                namespace = node.metadata.labels["box.meijingdata.com/namespace"]

                for pod in v1.list_namespaced_pod(namespace=namespace,
                                                  field_selector=f"spec.nodeName={node.metadata.name}").items:
                    pod_list.append(pod.metadata.name)

                if pod_list:
                    for pod_name in pod_list:
                        pod_log_format = self.get_format_podlog(pod_name, namespace)
                        podlog_dict = {"podlog": pod_log_format, "namespace": namespace,
                                       "log_flag": self.log_flag[pod_name]}
                        pod_dict.update({pod_name: podlog_dict})
                if not pod_list:
                    pod_dict = {"podlog": "pod下面没有应用"}
            else:
                pod_dict = {"podlog": "这个pod没有命名空间", "namespace": "missing"}
                # podlist.append(pod.metadata.name)
            # print(pod_dict)
            self.node_pod_dict.update({node.metadata.name: pod_dict})

def read_log(nodeid):
    nodeid = nodeid.lower()
    node = v1.read_node(nodeid)
    log_list = []
    if "box.meijingdata.com/namespace" in node.metadata.labels:
        namespace = node.metadata.labels["box.meijingdata.com/namespace"]

        for pod in v1.list_namespaced_pod(namespace=namespace,
                                          field_selector=f"spec.nodeName={node.metadata.name}").items:
            # pod_list.append(pod.metadata.name)
            podname = pod.metadata.name
            podlog = AIboxPodLog()
            podlog_f = podlog.get_format_podlog(podname, namespace)
            list = [nodeid, podname, podlog_f, podlog.log_flag]
            log_list.append(list)
    return log_list

