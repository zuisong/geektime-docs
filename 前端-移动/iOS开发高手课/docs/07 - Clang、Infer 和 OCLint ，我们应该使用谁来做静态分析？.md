你好，我是戴铭。

随着业务开发迭代速度越来越快，完全依赖人工保证工程质量也变得越来越不牢靠。所以，静态分析，这种可以帮助我们在编写代码的阶段就能及时发现代码错误，从而在根儿上保证工程质量的技术，就成为了iOS开发者最常用到的一种代码调试技术。

Xcode 自带的静态分析工具 Analyze，通过静态语法分析能够找出在代码层面就能发现的内存泄露问题，还可以通过上下文分析出是否存在变量无用等问题。但是，Analyze 的功能还是有限，还是无法帮助我们在编写代码的阶段发现更多的问题。所以，这才诞生出了功能更全、定制化高、效率高的第三方静态检查工具。比如，OCLint、Infer、Clang静态分析器等。

一款优秀的静态分析器，能够帮助我们更加全面的发现人工测试中的盲点，提高检查问题的效率，寻找潜在的可用性问题，比如空指针访问、资源和内存泄露等等。

同时，静态分析器还可以检查代码规范和代码可维护性的问题，根据一些指标就能够找出哪些代码需要优化和重构。这里有三个常用的复杂度指标，可以帮助我们度量是否需要优化和重构代码。

- 圈复杂度高。圈复杂度，指的是遍历一个模块时的复杂度，这个复杂度是由分支语句比如 if、case、while、for，还有运算符比如 &amp;&amp;、||，以及决策点，共同确定的。一般来说，圈复杂度在以 4 以内是低复杂度，5到7是中复杂度，8到10是高复杂度，11以上时复杂度就非常高了，这时需要考虑重构，不然就会因为测试用例的数量过高而难以维护。  
  而这个圈复杂度的值，是很难通过人工分析出来的。而静态分析器就可以根据圈复杂度规则，来监控圈复杂度，及时发现代码是否过于复杂，发现问题后及早解决，以免造成代码过于复杂难以维护。
- NPath 复杂度高。NPath 度量是指一个方法所有可能执行的路径数量。一般高于200就需要考虑降低复杂度了。
- NCSS 度量高。NCSS 度量是指不包含注释的源码行数，方法和类过大会导致代码维护时阅读困难，大的 NCSS 值表示方法或类做的事情太多，应该拆分或重构。一般方法行数不过百，类的行数不过千。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/45/d2d2f005.jpg" width="30px"><span>iLearn</span> 👍（20） 💬（4）<div>老师，Swift的要怎么搞？</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/fd/87b5d5d7.jpg" width="30px"><span>scorpiozj</span> 👍（2） 💬（1）<div>请问Xcode中的静态检查就是clang 静态检查吗？</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/05/9b32374a.jpg" width="30px"><span>jimmy</span> 👍（2） 💬（1）<div>oclint的一些研究 https:&#47;&#47;xiaozhuanlan.com&#47;topic&#47;9647358012</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/b2/8a3e8c28.jpg" width="30px"><span>頑 張</span> 👍（1） 💬（2）<div>infer跑不起来的 希望这篇能帮到https:&#47;&#47;blog.csdn.net&#47;elisa1988&#47;article&#47;details&#47;46531745?utm_source=blogxgwz7</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/f6/1f7dcc7c.jpg" width="30px"><span>择一城终老</span> 👍（0） 💬（1）<div>从来没有用过，感觉听天书一样，哈哈！不过大致了解了其功能，但是原理还真不好懂</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（0） 💬（1）<div>clang是一个c c++ oc 编译器，静态分析利用clang做代码编译层面的事情，内存泄露，强弱引用，方法调用深度等分析工作交给分析器本身。 

Clang是不是类似于oc中的runtime？</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/56/5f/b3f3d82e.jpg" width="30px"><span>Roger</span> 👍（32） 💬（1）<div>给宝宝喂夜奶，顺便来看看新的一课讲什么</div>2019-03-26</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（20） 💬（0）<div>1. OClint 想执行自己指定的项目，还是不会。。最后查了别的资料，说是要写脚本安装xcpretty，而且说是不维护了。

2. CLang 静态分析器的clang —analyze -Xclang -analyzer-checker-help 我执行之后，并没有成功显示常用的Checker。。

3. Clang 静态分析器的lib&#47;StaticAnalyzer&#47;Checkers这个路径也没有找到，是不是换地方了？

