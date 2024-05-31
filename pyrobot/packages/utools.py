import time
import os
import requests
import traceback
import shutil
import inspect
import functools
from typing import Callable


def wait(timeout:int, func:Callable, *args, interval = 10):
    '''timeout: 毫秒'''
    while timeout > 0:
        ret = func(*args)
        if ret:
            return ret
        timeout -= interval
        time.sleep(interval/1000)

def abspath(save_dir:str, filename:str, cur_dir="."):
    '''创建不存在的文件夹'''
    if not save_dir:
        return
    elif ":" not in save_dir:
        save_dir = os.path.join(cur_dir, save_dir)
    path = os.path.join(save_dir, filename)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
    return os.path.abspath(path)

def copy_file(src:str, dst:str):
    '''复制文件'''
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if os.path.isdir(src):
        return
    if src[0].lower() != dst[0].lower():
        shutil.copyfile(src, dst)
    else:
        # 如果在同一个分区的话，不拷贝文件。直接对文件做硬链接处理，避免空间浪费
        os.link(src, dst)

def download_file(url, retry=0):
    if retry > 2:
        return
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=6)
    except:
        traceback.print_exc()
        time.sleep(2)
        return download_file(url, retry+1)
    return resp.content

def catch_and_print_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            err = traceback.format_exc()
            module = inspect.getmodule(func)
            print(f"模块({module})函数({func.__name__})发生异常\n {err}")
    return wrapper

