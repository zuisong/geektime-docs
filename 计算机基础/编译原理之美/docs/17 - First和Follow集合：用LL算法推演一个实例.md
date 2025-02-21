在前面的课程中，我讲了递归下降算法。这个算法很常用，但会有回溯的现象，在性能上会有损失。所以我们要把算法升级一下，实现带有预测能力的自顶向下分析算法，避免回溯。而要做到这一点，就需要对自顶向下算法有更全面的了解。

另外，在留言区，有几个同学问到了一些问题，涉及到对一些基本知识点的理解，比如：

- 基于某个语法规则做解析的时候，什么情况下算是成功，什么情况下算是失败？
- 使用深度优先的递归下降算法时，会跟广度优先的思路搞混。

要搞清这些问题，也需要全面了解自顶向下算法。比如，了解Follow集合和$符号的用法，能帮你解决第一个问题；了解广度优先算法能帮你解决第二个问题。

所以，本节课，我先把自顶向下分析的算法体系梳理一下，让你先建立更加清晰的全景图，然后我再深入剖析LL算法的原理，讲清楚First集合与Follow集合这对核心概念，最终让你把自顶向下的算法体系吃透。

## 自顶向下分析算法概述

自顶向下分析的算法是一大类算法。总体来说，它是从一个非终结符出发，逐步推导出跟被解析的程序相同的Token串。

这个过程可以看做是一张图的搜索过程，这张图非常大，因为针对每一次推导，都可能产生一个新节点。下面这张图只是它的一个小角落。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（11） 💬（1）<div>Antlr中LL(k)中k是多少，是Antlr根据我们的文法动态决定的吗？还是老师文中说的那些写LL文法的注意点，我们在写Antlr文法的时候需要注意吗？Antlr会帮助我们自动处理这些吗？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/a6/3f15ba2f.jpg" width="30px"><span>czh</span> 👍（4） 💬（1）<div>今日份总结：今天是一个扫盲的学习，有以下两点总结

1.编译的过程：词法分析 语法分析 语义分析
1.1词法分析：读取的内容是字符，根据词法规则输出token。几乎不涉及语言的语法特性，是编译器的基础。
1.2语法分析:读取的内容是token，输出的是语法树AST。语言的表达式等功能又这部分中定义的上下文无关文法来实现。
1.3语义分析:操作的对象是AST，所谓语义主要完成上下文相关的推理逻辑，如类型问题，定义声明问题等

2.说说我对编译原理的初次见面感觉：编译原理相比于其他计算机基础知识而言，他的难主要集中在需要高度的对现实生活规则的抽象能力、逻辑思维能力，否则写不出没问题的上下文无关文法规则，以及无法发现、处理其中蕴含的一些“逻辑坑”，如左递归等问题。而一些其他的知识点，如算法部分，这些其实相比于抽象能力来说，就要简单、通用、好理解的多，更加考验你的编程基础，而不是脑子。</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（3） 💬（3）<div>还是不太明白为什么要有Follow集这个东西，如果First集中查找不到的话，直接将推导为ε，然后接着去推导下一个，如果发现不在下一个的First集中再报错，好像也不会有什么性能损失，那为什么要费那么大力气构建Follow集呢？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（1） 💬（1）<div>https:&#47;&#47;github.com&#47;moling3650&#47;Frontend-01-Template&#47;blob&#47;master&#47;week12&#47;ast.js
用JavaScript写了一个四则计算器，总算搞明白产生式和LL算法的对应关系了，这课真是太不容易了，对于一个前端来说。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/0a/7f9c476b.jpg" width="30px"><span>余晓飞</span> 👍（1） 💬（1）<div>下图是上述推导过程建立起来的 AST，“1、2、3……”等编号是 AST 节点创建的顺序
对这段话后前后两幅图有疑惑，前面一副图中的第4行是怎么直接到第5行的，
如果通过下面右递归版的产生式推导似乎省略了一步？
add -&gt; mul | mul + add
mul -&gt; pri | pri * mul
pri -&gt; Id | Num | (add) 

