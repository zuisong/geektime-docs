前面我们已经花了很多篇幅来介绍JavaScript是如何工作的，了解这些内容能帮助你从底层理解JavaScript的工作机制，从而能帮助你更好地理解和应用JavaScript。

今天这篇文章我们就继续“向下”分析，站在JavaScript引擎V8的视角，来分析JavaScript代码是如何被执行的。

前端工具和框架的自身更新速度非常快，而且还不断有新的出现。要想追赶上前端工具和框架的更新速度，你就需要抓住那些本质的知识，然后才能更加轻松地理解这些上层应用。比如我们接下来要介绍的V8执行机制，能帮助你从底层了解JavaScript，也能帮助你深入理解语言转换器Babel、语法检查工具ESLint、前端框架Vue和React的一些底层实现机制。因此，了解V8的编译流程能让你对语言以及相关工具有更加充分的认识。

要深入理解V8的工作原理，你需要搞清楚一些概念和原理，比如接下来我们要详细讲解的**编译器（Compiler）、解释器（Interpreter）、抽象语法树（AST）、字节码（Bytecode）、即时编译器（JIT）**等概念，都是你需要重点关注的。

## 编译器和解释器

之所以存在编译器和解释器，是因为机器不能直接理解我们所写的代码，所以在执行程序之前，需要将我们所写的代码“翻译”成机器能读懂的机器语言。按语言的执行流程，可以把语言划分为编译型语言和解释型语言。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/50/96/dd23dcb0.jpg" width="30px"><span>不将就</span> 👍（86） 💬（9）<div>重复看之前的文章，受益良多，在此表示感谢！
不过有几个疑问，老师有空的解答下哈！

问题一: 渲染进程里的input标签上传图片，通过与浏览器主进程通信，主进程读取硬磁盘图片数据返回给渲染进程，渲染进程里的js发起ajax请求，是通过浏览器主进程去调用网络进程发起请求，还是渲染进程可以直接调用网络进程发起请求？

问题二: 请求长时间处于pending状态或者脚本执行死循环，这时刷新或前进后退页面不响应，刷新或前进后退页面是属于浏览器主进程的UI交互行为，为什么渲染进程里的js引擎执行会影响到主进程？

