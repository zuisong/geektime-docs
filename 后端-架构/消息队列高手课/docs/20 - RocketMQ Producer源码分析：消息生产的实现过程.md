你好，我是李玥。

对于消息队列来说，它最核心的功能就是收发消息。也就是消息生产和消费这两个流程。我们在之前的课程中提到了消息队列一些常见问题，比如，“如何保证消息不会丢失？”“为什么会收到重复消息？”“消费时为什么要先执行消费业务逻辑再确认消费？”，针对这些问题，我讲过它们的实现原理，这些最终落地到代码上，都包含在这一收一发两个流程中。

在接下来的两节课中，我会带你一起通过分析源码的方式，详细学习一下这两个流程到底是如何实现的。你在日常使用消息队列的时候，遇到的大部分问题，更多的是跟Producer和Consumer，也就是消息队列的客户端，关联更紧密。搞清楚客户端的实现原理和代码中的细节，将对你日后使用消息队列时进行问题排查有非常大的帮助。所以，我们这两节课的重点，也将放在分析客户端的源代码上。

秉着先易后难的原则，我们选择代码风格比较简明易懂的RocketMQ作为分析对象。一起分析RocketMQ的Producer的源代码，学习消息生产的实现过程。

在分析源代码的过程中，我们的首要目的就是搞清楚功能的实现原理，另外，最好能有敏锐的嗅觉，善于发现代码中优秀的设计和巧妙构思，学习、总结并记住这些方法。在日常开发中，再遇到类似场景，你就可以直接拿来使用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/6d/3a/dfda3cbd.jpg" width="30px"><span>. 。o O</span> 👍（36） 💬（3）<div>请教老师一个问题,如果异步发送的话,就是把发送逻辑封装成任务放到线程池里去处理,那么是不是就没法保证消息的顺序性了呢?哪怕是通过key哈希到一个同一个队列,但是发送消息的任务执行先后顺序没法保证吧?</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/17/8763dced.jpg" width="30px"><span>微微一笑</span> 👍（24） 💬（3）<div>老师好，先祝您节日快乐！！！您辛苦了~
有几个疑问需要老师解答一下：
①今天在看rocketMq源码过程中，发现DefaultMQProducer有个属性defaultTopicQueueNums，它是用来设置topic的ConsumeQueue的数量的吗？我之前的理解是，consumeQueue的数量是创建topic的时候指定的，跟producer没有关系，那这个参数又有什么作用呢？
②在RocketMq的控制台上可以创建topic，需要指定writeQueueNums，readQueueNums，perm，这三个参数是有什么用呢？这里为什么要区分写队列跟读队列呢？不应该只有一个consumeQueue吗？
③用户请求--&gt;异步处理---&gt;用户收到响应结果。异步处理的作用是：用更少的线程来接收更多的用户请求，然后异步处理业务逻辑。老师，异步处理完后，如何将结果通知给原先的用户呢？即使有回调接口，我理解也是给用户发个短信之类的处理，那结果怎么返回到定位到用户，并返回之前请求的页面上呢？需要让之前的请求线程阻塞吗？那也无法达到【用更少的线程来接收更多的用户请求】的目的丫。
望老师能指点迷津~~~</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（14） 💬（1）<div>老师，异步发送为什么是弃用，还是没有看懂，感觉超时时间的计算没有错啊…</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（8） 💬（7）<div>课后作业，请老师指正：
从方法的注释看，说是因为异常处理和超时时间的语义不对。
异常处理这块我觉得应该是采用统一的异常处理，而不应该是有的异常抛出，而有的异常通过回调方法返回客户端。
再说超时时间的错误语义，严格来说应该是不准确的超时时间，因为在run方法里进行时间判断（if (timeout &gt; costTime)）实际上已经是开始执行当前线程的时间，而之前的排队时间没有算，因此我改进的方法应该是这样：
CompletableFuture.runAsync(() -&gt; {
            long costTime = System.currentTimeMillis() - beginStartTime;
            if (timeout &gt; costTime) {
                try {
                    sendDefaultImpl(msg, CommunicationMode.ASYNC, sendCallback, timeout - costTime);
                } catch (Exception e) {
                    sendCallback.onException(e);
                }
            } else {
                sendCallback.onException(
                        new RemotingTooMuchRequestException(&quot;DEFAULT ASYNC send call timeout&quot;));
            }
        }, executor);</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（6） 💬（1）<div>       编程语言的话Python或Go可以么？极客时间里都有购买，就是忙着其它课程的学习，一直没顾的上编程语言的学习。
       从开始一路跟到现在：算是少数一直在完全没有缺的课；前期一直遍边学习边针对开篇时的学习目标针对当下工作环境的Nosql DB和MQ使用率的低下的问题找解决思路和方案，课后笔记主要同样集中在思路以及针对思路的困惑查疑上，代码这块完全没顾上。虽然代码的思路看的懂，发现动手能力确实非常欠缺。一路学到现在梳理到现在整体方案大致定下来：以及早期的部分课程的结束；课程的主要方案自己估计在掌握思路的基础上去补强Coding能力。虽然DBA的Coding能力都比较烂，不过还是得边学边啃下来；逼自己一下总能勉强写出来，估计就是效率问题、、、MQ这块PY或GO哪种更合适，或者说都可以？
        感谢老师一路的辛勤授业：授课之余尽力去帮助学生们解惑，让我们能一路走来一路成长；愿老师教师节快乐，谢谢老师的分享。</div>2019-09-10</li><br/><li><img src="" width="30px"><span>墙角儿的花</span> 👍（5） 💬（3）<div>老师 对于im服务器集群，客户端的socket均布在各个服务器，目标socket不在同一个服务器上时，服务器间需要转发消息，这个场景需要低延迟无需持久化，服务器间用redis的发布订阅，因其走内存较快，即使断电还可以走库。im服务器和入库服务间用其他mq解耦，因为这个环节需要持久化，所以选rocketmq或kafka，但kafka会延迟批量发布消息 所以选rocketmq，这两个环节的mq选型可行吗。</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（1） 💬（1）<div>老师继续请教问题：
