你好，我是秦粤。现在我们知道了在网络拓扑图中，只有Stateless节点才能自由扩缩容，而Stateful节点因为保存了重要数据，我们要谨慎对待，因此很难做扩缩容。

FaaS连接并访问传统数据库会增加额外的开销，我们可以采用数据编排的思想，将数据库操作转为RESTful API。顺着这个思路，我引出了后端应用的BaaS化，一句话总结，后端应用BaaS化就是将后端应用转换成NoOps的数据接口。那怎么理解这句话呢？后端应用BaaS化，究竟应该怎么做？接下来的几节课，我们会展开来讲。

我们先回忆一下上节课的“待办任务”Web应用，这个项目前端是单页应用，中间用了FaaS做SFF数据网关，后端数据接口还要BaaS化。这个案例会贯穿我们的课程，所以你一定要动手run一下。为了让你对我们的项目有个宏观上的认识，我还是先交付你一张大图。

![](https://static001.geekbang.org/resource/image/ba/c9/bab7e22b588d69cbe0197d36696411c9.jpg?wh=1670%2A820 "“待办任务”Web应用架构图")

这个架构的优势是什么呢？我们将这个图变个形，你就更容易理解了。

![](https://static001.geekbang.org/resource/image/66/8f/66aeb01686c94478b2847be5bb2a398f.jpg?wh=2462%2A828 "架构变形示意图")

咱从左往右看上面这张图。用户从浏览器打开我们网站时，前端应用响应返回index.html；然后浏览器去CDN下载我们的静态资源，完成页面静态资源的加载；与此同时，浏览器也向前端应用发起数据请求；前端应用经过安全签名后，再将数据请求发送给SFF；SFF再根据数据请求，调用后端接口或服务，最终将结果编排后返回。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（4） 💬（1）<div>请问数据库解耦时副本数据库允许数据写入吗？如果允许写入的话会不会因为写入的数据冲突导致数据不一致呢？</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（4） 💬（4）<div>老师好，在后台服务baas化的过程中，关于数据库跟以前微服务的方式有些不一样，微服务的各个节点是共享数据库的，但是baas化中，每个节点有自己的数据库，而且数据库的内容是一样的。这样是否带来2个问题：
1. 在数据量很大的情况下，每个节点都有一样的数据库，是否会使得数据存储量会翻几倍，成本会很高
2. 在扩容的情况下，如果数据量很大，新节点需要复制的数据也很多，启动时间会非常的长
3. 有多少个应用，就有多少个数据库实例。一般情况下，我们应用的数量会远高于数据库机器的数量。高并发场景下，会不会导致网络占用很高，性能整体上升
还是说这种方案本身就不适合大并发或者数据量很高的场景，谢谢了！</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（3）<div>哈哈，原来老师也觉得云厂商提供的kafka云服务贵。
我对这个深有体会！

我看领导买的一个阿里云kafka云服务，要4K+&#47;月，配置也就一般吧，可能监控做的比较好吧。
再想想我买的竞价付费实例，约64元&#47;月，4cpu8g配置，还不是突发性能的。当开发环境的k8s节点，也不怕丢数据，哈哈。

想一想，还是有钱真好。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/ae/0a5f7a56.jpg" width="30px"><span>此方彼方Francis</span> 👍（2） 💬（3）<div>微服务标准的做法是一个微服务实例独享一个数据库实例的。

这个说法有些夸张了吧？老师有生产上的实践案例吗？</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/4f/84ef0db0.jpg" width="30px"><span>liubin</span> 👍（0） 💬（1）<div>确实，有点扯了，每个应用副本一个db，谁来负责业务数据同步，不是kafka能解决的吧。而且事物也没法搞。这工作量比单db要大100倍</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/e4/81ee2d8f.jpg" width="30px"><span>Wisdom</span> 👍（0） 💬（1）<div>一个微服务，n个实例，一个实例对应一个数据库，这种方案，有点太浪费，而且数据的一致性方面还可能会有问题，不赞同这样，京乐、淘宝也没有这样搞，感觉这里有点误导</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/f9/ee/5294ebf4.jpg" width="30px"><span>youngwang1228</span> 👍（0） 💬（1）<div>我记得是微服务说的是： 每个服务有自己单独的数据库。
假如一个服务有5个实例，每个实例独享一个数据库的话，会不会有点奢侈。
例如，一个数据库的数据量是10G，那5个库就要50G，存储成本直线上升。
而且，新加实例的话，复制一个10G数据量的库实例，时间不短吧。</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/36/93/7dc76b32.jpg" width="30px"><span>PP-CIPDS-GRC</span> 👍（0） 💬（1）<div>BaaS 化只能基于 HTTP（RESTful）进行吗？可不可以基于 TCP，比如走 RPC 的方式？</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（1）<div>请问Rocketmq  10个9是怎么得出来的，是mttf  还是mttr  是一年周期么</div>2020-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ZkcKFzQ3qaIWpHjfOib9yU1LicthmiawfmkNhiakDdTUbTtCcworSZsxpiaib4sygOoc32duoUdQcI3Y1EmgcbicTzAyA/132" width="30px"><span>Geek_a5c054</span> 👍（0） 💬（3）<div>TypeError: Cannot read property &#39;0&#39; of undefined
    at Response.&lt;anonymous&gt; (&#47;home&#47;zyq&#47;Downloads&#47;todolist-backend-lesson08&#47;index.js:182:44)
这个是为什么呀</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/15/8db238ac.jpg" width="30px"><span>神仙朱</span> 👍（0） 💬（1）<div>疑问：通过额外进程让数据库与副本直接通过消息队列进行同步

为什么要让数据库产生一个副本，然后进行同步。这样不是两份相同的数据了吗，这样跟数据库瓶颈有什么关系，因为这样好像没有分担数据库的压力？只是copy 了一份？原数据库的数据多了，有了瓶颈，另一个副本因为数据一样，不也会产生瓶颈的吗</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/e3/2529c7dd.jpg" width="30px"><span>吴科🍀</span> 👍（0） 💬（1）<div>老师，关于用mq实现数据库同步的问题，如果要求数据强一直都业务场景很难实现啊，比如秒杀，通过mq同步不及时，用户会查到不同的库存，造成多卖的情况呢</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>感觉现在的学习门槛越来越高了.😁

0.要有自己的域名,最好还是备案过的.
1.需要会排查依赖包缺失的问题.
2.需要会开通简单的云服务.
3.需要会配置访问秘钥及授权.
4.还要会配置函数计算的日志,还需要会看.

-----------------
有个疑问咨询下老师:
如何用一套代码中的不同入口文件部署多个函数计算服务?

我现在是把代码仓库整个拷贝了一份,
一个是`cp index-faas.js index.js`,
另一个`cp rule-faas.js index.js`.
然后再微调下`template.yml`.

由于默认的运行时环境指定了入口文件`index.js`,我只能用这个笨办法.
不知道目前有没有什么简洁的方式.
[我目前只会使用fun命令行部署服务]
</div>2020-04-27</li><br/>
</ul>