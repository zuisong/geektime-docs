你好，我是于航。

“WebAssembly（缩写为 Wasm）是一种基于堆栈式虚拟机的二进制指令集。Wasm 被设计成为一种编程语言的可移植编译目标，并且可以通过将其部署在 Web 平台上，以便为客户端及服务端应用程序提供服务”。这是 Wasm 官网给出的一段，对 “Wasm 是什么？” 这个问题的解答。

其实，在开设这门课程之前，我曾在国内的各类博客和资讯网站上查阅过很多有关 Wasm 的相关资料。发现大多数文章都会声称 “Wasm 是一种新型的编程语言”。但事实真的是这样的吗？希望本篇文章的内容，能够给你心中的这个问题一个更加明确的答案。要想了解 Wasm 究竟是什么，我们还要先从“堆栈机模型”开始说起。

## 堆栈机模型

堆栈机，全称为“堆栈结构机器”，即英文的 “Stack Machine”。堆栈机本身是一种常见的计算模型。换句话说，基于堆栈机模型实现的计算机，无论是虚拟机还是实体计算机，都会使用“栈”这种结构来实现数据的存储和交换过程。栈是一种“后进先出（LIFO）”的数据结构，即最后被放入栈容器中的数据可以被最先取出。

接下来，我们将尝试模拟堆栈机的实际运行流程。在这个过程中，我们会使用到一些简单的指令，比如 “push”，“pop” 与 “add” 等等。这里你可以把它们想象成一种汇编指令。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/1d/102caf26.jpg" width="30px"><span>IV0id</span> 👍（25） 💬（5）<div>我觉得应该是20啊，命令执行每一行命令之后stack状态如图
i32.const 1          |    1
i32.const 1          |    1，1
i32.eq                |     1
i32.const 10        |     1，10
i32.const 10        |     1，10，10 
i32.add               |      1，20
i32.mul               |       20</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（2）<div>wasm 就是一种可以在虚拟机上执行的字节码。
 对于 JS 引擎 v8 , SpiderMonkey, JavascriptCore 是不是都支持直接执行 wasm 字节码了？</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（3） 💬（1）<div>和汇编的区别是wasm最终是字节码，汇编的最终是机器码。字节码最后会被浏览器转成机器码吗？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（1）<div>说个最能让大家快速理解的说法，就是Java虚拟机，执行的是字节码，不管是什么jvm语言，Java，kotlin等，最后生成字节码就行，字节码就是WASM</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（2） 💬（1）<div>请教老师，如果想实现wasm的目的，能否直接使用jvm，而不是另外开发一套V-ISA.</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（2）<div>最后的结果应该是 110，错了请指正。
这节可以说完全道出了 webassembly 的本质，它并不是一种新的编程语言，因为你只需要编写其他的语言，例如 c++ 和 rust 从而生成对应的字节码。
对于栈模型的语言太多了，例如 Java，寄存器模型有 lua，请问一下老师累加器模型的编程语言有哪些了？</div>2020-09-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ewb31JsMN7J18ZoZMR2DBGvoxv06oLDuMGBibE4LfHVDHrwNb7JWPXia787OGKAkMUYrymLqmj2hWut1R4bzEWAQ/132" width="30px"><span>Geek_175b82</span> 👍（1） 💬（1）<div>这是不是类似于Java 的.class字节码文件？</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/d7/68/39608e68.jpg" width="30px"><span>严敏</span> 👍（0） 💬（1）<div>请问WASM中对在浏览器中对socker支持的如何</div>2023-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/3b/b4a47f63.jpg" width="30px"><span>only</span> 👍（0） 💬（1）<div>有一点不明白，是浏览器集成了wasm的虚拟机还是操作系统集成了wasm虚拟机?</div>2022-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/73/56/9cfb1e43.jpg" width="30px"><span>sheeeeep</span> 👍（0） 💬（2）<div>我的答案
1，1
1
1，10，10
1，110
110</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（2） 💬（0）<div>需要理解的就是 i32.eq 对应的 operator ：https:&#47;&#47;webassembly.github.io&#47;spec&#47;core&#47;exec&#47;numerics.html#op-ieq</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/33/de01b796.jpg" width="30px"><span>胖狐狸</span> 👍（0） 💬（0）<div>说结果是110的都是看了旁边这个沙雕的ai吧？百度文言一心这水平真是一言难尽
</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（0）<div>本质上是一种编码的方式。跟汇编语言和vm里的字节码,llrm的中间代码一样，通过助记符来帮助我们来形成一个中间层来帮助我们解决移植的问题。</div>2022-12-02</li><br/>
</ul>