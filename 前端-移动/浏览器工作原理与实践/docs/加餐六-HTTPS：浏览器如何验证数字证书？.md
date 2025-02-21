你好，我是李兵。

在《[36｜HTTPS：让数据传输更安全](https://time.geekbang.org/column/article/156181)》这篇文章中，我们聊了下面几个问题：

- HTTPS使用了对称和非对称的混合加密方式，这解决了数据传输安全的问题；
- HTTPS引入了中间机构CA，CA通过给服务器颁发数字证书，解决了浏览器对服务器的信任问题；
- 服务器向CA机构申请证书的流程；
- 浏览器验证服务器数字证书的流程。

不过由于篇幅限制，关于“**浏览器如何验证数字证书”**的这个问题我们并没有展开介绍。那么今天我们就继续聊一聊这个问题。了解了这个问题，可以方便我们把完整的HTTPS流程给串起来，无论对于我们理解HTTPS的底层技术还是理解业务都是非常有帮助的。

因为本文是第36讲的延伸，所以在分析之前，我们还是有必要回顾下**数字证书申请流程**和**浏览器验证证书的流程**，同时你最好也能回顾下第36讲。

## 数字证书申请流程

我们先来回顾下数字证书的申请流程，比如极客时间向一个CA机构申请数字证书，流程是什么样的呢？

首先极客时间填写了一张含有**自己身份信息**的表单，身份信息包括了自己公钥、站点资料、公司资料等信息，然后将其提交给了CA机构；CA机构会审核表单中内容的真实性；审核通过后，CA机构会拿出自己的私钥，对表单的内容进行一连串操作，包括了对明文资料进行Hash计算得出信息摘要， 利用CA的私钥加密信息摘要得出数字签名，最后将数字签名也写在表单上，并将其返还给极客时间，这样就完成了一次数字证书的申请操作。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/45/b5/2a268b7e.jpg" width="30px"><span>世界和平</span> 👍（40） 💬（1）<div>工作两年，对很多前端知识有的还是比较乱的，一知半解禁不住深究，老师的课程帮助很好的梳理了这些知识，也详细的讲解了，让我有了系统的认知，也为之后的继续学习提供了方向，非常的感谢老师，很值。已经推荐给朋友，以后如果老师再出课，也会继续跟着学习。 我不是托，我不是托，我就是真诚的表示一下感谢。谢谢 ~ </div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/32/7ff3ae1d.jpg" width="30px"><span>雨儿</span> 👍（2） 💬（1）<div>老师太好了，每天都会看看，是否老师有新的更新，期待老师不定期能更新一些</div>2020-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/ba/0599cc8a.jpg" width="30px"><span>pacos</span> 👍（11） 💬（0）<div>期待老师的 Promise 加餐</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/0c/2ebdc487.jpg" width="30px"><span>魔兽rpg足球</span> 👍（8） 💬（1）<div>盗版的操作系统也有可能安装了恶意根证书啊，所以大家支持正版吧</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/21/df75ca94.jpg" width="30px"><span>林浩</span> 👍（4） 💬（0）<div>总结：
浏览器怎么验证证书？
一般通过 验证证书有效期， 证书是否被CA吊销，证书是否是合法CA机构颁发

  如何验证证书有效期？
  证书里面包含有效期

  如何获知证书被吊销？
  1. 下载吊销证书列表   2. 在线验证

  如何证明是合法CA机构？
  1. 通过证书原始信息（hash）计算消息摘要
  2. 利用CA公钥解密证书中的数字签名，得到消息摘要
  3. 将两者进行对比

浏览器怎么拿到CA公钥？
服务器部署时，除了当前数字证书外，还需要部署CA证书，CA证书上就包含了CA公钥，当建立HTTPS连接时，服务器会往浏览器发送两个证书，如果服务器上没有部署CA证书，浏览器会通过网络下载CA证书，也可以拿到CA公钥

这里只证明了CA公钥的来源，怎么知道它是合法机构？
很遗憾没有！退而求其次，计算机操作系统内置了一些颁发证书的机构，但因为机构众多不可能这么处理，所以将证书分成了“根CA”和“中间CA”，一个“根CA”会有多个“中间CA”，“根”给“中间”做认证

怎么知道根证书的合法性？
要成为“根CA”需要得到“Web Trust”认证通过才会内置到操作系统中，Web Trust 包括两个机构（AICPA【美国注册会计师协会】和 CICA【加拿大注册会计师协会】）

如果操作系统被入侵如何保证跟证书合法性？
凉凉。。。</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（4） 💬（8）<div>这篇文章就解决了客户端验证服务器正确性的问题。但是我有一个小疑问，如果我伪造了一个客户端，同时拿到数字签名和CA公钥，通过CA公钥解密数字信息，这样是否能骗取服务端的信任？老师可以讲讲这中间的细节吗？</div>2020-01-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJeUiajzIgiaAicogQkfjBm4wKVtkc1vKYAA3BfCV85V9ZOovJRCBROpZOweO2zMwFgLhxpJ458qohbA/132" width="30px"><span>Geek_c9436e</span> 👍（3） 💬（0）<div>我看完了，酣畅淋漓的感觉，满满干货，意犹未尽啊，给老师点赞，希望继续学习老师的课！</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0e/94/4a2bb019.jpg" width="30px"><span>Lorin</span> 👍（2） 💬（0）<div>老师开一个前端专栏吧，前端领域里面找一个如此高质量的课程简直是太少了。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（2） 💬（1）<div>我感觉老师这篇是看到了我之前的留言，专门延伸的一篇文章，点赞！</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0f/c0/e6151cce.jpg" width="30px"><span>花仙子</span> 👍（2） 💬（1）<div>众所周知，青花瓷工作原理就是在个人主机上设置了一个代理，浏览器信任代理，代理验证并信任服务器的证书，所以可以在青花瓷中看到https的请求内容，同样原理，有没有可能在我们的浏览器在访问服务器之间设置一个代理，而致使浏览器无知觉的先请求到”代理服务器“，而”代理服务器“也拥有CA颁发的合法证书，”代理服务器“可以肆无忌惮的查看甚至修改浏览器与服务器间的通信</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/70/466368e1.jpg" width="30px"><span>杰森莫玛</span> 👍（1） 💬（1）<div>那CA机构的数字证书到底是操作系统内置的还是服务端传过来的呢？</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/28/8c83d109.jpg" width="30px"><span>子曰</span> 👍（1） 💬（0）<div>通过图解的方式把一些底层的原理阐述的很清晰，老师辛苦，干货满满的课程������</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（1） 💬（1）<div>如果有些服务器没有部署 CA 的数字证书，那么浏览器还可以通过网络去下载 CA 证书，不过这种方式多了一次证书下载操作，会拖慢首次打开页面的请求速度，一般不推荐使用。

老师这块没听明白？这是默认因为吗？下载的是中间CA证书吗？去网络中什么地方下载？如何确保下载CA的有效性？
感谢。</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡，看完了，非常不错，干货满满</div>2024-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/40/2e/eff62a47.jpg" width="30px"><span>hadiss</span> 👍（0） 💬（0）<div>浏览器的hash算法是怎么和CA的hash一样的呢</div>2023-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e8/e2/ffb29a7d.jpg" width="30px"><span>雷厉</span> 👍（0） 💬（0）<div>感谢老师的分享</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/46/16/7eab6017.jpg" width="30px"><span>undefined</span> 👍（0） 💬（0）<div>看完了 感谢分享</div>2021-03-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLC4IhKmJDYdWhQms3dmZqJ5YMDGTlPa1o52DnKSErYjsqfc6iaRJrBDZpx0RqQx7eZAED797kiaV6aw/132" width="30px"><span>陈启航</span> 👍（0） 💬（0）<div>值得之后前端开发经验更多之后 回来重读</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/d5/b08a27ed.jpg" width="30px"><span>灵感_idea</span> 👍（0） 💬（0）<div>学完打个卡，老师讲的挺全面的，虽然很多地方稍显粗略，但或许是更利于接受的，还是要多学几遍，反复琢磨。</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/4b/b9/2449c7b7.jpg" width="30px"><span>‏5102</span> 👍（0） 💬（0）<div>虽然之前有到处查询百度过这些知识，到目前为止，这个专栏让我彻底重新认识浏览器等，也理清很多的疑惑，真是醍醐灌顶的感觉，非常赞，v8那篇我还是会继续订阅的。</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（0）<div>中间CA众多，如果证书链很长的话，浏览器对每一个中间证书都需要发起https请求去中间网站的CA获取么？</div>2020-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eokuZYcbHTG2HAICdczY7LX1dmFdIOPdJSJVWrzDQEP19QeUssibEvUoWaB7ode6zTYj2Wen0jFhZQ/132" width="30px"><span>Learning</span> 👍（0） 💬（0）<div>谢谢老师的加餐</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（0） 💬（0）<div>很好的解答了客户端是如何拿到CA公钥以及根CA的存储问题。说好的promise呢，哈哈。
题外话，极客时间课程更新没提示了，之前都有的。不知道是不是因为课程标记为”选学“的原因。
</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（0） 💬（1）<div>文中“通常，当你部署 HTTP 服务器的时候，除了部署当前的数字证书之外”，那个应该是HTTPS吧</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>良心老师！</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c2/82/58debf3e.jpg" width="30px"><span>lang</span> 👍（0） 💬（0）<div>老师辛苦啦</div>2019-12-20</li><br/>
</ul>