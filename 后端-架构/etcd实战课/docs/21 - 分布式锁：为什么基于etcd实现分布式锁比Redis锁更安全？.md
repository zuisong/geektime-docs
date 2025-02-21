你好，我是唐聪。

在软件开发过程中，我们经常会遇到各种场景要求对共享资源进行互斥操作，否则整个系统的数据一致性就会出现问题。典型场景如商品库存操作、Kubernertes调度器为Pod分配运行的Node。

那要如何实现对共享资源进行互斥操作呢？

锁就是其中一个非常通用的解决方案。在单节点多线程环境，你使用本地的互斥锁就可以完成资源的互斥操作。然而单节点存在单点故障，为了保证服务高可用，你需要多节点部署。在多节点部署的分布式架构中，你就需要使用分布式锁来解决资源互斥操作了。

但是为什么有的业务使用了分布式锁还会出现各种严重超卖事故呢？分布式锁的实现和使用过程需要注意什么？

今天，我就和你聊聊分布式锁背后的故事，我将通过一个茅台超卖的案例，为你介绍基于Redis实现的分布锁优缺点，引出分布式锁的核心要素，对比分布式锁的几种业界典型实现方案，深入剖析etcd分布式锁的实现。

希望通过这节课，让你了解etcd分布式锁的应用场景、核心原理，在业务开发过程中，优雅、合理的使用分布式锁去解决各类资源互斥、并发操作问题。

## 从茅台超卖案例看分布式锁要素

