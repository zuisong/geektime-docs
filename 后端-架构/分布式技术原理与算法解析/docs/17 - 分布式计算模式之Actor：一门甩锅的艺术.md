你好，我是聂鹏程。今天，我来继续带你打卡分布式核心技术。

我在前两篇文章中，带你一起学习了MapReduce和Stream计算模式，相信你对批处理和流计算也有了一定的了解。虽然这两种计算模式对数据的处理方式不同，但都是以特定数据类型（分别对应静态数据和动态数据）作为计算维度。

在接下来两篇文章中，我将从计算过程或处理过程的维度，与你介绍另外两种分布式计算模式，即Actor和流水线。分布式计算的本质就是在分布式环境下，多个进程协同完成一件复杂的事情，但每个进程各司其职，完成自己的工作后，再交给其他进程去完成其他工作。当然，对于没有依赖的工作，进程间是可以并行执行的。

你是不是想说，分布式进程那么多，如果需要开发者自己去维护每个进程之间的数据、状态等信息，这个开发量可不是一般得大，而且特别容易出错。那么，有没有什么办法可以让开发者只关注自己的逻辑呢？

答案是肯定的，Actor计算模式就能满足你的需求。也就是说，你可以把数据、状态等都扔给Actor。这是不是“一门甩锅的艺术”呢？

接下来，我们就一起打卡分布式计算模式中的Actor模式。

## 什么是Actor？

