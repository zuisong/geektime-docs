前面我们不止一次提到，用多线程优化性能，其实不过就是将串行操作变成并行操作。如果仔细观察，你还会发现在串行转换成并行的过程中，一定会涉及到异步化，例如下面的示例代码，现在是串行的，为了提升性能，我们得把它们并行化，那具体实施起来该怎么做呢？

```
//以下两个方法都是耗时操作
doBizA();
doBizB();
```

还是挺简单的，就像下面代码中这样，创建两个子线程去执行就可以了。你会发现下面的并行方案，主线程无需等待doBizA()和doBizB()的执行结果，也就是说doBizA()和doBizB()两个操作已经被异步化了。

```
new Thread(()->doBizA())
  .start();
new Thread(()->doBizB())
  .start();  
```

**异步化**，是并行方案得以实施的基础，更深入地讲其实就是：**利用多线程优化性能这个核心方案得以实施的基础**。看到这里，相信你应该就能理解异步编程最近几年为什么会大火了，因为优化性能是互联网大厂的一个核心需求啊。Java在1.8版本提供了CompletableFuture来支持异步编程，CompletableFuture有可能是你见过的最复杂的工具类了，不过功能也着实让人感到震撼。

## CompletableFuture的核心优势

为了领略CompletableFuture异步编程的优势，这里我们用CompletableFuture重新实现前面曾提及的烧水泡茶程序。首先还是需要先完成分工方案，在下面的程序中，我们分了3个任务：任务1负责洗水壶、烧开水，任务2负责洗茶壶、洗茶杯和拿茶叶，任务3负责泡茶。其中任务3要等待任务1和任务2都完成后才能开始。这个分工如下图所示。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（146） 💬（4）<div>思考题：
1.没有进行异常处理，
2.要指定专门的线程池做数据库查询
3.如果检查和查询都比较耗时，那么应该像之前的对账系统一样，采用生产者和消费者模式，让上一次的检查和下一次的查询并行起来。

另外，老师把javadoc里那一堆那一堆方法进行了分类，分成串行、并行、AND聚合、OR聚合，简直太棒了，一下子就把这些方法纳入到一个完整的结构体系里了。简直棒</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/49/ba/02742d56.jpg" width="30px"><span>袁阳</span> 👍（118） 💬（7）<div>思考题:
1，读数据库属于io操作，应该放在单独线程池，避免线程饥饿
2，异常未处理</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（50） 💬（5）<div>我在想一个问题，明明是串行过程，直接写就可以了。为什么还要用异步去实现串行？</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（45） 💬（2）<div>老师 ，我有个疑问。 completableFuture 中各种关系（并行、串行、聚合），实际上就覆盖了各种需求场景。 例如 ： 线程A 等待 线程B 或者 线程C 等待 线程A和B 。

