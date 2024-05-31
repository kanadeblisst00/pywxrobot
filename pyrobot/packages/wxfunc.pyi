
def GetContactList() -> dict:
    '''获取当前用户联系人列表'''

def getSelfInfo() -> dict:
    '''获取当前登录用户信息'''

def getWeChatFilePath() -> str:
    '''获取微信文件保存路径'''

def popFromMsgQueue() -> str:
    '''从队列中返回一条消息'''

def getMsgQueueSize() -> int:
    '''返回消息队列大小'''

def GetChatMsgJsonByLocalid(localid:int, dbindex:int) -> str:
    '''通过localid获取json格式的消息'''

def SendTextMsg(wxid:str, text:str) -> None:
    '''发送文本消息'''

def SendAtMsg(roomid:str, wxids:str, text:str) -> None:
    '''发送@消息
    wxids: 多个wxid用`分隔
    '''

def SendXmlMsg(wxid:str, xml:str, dtype:int=None) -> None:
    '''发送xml消息'''

def SendEmotionMsg(wxid:str, path:str) -> None:
    '''发送表情消息'''

def SendCardMsg(wxid:str, xml:str) -> None:
    '''发送名片消息'''

def SendCardMsgByWxid(wxid:str, cardWxid:str) -> None:
    '''通过wxid发送名片消息'''

def SendPatMsg(roomid:str, wxid:str) -> None:
    '''发送拍一拍消息'''

def SendImageMsg(wxid:str, path:str) -> None:
    '''发送图片消息'''

def SendFileMsg(wxid:str, path:str) -> None:
    '''发送文件消息'''

def SendAppMsg(wxid:str, appid:str) -> None:
    '''发送小程序消息'''

def SendRenferMsg(text:str, localid:int, dbindexHandle:int) -> None:
    '''发送引用消息'''

def ForwardMessage(wxid:str, localid:int, dbindexHandle:int) -> None:
    '''转发消息'''

def EditRemark(wxid:str, remark:str) -> None:
    '''编辑好友备注'''

def RevokeMsg(localid:int, dbindexHandle:int) -> None:
    '''撤回消息'''

def RecvTransfer(wxid:str, transferid:str,transcationid:str) -> None:
    '''接收转账'''

def RefundTransfer(wxid:str, transferid:str,transcationid:str) -> None:
    '''返还转账'''

def GetChatRoomMembers(roomid:str) -> str:
    '''获取群成员'''

def GetChatRoomMemberNickname(roomid:str, wxid:str) -> str:
    '''获取群成员昵称'''

def DelChatRoomMembers(roomid:str, wxid:str) -> None:
    '''删除群成员'''

def InviteChatRoomMembers(roomid:str, wxids:str, wait:int=0) -> None:
    '''等待wait毫秒后发送群邀请'''

def SetChatRoomAnnouncement(roomid:str, content:str) -> None:
    '''设置群公告'''

def SetChatRoomName(roomid:str, name:str) -> None:
    '''修改群名称'''

def SetChatRoomMyNickname(roomid:str, name:str) -> None:
    '''修改自己的群昵称'''

def AddChatRoomMembers(roomid:str, wxid:str) -> None:
    '''四十人以下群, 邀请群成员'''

def DownloadImageFromCdnByLocalid(localid:int, dbindexHandle:int) -> None:
    '''下载图片'''

def DownloadFileFromCdnByLocalid(localid:int, dbindexHandle:int) -> None:
    '''下载文件'''

def DownloadVideoFromCdnByLocalid(localid:int, dbindexHandle:int) -> None:
    '''下载视频'''

def AddFriendByV3V4(v3:str, v4:str, addType:int) -> None:
    '''同意好友请求'''

def GetUserInfoJsonByCache(wxid:str) -> str:
    '''从缓存获取好友信息'''

def GetUserInfoByNet(wxid:str) -> dict:
    '''从网络获取好友信息'''

def ExecuteSql(dbname:str, sql:str, resultsLen:int=0x50000) -> str:
    '''执行sql'''

def getMaxDbindex() -> int:
    '''获取msg数据库数量'''

def GetLatestMsgLocalidsCount(timestamp:int, dbindex:int) -> int:
    '''查询msg.db数据库从timestamp到现在的数据量'''

def GetLatestMsgLocalidsSlice(timestamp:int, dbindex:int, limit:int, offset:int) -> list:
    '''查询msg.db数据库从timestamp到现在的所有消息localid'''

def GetLatestMsgLocalids(timestamp:int) -> list:
    '''从所有msg数据库中查询出所有消息localid'''

def getLocalidByMsgid(msgid:str) -> dict:
    '''获取localid和dbindexHandle'''

def getMsgidByLocalid(localid:int, dbindexHandle:int) -> str:
    '''获取msgid'''

def GetFilePathByLocalid(localid, dbindex) -> str:
    '''获取文件消息保存的文件路径'''

def getVoiceLenByMsgid(msgid:str) -> int:
    '''获取语音字节长度'''

def getVoiceByMsgid(msgid:str) -> str:
    '''获取语音二进制内容'''

def getVoiceTextByMsgid(msgid:str) -> str:
    '''获取语音文本内容，需打开语音自动转文字'''

def getMsgByMsgid(msgid:str) -> dict:
    '''从数据库查询消息'''

def CheckFriendStatus(wxid:str, addType:int=6) -> str:
    '''检测好友状态'''






