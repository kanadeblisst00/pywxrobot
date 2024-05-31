import inspect
import sys
import thread
import wxfunc
import os
from importlib import import_module
from abc import ABC, abstractmethod, ABCMeta
from threading import Thread
from broadcast_service import broadcast_service
from preprocess import pre_deal



class PluginTemplate(Thread):
    def __init__(self, settings:dict) -> None:
        self.settings = settings
        self.inited = False
        super().__init__()
        module = inspect.getmodule(self.__class__)
        self.module_name = module.__name__
        self.wx_file_path = wxfunc.getWeChatFilePath().strip('\\').rsplit('\\', 1)[0] + '\\'
        self.cur_dir = os.path.dirname(os.path.dirname(module.__file__))
        print(f"插件({self.module_name})初始化完成")
        
    @abstractmethod
    def run(self):
        pass

    def start(self):
        if self.inited:
            return
        super().start()
        print(f"插件({self.module_name})已启动")
        thread.set(self.module_name, 1)
        self.inited = True
           
    @abstractmethod
    def close(self):
        '''关闭资源'''

    def join(self):
        if not self.inited:
            return
        super().join()
        print(f"插件({self.module_name})已停止")
        thread.set(self.module_name, None)
        self.inited = False


class MsgPluginTemplate(ABC):
    def __init__(self, settings:dict) -> None:
        self.settings = settings
        self.inited = False
        module = inspect.getmodule(self.__class__)
        self.module_name = module.__name__
        self.wx_file_path = wxfunc.getWeChatFilePath().strip('\\').rsplit('\\', 1)[0] + '\\'
        self.cur_dir = os.path.dirname(os.path.dirname(module.__file__))
        print(f"插件({self.module_name})初始化完成")
        
    @abstractmethod
    def run(self):
        pass

    def start(self):
        if self.inited:
            return
        self.run()
        print(f"插件({self.module_name})已启动")
        thread.set(self.module_name, 1)
        self.inited = True

    @abstractmethod
    def close(self):
        pass

    def join(self):
        if not self.inited:
            return
        self.close()
        print(f"插件({self.module_name})已停止")
        thread.set(self.module_name, None)
        self.inited = False


def load_module(module_name):
    module = sys.modules.get(module_name)
    if module:
        return module
    try:
        plugin_module = import_module(module_name)
    except Exception as e:
        print(f"{module_name} import error: {e}")
        return
    return plugin_module

def get_classes_from_module_name(module_name):
    module = load_module(module_name)
    is_abstract = lambda cls: ABC in cls.__bases__ or ABCMeta in cls.__bases__
    # 优先选择PluginTemplate的子类
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and not is_abstract(obj) and (issubclass(obj, PluginTemplate) or issubclass(obj, MsgPluginTemplate)):
            return obj, "消息"
        
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and not is_abstract(obj) and issubclass(obj, Thread):
            return obj, "功能"
        
def publish_msg(msg, *args, **kwargs):
    msg_struct, topic = pre_deal.run(msg)
    broadcast_service.broadcast(topic, msg_struct, *args, **kwargs)