我们之前讲的并发包里面 countdownLatch , 或者 threadPoolExecutor 和future  就是来解决这些关系场景的 ， 那有了 completableFuture 这个类 ，是不是以后有需求都优先考虑用 completableFuture ？感觉这个类就可以解决前面所讲的类的问题了</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/5b/2a342424.jpg" width="30px"><span>青莲</span> 👍（22） 💬（1）<div>1.查数据库属于io操作，用定制线程池
2.查出来的结果做为下一步处理的条件，若结果为空呢，没有对应处理
3.缺少异常处理机制</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/57/e3bd54bd.jpg" width="30px"><span>笃行之</span> 👍（17） 💬（2）<div>”如果所有 CompletableFuture 共享一个线程池，那么一旦有任务执行一些很慢的 I&#47;O 操作，就会导致线程池中所有线程都阻塞在 I&#47;O 操作上，从而造成线程饥饿，进而影响整个系统的性能。”老师，阻塞在io上和是不是在一个线程池没关系吧？</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（12） 💬（1）<div>我觉得既然都讲到CompletableFuture了，老师是不是有必要不一章ForkJoinPool呀？毕竟，ForkJoinPool和ThreadPoolExecutor还是有很多不一样的。谢谢老师</div>2019-04-23</li><br/><li><img src="http://thirdqq.qlogo.cn/qqapp/101418266/D6DD8CB1004D442B48914656340277F3/100" width="30px"><span>henry</span> 👍（11） 💬（4）<div>老师我现在有个任务，和您的例子有相似的地方，是从一个库里查询多张表的数据同步到另外一个库，就有双重for循环，最外层用与多张表的遍历，内层的for循环用于批量读取某一张表的数据，因为数据量可能在几万条，我想分批次读出来再同步到另一个数据库，昨天写的时候用的是futuretask,今天正好看到老师的文章就改成了CompletableFuture，还没有用异常处理的，后面我还要看看怎么加上异常处理的。其它的不知道我用的对不对，请老师看看：
   &#47;&#47; 初始化异步工具类，分别异步执行2个任务
        CompletableFuture&lt;List&lt;PBSEnergyData&gt;&gt; asyncAquirePBSEnergyData = new CompletableFuture();
        CompletableFuture&lt;List&lt;AXEEnergyData&gt;&gt; asyncSaveAxeEnergyData = new CompletableFuture();
        &#47;&#47; 初始化两个线程池， 分别用于2个任务 ，1个任务一个线程池，互不干扰
        Executor aquirePBSEnergyDataExecutor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        Executor saveAxeEnergyDataExecutor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        queryUtils.getTableNames().forEach(tableName -&gt; {
            int pageSize = queryUtils.getPageSize();
            &#47;&#47;查询该表有多少条数据，每${pageSize}条一次
            int count = pbsEnergyService.getCount(tableName);
            &#47;&#47;总页数
            int pages = count &#47; pageSize;
            int pageNum = 0;
            final int pageNo = pageNum;
            for(pageNum = 0; pageNum &lt;= pages; pageNum++){
                &#47;&#47; 异步获取PBS数据库的数据并返回结果
                asyncAquirePBSEnergyData
                        .supplyAsync(() -&gt; {
                    查询数据库
                    return pbsEnergyDatas;
                },aquirePBSEnergyDataExecutor)
                        &#47;&#47; 任务2任务1，任务1返回的结果
                        .thenApply(pbsEnergyDatas -&gt; asyncSaveAxeEnergyData.runAsync(()-&gt;{
                    List&lt;AXEEnergyData&gt; axeEnergyDatas = pbsEnergyDatas.stream().map(pbsEnergyData -&gt; {
                   	 &#47;&#47;进行类型转换
                    }).collect(Collectors.toList());
                    &#47;&#47;批量保存
                },saveAxeEnergyDataExecutor));
            }
        });
