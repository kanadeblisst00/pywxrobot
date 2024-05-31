## 简介

Python的微信机器人，内核由C++编写，并使用aardio加载Python提供脚本扩展功能。C++内核不开源，只提供exe和Python写的扩展插件。

#### hook实现

hook使用的是windows的VEH异常处理机制(和安卓的硬件断点hook类似)，不会修改内存字节码，所以会无痕一点，可以减小封号的风险。

当然，封号并非只靠客户端来判断，还有服务端的异常行为判断，所以无法保证百分百不封号。

## 使用步骤

#### 依赖环境

微信(版本3.9.6.32) 

下载地址: https://www.123pan.com/s/ihEKVv-u4Ox.html 提取码:yw41

里面有两个文件，zip是从exe用7zip解压得到的，可以作为绿色版直接使用。

#### 配置文件

在config.ini里填写相应的配置：

- 授权码(`license`)

授权码请联系微信`kanadeblisst`获取，有两个月的试用期，后面会按月付费。好不好用封不封号试用期两个月肯定能感觉出来，后面如果觉得不好用不续费即可。

#### 启动

先以**管理员权限**启动微信并登录, 打开`pywxrobot.exe`就会加载pyrobot目录下的`main.py`，相对于运行`python main.py`，只不过是从aardio层提供了一些内置函数给python使用。

`main.py`里的代码只是用于初始化插件，也就是plugins目录里的代码。

#### pyrobot目录结构

- .vscode: vscode的配置，用于配置语法提示
- packages: 依赖的一些其他包可以放在这个目录，这个目录默认已经加到sys.path
- plugins: 插件目录，可以是py文件或者文件夹(需包含__init__.py)。
- settings: 配置文件目录，文件名需和插件名一样
- test: 没什么用，我写的一些测试脚本
- .env: 可以设置packages的路径，这样引用packages里的包在vscode里就有语法提示了
- main.py: 启动文件
- requirements.txt: 依赖包，编写版Python已经携带。如果想用安装版Python需要自己安装这些依赖

#### 已有的插件列表

* `auto_accept_friend.py`: 自动接受好友请求
* `auto_download_file.py`: 自动下载聊天文件
* `auto_download_img.py`: 自动下载聊天图片，可以配置auto_download_img.json里的save_path来解密保存到其他目录
* `auto_download_video.py`: 自动下载聊天视频
* `auto_recv_transfer.py`: 自动接收转账
* `auto_save_emotion.py`: 将接收到的表情包保存到指定路径，
* `auto_save_voice.py`: 将收到的语音保存到指定路径(格式silk)
* `debug.py`: 控制台和日志打印所有消息，可通过配置文件关闭
* `echo_revoke_msg.py`: 打印撤回的消息
* `enter_room_tip.py`: 设置进群提示语，例子请看配置文件
* `interactive_console.py`: 如果启用，会在控制台开启一个python的交互式终端
* `keyword_invite_to_room.py`: 根据关键词邀请进群，会判断两个内容，聊天消息和加好友的验证消息
* `sysmsg_manager.py`: 内置插件，不需要管
* `xml_manager.py`: 内置插件，不需要管

## 如何开发

#### 编写插件

首先需要知道两个点：

- 如何获取到聊天消息
- 如何主动调用函数

编写好的插件放到`pyrobot/plugins`目录,然后关闭重新打开`pywxrobot.exe`就会生效

#### 如何获取到聊天消息

`broadcast_service.listen(消息类型, 处理函数)` 

当收到这个类型的消息，就会调用处理函数，具体可以参考其他插件的写法。每个处理函数是一个单独的线程，使用公共资源时需要加锁。

所有消息的类型定义在`wxstruct.py`里的`MsgType`、`XmlMsgType`和`SysMsgType`

MsgType有以下属性:

- `TEXT`: 文本消息
- `IMAGE`: 图片消息
- `VIDEO`: 视频消息
- `VOICE`: 语音消息
- `ADDFRIEND`: 好友请求
- `CARD`: 名片消息
- `EMOTION`: 表情消息
- `LOCATION`: 位置消息
- `XML`: XML消息，可能是文件、转账、文章、小程序、聊天记录等
- `VOIP` :  语音、视频通话
- `NOTICE`: 通知消息，可能是进群提示、红包、拍一拍等
- `SYSMSG`: 系统消息, 很多我也不知道是什么

`xml_manager`插件会进一步处理XML类型消息，生成以下类型消息:

- `BIZMSG`: 分享的文章
- `FILE`: 文件
- `SHARE_LOCATION`: 位置共享
- `MULTI_MSG`: 合并发送的多条消息
- `STEP_RANK_MSG`: 微信运行发送的步数消息
- `APPMSG`: 分享的小程序
- `FEED`:  视频号
- `REFERENCE_MSG`: 引用回复
- `ROOM_ANNOUNCEMENT`: 群公告
- `TRANSFER`: 转账

如果有些消息没有定义，你可以在`wxstruct.py`里定义一个名称，值是消息里msg_type的值。定义完成后，`broadcast_service.listen`就可以监听该类型的消息。


#### 如何导入外部依赖

如果是安装版，用pip安装即可。如果是便携版，你需要从安装版里复制出来放到packages下。有些库这么操作可能会报错，这个自行解决或者直接使用安装版。

#### 如何主动调用函数

导出微信函数的模块名是`wxfunc`，所有函数列表可以看`wxfunc.pyi`，[导出函数文档](/docs/wxfunc.md)

例如你想在插件里发送文本消息:
```python
import wxfunc

wxfunc.SendTextMsg("filehelper", "测试消息")
```

## 待补充

详细版的文档后面补充，后面的更新插件会在: `https://github.com/kanadeblisst00/pywxrobot`

#### 特殊功能

还有一些隐藏功能后面在发布，现在还不稳定。

- `pywxrobot.exe a.py` 直接执行Python脚本，方便测试一些函数。而且有些功能并不依赖消息机制，比如检测好友状态
- 插件界面，我一直在想用户能不能给自己的Python插件写一个界面操作，或者是能用aardio做插件的界面。这个暂时没有什么好的想法，后面在考虑实现

#### 功能exe

后面还会用aardio开发一些单独的exe使用，方便在界面上操作一些功能。

#### 多开实现

多开功能其实已经兼容，但是我并没有去测试，这个还是先等功能稳定后再去测试

#### http接口调用

开放http接口来调用功能，而不是通过Python插件。不过收消息这个不好处理，只能通过post提交消息，这样就需要用户开一个server端接收。







