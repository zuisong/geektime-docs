今天我们来继续了解Java虚拟机的监控及诊断工具。

## eclipse MAT

在上一篇中，我介绍了`jmap`工具，它支持导出Java虚拟机堆的二进制快照。eclipse的[MAT工具](https://www.eclipse.org/mat/)便是其中一个能够解析这类二进制快照的工具。

MAT本身也能够获取堆的二进制快照。该功能将借助`jps`列出当前正在运行的Java进程，以供选择并获取快照。由于`jps`会将自己列入其中，因此你会在列表中发现一个已经结束运行的`jps`进程。

![](https://static001.geekbang.org/resource/image/c9/7e/c9072149fb112312cbc217acc2660c7e.png?wh=1280%2A894)

MAT获取二进制快照的方式有三种，一是使用Attach API，二是新建一个Java虚拟机来运行Attach API，三是使用`jmap`工具。

这三种本质上都是在使用Attach API。不过，在目标进程启用了`DisableAttachMechanism`参数时，前两者将不在选取列表中显示，后者将在运行时报错。

当加载完堆快照之后，MAT的主界面将展示一张饼状图，其中列举占据的Retained heap最多的几个对象。

![](https://static001.geekbang.org/resource/image/da/bf/da2e5894d0be535b6daa5084beb33ebf.png?wh=1920%2A1116)

这里讲一下MAT计算对象占据内存的[两种方式](https://help.eclipse.org/mars/topic/org.eclipse.mat.ui.help/concepts/shallowretainedheap.html?cp=46_2_1)。第一种是Shallow heap，指的是对象自身所占据的内存。第二种是Retained heap，指的是当对象不再被引用时，垃圾回收器所能回收的总内存，包括对象自身所占据的内存，以及仅能够通过该对象引用到的其他对象所占据的内存。上面的饼状图便是基于Retained heap的。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（7） 💬（1）<div>JVM GUI监控和检测工具
1:MAT
2:JMC
这两个没怎么用过，回头下载、安装、使用下，国庆回家了，雨迪老师还在匀速的前进，是不是课程是提前编写好，录制好，然后定时放出？无论怎么非常感谢，跟着老师确实学习了不少东西，最后两天补上拉下的课程。</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/c7/966b6b85.jpg" width="30px"><span>遇见未来</span> 👍（0） 💬（1）<div>老师您好，openjdk可以用JFR嘛，配置了好久没成功，如果不能有没有类似的工具推荐，谢谢😁</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（14） 💬（0）<div>能否分享下实际工作中发生内存泄露，使用MAT分析和定位的案例呢？</div>2018-12-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKVicSvNf6OFvv4m3ibfsYCIUxic41kODPa9cuGUJjPcBtryLBDljalIVUiaJKlkGEJtOMZ03XSFlx1w/132" width="30px"><span>fuyu</span> 👍（6） 💬（0）<div>要是能举几个例子结合工具排查就更好了。</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/c4/be9f44bb.jpg" width="30px"><span>阿武</span> 👍（6） 💬（0）<div>国庆也推送，大写的服。👍👍</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（5） 💬（0）<div>MAT是一个非常有用的工具，已经用它成功排查过内存泄露的问题。</div>2018-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（4） 💬（0）<div>之前在项目上遇到了这种情况：我们有一个服务专门处理XML，有明显的内存泄漏，运行一天后内存会有几十G，导出的内存快照也是几十G，但压缩后只有几百M。用MAT查看内存快照，发现都是空的。现在回想起来，是不是我们用的XML类库，用了直接内存？那直接内存的话，用什么方法可以查看内存泄漏的情况呢？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/61/4999fbc3.jpg" width="30px"><span>啸疯</span> 👍（2） 💬（0）<div>Idea中有jprofile插件可以用</div>2021-12-30</li><br/><li><img src="" width="30px"><span>Geek_e2a822</span> 👍（2） 💬（0）<div>最好有点实际项目中问题定位的示例，否则整篇这样的介绍很鸡肋</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/67/a1e9aaba.jpg" width="30px"><span>Roway</span> 👍（1） 💬（1）<div>能否分享下实际工作中发生内存泄露，使用MAT分析和定位的案例呢？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/99/91b58bf7.jpg" width="30px"><span>Tomy</span> 👍（0） 💬（1）<div>老师能否出一版jvm的书，市面上这方面的书太少了且不够系统和全面</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（0）<div>有木有相关的IDEA插件之类的，开发的时候测试观察JVM状况。</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（0） 💬（0）<div>过段时间不用，都忘了，再来看看</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（0）<div>下了VisualVM，结合官方文档，发现真的好用。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/67/a1e9aaba.jpg" width="30px"><span>Roway</span> 👍（0） 💬（1）<div>老师，不说一下IBM的两个分析工具吗？一个内存的一个CPU的</div>2019-06-26</li><br/>
</ul>