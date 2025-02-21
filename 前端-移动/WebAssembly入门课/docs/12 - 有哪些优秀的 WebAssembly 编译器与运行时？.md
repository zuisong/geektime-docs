你好，我是于航。

本节课我们来一起看看，目前业界有哪些优秀的 Wasm 运行时。这些运行时都是 Wasm 可以在 out-of-web 领域大显身手的最基本保障。它们其中有些支持 WASI 抽象系统接口，有些支持 Wasm Post-MVP 标准中的部分提案，还有一些可以被专门用在诸如嵌入式、IOT 物联网以及甚至云，AI 和区块链等特殊的领域和场景中。

不仅如此，还有一些更具创新性的尝试，比如 “Wasm 包管理”。这一概念类比 npm 之于 JavaScript，PyPi 之于 Python，crates.io 之于 Rust，相信这一定可以为 Wasm 生态添砖加瓦。

这一切，我们都要先从“字节码联盟”这个特殊的组织开始说起。

## 字节码联盟（Bytecode Alliance）

“字节码联盟”成立于2019年末，是一个由个人和公司组成的团体。最初的一批创始成员为 Mozilla、Fastly、Intel 以及 Red Hat。联盟旨在通过协作的方式，来共同实现 Wasm 及 WASI 相关标准，并通过提出新标准的方式来共同打造 Wasm 在浏览器之外的未来。

对于开发者来说，联盟希望能够为开发者提供健全的、基于各类安全策略构建的成熟开发工具链（虚拟机、编译器以及底层库）生态。这样开发者便可以将目光更多地专注于应用本身的设计与研发上，同时可以在各类环境中，快速地构建可运行在浏览器之外的 Wasm 应用，并且不用考虑安全性等基本问题。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（8） 💬（1）<div>老师请教个问题哈，如果想开发一款自己的wasm运行时，大体思路是什么样的，有没有推荐的学习路径呀？</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/55/c5/7b0278df.jpg" width="30px"><span>Xi</span> 👍（1） 💬（1）<div>于老师，simd优化有那些学习资料可以推荐</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/aa/f6/9eafc261.jpg" width="30px"><span>陶雅阁</span> 👍（0） 💬（1）<div>老师请教一下，不同的语言被编译到wasm所对应的二进制字节码是否会有区别呢，或者说是优化程度的不同
另外像go语言运行时的垃圾回收是怎么处理的呢</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（0） 💬（1）<div>老师看到这，有一种all in wasm，感觉最后都是wasm都没问题的感觉。</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cb/91/14398631.jpg" width="30px"><span>王超</span> 👍（0） 💬（1）<div>lucet和wasmtime合并了</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>字节码联盟是不是自家开发自家的wasn’t运行时，然后以后再外力的作用下，再一起选出来一个事实的标准？</div>2020-09-30</li><br/><li><img src="" width="30px"><span>201201132</span> 👍（1） 💬（0）<div>SSVM更名成WasmEdge了</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（0） 💬（2）<div>老师，请教一下，wasm可以用来前端加密嘛？我是这样想的，传统的js即使压缩后下载到本地其实也能看懂，但是wasm这种字节码应该看还是比较困难的，是不是可以应用在机密场景？</div>2020-10-29</li><br/>
</ul>