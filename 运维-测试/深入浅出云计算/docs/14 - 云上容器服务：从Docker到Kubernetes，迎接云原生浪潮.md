你好，我是何恺铎。

容器，毫无疑问是近年来的又一个技术热词。容器化技术的诞生和兴起，以及它所催生的微服务架构、DevOps、云原生等技术理念，都对软件行业产生了深远的影响。

容器的优点有很多了，完善的封装、便捷的部署、轻量的启动和调度，这些都是容器技术受到欢迎的原因。与编排系统配合后，它能让我们的应用程序容易管理和迭代，即便是再复杂的系统也不在话下。同时呢，容器应用还能做到非常好的可迁移性，环境中只要有符合标准的容器运行时就可以顺利运行。

我相信你对容器其实有一定的了解，也知道Docker和Kubernetes分别是容器技术和容器编排的事实标准。甚至，不少同学已经有过一些实践的经验。

那么在容器这一讲中，我们主要关心什么问题呢？我认为，你需要重点搞清楚两个问题：

- **容器和云是什么关系呢？**
- **在云上运行容器有哪些方式，它们各自又有什么特点呢？**

让我们顺着容器上云的发展历程，来了解这两个问题的答案。

## 容器上云：从Docker到Kubernetes

轻量的容器和富有弹性的云计算，互相之间其实是非常契合的。容器对于运行环境的极强适应性和快速启动的能力，配合云上动态扩展的庞大资源规模，让云端的容器应用可以在短时间内拓展到成千上万个实例。所以，**云可以说是容器应用的最佳载体，容器应用也非常适合在云上运行和扩展。**
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/35/28758547.jpg" width="30px"><span>何恺铎</span> 👍（24） 💬（0）<div>[上讲问题参考回答]
1. 在Hadoop的黄金时代，就近访问是诞生在当时网络传输速度远远低于本地硬盘IO的大背景下的，所以它的作用非常大。随着数据中心高速网络技术的发展，网络传输得以不断接近本地IO，反而是算力容易成为瓶颈，所以使用对象存储时计算存储分离等优势就凸显出来了。
2. Hive是基于Hadoop生态的数据仓库，早期使用MapReduce作为计算实现引擎，更侧重大数据量的支持，查询实时性不佳。后来虽然使用Tez&#47;Spark等引擎进行了很多性能优化，但仍然和MPP类分析型数据库存在查询执行架构和效能方面的区别。所以相对来说，分析型数据库擅长即席查询，而Hive更适合离线计算。</div>2020-04-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（4） 💬（1）<div>请问云原生是怎么定义的，k8s就是云原生吗？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（8） 💬（0）<div>关于第一个问题我记得在张磊的课程中看到过，生产没用容器故而也就没钻了。
第二个问题我倒是看到过相关报道：尤其是Google在开发K8第二代时提及过其中引入一些ACID中的元素去解决一些问题；个人觉得更加偏向是云厂商中的一种服务形式。这就像现在几乎一提及设计就是分布式，可是我记得不少老师在其架构课中都有提及“分久必合，合久必分”；容器化的根本还是要一体机啊，Docker的产生并没有真正的代替VMware，一种个性化需求。
       早期我们觉得有了windows就足够了，现在有了Linux也挺好。各自都还安好了几十年了，没有见到谁彻底消灭谁；其实我们更需要思考的是分布式的下一种方式是什么？这个更加值得思考。</div>2020-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（3） 💬（1）<div>第一个问题，可不可以简化为一个k8s集群的POD能够调度到另一个k8s集群上，然后这个POD还归属与前者集群？如果是这样的话就不晓得了～

第二个问题，随着k8s的越来越成熟，以后所有的PAAS都能跑在k8s上，就像现在都是跑在操作系统上一样，我对云原生吞噬一切持有乐观态度，但是k8s还有很多问题要解决，比如现在还不支持强多租户。

还有几个问题，请教老师。
- 为什么云端的多租户特性，就能免去Master节点的开销的，这是说master节点是随便用的么，master节点消耗的资源不用自己买单是用的云厂商的资源么？
- 一个云厂商的容器实例服务是跑在一个大的k8s集群中么，容器实例服务之间的互相调用只能通过创建时候返回的域名么？
</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（0） 💬（0）<div>我觉得公有云应该也有通过CRD, Operator等方式集成自身容器服务到自身k8s服务中的例子吧。
有一些公有云资源对象在原版k8s型中就通过Cloud Provider以及Cloud Driver等形式集成了，说白了就是注册一个自定义资源，再写个自定义控制器来扩展API嘛。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/3f/a553d117.jpg" width="30px"><span>Michael Yang</span> 👍（0） 💬（0）<div>K8S只会是云服务的一种！</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/69/d5a28079.jpg" width="30px"><span>Bora.Don</span> 👍（0） 💬（0）<div>所以这就是serverless的实现方式？</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/ed/45ab9f03.jpg" width="30px"><span>八哥</span> 👍（0） 💬（0）<div>大多数云计算公司容器镜像服务是拿开源得Habor改的。感觉未来serverless服务可能是未来主流模式，期待。</div>2020-04-03</li><br/>
</ul>