问题三: 
function fn(){

var a =10

function f1(){

console.log(a)

};

function f2(){

console.log(&#39;f2&#39;)

};

f2();

};

fn();

我在函数f2里打断点，当执行到函数f2时，chrome里显示Closure:{a:10},如果把这个原因解释为在fn函数里会预扫描f1函数，那我现在把fn2函数和调用都注释了，现在执行fn函数时不产生Closure，为什么就不预扫描f1函数了？这是为什么？


</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e0/cf/08b04e00.jpg" width="30px"><span>钟钟</span> 👍（50） 💬（9）<div>执行时间越长，执行效率越高。是因为更多的代码成为热点代码之后，转为了机器码来执行吗？</div>2019-09-08</li><br/><li><img src="" width="30px"><span>Rapheal</span> 👍（46） 💬（7）<div>老师，编译的基本单位是一段JS代码（内敛JS）或者一个JS文件吗(还是以当前调用栈将要执行函数为单位）？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/2f/6efc3051.jpg" width="30px"><span>GY</span> 👍（12） 💬（5）<div>前面第7和第12讲，变量提升说js的执行过程，是有编译过程的，变量提升就发生在编译过程，经过编译后，会生成两部分内容，执行上下文和可执行代码，但是在这一讲中，却并没有编译过程，在AST生成后，解释器就开始执行生成字节码执行了，这几讲的内容有点互相冲突，那么详细的过程到底是怎样的呢
我在查看其它资料，出现了预编译这个名词，这个又怎么解释呢
希望能解答下</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/88/82/b789613e.jpg" width="30px"><span>Bazinga</span> 👍（10） 💬（2）<div>总结说：V8 依据 JavaScript 代码生成 AST 和执行上下文，再基于 AST 生成字节码，然后通过解释器执行字节码，通过编译器来优化编译字节码。但是第二节生成字节码那一段 说：解释器 Ignition 就登场了，它会根据 AST 生成字节码，并解释执行字节码。还有即时编译（JIT）技术那张图片，看起来也是先生成字节码 再经过解释器 。 所以字节码是解释器生成的吗？我都看懵了，求解答。</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（9） 💬（1）<div>字节码最终也会转成机器码来执行的吧？因为最终都是cpu来执行，cpu只能执行机器码</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（7） 💬（2）<div>我理解，V8执行越久，被编译成机器码的热点代码就越多，所以整体执行效率就越高。如果是这样的话，那么V8内存占用也会越来越多，会面临的问题会和</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（7） 💬（7）<div>避免大的内联脚本，因为在解析 HTML 的过程中，解析和编译也会占用主线程；这句话可以理解为解析HTML代码的时候需要解析内联代码，而放到js文件的时候不需要吗？
另外思考题应该是执行越久，热点代码越多，即时编译的作用越大。</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（7） 💬（1）<div>怎么都需要字节码文件，为啥，jsvaScript不像java一样先编译为字节码，这样执行效率不就高了么！</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（3） 💬（2）<div>V8执行越久，被编译成机器码的热点就越多，这些机器码帮助字节码可以直接执行而不用再使用解释器逐行执行，这相当于浏览器缓存，提高了执行性能。这些生成的机器码也会带来内存占用升高的问题，这里应该会有一个权衡措施吧，根据已占用的内存权衡如何判定是热点并生成机器码保存。</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（2） 💬（1）<div>V8 执行一段代码流程图 中，感觉图最下面的那个箭头不对吧，应该不是机器码，而是解释执行吧</div>2019-09-05</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（1） 💬（1）<div>知识的关联性让我在本节内重温了另外两个专栏的内容，JAVA核心技术专栏的JIT以及编译原理之美专栏的编译过程……底层基础知识的重要性真的不能忽视……之前我认识不清前端和后端，现在通过这几章的学习逐渐清晰了一些，看到了区别亦看到了相同点……</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>两个问题：1 “这段代码经过javascript-ast站点处理后&quot;，此句中“站点”对吗？2 Vue和React、bootstrap都是用于移动端开发吗？ 我开发PC端网页可以用吗？如果不能用，那PC端开发用什么前端框架？</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/a9/b3dcc723.jpg" width="30px"><span>舔命难违</span> 👍（31） 💬（9）<div>“V8 执行时间越久，执行效率越高”，难怪我电脑开机越久就越卡……</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（23） 💬（0）<div>从本文中明确的应该是在写代码的时候，如何让代码易于被 TurboFan 优化，减少反优化，老师提到的 hiddenClass 等我觉得大家还是有必要了解一下， 大家可以尝试使用 node 加选项 --trace-opt 跑代码体验一下 TurboFan 如何做优化，就会有很直观的感受 https:&#47;&#47;github.com&#47;hjzheng&#47;performance-test&#47;blob&#47;master&#47;v8&#47;addFunction.js</div>2019-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ0F94uoYZQicRd7YEFjEJWm0EaUJXzkhiaqa5GQQ8a1FkicQIoHC4sp2ZG9m1JAFABuGsj34ucztjibA/132" width="30px"><span>Geek_Jamorx</span> 👍（7） 💬（12）<div>我想提一个问题，V8解析后的字节码或热节点的机器码是存在哪的，是以缓存的形式存储的么？和浏览器三级缓存原理的存储位置比如内存和磁盘有关系么？
最近面试有被问到，没答上来。。希望老师回答，十分感谢~</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ce/62/026e4408.jpg" width="30px"><span>阳仔</span> 👍（4） 💬（1）<div>面试被问到：js 在编译过程中，会做一定的优化，那么日常开发，应该怎么利用这个优化，提升代码质量</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b9/0d/ae745ec0.jpg" width="30px"><span>刹那</span> 👍（3） 💬（4）<div>想到一个问题，可以把代码预先编译成字节码吗？这样浏览器下载了就能直接运行</div>2019-10-22</li><br/><li><img src="" width="30px"><span>Geek_panda</span> 👍（2） 💬（4）<div>老师还在吗，想请教2个问题
1. v8生成执行上下文是根据源码生成还是根据ast来生成呢？
2. 解释器执行字节码时是不是也需要将他转成机器码，如果是的话，那他是不是也会通过TurboFan编译器编译
@李兵 老师</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/10/4a/1a549f4e.jpg" width="30px"><span>crown</span> 👍（2） 💬（0）<div>V8刚开始执行代码的时候, 都是通过ignition解释器来逐行解析字节码的, 这样性能会比较慢. 当执行一段时间过后, ignition可以捕获到经常被执行的到的字节码.  这些字节码就会被作为热代码交给turbofan编译成为机器码. 后续可以直接使用机器码, 而机器码的执行效率优于字节码. 当V8执行越久, 使用量高的字节码都被编译为机器码. 故V8执行越久, 效率越高</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（2） 💬（2）<div>老师您好，我曾想过不用babel typescript等的ast而是自己开发一个c++项目，引入v8利用他的ast来做一些代码转换工作，这样可以基于c的很多机制做更多多线程方面的优化。后发现这对于v8来说是不可能的，因为v8是一部分一部分解析js的，v8为什么采用这样的机制呢？另外这方面如果想自己动手拿v8做些事儿 老师有什么推荐的资料 或书籍可以看看吗？</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/f6/3e2db176.jpg" width="30px"><span>七月有风</span> 👍（2） 💬（2）<div>老师,你好，node 的 JavaScript 引擎是 V8, ReactNative 和 Android webview 的 JavaScript 引擎是V8引擎吗？</div>2019-12-07</li><br/><li><img src="" width="30px"><span>Geek_177f82</span> 👍（2） 💬（2）<div>问一个基础的问题。希望老师解答。编译器编译后的二进制文件，与解析器解析后机器码是一个东西吗？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/22/257e9e21.jpg" width="30px"><span>Bryant-cx</span> 👍（1） 💬（0）<div>代码第一次执行的时候，解释器Ignition会逐条执行。但是在Ignition执行字节码的过程中，如果发现某一段代码被重复执行，那么后台的编译器TurboFan就会把该段热点的字节码编译为高效的机器码。当再次执行这段被优化的代码时，只需要执行这段被编译后的机器码即可，这样就大大提升了代码的执行效率。</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/30/b10d8b5a.jpg" width="30px"><span>😈Kyui</span> 👍（1） 💬（0）<div>老师能不能讲一下什么是反优化，以及如何触发的？</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/05/b8e769fa.jpg" width="30px"><span>Mickey</span> 👍（1） 💬（0）<div>看到这里，还是要感慨一下，老师好厉害，感觉自己还有很长的路子要走。</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/6c/923bced2.jpg" width="30px"><span>Yeehow Chng</span> 👍（1） 💬（0）<div>请问什么是V8的反优化?</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（1） 💬（1）<div>既然v8用到了编译器 可否认为js也得门编译型语言</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/de/ff/8b3b2e87.jpg" width="30px"><span>Clfeng</span> 👍（0） 💬（0）<div>可以顺便讲讲解释器遇到eval和new Function时的处理会有些怎样的不同吗？

</div>2024-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/d9/00870178.jpg" width="30px"><span>Slowdive</span> 👍（0） 💬（0）<div>老师的这个课真是常看常新，那些新出来的花里胡哨的技术最终的本质都能在这个课里看到</div>2024-09-22</li><br/>
</ul>