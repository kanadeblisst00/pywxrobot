import wxfunc
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct, MsgType, class_attrs_to_dict
from utools import catch_and_print_exception


class EchoRevokeMsg(MsgPluginTemplate):
    description = "打印撤回消息"
    enable = True

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self._msg_type_dict = class_attrs_to_dict(MsgType)

    @catch_and_print_exception
    def print_msg(self, msg_struct: ChatMsgStruct):
        root = ET.fromstring(msg_struct.content) 
        replacemsg = root.find('.//replacemsg').text
        newmsgid = root.find('.//newmsgid').text
        msg = wxfunc.getMsgByMsgid(str(newmsgid))
        msg = dict(msg) if msg else {}
        if msg.get("Type") == "1":
            content = msg.get("StrContent")
        else:
            content = self.get_msg_type_text(msg.get("Type"))
        print(f"{replacemsg}, 消息内容: {content}")
    
    def get_msg_type_text(self, _type:str):
        if not _type:
            return ""
        return self._msg_type_dict.get(int(_type))
    
    def run(self):
        broadcast_service.listen("revokemsg", self.print_msg)

    def close(self):
        broadcast_service.stop_listen("revokemsg", self.print_msg)