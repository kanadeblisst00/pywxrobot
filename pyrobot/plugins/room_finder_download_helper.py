import wxfunc
import redis
import time
import threading
from wxcodeapi import WxCodeAPi
import xml.etree.ElementTree as ET 
from preprocess import pre_deal
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct
from utools import catch_and_print_exception


class FinderDownloadHelper(MsgPluginTemplate):
    description = "群里解析并下载好友发送的视频号"
    lock = threading.Lock()
    redis_key = "pywxrobot:room_finder_download_helper"
    #enable = True

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.redis_client = redis.Redis()
        self.redis_client.ping()
        if not settings.get("rooms"):
            raise Exception("未配置生效群")
        self.wx = WxCodeAPi("192.168.31.63", 23238)
        self.admins = settings.get("admins", [])
        self.match_rooms = [pre_deal.find_user_by_nickname(i) for i in settings["rooms"] if pre_deal.find_user_by_nickname(i)]
    
    def get_finder_download_info(self, objectid:str, nonceid:str, retry=0):
        if retry > 2:
            return
        result = self.wx.getvideourl(objectid, nonceid)
        if not result:
            time.sleep(1)
            return self.get_finder_download_info(objectid, nonceid, retry+1)
        data = result.get("data")
        if data and not data.get("resolution_list"):
            time.sleep(1)
            return self.get_finder_download_info(objectid, nonceid, retry+1)
        return data

    @catch_and_print_exception
    def download_finder(self, msg_struct: ChatMsgStruct):
        room_sender  = msg_struct.room_sender
        sender = msg_struct.sender
        if not room_sender or sender not in self.match_rooms:
            return
        content = msg_struct.content
        # if room_sender not in self.admins and self.redis_client.get(f"{self.redis_key}:{room_sender}"):
        #     print(f"该用户({room_sender})今天已经使用过！")
        #     return
        with self.lock:
            root = ET.fromstring(content) 
            objectid = root.find(".//objectId").text
            nonceid = root.find(".//objectNonceId").text
            video_info = self.get_finder_download_info(objectid, nonceid)
            if not video_info:
                info = f"视频解析失败，objectid: {objectid}, nonceid: {nonceid}"
                print(info)
                wxfunc.SendTextMsg(sender, info)
                return
            title = video_info["description"]
            publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(video_info["publish_time"]))
            source = video_info["source"]
            if not video_info.get("resolution_list"):
                print("video_info: ", video_info)
                return
            self.redis_client.set(f"{self.redis_key}:{room_sender}", "1", ex=self.get_today_surplus_sec())
            resolution = video_info["resolution_list"][0]
            duration = int(resolution["duration"]/60)
            result = f'''视频标题: {title}\n发布时间: {publish_time}\n作者名称: {source}\n视频时长(秒): {duration}\n视频下载链接(请复制到其他浏览器打开): '''
            wxfunc.SendTextMsg(sender, result)
            time.sleep(1)
            wxfunc.SendTextMsg(sender, resolution["url"])
            time.sleep(1)


    # @catch_and_print_exception
    # def download_finder(self, msg_struct: ChatMsgStruct):
    #     room_sender  = msg_struct.room_sender
    #     sender = msg_struct.sender
    #     if not room_sender or sender not in self.match_rooms:
    #         return
    #     content = msg_struct.content
    #     if room_sender not in self.admins and self.redis_client.get(f"{self.redis_key}:{room_sender}"):
    #         print(f"该用户({room_sender})今天已经使用过！")
    #         return
    #     root = ET.fromstring(content) 
    #     objectid = root.find(".//objectId").text
    #     nonceid = root.find(".//objectNonceId").text
    #     video_info = self.get_finder_download_info(objectid, nonceid)
    #     if not video_info:
    #         print(f"获取视频号的信息失败，objectid: {objectid}, nonceid: {nonceid}")
    #         return
    #     title = video_info["description"]
    #     publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(video_info["publish_time"]))
    #     source = video_info["source"]
    #     if not video_info.get("resolution_list"):
    #         print("video_info: ", video_info)
    #         return
    #     self.redis_client.set(f"{self.redis_key}:{room_sender}", "1", ex=self.get_today_surplus_sec())
    #     resolution = video_info["resolution_list"][0]
    #     duration = int(resolution["duration"]/60)
    #     result = f'''视频标题: {title}\n发布时间: {publish_time}\n作者名称: {source}\n视频时长(分): {duration}\n视频下载链接(请复制到其他浏览器打开): '''
    #     wxfunc.SendTextMsg(sender, result)
    #     time.sleep(1)
    #     wxfunc.SendTextMsg(sender, resolution["url"])
    
    def get_today_surplus_sec(self):
        current_timestamp = int(time.time())
        seconds_in_a_day = 60 * 60 * 24
        seconds_passed_today = current_timestamp % seconds_in_a_day
        seconds_until_midnight = seconds_in_a_day - seconds_passed_today
        return seconds_until_midnight

    @catch_and_print_exception
    def del_transfer(self, msg_struct: ChatMsgStruct):
        if msg_struct.is_self_msg or msg_struct.room_sender:
            return
        root = ET.fromstring(msg_struct.content) 
        paysubtype = root.find('.//paysubtype').text
        amount = root.find('.//feedesc').text
        sender = msg_struct.sender
        if paysubtype != "1":
            return
        time.sleep(1)
        score = int(amount[1:].replace('.', ""))
        new_score = self.redis_client.zincrby(self.redis_key, score, sender)
        result = f"充值成功，当前积分: {int(new_score)}。"
        wxfunc.SendTextMsg(sender, result)
        time.sleep(0.5)
        wxfunc.SendTextMsg(sender, '请发送需要解析的视频号...')

    def run(self):
        broadcast_service.listen("FEED", self.download_finder)
        broadcast_service.listen("TRANSFER", self.del_transfer)

    def close(self):
        broadcast_service.stop_listen("FEED", self.download_finder)
        broadcast_service.listen("TRANSFER", self.del_transfer)

    
    