你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

上节课，我们系统性地介绍了使用大语言模型（Large Language Model，LLM）辅助软件开发的思路，也就是遵从测试驱动开发（Test Driven Development，TDD）的节奏，并与LLM结对编程（Pair Programming）完成需求。

那么，让我们使用这个思路，重新做一遍第15节课的例子，看看这一次有什么不一样。需求和之前是一样的：

> 我们中的大多数人都不得不时不时地解析一下命令行参数。如果我们没有一个方便的工具，那么我们就简单地处理一下传入main函数的字符串数组。有很多开源工具可以完成这个任务，但它们可能并不能完全满足我们的要求。所以我们再写一个吧。  
>    
> 传递给程序的参数由标志和值组成。标志应该是一个字符，前面有一个减号。每个标志都应该有零个或多个与之相关的值。例如：  
>    
> -l -p 8080 -d /usr/logs  
>    
> “l”（日志）没有相关的值，它是一个布尔标志，如果存在则为true，不存在则为false。“p”（端口）有一个整数值，“d”（目录）有一个字符串值。标志后面如果存在多个值，则该标志表示一个列表：  
>    
> -g this is a list -d 1 2 -3 5  
>    
> “g” 表示一个字符串列表\[“this”, “is”, “a”, “list”]，"d"标志表示一个整数列表\[1, 2, -3, 5]。  
>    
> 如果参数中没有指定某个标志，那么解析器应该指定一个默认值。例如，false代表布尔值，0代表数字， `""` 代表字符串，\[]代表列表。如果给出的参数与模式不匹配，重要的是给出一个好的错误信息，准确地解释什么是错误的。  
>    
> 确保你的代码是可扩展的，即如何增加新的数值类型是直接和明显的。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（2） 💬（2）<div>我一直有一个疑问，到底是任务列表？还是测试列表？

还是先根据软件架构和测试策略将需求切到足够小，形成任务列表，在针对任务列表中的每个任务写出测试，从而形成测试列表。

之前提到过用户故事及验收条件，用户故事需要根据软件架构和测试策略再切分吗？验收条件，是不是就是测试列表或者测试列表的一部分？

后面会有复杂点的例子，介绍需求如何从用户故事，到被不同软件架构，测试策略组合影响，从而导出不同的任务列表，进而导出测试列列表的过程吗？</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/ac/b7/92ebd0a5.jpg" width="30px"><span>起个名称吧</span> 👍（0） 💬（1）<div>我认为应该是庞杂+清晰
庞杂的认知行为模式，从gpt给与的需求拆分的任务列表，我们和llm进行认知对齐，帮其弥补llm认知需求的差异，在该模式下我们根据对齐的任务列表生成测试代码和生产代码
清晰的认知行为模式，根据测试代码执行进行测试来发现生产代码上的遗漏，发现错误,与llm进行交互调整生产代码，最终完成测试的通过。
这里有两个疑问
1. 假设根据测试代码执行发现未知的错误(此时无法与gpt进行交互)，我们也不理解改错误的信息，我们此时就需要debug一步步调试，此时我们本身又处于复杂模式下(探索-感知-响应)，而可以和llm交互后我们又处于清晰模式下(感知-分类-响应)。我们因为一个llm帮助我们的认知行为发生了两个重大的变更吗？
2. TDD测试驱动,红-绿-重构，这节课里没看到重构循环,感觉缺少了点啥</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c6/6c/a400175a.jpg" width="30px"><span>FARO_Z</span> 👍（2） 💬（0）<div>感觉 LLM 只能比较好的生成单点功能的代码，一般也就是工具类

如果涉及到业务上下文，不是歇菜，就是要喂大量 promot 进行调校。有这功夫代码早写完了

感觉目前 LLM 对于程序员最大的帮助在于阅读源码上面，对于已有内容 LLM 能作为一个很好的索引器，帮助快速理清代码上下文。至于很多业务驱动的工程，还是先不要动 LLM 提升工作效率的念头了吧</div>2024-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（2） 💬（0）<div>感谢老师，已经用到工作中了。
目前我们只让GPT进行了需求分解。
盲猜一波，接下来应该让gpt，不仅根据需求分解，还要根据架构，分解成功能上下文的任务项。

再根据任务项，列出测试场景和测试数据。
然后生成测试用例。
最后生成代码。

（这其中，我觉得还可以提供现有测试类的代码作为few shot，而且测试类也蕴含了SUT的API如何使用的信息）</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>学习后收获了 2 个模版
练习后获得经验：需要认真检查 AI 列出的测试场景，不然会出现奇怪的代码！

实用的 AI 模版
======

列出测试场景
----------------
功能需求
====
{requirement}

任务
====
请根据上面的功能需求，列出需要测试的场景。描述场景，并给出相关的测试数据。

编写测试代码
----------------
请生成 junit junpiter 测试
要求：
每个场景对应一个测试方法
使用 Kotlin 编写
使用 TDD 中的 should style 编写测试

