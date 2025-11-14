from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Literal
from enum import Enum

import logging

logger = logging.getLogger(__name__)


class MsgType(str, Enum):
    TEXT = "text"  # 文本消息
    AUDIO = "audio"  # 音频消息
    PICTURE = "picture"  # 图片消息
    VIDEO = "video"  # 视频消息
    FILE = "file"  # 文件消息
    RICH_TEXT = "richText"  # 富文本消息


class AtUser(BaseModel):
    dingtalkId: str = Field(..., description="加密的发送者ID")
    staffId: Optional[str] = Field(
        None, description="企业内部群有的发送者在企业内的userid"
    )


class MessageContent(BaseModel):
    """所有消息内容的基类"""

    model_config = ConfigDict(extra="allow")  # 允许额外的字段


class TextContent(MessageContent):
    """普通文本消息内容（非富文本场景）"""

    content: Optional[str] = Field(None, description="文本消息内容")


class TextContentInRichText(MessageContent):
    """富文本消息中的文本内容"""

    text: Optional[str] = Field(None, description="富文本消息中的文本内容")
    # 如果是@钉钉机器人链接，text为链接文本，url 字段为链接地址
    url: Optional[str] = Field(None, description="富文本消息中的链接URL")


class PictureContent(MessageContent):
    """图片消息内容"""

    pictureDownloadCode: Optional[str] = Field(
        None,
        description="图片文件的下载码，调用服务端API-下载机器人接收消息的文件内容接口，获取临时下载链接。",
    )
    downloadCode: Optional[str] = Field(
        None,
        description="图片文件的下载码，调用服务端API-下载机器人接收消息的文件内容接口，获取临时下载链接。",
    )
    type: Optional[Literal["picture"]] = Field(
        None, description="消息类型，固定为 picture"
    )


class AudioContent(MessageContent):
    """音频消息内容"""

    duration: Optional[int] = Field(None, ge=0, description="音频时长，单位毫秒")
    downloadCode: Optional[str] = Field(
        None,
        description="语音文件的下载码，调用服务端API-下载机器人接收消息的文件内容接口，获取临时下载链接。",
    )
    recognition: Optional[str] = Field(None, description="语音转文字结果")


class VideoContent(MessageContent):
    """视频消息内容"""

    spaceId: Optional[str] = Field(None, description="视频所在的空间ID")
    fileName: Optional[str] = Field(None, description="视频文件名")
    duration: Optional[int] = Field(None, ge=0, description="视频时长，单位毫秒")
    fileId: Optional[str] = Field(None, description="视频文件ID")
    downloadCode: Optional[str] = Field(
        None,
        description="视频文件的下载码，调用服务端API-下载机器人接收消息的文件内容接口，获取临时下载链接。",
    )
    videoType: Optional[str] = Field(None, description="视频文件类型，例如 mp4")


class FileContent(MessageContent):
    """文件消息内容"""

    spaceId: Optional[str] = Field(None, description="文件所在的空间ID")
    fileName: Optional[str] = Field(None, description="文件文件名")
    downloadCode: Optional[str] = Field(
        None,
        description="文件文件的下载码，调用服务端API-下载机器人接收消息的文件内容接口，获取临时下载链接。",
    )
    fileId: Optional[str] = Field(None, description="文件ID")
    fileType: Optional[str] = Field(None, description="文件类型")


class RichTextContent(MessageContent):
    """富文本消息内容"""

    richText: Optional[List[Union[TextContentInRichText, PictureContent]]] = Field(
        None, description="富文本内容列表"
    )


class BaseDingRobotRequest(BaseModel):
    """
    基础钉钉机器人请求模型，包含所有公共字段。
    注意：
         1. 群聊会话中：群成员@机器人，机器人不支持接收语音、文件、视频类型。
         2. 人与人的会话中：机器人不支持接收语音、文件、视频类型。
         3. 人与机器人的会话中：机器人支持接收语音、文件、视频类型。
    """

    model_config = ConfigDict(
        extra="allow",  # 兼容钉钉额外字段
        str_strip_whitespace=True,  # 自动去除字符串前后空格
        use_enum_values=True,  # 序列化时输出枚举值（如 "richText"）而非枚举对象
    )

    # 公共字段
    senderPlatform: Optional[str] = Field(None, description="发送平台")
    conversationId: str = Field(..., description="会话ID")
    atUsers: Optional[List[AtUser]] = Field(None, description="@用户列表")
    chatbotCorpId: str = Field(..., description="机器人所在的企业corpId")
    chatbotUserId: str = Field(..., description="加密后的机器人ID")
    openThreadId: str = Field(..., description="打开线程ID")
    msgId: str = Field(..., description="加密的消息ID")
    senderNick: str = Field(..., description="发送者昵称")
    isAdmin: bool = Field(..., description="是否为管理员")
    # 该字段在机器人发布线上版本后，才会返回。
    senderStaffId: Optional[str] = Field(
        None, description="企业内部群中@该机器人的成员userid "
    )
    sessionWebhookExpiredTime: int = Field(
        ..., description="当前会话的Webhook地址过期时间"
    )
    createAt: int = Field(..., description="消息的时间戳，单位毫秒")
    senderCorpId: Optional[str] = Field(
        None, description="企业内部群有的发送者当前群的企业corpId"
    )
    conversationType: str = Field(..., description="会话类型（1：单聊，2：群聊）")
    senderId: str = Field(..., description="加密的发送者ID")
    conversationTitle: Optional[str] = Field(None, description="群聊时才有的会话标题")
    isInAtList: Optional[bool] = Field(None, description="是否在@列表中")
    sessionWebhook: str = Field(..., description="会话 Webhook 地址")
    robotCode: Optional[str] = Field(None, description="机器人编码")
    msgtype: MsgType = Field(..., description="消息类型")


# 各消息类型的请求模型
class TextRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.TEXT] = MsgType.TEXT
    text: TextContent


class PictureRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.PICTURE] = MsgType.PICTURE
    content: PictureContent


class AudioRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.AUDIO] = MsgType.AUDIO
    content: AudioContent


class VideoRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.VIDEO] = MsgType.VIDEO
    content: VideoContent


class FileRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.FILE] = MsgType.FILE
    content: FileContent


class RichTextRequest(BaseDingRobotRequest):
    msgtype: Literal[MsgType.RICH_TEXT] = MsgType.RICH_TEXT
    content: RichTextContent


# 统一请求类型
DingRobotRequest = Union[
    TextRequest,
    PictureRequest,
    AudioRequest,
    VideoRequest,
    FileRequest,
    RichTextRequest,
]
