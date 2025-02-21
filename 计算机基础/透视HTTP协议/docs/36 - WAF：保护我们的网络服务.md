在前些天的“安全篇”里，我谈到了HTTPS，它使用了SSL/TLS协议，加密整个通信过程，能够防止恶意窃听和窜改，保护我们的数据安全。

但HTTPS只是网络安全中很小的一部分，仅仅保证了“通信链路安全”，让第三方无法得知传输的内容。在通信链路的两端，也就是客户端和服务器，它是无法提供保护的。

因为HTTP是一个开放的协议，Web服务都运行在公网上，任何人都可以访问，所以天然就会成为黑客的攻击目标。

而且黑客的本领比我们想象的还要大得多。虽然不能在传输过程中做手脚，但他们还可以“假扮”成合法的用户访问系统，然后伺机搞破坏。

## Web服务遇到的威胁

黑客都有哪些手段来攻击Web服务呢？我给你大概列出几种常见的方式。

第一种叫“**DDoS**”攻击（distributed denial-of-service attack），有时候也叫“洪水攻击”。

黑客会控制许多“僵尸”计算机，向目标服务器发起大量无效请求。因为服务器无法区分正常用户和黑客，只能“照单全收”，这样就挤占了正常用户所应有的资源。如果黑客的攻击强度很大，就会像“洪水”一样对网站的服务能力造成冲击，耗尽带宽、CPU和内存，导致网站完全无法提供正常服务。

“DDoS”攻击方式比较“简单粗暴”，虽然很有效，但不涉及HTTP协议内部的细节，“技术含量”比较低，不过下面要说的几种手段就不一样了。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（29） 💬（4）<div>DDoS攻击从产生攻击对象的协议的角度来看可以分为L4攻击和L7攻击，前者其实是针对TCP状态机的恶意hack，比如攻击三次握手机制的SYN Flood和攻击四次握手的TIME WAIT2等，这些方面的防范超出了HTTPS的范畴，需要特殊的安全网管来过滤，清洗和识别。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（17） 💬（1）<div>HTTPS 为什么不能防御 DDoS、代码注入等攻击呢？
DDoS、代码注入本身是遵循HTTPS协议的，它的攻击面不在HTTPS协议层，而在其它层面，所以HTTPS 不能防御此类攻击。

你还知道有哪些手段能够抵御网络攻击吗？
我还知道有CSP内容安全策略，CSRF防御，SYN cookie，流速控制等手段。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/e6/9c77acff.jpg" width="30px"><span>我行我素</span> 👍（8） 💬（1）<div>https是做数据加密防止泄露，而ddos是以数量取胜（伪装成正常请求），</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（5） 💬（1）<div>https是对数据的进行加密传输，并且保证了数据的有效性，而不关心数据本身是什么，所以不能防止sql注入。DDos本身也是符合http规范的请求，所以https也无法将其识别为攻击。</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d9/78/8a328299.jpg" width="30px"><span>佳佳大魔王</span> 👍（4） 💬（1）<div>问题一，我觉得是因为https只提供了对通信过程中的数据进行加密，如果黑客用大量资源充当客户端，对服务器进行大量请求，https是无法阻止的，代码注入也是一样</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ff/87d8de89.jpg" width="30px"><span>snake</span> 👍（2） 💬（1）<div>那能否用waf来做https流量的入侵检测和防御呢？https的密文的，waf应该看不到吧？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/00/2a248fd8.jpg" width="30px"><span>二星球</span> 👍（2） 💬（1）<div>老师好，向您请教最近遇到的一个问题，APP应用通过http长链接向后台发送请求，中间有几个代理服务器，偶尔发现app发送的请求返回的状态码是正常的200，但是没有返回值，没有出错，后台也没有收到请求，这是什么原因，该如何解决呢？</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/7e/963c037c.jpg" width="30px"><span>Aaron</span> 👍（1） 💬（1）<div>这节课内容很重要呀，但有种只讲了冰山一角的感觉。老师能不能自己系统回答一下『你还知道有哪些手段能够抵御网络攻击吗？』呢？好期待官方答案~</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>HTTPS 为什么不能防御 DDoS、代码注入等攻击呢？
因为HTTPS的核心工作是加密解密通过HTTPS传输的内容，保证传输的内容是安全的，至于内容是一个“炸弹”还是一把“匕首”她是管不着的。</div>2020-04-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（0） 💬（1）<div>项目中使用过基于业务的规则引擎，完全自研的；waf应该是规则引擎比较典型的应用了。</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/b0/8b808d33.jpg" width="30px"><span>fakership</span> 👍（0） 💬（1）<div>老师讲的太干货了 还想着2d看完。。 高估了。。</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>请问老师如果我的业务接入ddos服务后，是否高防节点只会对请求流量进行4层行为的检查？</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（0） 💬（1）<div>打卡！</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/86/e3/a31f6869.jpg" width="30px"><span> 尿布</span> 👍（1） 💬（0）<div>“CC攻击”（Challenge Collapser）是“DDos”的一种，它使用代理服务器发动攻击</div>2020-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIqzCbNMTJHEVNER4p8bsd8RHv3Sg84Ykd8uYQkOwV57ZqXTLib0AqtP7csKxOrICeFvdUrQWFKl0Q/132" width="30px"><span>张良</span> 👍（0） 💬（0）<div>测试JS脚本共计	&lt;script&gt;alert(&#39;ok&#39;);&lt;&#47;script&gt;</div>2021-04-11</li><br/>
</ul>