import time
import wxfunc
from typing import List


def main():
    contacts:List[dict] = dict(wxfunc.GetContactList())["friend"]
    with open("检测好友结果.csv", 'w', encoding='utf-8') as f:
        f.write("wxid,微信号,昵称,结果\n")
        for contact in contacts:
            wxid = contact["wxid"]
            nickname = contact["昵称"]
            wxh = contact.get("微信号") or ""
            result = wxfunc.CheckFriendStatus(wxid)
            print(wxid, nickname, result)
            f.write(f'{wxid},{wxh},{nickname},{result}\n')
            time.sleep(0.1)

def test():
    print(wxfunc.CheckFriendStatus("wxid_mp7earq22qtg22"))


if __name__ == "__main__":
    main()