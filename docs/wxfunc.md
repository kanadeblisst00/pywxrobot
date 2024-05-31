## 发送消息

### 文本消息

**函数原型**: `SendTextMsg(wxid:str, text:str) -> None`

**使用案例**: 

```python
import wxfunc

wxfunc.SendTextMsg("filehelper", "测试消息")
```

### 图片消息

**函数原型**: `SendImageMsg(wxid:str, path:str) -> None`

**使用案例**: 

```python
import wxfunc

wxfunc.SendTextMsg("filehelper", r"C:\1.png")
```

### AT消息

**函数原型**: `SendAtMsg(roomid:str, wxids:str, text:str) -> None`

**使用案例**: 

```python
import wxfunc

wxfunc.SendAtMsg("xxxxx@chatroom", "wxid_xxxxx", "消息内容")
```

**补充说明**：

一般消息内还会添加`@昵称`，所以发消息之前需要先获取到你AT的人的昵称拼接到消息内容

```python
import wxfunc
from preprocess import pre_deal

room_id = "22222@chatroom"
at_wxids = ["wxid_111111","wxid_222222"]
text = "你们好"
at_nicknames = ["@"+pre_deal.get_room_sender_nickname(room_id, wxid) for wxid in at_wxids]

at_text = ' '.join(at_nicknames) + ' ' + text
wxfunc.SendAtMsg(room_id, '`'.join(at_wxids), at_text)
```

### xml消息

**函数原型**: `SendXmlMsg(wxid:str, xml:str, dtype:int=None) -> None`

**使用案例**: 

```python
import wxfunc

s = '''
<msg>\n    <fromusername>wxid_mp7earq22qtg22</fromusername>\n    <scene>0</scene>\n    <commenturl></commenturl>\n    <appmsg appid=\"\" sdkver=\"0\">\n        <title>标题</title>\n        <des>简介</des>\n        <action>view</action>\n        <type>5</type>\n        <showtype>0</showtype>\n        <content></content>\n        <url>https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&amp;amp;__biz=MzU0OTkwODU2MA==&amp;amp;scene=1&amp;amp;album_id=3186032242465210368&amp;amp;count=3#wechat_redirect</url>\n        <dataurl></dataurl>\n        <lowurl></lowurl>\n        <lowdataurl></lowdataurl>\n        <recorditem></recorditem>\n        <thumburl>https://mmbiz.qpic.cn/mmbiz_jpg/Y56THyb6khPzg9p1PmiccLBQtibtAoMvVAUTH8xnK9ngicPBjrT5rBIzMOL3o9YFGJaOtoGQVfnKMxatViaue3FA2g/300?wxtype=jpeg&amp;wxfrom=0</thumburl>\n        <messageaction></messageaction>\n        <laninfo></laninfo>\n        <extinfo></extinfo>\n        <sourceusername>gh_98e6c50f500b</sourceusername>\n        <sourcedisplayname>Python成长路</sourcedisplayname>\n        <commenturl></commenturl>\n        <appattach>\n            <totallen>0</totallen>\n            <attachid></attachid>\n            <emoticonmd5></emoticonmd5>\n            <fileext></fileext>\n            <cdnthumburl>3057020100044b304902010002040b8e01bd02032e1802020488eda67c0204664f013a042463653562386262362d316238622d346434382d386264632d6632623236356334356538390204051408030201000405004c4c6e00</cdnthumburl>\n            <aeskey></aeskey>\n            <cdnthumbaeskey>91151136e05b317a07390aa70985c043</cdnthumbaeskey>\n            <cdnthumblength>7792</cdnthumblength>\n            <cdnthumbheight>150</cdnthumbheight>\n            <cdnthumbwidth>150</cdnthumbwidth>\n        </appattach>\n        <webviewshared>\n            <publisherId></publisherId>\n            <publisherReqId>0</publisherReqId>\n        </webviewshared>\n        <weappinfo>\n            <pagepath></pagepath>\n            <username></username>\n            <appid></appid>\n            <appservicetype>0</appservicetype>\n        </weappinfo>\n        <websearch />\n    </appmsg>\n    <appinfo>\n        <version>1</version>\n        <appname>Window wechat</appname>\n    </appinfo>\n</msg>
'''
wxfunc.SendXmlMsg("filehelper", "wxid_xxxxx")
```

**补充说明**：

可以先发一个消息，复制xml内容，修改你想要改的。如果是公众号链接，你填写的标题和描述在别人收到可能不生效。需要把&换成`&amp;amp;`，我猜测原理是让链接无法访问，就不会去获取链接的标题和描述，但是在浏览器可以转义就能访问。


## 好友相关

### 联系人列表

**函数原型**: `GetContactList() -> dict`

**使用案例**: 

```python
import wxfunc
contacts = wxfunc.GetContactList()
print("好友列表: ", contacts.friend)
print("群列表: ", contacts.chatroom)
print("公众号列表: ", contacts.biz)
```

**补充说明**：

列表的每个元素都是一个字典，字典有以下类型的键:

- wxid
- 微信号
- 备注
- 头像
- 小头像
- 昵称
- 地区
- 省份
- 城市
- 描述

可能某些键没有，请使用get方法来获取。

#### 