首先我们从去年一个因Redis分布式锁实现问题导致[茅台超卖案例](https://juejin.cn/post/6854573212831842311)说起，在这个网友分享的真实案例中，因茅台的稀缺性，事件最终定级为P0级生产事故，后果影响严重。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（23） 💬（1）<div>老师太厉害了👍etcd和redis 分析的太太透彻了！终于明白了etcd和redis 锁的区别了…….专栏快接近尾声了……真有点不舍！</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（8） 💬（1）<div>老师文中提到的思考题，多个client抢同一把锁与多个client各自抢自己的锁。我的想法是多个client抢同一把锁，在client数目多的时候，同一把锁的竞争比较激烈。而多个client各自抢各自的锁，会有锁饥饿问题，比如新的client因其version比较小，更容易获得锁。

</div>2021-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（5） 💬（1）<div>你要注意的是，实现分布式锁的方案有多种，比如你可以通过 client 是否成功创建一个固定的 key，来判断此 client 是否获得锁，你也可以通过多个 client 创建 prefix 相同，名称不一样的 key，哪个 key 的 revision 最小，最终就是它获得锁。至于谁优谁劣，我作为思考题的一部分，留给大家一起讨论。
1. 按照文中介绍concurrency包中用的是prefix
2. 如果使用相同的key，我能够想到存在的问题,在释放锁后，会导致获取锁的事务同时发生，事务数量变得很大
</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/30/85/14c2f16c.jpg" width="30px"><span>石小</span> 👍（4） 💬（2）<div>唐老师好，etcd有像innodb那样能能控制持久化程度的配置(主要指多久fsync一次磁盘)吗？或者说，etcd可能出现持久化失败(写入磁盘缓存，没fsync)吗？如果持久化失败会有哪些影响？</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（0） 💬（1）<div>我最近在做的工作中遇到了分布式锁，这篇文章解决了工作中的很多疑惑，忍不住想要分享给同事们，逻辑合理，切中要害，写的太赞了。</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/45/16c60da2.jpg" width="30px"><span>蔫巴的小白菜</span> 👍（0） 💬（1）<div>我理解多个客户端写一个key，与多个客户端写多个key，可以理解为非公平锁与公平锁。主要还是要看业务场景处理。</div>2021-04-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib3Rzem884S5MOS96THy0gQXcF26PNsnRBpyr3pM5rVibZdYvAibpVvAGfibF1ddpgrteg9fQUsq4vce9EM95Jj97Q/132" width="30px"><span>Geek_604077</span> 👍（20） 💬（0）<div>死锁、脑裂、惊群效应是分布式锁的核心问题，你知道它们各自是怎么一回事吗？ZooKeeper 和 etcd 是如何应对这些问题的呢？
死锁：加锁后由于没有添加锁的过期时间或者锁的时间设置过长，服务异常crash或者服务执行后漏执行释放锁操作，导致锁长时间没有释放

脑裂：分布式体系结构中的集中式结构（也称为 Master&#47;Slave 架构），一个Master节点多个Slave节点，所有的请求数据处理必须先经过Master中央服务器，由Master统一进行资源和任务调度，中央服务器根据这些信息，将任务下达给节点服务器，节点服务器执行任务，并将结果反馈给中央服务器。脑裂是在某些特殊条件下，如主备切换，Slave在与Master的网络出现故障的时候，Slave会认为Master已经故障，从而成为新的master，而原来的master也没有卸任，从而导致存在两个Master在对外服务，存在多master会导致共享资源的互斥性遭到破坏，出现资源争抢，数据不一致等问题

惊群效应：指多进程（多线程）在同时阻塞等待同一个事件的时候（休眠状态），如果等待的这个事件发生，那么他就会唤醒等待的所有进程（或者线程），但是最终却只能有一个进程（线程）获得这个时间的“控制权”，对该事件进行处理，而其他进程（线程）获取“控制权”失败，只能重新进入休眠状态，这种现象和性能浪费就叫做惊群效应。（当你往一群鸽子中间扔一块食物，虽然最终只有一个鸽子抢到食物，但所有鸽子都会被惊动来争夺，没有抢到食物的鸽子只好回去继续睡觉， 等待下一块食物到来。这样，每扔一块食物，都会惊动所有的鸽子，即为惊群。）

etcd如何避免死锁：利用Lease的活性检测机制，它提供了检测各个客户端存活的能力。你的业务 client 需定期向 etcd 服务发送&quot;特殊心跳&quot;汇报健康状态，若你未正常发送心跳，并超过和 etcd 服务约定的最大存活时间后，就会被 etcd 服务移除此 Lease 和其关联的数据。通过 Lease 机制就优雅地解决了 client 出现 crash 故障、client 与 etcd 集群网络出现隔离等各类故障场景下的死锁问题。一旦超过 Lease TTL，它就能自动被释放，确保了其他 client 在 TTL 过期后能正常申请锁，保障了业务的可用性。

etcd如何避免集群脑裂：在leader选举上采用了过半机制，即得到一半以上的follow才能成为leader，且新leader就任后旧leader必须卸任，所以etcd不存在脑裂问题

etcd如何避免惊群效应：mutex，通过 Watch 机制各自监听 prefix 相同，revision 比自己小的 key，因为只有 revision 比自己小的 key 释放锁，才能有机会，获得锁</div>2022-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib3Rzem884S5MOS96THy0gQXcF26PNsnRBpyr3pM5rVibZdYvAibpVvAGfibF1ddpgrteg9fQUsq4vce9EM95Jj97Q/132" width="30px"><span>Geek_604077</span> 👍（2） 💬（0）<div>若你锁设置的 10 秒，如果你的某业务进程抢锁成功后，执行可能会超过 10 秒才成功，在这过程中如何避免锁被自动释放而出现的安全性问题呢?
加锁时，先设置一个过期时间，然后我们开启一个「守护线程」，定时去检测这个锁的失效时间，如果锁快要过期了，操作共享资源还未完成，那么就自动对锁进行「续期」，重新设置过期时间。

幸运的是，已经有一个库把这些工作都封装好了：Redisson。

Redisson 是一个 Java 语言实现的 Redis SDK 客户端，在使用分布式锁时，它就采用了「自动续期」的方案来避免锁过期，这个守护线程我们一般也把它叫做「看门狗」线程。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/dc/b0/5b652423.jpg" width="30px"><span>Yang</span> 👍（2） 💬（0）<div>etcd实现的分布式所能保证高性能不</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/54/0aafbf5e.jpg" width="30px"><span>雄哼哼</span> 👍（0） 💬（0）<div>redis主备切换过程中，备的数据还没追上的时候 应该是禁止写入的，所以redis的set nx是写不进去的</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/36/fb/b480f2ac.jpg" width="30px"><span>人间理想</span> 👍（0） 💬（0）<div>讲的真的好，深入浅出</div>2023-03-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep0Cb1HGLBTD57I53ZLsIBnvN3YkJOTkibWyibPoCUM5cbnhqDicm1aKWTUFeI7SEd8REnibfZVWeM3BQ/132" width="30px"><span>Mr.zhou</span> 👍（0） 💬（0）<div>我自己使用etcd实现的一个小分布式锁的小栗子，不知道这么实现对不对
package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;github.com&#47;coreos&#47;etcd&#47;clientv3&quot;
	&quot;github.com&#47;coreos&#47;etcd&#47;clientv3&#47;concurrency&quot;
	&quot;sync&quot;
)

