import wxfunc
import os
from threading import Lock
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import wait, abspath, copy_file, catch_and_print_exception


class AutoDownloadFile(MsgPluginTemplate):
    description = "自动下载接收到的文件"
    enable = True
    lock = Lock()

    @catch_and_print_exception
    def download_file(self, msg_struct: ChatMsgStruct):
        sender_name = msg_struct.sender_nickname
        file_path = msg_struct.file_path
        room_nickname = msg_struct.room_nickname
        path = self.wx_file_path + file_path
        if room_nickname:
            print(f"收到文件消息, 群: {sender_name}[{msg_struct.sender}]，发送人: {room_nickname}[{msg_struct.room_sender}], 文件路径: {path}")
        else:
            print(f"收到文件消息, 发送人: {sender_name}[{msg_struct.sender}], 文件路径: {path}")
        if msg_struct.is_self_msg:
            return
        with self.lock:
            wait(1000, lambda : os.path.exists(path))
            if not os.path.exists(path):
                print("文件未下载，开始主动下载")
                localid_data = dict(wxfunc.getLocalidByMsgid(str(msg_struct.msgid)))
                dbindex_handle = localid_data.get("dbindexHandle")
                if dbindex_handle:
                    wxfunc.DownloadFileFromCdnByLocalid(msg_struct.localid, int(dbindex_handle))
                else:
                    print(f"获取dbindex句柄失败, msg_struct: {msg_struct}")
                    return
            wait(30000, lambda : os.path.exists(path))
            if not os.path.exists(path):
                print("文件下载失败")
                return
            else:
                print("文件下载完成")
            self.save_file(path, msg_struct)
        
    def save_file(self, file_path:str, msg_struct: ChatMsgStruct) -> None:
        if not os.path.exists(file_path):
            return
        save_dir:str = self.settings.get("save_path")
        if not save_dir:
            return
        name = os.path.basename(file_path)
        filename = f"{msg_struct.sender_nickname}【{msg_struct.sender}】{os.sep}{name}"
        save_abspath = abspath(save_dir, filename, cur_dir=self.cur_dir)
        if not save_abspath:
            return
        copy_file(file_path, save_abspath)

    def run(self):
        broadcast_service.listen("FILE", self.download_file)

    def close(self):
        broadcast_service.stop_listen("FILE", self.download_file)