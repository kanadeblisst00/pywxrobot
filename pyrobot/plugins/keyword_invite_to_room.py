import wxfunc
import time
import threading
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct, MsgType
from utools import catch_and_print_exception, wait


class KeywordInviteToRoom(MsgPluginTemplate):
    description = "匹配到关键词自动邀请进群"
    wait_lock = threading.Lock()
    wait_shared_dict = []

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        if not settings.get("rules"):
            raise Exception("rules未配置!")
        rooms = dict(wxfunc.GetContactList())["chatroom"]
        room_nicknames = {d.get('备注') or d.get("昵称"):d["wxid"] for d in rooms}
        self.init_rules(room_nicknames)
    
    def init_rules(self, room_nicknames:dict):
        self.rules = {}
        for room_name, keywords in self.settings["rules"].items():
            if not room_nicknames.get(room_name):
                print(f"未找到群名称({room_name})， 已忽略该配置")
                continue
            if isinstance(keywords, str):
                keywords = [keywords]
            for keyword in keywords:
                self.rules[keyword] = room_nicknames[room_name]
            
    @catch_and_print_exception
    def callback(self, msg_struct: ChatMsgStruct):
        if msg_struct.is_self_msg:
            return
        msg_type = msg_struct.msg_type
        if msg_type == MsgType.ADDFRIEND:
            xml = msg_struct.content
            root = ET.fromstring(xml) 
            datas = dict(root.items())
            content = datas["content"]
            wxid = datas["fromusername"]
            room_id = self.match_keyword(content)
            if not room_id:
                return
            # 等待接受好友请求
            if not wait(30000, self.wait_addfriend, wxid, interval=1000):
                print("等待已超时(30秒)，请开启自动同意好友请求!")
                return
            else:
                with self.wait_lock:
                    self.wait_shared_dict.remove(wxid)
        elif msg_type == MsgType.TEXT:
            if "@chatroom" in msg_struct.sender:
                return
            content = msg_struct.content
            wxid = msg_struct.sender
            room_id = self.match_keyword(content)
        elif msg_type == MsgType.NOTICE:
            content = msg_struct.content
            if content and "现在可以开始聊天了" in content:
                with self.wait_lock:
                    self.wait_shared_dict.append(msg_struct.sender)
            return
        else:
            return
        if not room_id:
            return
        members = wxfunc.GetChatRoomMembers(room_id).split("^G")
        if wxid in members:
            print(f"好友({wxid})已在群({room_id})内")
            return
        time.sleep(3)
        self.invite_member(room_id, wxid, len(members))
    
    def invite_member(self, room_id, wxid, members_size):
        if members_size < 35:
            # 邀请群成员，无需对方同意
            wxfunc.AddChatRoomMembers(room_id, wxid)
        else:
            # 等待5秒发送群成员邀请
            wxfunc.InviteChatRoomMembers(room_id, wxid, 5000)
    
    def match_keyword(self, content):
        for keyword, room_id in self.rules.items():
            if keyword in content:
                return room_id

    def wait_addfriend(self, wxid):
        with self.wait_lock:
            return wxid in self.wait_shared_dict

    def run(self):
        broadcast_service.listen("TEXT", self.callback)
        broadcast_service.listen("ADDFRIEND", self.callback)
        broadcast_service.listen("NOTICE", self.callback)

    def close(self):
        broadcast_service.stop_listen("TEXT", self.callback)
        broadcast_service.stop_listen("ADDFRIEND", self.callback)
        broadcast_service.stop_listen("NOTICE", self.callback)

