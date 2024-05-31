import code
from plugins_manager import PluginTemplate


class InteractiveConsole(PluginTemplate):
    description = "打开交互式终端"

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
    
    def run(self):
        try:
            code.interact()
        except KeyboardInterrupt:
            pass

    def close(self):
        pass