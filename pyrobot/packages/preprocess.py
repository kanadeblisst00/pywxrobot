'''会在收到消息时加载，用于消息预处理'''
import json
import random
import wxfunc
from typing import Tuple
from wxstruct import MsgType, class_attrs_to_dict
from wxstruct import ChatMsgStruct


class PreDealmsg:
    def __init__(self) -> None:
        self._room_nicknames = {}
        contacts = dict(wxfunc.GetContactList())
        self._contact_list = list(contacts["chatroom"]) + list(contacts["friend"]) + list(contacts["biz"])
        self._user_nicknames = {d["wxid"]:d.get('备注') or d.get("昵称") for d in self._contact_list}
        self._msg_type_dict = class_attrs_to_dict(MsgType)
        self._chatroom_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in contacts["chatroom"]}
        self._friend_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in contacts["friend"]}
        self._biz_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in contacts["biz"]}
    
    def find_user_by_nickname(self, name, _type="chatroom"):
        d:dict = getattr(self, f"_{_type}_nicknames")
        if not d:
            return  
        return d.get(name)
    
    def set_sender_name(self, msg_data:dict):
        '''设置发送者昵称'''
        sender = msg_data["sender"]
        msg_data["sender_nickname"] = self.get_sender_name(sender)
    
    def get_sender_name(self, wxid:str):
        sender_name = self._user_nicknames.get(wxid)
        if not sender_name:
            contacts = dict(wxfunc.GetContactList())
            self._contact_list = list(contacts["chatroom"]) + list(contacts["friend"]) + list(contacts["biz"])
            self._user_nicknames = {d["wxid"]:d.get('备注') or d.get("昵称") for d in self._contact_list}
            self._user_nicknames["filehelper"] = "文件传输助手"
            sender_name = self._user_nicknames.get(wxid)
        if not sender_name:
            sender_name = wxid
        return sender_name
    
    def set_room_sender_nickname(self, msg_data:dict):
        '''设置群发送者昵称'''
        if not msg_data.get('room_sender'):
            msg_data["room_nickname"] = None
            return
        room_sender = msg_data["room_sender"]
        sender = msg_data["sender"]
        msg_data["room_nickname"] = self.get_room_sender_nickname(sender, room_sender)

    def get_room_sender_nickname(self, room_id:str, wxid:str):
        room_nickname = self._room_nicknames.get(wxid)
        if not room_nickname:
            room_nickname = wxfunc.GetChatRoomMemberNickname(room_id, wxid)
            if not room_nickname:
                json_info = wxfunc.GetUserInfoJsonByCache(wxid)
                user_info = json.loads(json_info)
                room_nickname = user_info["nickname"]
            self._room_nicknames[wxid] = room_nickname
        return room_nickname
            
    def set_localid(self, msg_data:dict):
        if msg_data.get("localid") or not msg_data.get('msgid'):
            return
        msg_data["localid"] = self.get_localid(msg_data["msgid"])
    
    def get_localid(self, msgid:int):
        localid_data = dict(wxfunc.getLocalidByMsgid(str(msgid)))
        localid = localid_data.get("localid", "")
        return int(localid) if localid.isdigit() else -1

    def set_msgid(self, msg_data:dict):
        '''
        自己发的消息msgid还没拿到，随机一个
        也可以等待一定的时间后，去本地数据库里取
        '''
        if msg_data.get('msgid'):
            return
        msg_data["msgid"] = int(str(random.randint(1, 9)) + ''.join(random.choices("1234567890", k=17)))

    def _get_msg_type(self, msg_data:dict):
        msg_type = msg_data["msg_type"]
        msg_type_str = self._msg_type_dict.get(msg_type)
        if not msg_type_str:
            msg_type_str = "UNKNOWN"
        return msg_type_str
    
    def run(self, msg:str) -> Tuple[ChatMsgStruct, str]:
        # print("消息预处理: ", msg)
        msg_data = json.loads(msg)
        msg_type_str = self._get_msg_type(msg_data)
        if msg_data["msg_type"] not in  (MsgType.SYSMSG, MsgType.ADDFRIEND):
            self.set_room_sender_nickname(msg_data)
            self.set_sender_name(msg_data)
            self.set_localid(msg_data)
            self.set_msgid(msg_data)
        msg_struct = ChatMsgStruct(**msg_data)
        # new_msg = json.dumps(msg_data,ensure_ascii=False)
        # print("消息预处理结果: ", new_msg)
        return msg_struct, msg_type_str

pre_deal = PreDealmsg()
