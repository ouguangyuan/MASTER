# _*_ coding: utf-8 _*_


class QuestionA(object):
    def __init__(self):
        self.answer = ""
        self.standardQuestion = ""
        self.json = ""
        self.extList = list()

    def __str__(self):
        s = "================================\n"
        s = s + self.answer+",\n"+self.standardQuestion+",\n"+self.json
        for e in self.extLIst:
            s = s + ",\n"+e
        return s