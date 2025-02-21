你好，我是邢云阳。

在前两节课中，我们介绍了 client-go 的两种进阶使用技巧。但需要强调的是，“存在即合理”——client-go 中每种操作资源的方法都有其特定的使用场景。是否在项目中采用这些进阶技巧，最终还需要根据需求来判断。例如，如果项目中并不需要高频查询，就没有必要通过 Informer 将资源缓存到本地。分享这些技巧的目的，是为了拓宽你的知识面，让你在实际工作中多一些选择，提高应对的灵活性。

与此同时，正如我反复提到的，API 是 AI 时代的一等公民。因此本节课，我们将在前面内容的基础上，完成资源的创建、删除和查询三种操作的代码实现，并使用 Gin 框架构建一个 HTTP Server，将这些功能封装成三个独立的 API。这些 API 将为后续 Agent 的调用提供工具支持。

## Gin 简介

首先，我们来简单介绍一下 Gin。Gin 是一个用 Go 语言编写的高性能、轻量级 Web 框架。它的设计灵感来自于 Python 的 Flask 框架，以简洁易用著称，非常适合构建 RESTful API。可以说 gin 已经成为了 Go 语言编写 Web 后端的最佳实践。

以下是一段最简单的 Gin 示例代码，展示如何快速搭建一个返回 “Hello, Gin!” 的 HTTP Server：
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/88/222d946e.jpg" width="30px"><span>linxs</span> 👍（1） 💬（1）<div>1. 在示例项目中，InitInformer方法中只添加了Pod的，只能查询 pods 资源
2. 如果要支持查询 其他对象如deployment的话， 需要在InitInformer方法中创建deployment的informer
</div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>clinet-go 和 informer 等机制的源码这块我之前就搞这方面的开发，看的比较多，看下来比较顺利，其实对于gvk和 gvr 互转的部分，如果在代码层面要优化一下的话可以直接使用controller-runtime 库中封装过的方法，有兴趣的同学可以自己去找找，使用原生client-go的好处就是可以从编程细节上对这些机制更清楚一些。
最后的总结写的很好，之前也正好做过api网关相关的运维和开发工作，感觉这个比喻很通俗易懂。</div>2025-02-01</li><br/>
</ul>