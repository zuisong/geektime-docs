你好，我是轩脉刃。

上一讲我们使用 net/http 搭建了一个最简单的 HTTP 服务，为了帮你理解服务启动逻辑，我用思维导图梳理了主流程，如果你还有不熟悉，可以再回顾一下。

今天我将带你进一步丰富我们的框架，添加上下文 Context 为请求设置超时时间。

从主流程中我们知道（第三层关键结论），HTTP 服务会为每个请求创建一个 Goroutine 进行服务处理。在服务处理的过程中，有可能就在本地执行业务逻辑，也有可能再去下游服务获取数据。如下图，本地处理逻辑 A，下游服务 a/b/c/d， 会形成一个标准的树形逻辑链条。

![](https://static001.geekbang.org/resource/image/33/71/33361f90298865f98e3038f11f02e671.jpg?wh=1920x1080)

在这个逻辑链条中，每个本地处理逻辑，或者下游服务请求节点，都有可能存在超时问题。**而对于 HTTP 服务而言，超时往往是造成服务不可用、甚至系统瘫痪的罪魁祸首**。

系统瘫痪也就是我们俗称的雪崩，某个服务的不可用引发了其他服务的不可用。比如上图中，如果服务 d 超时，导致请求处理缓慢甚至不可用，加剧了 Goroutine 堆积，同时也造成了服务 a/b/c 的请求堆积，Goroutine 堆积，瞬时请求数加大，导致 a/b/c 的服务都不可用，整个系统瘫痪，怎么办？

最有效的方法就是从源头上控制一个请求的“最大处理时长”，所以，对于一个 Web 框架而言，“超时控制”能力是必备的。今天我们就用 Context 为框架增加这个能力。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（23） 💬（0）<div>“context作为函数的第一个参数”大概有两层意思。一是作为函数的参数传入。这个应该是针对在一个struct的多个方法中共享一个context的情况说的。因为每个方法都有可能需要创建子context，所以不应该共享而是应该显式传递。二是作为第一个参数。这个多半是一种约定。在支持可变长参数的语言中，固定参数只能出现在可变参数的前面。而作为与业务逻辑关系不大的context，出现在第一个的位置也方便也其他参数作区分。

说到与业务逻辑关系不大，个人以为显式传递context是对业务逻辑的侵入，更别提单元测试的时候还需要适当地mock掉。目前代码里请求控制和请求实现混在一起的情况后面应该会改掉吧？</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/3f/d96c1b97.jpg" width="30px"><span>zhao</span> 👍（7） 💬（2）<div>代码里面context的封装跟gin的源代码真是像极了，对照来看，对框架的理解又加深了一些。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（2） 💬（1）<div>真的很好，我读了四遍，才读懂老师代码的强大。</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/41/37/b89f3d67.jpg" width="30px"><span>我在睡觉</span> 👍（1） 💬（5）<div>你好老师，这个代码运行之后，一次HTTP请求过来，ServeHTTP函数会被调用两次，请问是为什么？
</div>2021-11-26</li><br/><li><img src="" width="30px"><span>2345</span> 👍（1） 💬（1）<div>文章写得很好，赞一个，比较有深度</div>2021-09-22</li><br/><li><img src="" width="30px"><span>0mfg</span> 👍（1） 💬（12）<div>叶老师您好，把分支2 git下来尝试运行，报错如下，求指教，谢谢
# command-line-arguments
.\main.go:10:2: undefined: registerRouter
</div>2021-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Qn1PDx7xA7jKFZr4vHibmsvoZ7bwUCzHTg3uywiaESCgFTTMibPpKdZOfrqTXtdQXxUJqFqmLAj5NoIFMJpYibbcOQ/132" width="30px"><span>happy learn</span> 👍（1） 💬（1）<div>到底是一个请求一个goroutine还是一个连接一个goroutine，前后两篇文章说的不一致</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/f1/39/b0960780.jpg" width="30px"><span>恶魔果实</span> 👍（1） 💬（1）<div>为什么会导致服务b和服务c的瞬时请求加大？这里不是很理解。
a请求失败，但是b，c请求是成功的呀。</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（0） 💬（1）<div>看完这一章，感觉目前还没达到这个水平，难以跟进呀</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（2）<div>在发出取消信号的时候，是不是所有子goroutine中都得有监听ctx.Done()并主动结束goroutine的代码逻辑，才能让所有gourutine都结束，还是说，不需要这样的逻辑所有就可以实现呢</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6b/23/ddad5282.jpg" width="30px"><span>Aaron</span> 👍（0） 💬（1）<div>我们公司用的是go micro微服务框架，在写所有的功能的时候，都是第一个参数是context，用的也是第三方的版本。平时使用时，会在ctx里流转很多必要的信息，比如认证信息等，都会存储进去。我觉得一是流转数据方便，在一个应该是一种标准约束，第三就是评论区里说的控制超时。</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>1 通过传值实现数据共享。
2 第一个参数也算是一种约定，防止参数错传。</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>【超时事件触发结束之后，已经往 responseWriter 中写入信息了，这个时候如果有其他 Goroutine 也要操作 responseWriter， 会不会导致 responseWriter 中的信息重复写入？】这句话不是很理解，为什么说超时事件触发结束后，已写入信息了呢？</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>你好，『超时事件触发结束之后，已经往 responseWriter 中写入信息了，这个时候如果有其他 Goroutine 也要操作 responseWriter， 会不会导致 responseWriter 中的信息重复写入？』请问为什么会提到重复写入呢？</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/01/ed3218c4.jpg" width="30px"><span>邵年紧时</span> 👍（0） 💬（2）<div>没太明白，这节内容设置超时context为什么要copy自主逻辑流程产生的Context；不用应该也可以啊；从代码上还没看到带来的好处。</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/67/4e381da5.jpg" width="30px"><span>Derek</span> 👍（0） 💬（1）<div>图片Context代码结构中有SetHandler方法，github的demo上没有这个方法</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/3f/d96c1b97.jpg" width="30px"><span>zhao</span> 👍（0） 💬（1）<div>搞清楚这一点，我们回看第二步，做完具体业务逻辑就结束是不行的，还需要处理 panic。所以这个 Goroutine 应该要有两个 channel 对外传递事件。
-------
这行话下面的代码块，go 一个匿名函数的时候少了右括号&#39;)&#39;。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/2d/0f/3d341419.jpg" width="30px"><span>.</span> 👍（0） 💬（1）<div>叶大可不可以在标注一下每段代码是在哪个文件夹里？从零开始的话不知道项目的目录结构是怎么样的</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/af/fd/a1708649.jpg" width="30px"><span>ゝ骑着小车去兜风。</span> 👍（4） 💬（0）<div>老师这个课程真的全是干货，感觉看了前两章都已经值回票价了</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ab/29/e4f7fb3c.jpg" width="30px"><span>高。</span> 👍（2） 💬（0）<div>老师，我有个疑问，代码中
go fun() {
&#47;&#47; 这里做具体的业务 
time.Sleep(10 * time.Second) 
c.Json(200, &quot;ok&quot;) ... 
&#47;&#47; 新的 goroutine 结束的时候通过一个 finish 通道告知父 goroutine 
finish &lt;- struct{}
} 

如果说设置的超时时间也是10秒，那么子goroutine中c.Json(200, &quot;ok&quot;)执行到一半，正好轮到父goroutine执行写入c.Json(500, &quot;time out&quot;)，此时是父goroutine会等待子goroutine写入完成，还是子goroutine由于写锁的原因被打断写入

如果是第一种的话，response就会被写入两次，就会产生以下报错
http: superfluous response.WriteHeader call from coredemo&#47;framework.(*Context).Json 

是否应该优化一下加锁的逻辑？</div>2022-11-04</li><br/><li><img src="" width="30px"><span>Geek_cbab11</span> 👍（2） 💬（6）<div>异常事件、超时事件触发时，需要往 responseWriter 中写入信息，这个时候如果有其他 Goroutine 也要操作 responseWriter，会不会导致 responseWriter 中的信息出现乱序？
超时事件触发结束之后，已经往 responseWriter 中写入信息了，这个时候如果有其他 Goroutine 也要操作 responseWriter， 会不会导致 responseWriter 中的信息重复写入？

问题1：这两个问题说的其他goroutine是哪些goroutine？
问题2：为什么controller中的goroutine没有进行Lock操作？
问题3：在Unlock之前已经进行了调用了Write方法，难道此次请求还没有结束吗？如果结束了为什么还允许继续写入呢？

还望老师解答一下。感谢！</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/65/df/11406608.jpg" width="30px"><span>轻剑切重剑</span> 👍（1） 💬（0）<div>老师好，请教下，为什么在超时之后 case &lt;-durationCtx.Done()，不添加 c.Abort() ？</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（1） 💬（0）<div>return rdb.Set(ctx, &quot;key&quot;, &quot;value&quot;, 0).Err()  老师 这个方法报错了欸：
源码： func (c *cmdable) Set(key string, value interface{}, expiration time.Duration) *StatusCmd {...}
好像多了一个参数啊</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（1） 💬（0）<div>不错不错 有深度</div>2021-09-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/81nl94ib1WUGibtLheNuBD9icaquiasIMia9ibdXF35Ia1NbYfIOt5tTEYFBEZvxiazwzJBSSicvUjWP4ldTGMJLVX0yXJjRTJPibjqnSHLGIK2NLSSs/132" width="30px"><span>Lee</span> 👍（0） 💬（0）<div>D:\goPath\src\net\dial.go:763:13: cannot use sl.listenMPTCP(ctx, la) (value of type *TCPListener) as Listener value in assignment: *TCPListener does not implement Listener (missing method Adbdr)
作者你好，能帮忙看一下这个问题，使用的go版本是1.23.0</div>2025-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/75/82/72398a60.jpg" width="30px"><span>?</span> 👍（0） 💬（0）<div>文章中对 ctx 的加锁感觉不应该暴露出来，应该在 ctx 内部实现对并发的控制。否则使用 ctx 的各个地方都需要写类似的代码。</div>2024-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/79/803537db.jpg" width="30px"><span>慢动作</span> 👍（0） 💬（0）<div>为什么要在goroutine里做c.json,把结果传回去，就不用加锁了（select只会执行一次）？</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/08/01/da970033.jpg" width="30px"><span>zh</span> 👍（0） 💬（0）<div>不是视频嘛？请问</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/61/77/e4d198a6.jpg" width="30px"><span>MR.偉い！</span> 👍（0） 💬（0）<div>c.Json(200, &quot;ok&quot;)也是对操作 responseWriter进行的操作，为什么不在c.Json的时候加锁呢？
在c.Json的时候，case &lt;-durationCtx.Done():也是有可能发生的呀？</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/0a/23/c26f4e50.jpg" width="30px"><span>Sunrise</span> 👍（0） 💬（1）<div>最后两种边界情况不太懂，如果有其他 Goroutine 也要操作 responseWriter 不是新的请求吗，跟这次的没啥关联吧，能举个具体场景吗</div>2022-11-29</li><br/>
</ul>