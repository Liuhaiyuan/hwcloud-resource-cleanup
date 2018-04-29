# hwcloud-resource-cleanup

# 2018-4-29  commit

定义EcsInfo、UserInfo、smsNotice 类，分别实现：
类初始化方法；
获取token方法（两种）
获取ECS List 详情列表；
查询详情iam 用户方法；
短信通知方法；

工具功能实现为：
    配合定时任务主动拉取华北区ECS列表详情，检索分属对应iam用户，生成模板短信通知对应组负责人；

# 2018-05-04 下版本预计迭代内容：

优化userInfo类，计划使用单例模式进行用户资料保存和鉴权；
添加全region支持；
