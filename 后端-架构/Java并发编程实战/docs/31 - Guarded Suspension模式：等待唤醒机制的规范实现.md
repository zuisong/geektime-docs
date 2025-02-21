前不久，同事小灰工作中遇到一个问题，他开发了一个Web项目：Web版的文件浏览器，通过它用户可以在浏览器里查看服务器上的目录和文件。这个项目依赖运维部门提供的文件浏览服务，而这个文件浏览服务只支持消息队列（MQ）方式接入。消息队列在互联网大厂中用的非常多，主要用作流量削峰和系统解耦。在这种接入方式中，发送消息和消费结果这两个操作之间是异步的，你可以参考下面的示意图来理解。

![](https://static001.geekbang.org/resource/image/d1/21/d1ad5ce1df66d85698308c41e4e93a21.png?wh=1142%2A393)

消息队列（MQ）示意图

在小灰的这个Web项目中，用户通过浏览器发过来一个请求，会被转换成一个异步消息发送给MQ，等MQ返回结果后，再将这个结果返回至浏览器。小灰同学的问题是：给MQ发送消息的线程是处理Web请求的线程T1，但消费MQ结果的线程并不是线程T1，那线程T1如何等待MQ的返回结果呢？为了便于你理解这个场景，我将其代码化了，示例代码如下。

```
class Message{
  String id;
  String content;
}
//该方法可以发送消息
void send(Message msg){
  //省略相关代码
}
//MQ消息返回后会调用该方法
//该方法的执行线程不同于
//发送消息的线程
void onMessage(Message msg){
  //省略相关代码
}
//处理浏览器发来的请求
Respond handleWebReq(){
  //创建一消息
  Message msg1 = new 
    Message("1","{...}");
  //发送消息
  send(msg1);
  //如何等待MQ返回的消息呢？
  String result = ...;
}
```

看到这里，相信你一定有点似曾相识的感觉，这不就是前面我们在[《15 | Lock和Condition（下）：Dubbo如何用管程实现异步转同步？》](https://time.geekbang.org/column/article/88487)中曾介绍过的异步转同步问题吗？仔细分析，的确是这样，不过在那一篇文章中我们只是介绍了最终方案，让你知其然，但是并没有介绍这个方案是如何设计出来的，今天咱们再仔细聊聊这个问题，让你知其所以然，遇到类似问题也能自己设计出方案来。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（64） 💬（10）<div>当从消息队列接收消息失败时，while循环会一直执行下去，永远不会结束，回占用大量资源。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/d5/e23dc965.jpg" width="30px"><span>Felix Envy</span> 👍（49） 💬（2）<div>老师，感觉如果有方法调用了GuardedObect.create方法但是没有任何其他线程调用fireEvent方法会造成内存泄漏啊，这种情况需要考虑吗？</div>2019-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvrwfqAuRkaK8Pl2apHKFZxd5mjnFhROMNcg5qXUT4AxE2ZTTia5Hg6pmFM1vozq3vZiagJoaJ4Pyg/132" width="30px"><span>zhangwei</span> 👍（40） 💬（14）<div>老师，我有个疑问，希望帮忙解答。如果Web应用是集群的，A节点处理HTTP请求后发了MQ，B节点的onMessage消费了回执消息，那么A节点怎么把结果响应给客户端呢？疑问好久了，希望老师给个思路，谢谢！</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/ba/2175bc50.jpg" width="30px"><span>Mr.Brooks</span> 👍（26） 💬（2）<div>没有锁也无法保证内存可见性吧</div>2019-05-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Dh6hib6KsQDsucBZztpyAp6hEhb4j2aJrLdsYnH1Ll6D0yaTuYPpYj1vmwWN97lfxsH6V8CZp8nCXdIejffslVg/132" width="30px"><span>朵朵集团总裁</span> 👍（10） 💬（1）<div>如果mq服务挂了无法消费，会引起web请求服务很多线程出于等待状态，是不是应该whlie循环加上超时。</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（9） 💬（1）<div>接入微信支付支付宝支付里边，也需要提供一个回调函数，onChange()就是一个回调函数吧，不过微信支付宝支付是异步回调，是不是也可以改成这种？微信支付宝里边的其它第三方支付是不是就是这种模式，因为支付成功之后跳转到它们自己的页面，而不是微信支付宝官方的支付成功界面</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（7） 💬（3）<div>老师 future.get 就是guarded suspension 的应用吧</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/22/9024c062.jpg" width="30px"><span>庄墨寒</span> 👍（7） 💬（1）<div>老师, 我觉得您只是举个例子吧. 真实的生成环境, A和B肯定都是一个集群; A 给 B发一个消息. B处理完后再给A发一个消息,  在A 集群中发送和接收消息的大概率两台不同的机器. 解决这个问题两种办法: 1. web 请求长轮询; 2. A集群有分布式的缓存, A的某台机器处理消息后把结果写到缓存, 处理web请求的机器有专门的线程去轮询. </div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（7） 💬（1）<div>如果以文中的最后一段示例代码来看，每一个请求生成一个id，对应一个GuardedObject，并没有线程安全问题。我觉得可以去掉锁。
但是加sleep的话，没有办法唤醒，只能等到超时。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/fc/d1dd57dd.jpg" width="30px"><span>ipofss</span> 👍（5） 💬（1）<div>老师，这节听了个大概，不是非常懂。其中有一点没理解，get方法加锁后，while判断一直都为true，也就一直不会释放锁，那onChanged方法进去之后，获取不到锁，双方不久互相死等下去了么，我应该还是哪里没想明白</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（5） 💬（2）<div>问题的原因主要是sleep没办法提供等待-唤醒机制，也就是说极端情况下可能会一直处于睡眠状态。
老师，有个问题，为什么sleep不能被唤醒啊？网上查了下答案，好像是说wait会持有一个对象锁(JVM)提供的，然后在执行notify操作的时候，JVM会释放这个对象锁，并选择一个等待的线程执行。而sleep并没有释放这个锁，所以没办法唤醒？感觉有点道理，但是不知道对不对，望老师不吝赐教</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/6a/b5478b65.jpg" width="30px"><span>Ab</span> 👍（4） 💬（2）<div>老师， 有一个地方不太理解，扩展 Guarded Suspension 模式 这一节第一个例子，get和onChange方法应该是在同一个GuardedObject上调用的吧，为啥还有维护一个Map来存储msgId和GuardedObject之间的关系呢？</div>2019-08-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（2） 💬（4）<div>老师，您好！
我想到了一个场景：​线程 t1 提交了消息 m1，线程 t2 提交了消息 m2，此时都在 get() 方法处等待结果返回。m2 先被处理完，this.obj 对应的是消息 m2 的结果，调用 fireEvent() 唤醒 t1 和 t2，t1 竞争到锁资源，消费了 m2 的结果 this.obj。

如果存在这种场景，再维护一个 ConcurrentHashMap，key 是 msg.id，value 是对应的 obj，是否就能解决结果这问题？

谢谢老师！</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（1）<div>guarded suspension模式解决了我工作中的一个问题
client同步掉我的服务a，服务a处理并需要等待一个定时任务的执行结果，</div>2020-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（1） 💬（2）<div>王老师，请问这里lock是实例私有对象，为什么不用 lock.signal？  感觉文案里的代码不需要signalall函数，因为这个lock是每次都new出来的，线程等待队列里永远只有一个线程，所以signalall意义不大</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（2）<div>项目中我使用了Map&lt;key, CountdownLatch&gt;来处理异步转同步调用，异步等待时通过countdownLatch.await(timeout)设置超时时长，请问老师这跟你讲的lock nitifyAll管程方法是否类似？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（1） 💬（1）<div>

老师，问个细节问题：就餐人与餐桌的关系不是在大堂经理脑中吗？怎么写在就餐人的内部呢？是因为GuardedObject的类本身充当的大堂经理角色，类实例充当就餐人角色吗？
如果是这样的话，那大堂经理是唯一的吗？

回答问题：改成sleep不加锁就变成线程不安全的忙等待模式，应该不符合需求。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（0） 💬（2）<div>请问老师，真正消息队列的请求中，如果是需要有消息处理返回值的情况，就是采用这种模式实现的吗，例如RabbitMQ</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（1）<div>想问一下分布式环境下，异步转同步的方法有哪些？例如，数据服务部署多个instance，客户在Web UI上点击外部数据源试用，后端通过一个数据服务instance请求外部数据源，外部数据源会异步回调结果(LB地址)返回，怎么样将结果显示在请求数据服务的Web UI上? 客户试用的过程是同步的，但请求外部数据源操作流程是异步的。谢谢！</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/99/42929758.jpg" width="30px"><span>andy</span> 👍（0） 💬（1）<div>我有个疑惑就是，这里所说的MQ可以是RabittMQ或者是其他类型的MQ吗？还是说这个MQ其实就JAVA中的一个数据结构？</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/d2/e3ae7ddd.jpg" width="30px"><span>三木禾</span> 👍（0） 💬（1）<div>老师，您这代码能不能写的完整一点啊，前面有个onMessage ,后面有个onChange</div>2019-05-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELPbl4btlC1JF5xIYuRLdtzliav2ib7NbsJAkumfGo7DI7XycBRKuadVBq5Sh4RxwuKicVIZ2PSL3qHSbSCjU2shmQSlUlYP3PCtqCrZPFUpv48g/132" width="30px"><span>Kaleidoscoper</span> 👍（0） 💬（1）<div>想问下老师，Create和fireEvent方法不加锁可以么，像Create方法不加锁指令重排优化，先返回object再加进map里会不会有问题</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（0） 💬（1）<div>请问老师MQ不是可以点对点吗，那服务提供方不可以指定消费某条消息吗，这样线程T是不是也可以获得MQ返回的结果</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/5b/2a342424.jpg" width="30px"><span>青莲</span> 👍（91） 💬（0）<div>sleep 无法被唤醒，只能时间到后自己恢复运行，当真正的条件满足了，时间未到，接着睡眠，无性能可言</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（15） 💬（0）<div>总结：Guarded Suspension模式，要解决的是，发送消息的线程和消费消息结果的线程不是同一个，但是消息结果又需要由发送的线程进行处理，为此需要为每个消息创建出类似大堂经理，生活中一般是只有一个大堂经理，但是在编程世界里需要为每个分配一个大堂经理，大堂经理主要做的事情就是发送线程发送完消息时，将其阻塞，提供消息结果的回调接口，通知阻塞的发送线程消费消息结果。
课后习题：1、使用sleep如果消息结果已经返回，还需等到sleep超时，才能继续执行2、使用加锁的await方法可以保证可见性，如果使用sleep的话，需要给obj加上volatile3、感觉在sent（message）成功后才阻塞，不然有可能mq接收消息失败，while循环会一直执行下去，sent失败，直接响应提示给前端。
</div>2019-05-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlwpFM3tkeG15YqyJTYWkfqkdmro9POq6SicYm57TaEFDOUZCXjoe0Z0Iz6UibGQqic3icJRsHdFzibtw/132" width="30px"><span>zero</span> 👍（10） 💬（0）<div>wait会释放占有的资源，sleep不会释放</div>2019-05-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4akcIyIOXB2OqibTe7FF90hwsBicxkjdicUNTMorGeIictdr3OoMxhc20yznmZWwAvQVThKPFWgOyMw/132" width="30px"><span>Chuan</span> 👍（5） 💬（1）<div>这里有一个区别就是每次都创建了一个GuardedObject，相当于创建了多个大堂经理，这里和现实中有点不一样。目的是，如果使用一个GuardedObject，在singalAll时，可能会导致线程2的回执结果被线程1消费，即锁冲突。所以这里每次都创建不同的GuardedObject，其内部的锁也不同，在唤醒的时候就不会出错了。</div>2020-02-09</li><br/><li><img src="" width="30px"><span>Geek_110f21</span> 👍（3） 💬（0）<div>sleep两个问题，一个是实效性不及等待唤醒，第二是obj变量要加volatile保证可见性</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/67/fcba0967.jpg" width="30px"><span>zapup</span> 👍（3） 💬（0）<div>go 像是 msg 的专属私人经理。
1. 拿着 id（预约的房号） 来，由大堂总部 GuardedObject 派一位私人经理 go 专门负责（static create()），并记录在册（gos）；
2. 如果你提前问你的私人经理「好了吗」（go.get()），他会先 hold 住你，并等待总部喊话；
3. 后勤部打扫好卫生之后，不会直接与某个私人经理（go）说，而是直接告诉大堂总部哪间房（id）已经好了（static fireEvent(id)）；
4. 大堂总部在小册子（gos）中找到负责此房间（id）的私人经理（go），并通知他「房间好了」（go.onChanged(obj)）；
5. 私人经理把被 hold 住的你唤醒（signAll）</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（2） 💬（0）<div>用sleep的话只能等睡眠时间到了之后再返回while循环条件去判断，但是wait相当于和singal组成等待唤醒的机制，这样满足条件的概率更大一些，性能也更好</div>2019-05-09</li><br/>
</ul>