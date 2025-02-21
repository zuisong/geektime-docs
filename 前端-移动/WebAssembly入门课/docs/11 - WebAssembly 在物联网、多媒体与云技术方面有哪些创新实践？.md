你好，我是于航。

我们继续接着上节课的内容，来一块看看 Wasm 在应用实践领域有哪些“新鲜事”。今天我们要来聊的是 Wasm 在物联网、多媒体与云技术领域内的一些创新性实践。我们一直说 Wasm 虽然“出身”于 Web，但实际上却也可以 out-of-web。

Wasm 本身作为一种新的虚拟机字节码格式，其使用场景从来都不会被仅仅限制在某个领域。鉴于 Wasm 在这些领域内的相关实践数量众多，因此在本节课里，我们仅挑选一些比较典型且具有一定现实意义的创新性实践来进行介绍。同时也欢迎你在评论区和我进行互动，补充一下你所知道的 Wasm 在这些或者其他领域内的相关实践。

## 物联网（IoT）

物联网（Internet of Thing），我们一般简称为 IoT。是指相对于传统的手机、笔记本电脑等大型电子设备来说，其可使用资源被有所限制（比如单核的 CPU、仅有几百 KB 的内存和硬盘容量、有限的网络上传速度，或仅需纽扣电池进行供电等）的小型嵌入式设备。

因此，相较于为传统 PC计算机等大型电子设备开发应用程序而言，为嵌入式设备开发程序则需要特殊的编程实践方法，以用来应对有限的软硬件资源。

### 统一的编程接口

在 IoT 刚刚走入人们视野的最初几年，人们通常只能够使用 C/C++ 甚至是汇编语言，来为这些物联网嵌入式设备编写应用程序。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（3） 💬（2）<div>您好老师，看完这节课，我想问一下是否有树莓派+wasm构建的demo，我想自己尝试一下。但是没有什么思路</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/a0/15c82d8b.jpg" width="30px"><span>Triton</span> 👍（1） 💬（1）<div>请问老师编译第三方包使用的wasm程序都需要使用到Emscripten，ogv.js也是生成一个ogv.wasm的文件么？对于Webpack的项目 如何优雅的引入这类型的文件？</div>2020-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/7a/1176bc21.jpg" width="30px"><span>Yarco</span> 👍（1） 💬（1）<div>&quot;通过使用 Unikraft，我们可以构建一个基于 Wasm 运行时的操作系统微内核&quot;
所以加入图形界面就变成另一个操作系统了？ </div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/35/74c36f63.jpg" width="30px"><span>Natsuki</span> 👍（0） 💬（1）<div>webpack 的 import wasm 的我研究了好长时间，它在编译 打包 wasm 的时候已经写好了 WebAssembly. compile 和 WebAssembly. instantiate，我看了源码看了好久没看懂 importObject 怎么传给 WebAssembly. instantiate，老师可以帮忙解答写吗？ https:&#47;&#47;github.com&#47;webpack&#47;webpack&#47;blob&#47;master&#47;lib&#47;wasm-sync&#47;WasmChunkLoadingRuntimeModule.js （大概是 292 - 344 行）</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/97/93e82345.jpg" width="30px"><span>陆培尔</span> 👍（9） 💬（0）<div>在云原生领域还有一个比较重要的应用方向，即istio团队目前在大力推广的基于wasm plugin机制的envoy扩展方式，这是目前istio团队主推的扩展模式，用于取代原有的mixer组件。</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/b1/fb117c21.jpg" width="30px"><span>先听</span> 👍（1） 💬（0）<div>以前不太喜欢帅男人，听到现在，感觉再帅也不是问题了。很喜欢这个内容和透露出的态度</div>2020-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>wasm 用在后端服务器上最大的优势可能是节省进程启动和销毁的开销了。请求来的时候当场分配资源来处理请求，请求结束后销毁全部资源，应用程序本身无需自己处理资源回收的事情，进程也不需要启动和销毁。</div>2023-05-09</li><br/>
</ul>