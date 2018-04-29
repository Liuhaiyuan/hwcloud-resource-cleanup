#!/usr/bin/python
import EcsInfo
import UserInfo
import requests
import time, json


# regions_headers = {'Content-Type':'application/json;charset=utf8',"X-Auth-Token":r_tocken}
# regions_url = "https://iam.cn-north-1.myhwclouds.com/v3/regions"
# regions = requests.get(url=regions_url,headers=regions_headers)
# print "regions is:",regions
# print "r_tocken :",r_tocken

# 定义发送短信息函数
def sendMessage(projectId, phones, token, message):
    message = message
    url = "https://smn.cn-north-1.myhwclouds.com/v2/" + projectId + "/notifications/sms"
    SMN_headers = {"Content-type": "application/json", "X-Auth-Token": token}  # header

    for phone in phones:  # 接口不允许群发短信，弄个循环搞定,phone取值后type为<str>
        body = {"endpoint": phone, "message": message}  # 消息体json格式，从帮助中心获得！
        smsReq = requests.post(url=url, headers=SMN_headers, json=body)

        if smsReq.status_code == 200:
            print("success"),
            time.sleep(0.1)

        else:
            print("失败")


def getPhones():
    # 西安业务线人员电话 weibo, dongpan, xudong, liukang,
    phones = ['17744469047', '13165750207', '15706017162', '18391250190', "18740706731", "18691575009", "18829597581"]
    # 其他人员，mingda，福寿，芙蓉，亮哥
    #phones = ['18062582937', '15771717728', '13709296375', '13323268512', '17744469047', '13333392837']
    #phones = ['17744469047']
    return phones

def getMessage(ecsLists):
    groupAList = []
    groupBList = []
    groupCList = []
    groupDList = []
    groupEList = []
    groupOthers = []
    messageEcs = "华为云账号hwx535937，子账号ECS资源情况如下:"
    for ecsinfo in ecsLists:
        if ecsinfo.iamUserName == "groupA":
            groupAList.append(ecsinfo)
        elif ecsinfo.iamUserName == "groupB":
            groupBList.append(ecsinfo)
        elif ecsinfo.iamUserName == "groupC":
            groupCList.append(ecsinfo)
        elif ecsinfo.iamUserName == "groupD":
            groupDList.append(ecsinfo)
        elif ecsinfo.iamUserName == "groupE":
            groupEList.append(ecsinfo)
        else:
            groupOthers.append(ecsinfo)

    if len(groupAList) > 0:
        message = "用户groupA，当前有ECS资源" + str(len(groupAList)) + "台。"
        for ecsA in groupAList:
            message += ecsA.ecsName + "(" + ecsA.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message
    if len(groupBList) > 0:
        message = "用户groupB，当前有ECS资源" + str(len(groupBList)) + "台。"
        for ecsB in groupBList:
            message += ecsB.ecsName + "(" + ecsB.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message
    if len(groupCList) > 0:
        message = "用户groupC，当前有ECS资源" + str(len(groupCList)) + "台。"
        for ecsC in groupCList:
            message += ecsC.ecsName + "(" + ecsC.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message
    if len(groupDList) > 0:
        message = "用户groupD，当前有ECS资源" + str(len(groupDList)) + "台。"
        for ecsD in groupDList:
            message += ecsD.ecsName + "(" + ecsD.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message
    if len(groupEList) > 0:
        message = "用户groupE，当前有ECS资源" + str(len(groupEList)) + "台。"
        for ecsC in groupEList:
            message += ecsC.ecsName + "(" + ecsC.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message
    if len(groupOthers) > 0:
        message = "其他用户，当前有ECS资源" + str(len(groupOthers)) + "台。"
        for ecsC in groupOthers:
            message += ecsC.ecsName + "(" + ecsC.ecsCreated + ")"
            message += " , "
        # print(message)
        messageEcs += message

    messageEcs += "。请各组长及时清理,避免浪费。"
    print(messageEcs)

    return messageEcs

if __name__ == '__main__':
    user = UserInfo.UserInfo(domainName="hwx535937", userName="groupE", password="hWX535937@2018",
                    projectId="f5e7454905424cd98204e57b8ef66a3c")

    token = user.getUserToken("hwx535937", "groupE", "hWX535937@2018")
    phones = getPhones()
    ecsClass = EcsInfo.EcsClass()
    ecsLists = ecsClass.getEcsListData()
    message = getMessage(ecsLists)

    sendMessage(projectId=user.projectID, phones=phones, token=token, message=message )

