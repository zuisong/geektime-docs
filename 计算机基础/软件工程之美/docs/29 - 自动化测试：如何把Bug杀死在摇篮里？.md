你好，我是宝玉。前不久我所在项目组完成了一个大项目，把一个网站前端的jQuery代码全部换成React代码，涉及改动的项目源代码文件有一百多个，变动的代码有几千行，最终上线后出乎意料的稳定，只有几个不算太严重的Bug。

能做到重构还这么稳定，是因为我们技术水平特别高吗？当然不是。还是同样一组人，一年前做一个比这还简单的项目，上线后却跟噩梦一样，频繁出各种问题，导致上线后不停打补丁，一段时间才逐步稳定下来。

这其中的差别，只是因为在那次失败的上线后，我们总结经验，逐步增加了自动化测试代码的覆盖率。等我们再做大的重构时，这些自动化测试代码就能帮助我们发现很多问题。

当我们确保每一个以前写好的测试用例能正常通过后，就相当于把Bug杀死在摇篮里，再配合少量的人工手动测试，就可以保证上线后的系统是稳定的。

其实对于自动化测试，我们专栏已经多次提及，它是敏捷开发能快速迭代很重要的质量保障，是持续交付的基础前提。

所以今天我将带你一起了解什么是自动化测试，以及如何在项目中应用自动化测试。

## 为什么自动化测试能保障质量？

自动化测试并不难理解，你可以想想人是怎么做测试的：首先根据需求写成测试用例，设计好输入值和期望的输出，然后按照测试用例一个个操作，输入一些内容，做一些操作，观察是不是和期望的结果一致，一致就通过，不一致就不通过。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/d5/db/3f9499d1.jpg" width="30px"><span>勇闯天涯</span> 👍（19） 💬（1）<div>请教老师，我现在做的是嵌入式设备，要跟很多硬件外设打交道，这块的自动化测试和持续集成有什么好的建议吗？我看到文章中大多提到的都是互联网相关的方法和工具</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（8） 💬（1）<div>.net core 的同學，我們項目使用 NUint 進行單元測試，集成測試可以使用 WebApplicationFactory，模擬工具可以使用 Moq</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/ec/0539c89d.jpg" width="30px"><span>易林林</span> 👍（8） 💬（1）<div>请教宝玉老师：团队成员的能力和素质参差不齐，如何有效的去组织和管理项目的自动化测试，自动化集成？</div>2019-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/c2/1740f435.jpg" width="30px"><span>Joey</span> 👍（5） 💬（1）<div>请教宝玉老师：
消息类接口应该通过哪种方式高效、有效维护？

现状：
系统A属于联机类系统（高并发、低延迟），其中接口B与多个应用相关，当接口B的定义发生变化时，往往忘记通知相关方或者漏通知，从而引发生产事件。

尝试过的手段：
1、通过流程约束，需求评审阶段，强制增加是否有接口变化的评审，但是落实结果不理想，主要因为增加流程，开发人员嫌浪费精力，最后流于形式。
2、通过自动化手段约束，原则上要求接口必须在CI阶段有自动化用例守护，但是效果也不理想，自动化用例缺失或者开发人员懒的写自动化用例，最后流于形式。（我们部门研发和测试属于不同的团队，所以开发人员对于代码质量，都指望测试人员守好最后一道关卡。）</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/ae/66ae403d.jpg" width="30px"><span>熊猫</span> 👍（4） 💬（1）<div>老师你好，请问下有没有介绍开发如何写好测试不错的书？</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（3） 💬（1）<div>1，小型、中型、大型自动化测试是不是对应单元、集成、系统测试。2、现在测试金字塔模型已经被防锤模型替代了，GUI自动化减少，Interface自动化测试增多。3、有没有必要小、中、大型自动化测试覆盖率均达到100％？4、开头你们前端改造项目自动化测试釆用GUI还是Interface？若是GUI，有多少个测试用例，每个测试用例执行时间有多长，所有测试用例执行有多长。若是Interface ，如何测试前端？5、前端有没有自动化测试框架？</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/47/a4be64d8.jpg" width="30px"><span>Liber</span> 👍（3） 💬（1）<div>宝玉老师你好，有个地方感觉有必要再展开谈谈：
以本文注册用户为例，本文分别对这个case写了小、中、大型测试用例，但实际开发过程中，如何权衡对一个场景是该小、中、大都写，还是只写部分？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（3） 💬（1）<div>宝哥，我想问一下：
1.开发哪些测试需要自己写的呀， “测试驱动开发”的概念，开发应该要会写测试吧？
  到底要求会写哪些测试？
2.现中小公司都没有自动化测试工程师，写好测试手工检查的多，怎搞？
  开发学一点selenium3自动化测试之类会不会好点？
