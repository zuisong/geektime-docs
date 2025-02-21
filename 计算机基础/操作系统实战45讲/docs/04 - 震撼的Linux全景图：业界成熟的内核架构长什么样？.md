你好，我是LMOS。

什么？你想成为计算机黑客？

梦想坐在计算机前敲敲键盘，银行账号里的数字就会自己往上涨。拜托，估计明天你就该被警察逮捕了。真正的黑客是对计算机技术有近乎极致的追求，而不是干坏事。

下面我就带你认识这样一个计算机黑客，看看他是怎样创造出影响世界的Linux，然后进一步了解一下Linux的内部结构。

同时，我也会带你看看Windows NT和Darwin的内部结构，三者形成对比，你能更好地了解它们之间的差异和共同点，这对我们后面写操作系统会很有帮助。

## 关于Linus

Linus Benedict Torvalds，这个名字很长，下面简称Linus，他1969年12月28日出生在芬兰的赫尔辛基市，并不是美国人。Linus在赫尔辛基大学学的就是计算机，妻子还是空手道高手，一个“码林高手”和一个“武林高手”真的是绝配啊。

Linus在小时候就对各种事情充满好奇，这点非常具有黑客精神，后来有了自己的计算机更是痴迷其中，开始自己控制计算机做一些事情，并深挖其背后的原理。就是这种黑客精神促使他后来写出了颠覆世界的软件——Linux，也因此登上了美国《时代》周刊。