全部贴上去，超过字符数了，只能请老师凑合看了 :(</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/3e/c39d86f1.jpg" width="30px"><span>Chocolate</span> 👍（10） 💬（4）<div>回答「密码123456」：CompletableFuture 在执行的过程中可以不阻塞主线程，支持 runAsync、anyOf、allOf 等操作，等某个时间点需要异步执行的结果时再阻塞获取。</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（8） 💬（2）<div>带有asyn的方法是异步执行，这里的异步是不在当前线程中执行？  比较困惑</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（7） 💬（1）<div>CompletableFuture从来没玩过，老师在工作&#47;实践中有使用过这个类吗？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/f1/996a070d.jpg" width="30px"><span>LW</span> 👍（6） 💬（1）<div>老师，为什么CompletableFuture中默认使用ForkJoinPool这个线程池呢？它为什么不用其他线程池？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/28/a8/eaa810af.jpg" width="30px"><span>Geek_0359eb</span> 👍（5） 💬（1）<div>老师您好，想问下主线程怎么捕获到多线程中抛出的异常，捕获后再抛出自定义异常呢？</div>2020-04-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（5） 💬（1）<div>老师我有一个问题：在描述串行关系时，为什么参数没有other？这让我觉得并不是在描述两个子任务的串行关系，而是给第一个子任务追加了一个类似“回调方法”fn等……而并行关系和汇聚关系则很明确的出现了other……</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/e3/99f330b8.jpg" width="30px"><span>_立斌</span> 👍（2） 💬（2）<div>老师好，想请问一下，如果一个事务里开了多个异步任务，如果其中一个任务抛出异常了，其他任务应该全部回滚，这样的异常如何捕获并处理呢？业界有最佳实践吗？谢谢老师</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/98/8f1aecf4.jpg" width="30px"><span>楼下小黑哥</span> 👍（2） 💬（1）<div>看了几篇 CompletableFuture 的文章，也写过测试 dmeo。不过 CompletableFuture API 太多了，看的迷迷糊糊的。老师这么分类，瞬间清除了，感谢！
嘿嘿，学到一招，分类归纳。</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（2）<div>如果所有 CompletableFuture 共享一个线程池，那么一旦有任务执行一些很慢的 I&#47;O 操作，就会导致线程池中所有线程都阻塞在 I&#47;O 操作上


这个是不是有问题？因为线程池有多个线程，如果只有一个阻塞，那么其他的线程也是可以的吧</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/5f/2cc4060c.jpg" width="30px"><span>子豪sirius</span> 👍（1） 💬（1）<div>我是先学了javascript的ES6的，发现CompletableFuture的使用方法跟Promise很相似，应该是不同语言的相互影响吧</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（1） 💬（1）<div>老师想请教您一个问题，我创建了一个用户线程然后将它设置为守护线程，为什么主线程结束时，它没有结束，需要在它的执行逻辑里调用sleep才会当主线程结束时结束。</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/89/e1621a01.jpg" width="30px"><span>zhangtnty</span> 👍（1） 💬（1）<div>王老师好，单看文中题目的代码是没问题的，读数和校验串行化了, 不考虑效率是没问题的。如果要提升效率最好并行化, 读数和校验利用队列方式效率更高。</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/f2/af/4f5f6d1e.jpg" width="30px"><span>xieyue</span> 👍（0） 💬（1）<div>文章中使用的绘图工具是什么呀，感觉挺好的，想学习一下</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>老师 问一下关于回调地狱的问题 ,回调和正常面向过程调用不都是嵌套方法吗，为什么回调会有问题</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ab/1c3dc64b.jpg" width="30px"><span>夏目🐳</span> 👍（0） 💬（1）<div>老师可以讲下flowAPI吗，工作中任务调度用的比较多～</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/09/eb3da11d.jpg" width="30px"><span>孟令超</span> 👍（0） 💬（1）<div>老师课程代码能公开下吗</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（1）<div>王老师好，其他地方看到说异步 IO 主要是为了控制线程数量，请问怎么理解？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f2/e0/9577744e.jpg" width="30px"><span>Mr.zhang</span> 👍（0） 💬（6）<div>老师您好，我想请问一下：(__, tf)-&gt;{ }，这是一种什么用法呢？括号中的__是什么意思呢？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（0） 💬（1）<div>嗯对，我以log的打印为准了，log打印结束并不代表主线程已经结束了，还是有个时间差，这个时候子线程还会运行一段时间，感谢老师</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（0） 💬（1）<div>是的，启动前设置成守护线程了，就像这样
public static void main(String[] args){
    Thread thread = new Thread(new Runnable() {
        @Override
        public void run() {
             for(int i=0;i&lt;10;i++){
                 try {
                     Thread.sleep(1);
                 } catch (InterruptedException e) {
                     e.printStackTrace();
                 }
                 log.info(&quot;子线程执行任务&quot;+i);
             }
        }
    });
    thread.setDaemon(true);
    thread.start();
    for (int j=0;j&lt;3;j++){
        log.info(&quot;主线程执行任务&quot;+j);
    }
    log.info(&quot;运行结束&quot;);
}
    如果把sleep部分去掉，即使设成守护线程，主线程结束后子线程仍不会结束</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/3b/a1f7e3a4.jpg" width="30px"><span>ZOU志伟</span> 👍（0） 💬（1）<div>想知道()-&gt;是什么用法？哪里有介绍</div>2019-04-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKR3ibELhjgVicCNShZCBwvaDxibnzibggG4wUzVkS2mkDxUBZyIs87nDEdJ7PiahJBVoZcuhQ84RxAziag/132" width="30px"><span>周治慧</span> 👍（0） 💬（1）<div>在第3快描述or聚合的时候，第二个f1应该是f2。关于思考题，在进行数据校验时依赖查询规则的查询结果是个串行操作，但是需要对异常进行处理</div>2019-04-23</li><br/>
</ul>