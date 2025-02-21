在前面几篇文章中，我从页面操作的角度介绍了GUI自动化测试，讲解了页面对象模型和业务流程封装，今天我将从测试数据的角度再来谈谈GUI自动化测试。

为了顺利进行GUI测试，往往需要准备测试数据来配合测试的进行，如果不采用事先数据准备的方式，测试效率将会大打折扣，而且还会引入大量不必要的依赖关系。

以“用户登录”功能的测试为例，如果你的目的仅仅是测试用户是否可以正常登录，比较理想的方式是这个用户已经存在于被测系统中了，或者你可以通过很方便的方式在测试用例中生成这个用户。否则，难道你要为了测试用户登录功能，而以GUI的方式当场注册一个新用户吗？显然，这是不可取的。

其实从这里，你就可以看出测试数据准备是实现测试用例解耦的重要手段，你完全不必为了测试GUI用户登录功能而去执行用户注册，只要你能够有方法快速创建出这个登录用户就可以了。

在正式讨论测试数据的创建方法前，我先来分析一下GUI测试中两种常见的数据类型：

- 第一大类是，测试输入数据，也就是GUI测试过程中，通过界面输入的数据。比如“用户登录”测试中输入的用户名和密码就就属于这一类数据；再比如，数据驱动测试中的测试数据，也是指这一类。
- 第二大类是，为了完成GUI测试而需要准备的测试数据。比如，“用户登录”测试中，我们需要事先准备好用户账户，以便进行用户的登录测试。今天我分享的测试数据创建的方法，也都是围着这一部分的数据展开的。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/ed/db97ffe5.jpg" width="30px"><span>晴天</span> 👍（1） 💬（1）<div>hui测试的两类数据感觉没有什么区别，老师能详细说下嘛</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/af/3d/28b61e6b.jpg" width="30px"><span>假装乐</span> 👍（31） 💬（1）<div>数据库监控工具有推荐的吗</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（15） 💬（1）<div>是不是可以这么理解：
API 调用和数据库操作创建，本质上都是操作数据库，不过 API 调用是做了一层封装，保证了操作的可控性（避免胡乱写数据库操作语句）。
实时创建数据和事先创建测试数据，其实也是不冲突的，我理解他俩并不是互斥的关系，而是互为补充，在 API 调用逻辑内部，先检查数据库中是否存在需要的测试数据，存在则继续，不存在则创建即可。
欢迎沟通交流，公众号「sylan215」</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（7） 💬（0）<div>了解到的新知识：利用数据库监控工具获取一段时间内数据库所有的业务表修改记录，以此为依据得到创建数据的 SQL 语句集。

在自己实际工作中，自己曾经使用QTP来创建测试数据，都是准备给自己使用，所以数据量不大。

我在银行做测试，测试数据准备是一个很大的问题，测试的对公信贷系统对接了几十个系统，现在还是主要以手工准备数据为主。

虽然有一个造数平台，现在准备数据比以前方便了，但是还是做不到快速大批量造数。是手工在造数平台造数后，再在对公信贷手工引入数据。

至于使用API造数，现在也实现不了，项目中接口文档没有形成知识资产，有些接口找不到接口文档，不知道具体字段的含义，项目内没有安排人统一去梳理接口，估计难以使用API造数。

数据库改数，也是很困难。银行内有专门的环境组管理环境，一般人使用的数据库用户都只有查询权限，没有改数权限，只有在测试的时候，真的需要改数，得提单进行申请修改。而且不同系统间是不同的人管理。

