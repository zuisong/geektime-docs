你好，我是姚秋辰。

在上节课中，我提到过一个叫Transaction Coordinator的组件，它在分布式事务中扮演了一个协调者的角色，用来保证事务的最终一致性。这个昨日配角摇身一变就成了今天的主角，还有了一个新的名字：Seata Server。这节课我就带你了解Seata Server的交互模型，再手把手带你搭建一个Seata Server。

但凡名字里带个Server的组件，不用想就知道这一定又是一个“中间件”，Seata Server就是这么一个中心化的、单独部署的事务管理中间件。在开始搭建Seata Server之前，我们先来了解一下Seata Server在整个分布式事务方案中是如何跟各个应用交互的吧。

![图片](https://static001.geekbang.org/resource/image/de/45/de3cf5f08e1a169060b9be59c3f36045.jpg?wh=1920x683)

在上面的图里，除了微服务和Seata以外，还多了Nacos和MySQL的影子，它俩来凑什么数呢？

在分布式事务的执行过程中，各个微服务都要向Seata汇报自己的分支事务状态，亦或是接收来自Seata的Commit/Rollback决议，这些微服务是如何勾搭上Seata Server的呢？答案就是**服务发现**。Seata Server把自己作为了一个微服务注册到了Nacos，各个微服务利用Nacos的服务发现能力获取到Seata Server的地址。如此一来，微服务到Seata Server的通信链路就构建起来了。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：微服务端的undo_log表，其字段是固定的还是任意的？
Q2：微服务端的undo_log表，业务代码需要对其操作吗？或者是seat在微服务端有一个客户端，由此客户端代码对其进行操作？
Q3：能否加餐讲一下持续集成？
Q4：微服务部署问题
一个网站，微服务会有很多，比如二十个，SpringCloud的组件也很多，需要用到的也差不多有十个左右。这样就有三十个实体，每一个都要有备份的话，就需要30*2=60台机器。六十台机器，对于大公司不算什么，对于创业公司，成本会很高啊。这个问题有什么解决办法吗？一个微服务实例要占用一台物理机吗？</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/6d/a4ff33bb.jpg" width="30px"><span>Lee</span> 👍（0） 💬（1）<div>对于互联网来说，高并发情况下，更多是AP吧；金融或者互联网部分场景会用分布式事务、事务消息或者补偿等，但是也会给性能带来一定的问题</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/e7/495068f6.jpg" width="30px"><span>文艺码农</span> 👍（0） 💬（1）<div>老师好.我碰到了一个问题,file文件里面配置 url = &quot;jdbc:mysql:&#47;&#47;127.0.0.1:3306&#47;seata?rewriteBatchedStatements=true&quot; 会报错说serverTimezone啥啥啥的.然后我配置成这样就ok了:
 url = &quot;jdbc:mysql:&#47;&#47;127.0.0.1:3306&#47;seata?rewriteBatchedStatements=true&amp;serverTimezone=Hongkong&quot;</div>2022-04-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/3icaaUibVCz5gYiaj5gZ4wV8ick5RhEMpe47XKkdK1nAhA9qic6rwhSrpiasDSQYAwfiaIulhE4YKsbwoOXUfvL76EPSw/132" width="30px"><span>Geek_f76b23</span> 👍（0） 💬（1）<div>夺命连环催，大仙速更</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4f/1f/791d0f5e.jpg" width="30px"><span>Geek_159e2d</span> 👍（0） 💬（1）<div>在 Seata 2.0.0 版本中，运行时，只需删掉 lib\jdbc 与配置文件中指定数据库版本不对应的驱动即可</div>2024-07-25</li><br/>
</ul>