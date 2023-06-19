# IPProxyPool
IPProxyPool代理池项目, 改自: [IPProxyPool](https://github.com/qiyeboy/IPProxyPool.git)


api包: 主要是实现http服务器，提供api接口(通过get请求,返回json数据)

data文件夹: 主要是数据库文件的存储位置和qqwry.dat(可以查询ip的地理位置)

db包：主要是封装了一些数据库的操作

spider包：主要是爬虫的核心功能，爬取代理网站上的代理ip

test包：测试一些用例，不参与整个项目的运行

util包：提供一些工具类。IPAddress.py查询ip的地理位置

validator包: 用来测试ip地址是否可用

config.py：主要是配置信息(包括配置ip地址的解析方式和数据库的配置)


修改:
1. ip验证修改为httpx异步方式
2. 增加了部分代理网站,对爬虫解析方式做了相应修改
3. 更新到最新qqwry.dat

