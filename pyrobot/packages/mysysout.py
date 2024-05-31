import sys
import alogger

class CustomOutput:
    def __init__(self):
        self.content = ""

    def write(self, text):
        if text == "\n":
            alogger.info(self.content)
            self.content = ""
            return
        self.content += text

    def flush(self):
        # 如果需要，可以实现flush方法
        pass


# 创建自定义输出类的实例
custom_output = CustomOutput()

# 将sys.stdout重定向到自定义输出
sys.stdout = custom_output
sys.stderr = custom_output
# 恢复原始的sys.stdout
# original_stdout = sys.__stdout__
# sys.stdout = original_stdout

