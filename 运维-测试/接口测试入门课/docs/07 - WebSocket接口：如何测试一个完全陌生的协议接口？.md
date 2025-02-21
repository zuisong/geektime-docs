你好，我是陈磊。很高兴你又来和我一起探寻接口测试的奥秘了。

我们在前面一起学习了怎么分析和完成一个HTTP协议的接口测试，又一起学习了如何封装接口测试框架，以及如何搭建接口测试平台。我相信，现在你已经完全掌握了HTTP协议的接口测试了。

但是，这还不能说明你已经能独立完成接口测试了，为什么这么说呢？这是因为数据在网络传输上都是依靠一种协议来完成的，在上学的时候，你肯定学过包括TCP、UDP、HTTP等在内的一堆协议，但是如果你遇见了一个全新的协议，你知道怎么从零开始，完成接口测试吗？

今天我就以WebSocket为例，告诉你当你第一次接触一个完全陌生的协议接口时，你要如何开始完成接口测试工作。

## 未知的新协议接口并不可怕

作为一名测试工程师，在面对一个陌生协议的接口测试时，你是不是会常常感到很无助？面对这样的任务时，你的第一反应肯定是向开发工程师求助，因为开发工程师基于新协议已经完成了接口开发，向开发工程师求助显然是最好的办法。

我在工作中就遇见过类似的事情。记得那是在我参加工作的前几年，有一个被测项目的接口是一个私有协议，当我看到接口文档的时候，第一反应就是找开发工程师，向他求教一下这个私有协议。这个开发工程师人很好，他给了我一个学习脉络，其中包含了协议的说明文档、代码开发文档、实现代码等内容，我拿到这些资料后，马上按照上面他给出的学习顺序投入学习。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/2e/01/14a478bb.jpg" width="30px"><span>happychap</span> 👍（17） 💬（1）<div>我的尝试的一般顺序：现成工具，工具现成插件，测试框架+项目组封装或采用的api库（如：junit +对应的协议开源库）。
个人觉得遇到这种情况，要会点编程，孰练测试框架胜算才大ʘᴗʘ
工作中有突然遭遇xmpp和mqtt协议性能测试的经历，最终jmeter+开源插件+厂商client jar包+demo+api手册搞定了任务。</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（12） 💬（7）<div>年前刚好公司年会，然后开发了个聊天小程序，就给我测。当时完全不知道怎么搞，就去看这个协议。然后就想先抓包，结果抓不到，捣鼓了修改fiddler抓到了包，然后也是看抓到的数据好像跟平时不一样，然后各种搜索，平时使用的jmeter，就在jmeter中按往常的来试试，正常取样器不行，最后看到jmeter中有个websocket取样器，开心完成压测。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/18/a5218104.jpg" width="30px"><span>🐾</span> 👍（8） 💬（3）<div>像微服务接口，一般都是使用特殊协议如dubbo、protobuf进行通信的，这种情况应该怎么做测试呢？只能用自己擅长的编程语言写一个客户端模拟调用来进行测试？这种还需要连接配置中心什么的。而且会不会存在有些协议是不跨语言的，比如仅限Java语言，不支持python。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/46/aa/5e1b5a8a.jpg" width="30px"><span>罗春南_Nancy</span> 👍（7） 💬（1）<div>    self.ws=&#39;null&#39;--加个定义好点
    if api_type==&#39;ws&#39;:
      self.ws = create_connection(url_root)
    elif api_type==&#39;http&#39;:
      self.url_root = url_root

------------------------------------------

  # common类的析构函数，清理没有用的资源
  
  def __del__(self):
    &#39;&#39;&#39;
    :return:
    &#39;&#39;&#39;
    if self.ws!=&#39;null&#39;:------加个判断好点
      self.ws.close()

