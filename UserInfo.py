#!/usr/bin/python

import requests
import threading
from LoggingClass import HwcloudLog


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass


    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


class UserSingleton(Singleton):
    userName = "liuhaiyuan"
    password = "Haiyuan9047@#"
    domainName = "hwcloudsom1"

# IAM 统一身份认证 进行用户身份鉴权
class UserInfo(Singleton):
    domainName = "hwx535937"
    userName = "groupE"
    password = "hWX535937@2018"
    northProjectId = "f5e7454905424cd98204e57b8ef66a3c"
    eastProjectId = "3c113ff1ceae45728aab1017eda97404"
    northeastProjectId = "57ccab022fe140b398c0894285342582"
    sourthProjectId = "05eff5fc7889491e9272c1316bd7600f"
    hangKongProjectId = "d25ffdcd5e764c9c8a565b98874c2c2c"


    # def __init__(self, domainName, userName, password, projectId):
    #     self.domainName = domainName
    #     self.userName = userName
    #     self.password = password
    #     self.projectID = projectId

    # 获取token的header体
    def getRequestHeader(self):
        header = {"Content-Type": "application/json"}
        return header

    def getRequestBodyByProjectId(self, regionProjectId):
        body = {
                  "auth": {
                    "identity": {
                      "methods": ["password"],
                      "password": {"user": {
                          "name": self.userName,
                          "password": self.password,
                          "domain": {"name": self.domainName}
                        }
                      }
                    },
                    "scope": {
                      "project": {"id": regionProjectId }
                    }
                  }
                }
        return body

    def getRequestBodyByDomainName(self):
        body = {
                  "auth": {
                    "identity": {
                      "methods": ["password"],
                      "password": {"user": {
                          "name": self.userName,
                          "password": self.password,
                          "domain": {"name": self.domainName}
                        }
                      }
                    },
                    "scope": {
                      "domain": {"name": self.domainName}
                    }
                  }
                }
        return body

    def getUserTokenByProjectId(self, regionProjectId):
        reqUrl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
        header = self.getRequestHeader()
        body = self.getRequestBodyByProjectId(regionProjectId=regionProjectId)
        iamReq = requests.post(url=reqUrl, headers=header, json=body, )

        if iamReq.status_code == 201:
            HwcloudLog().info("get iam token success by project id.")
            token = iamReq.headers["X-Subject-Token"]
            HwcloudLog().debug("token values is %s" % token)
            return token
        else:
            HwcloudLog().error("get iam token failed by project id, return none.")
            HwcloudLog().error(iamReq.status_code)
            HwcloudLog().error(iamReq.text)
            return ""

    def getUserTokenByDomainName(self):
        reqUrl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
        header = self.getRequestHeader()
        body = self.getRequestBodyByDomainName()
        iamReq = requests.post(url=reqUrl, headers=header, json=body, )

        if iamReq.status_code == 201:
            HwcloudLog().info('get iam domain token success')
            token = iamReq.headers["X-Subject-Token"]
            HwcloudLog().debug("token values is %s" % token)
            return token
        else:
            HwcloudLog().error("get iam domain token failed")
            HwcloudLog().error(iamReq.status_code)
            HwcloudLog().error(iamReq.text)
            return ""


    def selectUserIdForUserName(self, iamUserId, token):
        # reqUrl = 'https://iam.myhuaweicloud.com/v3/users/' + iamUserId
        reqUrl = "https://iam.cn-north-1.myhwclouds.com/v3/users/" + iamUserId

        iamPubHeader = {"Content-Type": "application/json;charset=utf8",
                        "X-Auth-Token": token}
        iamReq = requests.get(url=reqUrl, headers=iamPubHeader)
	#print(iamReq.text)
 	#print(iamReq.text)
        if iamReq.status_code == 200:
            return iamReq.json()["user"]["name"]
        else:
            return "ortherUser"       
	# print(iamReq.json()["user"]["name"])
        #return iamReq.json()["user"]["name"]

