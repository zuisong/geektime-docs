你好，我是蔡元楠。

今天我要与你分享的主题是“ Apache Beam的前世今生”。

从这一讲开始，我们将进入一个全新的篇章。在这一讲中，我将会带领你了解Apache Beam的完整诞生历程。

让我们一起来感受一下，Google是如何从处理框架上的一无所有，一直发展到推动、制定批流统一的标准的。除此之外，我还会告诉你，在2004年发布了MapReduce论文之后，Google在大规模数据处理实战中到底经历了哪些技术难题和技术变迁。我相信通过这一讲，你将会完整地认识到为什么Google会强力推崇Apache Beam。

在2003年以前，Google内部其实还没有一个成熟的处理框架来处理大规模数据。而当时Google的搜索业务又让工程师们不得不面临着处理大规模数据的应用场景，像计算网站URL访问量、计算网页的倒排索引（Inverted Index）等等。

那该怎么办呢？这个答案既简单又复杂：自己写一个。

没错，当时的工程师们需要自己写一个自定义的逻辑处理架构来处理这些数据。因为需要处理的数据量非常庞大，业务逻辑不太可能只放在一台机器上面运行。很多情况下，我们都必须把业务逻辑部署在分布式环境中。所以，这个自定义的逻辑处理架构还必须包括容错系统（Fault Tolerant System）的设计。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（79） 💬（2）<div>文章中的几篇论文地址：
0. MapReduce: https:&#47;&#47;research.google.com&#47;archive&#47;map reduce-osdi04.pdf 
1. Flumejava: https:&#47;&#47;research.google.com&#47;pubs&#47;archive&#47;35650.pdf
2. MillWheel: https:&#47;&#47;research.google.com&#47;pubs&#47;archive&#47;41378.pdf
3. Data flow Model: https:&#47;&#47;www.vldb.org&#47;pvldb&#47;vol8&#47;p1792-Akidau.pdf

个人认为还是应该读一读的，毕竟几十年的发展不能靠看一两篇文章就搞清楚的
</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/b8/6510592e.jpg" width="30px"><span>渡码</span> 👍（42） 💬（1）<div>我举一个前端技术变迁的例子，移动端开发最早分android和iOS分别开发，往往相同逻辑要不同团队开发两次，成本大且重复。后来出现h5 ，但h5性能不行。再后来fb推react native，在原生开发之上加了一层bridge，上层提供统一接口，下层分平台调用，这解决了h5的性能问题，但应用大了以后上层与原生层通信又是影响性能的瓶颈。后来谷歌推出了flutter 直接编译成不同平台运行代码，减少了中间通信过程，有点beam的意思。看来谷歌挺热衷于干这事</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（15） 💬（2）<div>感觉MapReduce、FlumeJava、Spark等这些框架的思想跟目前在ML领域大火的tensorflow类似。TensorFlow是把数据抽象成Tensor，有一系列对它的操作，conv、pooling等，dnn模型在框架内部的表示也是图的形式，计算图，节点表示计算，边表示tensor，通过在计算图上做调度和优化，转换成比较高效的计算图。再通过stream executor映射到具体的计算平台上，e.g. TPU，GPU等，操作会转换成库调用或者通过xla编译器转换成hlo IR，再经过一系列的优化，最终转换成具体硬件平台的指令。总之，这些框架背后的思想挺类似的</div>2019-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1o8gB5DOdHfAMQb91icmGDvTLhC4N9gusYGryBOxhtEeEDhWlzCkLib06hIeCejwuxBiaXpAZ17JVAtcVbmKfat5Q/132" width="30px"><span>morgan</span> 👍（4） 💬（1）<div>您好，beam和spark是什么关系呢？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/45/05a88185.jpg" width="30px"><span>住羽光</span> 👍（1） 💬（1）<div>请问老师，是如何了解这些大数据处理框架的历史呢？，老师自己，有什么查找资料的好方法吗？</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（1）<div>onnx走的路子和beam一致呀</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（5） 💬（4）<div>一直有个疑问，既然StructedStreaming已经实现了流批一致的API，为什么还要学Beam</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/96/4a7b7505.jpg" width="30px"><span>Eden2020</span> 👍（2） 💬（0）<div>经历过数据库技术变迁，关系数据库，面向分析的列式数据库，分布式文档数据库，时序数据库，图数据库等等</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/57/750c641d.jpg" width="30px"><span>linuxfans</span> 👍（2） 💬（2）<div>如蔡老师所说，任何新技术都要了解来龙去脉，尤其是如何解决当前问题的。但实际上操作起来，尤其在国内，我们是无法在网上找到线索或者文章分析新技术的动机和理念的，通常就是直接告诉你，我这个技术多好，可往往未必适合自己的场景，这个如何破？</div>2019-06-16</li><br/>
</ul>