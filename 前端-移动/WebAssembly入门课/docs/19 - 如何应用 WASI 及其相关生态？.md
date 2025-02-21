你好，我是于航。

作为“实践篇”的最后一课，今天我们来一起看看“如何从零构建一个 WASI 应用？”。在实践篇的前三节课里，我花了大量的篇幅来介绍如何基于 Emscripten ，去构建一个可以运行在 Web 浏览器中的 Wasm 应用。而基于 WASI 构建的 Wasm 应用将会被运行在浏览器之外的 Native 环境中，因此其构建和使用方式与基于 Emscripten 的 Wasm 应用有所不同。

但也正如我们在第 [07](https://time.geekbang.org/column/article/287138) 讲中介绍的那样，WASI 本身作为一种抽象的操作系统调用接口，对上层的应用开发者来说，没有较为直接的影响。

甚至对于同样的一段可以被编译为本地可执行应用程序的代码来说，我们只需要适当调整编译器的相关设置，就可以在不做任何代码更改的情况下，编译出所对应的 WASI 版本代码（也就是 Wasm 字节码）。然后再配合相应的 Wasm 虚拟机，我们就能够以“另一种方式”来执行这些代码了。

总的来说你可以看到，相较于传统的可执行文件，WASI 应用程序的整个“生命周期”基本上只有“编译”与“运行”两个阶段会有所不同。在接下来的内容中，我们将以一段 C/C++ 代码入手，来从编码、编译，再到运行，一步步带你完成这个 WASI 应用。

## 编码

首先，我们先来编写应用对应的 C/C++ 代码，这部分内容如下所示。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/df/7a/1176bc21.jpg" width="30px"><span>Yarco</span> 👍（3） 💬（2）<div>不知道chrome扩展开发是否支持wasm代码的运行... </div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（1） 💬（1）<div>老师之前我在Twitter上看到说如果wasm+wasi早点出来，就没docker什么事情了，具体原因还希望老师多说一下。</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（1） 💬（1）<div>WASI的目的：相对java的优势是在可以把已经存在的C&#47;C++等代码库功能变异成跨平台。不知道我理解是否对？这部分对前端会有什么影响吗？</div>2020-10-16</li><br/><li><img src="" width="30px"><span>Geek_362e38</span> 👍（0） 💬（0）<div>请问我想在electron主进程（nodejs环境）调用.wasm文件要怎么做？其中.wasm文件是通过wasi-sdk转化的，其中访问了操作系统功能，会在当前路径创建一个hello.txt并且写入部分内容。</div>2023-09-13</li><br/>
</ul>