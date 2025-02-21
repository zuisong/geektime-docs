上一讲，我带你用Antlr生成了词法分析器和语法分析器，也带你分析了，跟一门成熟的语言相比，在词法规则和语法规则方面要做的一些工作。

在词法方面，我们参考Java的词法规则文件，形成了一个CommonLexer.g4词法文件。在这个过程中，我们研究了更完善的字符串字面量的词法规则，还讲到要通过规则声明的前后顺序来解决优先级问题，比如关键字的规则一定要在标识符的前面。

目前来讲，我们已经完善了词法规则，所以今天我们来补充和完善一下语法规则，看一看怎样用最高效的速度，完善语法功能。比如一天之内，我们是否能为某个需要编译技术的项目实现一个可行性原型？

而且，我还会带你熟悉一下常见语法设计的最佳实践。这样当后面的项目需要编译技术做支撑时，你就会很快上手，做出成绩了！

接下来，我们先把表达式的语法规则梳理一遍，让它达到成熟语言的级别，然后再把语句梳理一遍，包括前面几乎没有讲过的流程控制语句。最后再升级解释器，用Visitor模式实现对AST的访问，这样我们的代码会更清晰，更容易维护了。

好了，让我们正式进入课程，先将表达式的语法完善一下吧！

## 完善表达式（Expression）的语法

