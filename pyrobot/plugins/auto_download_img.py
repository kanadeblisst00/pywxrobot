import wxfunc
import os
import traceback
from threading import Lock
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import wait, abspath, catch_and_print_exception
from WechatImageDecoder import WechatImageDecoder


class AutoDownloadImg(MsgPluginTemplate):
    description = "自动下载接收到的图片"
    enable = True

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.img_decoder = WechatImageDecoder()

    @catch_and_print_exception
    def download_img(self, msg_struct: ChatMsgStruct):
        sender_name = msg_struct.sender_nickname
        room_nickname = msg_struct.room_nickname
        img_path = self.wx_file_path + msg_struct.file_path
        if room_nickname:
            print(f"收到图片消息, 群: {sender_name}[{msg_struct.sender}]，发送人: {room_nickname}[{msg_struct.room_sender}], 图片路径: ", img_path)
        else:
            print(f"收到图片消息, 发送人: {sender_name}[{msg_struct.sender}], 图片路径: ", img_path)
        if msg_struct.is_self_msg:
            return    
        wait(1000, lambda : os.path.exists(img_path))
        if not os.path.exists(img_path):
            print("图片未下载，开始主动下载")
            localid_data = dict(wxfunc.getLocalidByMsgid(str(msg_struct.msgid)))
            dbindex_handle = localid_data.get("dbindexHandle")
            if dbindex_handle:
                wxfunc.DownloadImageFromCdnByLocalid(msg_struct.localid, int(dbindex_handle))
            else:
                print(f"获取dbindex句柄失败, msg_struct: {msg_struct}")
                return
        wait(10000, lambda : os.path.exists(img_path))
        if not os.path.exists(img_path):
            print("图片下载失败")
            return
        else:
            print("图片下载完成")
        self.save_img(img_path, msg_struct)
    
    def save_img(self, dat_path:str, msg_struct: ChatMsgStruct) -> None:
        if not os.path.exists(dat_path):
            return
        save_dir:str = self.settings.get("save_path")
        if not save_dir:
            return
        filename = f"{msg_struct.sender_nickname}【{msg_struct.sender}】{os.sep}{msg_struct.msgid}.png"
        save_abspath = abspath(save_dir, filename, cur_dir=self.cur_dir)
        if not save_abspath:
            return
        try:
            self.img_decoder.decode_pc_dat(dat_path, save_abspath)
        except:
            traceback.print_exc()
        else:
            print(f"图片另存为成功，保存路径: {save_abspath}")
    
    def run(self):
        broadcast_service.listen("IMAGE", self.download_img)

    def close(self):
        broadcast_service.stop_listen("IMAGE", self.download_img)