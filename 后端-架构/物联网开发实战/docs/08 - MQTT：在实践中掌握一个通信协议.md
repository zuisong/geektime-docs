你好，我是郭朝斌。

在基础篇的[第 3 讲](https://time.geekbang.org/column/article/307518)中，我介绍了几种物联网系统中常用的网络协议。它们是物联网设备之间沟通的“语言”，使用同一种语言，双方才能通信成功。

那么，在这么多网络协议当中，最流行的是哪一种呢？毫无疑问，是MQTT协议，它甚至已经成为物联网系统事实上的网络协议标准。如果你想从事物联网开发，就一定要掌握MQTT。

所以这一讲，我就会带你了解MQTT，在实践中熟悉它的特性。

## 体验MQTT

为了让你对MQTT有一个直观的印象，我先带你体验一下它的通信过程，

第一步是安装 hbmqtt，它是一个开源的基于Python语言的 MQTT Broker 软件，正好包括我们需要使用一些工具。跟其他选择相比，这个软件安装起来非常方便，因为它在 Python 的 PYPI 软件仓库中就有，所以你通过 pip 命令就可以安装。这也是选择使用它的主要原因。

不过要注意的是，hbmqtt 是基于Python3实现的，因此这里使用的是 pip3 工具。

```
pip3 install hbmqtt
```

安装完成后，我们就可以使用 hbmqtt 中提供的 hbmqtt\_sub 和 hbmqtt\_pub 这两个命令行工具了。通过名字，你应该也可以看出 hbmqtt\_sub 可以充当**订阅者**的角色；hbmqtt\_pub 可以作为消息的**发布者**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/c4/40609b81.jpg" width="30px"><span>莹</span> 👍（13） 💬（5）<div>老师，我试了一下你给的代码
hbmqtt_sub --url mqtt:&#47;&#47;mqtt.eclipse.org:1883 -t &#47;geektime&#47;iot，这个URL有问题mqtt.eclipse.org我怎么也连不上；但是换成它页面上给的mqtt.eclipseprojects.io就没有问题。还有python 3.9 似乎重写了一些关于lock的代码，hbmqtt会有问题，Python 3.8就没问题。</div>2020-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eolBabicK5OTVJJJlUA4wwRtwCohCb75ahtbiaopsicnG3HRQTBOVEUrRY1KYCRZH78cDweQllh0Jzeg/132" width="30px"><span>like_wind</span> 👍（10） 💬（1）<div>自己用EMQ X搭建了一个broker服务器，收发消息成功，支持国产软件，不过EMQ文档真的很全。附上文档链接：https:&#47;&#47;docs.emqx.cn&#47;cn&#47;broker&#47;latest&#47;getting-started&#47;install.html</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（5） 💬（1）<div>测试了，如果pub和sub都是2，就是2组4次交互。如果只有pub为2，一组4次交互。但如果pub是1，sub为2，则测试结果和sub，pub都为1的情况一样，sub和broker之间不是4次交互。</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（3） 💬（1）<div>Client 在重复发送一个主题的消息时，可以从第二次开始，将主题名长度设置为 0，这样 Broker 会自动按照上次的主题来处理消息。这种情况对传感器设备来说十分常见，所以这个特性在工作中很有实际意义。

这段没有太懂, 有老哥给提示一下吗? 多谢了</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/55/4a/8a841200.jpg" width="30px"><span>ACK</span> 👍（3） 💬（2）<div>作为智能锁嵌入式开发者，觉得老师讲的东西很受用😃</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/04/1c/15c00997.jpg" width="30px"><span>9ambition</span> 👍（1） 💬（1）<div>针对思考题，我的回答是这样子的：
对于发布者（pub），采用QoS = 1，也就意味着就算broker已经收到此发布者发送的数据，发布者还是会重复一样的数字，对于发布者本身来说就是不想自己发出的每一条信息被遗漏。
对于订阅者（sub），采用QoS = 2, 说明sub在面对订阅主题时，每一次从broker获得数据前都会经过publish, pubreck, pubrel, pubcomp这四步后才能从订阅主题处获得一次数据。
所以broker的行为只需要从pub-broker和broker-sub两步看就可以：
对于pub-broker的部分，broker只需要进行puback来确认broker已经收到pub发送的数据了。
对于broker-sub的部分，broker一定要先确认自己执行了从pub获得的数据发出去的行为，也就是publish，接着确认收到sub的回复：pubrec来说明broker确实成功把数据发出去了；接着确认broker确实把数据发出去了，也就是pubrel；最后让sub回复pubcomp来说明sub确实收到broker发出的数据了。就相当于publish和pubrec是确认broker发数据的行为，pubrel和pubcomp是确认broker的数据内容已经被发送和被sub接收。</div>2021-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/30/d7/4999e677.jpg" width="30px"><span>大王叫我来巡山</span> 👍（1） 💬（1）<div>有java版本的 mqtt broker 么 最好是springboot开箱即用，且可开发的那种</div>2020-12-09</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVlib8n4JZhIomleMIyJTrbhn81kXG39DhJzrFMwmwxFsHCkicsC4CmY5Ft8icmzibWzmvibsDKDP3ORQ/132" width="30px"><span>InfoQ_Albert</span> 👍（1） 💬（2）<div>经实践SSL 证书已经可用，利用mqtts发布和订阅消息成功。</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（0） 💬（1）<div>https:&#47;&#47;mqtt.eclipse.org&#47; 打不开。</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c6/64/a8e09695.jpg" width="30px"><span>假行僧</span> 👍（0） 💬（1）<div>老师，遇到错误MOSQ_ERR_EAI代表什么意思？</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/56/41cbcda2.jpg" width="30px"><span>Sissi</span> 👍（0） 💬（2）<div>如果有第三个字节，那它的最高位表示是否有第四个字节，来和第二个字节、第三个字节一起表示字节总个数。依此类推，还可能有第四个字节、第五个字节，不过这个表示可变头部和消息体的字节个数的部分，最多也只能到第五个字节，所以可以表示的最大数据包长度有 256MB。 这个256MB是怎么计算出来的呢？我不太懂</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/30/d7/4999e677.jpg" width="30px"><span>大王叫我来巡山</span> 👍（0） 💬（1）<div>老师,你们公司在现实环境中mqtt broker 是使用类似emq这类成熟的软件么   还是自己开发?</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/fd/711df44c.jpg" width="30px"><span>天得一以清</span> 👍（0） 💬（1）<div>不同版本的client broker能同时做行吗？</div>2021-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK5icO2A4K7HYTYfQoagTz7VbtgxfS2ibBqLnKVWwQZgsePibZWFvFJEhPT8BtpQSaFx9IEodyp6c0dw/132" width="30px"><span>Geek_jg3r26</span> 👍（0） 💬（1）<div>发布 订阅模式可以理解为 观察者或者通知设计模式吗。，都是一对多的关系。</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/c4/40609b81.jpg" width="30px"><span>莹</span> 👍（0） 💬（6）<div>我用不加密的mqtt发布&#47;订阅连不上broker，总是timeout，试了很多次，也到网上搜了一下，但没有找到解决办法。有其他小伙伴遇到这个问题吗？也想请教一下老师。
[2020-12-16 21:50:17,454] :: WARNING - MQTT connection failed: TimeoutError(60, &quot;Connect call failed (&#39;198.41.30.194&#39;, 1883)&quot;)
[2020-12-16 21:50:17,455] :: INFO - Finished processing state new exit callbacks.
[2020-12-16 21:50:17,456] :: INFO - Finished processing state disconnected enter callbacks.
[2020-12-16 21:50:17,456] :: WARNING - Connection failed: ConnectException(TimeoutError(60, &quot;Connect call failed (&#39;198.41.30.194&#39;, 1883)&quot;))
[2020-12-16 21:50:17,456] :: CRITICAL - connection to &#39;mqtt:&#47;&#47;mqtt.eclipse.org:1883&#39; failed: ConnectException(TimeoutError(60, &quot;Connect call failed (&#39;198.41.30.194&#39;, 1883)&quot;))</div>2020-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/91/6606a3c5.jpg" width="30px"><span>A-Bot</span> 👍（0） 💬（3）<div>老师，我知道MQTT协议5.0版本实现了请求应答模式。但是我想请教下，在MQTT协议中，订阅者如何主动拉取消费信息？
麻烦您看见还能回答下，谢谢</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/b3/446b877d.jpg" width="30px"><span>Felix</span> 👍（0） 💬（1）<div>发布着选择忽略PUBACK?
如果反过来，发布者选择QoS等级是2，订阅者选择QoS等级是1呢？发布者就会重复发布同样的消息？
————————
如果 Client 发布消息时选择的 QoS 等级是 1 ，而订阅者在订阅这个主题消息时选择的 QoS 等级是 2 ，这种情况下 Broker 会怎么处理呢？

</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/0d/71053329.jpg" width="30px"><span>il李li</span> 👍（0） 💬（1）<div>MQTT Broker 根据客户端建立连接时选择的QoS级别与客户端交互，也即是与发布消息的Client按照QoS=1 （至少一次）处理，broker将消息推送给订阅这个主题的Clien时选择 QoS=2（只有一次）来处理</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/c3/18fce18c.jpg" width="30px"><span>Justone</span> 👍（18） 💬（3）<div>1.  pip install hbmqtt 后运行 hbmqtt_sub 或 hbmqtt_pub 命令，抛出了 ModuleNotFoundError: No module named &#39;websockets.protocol&#39;
2.  抛出异常的代码是 from websockets.protocol import, no module 可能是相应的 protocol.py 文件缺失
3.  这时可以根据命令行提示的错误路径，ls 一下 websockets 文件夹有什么东西，会发现没有 protocol.py 文件
4.  在网上检索 websockets，发现它源码在 github 中，这个 repo 用 tag 区别不同版本，通过对比可以发现，在 websockets 9.0 之后去除了 protocol.py 文件，在 8.1 以前还保留着 protocol.py
5.  解决思路有两个：
a.  修改 hbmqtt 库的 adapters.py 代码（可能还有其它地方要改）
b.  降低 websockets 版本（pip uninstall websockets; pip install websockets==8.1; 问题解决)</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/c4/40609b81.jpg" width="30px"><span>莹</span> 👍（3） 💬（3）<div>老师给的思考题，用wireshark试了一下，第一次用，不太确定理解完全正确——我感到都是按照publisher的QoS等级走的：

如果 Publisher QoS 1 (at least once)，subsciber QoS 2（exactly once），我看到的是有两次Publish Message，然后两次Publish Ack。

如果反过来，Publisher QoS 2（exactly once），subsciber QoS 1 (at least once)，我看到的情况是会有publish确认，看到这几个连续动作Publish Message, Publish Received, Publish Release, Publish Complete, Publish Ack</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/b6/8c/d5019728.jpg" width="30px"><span>予歌</span> 👍（1） 💬（0）<div>抛出了 ModuleNotFoundError: No module named &#39;websockets.protocol&#39;
可以用
pip install &quot;websockets==8.1&quot;
解决</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b8/bc/5f4c9cb2.jpg" width="30px"><span>掂过碌蔗</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;njouanin&#47;hbmqtt&#47;issues&#47;239

mac 安装hbmqtt 1.15.0 之后，输入hbmqtt_sub、hbmqtt等命令，会报websockets找不到一些东西，是因为版本问题。降一下版本就好了。

安装websockets命令：
pip install &quot;websockets==8.1&quot;

报错信息：
ImportError: cannot import name &#39;WebSocketCommonProtocol&#39; from &#39;websockets.protocol&#39; (&#47;Users&#47;dujiabao&#47;Library&#47;Python&#47;3.9&#47;lib&#47;python&#47;site-packages&#47;websockets&#47;protocol.py)</div>2024-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/03/f1/69e111f0.jpg" width="30px"><span>walter</span> 👍（0） 💬（0）<div>如何用MQTT连接海康威视 普联这些品牌的摄像头呢</div>2024-04-18</li><br/><li><img src="" width="30px"><span>Geek_bobo</span> 👍（0） 💬（0）<div>老师您好
 
python3.10.0，websockets==8.1，订阅主题时报错：
TypeError: As of 3.10, the *loop* parameter was removed from Event() since it is no longer necessary

这个该如何解决，我若将websockets升高又会报“TypeError: As of 3.10, the *loop* parameter was removed from Event() since it is no longer necessary”</div>2022-07-01</li><br/><li><img src="" width="30px"><span>Geek_58fcf2</span> 👍（0） 💬（0）<div>学习总结：
mqtt协议
1.生态丰富
2.二进制传输
3.适合物联网的模式，发布与订阅
3.低功耗
4.安全</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f0/b1/2ec47baa.jpg" width="30px"><span>icekiller</span> 👍（0） 💬（0）<div>客户端c,服务器s
(pub0,sub0)(pub0,sub1)(pub0,sub2) 一发一回共2条消息

(pub1,sub1)(pub1,sub2) c(Publish Message)-&gt;s(Publish Ack)-&gt;s(Publish Message)-&gt;c(Publish Ack)共4条消息
(pub1,sub0) c(Publish Message)-&gt;s(Publish Ack)-&gt;s(Publish Message) 共3条消息

(pub2,sub2) c(Publish Message)-&gt;s(Publish Received)-&gt;s(Publish Message)-&gt;c(Publish Release)-&gt;s(Publish Complete)-&gt;c(Publish Received)-&gt;s(Publish Release)-&gt;c(Pubish Complete) 两组共8条消息
(pub2,sub1) c(Publish Message)-&gt;s(Publish Received)-&gt;s(Publish Message)-&gt;c(Publish Release)-&gt;s(Publish Complete)-&gt;c(Publish Ack)共6条消息
(pub2,sub0) c(Publish Message)-&gt;s(Publish Received)-&gt;s(Publish Message)-&gt;c(Publish Release)-&gt;s(Publish Complete)共5条消息
</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（0）<div>我看老师的整个课程所有的设备交互都是基于MQTT，但是MQTT本质上是一个订阅发布模式，老师会用MQTT来做一些需要返回值（比如查询命令，或者修改命令但是需要知道执行成功与否）的命令下发吗？</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（0） 💬（0）<div>MQTT的客户端和broker之间的通信是长连接吗？ 如果客户端断开连接，从broker发给客户端的消息怎么到达客户端？ </div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/8a/891b0e58.jpg" width="30px"><span>wnz27</span> 👍（0） 💬（0）<div>一个请求建立连接的 CONNECT 类型数据包，头部需要 14 个字节；发布消息的 PUBLISH 类型数据包头部只有 2～4 个字节。 
这个咋算的啊老师~~~~</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/e0/27d3cafe.jpg" width="30px"><span>开心点朋友们，人间不值得</span> 👍（0） 💬（0）<div>有个疑问，对于实际情况来说，mqtt的服务是要发布者和订阅者都能访问吗？是不是要暴露在公网上</div>2021-11-08</li><br/>
</ul>