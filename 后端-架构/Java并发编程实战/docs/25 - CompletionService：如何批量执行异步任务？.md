在[《23 | Future：如何用多线程实现最优的“烧水泡茶”程序？》](https://time.geekbang.org/column/article/91292)的最后，我给你留了道思考题，如何优化一个询价应用的核心代码？如果采用“ThreadPoolExecutor+Future”的方案，你的优化结果很可能是下面示例代码这样：用三个线程异步执行询价，通过三次调用Future的get()方法获取询价结果，之后将询价结果保存在数据库中。

```
// 创建线程池
ExecutorService executor =
  Executors.newFixedThreadPool(3);
// 异步向电商S1询价
Future<Integer> f1 = 
  executor.submit(
    ()->getPriceByS1());
// 异步向电商S2询价
Future<Integer> f2 = 
  executor.submit(
    ()->getPriceByS2());
// 异步向电商S3询价
Future<Integer> f3 = 
  executor.submit(
    ()->getPriceByS3());
    
// 获取电商S1报价并保存
r=f1.get();
executor.execute(()->save(r));
  
// 获取电商S2报价并保存
r=f2.get();
executor.execute(()->save(r));
  
// 获取电商S3报价并保存  
r=f3.get();
executor.execute(()->save(r));

```

上面的这个方案本身没有太大问题，但是有个地方的处理需要你注意，那就是如果获取电商S1报价的耗时很长，那么即便获取电商S2报价的耗时很短，也无法让保存S2报价的操作先执行，因为这个主线程都阻塞在了 `f1.get()` 操作上。这点小瑕疵你该如何解决呢？

估计你已经想到了，增加一个阻塞队列，获取到S1、S2、S3的报价都进入阻塞队列，然后在主线程中消费阻塞队列，这样就能保证先获取到的报价先保存到数据库了。下面的示例代码展示了如何利用阻塞队列实现先获取到的报价先保存到数据库。

```
// 创建阻塞队列
BlockingQueue<Integer> bq =
  new LinkedBlockingQueue<>();
//电商S1报价异步进入阻塞队列  
executor.execute(()->
  bq.put(f1.get()));
//电商S2报价异步进入阻塞队列  
executor.execute(()->
  bq.put(f2.get()));
//电商S3报价异步进入阻塞队列  
executor.execute(()->
  bq.put(f3.get()));
//异步保存所有报价  
for (int i=0; i<3; i++) {
  Integer r = bq.take();
  executor.execute(()->save(r));
}  
```

## 利用CompletionService实现询价系统

不过在实际项目中，并不建议你这样做，因为Java SDK并发包里已经提供了设计精良的CompletionService。利用CompletionService不但能帮你解决先获取到的报价先保存到数据库的问题，而且还能让代码更简练。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（139） 💬（11）<div>我觉得问题出在return m这里需要等待三个线程执行完成，但是并没有。
...
AtomicReference&lt;Integer&gt; m = new AtomicReference&lt;&gt;(Integer.MAX_VALUE);
CountDownLatch latch = new CountDownLatch(3);
for(int i=0; i&lt;3; i++) {
	executor.execute(()-&gt;{
		Integer r = null;
		try {
			r = cs.take().get();
		} catch(Exception e) {}
		save(r);
		m.set(Integer.min(m.get(), r));
		latch.countDown();
	});
	latch.await();
	return m;
}</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/ab/facff632.jpg" width="30px"><span>小华</span> 👍（33） 💬（1）<div>看老师的意图是要等三个比较报假的线程都执行完才能执行主线程的的return  m，但是代码无法保证三个线程都执行完，和主线程执行return的顺序，因此，m的值不是准确的，可以加个线程栈栏，线程执行完计数器，来达到这效果</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/00/c4/634c1e10.jpg" width="30px"><span>西行寺咕哒子</span> 👍（31） 💬（8）<div>试过返回值是2147483647，也就是int的最大值。没有等待操作完成就猴急的返回了。 m.set(Integer.min(m.get(), r)... 这个操作也不是原子操作。
试着自己弄了一下：
public Integer run(){
        &#47;&#47; 创建线程池
        ExecutorService executor = Executors.newFixedThreadPool(3);
        &#47;&#47; 创建 CompletionService
        CompletionService&lt;Integer&gt; cs = new ExecutorCompletionService&lt;&gt;(executor);
        AtomicReference&lt;Integer&gt; m = new AtomicReference&lt;&gt;(Integer.MAX_VALUE);
        &#47;&#47; 异步向电商 S1 询价
        cs.submit(()-&gt;getPriceByS1());
        &#47;&#47; 异步向电商 S2 询价
        cs.submit(()-&gt;getPriceByS2());
        &#47;&#47; 异步向电商 S3 询价
        cs.submit(()-&gt;getPriceByS3());
        &#47;&#47; 将询价结果异步保存到数据库
        &#47;&#47; 并计算最低报价
        for (int i=0; i&lt;3; i++) {
            Integer r = logIfError(()-&gt;cs.take().get());
            executor.execute(()-&gt; save(r));
            m.getAndUpdate(v-&gt;Integer.min(v, r));
        }
        return m.get();
    }
不知道可不可行</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/fc/d1dd57dd.jpg" width="30px"><span>ipofss</span> 👍（17） 💬（2）<div>老师，并发工具类，这整个一章，感觉听完似懂非懂的，因为实践中没用过，我要如何弥补这部分，还是说只要听说过，然后用的时候再去查看demo吗</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（8） 💬（1）<div>老师stampedLock的获取锁源码，老师能帮忙解惑下么？阻塞的读线程cowait是挂在写节点的下方么？老师能解惑下基于的理论模型
private long acquireWrite(boolean interruptible, long deadline) {
        WNode node = null, p;
        for (int spins = -1;;) { &#47;&#47; spin while enqueuing
            long m, s, ns;
            &#47;&#47;如果当前的state是无锁状态即100000000
            if ((m = (s = state) &amp; ABITS) == 0L) {
            	&#47;&#47;设置成写锁
                if (U.compareAndSwapLong(this, STATE, s, ns = s + WBIT))
                    return ns;
            }
            else if (spins &lt; 0)
            	&#47;&#47;当前锁状态为写锁状态，并且队列为空，设置自旋值
                spins = (m == WBIT &amp;&amp; wtail == whead) ? SPINS : 0;
            else if (spins &gt; 0) {
            	&#47;&#47;自旋操作，就是让线程在此自旋
                if (LockSupport.nextSecondarySeed() &gt;= 0)
                    --spins;
            }
            &#47;&#47;如果队列尾元素为空，初始化队列
            else if ((p = wtail) == null) { &#47;&#47; initialize queue
                WNode hd = new WNode(WMODE, null);
                if (U.compareAndSwapObject(this, WHEAD, null, hd))
                    wtail = hd;
            }
            &#47;&#47;当前要加入的元素为空，初始化当前元素，前置节点为尾节点
            else if (node == null)
                node = new WNode(WMODE, p);
            &#47;&#47;队列的稳定性判断，当前的前置节点是否改变，重新设置    
            else if (node.prev != p)
                node.prev = p;
            &#47;&#47;将当前节点加入尾节点中    
            else if (U.compareAndSwapObject(this, WTAIL, p, node)) {
                p.next = node;
                break;
            }
        }

        </div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7c/b5/4a7a2bd4.jpg" width="30px"><span>Sunqc</span> 👍（3） 💬（1）<div>&#47;&#47; 获取电商 S1 报价并保存
r=f1.get();
executor.execute(()-&gt;save(r));

如果把r=f1.get（）放进execute里应该是也能保证先执行完的先保存</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（3） 💬（1）<div>我实际测试了第一段代码，确实是异步的，f1.get不会阻塞主线程。。。

public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(3);
        Future&lt;Integer&gt; f1 = executor.submit(()-&gt;getPriceByS1());
        Future&lt;Integer&gt; f2 = executor.submit(()-&gt;getPriceByS2());
        Future&lt;Integer&gt; f3 = executor.submit(()-&gt;getPriceByS3());

        executor.execute(()-&gt; {
            try {
                save(f1.get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        });
        executor.execute(()-&gt; {
            try {
                save(f2.get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        });
        executor.execute(()-&gt; {
            try {
                save(f3.get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        });
    }

    private static Integer getPriceByS1() {
        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return 1;
    }
    private static Integer getPriceByS2() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return 2;
    }
    private static Integer getPriceByS3() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return 3;
    }
    private static void save(Integer i) {
        System.out.println(&quot;save &quot; + i);
    }</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/ac/9cc5e692.jpg" width="30px"><span>Corner</span> 👍（3） 💬（1）<div>1.AtomicReference&lt;Integer&gt;的get方法应该改成使用cas方法
2.最后筛选最小结果的任务是异步执行的，应该在return之前做同步，所以最好使用sumit提交该任务便于判断任务的完成
最后请教老师一下，第一个例子中为什么主线程会阻塞在f1.get()方法呢？</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/3a/76dbbd0e.jpg" width="30px"><span>空空空空</span> 👍（2） 💬（1）<div>算低价的时候是用三个不同的线程去计算，是异步的，因此可能算出来并不是预期的结果
老师，这样理解对吗？</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/23/d722d6ec.jpg" width="30px"><span>梅小西</span> 👍（1） 💬（1）<div>老师讲的挺不错的，看了这个例子，有几点疑问，还希望老师说明下：
&#47;&#47; 这个是老师例子：

&#47;&#47; 创建线程池
ExecutorService executor = 
  Executors.newFixedThreadPool(3);
&#47;&#47; 创建CompletionService
CompletionService&lt;Integer&gt; cs = new 
  ExecutorCompletionService&lt;&gt;(executor);
&#47;&#47; 异步向电商S1询价
cs.submit(()-&gt;getPriceByS1());
&#47;&#47; 异步向电商S2询价
cs.submit(()-&gt;getPriceByS2());
&#47;&#47; 异步向电商S3询价
cs.submit(()-&gt;getPriceByS3());
&#47;&#47; 将询价结果异步保存到数据库
for (int i=0; i&lt;3; i++) {
  Integer r = cs.take().get();
  executor.execute(()-&gt;save(r));
}

首先，CompletionService应该是要绑定泛型，代表异步任务的返回结果，实际应用中，几乎不太可能所有的异步任务的返回类型是一样的，除非设置成Object这种通用型，那又会导致拿到结果后需要强转，代码看起来更难受；
其次，对于返回的结果的处理方式，实际应用中几乎也是不同的，那就要针对每一个take出来的结果做判断，这实际上也是会导致代码很难维护；

综上，CompletionService 看来能够做批量处理异步任务的事情，实际应用中，我感觉不太实用！

以上两点是个人见解，有不对之处请老师指教！</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/ca/ea85bfdd.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>老师，冒昧的问下：在文章刚开始的例子，无论是三个询价任务（通过submit方法提交），还是保存询价任务（通过execute方法提交）都是异步的执行执行的啊！如果s1询价的时间过长的话，也不会影响到s2保存保价的先执行啊！他只影响到s1保存询价的动作。老师不知道我说的有么有道理，有问题请老师帮忙指正</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（1） 💬（1）<div>&#47;&#47; 创建线程池
ExecutorService executor =
  Executors.newFixedThreadPool(3);
&#47;&#47; 创建 CompletionService
CompletionService&lt;Integer&gt; cs =
  new ExecutorCompletionService&lt;&gt;(executor);
&#47;&#47; 用于保存 Future 对象
List&lt;Future&lt;Integer&gt;&gt; futures =
  new ArrayList&lt;&gt;(3);
&#47;&#47; 提交异步任务，并保存 future 到 futures 
futures.add(
  cs.submit(()-&gt;geocoderByS1()));
futures.add(
  cs.submit(()-&gt;geocoderByS2()));
futures.add(
  cs.submit(()-&gt;geocoderByS3()));
&#47;&#47; 获取最快返回的任务执行结果
Integer r = 0;
try {
  &#47;&#47; 只要有一个成功返回，则 break
  for (int i = 0; i &lt; 3; ++i) {
    r = cs.take().get();
    &#47;&#47; 简单地通过判空来检查是否成功返回
    if (r != null) {
      break;
    }
  }
  &#47;&#47; **********************************
  &#47;&#47; for 循环其实没有必要吧？
  &#47;&#47; take() 是阻塞的拿到结果，get()也是阻塞的
  &#47;&#47; 只要有个任务完成，这个for循环就结束了
} finally {
  &#47;&#47; 取消所有任务
  for(Future&lt;Integer&gt; f : futures)
    f.cancel(true);
}
&#47;&#47; 返回结果
return r;
</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（0） 💬（1）<div>老师，那个futures保存future就是为了后面取消(`cancel()`)，对吧</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e5/a5/fae40ac3.jpg" width="30px"><span>倚梦流</span> 👍（0） 💬（1）<div>请问老师，任务操作中包含io操作，比如正在增删读写文件，这时候突然cancel，会有什么不良影响吗？或者任务里面包含数据库操作，如果突然cancel，岂不是需要在异步任务中，进行事务回滚？</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（0） 💬（1）<div>请教下老师，实际生产中，使用BlockingQueue 时，
若重启实例，BQ 的任务可能会丢，对此有何通用方案？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/eb/8bfd69b0.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>想问下，老师第二个例子里 cs.submit 返回的future 和 cs.take 获取的是同样的future吗 为什么还要加一个数组这个多余的东西啊</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/1e/51ad425f.jpg" width="30px"><span>tdytaylor</span> 👍（0） 💬（1）<div>老师，我看到几节中的demo都有在线程池里面取消任务执行，我之前看源码了解到，调用cancel时，如果线程已经在执行任务了，是没得办法终止这个任务的运行的，这种情况有没办法处理呢</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/58/008173ad.jpg" width="30px"><span>punchline</span> 👍（0） 💬（1）<div>这一期的评论把我看懵了，future.get()就是阻塞当前线程啊</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（0） 💬（1）<div>老师我对第一个例子还是有疑问，f.get()已经提交给了线程池执行了，为什么会说阻塞主线程呢？</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（0） 💬（1）<div>老师,感觉开篇的阻塞队列解决future.get阻塞 存在问题,阻塞队列也是把执行get结果加到队列,然后take出来,如果线程池不够大, f1的submit 和 get占满了线程,其他线程的执行都需要等待...还是会阻塞
如果线程池足够大,原始方案就可以直接申请新的线程执行</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（0） 💬（1）<div>1.m.set(Integer.min(m.get(), r))不是原子操作
2.catch住exception后，是否需要给r一个默认值呢
3.return 等不到异步结果

另外我有1个问题
我觉得第一个例子后面3个线程异步保存，不应该阻塞在f1.get，get方法会阻塞，但是只阻塞当前线程啊

</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（0） 💬（1）<div>第一个例子 我感觉f1.get()没有阻塞主线程啊  f1.get()是在线程池里异步执行的啊</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（0） 💬（1）<div>老师，有个地方不理解。。第一段代码中这个f1.get不是在线程池里执行的吗？为何会阻塞了主线程？

&#47;&#47;获取电商 S1 报价并异步保存
executor.execute(
  ()-&gt;save(f1.get()));</div>2019-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKR3ibELhjgVicCNShZCBwvaDxibnzibggG4wUzVkS2mkDxUBZyIs87nDEdJ7PiahJBVoZcuhQ84RxAziag/132" width="30px"><span>周治慧</span> 👍（0） 💬（1）<div>存在问题，在执行executor.execute的时候多个线程是非阻塞的异步执行，可能还没等到线程执行完的时候就直接返回结果了，大部分情况会出现是integer的最大值。改进的办法是在遍历时去取阻塞队列中的值后再执行set操作，因为在get取阻塞队列中的值的过程是一个阻塞，最后在利用线程池的非阻塞异步操作去保存结果。</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（22） 💬（1）<div>m.get()和m.set()不是原子性操作，正确代码是:do{int expect = m.get();int min= Integer.min(expect,r);}while(!m.compareAndSet(expect,min))。老师，是这样吗？</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/27/8b72141c.jpg" width="30px"><span>天涯煮酒</span> 👍（6） 💬（1）<div>先调用m.get()并跟r比较，再调用m.set()，这里存在竞态条件，线程并不安全</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ea/fd/89d3d0b5.jpg" width="30px"><span>王昊哲</span> 👍（5） 💬（3）<div>有个疑问：老师也提到那种线程池+阻塞队列实现方式，队列里保存的是任务的结果，而completionService保存的future，那completionService的future拿出来get的时候，也阻塞在get那里了啊，那不跟跟线程池+future的实现一样的弊端了啊？</div>2019-11-28</li><br/><li><img src="" width="30px"><span>一眼万年</span> 👍（5） 💬（3）<div>课后思考如果需要等待最小结果，本来就有阻塞队列了，加了个线程池，评论还要加上栏栅，那除了炫技没啥作用</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/93/098e5ef5.jpg" width="30px"><span>海鸿</span> 👍（4） 💬（0）<div>重新发过，刚刚的代码有误！
1.for循环线程池执行属于异步导致未等比价结果就 return了，需要等待三次比价结果才能 return，可以用 CountDownLatch
2. m. set( Integer. min( m. get(), r))存在竞态条件，可以更改为 
Integer o; 
do{ 
o= m. get(); 
if(o&lt;=r){ break;}
} 
while(! m. compareAndSet( o, r));
3.还有一个小问题就是 try- catch捕获异常后的处理，提高程序鲁棒性</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/8e/cf0b4575.jpg" width="30px"><span>郑晨Cc</span> 👍（4） 💬（0）<div>executor.execute（Callable）提交任务是非阻塞的 return m；很大概率返回 Integer.Maxvalue，而且老师为了确保返回这个max还特意加入了save这个阻塞的方法</div>2019-04-25</li><br/>
</ul>