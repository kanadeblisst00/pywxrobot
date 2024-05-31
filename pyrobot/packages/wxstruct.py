#-*- coding: utf-8 -*-
import json


class MDict(object):
    def __init__(self, **kwargs):
        super().__setattr__("_items", {})
        annotations = self.__annotations__ if self.__annotations__ else {}
        for key in annotations:
            v1 = kwargs.get(key)
            self._items[key] = getattr(self, key) if v1 is None else v1

    def __len__(self):  
        return len(self._items)

    def __getitem__(self, key):  
        return self._items.get(key)

    def __setitem__(self, key, value): 
        if self.__annotations__ and key in self.__annotations__: 
            self._items[key] = value
    
    def __delitem__(self, key):
        del self._items[key]

    def __iter__(self):  
        return iter(self._items.keys())
    
    def __getattr__(self, key):
        if hasattr(self._items, key):
            return getattr(self._items, key)
        else:
            return self._items.get(key)
    
    def get(self, key):
        return self._items.get(key)
    
    def __setattr__(self, key, value):
        if self.__annotations__ and key in self.__annotations__:
            self._items[key] = value
    
    def to_dict(self):
        return self._items
    
    def to_json(self):
        return json.dumps(self._items, ensure_ascii=False)

    def __repr__(self):
        return self.to_json()


def class_attrs_to_dict(cls, key="value"):
    # 获取 MsgType 类的所有属性
    attributes = vars(cls)
    # 过滤掉魔术方法和私有属性
    filtered_attributes = {value: name for name, value in attributes.items() if not name.startswith('__') and not name.startswith('_')}
    if key == "name":
        filtered_attributes = {value: key for key, value in filtered_attributes.items()}
    return filtered_attributes


class MsgType:
    TEXT = 0x1
    IMAGE = 0x3
    VIDEO = 0x2B
    VOICE = 0x22
    ADDFRIEND = 0x25
    CARD = 0x2A
    EMOTION = 0x2F
    LOCATION = 0x30
    XML = 0x31 # 文件、转账、文章、小程序、聊天记录等
    VOIP = 0x32 # 语音、视频通话
    NOTICE = 0x2710 # 红包、拍一拍等
    SYSMSG = 0x2712 # 系统消息

class XmlMsgType:
    BIZMSG = 5
    FILE = 6
    SHARE_LOCATION = 17 # 位置共享
    MULTI_MSG = 19 # 合并发送的多条消息
    STEP_RANK_MSG = 21 # 微信运行发送的步数消息
    APPMSG = 33   # 分享的小程序
    FEED = 51 # 视频号
    REFERENCE_MSG = 57 # 引用回复
    ROOM_ANNOUNCEMENT = 87 # 群公告
    TRANSFER = 2000 # 转账

class SysMsgType:
    modtextstatus = "modtextstatus"
    gamecenter = "gamecenter"
    uploadfinishmsg = "uploadfinishmsg"
    dynacfg = "dynacfg"
    dynacfg_split = "dynacfg_split"
    newabtest = "newabtest"
    expt = "expt"
    revokemsg = "revokemsg"
    mmchatroomtopmsg = "mmchatroomtopmsg"
    mmchatroombarannouncememt = "mmchatroombarannouncememt"
    qy_status_notify = "qy_status_notify"
    qy_chat_update = "qy_chat_update"
    MMBizPaySubscribePayNotify = "MMBizPaySubscribePayNotify"
    qy_revoke_msg = "qy_revoke_msg"
    functionmsg = "functionmsg"
    EmojiBackup = "EmojiBackup"
    EmotionBackup = "EmotionBackup"
    multivoip = "multivoip"
    voipmt = "voipmt"
    teenagermodeagreenauthorization = "teenagermodeagreenauthorization"
    SnsAd = "SnsAd"
    paymsg = "paymsg"
    wintest = "wintest"
    DebugAppCodeUpdatedToPC = "DebugAppCodeUpdatedToPC"
    subscribesysmsg = "subscribesysmsg"
    AppBrandTestUpdateWxaUsageListNotify = "AppBrandTestUpdateWxaUsageListNotify"
    ForceOpenAppNotify = "ForceOpenAppNotify"
    AppBrandForceKill = "AppBrandForceKill"
    AppBrandNotify = "AppBrandNotify"
    CloseLive = "CloseLive"
    ApplyLiveMic = "ApplyLiveMic"
    CloseLiveMic = "CloseLiveMic"
    LiveMicSucc = "LiveMicSucc"
    AcceptLiveMic = "AcceptLiveMic"
    CloseApplyLiveMic = "CloseApplyLiveMic"
    BanLiveComment = "BanLiveComment"
    pat = "pat"
    roomtoolsalter = "roomtoolsalter"
    sysmsgtemplate = "sysmsgtemplate"
    revokehistoryinjoinroommsg = "revokehistoryinjoinroommsg"
    delchatroommember = "delchatroommember"
    bizlivenotify = "bizlivenotify"
    resourcemgr = "resourcemgr"
    mmsearch_reddot_new = "mmsearch_reddot_new"
    PushLoginUrlAutoLoginSwitchUpdate = "PushLoginUrlAutoLoginSwitchUpdate"
    FinderChatRoomLiveClose = "FinderChatRoomLiveClose"
    secmsg = "secmsg"



class ChatMsgStruct(MDict):
    wxpid: int
    localid: int # 数据库中的递增id，可以用于转发消息，查询消息等
    msgid: int   # 服务器生成的消息唯一id，
    msg_type: int # 消息类型
    is_self_msg: int # 是否是自己发送的消息
    timestamp: int  # 消息时间
    sender: str # 发送人wxid或群id
    sender_nickname: str
    room_sender: str # 如果sender是群id，则该字段是群发送人的wxid
    room_nickname: str 
    content: str # 消息内容
    sign: str # 消息md5
    thumb_path: str # 缩略图存储路径
    file_path: str # 原图或文件保存路径
    extrainfo: str # 不知道是什么数据
    unknow_value0: int
    unknow_value1: int
    unknow_value2: str
    unknow_value3: int
    unknow_value4: int



class AddFriendXmlField:
    fromusername: str # wxid
    encryptusername: str # v3
    fromnickname: str # 昵称
    content: str # 验证消息
    imagestatus: str
    scene: str # 添加类型, 手机号 0xF，微信号 0x3，QQ号 0x1，wxid 0x6,名片 0x11 
    country: str 
    province: str
    city: str
    sign: str
    sex: str
    alias: str # 微信号
    bigheadimgurl: str
    smallheadimgurl: str
    ticket: str # v4
    opcode: str  # 1 查询好友状态 2 加好友