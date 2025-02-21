你好，我是徐文浩，今天是第二期FAQ，我搜集了第3讲到第6讲，大家在留言区问的比较多的问题，来做一次集中解答。

有些问题，可能你已经知道了答案，不妨看看和我的理解是否一样；如果这些问题刚好你也有，那可要认真看啦！

希望今天的你，也同样有收获！

* * *

## Q1：为什么user + sys运行出来会比real time多呢？

![](https://static001.geekbang.org/resource/image/36/4c/3665db1602c971c2cad1932ee8d0804c.png?wh=1125%2A1918)

我们知道，实际的计算机运行的过程中，CPU会在多个不同的进程里面切换，分配不同的时间片去执行任务。所以，运行一个程序，在现实中走过的时间，并不是实际CPU运行这个程序所花费的时间。前者在现实中走过的时间，我们叫作real time。有时候叫作wall clock time，也就是墙上挂着的钟走过的时间。

而实际CPU上所花费的时间，又可以分成在操作系统的系统调用里面花的sys time和用户态的程序所花的user time。如果我们只有一个CPU的话，那real time &gt;= sys time + user time 。所以，我当时在文章里给大家看了对应的示例。

不过，有不少同学运行出来的结果不是这样的。这是因为现在大家都已经用上多核的CPU了。也就是同一时间，有两个CPU可以同时运行任务。

你在一台多核或者多CPU的机器上运行，seq和wc命令会分配到两个CPU上。虽然seq和wc这两个命令都是单线程运行的，但是这两个命令在多核CPU运行的情况下，会分别分配到两个不同的CPU。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（2） 💬（1）<div>“user 和 sys 的时间是两个 CPU 上运行的时间之和，这就可能超过 real 的时间。”多核感觉运行会更快，为什么反而比单核user 和 sys的时间更多呢，并且超出real</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/57/31595f22.jpg" width="30px"><span>Lrwin</span> 👍（6） 💬（0）<div>这个专栏真的学到很多</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（4） 💬（0）<div>这几个加餐同样不能错过，徐老师分享了许多学习的方法和经验。
</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（3） 💬（0）<div>读书百遍 其义自见把 看不懂 就多读几遍把 </div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（3） 💬（0）<div>赞~</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（2） 💬（0）<div>这个自举有点意思</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f5/47/34822f40.jpg" width="30px"><span>烟云</span> 👍（1） 💬（0）<div>学习方法不错!赞!</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（0）<div>跟着老师一起精进。</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（1）<div>       老师提到了低电压其实只是和能熬有关而不省电，那么为何它能提升性能呢？
      想进一步求教老师一个问题；自己试过低电压的内存和常规的内存，为何主频一样但是就是明显的感觉笔记本的流畅性不同-尤其是加载虚机或者文件时，明显就是使用的时候感觉低电压顺畅一些，时间大概能节约大概20-30%左右。这是为何？希望老师提点。</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/6d/8b417c84.jpg" width="30px"><span>Wheat Liu</span> 👍（0） 💬（1）<div>还是不太懂，real time那块。单CPU顺序执行两条指令的时间，跟多CPU执行两条指令的时间然后加在一起，为什么会不一样，时间差在哪</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/f2/453d5f88.jpg" width="30px"><span>seker</span> 👍（0） 💬（0）<div>汇编语言不是一门统一的编程语言，不同的指令集对应不同的汇编语言。汇编语言会对应到指令集中的机器码，可以把汇编语言理解为机器码的一种“书写方式”。高级语言在转换为机器码的时候，需要用到编译器，而编译器是需要指定编译为哪种机器码的。

基于Q5，我总结后想提一个问题，自己先回答了下，不知是否准确。

【不同高级语言转换为机器码的时候，转换出的机器码，是否是一样的？】
我的理解是，如果你的CPU是Intel X86指令集，在指令集相同的情况下，不同高级语言转换出的机器码是一样的。如果CPU是不同的指令集，那么不同高级语言转换出的机器码是不一样的。</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/a8/a7aedb90.jpg" width="30px"><span>叶昊</span> 👍（0） 💬（0）<div>很有用的方法</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/f0/678e6643.jpg" width="30px"><span>赵捌玖</span> 👍（0） 💬（0）<div>打个卡哈哈哈哈哈</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/19/05a2695f.jpg" width="30px"><span>伟忠</span> 👍（0） 💬（0）<div>👍🏻👍🏻👍🏻</div>2019-08-23</li><br/>
</ul>