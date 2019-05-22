'''20180918'''

import logging
import xlrd
from AIbot.common.BotScene import SceneA
from AIbot.common.BotQuestion import QuestionA


logger = logging.getLogger("django")


def read_sceneExcel(excel_file, yiyi_sheet):
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_name(yiyi_sheet)

    logger.info("load sheet..")
    sceneDict = {}
    #按列读取
    for j in range(sheet.ncols):
        #跳过第一列
        if j < 1: continue
        sceneName = get_excel_value(sheet, 0, j)
        if sceneName not in sceneDict.keys():
            sceneDict[sceneName] = SceneA()
            sceneDict[sceneName].name = sceneName

        scene = sceneDict[sceneName]
        q = QuestionA()
        q.answer = get_excel_value(sheet, 1, j)
        q.json = get_excel_value(sheet, 2, j)
        q.standardQuestion = get_excel_value(sheet, 3, j)
        for i in range(sheet.nrows):
            if i < 4: continue
            ext = get_excel_value(sheet, i, j)
            if ext != "":
                q.extList.append(ext)
        scene.questionList.append(q)

    return sceneDict

def read_chatExcel(excel_file, yiyi_sheet):
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_name(yiyi_sheet)

    logger.info("load sheet..")
    qList = []
    col1 = None
    col2 = None
    col3 = None

    for j in range(sheet.ncols):
        if get_excel_value(sheet, 0, j) == "标准问题":
            col1 = j
        if get_excel_value(sheet, 0, j) == "对外答案":
            col2 = j
        if get_excel_value(sheet, 0, j) == "客户问题":
            col3 = j

    #按行读取
    for i in rang(sheet.nrows):
        #跳过第一行
        q = QuestionA()
        if i < 1:continue
        q.standardQuestion = get_excel_value(sheet, i, col1)
        q.answer = get_excel_value(sheet, i, col2)
        if col3 != None:
            if get_excel_value(sheet, i, col3) != "":
                ext = get_excel_value(sheet, i, col3)
                if "|" in ext:
                    q.extList = ext.sqlit("|")
                else:
                    q.extList.append(ext)
        q.json = ""
        qList.append(q)

	print(qList)
#   print(len(qList))

    return qList





