# NK-eamis
You know what is this and so do I.  

## Node.js
eamis十分奇葩地将含数据的JS脚本作为请求的回复。此项目使用[JSPyBridge](https://github.com/extremeheat/JSPyBridge)调用[Node.js](https://nodejs.org/zh-cn)解码这种回复。  
你需要安装Node.js才能成功运行此项目。Windows用户建议使用[安装器](https://nodejs.org/zh-cn/download/prebuilt-installer)安装，Linux用户建议使用[包管理器](https://nodejs.org/zh-cn/download/package-manager)安装。

## 无头服务器兼容性
由于我尚未逆向飞连的登录API，此项目需要使用webview图形界面登录，暂不支持无头服务器。

## 测试数据
test_data目录下包含一些来自现实的测试数据。  
这些测试数据是被刻意保留的，因为选课每年只开放两次，等选课开放再测试会导致开发效率过低。

## TODO
- 简化课程ID的获取流程
- 写一个预选课UI
- 集成其他相关功能