你是否对很多垃圾软件感到愤慨，但自己又无法改变。Linus就不一样，他为了方便访问大学服务器中的资源 ，而在自己的机器上写了一个文件系统和硬盘驱动，这样就可以把自己需要的资源下载到自己的机器中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（69） 💬（5）<div>NT是混合内核，内核相较于linux来说小，但是仍有一些模块在内核，也有相当多的模块在用户态。
架构额外清晰，也难怪几十年迭代都未曾大改大变</div>2021-05-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/a8PMLmCTCBa40j7JIy3d8LsdbW5hne7lkk9KOGQuiaeVk4cn06KWwlP3ic69BsQLpNFtRTjRdUM2ySDBAv1MOFfA/132" width="30px"><span>Ilovek8s</span> 👍（11） 💬（6）<div>NT内核是微内核，但是是混合内核结构，原因如老师讲的，NT内核里还有内核，内核之上是执行体，说明各内核上的系统组件都是以进程方式运行起来，并且通过消息传递来实现各系统组件的功能协作</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/45/9edd38ba.jpg" width="30px"><span>超级励辰</span> 👍（49） 💬（7）<div>确实有点颠覆自己的认知，一直以为Linux的内核时及其优秀且优雅的，然而并不是。反而一直觉得不稳定的Windows的内核时那么优雅。</div>2021-05-21</li><br/><li><img src="" width="30px"><span>Geek_e2256b</span> 👍（46） 💬（1）<div>看完这两节有些概念不清楚，想问问老师：
所以宏内核相当于所有的功能都耦合在一起，放在内核内
微内核是把大多数功能解耦出来，放在用户态，使用IPC在用户态调用服务进程
混合结构其实与微内核相似，只不过解耦出来的这些功能依然放在内核里，不通过IPC调用
想问一下老师这样理解是正确的吗？</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ea/72/78b8ad87.jpg" width="30px"><span>os</span> 👍（40） 💬（4）<div>高清全景图来源 https:&#47;&#47;makelinux.github.io&#47;kernel&#47;map&#47; ，在线可缩放，点击进源码</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/60/81/38b00111.jpg" width="30px"><span>Feen</span> 👍（27） 💬（4）<div>突然有点想笑，觉得很有意思，最近几年很火在linux上跑的微服务架构，本质对应在宏内核的架构上运行着微内核模式的微服务架构，好有意思。</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/37/72/fa5bf2b6.jpg" width="30px"><span>fw～繁闻</span> 👍（21） 💬（1）<div>一直以为linux的内核应该是最简单优雅的，window内核应该是极其复杂的，看了东哥的文章真是颠覆了我的认知。</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/b5/4159fa05.jpg" width="30px"><span>zhanyd</span> 👍（19） 💬（5）<div>这么说来Linux的内核架构相比较而言是最糟糕的咯？</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（13） 💬（7）<div>从just for fun读到：就像Linus自己说：没有篮球，没有暑假，没有约会。当然也与他的启蒙人密不可分，外公是大学的数学教授。
从用户体验来讲：
1. macOS流畅又稳定，已经10年的mbp 没有死机崩溃过，
2. Linux server也是超级稳定，虽然GUI偶尔无响应，但是在ALT+F1 到F7 下无敌。
3. 除了蓝屏还是蓝屏，或者C盘xx 文件不存在.
话糙理不糙：NT内核再优雅连花瓶都不如。既不中看又不中用。</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0f/4c/8f6d3b8d.jpg" width="30px"><span>陈宇鸣</span> 👍（13） 💬（1）<div>既然Linux是宏内核，宏内核中模块耦合性很高，那Linux是如何保证系统稳定性的呢？</div>2021-07-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM72LSGBkXDj3jpuhZp45mjwDDAJW6FS6PwtDjaTg03H64fhHyDAIrF9H8iazY3pM6earSr3cOu96ew/132" width="30px"><span>royalfarmer</span> 👍（11） 💬（3）<div>真是颠覆认知。以前只听人说Linux怎么怎么好，Windows怎么怎么差，其实主要是因Linux为开源，大家都能轻松接触到其内核，Windows不开源，研究其内核就有难度，造成了认知偏见。
免费的不一定是好的。不能人云亦云。如果Linux真的是最好又免费，应该属它发展最大才对。
客观理性，佩服老师</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/2c/b5/10141329.jpg" width="30px"><span>杰良</span> 👍（10） 💬（2）<div>Linux 内核的两个维度划分：
功能模块：human interface、system、processing、memory、storage、networking。
层次划分：user space interface、virtual、bridges、logical、device control、hardware interface、electronics。</div>2021-05-20</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（9） 💬（4）<div>Windows NT从设计架构上看属于微内核结构，HAL层之上的内核层属于微内核的核心，之上的执行体属于内核级别的应用层。Windows NT从权限的角度看属于宏内核，内核模式之下功能完备，并不是微内核那样单薄。这种设计兼顾了结构清晰和性能良好两个优点。但是老师，大互联公司用的基本是Linux服务器，微软自己hotmail转成Windows服务器也不顺利，这是为何呀？</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（8） 💬（6）<div>windows容易有病毒，linux很少有病毒，说明windows漏洞多</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（8） 💬（2）<div>一直用linux，有点神化linus了，确实需要对比，保持开放心态了解优秀的商业操作系统</div>2021-07-18</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（8） 💬（7）<div>nt的内核还是混合内核。
nt的图形部分是放在内核里的，这样设计是为了提供更快的响应么？
像在xp的时代3d加速必须使用DX来提供访问，vista后就可以任何窗体都有3d的特效，比如桌面的毛玻璃效果用了3d加速，为啥xp的桌面系统来实现同样效果却很困难？

对于apple的darwin系统图形系统是在用户态下的，这个是什么设计？而且在ios6系统之前是用3d拟物的操作界面丝毫无卡顿，这又是如何实现的？
现在的ios系统界面风格却越来越像android了。