3.单元测试是不是数据越简单越好，最好不使用数据库，在dao层组或map
4.集成测试和大型测试用数据库则比较好，对吗？</div>2019-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/68/821e1855.jpg" width="30px"><span>Zebin</span> 👍（2） 💬（2）<div>宝玉老师，请教下，我们现在LINUX环境下开发项目，主要编程需要是C&#47;C++。
现在想搭建持续集成开发环境，有什么合适的工具可以推荐下吗</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/87/7604d7a4.jpg" width="30px"><span>起而行</span> 👍（2） 💬（1）<div>老师，持续集成怎么理解呢，我看知乎上说就是团队成员在一天内多次进行编译，发布或自动化测试</div>2019-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2Q5YYVUmVHh9yT84P1uib637fPAwUCaxrUujFJnslfa6MuuTCyXl7kodgokd6DAHsYzrib38ztjlXgGR7k3RIOjA/132" width="30px"><span>wanghua</span> 👍（1） 💬（1）<div>对于集成测试，接口测试，契约测试等概念，还是不太理解他们差别在哪里，老师是怎么理解的呢？</div>2020-04-02</li><br/><li><img src="" width="30px"><span>Sam</span> 👍（1） 💬（2）<div>您好，请问下，我在.net framework平台下，单元测试工具如何选择（能与jenkins接合的）</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（1） 💬（1）<div>老师你好，各种类型的测试覆盖率你们一般采用什么指标？个人感觉在理想的情况下最好是做到百分百覆盖率</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/53/5d/46d369e5.jpg" width="30px"><span>yellowcloud</span> 👍（1） 💬（1）<div>宝玉老师，我们现在使用的框架是.net core,语言是C#，用其进行后端开发。能否推荐一下好的自动化测试框架。我根据您的检索方法语言+自动化测试框架找到的是RedwoodHQ，不知道它在实际使用中是否可行。</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（1） 💬（1）<div>看到bug我又想起了网站安全，宝哥，像我们中小公司网站安全也是运维负责的
一般网站安全怎做呀？如果服务器linux(centos)被入侵一般怎么查别人是怎么入侵的？
宝哥您了解这方面的吗？小公司运维真是什么都做，打杂的~~</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/bd/80f587ad.jpg" width="30px"><span>丿淡忘</span> 👍（1） 💬（1）<div>宝玉老师，我想问一下，针对桌面开发的界面自动化测试一般是怎么进行的</div>2019-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2Q5YYVUmVHh9yT84P1uib637fPAwUCaxrUujFJnslfa6MuuTCyXl7kodgokd6DAHsYzrib38ztjlXgGR7k3RIOjA/132" width="30px"><span>wanghua</span> 👍（0） 💬（1）<div>对于单元测试，需要每个函数都写吗，这样工作量好大，有什么方法确定哪些该写，哪些不用写呢？</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/21/41823347.jpg" width="30px"><span>Harold</span> 👍（0） 💬（1）<div>是否能执行自动化测试，完全看带团队的Leader，很多Leader不给开发留写测试代码的时间，开发进度又很赶，程序员根本没时间写。等项目上线了，大家都忽略了</div>2020-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6Be8vjNk03LEXMl52vONOQvdKTL1MWPR6OsAGEDsHIZXw9FibW8c4YtNL6HAmB8wRkDNIEx15xawJ9PWLW4y1UA/132" width="30px"><span>董飞</span> 👍（0） 💬（1）<div>老师，开发把自动化做了，还要我们测试干什么？自动化测试一般都是测试做的啊？</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/f6/07ca7f70.jpg" width="30px"><span>miketan</span> 👍（0） 💬（1）<div>我们项目中主要是通过单元测试和集成测试来做自动化测试。单元测试主要做最外层的代码覆盖率要求。</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>自动化测试，一定要配合好持续集成，才能最大化发挥其效用。--记下来</div>2022-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/2f/f4adcb41.jpg" width="30px"><span>。。。</span> 👍（0） 💬（0）<div>老师，一般，都比较常看哪些网站的文章</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/16/99/71f159ed.jpg" width="30px"><span>Ho</span> 👍（0） 💬（0）<div>老师讲的真好！</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（0） 💬（0）<div>老师你好 之前我遇到的开发流程是本地代码修改完毕后 本地构建 构建过程中会跑单元测试 没问题后 再提交分支 然后再发起pull request 合进代码线后 jekins会触发一次与提交代码相关的服务的构建 这个过程中会构建代码并且跑单元测试  如果没过 服务会挂掉。 我想问下如果这里要加业务模块的自动化测试的话 也是在这次构建中执行的么? 还有我看老师你说的好像是单元测试或者自动化测试未通过是不允许合并主干的  但是我们之前是合并主干之后才去跑测试 这里是不是存在问题?</div>2021-01-24</li><br/>
</ul>