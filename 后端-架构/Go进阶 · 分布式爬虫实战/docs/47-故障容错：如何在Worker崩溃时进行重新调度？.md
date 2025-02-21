你好，我是郑建勋。

上一节课，我们用随机的方式为资源分配了它所属的Worker。这一节课，让我们更进一步优化资源的分配。

对资源进行分配不仅发生在正常的事件内，也可能发生在Worker节点崩溃等特殊时期。这时，我们需要将崩溃的Worker节点中的任务转移到其他节点。

## Master调度的时机

具体来说，分配资源的时机可能有下面三种情况。

- 当Master成为Leader时。
- 当客户端调用Master API进行资源的增删查改时。
- 当Master监听到Worker节点发生变化时。

其中，第二点“调用Master API进行资源的增删查改”我们会在这节课的最后完成，下面让我们实战一下剩下两点是如何实现资源的调度的。

### Master成为Leader时的资源调度

在日常实践中，Leader的频繁切换并不常见。不管是Master在初始化时选举成为了Leader，还是在中途由于其他Master异常退出导致Leader发生了切换，我们都要全量地更新一下当前Worker的节点状态以及资源的状态。

在Master成为Leader节点时，我们首先要利用m.updateWorkNodes 方法全量加载当前的Worker节点，同时利用m.loadResource 方法全量加载当前的爬虫资源。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_2c2c44</span> 👍（0） 💬（1）<div>master调用DeleteResource之后， 只不过worker在下一次在loadresource的时候不会加载被删除的任务而已， 那woker已经运行的爬虫任务岂不是还在运行？</div>2024-01-31</li><br/>
</ul>