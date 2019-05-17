'''
Created:2018.9.7
'''

import requests
import json
import re
import logging



logger = logging.getLogger()

def api_test(method, url, postplace, data, headers):
    print("requesting: " + url)
    try:
        if method == "post":
            if postplace == "params":
                results = requests.post(url, params=data, headers=headers)
            elif postplace == "multipart":
                filesDict={}
                if data is not None:
                    for key, value in data.items():
                        filesDict[key] = (None, value)
                results = requests.post(url, files=filesDict, headers=headers)

            else:
                results = requests.post(url, data=data, headers=headers)
        if method == "get":
            results = requests.get(url, params=data, headers=headers)
        if method == "delete":
            results = requests.delete(url, params=data, headers=headers)
        if method == "put":
            results.put(url, params=data, headers=headers)
        response = results.json()
        print(response)
        return response

    except Exception as e:
        logger.error("service is error", e)
        print(e)


def deal_expect(response1, param):
    try:
        if "data" in param:
            if "dialog" in param:
                si = json.loads(eval("response1" + param))
                sss1 = str(s1[0]["text"]).replace('\\n', '')
                return sss1
            else:
                s1 = eval("response1" + param)
                ss1 = s1.replace('["', '')
                sss1 = ss1.replace('"]', '')
                sss2 = sss1.replace('\\n', '')
                outStr2 = ''.join(re.findall(r'[\u4e00-\u9fa5]', sss2))
                if "content" in s1:
                    s2 = json.load(s1)
                    ss2 = str(s2[0]["content"]).replace("['", "")
                    sss2 = ss2.replace("']", "")
                    sss3 = sss2.replace('\\n', '')
                    outStr3 = ''.join(re.findall(r'[\u4e00-\u9fa5]', sss3))
                    return outStr3

                else:
                    return outStr2
        else:
            s1 = eval("response1"+param)
            s1 = str(s1).replace('\\n', '')
            outStr1 = ''.join(re.findall(r'[\u4e00-\u9fa5]', s1))
            return outStr1

    except Exception as e:
        logger.error("service is error", e)
        print(e)