func main() {
	cli, _ := clientv3.New(clientv3.Config{
		Endpoints: []string{&quot;192.168.2.45:2379&quot;, &quot;192.168.2.46:2379&quot;, &quot;192.168.2.47:2379&quot;},
	})
	defer cli.Close()
	session, _ := concurrency.NewSession(cli)
	defer session.Close()
	mutex := concurrency.NewMutex(session, &quot;&#47;mylock&#47;&quot;)

	wg := sync.WaitGroup{}
	wg.Add(2)
	sum := 0
	go func() {
		defer wg.Done()
		for i := 0; i &lt; 100; i++ {
			fmt.Println(&quot;1号协程拿到了锁&quot;)
			mutex.Lock(context.Background())
			sum = sum + 1
			fmt.Println(&quot;1号协程中sum是 &quot;, sum)
			mutex.Unlock(context.Background())
			fmt.Println(&quot;1号协程释放了锁&quot;)
		}

	}()
	go func() {
		defer wg.Done()
		for i := 0; i &lt; 100; i++ {
			mutex.Lock(context.Background())
			fmt.Println(&quot;2号协程拿到了锁&quot;)
			sum = sum - 1
			fmt.Println(&quot;2号协程中sum是 &quot;, sum)
			mutex.Unlock(context.Background())
			fmt.Println(&quot;2号协程释放了锁&quot;)
		}
	}()
	
	wg.Wait()
	fmt.Println(sum)
}
</div>2023-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/31/3820fbb7.jpg" width="30px"><span>星星</span> 👍（0） 💬（0）<div>强行吹 
Redisson 或者你自己写个watchdog 都可以解决续期问题 
本质上zk 的心跳维持就是 client 在自动续期

为什么这么多人使用redis 还是因为redis 读写性能远超 zk etcd</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/12/965a6cc9.jpg" width="30px"><span>菠萝power</span> 👍（0） 💬（0）<div>这个和lock API有什么区别吗 server&#47;etcdserver&#47;api&#47;v3lock&#47;v3lockpb&#47;v3lock.proto</div>2022-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c0/e7a59706.jpg" width="30px"><span>chongsheng</span> 👍（0） 💬（0）<div>如果用etcd，能指定锁的自动释放时间吗？我看NewSession方法里对lease做了keepalive，只要不unlock或者崩溃，是不是一直持有锁呢？</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>如果获取锁的client crash了。  其他的client监听到delete后获取到了锁，但是第一个client其实只是因为网络原因没有发送lease，但是它恢复后继续执行代码。就相当于一个资源被两个client操作了啊。</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/7d/ac715471.jpg" width="30px"><span>独孤九剑</span> 👍（0） 💬（0）<div>面试不怕分布式锁问题了</div>2021-07-05</li><br/>
</ul>