在第10篇文章“[分布式体系结构之非集中式结构：众生平等](https://time.geekbang.org/column/article/149653)”中，我曾提到Akka框架基于Actor模型，提供了一个用于构建可扩展的、弹性的、快速响应的应用程序的平台。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f2/66/b16f9ca9.jpg" width="30px"><span>南国</span> 👍（2） 💬（1）<div>怎么感觉actor类似于RPC，同样是发一条消息，然后进行某种计算，最后返回值</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/16/b0ab9a73.jpg" width="30px"><span>luffy</span> 👍（1） 💬（1）<div>actor能否理解为1条数据，如果计算的是图的话，每条数据都可以发消息到它相邻的点，这些相邻的点收到消息后，可以继续发消息和计算当前的点。</div>2020-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（9） 💬（0）<div>为什么认为Actor模式是计算模式呢？感觉更属于通信模式啊</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（8） 💬（2）<div>Actor 模型不适用于对消息处理顺序有严格要求的系统。因为在 Actor 模型中，消息均为异步消息，无法确定每个消息的执行顺序。虽然可以通过阻塞 Actor 去解决顺序问题，但显然，会严重影响 Actor 模型的任务处理效率。</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/fb/5a19b53e.jpg" width="30px"><span>胖虎</span> 👍（3） 💬（1）<div>阻塞则需要锁，actor本来的目的就是去锁化，与初衷背道而驰。</div>2019-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdCoCuWIfSd0z2Xd2iaYtM15Io390aqkQwpicvezs6Oeh7O5jleM555EZcmA5ibs2Rgu8nlWE1nvqww/132" width="30px"><span>Geek_eo2sbf</span> 👍（2） 💬（0）<div>全程都是在通信呢，跟计算有啥关系？
为什么这个算是计算模式的内容，而不是通信技术</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（0）<div>Actor 是否可以采用阻塞方式去运行呢，原因是什么呢？
说不可以，因为和设计初衷相悖，性能会下降，可用率也会下降。如果不在乎这些也就没什么不可以了，不违反自然规律，编程世界可以爱咋地就咋地😁</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/2d/1eebfc3c.jpg" width="30px"><span>GaGi</span> 👍（0） 💬（0）<div>文中说Actor的工作原理部分：Actor2 处理完 Actor1 的消息后，更新内部状态，并且向其他 Actor 发送消息，然后处理 Actor3 发送的消息。
老师，这里为什么Actor2更新完内部状态后要想其他Actor发送消息？发送什么消息呢？</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/80/540dd7ca.jpg" width="30px"><span>文刀流</span> 👍（0） 💬（1）<div>是不是可以理解如果把现有的系统全部都模块化然后给每一个模块分配一个消息队列来处理本模块的逻辑,用一个线程池来执行每个模块队列里面的消息,这样也是无需考虑加锁的.异步也能达到高并发。是不是就有点像akka</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/4a/d5f5a260.jpg" width="30px"><span>一毛钱</span> 👍（0） 💬（0）<div>如果使用阻塞的形式，各个actor会发生雪崩的现象，导致整个系统不可用</div>2019-11-14</li><br/><li><img src="" width="30px"><span>starnavy</span> 👍（0） 💬（0）<div>我觉得如果要保证消息处理顺序不一定要阻塞actor吧。每个actor都是单线程，只要每个actor都只有一个instance，那即便是异步处理也能保证消息处理顺序。这就像是消息队列，只要保证一个partition只有一个consumer在consume消息，这个partition的消息就可以保证顺序。
而且这个时候阻塞actor也没有用，因为下游的actor不会给一个response来确认消息已被成功处理。因为actor model里面本来大家都是异步的，是没有response机制的。</div>2019-11-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkia7vItdTgyYTtsiaTZQhktpOSJWj53EwvkgE2sfVg0zKokL6hKHicjxLYDXXoMA7EFzZGaTEDkYuw/132" width="30px"><span>Geek_21afdb</span> 👍（0） 💬（0）<div>参考zeromq，一样能够实现同步调用，虽然阻塞，但可以通过异步时间模型</div>2019-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（0）<div>我理解得是，Actor用mailbox（队列）就是方便存放暂时无法处理的消息；如果变成阻塞的这个mailbox元素个数就始终为1，那么这个mailbox还有存在的必要吗。

用JUC做类比，有ThreadPoolExecutor，用线程池加队列来高效处理任务；也有Exchanger这样一个线程生成一个消息，另一个才可以消费消息。

总之，利用合适的工具做合适的事，不能拿着锤子，看着什么都是钉子。
</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（0） 💬（1）<div>没接触过分布式的相关知识，看完有点不明觉厉</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（0）<div>是不是如果采用阻塞方式的话，比如有一个Actor发生阻塞，那与之关联的其它Actor为了等待任务的完成也会发生阻塞。因为Actor组成的网络结构是动态的，并没有一个预定的结构，因此会导致两个结果：

1、为了完成任务，被动阻塞的Actor新建Actor导致网络野蛮生长。

2、或者Actor的阻塞发生链式反应，最终导致整个系统可用性大幅下降。

异步方式就是为了解耦各个Actor，如果采用阻塞的模型，就与这个初衷南辕北辙了吧。

另外，感觉Actor模型和高并发网络编程中的reactor模型很像，虽然reactor模型不是分布式的，但是思路很像。</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/47/f6c772a1.jpg" width="30px"><span>Jackey</span> 👍（0） 💬（0）<div>简单思考了一下，Actor采用阻塞方式执行的话，很有可能出现多个Actor向一个Actor发消息，如果某个Actor发送的消息较大，或执行计算时被阻塞，后面的Actor再发送消息都会被阻塞，系统可用性就大大降低。
ps：跟着老师不仅能学分布式知识，还可以学到程序员必备技能—甩锅😂</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/29/c6/7fd7efa3.jpg" width="30px"><span>xingoo</span> 👍（0） 💬（0）<div>有点抓不住问题的关键点，感觉问的很模糊。

阻塞执行没啥不可以吧，效率低点而已，比如每个actor多线程调用队列中的任务，然后阻塞等待其他的actor，(不知道有没有这种用法）跟普通的分布式没啥区别。

不过actor得目标就是快速分布式计算，如果阻塞导致整体任务卡死，那就不如不要用他了。</div>2019-10-30</li><br/>
</ul>