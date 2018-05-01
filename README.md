# hwcloud-resource-cleanup

工具功能实现为：
    配合定时任务主动拉取华北区ECS列表详情，检索分属对应iam用户，生成模板短信通知对应组负责人；

# 2018-4-29  commit

定义EcsInfo、UserInfo、smsNotice 类，分别实现：
类初始化方法；
获取token方法（两种）
获取ECS List 详情列表；
查询详情iam 用户方法；
短信通知方法；

# 2018-05-01 commit

UserInfo 修改为单例模式
支持ECSInfo全region资源获取
修改短信通知模板

