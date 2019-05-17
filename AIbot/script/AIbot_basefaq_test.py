# _*_ coding: utf-8 _*_

'''20180919'''

import sys
sys.path.append(r"D:\JetBrains\AutoTest")
from AIbot.common import BotRunner

if __name__ == '__main__':

    BotRunner.init_server_value()
    BotRunner.init_baseFaq_value()
    BotRunner.run_chat_test()