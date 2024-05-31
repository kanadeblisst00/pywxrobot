import wxfunc
import time
import re
import os
from typing import List
from collections import deque
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct, MsgType
from utools import catch_and_print_exception
from preprocess import pre_deal


class EnterRoomTip(MsgPluginTemplate):
    description = "进群提示语"

    filter_set = deque(maxlen=500)

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        if not settings.get("rules"):
            raise Exception("rules未配置!")
        rooms = dict(wxfunc.GetContactList())["chatroom"]
        room_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in rooms}
        self.init_rules(room_nicknames)

    def init_rules(self, room_nicknames:dict):
        self.rules = {}
        self.room_nicknames = {}
        for room_name, tip in self.settings["rules"].items():
            room_id = room_nicknames.get(room_name)
            if not room_id:
                print(f"未找到群名称({room_name})， 已忽略该配置")
                continue
            if isinstance(tip, str):
                tip = [tip]
            self.rules[room_id] = tip
            self.room_nicknames[room_id] = room_name

    @catch_and_print_exception
    def callback(self, msg_struct: ChatMsgStruct):
        content = msg_struct.content
        sender = msg_struct.sender
        if "加入了群聊" not in content:
            return
        filter_str = f"{msg_struct.msgid}_{msg_struct.timestamp}"
        # 如果是你邀请的，会先接收到SYSMSG消息，在接收到NOTICE
        # 因为NOTICE消息里没有wxid，所以优先处理SYSMSG消息
        if filter_str in self.filter_set or not self.rules.get(sender):
            return
        self.filter_set.append(filter_str)
        room_nickname = msg_struct.sender_nickname
        # 注意这个name可能是你的备注
        name = re.search(r'邀请"(.*)"加入了群聊', content).group(1)
        if msg_struct.msg_type == MsgType.SYSMSG:
            root = ET.fromstring(content) 
            content = root.find(".//text").text
            # 被邀请人的wxid
            user = root.find(".//username").text
            # 获取他的昵称
            name = pre_deal.get_room_sender_nickname(sender, user)
        time.sleep(1)
        print(f"群({room_nickname}), {content}")
        tips:List[str] = self.rules[sender]
        # 根据配置，发送消息
        for tip in tips:
            text = tip.format(name=name, room_name=self.room_nicknames[sender]).strip()
            if text.startswith('<msg') or text.startswith('<?xml'):
                wxfunc.SendXmlMsg(sender, text)
            elif os.path.exists(text):
                if text.endswith(".jpg") or text.endswith(".png"):
                    wxfunc.SendImageMsg(sender, text)
                elif text.endswith('.gif'):
                    wxfunc.SendEmotionMsg(sender, text)
                else:
                    wxfunc.SendFileMsg(sender, text)
            else:
                wxfunc.SendTextMsg(sender, text)
            time.sleep(1)

    def run(self):
        broadcast_service.listen("SYSMSG", self.callback)
        broadcast_service.listen("NOTICE", self.callback)

    def close(self):
        broadcast_service.stop_listen("SYSMSG", self.callback)
        broadcast_service.stop_listen("NOTICE", self.callback)

# class EnterRoomTip(MsgPluginTemplate):
#     description = "进群提示语"

#     def __init__(self, settings: dict) -> None:
#         super().__init__(settings)
#         if not settings.get("rules"):
#             raise Exception("rules未配置!")
#         rooms = dict(wxfunc.GetContactList())["chatroom"]
#         room_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in rooms}
#         self.init_rules(room_nicknames)

#     def init_rules(self, room_nicknames:dict):
#         self.rules = {}
#         self.room_nicknames = {}
#         for room_name, tip in self.settings["rules"].items():
#             room_id = room_nicknames.get(room_name)
#             if not room_id:
#                 print(f"未找到群名称({room_name})， 已忽略该配置")
#                 continue
#             self.rules[room_id] = tip
#             self.room_nicknames[room_id] = room_name

#     @catch_and_print_exception
#     def callback(self, msg_struct: ChatMsgStruct):
#         content = msg_struct.content
#         if "加入了群聊" not in content:
#             return
#         sender = msg_struct.sender
#         room_nickname = msg_struct.sender_nickname
#         name = re.search(r'邀请"(.*)"加入了群聊', content).group(1)
#         print(f"群({room_nickname}), {content}")
#         text:str = self.rules[sender]
#         text = text.format(name=name, room_name=self.room_nicknames[sender]).strip()
#         if text.startswith('<msg') or text.startswith('<?xml'):
#             wxfunc.SendXmlMsg(sender, text)
#         else:
#             wxfunc.SendTextMsg(sender, text)

#     def run(self):
#         broadcast_service.listen("NOTICE", self.callback)

#     def close(self):
#         broadcast_service.stop_listen("NOTICE", self.callback)

