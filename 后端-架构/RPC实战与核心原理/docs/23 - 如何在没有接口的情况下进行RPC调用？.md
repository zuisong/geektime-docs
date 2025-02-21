你好，我是何小锋。上一讲我们学习了RPC如何通过动态分组来实现秒级扩缩容，其关键点就是“动态”与“隔离”。今天我们来聊聊如何在没有接口的情况下进行RPC调用。

## 应用场景有哪些？

在RPC运营的过程中，让调用端在没有接口API的情况下发起RPC调用的需求，不只是一个业务方和我提过，这里我列举两个非常典型的场景例子。

**场景一：**我们要搭建一个统一的测试平台，可以让各个业务方在测试平台中通过输入接口、分组名、方法名以及参数值，在线测试自己发布的RPC服务。这时我们就有一个问题要解决，我们搭建统一的测试平台实际上是作为各个RPC服务的调用端，而在RPC框架的使用中，调用端是需要依赖服务提供方提供的接口API的，而统一测试平台不可能依赖所有服务提供方的接口API。我们不能因为每有一个新的服务发布，就去修改平台的代码以及重新上线。这时我们就需要让调用端在没有服务提供方提供接口的情况下，仍然可以正常地发起RPC调用。

![](https://static001.geekbang.org/resource/image/fc/bc/fc0027ad042768d9aabf68182de5d2bc.jpg?wh=2792%2A1137 "示意图")

**场景二：**我们要搭建一个轻量级的服务网关，可以让各个业务方用HTTP的方式，通过服务网关调用其它服务。这时就有与场景一相同的问题，服务网关要作为所有RPC服务的调用端，是不能依赖所有服务提供方的接口API的，也需要调用端在没有服务提供方提供接口的情况下，仍然可以正常地发起RPC调用。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/ab/72/91c9853e.jpg" width="30px"><span>Reason</span> 👍（12） 💬（1）<div>能想到两种解决方法：
1. 通过泛化调用的接口名或者方法名，判断是否是泛化请求
2. 客户端发起调用时一定知道请求是泛化请求，因此可以在请求信息的附加字段中标识该请求为泛化请求</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（3） 💬（1）<div>没有接口API，调用者怎么使用插件完成序列化&#47;反序列化呢，总得知道序列化反序列化的目标Class才能进行吧</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（2） 💬（1）<div>方法名称需要特殊处理一下，参数不是很好，因为有的方法是没有参数的。</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a7/90/9a0da433.jpg" width="30px"><span>小哇</span> 👍（1） 💬（1）<div>老师好，我们这边是服务方也使用map做入参，然后在方法里再转成对象，就没有序列化问题，但感觉冗余。看到今天老师说的，意思是不是专属的序列化方式可以在调用方法前反序列为对象。这样做服务方的方法就可以使用对象入参而不用map做入参？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ab/72/91c9853e.jpg" width="30px"><span>Reason</span> 👍（1） 💬（3）<div>有个问题请教下老师，希望可以得到解答：
文中说泛化调用用于统一测试平台时，可以不需要修改平台代码重新上线。不修改平台代码重新上线，怎么编写相应的泛化调用代码呢？</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（0） 💬（2）<div>1.在原有的请求处理器里面加判断逻辑（不合理）。
2.单独为泛化请求添加请求处理器，在请求解析完，根据解析出来的数据决定走哪个处理器（泛化接口处理器，常规接口处理器）（合理）。


泛化请求不属于常规接口请求，它与常规请求应是平级的两种请求类型，故而认为应该将两种数据流分离，在编码层面就做好隔离，也为以后差异化迭代埋好扩展点。既增强语义准确性，也做前瞻性的需求预留。</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/bf/ee93c4cf.jpg" width="30px"><span>雨霖铃声声慢</span> 👍（0） 💬（1）<div>这个泛化调用好抽象，对于区分泛化调用和其他调用，一个是泛化调用的函数名和第一参数方法名，可以在这两个上做文章来分区泛化方法和其他方法</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/12/51b78d88.jpg" width="30px"><span>🐠</span> 👍（5） 💬（0）<div>对于Dubbo来说，根据org.apache.dubbo.config.AbstractReferenceConfig#generic 字段来标识该引用是否为泛化调用，所以根据该字段来使用对应的序列化插件就可以了，而且Dubbo对于POJO参数和返回值，统一都是用Map来接收的，可以看看官方文档https:&#47;&#47;dubbo.apache.org&#47;zh&#47;docs&#47;v2.7&#47;user&#47;examples&#47;generic-reference&#47;</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/f3/63fb86e4.jpg" width="30px"><span>王斌</span> 👍（0） 💬（0）<div>泛化调用性能只有正常调用的十分之一，有什么优化的办法吗？</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/38/5a857c96.jpg" width="30px"><span>ivan</span> 👍（0） 💬（0）<div>消息协议中定义泛化标示</div>2022-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/da/54/33dabd0a.jpg" width="30px"><span>闫同学</span> 👍（0） 💬（0）<div>grpc的unknownservice是不是个这个差不多呢？</div>2022-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/66/31c7969e.jpg" width="30px"><span>随风而逝</span> 👍（0） 💬（0）<div>也可以在定义传输协议时增加一位用来标识数据的请求类型</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>泛化序列化的具体细节怎么实现呢？二进制流总要变成对应的对象吧？还是需要一个对象来承载调用入参的，使用map？</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（0） 💬（2）<div>老师理论讲的很到位，深入理解还得去看代码，老师能否推荐一下学习rpc地方，理论听的明白，动手还差很多啊😊</div>2020-04-13</li><br/>
</ul>