4. OClint、Clang静态分析器与Infer 都需要Clang编译器的LLVM对源码做词法、语法上的分析生成AST（一种静态语法树，代码更精简，遍历更轻松），然后对生成的AST做静态分析，达到编译代码层面的分析。

5. OCLint说是不维护了，所以除了规则太多导致的重点找不到，可定制性过高导致的易用性变差外，也PASS（其实我对这句规则多所以XX的理解感受不是很深。。）

Clang静态分析器，规则少只能检策较大问题，对内存泄漏一类问题若无错误也不提示外，回调次数也多。每执行一句，都要回调所有的Checker的回调函数。所以PASS

Infer 定制性不是最高，但是不差。可以小范围分析，所以效率高。还支持增量分析（使用已缓存数据，非增量会清楚缓存）。所以，建议Infer
</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/c8/ef0d6c86.jpg" width="30px"><span>yb坏蛋biubiu</span> 👍（9） 💬（0）<div>clang作为llvm编译器前端，进行预编译、词法分析生成token片、语法分析生成AST后，提供一个切面，开发者可以在这里利用clang生成的AST语法树进行自定义规则遍历分析，clang也提供了相应的checker和抛出诊断异常的diagnosis。</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/a1/e943773e.jpg" width="30px"><span>简生</span> 👍（6） 💬（2）<div>个人觉得虽然OCLint检测规则多，易用性没有Infer好。但是Sonar+OCLint可以对检测结果进行一个可视化的管理，还是会偏向于选择OCLint。😊</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/80/3f/bc65b009.jpg" width="30px"><span>Yest</span> 👍（5） 💬（0）<div>fatal error: &#39;Foundation&#47;Foundation.h&#39; file not found 这么解决👇
infer -- clang -c -isysroot &#47;Applications&#47;Xcode.app&#47;Contents&#47;Developer&#47;Platforms&#47;iPhoneSimulator.platform&#47;Developer&#47;SDKs&#47;iPhoneSimulator.sdk Hello.m</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/33/fd/01a8e1f3.jpg" width="30px"><span>寻心</span> 👍（5） 💬（2）<div>这个问题有谁遇到吗？
怎么解决？
&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;

Internal Error:   &#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;infer&#47;bin&#47;..&#47;lib&#47;python&#47;infer.py
  -j 4 --project-root &#47;Users&#47;yy&#47;工作&#47;项目&#47;test --out
  &#47;Users&#47;yy&#47;工作&#47;项目&#47;test&#47;infer-out -- xcodebuild build -scheme test
  -workspace test.xcworkspace -configuration Debug -sdk iphonesimulator:
  exited with code 1
Error backtrace:
Raised at file &quot;base&#47;Die.ml&quot; (inlined), line 25, characters 6-36
Called from file &quot;base&#47;Logging.ml&quot;, line 314, characters 58-80
Called from file &quot;integration&#47;Driver.ml&quot;, line 159, characters 2-16
Called from file &quot;integration&#47;Driver.ml&quot;, line 280, characters 6-420
Called from file &quot;infer.ml&quot;, line 20, characters 2-36
Called from file &quot;infer.ml&quot;, line 130, characters 8-54

