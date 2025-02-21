你好，我是于航。

在之前两个章节的内容中，我们讲解了 Wasm 相关的核心原理，并介绍了 Wasm 在实际各个应用领域内的一些实践情况。从这一讲开始，我们将进入“实战篇”。作为第一个实战应用，我会手把手教你从零构建一个完整的 Wasm Web 应用。

具体是什么应用呢？你应该还记得，前面我们曾讲过一节课，题目是 “WebAssembly 在物联网、多媒体与云技术方面有哪些创新实践？” 。在那节课中，我们曾谈到过 Wasm 在 Web 多媒体资源处理领域所具有的极大优势。因此，接下来我们将一起尝试构建的应用，便是这样一个基于 Wasm 的在线 DIP 应用。

我把这个构建 Wasm Web 应用的完整过程，分成了上中下三讲。希望在你学完这三讲之后，能够游刃有余地了解一个 Wasm Web 应用从 0 到 1 的完整构建过程。我会在课程中尽量覆盖到足够多的实现细节，这样你可以通过细节去结合各方面的知识，不会在学习的过程中出现“断层”。

那接下来我们就直接进入主题，先来了解下这个 DIP 应用的概况。

## DIP 应用概览

DIP 的全称为 “Digital Image Processing”，即“数字图像处理”。在我们将要构建的这个 Web 应用中，我们将会为在线播放的流媒体资源，去添加一个特定的实时“图像处理滤镜”，以改变视频本身的播放显示效果。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/b4/bb/73586c43.jpg" width="30px"><span>张凯</span> 👍（2） 💬（1）<div>作为一个c++领域的web菜鸟，勉力看之，这个wasm是放到服务器上，客户端需要把这个文件一次性的加载到本地？？</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（4）<div>相比WebGL实现的滤镜有性能优势吗？</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（2） 💬（1）<div>emscripten的不同版本对编译后的wasm产物性能上会有差异吗？</div>2020-10-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIG27Geoy2wMlbUOYVRJwWRwaaARICQyQdC9no0A1qcY4uo62yX76DI8mWv89hXicv52DwMevlHbqg/132" width="30px"><span>Quickeryi</span> 👍（0） 💬（1）<div>“为了能够支持在 Web 浏览器中“使用”诸如 std::fopen 等 C&#47;C++ 语言中，用于访问本机文件资源的标准库函数，Emscripten 会使用诸如 LocalStorage 之类的浏览器特性，来模拟完整的 POSIX 文件操作和相关的数据结构。当然，只不过这一切都是使用 JavaScript 来模拟实现的”
关于上面的说法有个疑问，难道不是因为浏览器提供了对应的wasm runtime？</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/89/44/20c1b56b.jpg" width="30px"><span>看不山是山,看水是不水。</span> 👍（0） 💬（3）<div>在c中就只写了个malloc n个字节的接口和一个free的接口，并导出这两个接口，在html中先malloc一个大内存，比如100M,之后马上调用free接口，在任务管理器看内存参数，free之后怎么没有看到内存减少是什么现象啊</div>2021-07-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/pTZS48zWWAhI0zGXrib8s124HSenCS2FTDD0r4SKCqw2ub4adicI4x2wTeH7bHdlsl8QwxeVmzTGs1PIImURxxPg/132" width="30px"><span>itgou</span> 👍（0） 💬（2）<div>wasm能否实现解码rtsp并在网页上播放呢？目前网页播放rtsp困难重重，几乎都是要在服务器端转码才能播放</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/42/e1757583.jpg" width="30px"><span>Jason Yu 于航</span> 👍（4） 💬（0）<div>源码可以参考这里：https:&#47;&#47;github.com&#47;Becavalier&#47;geektime-wasm-tutorial。</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/5d/a09da7d5.jpg" width="30px"><span>高鹏gaopeng</span> 👍（2） 💬（0）<div>“还记得在今天的 Emscripten 实例中，我们使用到了名为 “EMSCRIPTEN_KEEPALIVE” 的宏，来确保被标记的函数不会被编译器优化掉。那么，你知道它具体是怎样实现的吗？”

用 __attribute__((used)) 来标记，防止链接器会优化删除未被使用的数据。</div>2022-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/7a/1176bc21.jpg" width="30px"><span>Yarco</span> 👍（1） 💬（3）<div>注: 
1. 第一次编译需要生成各种系统库 感觉会比较慢
2. 我homebrew安装的 emcc (不知道是不是这个原因) 会出错说  “html-minifier-terser was not found! ” 需要手工安装依赖包</div>2020-10-07</li><br/>
</ul>