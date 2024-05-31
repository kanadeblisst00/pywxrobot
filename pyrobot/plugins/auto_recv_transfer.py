import wxfunc
import time
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import catch_and_print_exception


class AutoRecvTransfer(MsgPluginTemplate):
    description = "自动接收转账"

    @catch_and_print_exception
    def accept_friend_req(self, msg_struct: ChatMsgStruct):
        sender_name = msg_struct.sender_nickname
        xml = msg_struct.content
        root = ET.fromstring(xml) 
        paysubtype = root.find('.//paysubtype').text
        amount = root.find('.//feedesc').text
        transcationid = root.find('.//transcationid').text
        transferid = root.find('.//transferid').text
        # invalidtime = root.find('.//invalidtime').text
        # begintransfertime = root.find('.//begintransfertime').text
        if paysubtype == "1":
            print(f"收到转账: 发送人: {sender_name}[{msg_struct.sender}], 金额: {amount}")
            time.sleep(3)
            wxfunc.RecvTransfer(msg_struct.sender, transferid, transcationid)
        else:
            print(f"已接收转账: 发送人: {sender_name}[{msg_struct.sender}], 金额: {amount}")

    def run(self):
        broadcast_service.listen("TRANSFER", self.accept_friend_req)

    def close(self):
        broadcast_service.stop_listen("TRANSFER", self.accept_friend_req)