后面一幅图中节点8, 9, 10在节点12, 13之前生成，似乎这与前一幅图第6到8行的展开顺序不一致？</div>2019-10-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBThvjr88V0BVAOC4PicPUNPITZ2la5iciatFNYyicibcwicBjIaxElz77xsphqStrr81CSQeTXiaBVMTAA/132" width="30px"><span>Geek_f9ea2d</span> 👍（1） 💬（2）<div>老师好，对First集合我基本能理解，对Fllow集合的计算，我看的有点懵，这个方法：addToRightChild 为什么需要：把某个节点的Follow集合，也给它所有右边分枝的后代节点？</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/19/14018371.jpg" width="30px"><span>瓜瓜</span> 👍（0） 💬（1）<div>这个符号通常记做 $，意味一个程序的结束。比如在表达式的语法里，expression 后面可能跟这个符号，expression 的所有右侧分支的后代节点也都可能跟这个符号，也就是它们都可能出现在程序的末尾。但另一些非终结符，后面不会跟这个符号，如 blockstatements，因为它后面肯定会有“}”。
这一段看了好几遍，没有看懂，老师能不能再解释下？</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bf/81/4c45a87b.jpg" width="30px"><span>LeeR</span> 👍（0） 💬（1）<div>老师你好，$ 是不是就是EOF符号，表示程序和文件的结束？</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/0a/7f9c476b.jpg" width="30px"><span>余晓飞</span> 👍（0） 💬（1）<div>我把程序打印输出的 First 和 follow 集合整理如下（其实打印输出还包含一些中间节点，这里就不展示了）：

这段下面的图中 assign1 的First 集合应该包含 Epsilon</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/0a/7f9c476b.jpg" width="30px"><span>余晓飞</span> 👍（0） 💬（1）<div>expression  : assign ;
assign  : equal | assign1 ;
assign1 : &#39;=&#39; equal assign1 | ε;  

文中这里第二行 assign 是不写错了？
我看代码SimpleGrammar.java中有这一行GrammarNode assign = exp.createChild(&quot;assign&quot;, GrammarNodeType.And);
注释中刚好缺了关于assign的内容。</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/0a/7f9c476b.jpg" width="30px"><span>余晓飞</span> 👍（0） 💬（1）<div>这样就形成了四条搜索路径，分别是 mul+mul、add+mul+mul、add+pri 和 add+mul+pri。
这里最后一个是不是应该为add+mul*pri</div>2019-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（1）<div>https:&#47;&#47;github.com&#47;RichardGong&#47;PlayWithCompiler&#47;blob&#47;master&#47;lab&#47;16-18&#47;src&#47;main&#47;java&#47;play&#47;parser&#47;LLParser.java#L242</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/05/2cd96ff1.jpg" width="30px"><span>军</span> 👍（2） 💬（0）<div>first集合和子集构造法很像呢</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/7d/a6/15798bf2.jpg" width="30px"><span>温雅小公子</span> 👍（1） 💬（0）<div>那个pri结点应该是蓝色吧，他的子节点是或的关系。</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/a2/4ece341b.jpg" width="30px"><span>Ivan.Qi</span> 👍（0） 💬（0）<div>LL(1)算法
https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;675095121</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>哈哈，看到一愣一愣的</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/91/a017bf72.jpg" width="30px"><span>coconut</span> 👍（0） 💬（2）<div>和某评论一样有一个疑问，为什么要计算Follow集合？

似乎用First集合就可以实现不回溯的递归下降算法。

遇到下面的文法，如果token不在 First(+ mul add1) 中，就直接匹配 ε。也不一定要计算 Follow(add1)

  add1 -&gt; + mul add1 | ε
</div>2021-04-11</li><br/><li><img src="" width="30px"><span>yydsx</span> 👍（0） 💬（0）<div>class LLParser 里面的 241行   
   if (i == grammar.getChildCount()) {
                            rightChildren.add(left);
      }
是不是应为
   if (i == grammar.getChildCount()-1) {
                            rightChildren.add(left);
                        }
如果i == grammar.getChildCount()  那么花括号里面的代码将永远不会执行</div>2020-04-15</li><br/>
</ul>