linux下早期版本是用的x server的图像架构，现在也变化成了wayland和DRM的图像架构这是为什么？
同样使用linux内核的android却使用的是framebuffer的图形架构。这些又如何分析呢？
我们这课会不会讲2d gui驱动方面的知识？如何与这些商用操作上gui系统进行比较优劣呢？</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/d6/278ad881.jpg" width="30px"><span>大鱼Coo</span> 👍（7） 💬（3）<div>现在大型服务器，选择Linux，是因为性能高+免费么？</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ee/6d/387fd3d4.jpg" width="30px"><span>刘立超</span> 👍（7） 💬（1）<div>为什么linux的结构不能清晰点呢</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/27/d6/2fc30df6.jpg" width="30px"><span>爱媛宝</span> 👍（5） 💬（1）<div>不过Nt内核架构设计比linux优雅，为什么linux开源， 没有人取长补短去重构一个崭新的Linux 内核架构呢？还是我孤陋寡闻，其实已经有人在干这件事了？不过微软 目前反而在积极把自己生态向Linux 系统延伸。这是为什么呢？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/f3/22481a37.jpg" width="30px"><span>小样</span> 👍（5） 💬（1）<div>90后路过，99年小学三年级第一次上微机课，带鞋套，禁止带零食饮料，那年的电脑没有配鼠标，开机后照着黑板敲命令(居然还有全键盘操作的射击游戏)。四年级开始win98，有鼠标了。现在想来第一年的微机课应该就是ms-dos</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（4） 💬（1）<div>小节整理
04 | 震撼的Linux全景图：业界成熟的内核架构长什么样？
关于 Linus
Linux 内核
Darwin-XNU 内核
Windows NT 内核

评论区留存：
1. https:&#47;&#47;makelinux.github.io&#47;kernel&#47;
2. 关于问题：
1）NT是混合内核，内核相较于linux来说小，但是仍有一些模块在内核，也有相当多的模块在用户态。
架构额外清晰，也难怪几十年迭代都未曾大改大变
2）是上一节末尾提出的内核结构，混合内核，各个硬件平台自己实现HAL接口，可移植性很高
3）高内聚，低耦合，兼具宏内核与微内核特点，所以是混合内核
3. NT的图形性能是最好的 苹果次之，Linux最差
4. 一直用linux，有点神化linus了，确实需要对比，保持开放心态了解优秀的商业操作系统 &#47; 作者回复: 要对比 不要盲从
5. 微内核是把内核服务 变成了一个个进程
6. 《Just for fun》</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/dd/ed/f6c5432b.jpg" width="30px"><span>Geek_783504</span> 👍（4） 💬（1）<div>是上一节末尾提出的内核结构，混合内核，各个硬件平台自己实现HAL接口，可移植性很高</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（4） 💬（1）<div>迫不及待想再敲几行代码，完善一下自己的操作系统了，问一下老师下一次实践是啥时候。。</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/96/52c3eb53.jpg" width="30px"><span>Today</span> 👍（3） 💬（1）<div>突然觉得，宏内核就像写c程序时引用头文件，编译时候链接动态库&#47;静态库。而微内核就像写c程序使用dlopen来调用动态库。不知道这样理解是否正确？</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e9/80/dc1ec311.jpg" width="30px"><span>500: ServerError</span> 👍（2） 💬（1）<div>真的颠覆认知，我是也从 win 转向 max os；开发时也是接触 linux 最多；接触下来，感觉 win 使用感最差的。但是在看完这节课，又在反思，为什么 win 给我的使用感最差？貌似还是很多不良开发商的软件，导致 win 的使用感差；其实从商业角度就可以得出，这 3 个操作系统内核的优秀程度了。</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/d8/71ef5aa1.jpg" width="30px"><span>ChenJz</span> 👍（2） 💬（1）<div>那这样说是不是Linux的移植性比较差？</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/5d/fc51d4f9.jpg" width="30px"><span>Stephen</span> 👍（2） 💬（1）<div>真正的强者，敢于对世间规则说不，并勇于改变</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fd/1f/63ed5bd3.jpg" width="30px"><span>Dicky</span> 👍（2） 💬（1）<div>NT 是混合内核</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/5f/4cbcbfb9.jpg" width="30px"><span>hello</span> 👍（2） 💬（1）<div>深夜，我刚看完最后一讲准备睡觉，结果突然跳出个第四讲来😂老师辛苦了</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（2） 💬（2）<div>Linux 是不是也有微内核架构的呢？他们的层级是不是会比较清晰呢？</div>2021-05-17</li><br/>
</ul>