1.DefaultMQPullConsumer和DefaultMQPushConsumer有什么区别
2.为什么pullConsumer的启动和producer的启动在同一个start方法里（最终都在MQClientInstance#start里）
3.rebalanceService服务是干嘛的</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（1）<div>     前期一直忙着强化和梳理一些基本功：操作系统、网络这块，学到现在发现老师的课程中的代码能看懂，大致思路也能明白；就是写不出。Python或者Go可以么？ Java实在、、、Python和Go极客时间都有购买课程。
           可能目前线上的存储中间件现状比较差【许老师的课程对数据存储的定义，觉得有道理就直接现用了】，尤其是Nosql DB和MQ基本处于闲置，故而一直焦虑在这块；可是当现在初期迷惑已经解除且基本清晰时发现学习这门课和使用MQ的瓶颈就在代码能力上，毕竟DBA的Coding能力都比较差尤其是开发相关的能力；准备开始把之前报的开发语言的课程学习一遍。
         今天教师节：愿老师节日快乐，感激老师在授课之余一直如此辛勤的回帖解答我们的困惑；谢谢老师。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/ca/02b0e397.jpg" width="30px"><span>fomy</span> 👍（0） 💬（1）<div>1、为什么ServiceState变量不设置成volatile呢？
2、消费者MessageQueue(readQueueNums)怎么和生产者MessageQueue(writeQueueNums)关联起来的呢？比如readQueueNums=19个，writeQueueNums=23个，它们是怎么关联的呢？</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（1）<div>DefaultMQProducerImpl的start和shutdown方法没有加同步，serviceState也只是一个普通成员变量没加volatile，不会有线程安全问题吗？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（1）<div>看了Rocketmq producer源码，关于producer这块有个疑问不知道能否请教下？就是producer启动过程中为什么MQClientInstance mQClientFactory.start()这个方法需要被执行2次？2次的作用分别是什么？</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（0） 💬（1）<div>老师，节日快乐🎉</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/18/393a841d.jpg" width="30px"><span>付永强</span> 👍（0） 💬（1）<div>教师节快乐！</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（0） 💬（1）<div>教师节，老师们都辛苦了！</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（0） 💬（1）<div>一定要学java吗 老师</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（20） 💬（8）<div>这种异步方式几乎没有意义，底层的netty已经实现了异步，这里只是在选择消息队列等判断的过程加了异步，最终callback还是由netty线程来调用的</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（6） 💬（0）<div>我总结的kafka生产消息的源码分析
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;-s34_y16HU6HR5HDsSD4bg</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/8d/09f28606.jpg" width="30px"><span>明日</span> 👍（4） 💬（0）<div>李老师节日快乐！
关于思考题看到了源码的注释说异常处理和超时时间有问题。
自己看的话一是异常这里抛未知的原因，不够明确。
二是这里用的线程池默认使用了虚拟机可用的线程，可能会对其他服务造成影响。
三是超时时间这把线程阻塞可能等待的时间也包括进去了不太合适。
感觉代码层次使用老师说过的completablefuture处理更优雅。另外底层使用了netty，应该直接用异步io就行了吧。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/de/9649fcee.jpg" width="30px"><span>侧面</span> 👍（2） 💬（0）<div>有这篇这课就买的值了</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/45/0c474d47.jpg" width="30px"><span>二少</span> 👍（1） 💬（0）<div>DefaultMQProducer是DefaultMQProducerImpl的门面，但二者的类名起得有点怪怪的感觉。类名有Impl后缀，一般都表示这个类是某个接口的实现类，但实际上却是门面和被包装类的关系。而且把门面类给个facade后缀不是更适当一些吗？大家怎么看。</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（1） 💬（0）<div>因为Netty本身就支持异步的写入消息,并注入Listener,这一步的发送,则是利用Nio的WorkGroup,这种情况下,显式的使用线程池异步的发送显得有点多余</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/c9/9f51fd27.jpg" width="30px"><span>编程界的小学生</span> 👍（1） 💬（0）<div>RocketMQ同等的策略模式还有消费端的时候选择消费者与queue的对应策略：
AllocateMessageQueueStrategy接口下有如下几个实现类
AllocateMessageQueueAveragely
AllocateMachineRoomNearby
AllocateMessageQueueAveragelyByCircle
AllocateMessageQueueByConfig：这个策略真不知道有啥鸟用
AllocateMessageQueueByMachineRoom
AllocateMessageQueueConsistentHash
而且看这名字就知道是策略模式。直接以Strategy结尾。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/b4/abb7bfe3.jpg" width="30px"><span>Geek_6ank0y</span> 👍（1） 💬（0）<div>跟踪源码发现，异步回调，最后还是在NettyRemotingAbstract中启动线程池做了    
&#47;**
     * Execute callback in callback executor. If callback executor is null, run directly in current thread
     *&#47;
    private void executeInvokeCallback(final ResponseFuture responseFuture) {
        boolean runInThisThread = false;
        ExecutorService executor = this.getCallbackExecutor();
        if (executor != null) {
            try {
                executor.submit(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            responseFuture.executeInvokeCallback();
                        } catch (Throwable e) {
                            log.warn(&quot;execute callback in executor exception, and callback throw&quot;, e);
                        } finally {
                            responseFuture.release();
                        }
                    }
                });
            } catch (Exception e) {
                runInThisThread = true;
                log.warn(&quot;execute callback in executor exception, maybe executor busy&quot;, e);
            }
        } else {
            runInThisThread = true;
        }

        if (runInThisThread) {
            try {
                responseFuture.executeInvokeCallback();
            } catch (Throwable e) {
                log.warn(&quot;executeInvokeCallback Exception&quot;, e);
            } finally {
                responseFuture.release();
            }
        }
    }</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（1） 💬（0）<div>1. 异常处理问题：线程内部抛出的异常，比如MQBrokerException，客户端无法感知到，以为发送成功，会继续执行。
