from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import catch_and_print_exception


class PrintMsg(MsgPluginTemplate):
    description = "测试打印所有类型消息"

    @catch_and_print_exception
    def print_msg(self, msg_data: ChatMsgStruct):
        print("args: ", msg_data)
    
    def run(self):
        broadcast_service.listen("__all__", self.print_msg)

    def close(self):
        broadcast_service.stop_listen("__all__", self.print_msg)