import traceback
import xml.etree.ElementTree as ET 
from broadcast_service import broadcast_service
from plugins_manager import MsgPluginTemplate
from wxstruct import ChatMsgStruct, XmlMsgType, class_attrs_to_dict
from utools import catch_and_print_exception


class XmlManager(MsgPluginTemplate):
    description = "解析xml类型消息，分发给其他插件"
    enable = True

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self._xml_type_dict = class_attrs_to_dict(XmlMsgType)
    
    @catch_and_print_exception
    def deal_xml_msg(self, msg_struct: ChatMsgStruct):
        _type = self.get_xml_type(msg_struct.content)
        xml_type_str = self._xml_type_dict.get(_type)
        if not xml_type_str:
            print(f"类型({_type})未定义")
            return
        print(f"收到({xml_type_str})类型的XML消息")
        broadcast_service.broadcast(xml_type_str, msg_struct)
    
    def get_xml_type(self, xml):
        try:
            root = ET.fromstring(xml) 
        except:
            traceback.print_exc()
            return 0
        _type = root.find('.//type').text
        return int(_type)
    
    def run(self):
        broadcast_service.listen("XML", self.deal_xml_msg)

    def close(self):
        broadcast_service.stop_listen("XML", self.deal_xml_msg)