你好，我是Barry。

上节课，我们初步了解了Flask认证机制，也完成了使用Token进行认证的前置工作。在我们的视频直播平台中，也需要通过认证机制来实现用户的平台认证和安全保障。

这节课，我们就进入项目实战环节，巩固一下你对Flask认证机制的应用能力。整体流程包括生成Token、Token验证、登录认证和用户鉴权这四个环节。

认证的第一步，我们就从生成Token开始说起。

## 生成Token

[上节课](https://time.geekbang.org/column/article/669871)，我们学习过Token结构，它有三个部分，分别是header，playload和signature。

在项目中我们借助Flask的扩展Flask-JWT来生成Token，具体就是使用JWT.encode函数将JSON对象编码为JWT Token。因此，我们有必要了解一下JWT.encode函数的参数，你可以参考后面我画的思维导图。

![](https://static001.geekbang.org/resource/image/2b/da/2b08510cae1b9446918329388223edda.jpg?wh=1900x922)

你或许注意到了，在JWT.encode函数中只传入了payload部分。这是因为在使用JWT.encode函数时，会自动根据默认算法生成Header部分，并将Header和Payload部分进行签名生成最终的Token字符串。我们需要手动指定Payload部分。

具体生成Token的实现代码是后面这样，你可以参考一下。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ec/58/7948ea79.jpg" width="30px"><span>胡歌衡阳分歌</span> 👍（1） 💬（3）<div>这个教程是相当的不完整啊，看的心烦</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/24/6c621045.jpg" width="30px"><span>石佛慈悲</span> 👍（0） 💬（1）<div>token存在redis里的意义是啥呢，为啥还要校验redis的token，不是解码比对都已经校验了吗？为了控制token失效？</div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：Config.SECRET_KEY是系统自带的吗？
Q2：token放在http的header中的Authorization字段，Authorization字段是http固有的字段吗？记不清楚了，好像应该是自定义字段？</div>2023-06-27</li><br/>
</ul>