2. 超时时间的概念问题：这里似乎去掉了线程调度的时间，将剩下的时间给了netty，个人感觉也应该包含进去。对客户端而言，调度是自己的事，不应包含在网络超时时间里。

请老师指正。</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/09/b7f0eac6.jpg" width="30px"><span>谁都会变</span> 👍（0） 💬（0）<div>消息生产者启动拉取消息这个感觉没什么用啊，它不是推送消息得吗？
</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c0/4f/db7f2ab2.jpg" width="30px"><span>七楼</span> 👍（0） 💬（1）<div>mvc框架的 controller也算是门面模式的门面把？他也是提供一个可访问系统的借口  隐藏了系统内部的复杂性  对吗</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（0） 💬（0）<div>老师请教问题：RocketMQ有个DefaultMQPullConsumer和DefaultMQPushConsumer，这两个类到底是干嘛的，它们到底什么关系？</div>2019-11-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（0） 💬（0）<div>老师，辛苦了，能否讲讲发送端如何找到broker上的文件，队列和文件的关系，消息都放到文件上吧，能否展开梳理梳理，不然还是不懂怎么实现的</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（0） 💬（0）<div>这里使用异步主要是提升消息发送的吞吐量，而在这过程中影响吞吐的有两个：磁盘IO和网络IO，而现在的这种异步方式好像并没有为这两部分设计详细的优化，似乎只是简单用了一个多线程去执行各自的操作，也就是并没有对真正的性能短板做优化。我觉得真要是异步的话，需要在这里维持一个队列、一个磁盘IO选择器和一个网络发送IO选择器，真正异步的点应该是两个选择器加并发协调处理待发送的数据。不过就像有些同学评价的，netty底层对各种IO已经做了很好的支持，这里的异步就显得很苍白无力了。不知netty是怎么设计异步来达到极致的性能的。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（0）<div>一是处理异常的代码很奇怪吧，有的异常使用sendCallback抛出，有的直接抛出；二是超时的语义有问题，现在的timeout意思是消息在线程池中排队的时间</div>2019-09-16</li><br/>
</ul>