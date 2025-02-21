你好，我是郑建勋。

上一节课，我们搭建起了Master的基本框架。这一节课，让我们接着实现分布式Master的核心功能：选主。

## etcd选主API

我们在讲解架构设计时提到过，可以开启多个Master来实现分布式服务的故障容错。其中，只有一个Master能够成为Leader，只有Leader能够完成任务的分配，只有Leader能够处理外部访问。当Leader崩溃时，其他的Master将竞争上岗成为Leader。

实现分布式的选主并没有想象中那样复杂，在我们的项目中，只需要借助分布式协调服务etcd就能实现。[etcd clientv3](https://pkg.go.dev/go.etcd.io/etcd/clientv3/concurrency) 已经为我们封装了对分布式选主的实现，核心的API如下。

```plain
// client/v3/concurrency
func NewSession(client *v3.Client, opts ...SessionOption) (*Session, error)
func NewElection(s *Session, pfx string) *Election
func (e *Election) Campaign(ctx context.Context, val string) error
func (e *Election) Leader(ctx context.Context) (*v3.GetResponse, error)
func (e *Election) Observe(ctx context.Context) <-chan v3.GetResponse
func (e *Election) Resign(ctx context.Context) (err error)
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/6e/5f2a8a99.jpg" width="30px"><span>無所畏</span> 👍（0） 💬（1）<div>这段话是不是有问题？
&quot;waitDeletes 函数会调用 client.Get 获取到当前争抢的 &#47;resources&#47;election&#47; 路径下具有最大版本号的 Key&quot; 
看waitDeletes 源码的注释是：
&quot;waitDeletes efficiently waits until all keys matching the prefix and no greater than the create revision.&quot;

</div>2023-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（3）<div>请问老师：

“当前 Master 需要监听这个最大版本号 Key 的删除事件。当这个特定的 Key 被删除，就意味着已经没有比当前 Master 创建的 Key 更早的 Key 了，因此当前的 Master 理所当然就排队成为了 Leader。”

1 是所有master监听的内容都相同吗？
2 这里如何避免惊群？

</div>2023-01-26</li><br/><li><img src="" width="30px"><span>Geek_2c2c44</span> 👍（0） 💬（0）<div>选主那里， for loop里面的time.After建议改一下， 每次调用time.After会返回一个channel, 可能有内存泄漏的风险；改成Ticker或者context.WithTimeout来实现</div>2024-01-30</li><br/><li><img src="" width="30px"><span>Geek_7e6c5e</span> 👍（0） 💬（0）<div>太酷了，etcd让普通程序员也有了开发分布式系统的能力</div>2023-01-23</li><br/>
</ul>