**一个在线问答项目：**
1. 展示所有的问题列表
2. 可以在线提问（鉴权通过）
3. 展示问题详情
4. 问题下展示所有人针对问题的回答，按照时间倒序排序
5. 可以通过关键字搜索对应的问题



**通过flask 框架 + 第三方开源库开发**






flask-sqlalchamy 实现数据的修改、增加、删除等操作
1. flask db init 进行数据库迁移仓库的建立，会自动创建migrations等目录和必要的文件
2. flask db migrate -m "some message" 用来自动创建一个数据库迁移脚本，会放在migrations/versions下面。因为是自动生成的不一定可靠，建议自己手动再去改改。
3. flask db upgrade 执行上面自动生成脚本中upgrade函数，相当于是把数据库表结构更新成当前models中定义的那样
4. flask db downgrade 执行上面脚本中的downgrade函数，把数据库表结构回滚一次改变。