&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;</div>2019-04-04</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqr5ibqxYwcSgqPA7s49MZb1vEKKXT4mPTojwiclXkJf3ug26NuzTa6A5gbicR2rAUHdEkUAn13Rr2KQ/132" width="30px"><span>吴小安</span> 👍（4） 💬（0）<div>infer 扫描怎么过滤不想扫描的文件呢，例如pod</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/9f/46ac03ad.jpg" width="30px"><span>快到碗里来</span> 👍（3） 💬（0）<div>infer扫描单个文件 报错
7 errors generated.
Error: the following clang command did not run successfully:
    &#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;facebook-clang-plugins&#47;clang&#47;install&#47;bin&#47;clang
    @&#47;var&#47;folders&#47;j_&#47;tb3f_ly50rj_qylmtk1h8k2w0000gn&#47;T&#47;clang_command_.tmp.11b92e.txt
  ++Contents of &#39;&#47;var&#47;folders&#47;j_&#47;tb3f_ly50rj_qylmtk1h8k2w0000gn&#47;T&#47;clang_command_.tmp.11b92e.txt&#39;:
    &quot;-cc1&quot; &quot;-load&quot;
    &quot;&#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;infer&#47;bin&#47;..&#47;..&#47;facebook-clang-plugins&#47;libtooling&#47;build&#47;FacebookClangPlugin.dylib&quot;
    &quot;-add-plugin&quot; &quot;BiniouASTExporter&quot; &quot;-plugin-arg-BiniouASTExporter&quot; &quot;-&quot;
    &quot;-plugin-arg-BiniouASTExporter&quot; &quot;PREPEND_CURRENT_DIR=1&quot;
    &quot;-plugin-arg-BiniouASTExporter&quot; &quot;MAX_STRING_SIZE=65535&quot; &quot;-cc1&quot; &quot;-triple&quot;
    &quot;x86_64-apple-macosx10.14.0&quot; &quot;-Wdeprecated-objc-isa-usage&quot;
    &quot;-Werror=deprecated-objc-isa-usage&quot; &quot;-emit-obj&quot; &quot;-mrelax-all&quot;
    &quot;-disable-free&quot; &quot;-disable-llvm-verifier&quot; &quot;-discard-value-names&quot;
    &quot;-main-file-name&quot; &quot;RootVC.m&quot; &quot;-mrelocation-model&quot; &quot;pic&quot; &quot;-pic-level&quot; &quot;2&quot;
    &quot;-mthread-model&quot; &quot;posix&quot; &quot;-mdisable-fp-elim&quot; &quot;-masm-verbose&quot;
    &quot;-munwind-tables&quot; &quot;-target-cpu&quot; &quot;penryn&quot; &quot;-dwarf-column-info&quot;
    &quot;-debugger-tuning=lldb&quot; &quot;-target-linker-version&quot; &quot;351.8&quot;

    &quot;&#47;Applications&#47;Xcode.app&#47;Contents&#47;Developer&#47;Platforms&#47;iPhoneSimulator.platform&#47;Developer&#47;SDKs&#47;iPhoneSimulator.sdk&quot;
    &quot;-include&quot;
    &quot;&#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;infer&#47;bin&#47;..&#47;lib&#47;clang_wrappers&#47;global_defines.h&quot;
    &quot;-Wno-ignored-optimization-argument&quot; &quot;-Wno-everything&quot;
    &quot;-fdebug-compilation-dir&quot; &quot;&#47;Users&#47;mingzhi.liu&#47;Desktop&#47;TON&#47;TON&quot;
    &quot;-ferror-limit&quot; &quot;19&quot; &quot;-fmessage-length&quot; &quot;0&quot; &quot;-stack-protector&quot; &quot;1&quot;
    &quot;-fblocks&quot; &quot;-fencode-extended-block-signature&quot;
    &quot;-fobjc-runtime=macosx-10.14.0&quot; &quot;-fobjc-exceptions&quot; &quot;-fexceptions&quot;
    &quot;-fmax-type-align=16&quot; &quot;-fdiagnostics-show-option&quot; &quot;-o&quot; &quot;RootVC.o&quot; &quot;-x&quot;
    &quot;objective-c&quot; &quot;RootVC.m&quot; &quot;-O0&quot; &quot;-include&quot;
    &quot;&#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;infer&#47;bin&#47;..&#47;lib&#47;clang_wrappers&#47;global_defines.h&quot;
    &quot;-Wno-everything&quot;</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/a9/ce5d2609.jpg" width="30px"><span>mosn</span> 👍（2） 💬（0）<div>infer --skip-analysis-in-path Pods </div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/05/b2776d73.jpg" width="30px"><span>Geek</span> 👍（2） 💬（0）<div>传统编译器的工作原理，基本上都是三段式的，可以分为前端、优化器和后端。前端负责解析源代码，检查语法错误，并将其翻译为抽象的语法树；优化器对这一中间代码进行优化，试图使代码更高效；后端则负责将优化器优化后的中间代码转换为目标机器的代码，这一过程后端会最大化的利用目标机器的特殊指令，以提高代码的性能。基于这个认知，我们可以认为 LLVM 包括了两个概念：一个广义的 LLVM 和一个狭义的 LLVM 。广义的 LLVM 指的是一个完整的 LLVM 编译器框架系统，包括了前端、优化器、后端、众多的库函数以及很多的模块；而狭义的 LLVM 则是聚焦于编译器后端功能的一系列模块和库，包括代码优化、代码生成、JIT 等。
--------------------- 
作者：艾蔓草 
来源：CSDN 
原文：https:&#47;&#47;blog.csdn.net&#47;xhhjin&#47;article&#47;details&#47;81164076 
版权声明：本文为博主原创文章，转载请附上博文链接！</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/c0/8d7dcaea.jpg" width="30px"><span>xixi</span> 👍（1） 💬（0）<div>APPCode 也有一个不错的</div>2020-11-18</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（1） 💬（0）<div>关于brew，因为我之前是在很久之前就安装了，所以现在在安装infer的时候会出现部分所需插件版本过低的情况。然后我想升级插件，也需要先更新brew，但我的brew更新也是失败：Error: &#47;usr&#47;local must be writable! 错误

