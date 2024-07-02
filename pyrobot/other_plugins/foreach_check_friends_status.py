import time
import os
import wxfunc
from typing import List


def main():
    filter_list = [
        "medianote", # 语音记事本
        "floatbottle", # 漂流瓶
        "fmessage", # 朋友推荐消息
        "filehelper", # 文件传输助手
        "qmessage", # QQ离线消息
        "qqmail", # QQ邮箱提醒
    ]

    contacts:List[dict] = dict(wxfunc.GetContactList())["friend"]
    path = os.path.abspath("检测好友结果.csv")
    with open(path, 'w', encoding='utf-8') as f:
        f.write("wxid,微信号,昵称,结果\n")
        for contact in contacts:
            wxid = contact["wxid"]
            if wxid in filter_list:
                continue
            nickname = contact.get("昵称", "")
            wxh = contact.get("微信号", "")
            result = wxfunc.CheckFriendStatus(wxid)
            print(wxid, nickname, result)
            if "好友" in result:
                continue
            f.write(f'{wxid},{wxh},{nickname},{result}\n')
            time.sleep(0.1)
    print(f"好友检测完成，检测结果文件(csv): {path}")

def test():
    print(wxfunc.CheckFriendStatus("wxid_mp7earq22qtg22"))


if __name__ == "__main__":
    main()