做为测试，太复杂的SQL写不出来，也不了解具体要改哪些表、哪些字段，所以很多时候还是得找开发帮忙。</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/af/006ae50e.jpg" width="30px"><span>任大树</span> 👍（4） 💬（0）<div>老师讲的很清楚～～我有个小问题想请教一下：自动化做完 要进行数据还原，老师有没有什么数据还原的方法推荐呢？比如数据库快照什么的。或者说有哪些类型的自动化测试根本不用还原？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/39/f7dcc2e6.jpg" width="30px"><span>叶夏立</span> 👍（4） 💬（0）<div>我的做法是备份还原整个数据库😂，当然也是看业务场景的</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/26/154f9578.jpg" width="30px"><span>口水窝</span> 👍（3） 💬（0）<div>小公司，没有做GUI自动化测试，更无从测试数据的准备谈起，只能自己摸索，不断尝试，总结更多的实践经验。</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/35/2c56c29c.jpg" width="30px"><span>arthur</span> 👍（3） 💬（0）<div>我们的产品有一个best practice的包，里面包含了很多数据，对测试非常有用</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/53/1e/7d098b33.jpg" width="30px"><span>年轻人的瞎折腾^.</span> 👍（2） 💬（0）<div>我们是out the box 脚本预制 然后on the fly 接口调用，API测试，经常因为接口变动大，数据库也有变化 这样脚本经常容易改动 有什么方法可以设置变量方面，灵活性的脚本？</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cd/ec/0d1c052e.jpg" width="30px"><span>FamilyLi</span> 👍（2） 💬（0）<div>最近几张讲的GUI测试，听起来主要是基于浏览器的业务测试，对于APP的测试如何应用</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d1/b1/453434dd.jpg" width="30px"><span>Lynn</span> 👍（1） 💬（0）<div>数据库监控工具有推荐的吗</div>2018-12-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FGeCDgpXdhsXseIGF3GCzZibDJlOfO4KDqPJkMra2e0TJj3QVQk4t1oEd1BuQPtYOeavFyYxicd5fTZ33tIbPOZQ/132" width="30px"><span>付晓杰</span> 👍（0） 💬（0）<div>创建测试数据的方式：
一、从创建的技术手段上来讲，创建测试数据的方法主要分为三种：
1.API 调用（最佳的选择）；
2.数据库操作；
3.综合运用 API 调用和数据库操作。
二、从创建的时机来讲，创建测试数据的方法主要分为两种：
1.测试用例执行过程中，实时创建测试数据，我们通常称这种方式为 On-the-fly。
2.测试用例执行前，事先创建好“开箱即用”的测试数据，我们通常称这种方式为 Out-of-box。
对于创建数据的时机，在实际项目中，往往是 On-the-fly 和 Out-of-box 结合在一起使用</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（0）<div>先看了后面测试数据的4讲再来看这篇，就像是复习啦</div>2022-02-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSGx0Fcs4kajDDVHjxjC3R1ibE1VmTnzPibohSP6ySBzoesCRLicKA9ocTtkceV9UlV6pvUj1vuh9TQ/132" width="30px"><span>Geek_da7f5e</span> 👍（0） 💬（0）<div>老师，这部分GUI自动化测试课程学起来有点吃力，我有对日外包的开发基础但没有测试经验，还需要自己补些什么基础知识吗？听不太懂呢</div>2021-07-20</li><br/><li><img src="" width="30px"><span>nn_20160123</span> 👍（0） 💬（0）<div>你好，造数据有一部分是调用接口，我怎么确定这次部署的造数据接口是没问题的呢？</div>2020-03-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eottzJibUvjql0cDsfqpBvpibib0B4GhVTs81jgcpwic5pCFYlf6wYhibqUw05cGQtoRvRVib8HoKgibvr2A/132" width="30px"><span>Geek_AX1</span> 👍（0） 💬（0）<div>老师，我以前做过一个项目，测试数据我们直接copy一些现网数据来创造数据，尤其是性能测试高并发的时候，请问这个是不是一种好方法呢？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/bb/99/a10d145e.jpg" width="30px"><span>孙建伟</span> 👍（0） 💬（0）<div>并不矛盾，GUI自动化测试是基于功能稳定的情况下进行的！</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>1，本文中需要注意的是，这两种思路的前提都是，假定产品功能正确，否则就会出现“一错到底”的尴尬局面。一一－前题是产品功能正确，测试的目的是找到产品中的Bug，没觉得这有矛盾吗？
2，在自动化测试中，teatdown方法中往往作的最重要的事情是清除脏数据。但是自动化测试往往出现的状况是测试程序在测试过程中遇到问题，挂掉了，这样造成的结果是执行不了teatdown方法中清除脏数据的操作，从而影响其他用例的运行。我一般Have to在所有测试开始(setup方法)一开始都清除所有脏数据，保证此测试用例在干净环境下运行。请问作者没有别的好办法。</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/a7/c4de1048.jpg" width="30px"><span>涅槃Ls</span> 👍（0） 💬（0）<div>打卡15</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/44/c2d77269.jpg" width="30px"><span>hi ！girl</span> 👍（0） 💬（0）<div>在准备测试数据中，我觉得应该尽量减少第三方的依赖，避免脚本的不稳定性，也就是说能预先设定的就先考虑，不能的再采取实时产生的方式</div>2018-08-02</li><br/>
</ul>