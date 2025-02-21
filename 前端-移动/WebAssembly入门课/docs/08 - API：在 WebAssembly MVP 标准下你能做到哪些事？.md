你好，我是于航。

在目前与 Wasm 相关的一系列标准中，我们可以将这些标准主要分为两个部分：“Wasm 核心标准（Core Interfaces）”以及“嵌入接口标准（Embedding interfaces）”。

其中，“Wasm 核心标准”主要定义了与 “Wasm 字节码”、“Wasm 模块结构”、“WAT 可读文本格式”以及模块验证与指令执行细节等相关的内容。关于这部分标准中的内容，我在前面几节课中，已经有选择性地为你挑选了部分重点进行解读。

而另一个标准“嵌入接口标准”，则定义了有关 Wasm 在 Web 平台上，在与浏览器进行交互时所需要使用的相关 Web 接口以及 JavaScript 接口。在本节课里，我们将讨论有关于这些 API 接口的内容。相信在学完本节课后你便会知道，在当前的 MVP 标准下，我们能够使用 Wasm 在 Web 平台上做些什么？哪些又是 Wasm 暂时无法做到的？

## Wasm 浏览器加载流程

那在开始真正讲解这些 API 之前，我们先来看一看，一个 Wasm 二进制模块需要经过怎样的流程，才能够最终在 Web 浏览器中被使用。你可以参考一下我画的这张图，这些流程可以被粗略地划分为以下四个阶段。

![](https://static001.geekbang.org/resource/image/8f/19/8f6880ef50727f61c5f1b72039cf5819.png?wh=1772%2A266)

首先是 “Fetch” 阶段。作为一个客户端 Web 应用，在这个阶段中，我们需要将被使用到的 Wasm 二进制模块，从网络上的某个位置通过 HTTP 请求的方式，加载到浏览器中。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/a6/6373416f.jpg" width="30px"><span>青史成灰</span> 👍（4） 💬（1）<div>从第一课到现在，都是文本。。。多搞点代码，是不是更好些。毕竟程序员，代码比文本更加直观</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（1）<div>获取完之后，没有全部编译成平台相关的机器码吧？还有一部分字节码，解释执行</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（1） 💬（1）<div>您好老师，麻烦问一下wasm在浏览器中执行的时候，也有内存对齐这一说吗？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>在 nodejs 的环境中进行测试 ，也是有上面那些 WebAssembly  的构造函数和方法的， 那么可以直接在 nodejs 的生产环境中使用吗？ 兼容程度是怎么样的？</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/75/35/a0c15ca8.jpg" width="30px"><span>一頭蠻牛</span> 👍（0） 💬（1）<div>最想听听老师分析下 浏览器编译wasm得到的moudule到底是什么</div>2022-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/15/886f5c66.jpg" width="30px"><span>Twittytop</span> 👍（0） 💬（1）<div>提一个建议，不一定是所有人的感受。感觉老师的课程战线拉得很长，后面的内容有很多是对前面内容的详细解释，我个人的感觉是前面有很多地方看得似懂非懂，然后到后面才有豁然开朗的感觉，然后再返回到前面的课程去阅读，就很清晰明了了，但是这样造成的一个问题是有很多同学看前面的没有看懂就放弃了，就会没有效果，所以老师能不能适当的改善一下这种情况。</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（4） 💬（2）<div>wasm和video若能更好的结合，解决播放H265的视频就好了</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c1/05/fd1d47b6.jpg" width="30px"><span>空间</span> 👍（2） 💬（0）<div>目前局限性（不是很确定）：
1. 不能脱离JS环境
2. 和JS的相互调用又不好用，麻烦
3. 虚拟机没有像JS一样访问浏览器功能的诸多接口如DOM, webgl, 定位，传感器，语音... 这些可以作为虚拟机在浏览器上提供的基础库，如果是其他环境（如作为云服务网格的插件）也可以提供不同的基础库</div>2020-10-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLUabUgtOZicYOXBr3LSGrRcXCkMNFn3qWib56Gc7got9XL940BC9SZW3lZlwxowG8RhODcB7C5rHlQ/132" width="30px"><span>大西瓜撒</span> 👍（0） 💬（0）<div>这节很精彩</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/b7/57f153f6.jpg" width="30px"><span>Sun Fei</span> 👍（0） 💬（0）<div>希望 Wasm 的不断发展，会出现更好的客户端跨平台方案。</div>2021-07-18</li><br/>
</ul>