你好，我是姚秋辰。

上一节课，我向你介绍了微服务架构的特点和优势。今天我就来带你了解 Spring Cloud 框架，看一看被称为微服务全家桶的 Spring Cloud 提供了哪些强大的工具。

通过今天的学习，你将会了解 Spring Cloud 框架的功能定位，以及它和 Spring Boot 之间的关系。除此之外，我还会详细讲解 Spring Cloud 的发展历史，并介绍 Netflix 和 Alibaba 两大核心组件库，以及 Spring Cloud 的版本更新策略。这样一来，你就对 Spring Cloud 框架有了一个全面的认识。

那我首先来带你了解一下什么是 Spring Cloud。

## 大话Spring Cloud

Spring Cloud可谓出身名门，它由Spring开源社区主导孵化的，专门为了解决微服务架构难题而诞生的一款微“微服务全家桶”框架。难能可贵的是，Spring Cloud走了一条博采众家之长的道路，除了Spring开源社区的研发力量以外，它还吸纳了很多业界一线互联网大厂的开源组件为己用，将这些经过大厂真实业务锤炼的组件孵化成为了Spring Cloud组件的一部分。

我们通过Spring社区发布的一张简化的架构图来看一下Spring Cloud的技能加点。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/5d/6a/83f7eb7f.jpg" width="30px"><span>PueC</span> 👍（19） 💬（1）<div>课程不涉及总线？</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（11） 💬（1）<div>第二排看戏，不拿生产小白鼠！</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/71/0d/4dc04ac8.jpg" width="30px"><span>Q</span> 👍（6） 💬（2）<div>我们公司用的就是eureka老的那一套，主业务的微服务代码堆砌已经相当臃肿了</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dd/00/4a7b9a9f.jpg" width="30px"><span>Nico</span> 👍（6） 💬（2）<div>一直还在用Greenwich版本，对于Gateway，做压测发现网关还是会对性能有一定的影响，不知道新版本的会不会好一些</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（5） 💬（1）<div>Spring Cloud 是一个组件库的集合，为什么 Spring Cloud 还有版本号的迭代呢？ 还是说 Spring Cloud 本身就是只有规范，组件库只是实现这些规范？</div>2022-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/b8/a7/e2bae013.jpg" width="30px"><span>Dobbykim</span> 👍（5） 💬（1）<div>老师你好，项目地址在哪里呀</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/33/c8019dc7.jpg" width="30px"><span>无崖子Z</span> 👍（4） 💬（1）<div>首先会考虑框架是否成熟，是否有组织或社区的支持，与公司现有的中间件的整合度。如果有很大的问题，对于线上项目是灾难性的。
其次会考虑提供的技术组件对业务功能的支持，或是扩展支持。
再次会考虑普及度，是否容易上手，团队人员的技术熟悉成度。
这三点不一定是绝对的优先级，要根据实际情况进行trade-off
</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（2） 💬（1）<div>spring cloud 的版本(Angel, Brixtion,..., Jubilee) 跟 Netflix 组件库和 Alibaba 组件库 是什么关系呢？</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（2） 💬（1）<div>会有具体的项目吗？</div>2021-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1gQDTkOQGHXCKA9ibickU65GDVxSdB6ptiaDy3uqDU61NbEslm3SOoFVVZcT19QS9svNBtdLzkT4FZpdvic32mzcXQ/132" width="30px"><span>Geek_7b7a93</span> 👍（1） 💬（1）<div>老师，可以通俗易懂的解释一下中台，总是感觉对中台的感念有点模糊</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/2c/180075e0.jpg" width="30px"><span>小豪</span> 👍（1） 💬（1）<div>spring cloud组件必须依赖spring boot才能使用吗
</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（1） 💬（1）<div>课程学完的话，能做到自己随意切换组件吗，例如把网关切换成shenyu？</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（1） 💬（1）<div>有项目源码吗</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/9e/0b/e4d80306.jpg" width="30px"><span>Magic</span> 👍（1） 💬（1）<div>当你考虑给自己的项目做底层技术框架升版的时候，你会基于哪些因素做出“升级版本”的决定：
1、旧版本存在的问题修复
2、新版本的新特性是否适用于项目
3、性能优化</div>2021-12-31</li><br/><li><img src="" width="30px"><span>Geek_ac4e9c</span> 👍（1） 💬（1）<div>1.讲解springboot和SpringCloud的关系；Springboot是基石，springCloud基于springboot实现微服务功能。
2.springcloud发展历史
3.springcloud版本依赖
</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/f5/5c/63197d07.jpg" width="30px"><span>Java田宝宝</span> 👍（0） 💬（1）<div>从十项全能追到微服务实战，姚老师的课程一直非常好，讲解通俗易懂，深入细致，这个课要是加上Swagger相关的实践和原理分析就好了，有点美中不足，however，已被姚老师实力圈粉👍</div>2024-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/27/19/8cc840cf.jpg" width="30px"><span>叶飘零</span> 👍（0） 💬（1）<div>Spring Boot是家庭主妇，家庭稳定基石；Spring Cloud拼搏奋斗的汉子，统领三军...😂</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/79/22/a41433e6.jpg" width="30px"><span>2022加油</span> 👍（0） 💬（1）<div>讲的很棒</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c8/715ce68f.jpg" width="30px"><span>201</span> 👍（5） 💬（0）<div>哈哈，升级策略不变。公司开发主用用g版本。自己电脑都是2020的版本。以前升级弄了几次测试事故再也不敢随便上了。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（1） 💬（0）<div>更新框架带来的好处（性能优势、Bug修复、使用体验）要大于成本​（故障风险）</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（1） 💬（0）<div>1.根据新版本的新特性；
2.针对旧版本的问题修复；
3.根据技术发展趋势。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d8/5d/07dfb3b5.jpg" width="30px"><span>杯莫停</span> 👍（0） 💬（0）<div>公司开发语言众多 没有使用Spring cloud 但是来学习一下。</div>2023-07-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4VCgcBbU51SiasW8tpjYwdqBGe2RNIy6neuI7AEjCQ6t9qqXw6tXpZ2bDCoxJhWqQJv2LlFmemVYJCrLze2Aa7g/132" width="30px"><span>beatdrug</span> 👍（0） 💬（0）<div>1、框架是否有bug需要升级来修复
2、框架新旧兼容性
3、框架新版本特性对系统的帮助</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（0） 💬（0）<div>Release 版 是稳定版，生产就用这个</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9f/e2/8fc12ce1.jpg" width="30px"><span>㏒</span> 👍（0） 💬（0）<div>期待下一次更新</div>2021-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ULSZxjHNT5ZMormTYmqSZvoCbKd0q6oN8V78QaLdzqkqs1AXMShysNczsOOVJrblE4dxhBuibDvkgIlzVAw2qeQ/132" width="30px"><span>Geek_e306aa</span> 👍（0） 💬（0）<div>坐等新的课程😍😍😍</div>2021-12-16</li><br/>
</ul>