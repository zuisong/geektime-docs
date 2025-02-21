你好，我是邢云阳。

在上一节课中，我们讲解了 client-go 的四种客户端的功能与使用场景，并且介绍了 RestMapper 的用法。RestMapper 就像一个全国联网的警务平台一样，可以在仅提供资源名称 resource 的情况下，拿到资源的 GVK、GVR、scope 等等全部信息。一旦得到 GVR，我们便可以利用动态客户端与 Kubernetes 资源进行交互。

我们还知道，无论使用哪种客户端方式，本质还是通过 Rest API 的方式去请求目标 Kubernetes 集群的 API Server。这样就不可避免的会对 API Server 造成访问压力。幸好，官方提供了 Informer 机制，为我们解决了这个问题。

这套机制是对 List &amp;&amp; Watch 做了封装，并加入了缓存等功能。在初始时可以将资源全部缓存到本地，并且之后可以通过监听增删改事件来更新缓存中的资源状态。这样，我们在做查询操作时，就可以从本地缓存中获取到最新资源状态，无需访问 API Server。

接下来，我们就从 Lsit &amp;&amp; Watch 开始讲起，看看如何从实操角度，在我们的业务中利用起 Informer。

## List &amp;&amp; Watch

List &amp;&amp; Watch 是 Kubernetes 为我们提供的查询资源的两种方式。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（0） 💬（1）<div>不错不错，关于client-go的一些知识经过讲解之后更清晰了，谢谢老师</div>2025-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/71/3762b089.jpg" width="30px"><span>stevensafin</span> 👍（0） 💬（1）<div>跟 AI 有什么关系？</div>2024-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/b1/3d6075cc.jpg" width="30px"><span>王建</span> 👍（0） 💬（0）<div>思考题：
当用户传入 resource = pods 时，使用上一节代码中的 mappingFor() 方法，获取到 RESTMapping，RESTMapping 中的 Resource 就是完整的GVR信息，将其传给 fact.ForResource() 方法即可创建 informer。核心代码如下：

        mapper := InitRestMapper(client)
	restMapping, _ := mappingFor(&quot;pods&quot;, &amp;mapper)

	fact := informers.NewSharedInformerFactoryWithOptions(client, 0, informers.WithNamespace(&quot;default&quot;))
	informer, err := fact.ForResource(restMapping.Resource)
	if err != nil {
		panic(err)
	}
	informer.Informer().AddEventHandler(&amp;PodHandler{})
	fact.Start(wait.NeverStop)

	select {}</div>2025-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/e5/f3df7b02.jpg" width="30px"><span>ly</span> 👍（0） 💬（0）<div>三节k8s的课了，我的agent呢</div>2024-12-29</li><br/>
</ul>