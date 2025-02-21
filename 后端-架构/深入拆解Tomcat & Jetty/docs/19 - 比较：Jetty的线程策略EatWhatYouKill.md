我在前面的专栏里介绍了Jetty的总体架构设计，简单回顾一下，Jetty总体上是由一系列Connector、一系列Handler和一个ThreadPool组成，它们的关系如下图所示：

![](https://static001.geekbang.org/resource/image/9b/41/9b0e08e109f41b1c02b9f324c0a71241.jpg?wh=1366%2A716)

相比较Tomcat的连接器，Jetty的Connector在设计上有自己的特点。Jetty的Connector支持NIO通信模型，我们知道**NIO模型中的主角就是Selector**，Jetty在Java原生Selector的基础上封装了自己的Selector，叫作ManagedSelector。ManagedSelector在线程策略方面做了大胆尝试，将I/O事件的侦测和处理放到同一个线程来处理，充分利用了CPU缓存并减少了线程上下文切换的开销。

具体的数字是，根据Jetty的官方测试，这种名为“EatWhatYouKill”的线程策略将吞吐量提高了8倍。你一定很好奇它是如何实现的吧，今天我们就来看一看这背后的原理是什么。

## Selector编程的一般思路

常规的NIO编程思路是，将I/O事件的侦测和请求的处理分别用不同的线程处理。具体过程是：

启动一个线程，在一个死循环里不断地调用select方法，检测Channel的I/O状态，一旦I/O事件达到，比如数据就绪，就把该I/O事件以及一些数据包装成一个Runnable，将Runnable放到新线程中去处理。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（21） 💬（1）<div>课后问题就有点像分布式服务为什么爱用消息中间件一样，一切都是为了解耦，服务类比线程，服务与服务可以直接通讯，线程与线程也可以直接通讯，服务有时候会比较忙或者挂掉了，会导致该请求消息丢失，线程与线程之间的上下文切换同样会带来很大的性能消耗，如果此时的线程池没有多余的线程使用，可能会导致线程积压致使cpu飙高，使用队列能够有效平衡消费者和生产者之间的压力，达到高效率执行。</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（3） 💬（1）<div>老实好!
检测到读就绪的时候数据已被拷贝到了内核缓存中。CPU的缓存中也有这些数据。
这句话怎么理解啊，CPU的缓存说的是高速缓存么?然后内核缓存是什么呢？这方面的知识需要看啥书补啊(是操作系统么?)?IO模型，数据需要拷贝的次数我一点搞不懂</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（2） 💬（1）<div>李老师能否讲一下怎么调试源码   怎么搭建调试源码的环境  就比如说拿Jetty举例</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（2） 💬（1）<div>老师，在NIO2中服务器端的几个概念不是很清晰，比如WindowsAsynchronousChannelProvider，Invoker等。如果需要系统了解这几个概念是怎么串起来的，怎么办呢。</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!我有个问题，我是先把学校教的计算机基础的书操作系统，计算机组成原理这些再看一遍补基础。还是直接上手撸源码啊？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（18） 💬（0）<div>第一selectorUpdate可以统一抽象封装注册的io事件，坐到面相抽象编程，将来如果nio的api接口有变动，也不需要改动ManangerSelector的代码 只需要新建一下selectorUpdate的子类来实现变更 第二  作为缓冲，，如果高并发的话，一下子很多channel注册到linux的epoll模型上，红黑树的层级就会很大，select的时候就比较耗时，有一个缓冲，可以均匀注册到linux的epoll模型上，既不会快速让红黑树发生过多旋转，也不会过多占用太多文件描述符</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（13） 💬（2）<div>李老师好!越看越不明白了，我承认我基础差也没去看源码。不晓得别的同学看不看的懂。
老师能不能画点图方便理解。managedSelector怎么工作的还是不清楚。
只看懂了四种生成消费模型
1.单线程
2.io多路复用，把selector当做生成着，处理的业务逻辑单做消费者。(缺点就是不能用缓存，接受任务和处理任务不在一个线程)
3.就是接受和处理放一个线程，整体放在多线程里面跑。好处就是可以用缓存
4.对3和2的优化。空余线程多的时候用3，不足用2。把接受到的任务缓存起来防止拒绝太多任务。
后面的就看不懂了。
问题1.managedSelector只负责监听read事件么?。accept事件他监听么?一个端口能被多个serversocketchannel监听么?
问题2.文中说managedselector由endpoint管理，具体怎么管理的呢?managedselector有多少个?怎么创建的?不同的managedselector之间channel共享么(个人感觉不共享会有并发冲突)?
问题3.线程不够用的时候具体怎么切换的呢?慢慢的全部都转成2还是保留一部分线程执行3一部分执行2。
问题4.我连channel是怎么注册到managedselector上的都没看明白。更别说销毁了。
其实就是想知道这几个类的生命周期，然候就是直接执行交互图，纯文字我想不出。希望老师解惑不胜感激</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/78/0f/f4e012a1.jpg" width="30px"><span>掐你小77</span> 👍（3） 💬（0）<div>本章节中主要涉及的是三个组件：ManagerSelector,Producer(SelectoeProducer),ExecutionStrategy
其中三个组件的作用如下：
1，ManagerSelector用于其他调用者注册感兴趣事件和事件对应的处理逻辑。
   如何注册感兴趣事件和处理逻辑呢？提供了两个接口：SelectorUpdate和Selectable，
   其中SelectorUpdate接口让调用者可以网ManagerSelector中的Selector注册感兴趣事件，
   其中Selectable接口让调用者提供一个处理逻辑。
   
2，Producer是一个发动机，它的作用就是：注册 --&gt; 获取就绪的IO --&gt; 产生对应的处理任务
   上述对应了其内部的三个方法：processUpdates,select,processSelected
   其对应的实现类为：ManagerSelector.SelectoeProducer

3，ExecutionStrategy则是上面Producer接口产生处理任务的执行策略了，jetty中默认的策略有：
   a，ProduceConsume 单线程创建和执行所有任务
   b，ProduceExecuteConsume 专门线程创建任务，然后任务放进线程池中执行
   c，ExecuteProduceConsume 一个线程中创建任务并执行，同时启动另一个线程进行任务的创建
      和执行，其中顺序是：创建任务 --&gt; 开启新线程（使用线程池） --&gt; 执行任务
   d，EatWhatYouKill  判断当前当前是否系统忙碌，在ProduceExecuteConsume和ExecuteProduceConsume
      运行模式中切换
            
较于理解（不准确）的执行顺序：调用者 --&gt; ManagerSelector --&gt; SelectoeProducer --&gt; ExecutionStrategy

这样总结对么？老师。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8c/48/2838ad55.jpg" width="30px"><span>sionsion</span> 👍（2） 💬（0）<div>https:&#47;&#47;webtide.com&#47;eat-what-you-kill&#47; , 这里有一篇文章也做了解释，有兴趣的可以看看。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/e9/a99ced9e.jpg" width="30px"><span>Gary</span> 👍（1） 💬（2）<div>老师好，在 ManagedSelector # SelectorProductor # processUpdates() 源码中看到有这么一段 
            synchronized(ManagedSelector.this)
            {
                Deque&lt;SelectorUpdate&gt; updates = _updates;
                _updates = _updateable;
                _updateable = updates;
            }
            ···
           for (SelectorUpdate update : _updateable){
            ···
            }
           这里不直接循环 _updates 的原因是防止不断有请求填充了 _updates，导致前面的请求无法返回吗，感觉这里的_updateable 用一个局部变量就可以了，为啥他要作为类的字段</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/45/e4314bc6.jpg" width="30px"><span>magicnum</span> 👍（1） 💬（0）<div>不直接注册I&#47;O事件是为了解耦吧，而且队列平衡了生产者消费者的处理能力</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/fa/4b8b3ece.jpg" width="30px"><span>Markss</span> 👍（0） 💬（0）<div>老师,有个地方不太理解, 利用同一个线程执行业务可以理解, 但是即使是同一个线程,用完cpu时间也会有上下文切换, 下一次执行依旧有可能被分配至其他cpu的呀, 依旧存在无法使用cpu缓存的问题呀?</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（0） 💬（0）<div>“根据 Jetty 的官方测试，这种名为“EatWhatYouKill”的线程策略将吞吐量提高了 8 倍”，jetty官方说明的链接有吗？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/e6/7808520d.jpg" width="30px"><span>Edward Lee</span> 👍（0） 💬（0）<div>对于课后习题，我说下自己的理解

ManagerSelector 管理 Queue 的好处
1、单线程管理 IO 事件无需加锁操作
2、从 Queue 里获取的 IO 事件可以根据策略选择更高效的处理方式
3、屏蔽 SelectKey 繁琐的感兴趣的设置操作
</div>2020-11-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4akcIyIOXB2OqibTe7FF90hwsBicxkjdicUNTMorGeIictdr3OoMxhc20yznmZWwAvQVThKPFWgOyMw/132" width="30px"><span>Chuan</span> 👍（0） 💬（0）<div>```
            case PRODUCE_CONSUME:
                _pcMode.increment();
                runTask(task);
                return true;

            case PRODUCE_INVOKE_CONSUME:
                _picMode.increment();
                invokeTask(task);
                return true;

            case PRODUCE_EXECUTE_CONSUME:
                _pecMode.increment();
                execute(task);
                return true;

            case EXECUTE_PRODUCE_CONSUME:
                _epcMode.increment();
                runTask(task);
```

老师，看了EatWhatYouKill的代码，在doProduce()方法中有以上内容，来执行生产的任务，第一种是当前线程串行执行，第二种是由生产的线程非阻塞的执行？？第三种是开新线程执行，第四种好像也是当前线程执行，不过每个执行前都有个_xxxMode.increment()，好像是通过这个变量来控制的？不太明白代码里第二种的非阻塞怎么体现，以及第一种和和第四种的区别，好像和_xxxMode这个变量相关，望老师指点下，谢谢！！</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>1. 原来EatWhatYouKill是这个意思啊！ 

2. 感觉jetty比tomcat更会巧妙的使用资源

3. 评论区的问题和我的好像也差不多，22讲答疑应该会有。

4. 操作系统的知识确实要常识化，到现在都没弄懂select poll epoll 是什么，已经三者之间的区别。

5. 但是看了老师的讲解后，自己渐渐对网络编程好像有兴趣了，也更好奇了，之前从来没有过的感觉。只是现在还不知道从哪入手。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/27/5556ae50.jpg" width="30px"><span>Demter</span> 👍（0） 💬（0）<div>赞一个</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/10/a543759a.jpg" width="30px"><span>kyon</span> 👍（0） 💬（1）<div>请问 Selectable 实现类是在什么时机注册到 ManagedSelector 的？是和提交 Selector 更新任务类一起吗？_selector.submit(_updateKeyAction)?

另外 ManagedSelector 里为什么有两个 SelectorUpdate 队列，下面一个是不是 Selectable 队列？
private Deque&lt;Selectable&gt; _updateable = new ArrayDeque&lt;&gt;();</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（0）<div>李老师!SelectorUpdate接口的update方法有个入参完了。硬是没看见哪用了这个入参。泪流满面老师。</div>2019-06-24</li><br/>
</ul>