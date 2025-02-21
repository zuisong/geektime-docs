在上一篇文章[《22 | Executor与线程池：如何创建正确的线程池？》](https://time.geekbang.org/column/article/90771)中，我们详细介绍了如何创建正确的线程池，那创建完线程池，我们该如何使用呢？在上一篇文章中，我们仅仅介绍了ThreadPoolExecutor的 `void execute(Runnable command)` 方法，利用这个方法虽然可以提交任务，但是却没有办法获取任务的执行结果（execute()方法没有返回值）。而很多场景下，我们又都是需要获取任务的执行结果的。那ThreadPoolExecutor是否提供了相关功能呢？必须的，这么重要的功能当然需要提供了。

下面我们就来介绍一下使用ThreadPoolExecutor的时候，如何获取任务执行结果。

## 如何获取任务执行结果

Java通过ThreadPoolExecutor提供的3个submit()方法和1个FutureTask工具类来支持获得任务执行结果的需求。下面我们先来介绍这3个submit()方法，这3个方法的方法签名如下。

```
// 提交Runnable任务
Future<?> 
  submit(Runnable task);
// 提交Callable任务
<T> Future<T> 
  submit(Callable<T> task);
// 提交Runnable任务及结果引用  
<T> Future<T> 
  submit(Runnable task, T result);
```

你会发现它们的返回值都是Future接口，Future接口有5个方法，我都列在下面了，它们分别是**取消任务的方法cancel()、判断任务是否已取消的方法isCancelled()、判断任务是否已结束的方法isDone()以及2个获得任务执行结果的get()和get(timeout, unit)**，其中最后一个get(timeout, unit)支持超时机制。通过Future接口的这5个方法你会发现，我们提交的任务不但能够获取任务执行结果，还可以取消任务。不过需要注意的是：这两个get()方法都是阻塞式的，如果被调用的时候，任务还没有执行完，那么调用get()方法的线程会阻塞，直到任务执行完才会被唤醒。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（107） 💬（14）<div>建议并发编程课程中的Demo代码，尽量少使用System.out.println, 因为其实现有使用隐式锁，一些情况还会有锁粗化产生</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（19） 💬（5）<div>```java
ExecutorService futuresPool = Executors.newFixedThreadPool(3);
        Future&lt;Price&gt; future1 = futuresPool.submit(this::getPriceByS1);
        Future&lt;Price&gt; future2 = futuresPool.submit(this::getPriceByS2);
        Future&lt;Price&gt; future3 = futuresPool.submit(this::getPriceByS3);

        ExecutorService saveThreadPool = Executors.newFixedThreadPool(3);
        saveThreadPool.execute(() -&gt; {
            try {
                Price r1= future1.get();
                save(r1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }

        });
        saveThreadPool.execute(() -&gt; {
            try {
                Price r2= future2.get();
                save(r2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }

        });
        saveThreadPool.execute(() -&gt; {
            try {
                Price r3= future3.get();
                save(r3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        });
```

用三个线程把这个并行执行，麻烦老师看看，谢谢</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（10） 💬（4）<div>我不知道是不是理解错老师意思了，先分析依赖有向图，可以看到三条线，没有入度&gt;1的节点
那么启动三个线程即可。
图：
s1询价 -&gt; s1保存  
s2询价 -&gt; s2保存
s3询价 -&gt; s3保存  
代码：
        new Thread(() -&gt; {
        	r1 = getPriceByS1();
        	save(r1);
        }).start();
        new Thread(() -&gt; {
        	r2 = getPriceByS2();
        	save(r2);
        }).start();
        new Thread(() -&gt; {
        	r3 = getPriceByS3();
        	save(r3);
        }).start();
我觉得这里不需要future,除非询价和保存之间还有别的计算工作</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/df/dd536ff5.jpg" width="30px"><span>魏斌斌</span> 👍（9） 💬（3）<div>老师，我看了下futruerask的源码，当调用futrue.get()方法，其实最终会调用unsafe方法是当前线程阻塞。但是我不太理解线程阻塞到哪去了，也没看到锁。</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7c/b5/4a7a2bd4.jpg" width="30px"><span>Sunqc</span> 👍（6） 💬（1）<div>老师，你所说的订蛋糕，我这样理解对吗，把任务提交给线程池就是让蛋糕店做蛋糕；去看电影就是主线程做其他事，提货单是对应调用future的get</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/65/23/b42f102c.jpg" width="30px"><span>the only Mia’s</span> 👍（3） 💬（1）<div>老师，jdk 8提供的CompletableFuture，以后异步处理是不是可以直接用此替代</div>2020-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（3） 💬（2）<div>课后习题，老师帮忙看下哦
public class ExecutorExample {
private static final ExecutorService executor;
    static {executor = new ThreadPoolExecutor(4, 8, 1, TimeUnit.SECONDS, new ArrayBlockingQueue&lt;Runnable&gt;(1000), runnable -&gt; null, (r, executor) -&gt; {&#47;&#47;根据业务降级策略});
}
static class S1Task implements Callable&lt;String&gt; {
        @Override
        public String call() throws Exception {return getPriceByS1();}}
    static class S2Task implements Callable&lt;String&gt; {
        @Overridepublic String call() throws Exception {return getPriceByS2();}}
    static class S3Task implements Callable&lt;String&gt; {@Override public String call() throws Exception {return getPriceByS3();}}
    static class SaveTask implements Callable&lt;Boolean&gt; {private List&lt;FutureTask&lt;String&gt;&gt; futureTasks; public SaveTask(List&lt;FutureTask&lt;String&gt;&gt; futureTasks) {this.futureTasks = futureTasks;
}
        @Override
        public Boolean call() throws Exception {
            for (FutureTask&lt;String&gt; futureTask : futureTasks) {
                String data = futureTask.get(10, TimeUnit.SECONDS);
                saveData(data);
            }
            return Boolean.TRUE;
        }
    }
    private static String getPriceByS1() {
        return &quot;fromDb1&quot;;
    }
    private static String getPriceByS2() {
        return &quot;fromDb2&quot;;
    }
    private static String getPriceByS3() {
        return &quot;fromDb3&quot;;
    }
    private static void saveData(String data) {
        &#47;&#47;save data to db
    }
    public static void main(String[] args) {
        S1Task s1Task = new S1Task();FutureTask&lt;String&gt; st1 = new FutureTask&lt;&gt;(s1Task);S2Task s2Task = new S2Task();FutureTask&lt;String&gt; st2 = new FutureTask&lt;&gt;(s2Task);S3Task s3Task = new S3Task();FutureTask&lt;String&gt; st3 = new FutureTask&lt;&gt;(s3Task);List&lt;FutureTask&lt;String&gt;&gt; futureTasks = Lists.&lt;FutureTask&lt;String&gt;&gt;newArrayList(st1, st2, st3);FutureTask&lt;Boolean&gt; saveTask = new FutureTask&lt;&gt;(new SaveTask(futureTasks));executor.submit(st1);executor.submit(st2);executor.submit(st3);executor.submit(saveTask);}}</div>2019-04-22</li><br/><li><img src="http://thirdqq.qlogo.cn/qqapp/101418266/D6DD8CB1004D442B48914656340277F3/100" width="30px"><span>henry</span> 👍（3） 💬（1）<div>现在是在主线程串行完成3个询价的任务，执行第一个任务，其它2个任务只能等待执行，如果要提高效率，这个地方需要改进，可以用老师今天讲的futuretask，三个询价任务改成futuretask并行执行，效率会提高</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（2） 💬（1）<div>我也同意张天屹同学的观点   这个询价操作如果之间没有联系的话  直接起三个线程就可以了 老师能不能讲一下 用线程池怎么就有关联了？</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/8a/e3/c967e11a.jpg" width="30px"><span>near</span> 👍（1） 💬（1）<div>老师，有问题问一下：1.在泡茶的例子中，如果使用线程池创建线程，假设有很多个泡茶任务都要反复调用线程池中的线程，那么在T2提前完成任务，T1获取T2的结果前，T2这个线程会不会被线程池回收？2.假设T1在T2前完成，当T1要获取T2结果时，T1中的代码是阻塞的状态吗？</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（1） 💬（1）<div>老师，在提交 Runnable 任务及结果引用的例子里面的x变量是什么?</div>2019-04-20</li><br/><li><img src="" width="30px"><span>Geek_31594d</span> 👍（0） 💬（1）<div>老师，有个一直比较疑虑的地方，future.get获取返回值是去阻塞，如果get使用太多，那么阻塞的地方就会感觉有问题</div>2021-09-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/LPnuO9GleKEwso2rSbibmbEwn49hnGl9qTQDBv2xLOOWOflQsc9oVEEuZgNBt7TrqRKvk8CX7Tc8iakhEicBCCfFg/132" width="30px"><span>盛权_vinc</span> 👍（0） 💬（1）<div>老师，你这个泡茶例子，看你最终的执行结果，洗水壶和洗茶壶并行了，然后才开始烧水洗茶杯，这好像有点违背了最优分工方案的图和现实？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ce/c3/688b8bf9.jpg" width="30px"><span>是我！</span> 👍（0） 💬（1）<div>老师您好：请问这样是否有问题？  
public static void main(String[] args) throws Exception {
        FutureTask t1 = new FutureTask(new Callable() {
            @Override
            public String call() {
                return &quot;getPriceByS1()&quot;;
            }
        });
        FutureTask t2 = new FutureTask(() -&gt; &quot;getPriceByS2()&quot;);
        FutureTask t3 = new FutureTask(() -&gt; &quot;getPriceByS3()&quot;);
        BlockingQueue&lt;Runnable&gt; blockingQueue = new ArrayBlockingQueue&lt;&gt;(3);
        ThreadPoolExecutor poolExecutor =
                new ThreadPoolExecutor(10, 10, 10,
                        TimeUnit.SECONDS, blockingQueue);
        poolExecutor.submit(t1);
        save(t1.get().toString());
        poolExecutor.submit(t2);
        save(t2.get().toString());
        poolExecutor.submit(t3);
        save(t3.get().toString());
    }

    private static void save(String ss) {
        System.out.println(&quot;保存&quot; + ss);
    }</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/18/245f8558.jpg" width="30px"><span>爱上丘比特</span> 👍（0） 💬（1）<div>老师，既然get是阻塞方法，那应该何时调用呢？或者说在哪种场景调用避免阻塞主线程？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/42/fbe890c0.jpg" width="30px"><span>vector</span> 👍（59） 💬（0）<div>最近使用CompletableFuture工具方法以及lamda表达式比较多，语言语法的变化带来编码效率的提升真的很大。</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（43） 💬（2）<div>课后题：
可以用 Future
        ExecutorService threadPoolExecutor = Executors.newFixedThreadPool(3);
        Future&lt;R&gt; future1 = threadPoolExecutor.submit(Test::getPriceByS1);
        Future&lt;R&gt; future2 = threadPoolExecutor.submit(Test::getPriceByS2);
        Future&lt;R&gt; future3 = threadPoolExecutor.submit(Test::getPriceByS3);
        R r1 = future1.get();
        R r2 = future2.get();
        R r3 = future3.get();

也可以用 CompletableFuture
        CompletableFuture&lt;R&gt; completableFuture1 = CompletableFuture.supplyAsync(Test::getPriceByS1);
        CompletableFuture&lt;R&gt; completableFuture2 = CompletableFuture.supplyAsync(Test::getPriceByS2);
        CompletableFuture&lt;R&gt; completableFuture3 = CompletableFuture.supplyAsync(Test::getPriceByS3);
        CompletableFuture.allOf(completableFuture1, completableFuture2, completableFuture3)
                         .thenAccept(System.out::println);
 老师这样理解对吗 谢谢老师</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/90/be01bb8d.jpg" width="30px"><span>Asanz</span> 👍（23） 💬（8）<div>不是不建议使用 Executors 创建线程池了吗？？？
</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/d2/e3ae7ddd.jpg" width="30px"><span>三木禾</span> 👍（6） 💬（0）<div>这个可以用生产消费者模式啊</div>2019-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（5） 💬（0）<div>分别提交三个futuretask给线程池，然后最后分别get出结果，统一进行保存数据库</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/9f/f4b06bd5.jpg" width="30px"><span>见南山</span> 👍（2） 💬（0）<div>给最后问题再加一步，询价后，得到最小的一家。题就比较好了</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/bc/664bbdf7.jpg" width="30px"><span>女巫在寒江</span> 👍（2） 💬（0）<div>		ExecutorService executor = Executors.newFixedThreadPool(3);

		executor.submit(new Task1());
		executor.submit(new Task2());
		executor.submit(new Task3());
		
		class Task1  implement Runnable {
			void run(){
				r = getPriceByS1();
				save(r);
			}
		}
		
		class Task2  implement Runnable {
			void run(){
				r = getPriceByS2();
				save(r);
			}
		}
		
		class Task3  implement Runnable {
			void run(){
				r = getPriceByS3();
				save(r);
			}
		}</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/0c/c623649c.jpg" width="30px"><span>稚者</span> 👍（2） 💬（3）<div>烧水泡茶的Demo有点小问题，Task2的启动时间应该在Task1的洗茶壶之后开始，现在的代码是一起开始。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/04/ba949d78.jpg" width="30px"><span>圆圜</span> 👍（2） 💬（0）<div>你这个不对啊，应该是executeservice.submit t2furturetask，不能直接提交t2</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/63/7eb32c9b.jpg" width="30px"><span>捞鱼的搬砖奇</span> 👍（2） 💬（1）<div>Future的get()是拿到任务的执行结果不吧。为什么又说是拿到方法的入参了。</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（2） 💬（0）<div>在实际项目中应用已经应用到了Feture,但没有使用线程池，没有那么优雅，所以算是get到了👍</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（0）<div>打卡。感觉很神奇，之前完全不会用。学的知识太陈旧了，继续学习。</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（1） 💬（0）<div>1 三个可以异步执行
2 利用countdownlact 计数 三个线程(or线程池)去处理
3 使用CompletableFuture去处理</div>2022-05-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL77I4uYg4oBMiclTFdMdcwNiaPXzwNZWvGr9Vpl84wKdEiaHGTZuAFkscS8mItthOEa12p5wLicJb5lg/132" width="30px"><span>Geek_96a4cb</span> 👍（1） 💬（0）<div>课后思考题:
Executor executor = Executors.newFixedThreadPool(3);
executor.submit(()-&gt;save(getPriceByS1()));
executor.submit(()-&gt;save(getPriceByS2()));
executor.submit(()-&gt;save(getPriceByS3()));</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（1） 💬（0）<div>我觉得最后一题完全可以做三个不同功能接口，不能为了多线程而多线程。因为三个又没交集。各自处理好了。</div>2021-05-11</li><br/>
</ul>