## 便携版安装库

先说一下便携版Python怎么安装库，先下载pip：从`https://bootstrap.pypa.io/get-pip.py`下载下来，然后`.\python.exe get-pip.py`。

接着就可以使用pip来安装了，--target选项可以指定安装到某个路径, 接着在`python38._pth`里可以添加这个路径到`sys.path`(每行一个)。也可以不指定，它默认会安装到当前目录下的Lib下的site-packages里。

例如安装到`.\python.exe -m pip install --target d:\somewhere\other\than\the\default requests`

## 切换到安装版

先下载安装包: `https://wwm.lanzoue.com/ilsFn24ere6d`。这个是32位版本的Python，因为exe是32位aardio写的，只支持加载32位Python。

安装完成后用pip安装`pyrobot\requirements.txt`里的包，然后在config.ini里加上一个pythonPath的参数，具体见config_bak.ini里的示例。

然后你只需要用pip安装你需要的包就可以了。





















