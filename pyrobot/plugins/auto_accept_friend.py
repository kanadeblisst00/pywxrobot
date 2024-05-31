import wxfunc
import time
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import catch_and_print_exception


class AutoAcceptFriend(MsgPluginTemplate):
    description = "自动接受好友请求"

    @catch_and_print_exception
    def accept_friend_req(self, msg_struct: ChatMsgStruct):
        xml = msg_struct.content
        root = ET.fromstring(xml) 
        datas = dict(root.items())
        print(f"收到好友({datas['fromnickname']})的请求。")
        v3 = datas["encryptusername"]
        v4 = datas["ticket"]
        addType = datas["scene"]
        time.sleep(5)
        wxfunc.AddFriendByV3V4(v3, v4, addType)
        print(f"已同意好友({datas['fromnickname']})的请求。")

    def run(self):
        broadcast_service.listen("ADDFRIEND", self.accept_friend_req)

    def close(self):
        broadcast_service.stop_listen("ADDFRIEND", self.accept_friend_req)

