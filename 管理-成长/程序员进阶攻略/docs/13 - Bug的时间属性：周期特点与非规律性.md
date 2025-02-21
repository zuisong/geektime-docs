在上一篇文章中，我说明了“技术性 Bug 可以从很多维度分类，而我则习惯于从 Bug 出现的 ‘时空’ 特征角度来分类”。并且我也已讲解了Bug 的**空间维度**特征：程序对运行环境的依赖、反应及应对。

接下来我再继续分解 Bug 的**时间维度**特征。

Bug 有了时间属性，Bug 的出现就是一个概率性问题了，它体现出如下特征。

## 周期特点

周期特点，是一定频率出现的 Bug 的特征。

这类 Bug 因为会周期性地复现，相对还是容易捕捉和解决。比较典型的呈现此类特征的 Bug 一般是资源泄漏问题。比如，Java 程序员都不陌生的 `OutOfMemory` 错误，就属于内存泄漏问题，而且一定会周期性地出现。

好多年前，我才刚参加工作不久，就碰到这么一个周期性出现的 Bug。但它的特殊之处在于，出现 Bug 的程序已经稳定运行了十多年了，突然某天开始就崩溃（进程 Crash）了。而程序的原作者，早已不知去向，十多年下来想必也已换了好几代程序员来维护了。

一开始项目组内经验老到的高工认为也许这只是一个意外事件，毕竟这个程序已经稳定运行了十来年了，而且检查了一遍程序编译后的二进制文件，更新时间都还停留在那遥远的十多年前。所以，我们先把程序重启起来让业务恢复，重启后的程序又恢复了平稳运行，但只是安稳了这么一天，第二天上班没多久，进程又莫名地崩溃了，我们再次重启，但没多久后就又崩溃了。这下没人再怀疑这是意外了，肯定有 Bug。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/66/2a/3bac3cec.jpg" width="30px"><span>sunny</span> 👍（9） 💬（1）<div>看得我惊心动魄，以前老是害怕bug出现，现在有点小期待；看看热闹，长长见识，毕竟还在初级，</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/fc/b8d83d56.jpg" width="30px"><span>Geek_e68th4</span> 👍（4） 💬（1）<div>少壮不遇bug，老大徒伤悲</div>2018-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/39/3168c4ca.jpg" width="30px"><span>二木🐶</span> 👍（3） 💬（1）<div>第一类bug的查找案例实在是不敢恭维，重要的正式环境这样去不断重启应用，加日志等方式简直就是不可能的</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/64/04/18875529.jpg" width="30px"><span>艾尔欧唯伊</span> 👍（3） 💬（1）<div>最近刚入职组里遇到的问题。。四个应用加一层设备，然后还有硬件资源紧张，合在一起出现的bug表象，基本就是各种展示数据不对。。。
有些提了缺陷，但是问题环境都没了。。复现都很难。。。真不容易。。</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/9e/99cb0a7a.jpg" width="30px"><span>心在飞</span> 👍（3） 💬（1）<div>我现在就遇到个海森堡bug, 客户现场出现过一次，在自己的服务器环境里一切正常，只能通过code review的方式做一些防御性编程，结果发现算法是老美算法专家92年写的！乱飞的point、各种业务处理算法，瞬间我就不想看了！</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/57/a9f9705a.jpg" width="30px"><span>无聊夫斯基</span> 👍（3） 💬（2）<div>需要这么多的逻辑判断的50ms的程序你是如何优化成3ms的？</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/46/df595e4a.jpg" width="30px"><span>CatTalk</span> 👍（3） 💬（1）<div>生动形象的讲解</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/56/ec/1c38b82c.jpg" width="30px"><span>香槟</span> 👍（2） 💬（1）<div>之前有遇到一个bug，关于redis序列化和反序列化的。线上有6台服务器，升级了其中一台服务器，内容是增加了调用链监控的程序。升级完先上线看效果。由于机子的aspnet版本需更新，同时更新了内部redis封装的库。前半天运行正常，然后出现部分列表数据不一致的情形。赶紧写了段程序输出值看下。发现值均变为0。看代码是反序列化出值部分。看正常的列表数据，反序列化有值。看库里，发现两者的区别是一种序列化进去有引号，另一种序列化进去没引号。没引号的能在其他5台机子解析，而有引号的只能在升级库中解析。所以定位到了原因。为了顺利上线监控程序，又能平滑升级，选择了调整封装库的序列策略，改为序列成无引号的方式。这才解决不一致的问题。</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（2） 💬（2）<div>迟到了。总算解决好学校的事情了。

心得如下

1，bug的时间属性：周期特点和非规律性


2，周期性出现，比如OutOfMemory，内存泄露。


3，非规律性，解决麻烦，采用工具，直接引入代码 Profiler 等性能剖析工具，就可以准确地找到有性能问题的代码段


4，神出鬼没，海森堡 Bug（Heisenbug）


5，bug的解决之道有两种，事前的，事后的。


6，事后，Bug 出现后，捕捉现场并定位解决的


7，事前进行预防和埋伏</div>2018-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（0）<div>目前在优化的一些缓存刷新的定时任务，就属于过几年可能会出Bug的代码（因为这代码就是几年前写的，现在出问题了）原因如下
1:缓存刷新的方式是先删后插

2:我厂的统一规定不允许数据物理删除

3:经久年月，无效数据越来越多，原来缓存刷新没问题，后来就有了空窗期，在空窗期内访问缓存就会出现问题了
</div>2018-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（1） 💬（0）<div>1. 应对时间变迁带来的变化，定时检查
2. debug很考验基本功
3. 遇到灵异事件，掂量一下自己能不能兜住，兜不住的话及早上报，免得挨板子</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/26/2e9bc97f.jpg" width="30px"><span>今之人兮</span> 👍（1） 💬（0）<div>周期性bug 非规律性bug和海森堡bug，周期性的bug因为复现很容易会比较好解决。非规律性的虽然没有特殊规律。但是bug一直存在总会找到如何解决。海森堡bug难以浮现没有规律。可能随着代码量的增加以及代码深度理解可以有效避免这类bug</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/93/6fef7aaa.jpg" width="30px"><span>石头</span> 👍（0） 💬（0）<div>时间类Bug种类：周期、非规律、海森堡。
解决：事后与事前。事后：根据逻辑、性能工具等进行分析与定位案发现场[预防与埋伏]，然后解决之；事前：运维代码证，帮助发现、诊断、甚至抵御bug。</div>2018-09-05</li><br/>
</ul>