上一节我们讲了RPC的经典模型和设计要点，并用最早期的ONC RPC为例子，详述了具体的实现。

## ONC RPC存在哪些问题？

ONC RPC将客户端要发送的参数，以及服务端要发送的回复，都压缩为一个二进制串，这样固然能够解决双方的协议约定问题，但是存在一定的不方便。

首先，**需要双方的压缩格式完全一致**，一点都不能差。一旦有少许的差错，多一位，少一位或者错一位，都可能造成无法解压缩。当然，我们可以用传输层的可靠性以及加入校验值等方式，来减少传输过程中的差错。

其次，**协议修改不灵活**。如果不是传输过程中造成的差错，而是客户端因为业务逻辑的改变，添加或者删除了字段，或者服务端添加或者删除了字段，而双方没有及时通知，或者线上系统没有及时升级，就会造成解压缩不成功。

因而，当业务发生改变，需要多传输一些参数或者少传输一些参数的时候，都需要及时通知对方，并且根据约定好的协议文件重新生成双方的Stub程序。自然，这样灵活性比较差。

如果仅仅是沟通的问题也还好解决，其实更难弄的还有**版本的问题**。比如在服务端提供一个服务，参数的格式是版本一的，已经有50个客户端在线上调用了。现在有一个客户端有个需求，要加一个字段，怎么办呢？这可是一个大工程，所有的客户端都要适配这个，需要重新写程序，加上这个字段，但是传输值是0，不需要这个字段的客户端很“冤”，本来没我啥事儿，为啥让我也忙活？
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/43/62/cd7d8b3b.jpg" width="30px"><span>叹息无门</span> 👍（37） 💬（1）<div>感觉这篇写的不是很严谨:
1，首先SOAP并非只能通过HTTP进行传输，关于SOAP binding应该提一下？
2，SOAP 的HTTP Binding 支持比较完整的Web Method，http GET&#47;POST都是可以支持的，并且对应不同的模式。大多数情况下只使用POST是具体实现的问题。</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/31/14f00b1c.jpg" width="30px"><span>燃</span> 👍（11） 💬（1）<div>webservice   soap的初始目标：服务自描述，其实就是没有达成，UDDI早已默默死掉</div>2018-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d5/00/a88c24c0.jpg" width="30px"><span>雪山飞猪</span> 👍（5） 💬（1）<div>这套教程真的是比以前看过的好多书都要生动形象，高手出马，化繁为简，非常感谢老师的倾情分享</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/2f/54f7f676.jpg" width="30px"><span>Jerry Chan</span> 👍（0） 💬（1）<div>但是这个二进制格式，怎么转换为xml这种格式呢？过程是怎么解析的呢？主要是这块不清楚，作者能解惑下不？</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/8e/0a546871.jpg" width="30px"><span>凡凡</span> 👍（17） 💬（0）<div>1.虽然http协议有post，get，head，put，delete等多种方法，但是平常来说post，get基本足够用。所以soap只支持post方法的差别应该在缺少get方法，get方法可以浏览器直接跳转，post必须借助表单或者ajax等提交。也就限制了soap请求只能在页面内获取或者提交数据。 
另外，soap协议规范上是支持get的，但是由于一般xml比较复杂，不适合放在get请求的查询参数里，所以soap协议的服务多采用post请求方法。
2.应该要讲restful协议了，一种使用json格式交互数据的，基于http协议的，轻量级网络数据交互规范。</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（10） 💬（3）<div>1.没有充分利用http协议原有的体系 比如get表示获取资源 post表示创建资源 delete表示删除资源 patch表示更新资源
2.restful协议</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（3） 💬（0）<div>1. POST 请求构造比较麻烦，需要专门的工具，所以调用和调试更费事。
2. 更简单的应该就是RESTful 了吧，SOAP 感觉不太好用，复杂度比较高，用起来没有http顺手。</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/b2/57c39f3d.jpg" width="30px"><span>vloz</span> 👍（3） 💬（0）<div>面向函数和面向对象在信息交互上的特征是什么？为什么讲onc合适面向函数？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（2） 💬（0）<div>题目1:
HTTP请求里面有很多种提交方式，文中只是提到了可以用post，其实还是可以用其他方式的，比如get。
题目2:
restful，用json格式的数据发送请求和返回数据。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/5e/9431165a.jpg" width="30px"><span>spdia</span> 👍（2） 💬（0）<div>soap的方言问题过于严重。其实简单场景可以用http rest或者json+http post,或者用比较新的graphql</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/40/18/cc3804e2.jpg" width="30px"><span>沈洪彬</span> 👍（1） 💬（1）<div>不是网络传输都要变成二进制传输么？  是不是xml也要变成二进制才能传输，这个是谁去做？ stub么？</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/bb/98a8b8be.jpg" width="30px"><span>LHW</span> 👍（1） 💬（0）<div>不用get是考虑传输的内容长度大小吧，如果是提交文件流的形式，post怎么处理？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/31/53b449e9.jpg" width="30px"><span>andy</span> 👍（1） 💬（0）<div>可以使用类似thrift的DSL来描述服务接口，然后生成服务端和客户端</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/78/eb86673c.jpg" width="30px"><span>我在你的视线里</span> 👍（0） 💬（0）<div>webserice和HTTP 有什么区别和联系呢？接口传数据不都是http传输吗？</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（0） 💬（0）<div>现在还有用SOAP协议的吗？</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/72/85/c337e9a1.jpg" width="30px"><span>老兵</span> 👍（0） 💬（0）<div>1. 用post是因为每次都是到service创建一些资源，之前为什么只用post呢？是不是因为访问soap大部分情况都是需要在服务端保存一些数据之类？ get, post, put, patch, delete也都是http协议里面的method类型。
2. restful，grpc</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/f9/b2fe7b63.jpg" width="30px"><span>King-ZJ</span> 👍（0） 💬（0）<div>在微服务调用这块得多学多看多实践。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7a/32/27a8572a.jpg" width="30px"><span>渣渣</span> 👍（0） 💬（0）<div>1.只用http (参数在body中)，如果客户端不是用post接收，就收不到，有一些不太灵活，
2.restful</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（0） 💬（0）<div>读完之后才发现最初的rpc协议并没有做到对调用者的完全透明，不利于扩展</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/32/535e5c3c.jpg" width="30px"><span>mlbjay</span> 👍（0） 💬（0）<div>之前工程里需要调用第三方的SOAP接口，于是研究了一下web servies，但是云里雾里的。
这下感觉WSDL，XML，SOAP等技术的关系现在清晰多了。</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a8/1b/ced1d171.jpg" width="30px"><span>空档滑行</span> 👍（0） 💬（0）<div>1.只使用post需要把动作封装到传输内容里
2.其他的协议比如json 
</div>2018-08-02</li><br/>
</ul>