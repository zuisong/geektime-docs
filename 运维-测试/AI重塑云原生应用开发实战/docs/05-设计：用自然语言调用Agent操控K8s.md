你好，我是邢云阳。

在上一章中，我们深入探讨了 Function Calling 和 AI Agent 的原理，并通过 Go 语言实践了 ReAct Agent。在操作之后，你可能发现，看似复杂的 Agent 实际上只是将人类的工作经验传授给大模型，使其能够代替我们完成任务，理解起来并不困难。更为简单的是，在实际操作中，我们只需要设计出一套优质的 prompt 模板，就能完成 Agent 应用开发的一半工作，真是应了那句话：得 prompt 者得天下！

既然我们的课程主题是 AI + 云原生应用开发，那么接下来的两章，我将带领你通过 Agent 与 Kubernetes（K8s）进行实际操作与应用。本章我们将聚焦如何用自然语言来控制 Kubernetes，在下一章，我们再进一步探讨 Kubernetes 的智能运维。

## 传统的 Kubernetes 交互方式

众所周知，与 Kubernetes 交互的方式主要有以下几种：

- **kubectl 命令行**

Kubectl 是官方提供的命令行工具，用于与 Kubernetes 集群进行交互。比如要获取 default 命名空间下的 Pods 信息，命令如下：

```powershell
root@hi-test:~# kubectl get po                                                                                                                                           
NAME                       READY   STATUS    RESTARTS   AGE                                                                                                              
ng-test-7bdff759b9-r49jj   1/1     Running   0          13d
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/43/e0/66b71c1f.jpg" width="30px"><span>哈哈</span> 👍（2） 💬（1）<div>老师，咨询个问题，AI agent在联通容器云的生产环境，有应用场景没？我个人感觉，学这个暂时做技术储备，有时候考虑安全性，特别是金融领域，很少用于生产。</div>2024-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>充电中，对 client-go 比较熟，看看后续的章节最终会实现一个什么样的效果，感觉挺有意思</div>2025-02-01</li><br/>
</ul>