在上一篇文章中，我们讲到Java SDK并发包里的Lock有别于synchronized隐式锁的三个特性：能够响应中断、支持超时和非阻塞地获取锁。那今天我们接着再来详细聊聊Java SDK并发包里的Condition，**Condition实现了管程模型里面的条件变量**。

在[《08 | 管程：并发编程的万能钥匙》](https://time.geekbang.org/column/article/86089)里我们提到过Java 语言内置的管程里只有一个条件变量，而Lock&amp;Condition实现的管程是支持多个条件变量的，这是二者的一个重要区别。

在很多并发场景下，支持多个条件变量能够让我们的并发程序可读性更好，实现起来也更容易。例如，实现一个阻塞队列，就需要两个条件变量。

**那如何利用两个条件变量快速实现阻塞队列呢？**

一个阻塞队列，需要两个条件变量，一个是队列不空（空队列不允许出队），另一个是队列不满（队列已满不允许入队），这个例子我们前面在介绍[管程](https://time.geekbang.org/column/article/86089)的时候详细说过，这里就不再赘述。相关的代码，我这里重新列了出来，你可以温故知新一下。

```
public class BlockedQueue<T>{
  final Lock lock =
    new ReentrantLock();
  // 条件变量：队列不满  
  final Condition notFull =
    lock.newCondition();
  // 条件变量：队列不空  
  final Condition notEmpty =
    lock.newCondition();

  // 入队
  void enq(T x) {
    lock.lock();
    try {
      while (队列已满){
        // 等待队列不满
        notFull.await();
      }  
      // 省略入队操作...
      //入队后,通知可出队
      notEmpty.signal();
    }finally {
      lock.unlock();
    }
  }
  // 出队
  void deq(){
    lock.lock();
    try {
      while (队列已空){
        // 等待队列不空
        notEmpty.await();
      }  
      // 省略出队操作...
      //出队后，通知可入队
      notFull.signal();
    }finally {
      lock.unlock();
    }  
  }
}
```

不过，这里你需要注意，Lock和Condition实现的管程，**线程等待和通知需要调用await()、signal()、signalAll()**，它们的语义和wait()、notify()、notifyAll()是相同的。但是不一样的是，Lock&amp;Condition实现的管程里只能使用前面的await()、signal()、signalAll()，而后面的wait()、notify()、notifyAll()只有在synchronized实现的管程里才能使用。如果一不小心在Lock&amp;Condition实现的管程里调用了wait()、notify()、notifyAll()，那程序可就彻底玩儿完了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/3b/a1f7e3a4.jpg" width="30px"><span>ZOU志伟</span> 👍（164） 💬（20）<div>不合理，会导致很多请求超时，看了源码是调用signalAll()</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（112） 💬（13）<div>我理解异步的本质是利用多线程提升性能，异步一定是基于一个新开的线程，从调用线程来看是异步的，但是从新开的那个线程来看，正是同步（等待）的，只是对于调用方而言这种同步是透明的。正所谓生活哪有什么岁月静好，只是有人替你负重前行。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（50） 💬（1）<div>in the method of org.apache.dubbo.remoting.exchange.support.DefaultFuture#doReceived, I think we should call done.signalAll() instead of done.signal() ,and it&#39;s unnecessary to check done != null because it&#39;s always true</div>2019-04-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotuhVFN9phZnUxxXueAm8rDDibjIkj0L8W7VojYRpSeXwHtDSgLW3SdrNjMQy0AcOUuMmTAQSyO3g/132" width="30px"><span>Geek_e6f3ec</span> 👍（20） 💬（4）<div>老师关于dubbo源码的执行流程有一点疑问。
以下是源码
&#47;&#47; 调用通过该方法等待结果
Object get(int timeout){
        long start = System.nanoTime();
        lock.lock();
        try{
            while (!isDone()){
                done.wait(timeout);   &#47;&#47; 在这里调用了等待方法后面的代码还能执行吗？  我理解的管程，是在条件变量等待队列中阻塞等待，被唤醒之后也不是马上执行也要去管程入口等待队列，也就是lock.lock处等待获取锁。 老师是这样的吗？
                long cur = System.nanoTime();
                if (isDone()||cur-start&gt; timeout){
                    break;
                }
            }
        }finally {
            lock.unlock();
        }
        return returnFromResponse();

    }

 



</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/36/972f7abf.jpg" width="30px"><span>木刻</span> 👍（18） 💬（1）<div>老师今天提到异步转同步，让我想到这两天看的zookeeper客户端源码，感觉应该也是这个机制，客户端同步模式下发送请求后会执行packet.wait，收到服务端响应后执行packet.notifyAll</div>2019-04-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/90ZCAwGj0kaicic73wdrqeTicuYbPVib7biczdVC4KiaAKhp5L1eFqzXXyN2y9PoqVfVpFhcM9cnf5Vz7lrv0gaSySfA/132" width="30px"><span>苏格拉底23</span> 👍（14） 💬（2）<div>老师您好！

有一个基本的问题不明白，如果每个request对应一个线程，似乎并没有用到共享的资源，那么为什么要加锁呢？</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（8） 💬（2）<div>老师，求指教
DefaultFuturewhile这个类为什么要加 while(!isDone()) 这个条件，我看代码while里面加了done.await(timeout);是支持超时的，就是说设置5秒超时， if (isDone() || cur-start &gt; timeout){，只要超过没有被signal()唤醒，那5秒就会自动唤醒，这时候就会在if (isDone() || cur-start &gt; timeout){ 被校验通过，从而break，退出。这时候在加个while条件是不是没必要。
还是说加个while条件是因为时间到点的时候自动唤醒后，Response可能是空，而且时间cur-start &gt; timeout 不超时，所以才有必要进行while再一次判断isDone()是否有值。</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/72/7f/5da093c5.jpg" width="30px"><span>水目沾</span> 👍（7） 💬（1）<div>这是一对一的关系，肯定只需要 signal。每个线程都是相互独立的，lock 和 condition 也是各自独享的。</div>2019-04-02</li><br/><li><img src="" width="30px"><span>ycfHH</span> 👍（5） 💬（3）<div>作为一个完全不懂dubbo的新人，我很好奇是什么bug能让signal改成signalAll,因为不管怎么看都感觉signal就已经可以了啊(虽然使用signalall也不错)</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/ed/b2fc0e7c.jpg" width="30px"><span>7</span> 👍（5） 💬（1）<div>老师，有个疑问
为什么要判断done!=null呢？这个条件不是永远为true吗。</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/96/5160cd31.jpg" width="30px"><span>阿甘</span> 👍（3） 💬（2）<div>看了最新的DefaultFuture，已经去掉了lock，老师能分析下最新实现的原理吗</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/78/f011d586.jpg" width="30px"><span>遇见阳光</span> 👍（3） 💬（1）<div>老师，我想问下locksupport与此处用lock来阻塞调用者线程有什么区别</div>2019-04-05</li><br/><li><img src="" width="30px"><span>sibyl</span> 👍（2） 💬（1）<div>动手实现阻塞队列时，一定注意synchronized&#47;wait&#47;notify ， Lock&#47;Condition&#47;await&#47;signal的组合！ 

我在实现时，同时用了Lock和notify，一直报错IllegalMonitorStateException，该异常表示没加锁，而norify要求的锁必须是synchronized的锁，的确notify必须在synchronized临界区中使用，这是才加synchronized锁的！！！</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（2） 💬（1）<div>TCP 协议本身就是异步的，我们工作中经常用到的 RPC 调用，在 TCP 协议层面，发送完 RPC 请求后，线程是不会等待 RPC 的响应结果的。
-------------
老师，我也有类似的疑问，如果说TCP都是异步的，那么我们平时用的各种httpClient的sdk开发，它们也做了异步转同步的事情？</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7b/ea/a64f7822.jpg" width="30px"><span>yc</span> 👍（2） 💬（2）<div>请问老师，阻塞队列的实现，入队和出队都要先获取锁，如果有一个线程正在入队同时又有一个线程在出队，是不是只有一个线程能拿到锁从而成功操作，另一个需要灯unlock，那么入队和出队就是串行了；又或者有两个线程同时入队，也是只有一个线程能够拿到锁从而成功执行入队，另一个线程需要等unlock，也是变成串行了。这样不会影响效率吗？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/68/9a/791d0f5e.jpg" width="30px"><span>scp</span> 👍（2） 💬（2）<div>老师，jdk已经实现了Future去把异步转换为同步，我们直接使用get()方法就会让线程阻塞的获取线程执行结果，为什么dubbo还要自己实现MESA模型，不太理解。业务中不知道什么时候该用这个模型</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/89/e1621a01.jpg" width="30px"><span>zhangtnty</span> 👍（2） 💬（1）<div>合理，等待条件都是response不空，等到通知后的动作都是返回response,也是通知一个线程。
老师，您在文中提到，子线程和新线程，代码上怎么区分呢？我认为在main中new thread,即使立刻返回main,也得在new thread之后。这是子线程还是新线程呢？</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（1） 💬（1）<div>老师 有个问题 condition 这个 如果我每次都调用入队 直到看了 入队线程阻塞，此时我在调用出队，但是lock被入队线程获取了已经，因此出队线程就会阻塞，这样不就死锁了嘛？ 这个程序是不是有问题</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/ff/6201122c.jpg" width="30px"><span>Geek_89bbab</span> 👍（1） 💬（1）<div>引用：
`
当 RPC 返回结果之前，阻塞调用线程，让调用线程等待；当 RPC 返回结果后，唤醒调用线程，让调用线程重新执行。
`
请问老师，这里线程等待是否影响了并发呢？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/58/2468a5e9.jpg" width="30px"><span>JGOS</span> 👍（1） 💬（2）<div>老师,在进入等待之前的为什么都是用while()进行判断啊, await和wait方法不是讲持有锁的线程挂起吗,为什么不用if做判断啊</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bc/6d/f6f0a442.jpg" width="30px"><span>汤小高</span> 👍（0） 💬（1）<div>老师能说下为啥TCP是异步的吗？</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/96/beb89790.jpg" width="30px"><span>hl</span> 👍（0） 💬（1）<div>如果是公平锁的话，signal和signal all还是一样吗？</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/b0/b52d9ade.jpg" width="30px"><span>苏彧</span> 👍（0） 💬（2）<div>老师，为什么异步要转成同步呢
</div>2021-08-09</li><br/><li><img src="" width="30px"><span>尼糯米</span> 👍（0） 💬（1）<div>最近在了解CompletableFuture，然后就接触dubbo2.7版本引入的CompletableFuture，然后就想到这里的DefaultFuture，发现这里的内容都忘了，这个怎么办呢？</div>2020-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKvNozkiaiao1I945xyUGC0vXZSnibImBPbf7CtibqKoGDsbmZGnia62zibv4s3grqtVllO82tILEJ1Dh2w/132" width="30px"><span>惊蛰</span> 👍（0） 💬（1）<div>老师好，在 TCP 协议层面，发送完 RPC 请求后，线程是不会等待 RPC 的响应结果的。 这句话能理解成‘ tcp 协议本身是异步的么’？</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/f8/24fcccea.jpg" width="30px"><span>💢 星星💢</span> 👍（0） 💬（1）<div>老师。为啥不用synchronzied实现阻塞队列呀。而且代码好像还更简洁。</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/78/23c56bce.jpg" width="30px"><span>james</span> 👍（0） 💬（2）<div>notFull 和 notEmpty 让人很晕 改成 canEnq 和 canDeq 更好懂</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/b2/3fb9a4a1.jpg" width="30px"><span>招财</span> 👍（0） 💬（1）<div>老师，这个读锁，就是可以让很多个线程可以访问他，那我只加写锁，不加读锁可以吗？感觉读锁，好像并没有什么用呢</div>2019-06-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qqPULdMQxtY3hv1hyuyaHgzGulEoo8q1KaSWnllp6I7OzK6pZpy7ujtmrtavVVcsicibWWjKicnqd5vugiczj5XFqQ/132" width="30px"><span>Just</span> 👍（0） 💬（1）<div>signal替换为 signalall 是在哪个版本呢，我没找到区别，还是使用了其他方式替代

</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/27/8b72141c.jpg" width="30px"><span>天涯煮酒</span> 👍（45） 💬（9）<div>合理。

每个rpc请求都会占用一个线程并产生一个新的DefaultFuture实例，它们的lock&amp;condition是不同的，并没有竞争关系

这里的lock&amp;condition是用来做异步转同步的，使get()方法不必等待timeout那么久，用得很巧妙</div>2019-04-02</li><br/>
</ul>