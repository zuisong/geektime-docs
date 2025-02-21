你好，我是何辉。

今天我们用视频形式，统一梳理Dubbo日常开发必须掌握的基础特性，帮你查漏补缺。

视频是我之前录的，在网上发布过，这次统一整理了一下，你可以按需学习。之后遇到类似实现需要，你也可以回来复习。主要会涉及这几个知识点：

- XML配置发布与服务调用
- Java代码发布与服务调用
- 服务提供方异步化实践：AsyncContext#startAsync、返回CompletableFuture
- 服务消费方异步化实践：getFuture方式、setCallback方式、getCompletableFuture方式
- 常用配置参数：启动时服务依赖检查参数、读写请求重试次数设置参数、调用失败时的容错设置、负载均衡策略设置、线程模型设置、服务提供方超时中断流程设置、导出线程堆栈设置。

好，我们直接开始吧。

## XML配置发布与服务调用

1. 服务提供方provider的样例代码开发

<!--THE END-->

2. 服务消费方consumer的样例代码开发

<!--THE END-->

3. 服务消费方从Zookeeper获取地址调用提供方

## Java代码发布与服务调用

1. 启动服务提供方provider

<!--THE END-->

2. 启动服务消费方consumer

## 服务提供方异步化实践

1. 通过AsyncContext#startAsync实现提供方
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（4） 💬（1）<div>我是工作了5年多的，科班出身，本讲视频我全部学习了，并且都敲了一遍，来回看了好几遍，课程觉得非常实用，老师基本都是手把手教，值得一学，只要自己虚心学习。</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（1） 💬（1）<div>后续的课程都是视频的方式吗</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/41/62/cf9e3aaa.jpg" width="30px"><span>cheems</span> 👍（0） 💬（1）<div>老师视频课程的代码，有git地址吗</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/16/e0/7abad3cc.jpg" width="30px"><span>星期八</span> 👍（0） 💬（1）<div> RpcContext.getContext().getFuture().get() 这种调用方式怎么知道  就提调用的是哪个方法呢？</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（0） 💬（1）<div>nice!</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（1）<div>学习了一下 Dubbo 基础知识，感谢老师</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/bc/833c7968.jpg" width="30px"><span>大吖大鳄鱼</span> 👍（0） 💬（1）<div>老师代码有没有git地址</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/8e/850ce072.jpg" width="30px"><span>jizhi7</span> 👍（1） 💬（0）<div>dubbo 的基础视频在哪有发布么？</div>2023-08-20</li><br/>
</ul>