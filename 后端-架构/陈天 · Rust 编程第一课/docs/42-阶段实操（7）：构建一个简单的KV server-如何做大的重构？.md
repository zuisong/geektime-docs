你好，我是陈天。

在软件开发的过程中，一开始设计得再精良，也扛不住无缘无故的需求变更。所以我们要妥善做架构设计，让它能满足潜在的需求；但也不能过度设计，让它去适应一些虚无缥缈的需求。好的开发者，要能够把握这个度。

到目前为止，我们的 KV server 已经羽翼丰满，作为一个基本的 KV 存储够用了。

这时候，产品经理突然抽风，想让你在这个 Server 上加上类似 Redis 的 Pub/Sub 支持。你说：别闹，这根本就是两个产品。产品经理回应： Redis 也支持 Pub/Sub。你怼回去：那干脆用 Redis 的 Pub/Sub 得了。产品经理听了哈哈一笑：行，用 Redis 挺好，我们还能把你的工钱省下来呢。天都聊到这份上了，你只好妥协：那啥，姐，我做，我做还不行么？

这虽是个虚构的故事，但类似的大需求变更在我们开发者的日常工作中相当常见。我们就以这个具备不小难度的挑战，来看看，如何对一个已经成形的系统进行大的重构。

## 现有架构分析

先简单回顾一下 Redis 对 Pub/Sub 的支持：客户端可以随时发起 SUBSCRIBE、PUBLISH 和 UNSUBSCRIBE。如果客户端 A 和 B SUBSCRIBE 了一个叫 lobby 的主题，客户端 C 往 lobby 里发了 “hello”，A 和 B 都将立即收到这个信息。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/1b/11/7d96bff5.jpg" width="30px"><span>yyxxccc</span> 👍（6） 💬（1）<div>很多时候，实际工作修改老系统，老系统啥单元测试啥的都没有😂，果真是动一行，就是牵一发而动全身，这方面老师有什么指导性原则么。</div>2021-12-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（3） 💬（1）<div>我有个疑问, tokio 本身不就是 支持了多路复用吗
用 yamux来整合多路复用的意义是什么?</div>2021-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（0） 💬（1）<div>我现在有个困惑  这几天一直没想到答案
比如老师说的yamux 来做连接的多路复用
如果客户端不能用rust 有办法对接吗?
我试了一下 如果服务器yamux 过的服务
对方如果不是yamux包装的 请求 会报错 就是不能当成常规的tcp连接来处理</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>写测试代码的确有助于我们思考，从而把代码写的更好。</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ea/2e/814b2d61.jpg" width="30px"><span>Freedom</span> 👍（2） 💬（0）<div>tokio家出了，tokio-yamux，哈哈哈，这下不用util转了</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/72/e2/9a19b202.jpg" width="30px"><span>阳阳</span> 👍（2） 💬（0）<div>二刷，终于跟着把代码写下来了</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（1） 💬（0）<div>思考题1: 主要考虑如何检测 receiver 被 drop 的情况以及何时触发 gc 操作；对于如何检测 channel 被关闭有两种方式：
1. 每个 sender 发一次消息便可知道，这种方法低效，而且一方面需要考虑用于检测的消息不能和用户可能发送的消息出现重合，另一方面发送出去的消息还可能会被用户看到，不考虑这种方式
2. tokio::mpsc::sender 提供了 is_closed 方法来判断 channel 是否关闭，简单高效。如果使用的 channel 没有提供这个方法，可以考虑仿照第 35 讲中的 channel 的实现，对 channel 进行包装并增加一个原子计数来判断 receiver 的数量
有了检测方式，接下来就是考虑触发时机，考虑到并发情况下，访问 subscriptions 会有锁的问题，而且这种情况不会太频繁，因此可以放在 unsubscribe 的时候进行检查和清理。

思考题2：如果要提供 PSUBSCRIBE 功能，考虑增加一张 patter 表，按照 glob::Pattern 来匹配，则表的形式为 patterns: DashMap&lt;Pattern, DashSet&lt;u32&gt;&gt;，其中 DashSet 用于保存 subscription id。在 publish 时候，遍历 patterns 并于 channel 进行匹配，匹配成功则取出 subscription id 并发送一条消息。

思考题的完整实现可以参考：https:&#47;&#47;github.com&#47;Phoenix500526&#47;simple_kv&#47;blob&#47;main&#47;src&#47;service&#47;topic.rs</div>2022-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/6a/70636993.jpg" width="30px"><span>Geek_aa1610</span> 👍（0） 💬（0）<div>有一个问题, 假设一个client sub了很多topic (同时有其他client在这些topic上做publish) sub的client端如何区分一次response是上一次sub的CommnadResponse::ok还是之前某次sub的topic上push来的新内容?</div>2022-08-28</li><br/>
</ul>