'''20180918'''

class SceneA(object):
    '''classdocs'''


    def __init__(self):
        '''constructor'''
        self.name= ""
        self.questionList = list()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = self.name + "\n"
        for q in self.questionList:
            s = s + "," + str(q)
        return s




    
