# #!/usr/bin/python
# _*_ coding:utf-8 _*_
import UserInfo
import requests
import json

class EcsClass(object):
    def __init__(self):
        self.ecsName = None         # ecs Nmae
        self.ecsStatus = None       # ecs当前的状态
        self.ecsCreated = None      # 创建ecs的时间
        self.iamUserId = None       # 操作时的对应user id
        self.iamUserName = None

    # 返回ECS API的请求公共header
    def getPubHeaderForToken(self, projectId, token):
        header = {
            "Content-Type":"application/json",
            "X-Project-Id":projectId,
            "X-Auth-Token":token,
        }
        return header

    # 请求获取ECS List的函数
    def getEcsListFroNorth(self, ecsPubHeaderForToken):
        projectId_str = ecsPubHeaderForToken["X-Project-Id"]
        getUrl = "https://ecs.cn-north-1.myhuaweicloud.com/v2/" + projectId_str + "/servers"
        getEcsReq = requests.get(url=getUrl, headers=ecsPubHeaderForToken)

        return getEcsReq

    def getEcsListDetailForNorth(self, ecsPubHeaderForToken):
        projectId_str = ecsPubHeaderForToken["X-Project-Id"]
        getUrl = "https://ecs.cn-north-1.myhuaweicloud.com/v2/" + projectId_str + "/servers/detail"
        getEcsReq = requests.get(url=getUrl, headers=ecsPubHeaderForToken)
        servers = getEcsReq.json()
        return servers


    # 根据详细ECS list 获取列表，根据业务逻辑，获取对应字段的值。

    def getEcsListData(self):

        userinfo = UserInfo.UserInfo()
        token = userinfo.getUserToken()
        domainToken = userinfo.getUserTokenByDomainName()
        ecsclass = EcsClass()
        ecsPubHeader = ecsclass.getPubHeaderForToken(projectId=userinfo.northProjectId, token=token)
        getEcsDetailList = ecsclass.getEcsListDetailForNorth(ecsPubHeaderForToken=ecsPubHeader)
        servers = getEcsDetailList["servers"]
        ecslist = []
        for server in servers:
            ecsinfo = EcsClass()
            ecsinfo.ecsName = server["name"]
            ecsinfo.ecsCreated = server["created"]
            ecsinfo.ecsStatus = server["status"]
            ecsinfo.iamUserId = server["user_id"]
            ecsinfo.iamUserName = userinfo.selectUserIdForUserName(iamUserId=ecsinfo.iamUserId, token=domainToken)

            ecslist.append(ecsinfo)

        return ecslist


# if __name__ == '__main__':
#    projectId_str = 'f5e7454905424cd98204e57b8ef66a3c'
#    userinfo = UserInfo.UserInfo(domainName="hwx535937", userName="groupE", password="hWX535937@2018",
#                    projectId=projectId_str)
#
#    token = userinfo.getUserToken("hwx535937", "groupE", "hWX535937@2018")
#
#    ecsclass = EcsClass()
#    ecsPubHeader = ecsclass.getPubHeaderForToken(projectId=projectId_str, token=token)
#
#    servers = ecsclass.getEcsListDetailForNorth(ecsPubHeaderForToken=ecsPubHeader)

