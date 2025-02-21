今天是第一模块的最后一讲。在这一讲中，我们主要讲了软件的基础原理，今天，我将会针对这一模块中大家提出的普遍问题进行总结和答疑，让我们整理一下，再接着学习下一个模块的内容。

## 问题一

> @小美  
> 既然一个JVM是一个进程，JVM上跑Tomcat，Tomcat上可以部署多个应用。这样的话，每个跑在Tomcat上的应用是一个线程吗？该怎么理解“如果一个应用crash了，其他应用也会crash”？

理解程序运行时的执行环境，直观感受程序是如何运行的，对我们开发和维护软件很有意义。我们以小美同学提的这个场景为例，看下Java Web程序的运行时环境是什么样的，来重新梳理下进程、线程、应用、Web容器、Java虚拟机和操作系统之间的关系。

我们用Java开发Web应用，开发完成，编译打包以后得到的是一个war包，这个war包放入Tomcat的应用程序路径下，启动Tomcat就可以通过HTTP请求访问这个Web应用了。

在这个场景下，进程是哪个？线程有哪些？Web程序的war包是如何启动的？HTTP请求如何被处理？Tomcat在这里扮演的是什么角色？JVM又扮演什么角色？

首先，我们是通过执行Tomcat的Shell脚本启动Tomcat的，而在Shell脚本里，其实启动的是Java虚拟机，大概是这样一个Shell命令：
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/e8/52/931888d7.jpg" width="30px"><span>InvisibleDes</span> 👍（0） 💬（1）<div>这个大佬太牛了</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/f0/41590e10.jpg" width="30px"><span>Citizen Z</span> 👍（115） 💬（2）<div>成就一个人的，是事业所带来的社会效益。
衡量一个人成就的是他所带来贡献，而非多么华丽惊艳的技术实现。
能力是实现成就的条件，不是终极目标。
技术只是重要工具，应该精进，不必狂热。

做技术的其实挺容易迷失在无尽地追逐技术牛逼的道路上，诚然能带来快乐，却很容易造成思维封闭。想在事业上更上一层楼，要把眼光放在更大的局面上，小到帮助同事朋友，大到给公司战略提供建议、给开源社区贡献力量，虽然各方面能力暂时不一定能匹配得上，但是大的目标能让人豁然开朗，提高学习动力和做事动机。

个人经验，程序员应该敢于务虚、吹理论、玩圈子。不该将自己约束到一个码农的标签里，追求字面意义上的“talke cheap show code”，更不该用“我学技术就是为了挣钱”这种消极思想来对待职业发展，应该回归到“一个会计算机技术的职场人”的角色中。
归根结底，职业发展目标应该建立在事业的成功和价值的创造上，如此，能力、影响力、金钱会很自然地在过程中积累。

价值第一，效率第二，名利第三，目标向善，正向循环。</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（32） 💬（2）<div>程序员很容易有一种错觉，觉得这个世界是由技术推动的，其实不是，这个世界一直以来都是由资本推动的，技术只是资本的一种体现而已，工作中目的不应该是实现技术的最高难度，而应该是业务的最大价值呈现</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0a/e9/6fad9109.jpg" width="30px"><span>宁静志远</span> 👍（10） 💬（0）<div>最主要的是要去做一流的事，解决现实中大多人的痛点或问题</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/08/96/231fdd9e.jpg" width="30px"><span>未知</span> 👍（6） 💬（0）<div>“BAT 似乎成为当年的 IBM，历史好像进入了某种循环”
老师说的这句话感触很深。平时看公司比较核心的业务系统或者基础系统代码（新做的除外），代码一般都是很久以前的。这种现象应该都比较普遍，程序嘛，只要能满足目前的量并且没BUG，大家都没改重构的动力。但是如果从公司业务上来说，这种现象就比较危险：业务可以关系公司生死。大家都说乔布斯厉害，为什么厉害。感觉就是破、立。乔布斯二次回归时候，苹果已经从初创时候的高点落下来了，还差点卖身了。电脑不好卖加上金融危机，怎么办呢？但是他搞出了iPod。革了CD机的命，有搞出了Imac、iPhone。并且每个产品都标新立异。现在我们看，一个做电脑的公司做音乐播放器、做手机似乎正常。但是我们看看联想做手机、格力做手机、华为做手机。这些在发展初期都很困难，而且有的死了有的成功了。所以大公司转型或者插足新行业（那怕是同行业另一个领域），都比较谨慎，成不成完全未知，就像阿里云的初期一样。
一个产品能够做好，做大，流芳百世实属不易
</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/1e/378ed6bf.jpg" width="30px"><span>李子木</span> 👍（5） 💬（0）<div>老师讲的真的很好，从第一节一直看下来我觉得对我这种想在IT领域深入学习的初学者解答了很多疑问，期待后面的更新！</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/47/12/2c47bf36.jpg" width="30px"><span>Geek_2b3614</span> 👍（5） 💬（0）<div>真是有感而发呀。</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（0）<div>我觉的关于 Java Web 程序运行时环境的讲解是非常精彩的，可能是我读书少，之前一直没有搞明白。这部分内容相对偏底层，平时写代码的时候不一定用得上，但是了解之后，还是会有茅塞顿开的感觉。

