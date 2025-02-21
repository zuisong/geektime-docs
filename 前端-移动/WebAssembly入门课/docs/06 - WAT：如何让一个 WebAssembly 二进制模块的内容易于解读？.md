你好，我是于航。

在前面的两节课中，我们分别讲解了 Wasm 模块在二进制层面的基本组成结构与数据编码方式。在 04 的结尾，我们还通过一个简单的例子，逐个字节地分析了定义在 C/C++ 源代码中的函数，在被编译到 Wasm 之后所对应的字节码组成结构。

比如字节码 “0x60 0x2 0x7f 0x7f 0x1 0x7f” ，便表示了 Type Section 中定义的一个函数类型（签名）。而该函数类型为 “接受两个 i32 类型参数，并返回一个 i32 类型值”。

我相信，无论你对 Wasm 的字节码组成结构、V-ISA 指令集中的各种指令使用方式有多么熟悉，在仅通过二进制字节码来分析一个 Wasm 模块时，都会觉得无从入手。那感觉仿佛是在上古时期时，直接面对着机器码来调试应用程序。那么，有没有一种更为简单、更具有可读性的方式来解读一个 Wasm 模块的内容呢？答案，就在 WAT。

## WAT（WebAssembly Text Format）

首先，我们来直观地感受一下 WAT 的“样貌”。假设我们有如下这样一段 C/C++ 源代码，在这段代码中，我们定义了一个函数 factorial，该函数接受一个 int 类型的整数 n，然后返回该整数所对应的阶乘。现在，我们来将它编译成对应的 WAT 代码。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（7） 💬（3）<div>老师您好，请教一个问题。我们一般都是把c或者c++直接编译成wasm，只要native通了，wasm也没问题。那么出现wat得意义在哪里？貌似不需要通过wat来调试之类的……</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（3） 💬（1）<div>感觉 Flat-WAT，比 WAT 看着好懂，为啥不直接只用 Flat-WAT？</div>2020-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（2） 💬（1）<div>老师能在浏览器中像调试js一样调试wasm的C代码吗？（浏览器source中显示C代码，断点单步调试？）我自己尝试了一些方法还没成功</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/38/42ff18f1.jpg" width="30px"><span>Running</span> 👍（1） 💬（1）<div>因为最近工作涉及到一些WASM，及时购买了这个课程恶补基础，很好的一门课程。最近遇到一点技术问题想请教一下于老师，Chrome Web Store要求新上架的应用需要支持Manifest V3, 由于应用有部分代码是使用C语言实现的，编译成WASM，那么问题是WASM 在支持 Manifest V3 遇到了加载的问题。 在Manifest V2使用CSP unsafe-eval 是可以运行的，但是V3 已经禁止了eval运行。
https:&#47;&#47;bugs.chromium.org&#47;p&#47;chromium&#47;issues&#47;detail?id=1173354#c19  于老师，对于这个问题有什么建议吗?这个问题困扰了好久 </div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（0） 💬（1）<div>老师您好 有个问题请教一下：
正文中 “经过编译和转换后，该函数对应的 WAT 文本代码如下所示。”下面的wat代码，我使用WABT中的wat-desugar进行flat时候出现错误：
ASM&#47;test.wat:8:6: error: unexpected token &quot;get_local&quot;, expected an expr.
..&#47;..&#47;WASM&#47;test.wat:11:4: error: unexpected token set_local.
..&#47;..&#47;WASM&#47;test.wat:15:4: error: unexpected token (, expected ).
..&#47;..&#47;WASM&#47;test.wat:15:5: error: unexpected token set_local.
..&#47;..&#47;WASM&#47;test.wat:17:7: error: unexpected token &quot;get_local&quot;, expected an expr.
..&#47;..&#47;WASM&#47;test.wat:18:7: error: unexpected token get_local.
..&#47;..&#47;WASM&#47;test.wat:21:5: error: unexpected token set_local.
..&#47;..&#47;WASM&#47;test.wat:22:6: error: unexpected token tee_local.
..&#47;..&#47;WASM&#47;test.wat:24:8: error: unexpected token &quot;get_local&quot;, expected an expr.
..&#47;..&#47;WASM&#47;test.wat:27:5: error: unexpected token ), expected EOF.
这个是什么原因呢 是我的wabt安装的不正确么</div>2022-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/59/90/e763ed18.jpg" width="30px"><span>Clearly</span> 👍（0） 💬（1）<div>老师那个给的演示地址，查看对应生成的 WAT 可读文本代码，怎么用啊，一直在build状态</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/60/bb/69cc96cb.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>老师的原理讲解很细致，受益匪浅，以前自认为自己了解了 wasm，课程看到此意识到自己所知甚少。谢谢于老师的讲解，期待于航老师的实战讲解！</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（1） 💬（0）<div>wat 代码里出现了多次 255 立即数，请问是用来做什么的？按理说 i32 的最大值也不是 255 吧。</div>2023-05-04</li><br/>
</ul>