不然测http的时候websocket会报错。</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/75/71845744.jpg" width="30px"><span>VeryYoung</span> 👍（6） 💬（3）<div>好巧，websocket协议也是我遇到的第一个陌生协议，那个时候测试工期短，用的是java技术栈，就用了netty框架来封装，后面有时间了就进行回顾，发现还有有个websocket.jar开源包，后面又相继遇到了amqp、mqtt等非http协议！</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/b0/50bc0dd7.jpg" width="30px"><span>孟见大侠</span> 👍（3） 💬（1）<div>其实根本就不要加api_type这个参数，根据url_root 就可以知道协议类型了。ws:&#47;&#47;echo.websocket.org 是ws协议，https:&#47;&#47;echo.websocket.org是https协议。根据协议头，截取出来就可以了。这样可以少传一个参数。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d6/09/e9bfe86f.jpg" width="30px"><span>夜歌</span> 👍（1） 💬（6）<div>from websocket import create_connection，请问websocket是您自己封装的类吗？试着运行代码，发现没有websocket这个模块，然后pip install websocket 后也没有 create_connection 这个方法。所以是自己封装的吗？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b0/9f/16585556.jpg" width="30px"><span>shadow</span> 👍（1） 💬（1）<div>这里Common里增加了一个入参api_type『def __init__(self,url_root,api_type)』，用于标记请求协议类型，这实际相当于框架底层方法重构，一个方法是给这个入参加默认传参，就是之前的http，不知道还有没有别的方法？
还有一个就是，框架开发，会多多少少的涉及到底层重构，然后可能影响的就是所有的用例都需要修改，这种情况，不知道有没有什么好的规避方法？</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c3/35/133f7f4b.jpg" width="30px"><span>April Gao</span> 👍（0） 💬（1）<div>不懂就问，self.ws=&#39;null&#39;，python中没有null，请问这个写法是正确的吗？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e9/34/83025564.jpg" width="30px"><span>-_-</span> 👍（0） 💬（1）<div>elif api_type==&#39;http&#39;: self.ws=&#39;null&#39;这边为啥要加self.ws=&#39;null&#39;这边不加有什么影响吗既然是http为什么要写这一行是为了迎合析构函数吗</div>2020-07-30</li><br/><li><img src="" width="30px"><span>雪糕</span> 👍（0） 💬（1）<div>from common import Common 运行时报错：ModuleNotFoundError: No module named &#39;common&#39;
代码里确实没有小写的common模块，请问老师这是怎么回事呢？</div>2020-06-17</li><br/><li><img src="" width="30px"><span>博彦-孙文</span> 👍（0） 💬（1）<div>你好老师，我现在面临一个问题，RPC接口怎么用脚本实现接口测试？目前这类接口是蚂蚁的，属于人家的东西，Python中没有这样的工具包</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（1）<div>老师的故事很有趣</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/7f/1ecf6e89.jpg" width="30px"><span>Ruby | 成长精进</span> 👍（0） 💬（1）<div>ws消息通过jmeter请求发送成功了，但是聊天窗口没有收到消息，请问会是什么原因，现在遇到这个问题，求解中</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（0） 💬（3）<div>你好，我想问一下这里做陌生的协议接口测试，测试人员参考的依据是什么文档，我们怎么得知我们测试的接口准确性呢？</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（9） 💬（1）<div>过，定位很清楚，先搞定工作，再补充技术原理，技术原理是重要不紧急的事情，工作是重要紧急的事情，不过技术原理需要不断的补充才行，共勉。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/d3/62/791d0f5e.jpg" width="30px"><span>鑫宝</span> 👍（0） 💬（0）<div>技术发展到现在这个地步， 遇见不会的技术或者协议， 我们都要有一颗不畏难的心。 我们肯定不是第一个遇见的，也不是最后一个遇见的。大方的向开发、向百度、向gpt 询问就好了</div>2023-08-04</li><br/><li><img src="" width="30px"><span>张毅</span> 👍（0） 💬（0）<div>不错，工作中确实会遇到工具不支持的协议，比如jmeter性能测试时需要支持jmeter本身不支持的协议等，这种需要通过代码来拓展和实现</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/49/09/9afe9a24.jpg" width="30px"><span>三日月</span> 👍（0） 💬（1）<div>老师您好，websocket没有create_connection()啊</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（0） 💬（0）<div>遇到陌生协议的接口怎么办？文章解决问题的思路还是具有借鉴意义。
当你面对陌生技术问题的时候，你应该使用你最熟悉的技术去尝试解决问题。
先学习怎么使用新的协议，而不是先了解其底层。

如刚开始学习测试http协议的接口，刚开始的时候我可能不大清楚很多计算机网络的知识，什么七层模型、TCP&#47;IP协议族，我只要知道使用python的requests库可以发起get、post请求，就可以先做接口测试。</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/89/97/53b92627.jpg" width="30px"><span>Cubat</span> 👍（0） 💬（1）<div>第一次见到 Websocket 的时候也是头皮发麻，还有 HTTP2，不过好在后者目前用的不是很多。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>你这里协议均可找到类似import requests
from websocket import create_connection这样的类。那比如我在爱立信公司测试DNS、DHCP、AAA协议，我又如何用python进行测试呢，或许python就没类似协议的基类。</div>2020-04-20</li><br/>
</ul>