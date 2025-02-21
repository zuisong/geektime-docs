你好，我是于航。

应用 Wasm 的常见方式有几种类型，一种方式是通过 Web 浏览器提供的 JavaScript API 与 Web API ，来在 Web 应用中调用从 Wasm 模块中导出的函数。通过这种方式，我们可以充分利用 Wasm 的安全、高效及可移植性等优势。

另一种方式是通过 WASI 抽象系统调用接口，以便在 out-of-web 应用中使用 Wasm。这种使用方式与 Web 端大同小异，不过区别是可以借助底层运行时的能力，使得我们构建出的 Wasm 应用可以在 Web 浏览器外的 Native 环境中与操作系统打交道，并同样享受着 Wasm 本身所带来的安全、高效及可移植性。

而今天我们要介绍的另外一个 Wasm 的应用场景，则相对有些特殊。在大多数时候，我们都是将由诸如 C/C++ 以及 Rust 等语言编写的源代码，编译至 Wasm 字节码格式来使用。假设此时我们想要设计开发一款自定义的静态编程语言，那么怎样才能够方便快捷地为它的编译器添加一个能力，可以让编译器支持将 Wasm 作为编译目标呢？

关于这个问题，我们要先从传统的编译器链路开始说起。

## 传统编译器链路

对于传统的静态语言编译器来说，通常会采用较为流行的“三段式”链路结构。如下图所示，三段式结构分别对应着整个编译器链路中三个最为重要的组成部分：编译器前端（Compiler Frontend）、中间代码优化器（Optimizer），以及编译器后端（Compiler Backend）。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（5） 💬（2）<div>使用llc编译后可以在浏览器中运行了吗？好emscripten编译上有什么差异？</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/db/791d0f5e.jpg" width="30px"><span>俺足</span> 👍（0） 💬（1）<div>请教于老师，我mac里没有wasm32 或 wasm64的目标怎么安装呢？ 有其他同学知道吗</div>2022-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/53/871b2161.jpg" width="30px"><span>鹦鹉</span> 👍（9） 💬（0）<div>类似操作系统的 32 位与 64 位之分. 简而言之, wasm32 与 wasm64 的区别主要在于内存寻址范围的不同, 对于 wasm32 仅能对 2 的 32 次方(大约 4GB) 的线性内存范围进行寻址, 而 wasm64 能够在更大范围的内存中寻址. 虽然现在我们的操作系统基本都是 64 位, 但对于 wasm 来说, 区分 wasm32 和 wasm64 两个编译目标的主要的原因在于: 绝大多数 wasm 应用都不需要使用到超过 4GB 的内存.
参考: https:&#47;&#47;webassembly.org&#47;docs&#47;faq&#47;</div>2020-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（0）<div>llc add.ll -filetype=obj -mtriple=wasm64 -o add1.wasm
在 Mac 平台 执行这行命令，生成  wasm64 的目标代码，提示 不支持的
LLVM ERROR: 64-bit WebAssembly (wasm64) is not currently supported

版本信息：
LLVM (http:&#47;&#47;llvm.org&#47;):
  LLVM version 10.0.1
  Optimized build.
  Default target: x86_64-apple-darwin19.3.0
  Host CPU: skylake</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（0）<div>存在 wasm32 和 wasm64的平台， 应该可以操作系统 中存在64和32 位的原因是一样的
1:  64 有更大的 CPU 位宽，可以进行更大的数值的计算
2:  内存寻址空间大小不一样</div>2020-10-07</li><br/>
</ul>