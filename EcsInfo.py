# #!/usr/bin/python
# _*_ coding:utf-8 _*_
import UserInfo
import requests
import json
from LoggingClass import HwcloudLog

class EcsClass(object):
    def __init__(self):
        self.ecsName = None         # ecs Nmae
        self.ecsStatus = None       # ecs当前的状态
        self.ecsCreated = None      # 创建ecs的时间
        self.iamUserId = None       # 操作时的对应user id
        self.iamUserName = None
        self.cnNorth1EndPoint = "https://ecs.cn-north-1.myhuaweicloud.com"
        self.cnEast2EndPoint = "https://ecs.cn-east-2.myhuaweicloud.com"
        self.cnSouth1EndPoint = "https://ecs.cn-south-1.myhuaweicloud.com"
        self.cnNortheast1EndPoint = "https://ecs.cn-northeast-1.myhuaweicloud.com"
        self.apSouthEast1EndPoint = "https://ecs.ap-southeast-1.myhwclouds.com"      # hangkang

    # 返回ECS API的请求公共header
    def getPubHeaderForToken(self, projectId, token):
        header = {
            "Content-Type":"application/json",
            "X-Project-Id":projectId,
            "X-Auth-Token":token,
        }
        HwcloudLog().debug("Return ECS API Request Header.")
        return header

    # 请求获取ECS List的函数
    def getEcsListFroNorth(self, ecsPubHeaderForToken):
        projectId_str = ecsPubHeaderForToken["X-Project-Id"]
        getUrl = "https://ecs.cn-north-1.myhuaweicloud.com/v2/" + projectId_str + "/servers"
        getEcsReq = requests.get(url=getUrl, headers=ecsPubHeaderForToken)

        return getEcsReq

    # 获取华北区ESC详情列表
    def getEcsListDetailForNorth(self, ecsPubHeaderForToken):
        projectId_str = ecsPubHeaderForToken["X-Project-Id"]
        getUrl = "https://ecs.cn-north-1.myhuaweicloud.com/v2/" + projectId_str + "/servers/detail"
        getEcsReq = requests.get(url=getUrl, headers=ecsPubHeaderForToken)
        servers = getEcsReq.json()
        return servers

    def getEcsListDetailFromRegin(self, ecsPubHeaderForToken, regionEndPoint):
        projectId_str = ecsPubHeaderForToken["X-Project-Id"]
        getUrl = regionEndPoint + "/v2/" + projectId_str + "/servers/detail"
        getEcsReq = requests.get(url=getUrl, headers=ecsPubHeaderForToken)
        if getEcsReq.status_code == 200:
            servers = getEcsReq.json()
            HwcloudLog().info("get Ecs List Detail from region %s success. " % regionEndPoint)
            return servers
        else:
            HwcloudLog().error("get Ecs List Detail from region %s failure. " % regionEndPoint)
            HwcloudLog().error("statue.code is %s" % getEcsReq.status_code)
            HwcloudLog().error("Error Message is : %s" % getEcsReq.text)
            return []

    def getEcsListDetailFromAllRegin(self):
        userInfo = UserInfo.UserInfo()

        sourthToken = userInfo.getUserTokenByProjectId(regionProjectId=userInfo.sourthProjectId)
        sourthPubHeader = self.getPubHeaderForToken(projectId=userInfo.sourthProjectId, token=sourthToken)
        sourthServers = self.getEcsListDetailFromRegin(ecsPubHeaderForToken=sourthPubHeader, regionEndPoint=self.cnSouth1EndPoint)

        northToken = userInfo.getUserTokenByProjectId(regionProjectId=userInfo.northProjectId)
        northPubHeader = self.getPubHeaderForToken(projectId=userInfo.northProjectId, token=northToken)
        northServers = self.getEcsListDetailFromRegin(ecsPubHeaderForToken=northPubHeader, regionEndPoint=self.cnNorth1EndPoint)

        eastToken = userInfo.getUserTokenByProjectId(regionProjectId=userInfo.eastProjectId)
        eastPubHeader = self.getPubHeaderForToken(projectId=userInfo.eastProjectId, token=eastToken)
        eastServers = self.getEcsListDetailFromRegin(ecsPubHeaderForToken=eastPubHeader,
                                                      regionEndPoint=self.cnEast2EndPoint)

        northEastToken = userInfo.getUserTokenByProjectId(regionProjectId=userInfo.northeastProjectId)
        northEastPubHeader = self.getPubHeaderForToken(projectId=userInfo.northeastProjectId, token=northEastToken)
        northEastServers = self.getEcsListDetailFromRegin(ecsPubHeaderForToken=northEastPubHeader,
                                                      regionEndPoint=self.cnNortheast1EndPoint)

        hongKangToken = userInfo.getUserTokenByProjectId(regionProjectId=userInfo.hangKongProjectId)
        hongKangPubHeader = self.getPubHeaderForToken(projectId=userInfo.hangKongProjectId, token=hongKangToken)
        hongkangServers = self.getEcsListDetailFromRegin(ecsPubHeaderForToken=hongKangPubHeader,
                                                          regionEndPoint=self.apSouthEast1EndPoint)

        servers = []
        servers.append(sourthServers)
        servers.append(northServers)
        servers.append(eastServers)
        servers.append(northEastServers)
        servers.append(hongkangServers)

        HwcloudLog().debug("get ECS List Detial Data From all Region Message is")
        HwcloudLog().debug(servers)
        HwcloudLog().info("获取ECS List 详情页面全region信息。")

        return servers

    # 根据详细ECS list 获取列表，根据业务逻辑，获取对应字段的值。

    def getEcsListData(self):

        userinfo = UserInfo.UserInfo()
        domainToken = userinfo.getUserTokenByDomainName()
        ecsclass = EcsClass()
        getEcsDetailList = ecsclass.getEcsListDetailFromAllRegin()
        ecslist = []
        for regionEcsDetailList in getEcsDetailList:
            servers = regionEcsDetailList["servers"]
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
#     ecs = EcsClass()
#     ecs.getEcsListDetailFromAllRegin()
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

