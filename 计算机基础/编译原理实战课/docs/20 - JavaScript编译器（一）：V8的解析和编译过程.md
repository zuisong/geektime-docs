你好，我是宫文学。从这一讲开始，我们就进入另一个非常重要的编译器：V8编译器。

V8是谷歌公司在2008年推出的一款JavaScript编译器，它也可能是世界上使用最广泛的编译器。即使你不是编程人员，你每天也会运行很多次V8，因为JavaScript是Web的语言，我们在电脑和手机上浏览的每个页面，几乎都会运行一点JavaScript脚本。

扩展：V8这个词，原意是8缸的发动机，换算成排量，大约是4.0排量，属于相当强劲的发动机了。它的编译器，叫做Ignition，是点火装置的意思。而它最新的JIT编译器，叫做TurboFan，是涡轮风扇发动机的意思。

在浏览器诞生的早期，就开始支持JavaScript了。但在V8推出以后，它重新定义了Web应用可以胜任的工作。到今天，在浏览器里，我们可以运行很多高度复杂的应用，比如办公套件等，这些都得益于以V8为代表的JavaScript引擎的进步。2008年V8发布时，就已经比当时的竞争对手快10倍了；到目前，它的速度又已经提升了10倍以上。从中你可以看到，编译技术有多大的潜力可挖掘！

对JavaScript编译器来说，它最大的挑战就在于，当我们打开一个页面的时候，源代码的下载、解析（Parse）、编译（Compile）和执行，都要在很短的时间内完成，否则就会影响到用户的体验。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（4） 💬（1）<div>“Ignition 是一个基于寄存器的解释器。它把函数的参数、变量等保存在寄存器里。不过，这里的寄存器并不是物理寄存器，而是指栈帧中的一个位置。”请问老师，这样的话它跟基于栈的解释器有多大区别呢？</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（2） 💬（1）<div>&quot;Preparser 粗略地解析一遍程序，在正式运行某个函数的时候，编译器才会按需解析这个函数。&quot;——是否可以理解为，v8的懒解析是以js中的函数为原子粒度的？是否存在对较大的语法块，比如switch、某个if的条件内逻辑非常庞大等部分单独作为懒解析呢？ 因为有可能说一个if判断条件很少为true，但内部代码行数达到几百行，一次性解析成AST比较浪费... 但如果按function的粒度，这种情况也都会被一次性完全解析成AST了</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（2） 💬（10）<div>宫老师，想请教下在自己的c++项目中 如果想引入v8，对js source code作AST-parse，甚至单独抽出v8当中的某一些部分来做些事情，这方面是否有什么好的资料可以参考？在v8.dev官网似乎并没找到很详细的这方面的guidance，我经常遇到的就是很多头文件的依赖需要手动处理，毕竟v8本身的编译是基于ninja的，而自己的一些c++项目通常在mac本地会用xcode（v8项目中似乎有个可以build出.xcodeproj工程目录的选项，但我build出来放进xcode里一大堆报错，根本跑不通&gt;.&lt;），或者在linux上用make方式，这会遇到很多坑需要踩，不知这方面有没有比较好的资料推荐？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/5c/e09eac13.jpg" width="30px"><span>刘強</span> 👍（0） 💬（0）<div>有点奇怪，解释器也是一个程序，解释执行字节码，为什么能用上物理寄存器</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/d1/2bf322ed.jpg" width="30px"><span>VoiceWitness</span> 👍（0） 💬（0）<div>【你可以在终端测试一下懒解析和完整解析的区别。针对 foo.js 示例程序，你输入“.&#47;d8 – ast-print foo.js”命令。】
这里应该是 --print-ast
</div>2022-10-11</li><br/>
</ul>