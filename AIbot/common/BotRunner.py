'''20180918'''

from configparser import ConfigParser as Parser
from AIbot.common import BotLogger
import logging
from AIbot.common.Botapi_request import api_test, deal_expect
from AIbot.common import Botread_excel
import json
import random
import re
import time

logger = logging.getLogger()
Conf_file = '../data/config.txt'

def init_server_value():
    cf = Parser()
    cf.read(Conf_file, encoding="utf-8")
    global chat_url, chat_method, chat_postplace, header_conf, expect_code, prologue_url
    chat_url = cf.get("server_conf", "chat_url").strip()
    chat_method = cf.get("server_conf", "chat_method").strip()
    chat_postplace = cf.get("server_conf", "chat_postplace").strip()
    header_conf = cf.get("server_conf", "headers").strip()
    expect_code = cf.get("server_conf", "expect_code").strip()
    prologue_url = cf.get("server_conf", "prologue_url").strip()


def init_eLifeInsurance_value():
    cf = Parser()
    cf.read(Conf_file, encoding="utf-8")
    global excel_file, yiyi_sheet, sessionId, sceneId, type_conf, responseParm
    excel_file = cf.get("eLifeInsurance_conf", "excel_file").strip()
    yiyi_sheet = cf.get("eLifeInsurance_conf", "excel_file").strip()
    sessionId = cf.get("eLifeInsurance_conf", "sessionId").strip()
    sceneId = cf.get("eLifeInsurance_conf", "sceneId").strip()
    clientId = cf.get("eLifeInsurance_conf", "clientId").strip()
    type_conf = cf.get("eLifeInsurance_conf", "type_conf").strip()
    responseParam = cf.get("eLifeInsurance_conf", "responseParam").strip()

def init_giftInsurance_value():
    cf = Parser
    cf.read(Conf_file, encoding="utf-8")
    global excel_file, yiyi_sheet, sessionId, sceneId, clientId, type_conf, responseParm
    excel_file = cf.get("giftInsurance_conf", "excel_file").strip()
    yiyi_sheet = cf.get("giftInsurance_conf", "yiyi_sheet").strip()
    sessionId = cf.get("giftInsurance_conf", "sessionId").strip()
    sceneId = cf.get("giftInsurance_conf", "sceneId").strip()
    clientId = cf.get("giftInsurance_conf", "clientId").strip()
    type_conf = cf.get("giftInsurance_conf", "type_conf").strip()
    responseParam = cf.get("giftInsurance_conf", "gift_response").strip()


def init_chat_value():
    cf = Parser()
    cf.read(Conf_file, encoding="utf-8")
    global excel_file, yiyi_sheet, sessionId, sceneId, clientId, type_conf, responseParam
    # global sessionId, sceneId, clientId, type_conf, responseParam
    excel_file = cf.get("chat_conf", "excel_file").strip()
    yiyi_sheet = cf.get("chat_conf", "yiyi_sheet").strip()
    sessionId = cf.get("chat_conf", "sessionId").strip()
    sceneId = cf.get("chat_conf", "sceneId").strip()
    clientId = cf.get("chat_conf", "clientId").strip()
    type_conf = cf.get("chat_conf", "type_conf").strip()
    responseParam = cf.get("chat_conf", "chat_response").strip()


def init_baseFaq_value():
    cf = Parser()
    cf.read(Conf_file, encoding="utf-8")
    global excel_file, yiyi_sheet, sessionId, sceneId, type_conf, responseParam
    excel_file = cf.get("baseFaq_conf", "excel_file").strip()
    yiyi_sheet = cf.get("baseFaq_conf", "yiyi_sheet").strip()
    sessionId = cf.get("baseFaq_conf", "sessionId").strip()
    sceneId = cf.get("baseFaq_conf", "sceneId").strip()
    clientId = cf.get("baseFaq_conf", "clientId").strip()
    type_conf = cf.get("baseFaq_conf", "type_conf").strip()
    responseParam = cf.get("baseFaq_conf", "baseFaq_response").strip()



def random_string():
    '''return:返回随机字符串'''
    sd = ""
    sj0 = sd.join(random.sample)(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o' , 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], 5
    )
    datetime = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time))
    sj1 = ''.join((datetime, sj0))
    return sj1

def init_sessionId(scene):

    clientId = random_string()
    sceneId = scene

    datadict = dict()
    datadict["clientId"] = clientId
    datadict["sceneId"] = sceneId

    datadict1 = json.dumps(datadict)
    header_conf2 = eval(header_conf)

    try:
        prologue_responses = api_test(chat_method, prologue_url, chat_postplace, datadict1, header_conf2)

        if prologue_responses.get("code") == expect_code:
            r1 = prologue_responses.get("data")
            global new_sessionId, new_clientId, new_sceneId
            new_sessionId = r1["sessionId"]
            new_clientId = r1["clientId"]
            new_sceneId = r1["sceneId"]

    except Exception as e:
        logger.error("service is error", e)
        print(e)

