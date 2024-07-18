import os
import wxfunc
import time
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

    print("开始导出好友列表！")
    keys = ("wxid", "微信号", "备注", "头像", "小头像", "昵称", "地区", "省份", "城市", "描述", "性别", "好友")
    contacts:List[dict] = dict(wxfunc.GetContactList())["friend"]
    path = os.path.abspath("完整好友列表.csv")
    t0 = time.time()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(keys) + "\n")
        for contact in contacts:
            wxid = contact["wxid"]
            if wxid in filter_list:
                continue
            info = wxfunc.GetUserInfoByNet(wxid) or {}
            if not info:
                print(f'无法从网络获取到用户信息: {wxid}')
            line = ','.join([(contact.get(key) or info.get(key, "")).replace(",", "_").replace("\n", " ") for key in keys]) + '\n'
            print(line)
            f.write(line)
            time.sleep(2)
    print(f"导出好友列表完成, csv文件路径： {path}！, 耗时: {time.time()-t0}")


if __name__ == "__main__":
    main()