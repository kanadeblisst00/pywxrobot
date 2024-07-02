import os
import wxfunc
from typing import List


def main():
    print("开始导出公众号列表！")
    keys = ("wxid", "微信号", "备注", "头像", "小头像", "昵称", "地区", "省份", "城市", "描述")
    contacts:List[dict] = dict(wxfunc.GetContactList())["biz"]
    path = os.path.abspath("公众号列表.csv")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(keys) + "\n")
        for contact in contacts:
            # 如果想要所有字段，需要用wxfunc.GetUserInfoByNet从网络获取
            line = ','.join([contact.get(key, "") for key in keys]) + '\n'
            f.write(line)
    print(f"导出公众号列表完成, csv文件路径： {path}！")


if __name__ == "__main__":
    main()