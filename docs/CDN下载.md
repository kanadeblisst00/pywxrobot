### 下载视频

**函数原型**: `DownloadImageFromCdnByLocalid(localid:int, dbindexHandle:int) -> None`


**使用案例**: 

```python
import wxfunc

# 消息的msgid
msgid = 1111111111
localid_data = getLocalidByMsgid(msgid)
wxfunc.DownloadImageFromCdnByLocalid(localid_data["localid"], localid_data["dbindexHandle"])
```

**补充说明**：具体使用请参考内置插件`auto_download_video.py`

### 下载图片

**函数原型**: `DownloadFileFromCdnByLocalid(localid:int, dbindexHandle:int) -> None`


**使用案例**: 

```python
import wxfunc

# 消息的msgid
msgid = 1111111111
localid_data = getLocalidByMsgid(msgid)
wxfunc.DownloadFileFromCdnByLocalid(localid_data["localid"], localid_data["dbindexHandle"])
```

**补充说明**：具体使用请参考内置插件`auto_download_file.py`

### 下载文件

**函数原型**: `DownloadVideoFromCdnByLocalid(localid:int, dbindexHandle:int) -> None`


**使用案例**: 

```python
import wxfunc

# 消息的msgid
msgid = 1111111111
localid_data = getLocalidByMsgid(msgid)
wxfunc.DownloadVideoFromCdnByLocalid(localid_data["localid"], localid_data["dbindexHandle"])
```

**补充说明**：具体使用请参考内置插件`auto_download_img.py`


