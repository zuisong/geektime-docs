你好，我是于航。

相信你在刚刚接触到 WebAssembly 这门技术的时候一定有所发现，WebAssembly 这个单词实际上是由两部分组成，也就是 “Web” 和 “Assembly”。

“Web” 表明了 Wasm 的出身，也就是说它发明并最早应用于 Web 浏览器中， “Assembly” 则表明了 Wasm 的本质，这个词翻译过来的意思是 “汇编”，也就是指代它的 V-ISA 属性。

鉴于 Wasm 所拥有“可移植”、“安全”及“高效”等特性，Wasm 也被逐渐应用在 Web 领域之外的一些其他场景中。今天我们将要讲解的，便是可以用于将 Wasm 应用到 out-of-web 环境中的一项新的标准 —— WASI（WebAssembly System Interface，Wasm 操作系统接口）。通过这项标准，Wasm 将可以直接与操作系统打交道。

在正式讲解 WASI 之前，我们先来学习几个与它息息相关的重要概念。在了解了这些概念之后，相信甚至不用我过多介绍，你也能够感受到 WASI 是什么，以及它是如何与 Wasm 紧密结合的。

## Capability-based Security

第一个我们要讲解的，是一个在“计算机安全”领域中十分重要的概念 —— “Capability-based Security”，翻译过来为“基于能力的安全”。由于业界没有一个相对惯用的中文表达方式，因此我还是保持了原有的英文表达来作为本节的标题，在后面的内容中，我也将直接使用它的英文表达方式，以保证内容的严谨性。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（6） 💬（2）<div>请问老师，那WASI是将系统调用函数在编译期替换成WASI标准函数的吗？还是在运行期通过调用拦截或动态替换的方式？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/59/78042964.jpg" width="30px"><span>Cryhard</span> 👍（5） 💬（1）<div>那这意味着Wasm的编写也需要像原生APP一样，运行中申请一组由WASI“代理”的系统权限的集合（而用户可以提供长期或者单次授权）。而程序也得支持“部分权限被禁用”的情况，例如在“不能调用本地录音设备”的状态下继续正常运行吗？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8f/30/abb7bfe3.jpg" width="30px"><span>欢乐马</span> 👍（1） 💬（2）<div>wasm在浏览器中应该用可以理解 -可以提高性能，但在其他地方应用就是一个全新语言吧？除了发展生态，有实际价值么？没有想清楚</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（1） 💬（1）<div>除了浏览器和node，还有其它可运行WASI的运行环境吗？或者如何自己构建这个运行环境？</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>wasm 可以直接运行在 Chrome 浏览器上 V8 引擎的，不存在系统调用。 那么可以直接使用的 node 环境吗？（node 的引擎也是 v8, 但是有系统调用）  还是要需要 引入  wasi 来重新编译 node 才能使用的？</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e2/f2/081d21b4.jpg" width="30px"><span>The Crusades</span> 👍（0） 💬（1）<div>老师，我理解加一层抽象可以更便于规范和统一，但为什么不能直接规范wasm字节码时对`fopen`这类c函数的实现呢？</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（0） 💬（1）<div>网络的分层算吗？
抽象就是基于事物之上提取出一种规范，只要实现这种规范就可以表示此种事物，那从这个角度而言，编程语言中的 interface 也是一种抽象吗？</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（0） 💬（1）<div>wasi已经是一种标准了吗 我了解的比较出名的支持wasi的运行时有wasmer和wasmtime 他们和wasi的关系是类似于不同浏览器的js引擎和ecma的关系吗 </div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/d8/2bacd9bb.jpg" width="30px"><span>GEEK_jahen</span> 👍（0） 💬（0）<div>TCP&#47;IP 网络模型加了很多抽象层；计算机里面ISA、编程语言、编程框架、业务框架，也是一层层的抽象</div>2022-08-08</li><br/>
</ul>