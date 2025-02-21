上期文章我们介绍了混合云，以及在实际操作中我们常见的几种混合云模式。今天我们来聊一聊Spring Cloud如何解决应用层的云架构问题。

对于Spring Cloud，你大概不会陌生，它跟Spring生态中的另一个开源项目Spring Boot，基本上已经成为国内绝大多数公司向微服务架构转型时的首选开发框架。

Spring Boot可以支持快速开发单个微服务应用，Spring Cloud则提供一系列的服务治理框架，比如服务注册、服务发现、动态路由、负载均衡以及熔断等等能力，可以将一个个独立的微服务作为一个整体，进行很好的管理和维护。

从业界实际使用情况和反馈来看，由于两者完美的搭配，Spring Cloud和Spring Boot确实是可以通过相对较低的技术成本，让开发人员方便快速地搭建起一套分布式应用系统，从而进行高效的业务开发。

同时，优秀的服务治理能力，也为其后续在稳定性保障工作方面打下了不错的基础。

（注：因为Spring Cloud必须基于Spring Boot框架才能发挥它的治理能力，所以下面我们提到的Spring Cloud是默认包含了Spring Boot框架的。）

所以，通常我们更多地是把Spring Cloud作为微服务应用层面的开发框架，帮助我们提升开发效率。看起来，它貌似跟“云”这个概念没有什么直接关系。

而实际上，在将应用与云平台连接方面，Spring Cloud也发挥着非常核心的作用。这也是为什么本期文章的标题没有直接定义为微服务治理架构，而是面向应用层的云架构。

下面我们具体来看看。

## Spring Cloud框架中云的影子

目前整个Spring生态是由Pivotal这家商业公司在主导，但是Pivotal更大的目标是要为客户提供云上的端到端的解决方案。

所以Pivotal最早提出了Cloud-Native（云原生）的概念，或者说是一种理念，**目的是帮企业提供云上业务端到端的技术解决方案，全面提升软件交付效率，降低运维成本。**简单来说，就是除了业务解决方案和代码，其它事情都可以交给平台处理。

基于这样的理念，Pivotal打造了自己的云原生解决方案PCF（Pivotal Cloud Foundry），包括多云和跨云平台的管理、监控、发布，以及基础的DB、缓存和消息队列等等，一应俱全。

我们可以看到，在PCF整体解决方案中，Spring生态是向用户的业务应用层架构拓展的非常重要的一环，帮助其进行高效的业务开发，并提供后续的稳定性保障。  
￼  
![](https://static001.geekbang.org/resource/image/88/17/880d3bf4d381126a0795b06de279de17.jpg?wh=1107%2A556)

所以，这个时候，**Spring Cloud除了提供微服务治理能力之外，还成为了微服务应用与云平台上各项基础设施和基础服务之间的纽带，并在其中起到了承上启下的关键作用。**
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（2） 💬（1）<div>上云不可避免了</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/21/34c72e67.jpg" width="30px"><span>cyz</span> 👍（1） 💬（1）<div>The teacher is a light to guide us.我们应该成为技术架构的管理者。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（0） 💬（1）<div>首选 spring boot.
Spring cloud 很多组件还没在公司广泛应用。 有很多组件还在快速发展中</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/1d/1b1f0a1f.jpg" width="30px"><span>刘圣威</span> 👍（0） 💬（2）<div>非常认同您的假设，甚至以后都可以是ai写代码</div>2018-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/7e/6639cdd4.jpg" width="30px"><span>casper2dd</span> 👍（0） 💬（1）<div>“那么运维应该成为技术架构的管理者，从效率、成本、稳定性这几个方面来检验架构是否合理” 这句话能具体举个例子么 因为感觉成熟的解决方案 对运维关心的 成本 效率 稳定性都包括了 比如弹性扩容 故障定位 感觉以后能做的越来越少了</div>2018-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（0） 💬（0）<div>当初离职找工作时怎么没想到这里有这样的文章呢 吗的 后悔莫及，真是什么都讲到了 就看你能不能理解。
另外，CNCF 的核心项目除了 K8S 外，还有 Goggle 的 gRPC，Docker 的 ContainerD，这段话应是google吧 打错了</div>2023-01-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmoUFrDUO3CKia9QzAPBEgnOX5QWumr2Ez997GmrEup38jdicm2w7FulL3d9chGYwGNUAP7e3xKOEw/132" width="30px"><span>郭小青</span> 👍（0） 💬（0）<div>很有触感的一篇。在较早之前我和同学讨论过，以后中小型企业不再有网络工程师，因为他们的基础设施在云上，也只会存在优秀的网络工程师，并在云计算类企业中发展。因为云上依然有服务器的原因，我们并未讨论到运维(系统，业务)的会消失的可能性。今天读完这篇，才发现在未来云计算公司提供了运维所能提供的一切解决方案，那么非技术性公司就真的只剩下代码实现业务了，而那时的运维职责就如同文中所说 利用云平台各项能力实现业务，发力点在架构的成本，效率，稳定性上，而不是研究某项基础设施的技术了。这里我们不妨再大胆设想一下，在未来如果业务是有代码模块(由云计算公司提供)组合拼凑起来的，是否程序员也将减少呢！或许到那时程序员也不再叫程序员了！(这是最近看到的一篇公众号的文章，结合赵老师的这篇文章引发的感想)
这有什么现实意义呢？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/99/4f5857a8.jpg" width="30px"><span>竹影</span> 👍（0） 💬（0）<div>这一讲的核心是什么？介绍Spring和cncf？</div>2021-07-02</li><br/>
</ul>