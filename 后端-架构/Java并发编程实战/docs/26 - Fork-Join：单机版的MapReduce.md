前面几篇文章我们介绍了线程池、Future、CompletableFuture和CompletionService，仔细观察你会发现这些工具类都是在帮助我们站在任务的视角来解决并发问题，而不是让我们纠缠在线程之间如何协作的细节上（比如线程之间如何实现等待、通知等）。**对于简单的并行任务，你可以通过“线程池+Future”的方案来解决；如果任务之间有聚合关系，无论是AND聚合还是OR聚合，都可以通过CompletableFuture来解决；而批量的并行任务，则可以通过CompletionService来解决。**

我们一直讲，并发编程可以分为三个层面的问题，分别是分工、协作和互斥，当你关注于任务的时候，你会发现你的视角已经从并发编程的细节中跳出来了，你应用的更多的是现实世界的思维模式，类比的往往是现实世界里的分工，所以我把线程池、Future、CompletableFuture和CompletionService都列到了分工里面。

下面我用现实世界里的工作流程图描述了并发编程领域的简单并行任务、聚合任务和批量并行任务，辅以这些流程图，相信你一定能将你的思维模式转换到现实世界里来。

![](https://static001.geekbang.org/resource/image/47/2d/47f3e1e8834c99d9a1933fb496ffde2d.png?wh=1142%2A706)

从上到下，依次为简单并行任务、聚合任务和批量并行任务示意图
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/cb/f8157ad8.jpg" width="30px"><span>爱吃回锅肉的瘦子</span> 👍（116） 💬（9）<div>https:&#47;&#47;www.liaoxuefeng.com&#47;article&#47;001493522711597674607c7f4f346628a76145477e2ff82000，老师，您好，我在廖雪峰网站中也看到forkjoin使用方式。讲解了，为啥不使用两次fork，分享出来给大家看看。</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（71） 💬（5）<div>CPU同一时间只能处理一个线程，所以理论上，纯cpu密集型计算任务单线程就够了。多线程的话，线程上下文切换带来的线程现场保存和恢复也会带来额外开销。但实际上可能要经过测试才知道。</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c1/1b/e08d42f8.jpg" width="30px"><span>尹圣</span> 👍（44） 💬（6）<div>看到分治任务立马就想到归并排序，用Fork&#47;Join又重新实现了一遍，
 &#47;**
  * Ryzen 1700 8核16线程 3.0 GHz
  *&#47;
 @Test
 public void mergeSort() {
     long[] arrs = new long[100000000];
     for (int i = 0; i &lt; 100000000; i++) {
         arrs[i] = (long) (Math.random() * 100000000);
     }
     long startTime = System.currentTimeMillis();
     ForkJoinPool forkJoinPool = new ForkJoinPool(Runtime.getRuntime().availableProcessors());
     MergeSort mergeSort = new MergeSort(arrs);
     arrs = forkJoinPool.invoke(mergeSort);
     &#47;&#47;传统递归
     &#47;&#47;arrs = mergeSort(arrs);
     long endTime = System.currentTimeMillis();
     System.out.println(&quot;耗时：&quot; + (endTime - startTime));
 }
 &#47;**
  * fork&#47;join
  * 耗时：13903ms
  *&#47;
 class MergeSort extends RecursiveTask&lt;long[]&gt; {
     long[] arrs;
     public MergeSort(long[] arrs) {
         this.arrs = arrs;
     }
     @Override
     protected long[] compute() {
         if (arrs.length &lt; 2) return arrs;
         int mid = arrs.length &#47; 2;
         MergeSort left = new MergeSort(Arrays.copyOfRange(arrs, 0, mid));
         left.fork();
         MergeSort right = new MergeSort(Arrays.copyOfRange(arrs, mid, arrs.length));
         return merge(right.compute(), left.join());
     }
 }
 &#47;**
  * 传统递归
  * 耗时：30508ms
  *&#47;
 public static long[] mergeSort(long[] arrs) {
     if (arrs.length &lt; 2) return arrs;
     int mid = arrs.length &#47; 2;
     long[] left = Arrays.copyOfRange(arrs, 0, mid);
     long[] right = Arrays.copyOfRange(arrs, mid, arrs.length);
     return merge(mergeSort(left), mergeSort(right));
 }
 public static long[] merge(long[] left, long[] right) {
     long[] result = new long[left.length + right.length];
     for (int i = 0, m = 0, j = 0; m &lt; result.length; m++) {
         if (i &gt;= left.length) {
             result[m] = right[j++];
         } else if (j &gt;= right.length) {
             result[m] = left[i++];
         } else if (left[i] &gt; right[j]) {
             result[m] = right[j++];
         } else result[m] = left[i++];
     }
     return result;
 }</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（36） 💬（1）<div>学习了老师的分享，现在就已经在工作用到了，的确是在同事面前好好装了一次逼</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（35） 💬（1）<div>以前在面蚂蚁金服时，也做过类似的题目，从一个目录中，找出所有文件里面单词出现的top100，那时也是使用服务提供者，从目录中找出一个或者多个文件（防止所有文件一次性加载内存溢出，也为了防止文件内容过小，所以每次都确保读出的行数10万行左右），然后使用fork&#47;join进行单词的统计处理，设置处理的阈值为20000。
课后习题：单核的话，使用单线程会比多线程快，线程的切换，恢复等都会耗时，并且要是机器不允许，单线程可以保证安全，可见性（cpu缓存，单个CPU数据可见），线程切换（单线程不会出现原子性）</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（25） 💬（6）<div>请教老师一个问题，merge函数里的mr2.compute先执行还是mr1.join先执行，这两个参数是否可交换位置</div>2019-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（14） 💬（1）<div>如果所有的并行流计算都是 CPU 密集型计算的话，完全没有问题，但是如果存在 I&#47;O 密集型的并行流计算，那么很可能会因为一个很慢的 I&#47;O 计算而拖慢整个系统的性能。

老师这里的意思是不是，如果有耗时的i&#47;o计算，需要用单独的forkjoin pool 来处理这个计算，在程序设计的时候就要跟其他cpu密集计算的任务分开处理？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0e/b9/7866f19d.jpg" width="30px"><span>王伟</span> 👍（9） 💬（2）<div>老师，我现在碰到一个生产问题：用户通过微信小程序进入我们平台，我们只能需要使用用户的手机号去我们商家库中查取该用户的注册信息。在只知道用户手机号的情况下我们需要切换到所有的商家库去查询。这样非常耗时。ps：我们商家库做了分库处理而且数量很多。想请教一下您，这种查询该如何做？</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/d3/e25d104a.jpg" width="30px"><span>êｗěｎ</span> 👍（7） 💬（1）<div>老师，fork是fork调用者的子任务还是表示下面new出来的任务是子任务？</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fe/b8/24a6e0cb.jpg" width="30px"><span>Nick</span> 👍（6） 💬（1）<div>简易的MapReduce的程序跑下来不会栈溢出吗？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（6） 💬（3）<div>老师，请问为什么不能merge mr1.compute和mr2..compute或者mr1.join和mr2的join呢？
</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/55/fccafd61.jpg" width="30px"><span>王彬-Antonio</span> 👍（3） 💬（1）<div>老师，您在文中提到io密集型和计算密集型最好区分开不同线程池。假设两个线程池如果都在运行，它们之间怎么竞争CPU线程？</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（3） 💬（1）<div>这里用的递归调用，数据量大的时候会不会粘溢出，虽然这里用的二分，时间复杂度为logn</div>2019-04-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（2） 💬（1）<div>老师，您好，有个问题想请教您一下

问题：使用 fork&#47;join 框架，ForkJoinTask 不是只提交给 ForkJoinPool 线程池里的线程执行么？为什么 main 主线程也参与了运算？


验证如下：
public static void main(String[] args) {
        IntStream.range(1, 3).parallel().forEach(i -&gt; System.out.println(Thread.currentThread().getName() + &quot;##&quot; + i));
    }

输出：
ForkJoinPool.commonPool-worker-1##1
main##2

除了 ForkJoinPool.commonPool-worker，还有 main 的输出。</div>2020-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKZSibeTatZ2ImL5Xu3QqdTWQs5nyQAxDlsm3m0KicP3TN6icJqYricvhjOFfTB2B3oLInU45CC9LtqMA/132" width="30px"><span>狂风骤雨</span> 👍（2） 💬（2）<div>好希望工作当中能有老师这样一位大牛，能为我答疑解惑</div>2019-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3qfPEnr4rIVUicypRp4tlZUh8fliaZgJWHDOxxSia1ShPCxK61cpWCgN2piaf5xksTr3jic0YypSvsgM6u5sop9FlsQ/132" width="30px"><span>Geek_c40c24</span> 👍（1） 💬（1）<div>static class Fibonacci extends RecursiveTask&lt;Integer&gt; {
        final int n;

        Fibonacci(int n) {
            this.n = n;
        }


        @Override
        protected Integer compute() {
            if (n &lt;= 1) {
                return n;
            }
            Fibonacci f1 = new Fibonacci(n-1);



            Fibonacci f2 = new Fibonacci(n-2);


            return f2.compute() +  f1.compute();
        }
    }
这样和老师你的例子有什么区别呀 ，我还不不理解深层次的含义</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/9d/abb7bfe3.jpg" width="30px"><span>林伊</span> 👍（1） 💬（1）<div>1.8中对fork()方法做了改进，会先判断是不是当前线程，如果是则放入当前线程的任务队列中的。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（1） 💬（1）<div>“如果存在 I&#47;O 密集型的并行流计算，那么很可能会因为一个很慢的 I&#47;O 计算而拖慢整个系统的性能。”

老师这个问题，这句话前面的文字也看到，但是不太懂。如果共用一个线程池，但是不是有多个线程，如果一个线程操作I&#47;O，应该不影响其他线程吧，其他线程还能继续执行，我不太理解为什么会拖慢整个系统，求老师帮我解答这个疑问。</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（1） 💬（1）<div>对于单核CPU而言，FJ线程池默认1个线程，由于是CPU密集型，失去了线程切换的意义，平白带来上下文切换的性能损耗。
老师我想请教下前文斐波那契数列的例子，一个30的斐波那契递归展开后是一个深度30的二叉树，每一层的一个分支由主线程执行，另一个提交FJ的线程池执行，那么可不可以理解为最后一半的任务被主线程执行了，另一半的任务被FJ 的线程池执行了呢。如果是的话，提交给FJ任务队列的任务会进入不同的任务队列吗？我对于FJ分多个任务队列的目的和原理都不太了解。</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/f7/0ca6cf20.jpg" width="30px"><span>嘉莹</span> 👍（0） 💬（1）<div>老师，计算Fibonacci那个例子里，compute方法中条件if (n &lt;= 1)应该是if (n &lt;= 2)吧？</div>2021-02-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiauonyMORA2s43W7mogGDH4WYjW0gBJtYmUa9icTB6aMPGqibicEKlLoQmLKLWEctwHzthbTZkKR20w/132" width="30px"><span>Spring4J</span> 👍（0） 💬（1）<div>统计单词的merge函数里面，感觉应该先比较两个map的size，然后循环小的那个，应该会更快</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/14/e9ca2d09.jpg" width="30px"><span>小予</span> 👍（0） 💬（2）<div>我测试了一下Fork&#47;Join计算Fibonacci数列的性能，用Fork&#47;Join的耗时是直接用递归方法的几十倍，是Fork&#47;Join不适合这样的场景呢，还是我的用法有问题啊，希望老师可以抽时间看下。 代码如下：
public class TestForkJoin {
    public static void main(String[] args) {
        long n = 50;
        long start = System.currentTimeMillis();
        System.out.println(&quot;递归结算结果：&quot; + fibonacciN(n) + &quot; 耗时：&quot; + (System.currentTimeMillis() - start));
        System.out.println(&quot;================================&quot;);

        start = System.currentTimeMillis();
        ForkJoinPool forkJoinPool = new ForkJoinPool(4);
        &#47;&#47; 创建分治任务
        Fibonacci fibonacci = new Fibonacci(n);
        &#47;&#47; 启动分治任务
        Long result = forkJoinPool.invoke(fibonacci);
        System.out.println(&quot;Fork&#47;Join结果：&quot; + result + &quot; 耗时：&quot; + (System.currentTimeMillis() - start));
    }

    public static long fibonacciN(long n) {
        if (n &lt; 1)
            return n;
        if (n == 1 || n == 2)
            return 1;
        return fibonacciN(n - 1) + fibonacciN(n - 2);
    }

    static class Fibonacci extends RecursiveTask&lt;Long&gt; {
        private final long n;

        public Fibonacci(long n) {
            this.n = n;
        }

        @Override
        protected Long compute() {
            if (n &lt;= 1)
                return n;
            Fibonacci f1 = new Fibonacci(n - 1);
            &#47;&#47; 创建子任务
            f1.fork();
            Fibonacci f2 = new Fibonacci(n - 2);
            &#47;&#47; 等待子任务结果，并合并结果
            return f2.compute() + f1.join();
        }
    }
}</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（1）<div>“如果任务在执行过程中会创建出子任务，那么子任务会提交到工作线程对应的任务队列中。”
抱歉来得晚了些。
上面这句话不太理解。如果“创建子任务”指的是fork的话，是不是应该提交到其他任务队列中？否则岂不是全部在一个队列中，被一个线程处理，其他线程对应的队列都是空，全靠steal？
那样的话有什么办法利用其他线程？</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/6d/19/204b0900.jpg" width="30px"><span>Black Jack</span> 👍（3） 💬（1）<div>return f2.compute() + f1.join();
对这行代码的理解是 当前线程把 f1的工作分配出去,并等待其完成，然后自己进行f2的工作。如果使用f2.fork,f2.join.相当于当前线程空闲了，存在资源浪费了</div>2021-11-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（3） 💬（1）<div>@王伟童鞋的问题，我们也有这场景：通过手机号查询商家信息。
我们是在 redis 里维护(手机号，商家号)关联关系，在 redis 里通过手机号查询商家号，就知道该去哪个库表查询商家具体信息了。

内存开销：
手机号，11 个字符，占用 11B；
商家号，4 个字符，占用 4B；
一条记录占用 15B，100 万条记录，就 15*100万B，大概是：
15*1,000,000B&#47;1000&#47;1000=15M</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（3） 💬（0）<div>ForkJoinTask这个抽象类的 fork() 和 join（）底层是怎么实现的呢？</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/47/39/0ce1aa62.jpg" width="30px"><span>罗洲</span> 👍（2） 💬（1）<div>单核cpu上多线程会导致线程的上下文切换，还不如单核单线程处理的效率高。</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/b6/8fb15749.jpg" width="30px"><span>夏目</span> 👍（1） 💬（1）<div>请教一下：return merge(mr2.compute(), mr1.join());
这样写mr2又会被分割为mr3、mr4，mr3又会被分割为mr5、mr6.....,无线分割下去吗？
</div>2020-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4akcIyIOXB2OqibTe7FF90hwsBicxkjdicUNTMorGeIictdr3OoMxhc20yznmZWwAvQVThKPFWgOyMw/132" width="30px"><span>Chuan</span> 👍（1） 💬（1）<div>关于使用两次fork，官方的建议如下：
```
 * &lt;p&gt;In the most typical usages, a fork-join pair act like a call
 * (fork) and return (join) from a parallel recursive function. As is
 * the case with other forms of recursive calls, returns (joins)
 * should be performed innermost-first. For example, {@code a.fork();
 * b.fork(); b.join(); a.join();} is likely to be substantially more
 * efficient than joining {@code a} before {@code b}.
```

先join a再join b，确实会出现类似监工的问题，当前线程并没有执行计算任务。但请教下老师，如果先join b再join a，当前线程好像也没有执行计算任务，一样会存在“监工问题”而影响性能，不知道这块老师是怎么看的？</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/8e/2376cd87.jpg" width="30px"><span>蓝天白云看大海</span> 👍（1） 💬（2）<div>join会阻塞线程吗？如果阻塞线程，而线程池里的线程个数又有线，那么递归几次之后所有线程不都全阻塞了吗！</div>2019-06-02</li><br/>
</ul>