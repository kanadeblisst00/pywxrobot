import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import abspath, download_file, catch_and_print_exception


class AutoSaveEmotion(MsgPluginTemplate):
    description = "自动保存表情包"

    @catch_and_print_exception
    def save_emotion(self, msg_struct: ChatMsgStruct):
        sender_name = msg_struct.sender_nickname
        room_nickname = msg_struct.room_nickname
        if room_nickname:
            print(f"收到表情消息, 群: {sender_name}[{msg_struct.sender}]，发送人: {room_nickname}[{msg_struct.room_sender}], 文件名: {msg_struct.file_path}")
        else:
            print(f"收到表情消息, 发送人: {sender_name}[{msg_struct.sender}], 文件名: {msg_struct.file_path}")
        save_dir:str = self.settings.get("save_path")
        if not save_dir:
            return
        xml = msg_struct.content
        root = ET.fromstring(xml) 
        datas = dict(root.find('.//emoji').items())
        cdnurl = datas["cdnurl"].replace('&amp;', '&')
        filename = msg_struct.file_path
        if not filename:
            filename = msg_struct.msgid
        filename = f"{filename}.gif"
        save_abspath = abspath(save_dir, filename, cur_dir=self.cur_dir)
        with open(save_abspath, 'wb') as f:
            f.write(download_file(cdnurl))

    def run(self):
        broadcast_service.listen("EMOTION", self.save_emotion)

    def close(self):
        broadcast_service.stop_listen("EMOTION", self.save_emotion)

    
    