这种情况下，还想是使用Brew进行安装的话，需要如下操作:
1.卸载旧的brew
```
&#47;usr&#47;bin&#47;ruby -e &quot;$(curl -fsSL https:&#47;&#47;raw.githubusercontent.com&#47;Homebrew&#47;install&#47;master&#47;uninstall)”

```
2.安装新的brew
```
&#47;usr&#47;bin&#47;ruby -e &quot;$(curl -fsSL https:&#47;&#47;raw.githubusercontent.com&#47;Homebrew&#47;install&#47;master&#47;install)&quot;
```
之后，再按照infer的安装提示一步步安装。</div>2019-03-28</li><br/><li><img src="" width="30px"><span>Geek_1ce2e0</span> 👍（1） 💬（0）<div>Swiftlint就行</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/63/6c387163.jpg" width="30px"><span>Nevermore</span> 👍（1） 💬（0）<div>SwiftLint</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/f4/abb7bfe3.jpg" width="30px"><span>Mr.C</span> 👍（0） 💬（0）<div>您好！我将自定义的插件集成到Xcode后，发现Xcode的自动补全功能失效了，请问有解决的办法吗？谢谢！</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/64/6f/2ce61440.jpg" width="30px"><span>黄苗炜</span> 👍（0） 💬（0）<div>老师，我想要git commit 提交之前，进行oclint或者infer，我想到是触发pre-commit 钩子，执行对应的脚本，输出一个html报告。但是我怎么从报告中提取信息告诉开发工程师，代码有问题，拒绝当次commit</div>2021-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/56/07920099.jpg" width="30px"><span>微笑美男😄</span> 👍（0） 💬（0）<div>老师 Infer可以用于swift吗</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/09/d0/baa520ac.jpg" width="30px"><span>无问西东</span> 👍（0） 💬（1）<div>用infer分析没cocoapod 管理的项目, 写个strong 的代理都检测不出来问题, cocoapod 管理后, 一直各种报错, 百度找了很久也没找到为什么, 菜鸡路过..., 有大佬路过指点一下吗?
</div>2020-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/33/42/a981ef2e.jpg" width="30px"><span>费城</span> 👍（0） 💬（0）<div>OCLint的最新安装使用，感觉也可以参考这个：https:&#47;&#47;juejin.im&#47;post&#47;5ce9f477f265da1b7c60f4fe#heading-4</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/94/5058c24f.jpg" width="30px"><span>疯狂的石头</span> 👍（0） 💬（0）<div>遇见这个问题的童鞋
Error: the following clang command did not run successfully:
    &#47;usr&#47;local&#47;Cellar&#47;infer&#47;0.15.0&#47;lib&#47;infer&#47;facebook-clang-plugins&#47;clang&#47;install&#47;bin&#47;clang 
去&#47;Library&#47;Developer&#47;CommandLineTools&#47;Packages这个目录，安装pkg可以解决</div>2019-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erhzZ8J7EZm0s94p1RTibOBzpqsbCajKYmkjX35Clfdvpv8ZdSKGicT2A4VyicIhy9yNjJjJcTeJX7rQ/132" width="30px"><span>烈人</span> 👍（0） 💬（0）<div>使用homebrew安装infer后，直接infer -- clang xx.m ，报头文件找不到。我也是无语。xcode10。然后扫描整个工程又是正常的。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/53/01a6c4da.jpg" width="30px"><span>GODV</span> 👍（0） 💬（0）<div>Error while trying to load a compilation database:
Could not auto-detect compilation database for file &quot;Hello.m&quot;
No compilation database found in &#47;Users&#47;***&#47;Desktop&#47;OCLintTest or any parent directory
用OCLint创建应该放在那个目录下，不太明白</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/09/05/c3eb8fa9.jpg" width="30px"><span>CalvinGao</span> 👍（0） 💬（0）<div>老师，-bash: scan-build: command not found 是什么原因呢，资源也下了，为什么会报这样的错误呢</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/9f/46ac03ad.jpg" width="30px"><span>快到碗里来</span> 👍（0） 💬（0）<div>infer扫描iOS单个文件报错 怎么回事啊</div>2019-04-19</li><br/>
</ul>