def request_test(scenename, questions, expect_answer, responseParam, mylogger, is_ext):
    failC = 0
    requestdata = dict()
    requestdata["question"] = questions
    requestdata["type"] = type_conf
    # requestdata["sessionId"] = sessionId
    # requestdata["clientId"] = clientId
    # requestdata["sceneId"] = sceneId
    requestdata["sessionId"] = new_sessionId
    requestdata["clientId"] = new_clientId
    requestdata["sceneId"] = new_sceneId

    requestdata1 = json.dumps(requestdata)
    header_conf1 = eval(header_conf)

    response1 = api_test(chat_method, chat_url, chat_postplace, requestdata1, header_conf1)
    code = response1.get("code")

    if code == "00":
        responses_answer = deal_expect(response1, responseParam)
        #print(responses_answer)
        if responses_answer != expect_answer:
            failC += 1
            mylogger.writeTestLog(scenename, questions, is_ext, responses_answer, expect_answer, code, expect_code, response1, False)

        else:
            mylogger.writeTestLog(scenename, questions, is_ext, responses_answer, expect_answer, code, expect_code, response1, True)

    else:
        failC += 1
        responses_answer = response1.get("msg")
        mylogger.writeTestLog(scenename, questions, is_ext, responses_answer, expect_answer, code, expect_code, response1,False)

    return failC

def run_scense_test():
    sceneDict = Botread_excel.read_sceneExcel(excel_file, yiyi_sheet)
    mylogger = BotLogger.MyLogger("./")
    fail = 0
    lenCase = 0
    for scene in sceneDict.values():
        #if scene.name == "异议处理" or scene.name =="场景意图话术"
        if scene.name == "异议处理":
            for q in scene.questionList:
                print("running test case begin:" + str(q.answer))
                is_ext = "no"
                lenCase += 1
                global expect_answer
                expect_answer = str(q.answer).replace9('\n', '')
                expect_answer = ''.join(re.findall(r'[\u4e00-\u9fa5]', expect_answer))
                init_sessionId("eLisfeInsurance")
                fail = fail + request_test(scene.name, q.standardQuestion, expect_answer, responseParam, mylogger, is_ext)

                if len(q.extList) != 0:
                    for ext in q.extList:
                        is_ext = "yes"
                        if "|" in ext:
                            extA = ext.split("|")
                            for ph in extA:
                                init_sessionId("eLifeInsurance")
                                fail = fail + request_test(scene.name, ph, expect_answer, responseParam, mylogger, is_ext)
                                lenCase += 1
                        else:
                            init_sessionId("eLifeInsurance")
                            fail = fail + request_test(scene.name, ext, expect_answer, responseParam, mylogger, is_ext)
                            lenCase += 1

    c = lenCase
    descript = "\ntotal %d test case, success $d, fail %d, %.2f" % (c, c - fail, fail, ((c-fail)/c))
    mylogger.writeLog(descript)
    mylogger.finishWrite()
    logger.log(logging.INFO, descript)


def run_chat_test():
    qList = Botread_excel.read_chatExcel(excel_file, yiyi_sheet)
    mylogger = BotLogger.MyLogger("./")
    fail = 0
    lenCase = 0
    sceneName = "闲聊"

    for q in qList:
        print("running test case begin:" + str(q.standardQuestion))
        # init_sessionId("giftInsurance")
        # init_sessionId("eLifeInsurance")
        init_sessionId("")
        is_ext = "no"
        lenCase += 1
        global expect_answer
        expect_answer = str(q.answer).replace('\n', '')
        expect_answer = ''.join(re.findall(r'[\u4e00-\u9fa5]', expect_answer))
        #print(expect_answer)
        fail = fail + request_test(sceneName, str(q.standardQuestion),expect_answer, responseParam, mylogger, is_ext)

        if len(q.extList) != 0:
            for ext in q.extList:
                #print(ext)
                is_ext = "yes"
                if "|" in ext:
                    extA = ext.spilt("|")
                    #print(extA)
                    for ph in extA:
                        init_sessionId("")
                        # init_sessionId("giftInsurance")
                        # init_sessionId("eLifeInsurance")
                        fail = fail + request_test(sceneName, str(ph), expect_answer, responseParam, mylogger, is_ext)
                        lenCase += 1
                else:
                    init_sessionId("")
                    # init_sessionId("giftInsurance")
                    # init_sessionId("eLifeInsurance")
                    fail = fail + request_test(sceneName, str(ext), expect_answer, responseParam, mylogger, is_ext)
                    lenCase +=1

    c = lenCase
    descript = "\ntotal %d test case, success %d, fail %d, %,2f" % (c, c - fail, fail, ((c-fail)/c))
    mylogger.writeLog(descript)
    mylogger.fainishWrite()
    logger.log(logging.INFO, descript)