至于互联网大厂的技术栈，最近在看淘宝技术发展之类的文章，也感觉有点奇怪，BAT 大厂的架构大多在几年前就已经发展成熟；然后近些年虽然人工智能、大数据、区块链之类的技术热点不断涌现，但是似乎也没有什么特别颠覆性的发展。

互联网大厂最终会像传统 IT 企业那样凋零么？

老师提出应该好好想想未来，我真的想不出来。只是感觉，如果可能的话，教育、医疗等垂直领域应该还有机会，面向企业的软件服务或者是互联网化似乎也有很多事情可做。编程从本质上来说，其实是帮助人们提高效率。</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7b/0a/b65e1fae.jpg" width="30px"><span>不要挑战自己的智商</span> 👍（1） 💬（0）<div>选择比努力重要</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（1） 💬（0）<div>目前技术给我的感觉是，很多都是在基于http协议上面进行开发。最近一直在想还有那些领域可以使用编程提高生产力。</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e8/52/931888d7.jpg" width="30px"><span>InvisibleDes</span> 👍（0） 💬（0）<div>把技术的过程，丝滑的，渐进的娓娓道来，太腻害了</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/7a/02fdf1a2.jpg" width="30px"><span>FreezeSoul</span> 👍（0） 💬（0）<div>我们通过技术的手段为自己也为世界做出一点点贡献</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/67/8922c991.jpg" width="30px"><span>Geek_5qjxgy</span> 👍（0） 💬（2）<div>智慧老师。按照文章说每一个请求Tomcat都会起一个新线程负责处理，那么如果该请求逻辑代码自行新建线程，是不是就是再创建一个线程了？是不是被一个请求都会新建一个新线程，那么代码里面就不需要自行新建一个新的线程？</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/b9/888fe350.jpg" width="30px"><span>不记年</span> 👍（0） 💬（0）<div>第五篇的答案原来是负载均衡啊</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/5d/69170b96.jpg" width="30px"><span>灰灰</span> 👍（0） 💬（0）<div>打卡</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ad/31193b83.jpg" width="30px"><span>孙志强</span> 👍（0） 💬（0）<div>单线程OOM,会触发一次Full GC,如果能够回收掉，应该不会导致整个JVM 挂掉，使用的收集器是G1</div>2019-12-17</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>tomcat进程的职责是监听80端口，分派线程处理请求，war包定义如何处理请求。

RAID5  假设有8块盘，校验那一部分写入是正常信息写入的7倍,所以要把校验信息分散到8块盘中，以使得每块盘寿命大致相等。每块盘有1&#47;8的存储信息是其他7块盘（每块非校验信息是7&#47;8）的校验，具体是把数据分块，每块盘轮流作为校验盘。</div>2019-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Gswh7ibY4tubXhp0BXOmV2pXZ3XsXic1d942ZMAEgWrRSF99bDskOTsG1g172ibORXxSCWTn9HWUX5vSSUVWU5I4A/132" width="30px"><span>奔奔奔跑</span> 👍（0） 💬（0）<div>哈哈，频繁写入的这个没考虑到，不过老师答疑hash表的问题我还是很有反思的，但是现在大部分公司要求高并发，用过这个redis，用过那个kafka，rocketmq，用过这个Api网关，用过那个etcd，为啥都这样呢</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/27/5556ae50.jpg" width="30px"><span>Demter</span> 👍（0） 💬（0）<div>希望多出点专栏</div>2019-12-04</li><br/>
</ul>