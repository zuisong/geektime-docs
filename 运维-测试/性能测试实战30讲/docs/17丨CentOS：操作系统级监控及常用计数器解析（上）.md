我相信有一些人看到这篇文章的标题肯定有种不想看的感觉，因为这样的内容实在被写得太多太多了。操作系统分析嘛，无非就是CPU使用率、I/O使用率、内存使用率、网络使用率等各种使用率的描述。

然而因为视角的不同，在性能测试和分析中，这始终是我们绕不过去的分析点。我们得知道什么时候才需要去分析操作系统，以及要分析操作系统的什么内容。

首先，我们前面在性能分析方法中提到，性能分析要有起点，通常情况下，这个起点就是响应时间、TPS等压力工具给出来的信息。

我们判断了有瓶颈之后，通过拆分响应时间就可以知道在哪个环节上出了问题，再去详细分析这个操作系统。这就需要用到我们的分析决策树了。

你还记得我们[在第6篇文章](https://time.geekbang.org/column/article/182912)中提到的分析决策大树吗？今天我们单独把操作系统的这一环节给提出来，并加上前面说的细化过程，就可以得到下面的这个分析决策树。

![](https://static001.geekbang.org/resource/image/a1/f7/a130dc74013b8760dfca23a58fef1af7.jpg?wh=1696%2A1568)

在分段分层确定了这个系统所运行的应用有问题之后，还要记起另一件事情，就是前面提到的“全局—定向”的监控思路。

既然说到了全局，我们得先知道操作系统中，都有哪些大的模块。这里就到了几乎所有性能测试人员看到就想吐的模块了，CPU、I/O、Memory、Network…

没办法，谁让操作系统就这么点东西呢。我先画一个思维导图给你看一下。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（21） 💬（1）<div>不知道我理解得对不对，应用无非就是两种计算密集型和IO密集型，计算密集集就体现在CPU忙，IO密集型就体现在CPU空闲，我想接下来无非就是围绕这两种类型展开分析，所以说CPU是性能分析的方向性指标。</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/22/23/5bf30be6.jpg" width="30px"><span>potato</span> 👍（7） 💬（1）<div>现在 我们这边压测有一个指标，混合压测的时候，看cpu的使用率 超过60%的就定义为系统瓶颈，这个是不是不太合理呢</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（6） 💬（1）<div>swap是干嘛的？
在Linux下，SWAP的作用类似Windows系统下的“虚拟内存”。当物理内存不足时，拿出部分硬盘空间当SWAP分区（虚拟成内存）使用，从而解决内存容量不足的情况。

SWAP意思是交换，顾名思义，当某进程向OS请求内存发现不足时，OS会把内存中暂时不用的数据交换出去，放在SWAP分区中，这个过程称为SWAP OUT。当某进程又需要这些数据且OS发现还有空闲物理内存时，又会把SWAP分区中的数据交换回物理内存中，这个过程称为SWAP IN。

当然，swap大小是有上限的，一旦swap使用完，操作系统会触发OOM-Killer机制，把消耗内存最多的进程kill掉以释放内存。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（5） 💬（2）<div>做个内容小结：

1、操作系统需要监控的模块：CPU、I&#47;O、Memory、Network、System、Swap。
2、仅需四个命令就能监控以上6个模块：top、wmstat、iostat、netstat。
3、监控命令是可以监控到相应模块的计数器，而不是监控某个模块。对于监控命令，要知道它的局限性，并且要通过大量的练习来掌握。
4、监控的思考逻辑：因为需要监控某个计数器，才使用某个监控命令。（有点类似分析性能数据时，自己应该知道要从哪些数据入手，而不是把全部的数据看一遍）
5、CPU常用的8个计数器中，容易出现性能问题是以下四个计数器，排序按照频率由高到低：us、wa、sy、si。要分别构建分析决策树。CPU是重点分析对象。
6、为了保证分析方向的正确性，用perf top -g命令确定CPU用在哪里。（需要先安装perf）</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（4） 💬（1）<div>老师，1. 在落地si cpu 的时候 看interrupts的目的是什么，不能直接看softirqs吗 ？从interrupts--&gt;softirqs 这个判断逻辑是什么？ 2. 判断si 高低的逻辑和标准是什么？ </div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/8c/bc76ecd3.jpg" width="30px"><span>吴小喵</span> 👍（4） 💬（1）<div>8919 的模板导入没有成功呢，什么数据都出不了</div>2020-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sOvjoV6STk6SYPHRqVOo7ExojUbc4NgJAd7pGnyQQfJYFS97pYg744PNibalzy6gqZEicoHS2g6ibzK0OLhP6l0TA/132" width="30px"><span>喜哥</span> 👍（4） 💬（1）<div>你好，高老师，问下 如果应用部署在k8s上  ，用top或是vmstat等命令查看都是node节点的指标，如何精确排查应用问题导致的性能问题呢</div>2020-02-10</li><br/><li><img src="" width="30px"><span>学员141</span> 👍（3） 💬（2）<div>高老师好，最近压测集群的pod应用，发现pod的内存只会上涨不会释放，登录pod所在节点，根据命令（TOP PIDSTAT）监控pod应用对应的线程pid，内存也没有释放，这个有影响吗？我看内存长期在pod的limit下，也没有内存溢出</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/33/cdea4bca.jpg" width="30px"><span>zwm</span> 👍（3） 💬（1）<div>第二编读，有新收获</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/3e/abb7bfe3.jpg" width="30px"><span>浅浅</span> 👍（1） 💬（1）<div>PHP语言的us  CPU高，怎么分析呢？老师，求回复</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（1） 💬（1）<div>Perf top -g  怎么确定方向对不对可以展开详细说一下吗？后面有个例子也是用这个确定方向的，但是没看懂，跪求</div>2020-03-05</li><br/><li><img src="" width="30px"><span>甜芯儿</span> 👍（0） 💬（1）<div>听老师讲的最多的是，我实在不想展开讲开多，其实作为学生还是比较想听透彻了</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/de/80/791d0f5e.jpg" width="30px"><span>娜娜</span> 👍（0） 💬（1）<div>请问容器应用CPU高怎么去查看呢 文章中的命令top、nmon 等都是基于宿主机节点呢 看到的落在主机上面的所有应用，怎么看内部节点的CPU高呢</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/0f/a8/956452cd.jpg" width="30px"><span>蔚来懿</span> 👍（0） 💬（1）<div>老师，问下，CPU使用率达到多少才会引起我们的关注呢？网上资料一般都说75%以上，但是我这边在项目中发现，基本资源配置都比较好，CPU使用率或者说是整个服务器资源使用都不是很高，顶多50%，但这个时候就已经到达tps最大值了，这种情况下，是不是就能证明是应用本身的问题，还是我监控范围不够？</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/89/7d/01507d66.jpg" width="30px"><span>One Tester</span> 👍（0） 💬（1）<div>老师，请问一下,关于top命令中load average的值该怎么理解？看网上有两种说法：(1)load值除以逻辑CPU的数量，大于5就表明系统在超负荷运转了。(2)在评估cpu的性能优劣时完全照搬网上说的几倍几倍是不准确的，还得你自己动手看看vmstat显示的run值和blocked值，当出现明显较多的blocked的时候，就说明cpu产生了瓶颈。而top命令和uptime命令显示的负载均值，只能作为判断系统过去某个时间段的状态的参照，与cpu的性能关系不大</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/42/84/e0a6fc1c.jpg" width="30px"><span>wjh</span> 👍（0） 💬（3）<div>想知道，响应时间很短，但是cpu使用率又不高的现象的分析思路是什么？谢谢</div>2020-02-10</li><br/>
</ul>