你好，我是郑建勋。

这节课，让我们继续优化Master服务，实现Master请求转发和并发情况下的资源保护，同时实现Worker对分配资源的监听。

## 将Master请求转发到Leader

首先我们需要考虑一下，当Master是Follower状态，同时还接收到了请求的情形。在之前的设计中，为了避免并发处理时可能出现的异常情况，我们只打算让Leader来处理请求。所以，当Master节点接收到请求时，如果当前节点不是Leader，我们可以直接报错，由客户端选择正确的Leader节点。如下所示。

```plain
func (m *Master) AddResource(ctx context.Context, req *proto.ResourceSpec, resp *proto.NodeSpec) error {
	if !m.IsLeader() {
		return errors.New("no leader")
	}
}
```

我们还可以采用另外一种更常见的方式：将接收到的请求转发给Leader。要实现这一点，首先所有Master节点要在Leader发生变更时，将当前最新的Leader地址保存到leaderID中。

```plain
func (m *Master) Campaign() {
	select {
		case resp := <-leaderChange:
			m.logger.Info("watch leader change", zap.String("leader:", string(resp.Kvs[0].Value)))
			m.leaderID = string(resp.Kvs[0].Value)
		}	
		for {
			select {
			case err := <-leaderCh:
					m.leaderID = m.ID
			case resp := <-leaderChange:
				if len(resp.Kvs) > 0 {
					m.logger.Info("watch leader change", zap.String("leader:", string(resp.Kvs[0].Value)))
					m.leaderID = string(resp.Kvs[0].Value)
				}
		}
}
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIqvYMQ1yscgB6xS4nDkoOuP6KiaCiaichQA1OiaQ9rFmNtT9icgrZxeH1WRn5HfiaibDguj8e0lBpo65ricA/132" width="30px"><span>Geek_crazydaddy</span> 👍（0） 💬（2）<div>watchResource里获取和删除任务时为啥都不判断任务是不是分配给当前worker了？</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（0）<div>follow节点在收到资源变更请求，当请求到达grpc服务层时，通过注入进来的master grpc client，向master发起请求，参数不变，实现了转发功能，这个设计很赞！👍</div>2023-02-07</li><br/>
</ul>