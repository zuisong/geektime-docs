你好，我是Chrono。

不知不觉，《透视HTTP协议》这个专栏马上就要两周岁了。前几天我看了一下专栏的相关信息，订阅数刚好破万，非常感谢包括你在内的所有朋友们的关心、支持、鼓励和鞭策。

在专栏的结束语里我曾经说过，希望HTTP/3发布之时能够再相会。而如今虽然它还没有发布，但也为时不远了。

所以今天呢，我就来和你聊聊HTTP/3的一些事，就当是“尝尝鲜”吧。

## HTTP/3的现状

从2019到2021的这两年间，大家对HTTP协议的关注重点差不多全都是放在HTTP/3标准的制订上。

最初专栏开始的时候，HTTP/3草案还是第20版，而现在则已经是第34版了，发展的速度可以说是非常快的，里面的内容也变动得非常多。很有可能最多再过一年，甚至是今年内，我们就可以看到正式的标准。

在标准文档的制订过程中，互联网业届也没有闲着，也在积极地为此做准备，以草案为基础做各种实验性质的开发。

这其中比较引人瞩目的要数CDN大厂Cloudflare，还有Web Server领头羊Nginx（而另一个Web Server Apache好像没什么动静）了。

Cloudflare公司用Rust语言编写了一个QUIC支持库，名字叫“quiche”，然后在上面加了一层薄薄的封装，由此能够以一个C模块的形式加入进Nginx框架，为Nginx提供了HTTP/3的功能。（可以参考这篇文章：[HTTP/3：过去，现在，还有未来](https://blog.cloudflare.com/zh-cn/http3-the-past-present-and-future-zh-cn/)）
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（8） 💬（2）<div>惊喜，刚刚好在学习第二遍，看到 HTTP&#47;3 的新文章更新。谢谢老师。</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/97/d0/95eaabef.jpg" width="30px"><span>水手辛伯达</span> 👍（3） 💬（1）<div>第二遍学习Chrono老师的http协议。这门课分层清晰，环环相扣，由简入繁，对于初中级前端和运维人员去了解http协议帮助是比较大的！最难能可贵的是，老师前后两年时间一直坚持更新，又增加了docker试验环节和http3的发展updates , 同时，老师十分注意和学员的互动，而且几乎和每个留言进行点评和分析，这些课后答疑又极大地分丰富了大家的知识，增涨了经验，十分庆幸在极客时间里面遇到这么优秀的课程！

祝老师健康，顺利！</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>打卡，真不错</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（1） 💬（1）<div>为老师对课程的持续关注和技术更新的科普点赞！</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/63/30/6f4b925c.jpg" width="30px"><span>Luca</span> 👍（0） 💬（2）<div>更新到了Chrome89.0.4389.90，无需进行额外设置就能够有QUIC支持了。</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（0） 💬（2）<div>实测chrome版本 88.0.4324.190（正式版本）无需设置可以支持quic
firefox 86.0需要简单设置一下，具体页面搜firefox，第一条就是
wireshark3.4.3抓包结果和大师一样，payload解不出来
请问大师，现在学习HTTP&#47;3，现在如果要深入了解HTTP&#47;3,需要看rfc吧？有没有其他好的资源？
</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/4e/1c654d86.jpg" width="30px"><span>Omooo</span> 👍（0） 💬（0）<div>牛逼！</div>2021-11-27</li><br/>
</ul>