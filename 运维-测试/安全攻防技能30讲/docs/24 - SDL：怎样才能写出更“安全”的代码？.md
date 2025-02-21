你好，我是何为舟。

安全漏洞的源头是开发，只有当开发人员写出了包含安全漏洞的代码，黑客才有可乘之机。因此，如何保障开发写出更“安全”的代码，是安全防护工作中最关键的一环。

2004年，微软提出了SDL（Security Development Lifecycle，安全开发生命周期）。因为对安全和隐私的考虑贯穿了整个软件的开发进程，SDL能够帮助开发人员写出更“安全”的代码，在解决安全合规需求的同时，也能减少由安全问题带来的损失。

和安全标准一样，SDL本质上是一个宏观指导性质的框架。但是，它确实成为了很多公司建设安全开发体系的参照标准。各个公司依据微软的SDL标准，结合自身的实际情况，衍生出了适合公司自身发展的SDL。今天，我们就一起来学习，到底什么是SDL，以及SDL是如何让开发写出更安全的代码的。

## SDL中的基础概念

我们先来看一个软件开发中的经典概念：软件开发生命周期DLC（Software Development Life Cycle）（这个概念的英文缩写种类比较多，为了和SDL区分，我们用DLC代表软件开发生命周期）。SDL是以软件开发生命周期为基础发展成的安全框架，所以，了解DLC能够帮助我们更好地认识SDL。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（4） 💬（1）<div>1，SDL适用于敏捷和DevOps，若适用有什么不同之外，若不适用，那在敏捷和DevOps下又有什么框架（据我学习，DevOps包括开发、测试、运维、安全的统一)2，我是一个从事二十年的测试人员，您认为安全测试应该由测试人员来作好还是安全人员来作，当然包括测试分析、设计、准备、执行及报告各个测试阶段。</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/0d/e16dff4e.jpg" width="30px"><span>瑞泉</span> 👍（4） 💬（2）<div>老师，持续集成工具，比如jenkins集成openvas漏扫工具是否可行，自动测试软件漏洞</div>2020-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HRj6TPD2IGzIvSvib8MRavM4nicqgZHB7h904VVg0SMWBaDvavPeicPhnQgoL3OoPnzlwGx7jy1qOtED3jMABkgpQ/132" width="30px"><span>Parko</span> 👍（1） 💬（1）<div>从原来注重开发管理的SDLC，到打通开发与运维隔阂的DevOps，在发展到DevSecOps，把代码安全扫描也加入到整个自动化发布过程中</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（0）<div>学习了：这块确实可以去研究一下；看来这块确实是我最后一块真正的弱点。去年的运维大会刚好有提及，然后发现确实这也是属于运维的一方面，一点点学习一点点补漏。</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（1） 💬（0）<div>SDL开发测试过程中可以集成一些插件漏洞检测工具，看看引入的第三方插件是否有已知的安全漏洞，比如之前文中提到的dependecy-check工具检查cve漏洞，最好是将这个工具集成到devops pipeline中，这样可以做到自动化的定期检查预警</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（1）<div>SDL要落地挺难的，特别是在大家都觉得安全很重要，却又不肯在安全上多投入的时候</div>2020-03-29</li><br/>
</ul>