在“[06 | 编译器前端工具（一）：用Antlr生成词法、语法分析器](https://time.geekbang.org/column/article/126910)”中，我提到Antlr能自动处理左递归的问题，所以在写表达式时，我们可以大胆地写成左递归的形式，节省时间。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（20） 💬（2）<div>现在都是用一门语言去实现这些功能，我想知道最开始的语言是怎么实现分析的呢！有一点鸡生蛋蛋生鸡！</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/a3/9670d4b4.jpg" width="30px"><span>Spring</span> 👍（17） 💬（1）<div>老师，你好。请教一下，词法，语法解析后生成 AST 后，计算机怎么指导我的AST 中的“+” 就是执行 add  的计算呢？这其中是不是还有还存在一个中间层？</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/0f/1f229bf5.jpg" width="30px"><span>Void_seT</span> 👍（15） 💬（1）<div>老师，目前的学习过程中，比如表达式语法规则、语句语法规则等，虽然能知道它们表示了什么，但是并不知道它是怎么凭空产生的；请问：这种规则是相对比较固定的，我们要使用时，可以参照“标准”的规则文法进行修改呢？还是要自己掌握各种类型语法规则的各个组成细节，以便于在写语法规则时可以信手拈来呢？如果需要熟练掌握语法规则的各个组成细节，目前的工作如果还用不到生成“小编译器”这种技能，也就是没有练习或高强度的训练时间的话，是否需要现在就硬啃下这块硬骨头（因为怕长时间不使用，将来真正要使用时，还是要重新再训练一遍）？</div>2019-08-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKQBotbJDGmnxL1ib3yD2XI7HfRcLMLmNfMXEIIebWaT9q2fvmTYm7lfISgic4W7BZ5r4Jtib9iawEJhg/132" width="30px"><span>宇智波芭芭干</span> 👍（8） 💬（7）<div>学习时总感觉节奏在老师那边，自己的思路并不连贯，对于初学者容易出现断片。在极客时间其它老师那里也同步购买了linux以及网络协议，另外一边通过故事的形式通熟易懂的讲解了一些底层知识原理，学习也是相当顺畅有兴趣，而这里不知道为啥就是顺畅不起来，差距不是一般的大。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/5f/0c870296.jpg" width="30px"><span>windpiaoxue</span> 👍（8） 💬（1）<div>老师您好
例如下面这个规则：
stmt -&gt; if expr stmt
      | if expr stmt else stmt
      | other
我测试了一下，antlr使用上面这个规则可以正确的处理悬挂else的问题，
antlr在处理这种二义性问题的时候，是依据什么来处理的。
</div>2019-08-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLJ9I2tZHaGuvibuLQFxTicoC1PQTwswI6NDCT6MV1IgqE5ibAVPucKXaiafTpCmvtGPtfSSpC4rbH5aA/132" width="30px"><span>fung</span> 👍（2） 💬（2）<div>老师，这一段看不懂咋办，有的救吗？看不懂这些语法啊，能解析下吗？或有其他资料介绍吗？谢谢
expression : primary | expression bop=&#39;.&#39; ( IDENTIFIER | functionCall | THIS ) | expression &#39;[&#39; expression &#39;]&#39; | functionCall | expression postfix=(&#39;++&#39; | &#39;--&#39;) | prefix=(&#39;+&#39;|&#39;-&#39;|&#39;++&#39;|&#39;--&#39;) expression | prefix=(&#39;~&#39;|&#39;!&#39;) expression | expression bop=(&#39;*&#39;|&#39;&#47;&#39;|&#39;%&#39;) expression | expression bop=(&#39;+&#39;|&#39;-&#39;) expression | expression (&#39;&lt;&#39; &#39;&lt;&#39; | &#39;&gt;&#39; &#39;&gt;&#39; &#39;&gt;&#39; | &#39;&gt;&#39; &#39;&gt;&#39;) expression | expression bop=(&#39;&lt;=&#39; | &#39;&gt;=&#39; | &#39;&gt;&#39; | &#39;&lt;&#39;) expression .......</div>2019-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ1KSrs5Wf7VFhckiaKClt4kmJibBVic9tp2GicoQ0pAU1FRwS7VrCUzPXu8GQ65biaibrKxibQ7TUI3IBDA/132" width="30px"><span>shantelle</span> 👍（2） 💬（1）<div>宫老师你好，请问这个匹配的是什么内容呢
&#39;\\&#39; [btnfr&quot;&#39;\\]</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/1c/b0c6c009.jpg" width="30px"><span>zhj</span> 👍（2） 💬（1）<div>现在拿到的ASTEvaluator，都裹扎了编译器相关的代码，这里才看到Ast树，这边没有很好的 版本迭代吗，上来直接就是讲课同步的代码，看的云里雾里，没法循序渐进</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（2） 💬（1）<div>statement
    : blockLabel=block
    | IF parExpression statement (ELSE statement)?
    | FOR &#39;(&#39; forControl &#39;)&#39; statement
    | WHILE parExpression statement
    | DO statement WHILE parExpression &#39;;&#39;
    | SWITCH parExpression &#39;{&#39; switchBlockStatementGroup* switchLabel* &#39;}&#39;
    | RETURN expression? &#39;;&#39;
    | BREAK IDENTIFIER? &#39;;&#39;
    | SEMI
    | statementExpression=expression &#39;;&#39;
    ;
请问&quot; : blockLabel=block&quot;这个规则如何解释?谢谢!</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/ea/c8136dfd.jpg" width="30px"><span>草戊</span> 👍（1） 💬（1）<div>老师，有些语言的部分文法是上下文有关，比如说必须是第七列写*号来注释。对于这样的语言分析，有什么好的建议吗？在parser前先做预处理变换？</div>2019-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/04/6d/c959cb93.jpg" width="30px"><span>cry soul</span> 👍（1） 💬（1）<div>建议老师用用git搭好tag来表示每个课程到到哪部分源码，不然需要读好几篇才能自己尝试。</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（1） 💬（4）<div>JavaScript中的this是咋实现的，这个一直处于迷糊当中，好想弄清楚，不同语言之间语意的差别，学完语意能理解么😇 😇 😇 ，看了很多课程，都很失望，都是再讲几种场景，怎么指向，没实质的改变！</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/64/06d54a80.jpg" width="30px"><span>中年男子</span> 👍（1） 💬（1）<div>编译 git 里 PlayScript-cpp， 我这里报错， PlayScriptJit.h 这个文件， 搞了半天没搞懂
In file included from &#47;Users&#47;shiny&#47;learn&#47;PlayWithCompiler&#47;playscript-cpp&#47;src&#47;PlayScript.cpp:5:
[build] In file included from &#47;Users&#47;shiny&#47;learn&#47;PlayWithCompiler&#47;playscript-cpp&#47;src&#47;grammar&#47;IRGen.h:28:
[build] &#47;Users&#47;shiny&#47;learn&#47;PlayWithCompiler&#47;playscript-cpp&#47;src&#47;grammar&#47;PlayScriptJIT.h:33:31: error: unknown type name &#39;LegacyRTDyldObjectLinkingLayer&#39;; did you mean &#39;RTDyldObjectLinkingLayer&#39;?
[build]             using ObjLayerT = LegacyRTDyldObjectLinkingLayer;
[build]                               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[build]                               RTDyldObjectLinkingLayer</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>难度越来越大了，要好好消化才行。</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4b/36/ed40fb3a.jpg" width="30px"><span>(￣_￣ )</span> 👍（1） 💬（1）<div>写了一晚上终于用c语言模仿着实现了第二节课的内容
https:&#47;&#47;github.com&#47;hongningexpro&#47;Play_with_Compiler&#47;tree&#47;master&#47;01-Simple_Lexer</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/3b/5502a4fa.jpg" width="30px"><span>Victor.qiu</span> 👍（0） 💬（1）<div>老师，那个表达式的规则里怎么没有看到对括号的匹配</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/91/a017bf72.jpg" width="30px"><span>coconut</span> 👍（0） 💬（1）<div>参考老师的Java代码，写了一个简陋的Python版本，目前可以解析下面的语句

int a=2*3+1;a=a+3*2;int b=1+2;snoopy_print(a, b);

https:&#47;&#47;github.com&#47;leveryd&#47;PlayWithCompiler&#47;blob&#47;master&#47;main.py</div>2020-12-16</li><br/><li><img src="" width="30px"><span>郭思奇</span> 👍（0） 💬（1）<div>老师，您好，想请教下，当前编程中常有数据类型定义，对于一种新定义的数据类型，例如 int_32 age = 45，语法分析时如何识别该语句是一条初始化语句呢？</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/cc/21/e3c45732.jpg" width="30px"><span>lcp0578</span> 👍（0） 💬（1）<div>好好学习天天向上</div>2020-03-21</li><br/><li><img src="" width="30px"><span>hilltsui</span> 👍（0） 💬（1）<div>学到挺多东西的课程。老师请问后面的课程会有讲解关于编译后端的内容吗挺期待的</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（2）<div>老师，examples&#47;BlockScope.play 的输出结果应该是 0 2 3 0。因为在 type resolve 阶段已经把所有的变量定义都识别出来了，然后在 ref resolve 阶段解决分号中第一个 i 的引用时会在当前作用域中寻找到，所以分号中对 i 的赋值不会影响到根作用域的变量 i。运行了一下程序确实如此。</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/44/88/69580101.jpg" width="30px"><span>长方体混凝土移动工程师</span> 👍（0） 💬（1）<div>blockLabel 这个怎么没看到在哪里定义的呢?</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/44/88/69580101.jpg" width="30px"><span>长方体混凝土移动工程师</span> 👍（0） 💬（1）<div>bop只是一个别名吗？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/03/bd7d8a6d.jpg" width="30px"><span>Lafite</span> 👍（0） 💬（1）<div>宫老师，本章的代码应该如何去学习呢，想学习一下 本章的解释器及其他代码， 结果发现代码量比较大，我阅读起来比较困难，麻烦老师指导一下，谢谢</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（2）<div>有个疑问，为什么expression的规则是写作  

expression bop=(&#39;+&#39;|&#39;-&#39;) expression 

而不是写作：

expression bop=(ADD|SUB) expression 

</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ee/e7/4375e97c.jpg" width="30px"><span>雲至</span> 👍（0） 💬（1）<div>老师能讲一下antlr的语法吗？</div>2019-08-28</li><br/><li><img src="" width="30px"><span>Geek_6304e3</span> 👍（4） 💬（1）<div>老师，后面的用 Vistor 模式升级脚本解释器开始有点看不懂，不懂java，有JavaScript版本的吗？文章一些代码都是直接说这样写，但是我不知道这样写之后在哪里关联运行起来。</div>2022-02-11</li><br/><li><img src="" width="30px"><span>Geek_6304e3</span> 👍（2） 💬（0）<div>visitor这些解释器要怎么执行呢？</div>2022-02-11</li><br/><li><img src="" width="30px"><span>Geek_6304e3</span> 👍（2） 💬（0）<div>visitExpression方法实在哪个文件生成的？文中没有说。</div>2022-02-11</li><br/><li><img src="" width="30px"><span>Geek_6304e3</span> 👍（1） 💬（0）<div>老师，你给的java版本的项目跑不起来。。不懂java
</div>2022-02-11</li><br/>
</ul>