详见 https:&#47;&#47;wyyl1.com&#47;post&#47;28&#47;17</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>有个问题，那如何把 TDD 与 LLM 结合写业务代码呢？
如果按照 16 节的内容，逻辑就是拆分一个业务功能的架构，比如 http 层、业务逻辑层、数据层
然后对业务逻辑层写清楚诉求，然后跟 LLM 结队编程吗？运用本篇内容</div>2024-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（0）<div>&#47;&#47; Question by EnigmaWU: generate could missing ut code for me
&#47;&#47; Answer from ChatCopilot:
TEST(CC_parseCmdLineArgs, LogSavingDir) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-d&quot;, (char *)&quot;&#47;path&#47;to&#47;log&quot;};
  EXPECT_EQ(CC_SUCCESS, CC_parseCmdLineArgs(3, argv, &amp;CmdLineArgs));
  EXPECT_FALSE(CmdLineArgs.IsLoggingEnabled);
  EXPECT_EQ(0, CmdLineArgs.RecvPort);
  EXPECT_STREQ(&quot;&#47;path&#47;to&#47;log&quot;, CmdLineArgs.pLogSavingDir);
}

TEST(CC_parseCmdLineArgs, InvalidArgs) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;invalid&quot;};
  EXPECT_EQ(CC_FAIL, CC_parseCmdLineArgs(2, argv, &amp;CmdLineArgs));
}

TEST(CC_parseCmdLineArgs, MissingValueForPort) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-p&quot;};
  EXPECT_EQ(CC_FAIL, CC_parseCmdLineArgs(2, argv, &amp;CmdLineArgs));
}

TEST(CC_parseCmdLineArgs, MissingValueForDir) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-d&quot;};
  EXPECT_EQ(CC_FAIL, CC_parseCmdLineArgs(2, argv, &amp;CmdLineArgs));
}

TEST(CC_parseCmdLineArgs, NonNumericPort) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-p&quot;, (char *)&quot;nonnumeric&quot;};
  EXPECT_EQ(CC_FAIL, CC_parseCmdLineArgs(3, argv, &amp;CmdLineArgs));
}

TEST(CC_parseCmdLineArgs, MultipleSameArgs) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-l&quot;, (char *)&quot;-l&quot;};
  EXPECT_EQ(CC_SUCCESS, CC_parseCmdLineArgs(3, argv, &amp;CmdLineArgs));
  EXPECT_TRUE(CmdLineArgs.IsLoggingEnabled);
}

TEST(CC_parseCmdLineArgs, ArgsInDifferentOrder) {
  CC_CmdLineArgs_T CmdLineArgs;
  char *argv[] = {(char *)&quot;test&quot;, (char *)&quot;-p&quot;, (char *)&quot;1234&quot;, (char *)&quot;-l&quot;, (char *)&quot;-d&quot;, (char *)&quot;&#47;path&#47;to&#47;log&quot;};
  EXPECT_EQ(CC_SUCCESS, CC_parseCmdLineArgs(6, argv, &amp;CmdLineArgs));
  EXPECT_TRUE(CmdLineArgs.IsLoggingEnabled);
  EXPECT_EQ(1234, CmdLineArgs.RecvPort);
  EXPECT_STREQ(&quot;&#47;path&#47;to&#47;log&quot;, CmdLineArgs.pLogSavingDir);
}</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（0）<div>&#47;&#47; Chat with Copilot, Question by EnigmaWU:
&#47;&#47; #file:CC_parseCmdLineArgs.c #file:CC_parseCmdLineArgsTest_byCopilot.cxx
&#47;&#47;      what UT already written and what UT is missed?

&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;&#47;
&#47;&#47; Answer from ChatCopilot:
&#47;**
The unit tests that are already written for the CC_parseCmdLineArgs function in the CC_parseCmdLineArgsTest_byCopilot.cxx file
are:

NullCmdLineArgs: Tests the function with argc as 0 and argv as NULL.
NullCmdLineArgsPtr: Tests the function with argc as 0, argv as NULL, and pCmdLineArgs as NULL.
NoArgs: Tests the function with no command line arguments.
LoggingEnabled: Tests the function with the logging enabled argument -l.
RecvPort: Tests the function with the receive port argument -p and a value.
LogSavingDir: Tests the function with the log saving directory argument -d and a value.
AllArgs: Tests the function with all possible arguments.
The unit tests that are missing could be:

InvalidArgs: Tests the function with invalid arguments that do not start with -.
MissingValueForPort: Tests the function with the -p argument but without a value following it.
MissingValueForDir: Tests the function with the -d argument but without a value following it.
NonNumericPort: Tests the function with a non-numeric value for the -p argument.
MultipleSameArgs: Tests the function with multiple instances of the same argument.
ArgsInDifferentOrder: Tests the function with all possible arguments in a different order.
 **&#47;</div>2024-04-15</li><br/>
</ul>