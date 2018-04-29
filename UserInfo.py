#!/usr/bin/python

import requests

# IAM 统一身份认证 进行用户身份鉴权
class UserInfo(object):
    def __init__(self, domainName, userName, password, projectId):
        self.domainName = domainName
        self.userName = userName
        self.password = password
        self.projectID = projectId

    # 获取token的header体
    def getRequestHeader(self):
        header = {"Content-Type": "application/json"}
        return header

    def getRequestBody(self):
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
                      "project": {"id": self.projectID }
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

    def getUserToken(self, domainName, userName, password):
        reqUrl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
        header = self.getRequestHeader()
        body = self.getRequestBody()
        iamReq = requests.post(url=reqUrl, headers=header, json=body, )

        if iamReq.status_code == 201:
            print('get iam token success')
            token = iamReq.headers["X-Subject-Token"]
            return token
        else:
            print("get iam token failed")
            print(iamReq.status_code)
            return ""

    def getUserTokenByDomainName(self, domainName, userName, password):
        reqUrl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
        header = self.getRequestHeader()
        body = self.getRequestBodyByDomainName()
        iamReq = requests.post(url=reqUrl, headers=header, json=body, )

        if iamReq.status_code == 201:
            print('get iam domain token success')
            token = iamReq.headers["X-Subject-Token"]
            return token
        else:
            print("get iam domain token failed")
            print(iamReq.status_code)
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
	
#if __name__ == '__main__':
#    user = UserInfo(domainName="hwx535937", userName="groupE", password="hWX535937@2018",
#                    projectId="f5e7454905424cd98204e57b8ef66a3c")
#
#    # token = user.getUserToken("hwx535937", "groupE", "hWX535937@2018")
#    domainToken = user.getUserTokenByDomainName("hwx535937", "groupE", "hWX535937@2018")
#    user.selectUserIdForUserName('1ac7ef22de6d4258aa2157c10cf895f5', domainToken)
#
#
