import os
import json
import time
import alogger
import thread
import wxfunc
import mysysout
import traceback
import plugins_manager
from typing import List


def enum_plugins():
    plugins_dir = 'plugins'
    for i in os.listdir(plugins_dir):
        if i.startswith('_') or i.startswith('.'):
            continue
        if i.endswith('.py'):
            i = i[:-3]
        yield i

def load_setting(plugin_name) -> dict:
    plugin_setting_path = f"settings{os.sep}{plugin_name}.json"
    if not os.path.exists(plugin_setting_path):
        return {}
    with open(plugin_setting_path, encoding='utf-8') as f:
        try:
            setting = json.loads(f.read())
        except:
            print("加载插件配置文件({plugin_name})出现异常")
            traceback.print_exc()
        else:
            return setting


def load_plugins() -> List[plugins_manager.MsgPluginTemplate]:
    plugins = []
    for plugin_name in enum_plugins():
        plugin_cls, plugin_type = plugins_manager.get_classes_from_module_name(plugin_name)
        setting = load_setting(plugin_name)
        if not getattr(plugin_cls, "enable", False) and not setting.get("enable"):
            continue
        try:
            plugin_obj = plugin_cls(setting)
            plugin_obj.start()
        except:
            traceback.print_exc()
            continue
        plugins.append(plugin_obj)
    return plugins


def main():
    plugin_objs = load_plugins()
    

    while not thread.get("PythonThreadStop"):
        try:
            msg = wxfunc.popFromMsgQueue()
            if not msg:
                time.sleep(0.1)
                continue
            plugins_manager.publish_msg(msg)
        except KeyboardInterrupt:
            pass

    for plugin_obj in plugin_objs:
        try:
            print(f"插件({plugin_obj.__name__})正在停止!")
        except:
            traceback.print_exc()
        plugin_obj.join()


if __name__ == "__main__":
    main()