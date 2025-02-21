你好，我是Barry。

在上节课我们实现了直播推拉流，并且完成了视频直播和直播存储功能。现在你应该对推拉流到直播视频播放的全过程非常熟悉了，但目前系统仍然不够完备，还有很多功能点需要完善。

所以，这节课我们将会整合直播所有的流程以及相关的功能接口，让系统更完备。这节课我们主要会解决后面这几个问题。

- 如何实现直播权限验证？
- 如何做推流验证？
- 如何用OBS实现音频采集和推流？
- 如何创建直播间？

好，话不多说，咱们正式开始。

## 直播权限验证

当一个用户想要发起直播时，系统需要验证用户的直播权限，当用户的直播权限验证通过之后，才能发起直播，这么做是为了增强平台的安全性和规范性。

想要完成权限验证，我们首先要在用户表中设定权限字段。具体就是在UserInfo数据库表模型中新增该字段，这样到了后面接口操作时，我们才能通过该字段状态做权限的判断。

具体的用户信息表字段如下所示，对应的路径是model/user.py。

```plain
class UserInfo(BaseModels, db.Model):
    """用户信息表"""
    __tablename__ = "user_info"
    #######
    is_streamer = db.Column(db.SmallInteger, default=0) #用于直播权限判断
    active = db.Column(db.SmallInteger, default=0) #用户状态
    last_message_read_time = db.Column(db.DateTime)
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/9f/d6042f62.jpg" width="30px"><span>liaozd</span> 👍（0） 💬（1）<div>老师，nginx的完整配文件有没？我看git上面没有</div>2024-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0f/4b/791d0f5e.jpg" width="30px"><span>Geek_zef</span> 👍（0） 💬（1）<div>查询视频流是否存在 如果存在直接删除，为什么有删除这个操作，业务逻辑不太懂</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1： name表示key，这个感觉不是很合适啊。
Q2： 文中的OBS推流是服务端的行为吗？
假设主播用手机，数据首先是从手机推到服务器，即推流是手机端的行为啊。
Q3：能否有一课来详细说明一下部署？
我对音视频和python都不熟悉，不过课程很好。我都是在地铁上看专栏的，
平时没有操作过。课程很有价值，很想操作一遍。期待老师写一个详细的部署文档，
比如，需要两台电脑，电脑A上部署XXX，电脑B上部署XXXX，等等。
正课或加餐都可以。</div>2023-07-18</li><br/>
</ul>