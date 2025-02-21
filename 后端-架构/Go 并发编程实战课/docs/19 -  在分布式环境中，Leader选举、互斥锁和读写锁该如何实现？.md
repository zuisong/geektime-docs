你好，我是鸟窝。

在前面的课程里，我们学习的并发原语都是在进程内使用的，也就是我们常见的一个运行程序为了控制共享资源、实现任务编排和进行消息传递而提供的控制类型。在接下来的这两节课里，我要讲的是几个分布式的并发原语，它们控制的资源或编排的任务分布在不同进程、不同机器上。

分布式的并发原语实现更加复杂，因为在分布式环境中，网络状况、服务状态都是不可控的。不过还好有相应的软件系统去做这些事情。这些软件系统会专门去处理这些节点之间的协调和异常情况，并且保证数据的一致性。我们要做的就是在它们的基础上实现我们的业务。

常用来做协调工作的软件系统是Zookeeper、etcd、Consul之类的软件，Zookeeper为Java生态群提供了丰富的分布式并发原语（通过Curator库），但是缺少Go相关的并发原语库。Consul在提供分布式并发原语这件事儿上不是很积极，而etcd就提供了非常好的分布式并发原语，比如分布式互斥锁、分布式读写锁、Leader选举，等等。所以，今天，我就以etcd为基础，给你介绍几种分布式并发原语。

既然我们依赖etcd，那么，在生产环境中要有一个etcd集群，而且应该保证这个etcd集群是7\*24工作的。在学习过程中，你可以使用一个etcd节点进行测试。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/46/75/d35c7623.jpg" width="30px"><span>鸟窝</span> 👍（9） 💬（1）<div>这一讲和下一讲的代码在 https:&#47;&#47;github.com&#47;smallnest&#47;distributed</div>2020-11-25</li><br/><li><img src="" width="30px"><span>K菌无惨</span> 👍（1） 💬（1）<div>老师, Locker是超时解锁是通过NewSession时添加WithTTL这个SessionOption来设置的吗</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/bb/4fb42628.jpg" width="30px"><span>gone with the wind</span> 👍（0） 💬（1）<div>        module declares its path as: go.etcd.io&#47;bbolt
                but was required as: github.com&#47;coreos&#47;bbolt
例子现在运行不起来了</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（0） 💬（1）<div>老师，问一下您这边有用过 redis 相关的分布式的并发原语库吗</div>2021-08-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（1）<div>关于leader选举，几个问题：
1. 如何获取从节点的信息？？
2. leader选举成功后， resign是只有主节点可以发起吗，还是从节点也可以发起resign</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/5f/6bf8b74a.jpg" width="30px"><span>Kepler</span> 👍（8） 💬（0）<div>类似zookeeper 的分布式锁原理，节点宕机对应session 销毁，持有的锁会被释放</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（0）<div>关于思考题，
如果持有互斥锁或者读写锁的节点意外宕机了，从调用接口来看，与当前节点启动的session有关系，节点宕机之后，感觉应该有与该session相关的处理，比如超时机制，所以它持有的锁会被释放。
etcd 提供的读写锁，按照rwmutex的实现写锁应该比读锁优先级高，但是在分布式环境下，如此实现的话，我想会增加复杂度和出问题的几率。

</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/b2/2e9f442d.jpg" width="30px"><span>文武木子</span> 👍（0） 💬（0）<div>Redis实现分布式锁大家用的多吗</div>2022-03-20</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（0） 💬（0）<div>还没来得及去看etcd库的代码，盲猜一下。
第一个问题，我觉得要看场景，如果被锁住的资源可以被重新分配，我相信etcd能检测到持有锁的节点断开，concurrent包里应该有相关的实现把锁释放。但是，如果被锁住的资源非常重要，影响到整个系统的状态，必须要人工介入才能把破损的数据修复，那这个时候自动释放锁反而可能完成更大规模的损失。
第二个问题，还是得去看代码再说</div>2020-11-23</li><br/>
</ul>