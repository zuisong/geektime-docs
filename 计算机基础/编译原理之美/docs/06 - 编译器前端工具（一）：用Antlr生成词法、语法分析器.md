前面的课程中，我重点讲解了词法分析和语法分析，在例子中提到的词法和语法规则也是高度简化的。虽然这些内容便于理解原理，也能实现一个简单的原型，在实际应用中却远远不够。实际应用中，一个完善的编译程序还要在词法方面以及语法方面实现很多工作，我这里特意画了一张图，你可以直观地看一下。

![](https://static001.geekbang.org/resource/image/49/c1/49098ee32e1344550c41312862ec8ec1.jpg?wh=1142%2A429)

如果让编译程序实现上面这么多工作，完全手写效率会有点儿低，那么我们有什么方法可以提升效率呢？答案是借助工具。

编译器前端工具有很多，比如Lex（以及GNU的版本Flex）、Yacc（以及GNU的版本Bison）、JavaCC等等。你可能会问了：“那为什么我们这节课只讲Antlr，不选别的工具呢？”主要有两个原因。

第一个原因是Antlr能支持更广泛的目标语言，包括Java、C#、JavaScript、Python、Go、C++、Swift。无论你用上面哪种语言，都可以用它生成词法和语法分析的功能。而我们就使用它生成了Java语言和C++语言两个版本的代码。

第二个原因是Antlr的语法更加简单。它能把类似左递归的一些常见难点在工具中解决，对提升工作效率有很大的帮助。这一点，你会在后面的课程中直观地感受到。

而我们今天的目标就是了解Antlr，然后能够使用Antlr生成词法分析器与语法分析器。在这个过程中，我还会带你借鉴成熟的词法和语法规则，让你快速成长。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/b0/e30fd916.jpg" width="30px"><span>京京beaver</span> 👍（21） 💬（4）<div>1. windows环境下配置
可执行文件，放在D:\tools\antlr\antlr-4.7.2-complete.jar下面

2.配置环境文件
CLASSPATH=%CLASSPATH%;D:\tools\antlr\antlr-4.7.2-complete.jar
PATH=%PATH%n;D:\tools\antlr

3.手写文件antlr4.bat和grun.bat
antlr4.bat
java org.antlr.v4.Tool %*

grun.bat
@ECHO OFF
SET TEST_CURRENT_DIR=%CLASSPATH:.;=%
if &quot;%TEST_CURRENT_DIR%&quot; == &quot;%CLASSPATH%&quot; ( SET CLASSPATH=.;%CLASSPATH% )
@ECHO ON
java org.antlr.v4.gui.TestRig %*

4.然后就可以执行antlr4和grun命令了
比如antlr4 Hello.g4,  javac Hello*.java, 
$ grun Hello r -gui
hello parrt
^Z (windows) 

5.java执行路径要注意事项
在命令行执行java命令，记得把目录设置到src&#47;main&#47;java这里，然后输入包名.类名，才能找到。
这是java执行的基本规则，一般IDE里面替你做了路径转换，在命令行要自己敲入。切记。

例如
F:\study_repo\mygeek_time\myclang-03-grammar-analysis\src\main\java&gt;
grun com.babayetu.myclang03gramm
aranalysis.antlrtest.PlayScript expression -gui</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（6） 💬（1）<div>这一讲走的有点艰难，记录一下：

1、
开始执行下面的命令，报找不到 CommonLexer。

antlr PlayScript.g4

看了下 Github 才发现有这个文件。

import CommonLexer, 在语法规则文件 PlayScript.g4 中导入词法规则。

2、

antlr PlayScript.g4

上面的命令后应该先 cd .. 回退一级目录，再执行：

javac antlrtest&#47;*.java

或者，直接:

javac .&#47;*java

3、

grun antlrtest.PlayScript expression -gui

文中说执行这条命令结果会以图形化界面显示，我执行之后什么都没有输出，以为前面步骤有什么问题，重新来了一次，还是这样，往下看才意识到没输出才是正常的。。。

——

看到最后弹出的 AST 树还是蛮有意思的。

我写了一版简单的 Swfit 规则文件：

https:&#47;&#47;github.com&#47;iostalks&#47;PlayWithCompiler&#47;tree&#47;lecture-6&#47;PlayWithCompiler&#47;Antlr</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/d1/cc6f82eb.jpg" width="30px"><span>kaixiao7</span> 👍（4） 💬（1）<div>在Windows下需要用 ^z 即Ctrl+z 来弹出AST窗口

That ^D means EOF on unix; it&#39;s ^Z in Windows.</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（3） 💬（1）<div>macOS下，需要将把 Antlr 的 JAR 文件设置到 CLASSPATH 环境变量中：
如果是用Homebrew 安装的 Antlr，安装路径是：&#47;usr&#47;local&#47;Cellar&#47;antlr&#47;4.7.2&#47;antlr-4.7.2-complete.jar；
可以使用vi ~&#47;.bash_profile命令打开bash_profile文件，将export CLASSPATH=&quot;.:&#47;usr&#47;local&#47;Cellar&#47;antlr&#47;4.7.2&#47;antlr-4.7.2-complete.jar:$CLASSPATH&quot;这段代码复制到里面。
然后就可以运行javac *.java了</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/f5/2c29b0d7.jpg" width="30px"><span>PythonAI</span> 👍（3） 💬（3）<div>➜  antlr grun antlrtest.PlayScriptexpression -gui

Can&#39;t load antlrtest.PlayScriptexpression as lexer or parser</div>2019-08-26</li><br/><li><img src="" width="30px"><span>江世民</span> 👍（2） 💬（1）<div>遇到了一个大坑。
Windows环境下，添加jar包到CLASSPATH中时，最好写在前面。如果是追加在后面，系统很可能不识别。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（2） 💬（2）<div>不知道是什么问题？
$ grun Hello tokens -tokens Hello.play
Exception in thread &quot;main&quot; java.lang.NoClassDefFoundError: antlrtest&#47;Hello (wrong name: Hello)
        at java.base&#47;java.lang.ClassLoader.defineClass1(Native Method)
        at java.base&#47;java.lang.ClassLoader.defineClass(ClassLoader.java:1016)
        at java.base&#47;java.security.SecureClassLoader.defineClass(SecureClassLoader.java:174)
        at java.base&#47;jdk.internal.loader.BuiltinClassLoader.defineClass(BuiltinClassLoader.java:802)
        at java.base&#47;jdk.internal.loader.BuiltinClassLoader.findClassOnClassPathOrNull(BuiltinClassLoader.java:700)
        at java.base&#47;jdk.internal.loader.BuiltinClassLoader.loadClassOrNull(BuiltinClassLoader.java:623)
        at java.base&#47;jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:581)
        at java.base&#47;jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:178)
        at java.base&#47;java.lang.ClassLoader.loadClass(ClassLoader.java:521)
        at org.antlr.v4.gui.TestRig.process(TestRig.java:135)
        at org.antlr.v4.gui.TestRig.main(TestRig.java:119)</div>2019-12-25</li><br/><li><img src="" width="30px"><span>mudfrog</span> 👍（2） 💬（2）<div>老师，我的程序能编译通过，也能正常运行，能正常的解析和运算出来，但就是想看看语法树直观一些。我使用grun的时候总是提示Can&#39;t load CalExpr as lexer or parser，这里CalExpr到底是G4文件还是tokens文件呢，我把这两个文件都拷贝到src目录下了。我用的是win7底下的eclipse，</div>2019-09-01</li><br/><li><img src="" width="30px"><span>minghu6</span> 👍（1） 💬（1）<div>ANTLR的使用一定要有 “The Definitive ANTLR 4 Reference”  推荐电子版 https:&#47;&#47;github.com&#47;antlr&#47;antlr4&#47;blob&#47;master&#47;doc&#47;index.md

可以做关键字搜索，查点儿语法概念性的东西比较方便，用一位网友说的话：
If you do not already have &quot;The Definitive ANTLR 4 Reference&quot; book I recommend getting hold of it. Will save you a lot of time. 
话说极客时间的内容还不错，没有那么多花里胡哨的噱头，但是这个书签笔记和评论的体验太差！
书签笔记甚至没有结构，留言也不支持markdown

一定要ommonLexer.g4</div>2021-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep2gRIticwS6CiatsCiaU4QRjAODKibQevrhSciatrmd90lNIZFxywE9yyZgAxKTmWiaBSH4zZUcRIV46qQ/132" width="30px"><span>englefly</span> 👍（1） 💬（1）<div>宫老师，Antlr的性能怎样？我们用antlr做了一个sql解析，当遇到比较长的sql语句是，antlr解析花了100ms，而mysql 只用了9ms。不知道是我们用法的问题，还是antlr本身为了使用简单牺牲了一些性能。</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/a2/c7a3758d.jpg" width="30px"><span>漏网之渔</span> 👍（1） 💬（2）<div>弄了三个小时，终于好了。老师文档写的很清楚。
https:&#47;&#47;github.com&#47;RichardGong&#47;PlayWithCompiler&#47;blob&#47;master&#47;antlr_install.md
我遇到的问题有两点：
1.执行 grun 的时候 没带package名如grun Hello tokens -tokens hello.play，会提示java.lang.NoClassDefFoundError: Hello (wrong name: antlrtest&#47;Hello)，这是因为老师源码Hello带了pack保命antlrtest

我的解决方法是在src\antlrtest\目录下执行命令grun antlrtest.Hello tokens -tokens hello.play

2.执行grun命令报错误java.nio.file.NoSuchFileException: hello.play，这是因为我在antlrtest\src\目录下运行的grun，而hello.play在antlrtest\src\antlrtest\下，解决方法是在antlrtest\src\antlrtest\下执行grun命令
，或者把hello.play文件代码拷贝到src\目录下再执行grun命令。

另外如果遇到javac命令遇见GBK错误，是因为编码格式问题，解决方法：javac -encoding utf-8 PlayScript.java

如果遇到找不到parse lexer问题，Class Path需要添加src目录</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fb/76/37dccd3d.jpg" width="30px"><span>徐炜</span> 👍（1） 💬（1）<div>Antlr、Lex&#47;Flex、 Yacc&#47;Bison 在目前市场上哪个会比较常用呢，在时间有限的情况下，哪一种会比较合适去学习。</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/5f/72195e7a.jpg" width="30px"><span>火火</span> 👍（1） 💬（3）<div>Hello.java:2: 错误: 程序包org.antlr.v4.runtime不存在
import org.antlr.v4.runtime.Lexer;
                           ^
Hello.java:3: 错误: 程序包org.antlr.v4.runtime不存在
import org.antlr.v4.runtime.CharStream;
                           ^
Hello.java:4: 错误: 程序包org.antlr.v4.runtime不存在
import org.antlr.v4.runtime.Token;
                           ^
Hello.java:5: 错误: 程序包org.antlr.v4.runtime不存在
import org.antlr.v4.runtime.TokenStream;
                           ^
Hello.java:8: 错误: 程序包org.antlr.v4.runtime.dfa不存在
import org.antlr.v4.runtime.dfa.DFA;
                               ^
Hello.java:12: 错误: 找不到符号</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（1） 💬（2）<div>老师，为什么我用antlr生成的AdditiveExpressionContext就没有示例程序中的ADD() SUB()这些直接以token名字命名的方法呢？</div>2019-08-29</li><br/><li><img src="" width="30px"><span>紫灵斗圣</span> 👍（0） 💬（1）<div>antlr的语法规则的顺序又要求吗，是否规则1是程序的开头</div>2021-04-01</li><br/><li><img src="" width="30px"><span>minghu6</span> 👍（0） 💬（1）<div>要是有个gitment 直接和代码仓库的issue关联起来就好了</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/09/db/78996b11.jpg" width="30px"><span>Gaollard</span> 👍（0） 💬（1）<div>看着好激动，对于我这样非科班出身的码农，简直打开了新世界大门。</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/d4/ff1c1319.jpg" width="30px"><span>金龟</span> 👍（0） 💬（1）<div>idea 的antlr插件，好像使用不了，怪了</div>2020-11-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epDGb8dkicTpmr4ic37dzEngibHQ0BvZyToQhsD0icMy2qxqiaJelYpPqzzkTfXsCibqjwbkK94beYC0N6Q/132" width="30px"><span>空山新雨后</span> 👍（0） 💬（1）<div>老师，我执行antlr Hello.g4 没有问题，但执行javac *.java时报错 “程序包org.antlr.v4.runtime不存在”等问题，是我配置环境变量的问题么？</div>2020-07-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/hkzTTpS89YDu3h48blvYUlzAKVEYkBhXiameEdJJHr6c9WUxfzf3sQ5wn0lwJQN2PTf2GJfqtBkNb0Ct35WuBew/132" width="30px"><span>Geek_8292d8</span> 👍（0） 💬（1）<div>执行下述语句：
grun antlrtest.PlayScript expression -gui

最后并没有swing的可视化窗口弹出，直接就结束了，什么都没输出？
请问如何输出，麻烦详细点。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（0） 💬（1）<div>用过flex和bison，跟antlr比起来，感觉antlr的模块化功能做得更全，包装出了visitor和listener 两种模式。跟flex和bison相比，antlr需要手写的代码更加少一些，且入门难度比flex和bison低很多</div>2020-03-30</li><br/><li><img src="" width="30px"><span>dbo</span> 👍（0） 💬（1）<div>grun运行报错的同学可以参考下，按如下方式运行

➜  src git:(master) ✗ pwd
&#47;Users&#47;dbo&#47;workspace&#47;PlayWithCompiler&#47;lab&#47;antlrtest&#47;src
➜  src git:(master) ✗ echo $CLASSPATH
&#47;usr&#47;local&#47;Cellar&#47;antlr&#47;4.8&#47;antlr-4.8-complete.jar:.
➜  src git:(master) ✗ javac antlrtest&#47;Hello.java
➜  src git:(master) ✗ grun antlrtest.Hello tokens -tokens antlrtest&#47;hello.play
ANTLR Tool version 4.7.2 used for code generation does not match the current runtime version 4.8[@0,0:2=&#39;int&#39;,&lt;&#39;int&#39;&gt;,1:0]
[@1,4:6=&#39;age&#39;,&lt;Id&gt;,1:4]
[@2,8:8=&#39;=&#39;,&lt;&#39;=&#39;&gt;,1:8]
[@3,10:11=&#39;45&#39;,&lt;IntLiteral&gt;,1:10]
[@4,12:12=&#39;;&#39;,&lt;&#39;;&#39;&gt;,1:12]
[@5,14:15=&#39;如果&#39;,&lt;If&gt;,2:0]
[@6,17:17=&#39;(&#39;,&lt;&#39;(&#39;&gt;,2:3]
[@7,18:20=&#39;age&#39;,&lt;Id&gt;,2:4]
[@8,22:23=&#39;&gt;=&#39;,&lt;RelationalOP&gt;,2:8]
[@9,25:26=&#39;17&#39;,&lt;IntLiteral&gt;,2:11]
[@10,27:27=&#39;+&#39;,&lt;&#39;+&#39;&gt;,2:13]
[@11,28:28=&#39;8&#39;,&lt;IntLiteral&gt;,2:14]
[@12,29:29=&#39;+&#39;,&lt;&#39;+&#39;&gt;,2:15]
[@13,30:31=&#39;20&#39;,&lt;IntLiteral&gt;,2:16]
[@14,32:32=&#39;)&#39;,&lt;&#39;)&#39;&gt;,2:18]
[@15,33:33=&#39;{&#39;,&lt;&#39;{&#39;&gt;,2:19]
[@16,39:44=&#39;printf&#39;,&lt;Id&gt;,3:4]
[@17,45:45=&#39;(&#39;,&lt;&#39;(&#39;&gt;,3:10]
[@18,46:61=&#39;&quot;Hello old man!&quot;&#39;,&lt;StringLiteral&gt;,3:11]
[@19,62:62=&#39;)&#39;,&lt;&#39;)&#39;&gt;,3:27]
[@20,63:63=&#39;;&#39;,&lt;&#39;;&#39;&gt;,3:28]
[@21,65:65=&#39;}&#39;,&lt;&#39;}&#39;&gt;,4:0]
[@22,66:65=&#39;&lt;EOF&gt;&#39;,&lt;EOF&gt;,4:1]
➜  src git:(master) ✗</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/19/14018371.jpg" width="30px"><span>瓜瓜</span> 👍（0） 💬（1）<div>ANTLR Tool version 4.8 used for code generation does not match the current runtime version 4.7.2
win7的系统 class_path：%TOOL_HOME%\antlr-4.7.2-complete.jar;
path：D:\antlr;

D:\antlr&gt;dir
 驱动器 D 中的卷没有标签。
 卷的序列号是 BE10-222B

 D:\antlr 的目录

2020&#47;02&#47;01  10:04    &lt;DIR&gt;          .
2020&#47;02&#47;01  10:04    &lt;DIR&gt;          ..
2020&#47;01&#47;29  10:07         2,079,769 antlr-4.7.2-complete.jar
2020&#47;01&#47;29  10:20                25 antlr.bat
2020&#47;01&#47;29  12:09                32 grun.bat
               3 个文件      2,079,826 字节
               2 个目录 18,834,886,656 可用字节
为什么总是报这个警告，我第一次下载了一个4.8版本的，放在了这个目录下，后来把4.8版本的删除了，望老师帮忙解答下，感谢</div>2020-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/8c/ff48ece3.jpg" width="30px"><span>小乙哥</span> 👍（0） 💬（1）<div>mac下面按照antlr的命令：： brew install Antlr
按照完成Antlr之后，需要配置一下CLASSPATH，不然使用antlr命令的时候会提示找不到antlr相关类

export ANTLR_HOME=&#47;usr&#47;local&#47;Cellar&#47;antlr&#47;4.7.2
export CLASSPATH=$JAVA_HOME&#47;lib&#47;tools.jar:$JAVA_HOME&#47;jre&#47;lib:$ANTLR_HOME&#47;antlr-4.7.2-com    plete.jar</div>2019-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（0） 💬（1）<div>按着顺序操作下来，词法分析这块的理解清晰很多。中文编程，在词法分析下，和英文编程几乎等价。感谢留言中筒靴的配置指南。

一个小Tip：windows下配置好环境变量，记得注销或重启，让环境变量生效。
</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/16/fa/722d0feb.jpg" width="30px"><span>庆霖</span> 👍（0） 💬（2）<div>哎呀，稀碎一个ANTLR4配了两天超低效率一顿踩坑最后终于在这个教程找到了坑在哪https:&#47;&#47;blog.csdn.net&#47;shine_journey&#47;article&#47;details&#47;17952163，那两个bat要放到C盘的system和system32才会生效(*￣m￣)，我一直以为是我环境变量设置的有问题我寻思着复制粘贴都有问题可咋整。另，宫老师我解决了vscode输出提示的COLON，目测是其中有些字符中文输入法输入了，找其他一样的地方复制粘一下就好了😁 </div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/16/fa/722d0feb.jpg" width="30px"><span>庆霖</span> 👍（0） 💬（1）<div>宫老师，我在写hello.g4的时候空白字符抛弃里[ \t]这里vscode的输出说这里缺少COLON这是为什么呢，求解答</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d6/2c/9aa0ae40.jpg" width="30px"><span>阿尔伯特</span> 👍（0） 💬（1）<div>This is really COOL!</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/79/f3/2d5ce916.jpg" width="30px"><span>wj</span> 👍（0） 💬（1）<div>请教老师,  Abstract Tree Matching 有已经实现的算法可以用吗? 网上我只找到相关的论文, 我在想比较两个 java 文件的结构, 可能比较 AST 树会更直接一些?</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/2a/b11d5ad8.jpg" width="30px"><span>曾经瘦过</span> 👍（0） 💬（1）<div>今晚回去后跟着操练操练，感觉很酷</div>2019-09-18</li><br/>
</ul>