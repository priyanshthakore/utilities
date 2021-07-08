### use health.json

import cv2
import json
import datetime
import time
import os
from logging.handlers import TimedRotatingFileHandler
import logging.handlers as handlers
import logging

# with open(os.path.join(os.getcwd(), "health.json")) as json_file:
def intialize_logging():
    console_display = False
    file_write = True
    debug_level = "DEBUG"

    if debug_level == 'DEBUG':
        _level = logging.DEBUG

    if debug_level == 'INFO':
        _level = logging.INFO

    # setting common value
    logger = logging.getLogger()
    logger.setLevel(_level)
    formatter = logging.Formatter('%(asctime)s : %(message)s',
                              "%Y-%m-%d %H:%M:%S")

    # remove all previous added handler
    # if present
    # print(logger.hasHandlers())
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    # again add them accordingly
    if console_display:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if file_write:
        date = datetime.date.today()
        # timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        log_filename = "number_plate.log"
        # timestamp = datetime.datetime.now().strftime("%H-%M-%S")
        log_path = os.path.join(os.getcwd())
        # if not os.path.exists(log_path):
        #     os.makedirs(log_path)

        # file_handler = logging.FileHandler(filename = log_path + '/' + timestamp + '.log')
        file_handler = TimedRotatingFileHandler(
            filename=log_path + '/' + log_filename , when="midnight", interval=1)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
def camera_health():
    global initial_start, number_sources
    temp_false_cam = 0
    temp_total_cam = 0
    temp_camera_health = True

    for key, dict_value in health_monitor.items():
        if key == 'server_config':
            temp_api_ip_port = dict_value["Hostname"]

    api_cam_health_url = str(temp_api_ip_port) + \
        "api/v1/application/camerahealth"

    for key, dict_value in health_monitor.items():
        if key == 'camera_config':
            if not bool(dict_value):
                temp_camera_health = False
                break

            for nkey, ndict in dict_value.items():
                link = ndict["rtsp_link"]
                cap = cv2.VideoCapture(link)
                ret, frame = cap.read()

                # if initial_start:
                #     if ret == True:
                #         dict_value[nkey]["sys_status"] = True
                #     else:
                #         dict_value[nkey]["sys_status"] = False
                    # logging.debug(
                    #     f"Camera ID : {nkey} ; Camera Link : {link} ; Status : {dict_value[nkey]['sys_status']}")
                # else:
                if ret:
                    if not dict_value[nkey]["sys_status"]:
                        data_send = {"Camera_id": nkey,
                                        "Status": "Running"}
                        headers = {'Content-type': 'application/json'}
                        # print(data_send)
                        # result = api_call.api(
                        #     api_cam_health_url, 'PUT', data=data_send, header=headers)
                        # logging.info(
                        #     f"Data Send - {data_send} ;  response - {result}")
                        # debug_logs.debug_log(
                        #     f"API data: {data_send}", nkey)
                        # debug_logs.debug_log(
                        #     f"Camera health API Status:{result}", nkey)

                        dict_value[nkey]["sys_status"] = True
                        dict_value[nkey]["counter"] = 0
                        temp_camera_health = False
                else:
                    if dict_value[nkey]["sys_status"] and dict_value[nkey]["counter"] >= 0:
                        data_send = {"Camera_id": nkey, "Status": "Stop"}
                        # print(data_send)
                        # headers = {'Content-type': 'application/json'}
                        # result = api_call.api(
                        #     api_cam_health_url, 'PUT', data=data_send, header=headers)
                        # logging.info(
                        #     f"Data Send - {data_send} ;  response - {result}")
                        # debug_logs.debug_log(
                        #     f"API data: {data_send}", nkey)
                        # debug_logs.debug_log(
                        #     f"Camera health API Status:{result}", nkey)

                        dict_value[nkey]["sys_status"] = False
                        dict_value[nkey]["counter"] = 0
                        temp_camera_health = False

                    # else:
                    #     health_monitor[cam]['counter'] += 1
                cap.release()

    for key, dict_value in health_monitor.items():
        if key == 'camera_config':
            for nkey, ndict in dict_value.items():
                temp_total_cam += 1
                if not ndict["sys_status"]:
                    temp_false_cam += 1

    if temp_total_cam == temp_false_cam:
        temp_camera_health = False

    return temp_camera_health


with open(os.path.join(os.getcwd(),"health.json")) as json_file:
    health_monitor = json.load(json_file)

intialize_logging()

while True:   
    camera_status = False
    # camera_status = camera_health()
    if camera_status == False:
        for key, dict_value in health_monitor.items():
            if key == "camera_config":
                for nkey, ndict in dict_value.items():
                    # print(f"Camera offline : {nkey} : {ndict['type']} : {datetime.datetime.now()}")
                    logging.debug(f"Camera Type : {ndict['type']}---> Status : {dict_value[nkey]['sys_status']}")
    time.sleep(5)
    logging.debug("***********************************************")