回顾之前讲的内容，原理篇重在建立直观理解，帮你建立信心，这是第一轮的认知迭代。应用篇帮你涉足应用领域，在解决领域问题时发挥编译技术的威力，积累运用编译技术的一手经验，也启发你用编译技术去解决更多的领域问题，这是第二轮的认知迭代。而为时三节课的算法篇将你是第三轮的认知迭代。

在第三轮的认知迭代中，我会带你掌握前端技术中的核心算法。而本节课，我就借“怎样实现正则表达式工具？”这个问题，探讨第一组算法：**与正则表达式处理有关的算法。**

在词法分析阶段，我们可以手工构造有限自动机（FSA，或FSM）实现词法解析，过程比较简单。现在我们不再手工构造词法分析器，而是直接用正则表达式解析词法。

你会发现，我们只要写一些规则，就能基于这些规则分析和处理文本。这种能够理解正则表达式的功能，除了能生成词法分析器，还有很多用途。比如Linux的三个超级命令，又称三剑客（grep、awk和sed），都是因为能够直接支持正则表达式，功能才变得强大的。

接下来，我就带你完成编写正则表达式工具的任务，与此同时，你就能用正则文法生成词法分析器了：

**首先，**把正则表达式翻译成非确定的有限自动机（Nondeterministic Finite Automaton，NFA）。  
**其次，**基于NFA处理字符串，看看它有什么特点。  
**然后，**把非确定的有限自动机转换成确定的有限自动机（Deterministic Finite Automaton，DFA）  
**最后，**运行DFA，看看它有什么特点。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/3f/06b690ba.jpg" width="30px"><span>刘桢</span> 👍（13） 💬（1）<div>尤雨溪:会编译原理真的可以为所欲为</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（8） 💬（2）<div>老师：为什么NFA要加空转换这样的操作呢，感觉对表达能力并没有扩展。</div>2019-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4OvKiaF14CVnpTUEibC06vyicltuXrXWKB44K1UERgrzJgVShHiaoicBSvWdQFEGqYHEL0k53GeXRKwpCmiaYof4NMTQ/132" width="30px"><span>漠北</span> 👍（4） 💬（1）<div>感觉很像递归转成动态规划</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/96/251c0cee.jpg" width="30px"><span>xindoo</span> 👍（4） 💬（1）<div>https:&#47;&#47;github.com&#47;xindoo&#47;regex  我用java写了个正则引擎，包含了老师这节讲的内容，readme中附了博客，欢迎各位查阅。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/11/80/730acb11.jpg" width="30px"><span>维李设论</span> 👍（1） 💬（1）<div>这里的柯林闭包和js中的闭包有什么关系吗？mdn中的定义是函数及其环境的混合，我理解的是js中的闭包是对理算数学中柯林闭包的扩展，推到极致是可以用集合去解释的，不知道我理解的对不对</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9d/9a/4cf0e500.jpg" width="30px"><span>芒果</span> 👍（1） 💬（1）<div>讲的深入原理，收益匪浅，NFA转DFA可以用子集法</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/ae/46ae526f.jpg" width="30px"><span>醉雪飘痕</span> 👍（1） 💬（1）<div>请问老师，您的图是用什么工具做得呀？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（1） 💬（2）<div>感觉NFA的匹配很适合并行啊，如果对于每个转换条件，开个线程并行匹配，这样就不需要回溯了，是不是能提升不少效率，虽然浪费了一些算力</div>2019-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/J3dqALgicfVklewMjVkpyLbTk9YiamnBf5QQZ3NPHGlMeVSdLDB5yHLicEZHKBbUets76KOFwbl9ju0xJw1VeGa1A/132" width="30px"><span>飞翔</span> 👍（0） 💬（1）<div>老师NFA2DFA这个函数的这一行dfaState = findDFAState(dfaStates, nextStateSet);中的nextStateSet是不是应该是calculatedClosures这个？还有，这一节的代码怎么运行啊，一直编不过</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/0a/7f9c476b.jpg" width="30px"><span>余晓飞</span> 👍（0） 💬（1）<div>文中代码块
int | [a-zA-Z][a-zA-Z0-9]* | [0-9]*
最后一个字符*应该是+
</div>2019-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/J3dqALgicfVklewMjVkpyLbTk9YiamnBf5QQZ3NPHGlMeVSdLDB5yHLicEZHKBbUets76KOFwbl9ju0xJw1VeGa1A/132" width="30px"><span>飞翔</span> 👍（0） 💬（2）<div>老师，这一节的代码怎么运行，GrammarNodeType没有找到定义的地方</div>2019-09-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLU70sUuWXN8aUViaIDMcuFT1uPvlKFk4dsceFNLNdNnUjQbNmHUZwFxDAnpm6dJHyOR0Q47Q2hpmw/132" width="30px"><span>Geek_dba6ea</span> 👍（0） 💬（1）<div>第一次从这个层面理解了贪心正则匹配</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（2） 💬（0）<div>理解了一点</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/05/ca9ce3e9.jpg" width="30px"><span>bucher</span> 👍（1） 💬（0）<div>如果在dfa中加上通配符点号有什么好方法吗，我是在move里进行修改的，但是这样的话如果有大量正则表达式的时候，nfa转dfa很慢.</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>用Python实现了一版RE引擎：
https:&#47;&#47;github.com&#47;killua-killua&#47;RE-Engine

包含了这节课的内容 + 一个手写的 re parser</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/2e/376a3551.jpg" width="30px"><span>ano</span> 👍（0） 💬（1）<div>老师，这个 playScript 的前端，我想用 Go 把它实现出来，就当是把代码都练习一遍，你觉得会有什么问题么？</div>2021-10-09</li><br/>
</ul>