import wxfunc
import os
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import wait, abspath, catch_and_print_exception


class AutoSaveVoice(MsgPluginTemplate):
    description = "自动保存语音，格式为silk"

    @catch_and_print_exception
    def save_voice(self, msg_struct: ChatMsgStruct):
        sender_name = msg_struct.sender_nickname
        room_nickname = msg_struct.room_nickname
        if room_nickname:
            print(f"收到语音消息, 群: {sender_name}[{msg_struct.sender}]，发送人: {room_nickname}[{msg_struct.room_sender}], msgid: {msg_struct.msgid}")
        else:
            print(f"收到语音消息, 发送人: {sender_name}[{msg_struct.sender}], msgid: {msg_struct.msgid}")
        if msg_struct.is_self_msg:
            return
        save_dir:str = self.settings.get("save_path")
        if not save_dir:
            return
        hexVoice = wait(5000, lambda : wxfunc.getVoiceByMsgid(str(msg_struct.msgid)), interval=200)
        if hexVoice:
            bytesVoice = bytes.fromhex(hexVoice)
            filename = f"{sender_name}【{msg_struct.sender}】{os.sep}{msg_struct.msgid}.silk"
            save_abspath = abspath(save_dir, filename, cur_dir=self.cur_dir)
            with open(save_abspath, 'wb') as f:
                f.write(bytesVoice)
            print(f"语音消息保存成功，保存路径: {save_abspath}")
        else:
            print("语音获取失败！")

    def run(self):
        broadcast_service.listen("VOICE", self.save_voice)

    def close(self):
        broadcast_service.stop_listen("VOICE", self.save_voice)
    