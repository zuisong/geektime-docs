你好，我是朱晔。

在[上一篇加餐](https://time.geekbang.org/column/article/224816)中，我们介绍了使用JDK内置的一些工具、网络抓包工具Wireshark去分析、定位Java程序的问题。很多同学看完这一讲，留言反馈说是“打开了一片新天地，之前没有关注过JVM”“利用JVM工具发现了生产OOM的原因”。

其实，工具正是帮助我们深入到框架和组件内部，了解其运作方式和原理的重要抓手。所以，我们一定要用好它们。

今天，我继续和你介绍如何使用JVM堆转储的工具MAT来分析OOM问题，以及如何使用全能的故障诊断工具Arthas来分析、定位高CPU问题。

## 使用MAT分析OOM问题

对于排查OOM问题、分析程序堆内存使用情况，最好的方式就是分析堆转储。

堆转储，包含了堆现场全貌和线程栈信息（Java 6 Update 14开始包含）。我们在上一篇加餐中看到，使用jstat等工具虽然可以观察堆内存使用情况的变化，但是对程序内到底有多少对象、哪些是大对象还一无所知，也就是说只能看到问题但无法定位问题。而堆转储，就好似得到了病人在某个瞬间的全景核磁影像，可以拿着慢慢分析。

Java的OutOfMemoryError是比较严重的问题，需要分析出根因，所以对生产应用一般都会这样设置JVM参数，方便发生OOM时进行堆转储：
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（15） 💬（1）<div>arthas的确很强，线上排查还真的爽，点赞</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4e/26/57eacd44.jpg" width="30px"><span>何嘉杰_JessyHo</span> 👍（11） 💬（1）<div>老师咨询一下，生产应用都打包成 docker 镜像跑在 k8s 集群中，镜像里面往往只有 jre ，jdk的工具乃至很多 linux 的命令都没有。这种情况下，如果出了异常，要怎样排查问题呢</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（10） 💬（1）<div>F**k, F**k, 太 powerful了，对于我这种小白来说，真的手把手教了，赶紧practice。哎，我工作10年了，以前写写C，最近3年才写java，真的越学越发现自己啥也不会，追赶呀，追赶！老师们，辛苦了。</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/ee/5ed997a6.jpg" width="30px"><span>devin.ou</span> 👍（7） 💬（2）<div>MAT发现Unreachable Objects Histogram的char[]占了3.6G, byte[]占了2.2G. 而且运行一段时间后, 这个Unreachable空间还会增长直接监控报警后手工重启应用.
这个与配置 -Xmx10g -Xms3g, 导致了GC不回收吗? 是否要将-Xms改少到1G, 才会GC回收. 或者有别的优化方式.</div>2020-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vK7WwQG23CI29w0iamcgetTicMdQ8NsJsQWSXIia3aSUbVE6dqfTiaVtqTdibJu31f7k2BkOSkQianxOUaqojEYP6ic3w/132" width="30px"><span>coffee</span> 👍（6） 💬（1）<div>老师，请教您一个问题，如果hprof堆转储文件过大，mat打不开，用什么办法来定位oom问题？</div>2020-04-30</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（3） 💬（1）<div>越觉得自己菜谢谢老师</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/f4/ce6acfc0.jpg" width="30px"><span>NARUTO</span> 👍（0） 💬（1）<div>metaspace oom原因比较好定位，就是定位到根本的代码行比较困难
</div>2023-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/70/f093eaf0.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（1）<div>老师，请问下，在线程池中使用threadlocal，作为二级缓存，但是有地方在使用后未及时清理该线程变量，导致内存泄露，用mat分析了下，但是没有详细引用链路，像您例子中那样可以看到具体是由那个类引发的，能帮忙给点意见吗？谢谢</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e9/d8/026493cc.jpg" width="30px"><span>vivi</span> 👍（14） 💬（0）<div>Arthas的代码热替换功能确实很香 但是还是有两个小问题  一个是没有权限控制  任何人都可以进行代码热替换操作  另一个就是代码热替换如果改错了 问题就不太好排查了</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（3） 💬（0）<div>以前用Eclipse 开发Android App的时候，遇到一些OOM，会跟着师傅一起用 MAT 排查，从不会用到使用，到一直使用一直爽的状态，排查了好多疑难杂症，真的很棒。老师讲的这个，又给我复习了一遍。

Arthas 真的强大，看评论去就懂了，所以感谢老师提供一个简短的教程，干就完事了</div>2020-10-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/k3YD3y3BzGDSdrwRJyJY4BXsNJibfM4uzOdDVKIAlFApR2FZCLg2ibrZtJ4vuahA3LHLW9GKzH5CMGqCDhWjhZqg/132" width="30px"><span>戒酒的李白</span> 👍（0） 💬（0）<div>真的很强大，收藏了</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（0） 💬（0）<div>明天尝试下热修功能</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（0） 💬（0）<div>厉害，以前没有想过的事情。</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/31/6f9f0145.jpg" width="30px"><span>꧁꫞꯭灯塔蟹꫞꧂</span> 👍（0） 💬（1）<div>公司线上禁止使用arthas怎么办呢</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/56/c6/0b449bc6.jpg" width="30px"><span>斐波那契</span> 👍（0） 💬（0）<div>老师 我想问一下 如何在容器里用arthas？ </div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/a4/fa0c13f1.jpg" width="30px"><span>阿怪</span> 👍（0） 💬（0）<div>不错，收藏先</div>2020-09-01</li><br/>
</ul>