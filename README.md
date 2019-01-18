# doubanrobot

A simple robot for douban.com

## Usage

[Examples](examples.py)

## 功能概览

### 登录

    import doubanrobot

    email = 'xxx@qq.com'
    password = 'password'

    auth = doubanrobot.Auth(email, password)

### 个人相关接口

    people = doubanrobot.People(auth)
    
- 修改简介
`people.edit_intro("i just changed my douban intro")`  

- 发状态
`people.talk_status("hhhhhh")`

- 发豆邮 (对同一人首次发豆邮后该endpoint失效，以后需要使用回复豆邮）
    `people.send_doumail("66902522", 'Hallo, linsir.')` 
    
- 回复豆邮
    `people.reply_doumail("66902522", 'Hallo again, linsir.')` 
    
- 获取关注的人
`print(people.get_contacts_list())`

- 获取关注我的人
print(people.get_contacts_rlist())

- 取消关注
`people.remove_contact("66902522")`

- 关注
`people.add_contact("66902522")`

- 获取黑名单
`print(people.get_blacklist())`

- 添加到黑名单
`people.add_to_blacklist("76326966")`

- 移出黑名单
`people.remove_from_blacklist("76326966")`

### 小组相关接口

    group = doubanrobot.Group(app)

- 获取加入的小组
`print(group.get_joined_groups())`

- 加入不需要验证的组
`group.join_group("TurboGears")`

- 加入需要验证的组
`group.join_group("343477", "申请加入！！！")`

- 退出小组
`group.quit_group("TurboGears")`

- 我发起的帖子列表
`print(group.get_my_publish_topics(reply=False))`

- 我回复的帖子列表及回应数
`print(group.get_my_reply_topics(reply=False))`

- 删除我发起的帖子（会删除所有评论）
`group.delete_my_topic("129875286", 155)`

- 获取帖子评论列表
`group.get_other_comments_list("41603339", 155)`

- 获取帖子我回应评论列表
`group.get_reply_comments_list("81705524")`

- 发表新帖子
`group.new_topic("centos", "test", "hahah.")`

- 抢沙发
`group.sofa("CentOS",['aaaa', 'bbbb', 'cccc'])`

- 顶帖子
`group.topics_up(["129875286"],['xxx', 'yyy', 'zzz'])`

- 删除所有回应的评论
`group.delete_reply_topic_comments()`

- 删除所有发布的帖子
`group.delete_my_publish_topics`

## 更多

验证码破解及更多接口请自己抓包分析。
