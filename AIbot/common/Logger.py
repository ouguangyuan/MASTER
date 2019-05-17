'''20180918'''

import datetime
import logging
# from imp import reload
logger = logging.getLogger()

class MyLogger(object):

    def __init__(self, path):
        #获取当前时间
        now = datetime.datetime.now() #这是时间数组格式
        #转换为指定格式：
        timeString = now .strftime('%Y%m%d%H%M%S')
        if path is None:
            path = './'
        if path.endswith('/') or path.ends_with('\\'):
            path = path + timeString
        elif path.index_of('/')>=0:
            path = path + '/' + timeString
        elif path.index_of('\\')>=0:
            path = path + '\\' + timeString
        else:
            path = timeString
        self.logFile = open(path, 'a', encoding = "utf-8")
        logger.log(logging.INFO, "test report: " + path)
        print("test report: " + path)

    def writeTestLog(self, scenename, questions, is_ext, responses_answer, expectr_answer, retcode, expect_code, response1, success):
        '''测试日志'''
        ss = "success"
        cc = "None"
        if retcode is not None:
            cc = str(retcode)
        if not success:
            ss = "failed"

        s = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (scenename, questions, is_ext, responses_answer, cc, expect_code, ss, response1)

        self.logFie.writelinnes(s)
        self.logFile.flush()

    def writeLog(self, logStr):
        '''写入日志文件'''
        self.logFile.writelines(logStr)

    def finishWrite(self):
        '''完成写入日志文件'''
        self.logFile.flush()
        self.logFile.close()

