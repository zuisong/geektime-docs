你好，我是郑建勋。

在上一节课程中，我们实现了Master的选主，这一节课，我们继续深入Master的开发，实现一下Master的服务发现与资源的管理。

## Master服务发现

首先我们来实现一下Master对Worker的服务发现。

Master需要监听Worker节点的信息，感知到Worker节点的注册与销毁。和服务的注册一样，我们的服务发现也使用micro提供的registry功能，代码如下所示。

m.WatchWorker方法调用registry.Watch监听Worker节点的变化，watch.Next()会堵塞等待节点的下一个事件，当Master收到节点变化事件时，将事件发送到workerNodeChange通道。m.Campaign方法接收到变化事件后，会用日志打印出变化的信息。

```plain

func (m *Master) Campaign() {
	...
	workerNodeChange := m.WatchWorker()

	for {
		select {
		...
		case resp := <-workerNodeChange:
			m.logger.Info("watch worker change", zap.Any("worker:", resp))
		}
	}
}

func (m *Master) WatchWorker() chan *registry.Result {
	watch, err := m.registry.Watch(registry.WatchService(worker.ServiceName))
	if err != nil {
		panic(err)
	}
	ch := make(chan *registry.Result)
	go func() {
		for {
			res, err := watch.Next()
			if err != nil {
				m.logger.Info("watch worker service failed", zap.Error(err))
				continue
			}
			ch <- res
		}
	}()
	return ch

}
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（1） 💬（0）<div>1 “当 Master 成为新的 Leader 后，我们还要全量地获取一次 etcd 中当前最新的资源信息，并把它保存到内存中”，
当添加单个task任务时，使用事件监听；
事件监听机制在服务异常时可能丢信息？
望勋哥指点.

2 雪花算法生成的id有可能会出现重复。
如一个节点时，把服务器时钟回拨的情况；
多个节点时候，假如服务器的标志位一样，同一毫秒不同的节点可能产生的id相同；</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/3a/de/ed40f1bb.jpg" width="30px"><span>胡军</span> 👍（0） 💬（0）<div>老师语速好快，都来不及思考和看文档😅</div>2023-02-02</li><br/>
</ul>