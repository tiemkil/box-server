import requests
import json
import box.AIBOXINFORMATION
import box.AIbox_pod_log
def get_token():
    '''
    获取并返回token
    :return:
    '''
    login_url = "https://cloud.meijingdata.com/simple-user-server/api/v1/auth/login"
    login_payload = "{phone:\"18008172431\",password:\"fpi@1234\",type:\"account\"}"
    login_headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Authorization=eyJhbGciOiJSUzI1NiJ9.eyJpZCI6NDUyNSwiYWNjb3VudCI6IjE4MDA4MTcyNDMxIiwibmlja25hbWUiOiLpurvng6bkvaDorqTnnJ_ngrkiLCJuYmYiOjE2NzY1Mjk5NjgsImV4cCI6MTY3NjYxNjY2OCwianRpIjoiMWQ1NzRhZDYtODcyNS00M2U2LTg4NDItZThmYmViNTY2MWIyIn0.clcY6WwWZfiDezRNu8FtOtct2goxnMICSRIuw144nb-BrvYN7Po3hOeH9fQv4ZvA9rpewnbXAfylpMIMWk7AGkQnhPCX9vLXhn1s3ELRv-aQisnUU9W0gp4kZyI6c3dI5WyGHAPERBXDlV-fn5nbAsJ51uVGALxeXsmV1kpxgRzIjk_M_l5q_8HDYPD_eOF538TUo4HH-NgXsOhos7xwfeOvbQu6mSTARLa9l20hyg_O17RbCxZUTEBn0m5dkbIOAvnVnDEfaHJ8klMDFwBbIFUjLUStkzHZ9tR1TQCWUYDdx87KCaI6qNk3Vor7rwAji8zwAakECfbZ-uIkdFpr3g'
    }
    response = requests.request("POST", login_url, headers=login_headers, data=login_payload)
    res = json.loads(response.text)
    return res["token"]

def get_nodeinfo(nodeid):
    """
    将nodeid改为小写，读取node信息并返回
    :param nodeid:
    :return:
    """
    nodeid = nodeid.lower()
    token = get_token()
    node = box.AIBOXINFORMATION.AIboxinformation(nodeid, token)
    node.get_nodeid_informationg()
    nodeinfo = node.nodeinfo_dict
    print(nodeinfo)

    return nodeinfo

def get_podlog(nodeid):
    nodeid = nodeid.lower()
    podlog = box.AIbox_pod_log.read_log(nodeid)
    return podlog

