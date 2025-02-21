你好，我是高楼。

这节课我们接着来“玩”一下用户登录。在[第10讲](https://time.geekbang.org/column/article/362010)的课程中，我们以登录功能为例做了一些分析，来说明基准场景中的一些要点。但是，我们还没有把它优化完，所以这节课还要接着来折腾它。

用户登录说起来只是一个很普通的功能，不过它的逻辑一点也不简单。因为登录过程要对个人的信息进行对比验证，验证过程中又要调用相应的加密算法，而加密算法是对性能要求很高的一种功能。复杂的加密算法安全性高，但性能就差；不复杂的加密算法性能好，但安全性低，这是一个取舍的问题。

另外，还有Session存储和同步。对于个大型的系统来说，不管你在哪个系统访问，在调用其他系统时如果需要验证身份就要同步Session信息，并且在做业务时，我们也要把相应的Session信息带上，不然就识别不了。

你看，登录功能实际上会涉及到很多的业务，它其实一点也不简单。所以，这节课我会带着你好好分析用户登录功能，并带你了解在压力过程中业务逻辑链路和整体TPS之间的关系。同时，也希望你能学会判断线程中的BLOCKED原因。

## 修改加密算法

还记得在[第10讲](https://time.geekbang.org/column/article/362010)中，我们在基准场景中对登录业务的测试结果吗？在10个压力线程下，TPS达到了100左右。

![](https://static001.geekbang.org/resource/image/e4/28/e487d4cc5eb67d58b6afc9e11eba7b28.png?wh=1208%2A255)

同时，在[第10](https://time.geekbang.org/column/article/362010)[讲](https://time.geekbang.org/column/article/362010)中，我们发现了加密算法BCrypt效率低之后，讨论了两种优化方式：一种是用更快的加密方式，另一种是去掉这个加密算法。当时，我选择把加密算法BCrypt直接去掉。在这节课中，我们来试试第一种方式，把它改为MD5，具体有两个动作：
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/77/2f708e02.jpg" width="30px"><span>继贤</span> 👍（5） 💬（1）<div>老师，堆栈分析工具用的是哪个？</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/fb/84/a1f866e7.jpg" width="30px"><span>涵涵</span> 👍（2） 💬（1）<div>基准测试中将缓存全部直接加载，那容量测试中也会将缓存直接全部加载吗？直接加载缓存不是对测试结果有影响吗？</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/3e/abb7bfe3.jpg" width="30px"><span>浅浅</span> 👍（2） 💬（1）<div>我们抓两段栈出来看一下，找一下锁之间的关系：
老师，这个是用什么抓取的呀？</div>2021-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（1） 💬（1）<div>老师，请问下，压测都是发请求到网关？为啥不是nginx呢？</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e4/e1/d1bf83c9.jpg" width="30px"><span>公瑾</span> 👍（1） 💬（1）<div>想抓 BLOCKED 状态的线程，并且线程描述是“Waiting on monitor”
--老师，是不是有阻塞的时候，先看block的线程是等待哪些锁，然后再去Waiting on monitor里查看是哪些线程持有这些锁(另外runnale的需要查看吗？)</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/2b/8cdad638.jpg" width="30px"><span>udsmdd</span> 👍（1） 💬（1）<div>老师，服务的消耗时间是怎么算。　</div>2021-06-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4PVUh26DjhjaV390eLR430aH6YCMJTvcaTGsCjqFoDnpGlP8DkSargr74efRSicwnTWNmjnPntTlQ/132" width="30px"><span>街角的风铃</span> 👍（0） 💬（3）<div>有项目源代码地址吗？，我想部署一下</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e0/e2/6054de3f.jpg" width="30px"><span>*回眸*·wdlcoke</span> 👍（0） 💬（1）<div>老师:
       怎么加载缓存？</div>2021-12-30</li><br/><li><img src="" width="30px"><span>wfw123</span> 👍（0） 💬（1）<div>老师 打印栈的时候，是在脚本运行时候还是运行结束后呢</div>2021-07-10</li><br/>
</ul>