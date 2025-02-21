你好，我是Barry。

在上节课，我们一起梳理了直播系统需要开发的功能模块以及整体搭建方案。当时我们提到过，直播服务器会用到Nginx代理。接下来，我们就来学习如何用Nginx实现直播的服务配置和部署。

其实我们前面第三十一节课已经用过Nginx来实现后端部署。但那时候，我们并没全面了解过这个技术，也没了解过Nginx如何在直播系统发挥作用。这节课我们不妨带着这些问题做进一步探索。

## Nginx详解

你可能听说过，Nginx是一个适合各种互联网应用场景的高性能Web服务器和反向代理服务器。不过你也许并没有全面思考过，它到底有哪些优势和功能特点，才能在众多代理服务器里脱颖而出。我们这就来详细聊聊这个问题。

Nginx由俄罗斯程序员Igor Sysoev开发。它有两个优势，第一个优势你安装的时候就会发现，Nginx占用内存非常少。另外，Nginx的并发能力也在同类型网页服务器里最为出色。

那Nginx的功能特点又有哪些呢？我归纳为四个特点。

第一，**Nginx可以作为反向代理服务器使用**，它可以将客户端的请求转发到后端的服务器处理。这么做能整合多个服务器的处理能力，实现负载均衡和高可用性，大大提高系统的整体性能和稳定性。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erAhtlpeFFwRk5g5LvzLcZgybImECIdKmhG1aPxdbnqWP6LmeNz5ibYibOedUwF7NjTy1asZqUur5uQ/132" width="30px"><span>kenan</span> 👍（0） 💬（2）<div>老师好，想请教一个问题：通过nginx -s reload 重新启动之后，还是会有接口报错，如何解决呢？</div>2023-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：Nginx正向代理作用于客户端，什么意思？
感觉正向和反向都是代表后端的服务器啊，好像没有什么区别啊。
Q2：线上应用中，正常应该是是”多数允许，少数禁止”，此时应该怎么配置？ Allow:all; deny: 192.168.3.2,这样吗？
Q3：worker_processor是进程吗？ 可以配置为大于1的数字吗？
Nginx不就是一个进程吗？ 怎么可能有多个进程？
Q4：MIME是具体的类型吗？ 设置这个代表了哪些类型？</div>2023-07-11</li><br/>
</ul>