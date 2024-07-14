import time
import os
import wxfunc
from typing import List


def main():
    '''经群友测试，有一类好友是有感知的：你有他好友，但他把你删了并且他没有设置加好友权限，这会导致你直接加上他'''
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
    t0 = time.time()
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
            time.sleep(2)
            if "好友" in result:
                continue
            f.write(f'{wxid},{wxh},{nickname},{result}\n')
            f.flush()
    print(f"好友检测完成，检测结果文件(csv): {path}, 耗时: {time.time()-t0}")

def test():
    print(wxfunc.CheckFriendStatus("wxid_mp7earq22qtg22"))


if __name__ == "__main__":
    main()