你好，我是邵亚方。

如果你做过性能优化的话，你应该有过这些思考，比如说：

- 如何让CPU读取数据更快一些？
- 同样的任务，为什么有时候执行得快，有时候执行得慢？
- 我的任务有些比较重要，CPU如果有争抢时，我希望可以先执行这些任务，这该怎么办呢？
- 多线程并行读写数据是如何保障同步的？
- …

要想明白这些问题，你就需要去了解CPU是如何执行任务的，只有明白了CPU的执行逻辑，你才能更好地控制你的任务执行，从而获得更好的性能。

## CPU是如何读写数据的 ？

我先带你来看下CPU的架构，因为你只有理解了CPU的架构，你才能更好地理解CPU是如何执行指令的。CPU的架构图如下所示：

![](https://static001.geekbang.org/resource/image/a4/7f/a418fbfc23d96aeb4813f1db4cbyy17f.jpg?wh=2598%2A1617 "CPU架构")

你可以直观地看到，对于现代处理器而言，一个实体CPU通常会有两个逻辑线程，也就是上图中的Core 0和Core 1。每个Core都有自己的L1 Cache，L1 Cache又分为dCache和iCache，对应到上图就是L1d和L1i。L1 Cache只有Core本身可以看到，其他的Core是看不到的。同一个实体CPU中的这两个Core会共享L2 Cache，其他的实体CPU是看不到这个L2 Cache的。所有的实体CPU会共享L3 Cache。这就是典型的CPU架构。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（6） 💬（0）<div>课后作业答案：
- 这节课的作业就是我们前面提到的思考题：在psi: Move PF_MEMSTALL out of task-&gt;flags这个 PATCH 中，为什么没有考虑多线程并行操作新增加的位域（in_memstall）时的竞争问题？
评论区很多同学回到的都很好。
因为新增的位域（in_memstall）只有current会写，而其他线程是只读，所以不存在并行写的问题，也就是没有竞争。</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/a9/3177e3ac.jpg" width="30px"><span>sufish</span> 👍（10） 💬（2）<div>1.不用考虑多线程并发访问：是因为调度机制已经保证了同一时间同个线程只会有一个cpu处理，相当于同一时间只会有一个cpu访问task_struct ，所以就避免了并发访问的问题？
2.关于Cache 伪共享问题的问题，是否可以考虑在全局变量的前面进行空填充，让这个变量在一个cache line里除了他之外，其他的变量都是占位用的。我猜 ____cacheline_aligned; 实际上也是干这个事</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（5） 💬（2）<div>课后思考题,如果不是老师的提示,估计我们是没法理解的了.
由于PF_*可能被其他线程写,而task_struct只能被当前运行的线程写,所以这样更改后最终的效果都一样,但是避免了写时冲突的可能.

我有两个疑问:
1. 这样调整后,实际的性能有多少提升呢?
   写时冲突是减少了,但读时,理论上还是可能引发类似伪共享的问题吧.
   (由于我对内核不太了解,也不清楚`current-&gt;flags`与`current-&gt;in_memstall`在其他地方被使用的频率.还请老师见谅)

2. 如何获取patch的更多上下文信息呢?
   老师对内核提交了很多patch,我很是佩服.
   每次commit的message也写的比较详细了.
   但我还是想了解更多相关的信息,比如别人的一些讨论,中间做过的一些尝试等等.
   目前老师附带的链接中只能看到`Link`(https:&#47;&#47;lkml.kernel.org&#47;r&#47;1584408485-1921-1-git-send-email-laoar.shao@gmail.com)
   由这个Link可以查看到`Subject`,`Message-ID`.
   但尝试了很久也没找类似issue的讨论信息.

   由于linux内核维护有自己的一套流程,好像走的邮件列表,我们外行对这些不太了解.
   如果老师觉得这个问题太简单的话,能否给一个学习资料,便于我们去学习和入门如何获取更多的patch相关信息?</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>老师的思考题，我的想法是这个in_memstall 的位域，是每个线程独享（排它）一个位域么？这样每个线程可以独立操作其所属位域，不存在竞争了。不知理解是否正确？</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（0） 💬（0）<div>请教一下邵老师：经常看到CPU高，而IPC不高，说是性能问题，这种是不是跟cache miss有关呢?另外使用perf之类的需要对PMU这些有所了解，请问有这块的资料推荐吗？</div>2020-11-17</li><br/>
</ul>