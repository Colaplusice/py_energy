## 第四个django_project 
关于节能减排的网站搭建：
1. 发布文章的功能
2. 留言板的功能，显示校园内水电报修的信息，供维修人员查看
3. 用户登录注册功能
4. 论坛功能，可以在上面发帖和评论，可以加载图片，可以查看浏览量
、浏览人数、评论数等信息

#设计数据库
message 需要comment 
comment 要将 user pubdate forign_key为message id

每条comment的primary key是id  时间可能不是唯一的 用户不是唯一的
没有类型