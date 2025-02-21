你好，我是陈天。

上一讲介绍了 FFI 的基本用法，今天我们就趁热打铁来做个实操项目，体验一下如何把 Rust 生态中优秀的库介绍到 Python/Node.js 的社区。

由于社区里已经有 PyO3 和 Neon 这样的工具，我们并不需要处理 Rust 代码兼容 C ABI 的细节，这些工具就可以直接处理。所以，今天会主要撰写 FFI shim 这一层的代码：  
![](https://static001.geekbang.org/resource/image/b2/90/b2578cf89cd55d59f74e48cf6d5bbb90.jpg?wh=2364x1513)

另外，PyO3和Neon的基本操作都是一样的，你会用一个，另一个的使用也就很容易理解了。这一讲我们就以 PyO3 为例。

那么，做个什么库提供给 Python 呢？

思来想去，我觉得 **Python 社区里可以内嵌在程序中的搜索引擎**，目前还是一块短板。我所知道的 [whoosh](https://github.com/mchaput/whoosh) 已经好多年没有更新了，[pylucene](https://lucene.apache.org/pylucene/) 需要在 Python 里运行个 JVM，总是让人有种说不出的不舒服。虽然 Node.js 的 [flexsearch](https://github.com/nextapps-de/flexsearch) 看上去还不错（我没有用过），但整体来说，这两个社区都需要有更强大的搜索引擎。

Rust 下，嵌入式的搜索引擎有 [tantivy](https://github.com/quickwit-inc/tantivy)，我们就使用它来提供搜索引擎的功能。

不过，tanvity 的接口比较复杂，今天的主题也不是学习如何使用一个搜索引擎的接口，所以我做了基于 tanvity 的 crate [xunmi](https://github.com/tyrchen/xunmi)，提供一套非常简单的接口，**今天，我们的目标就是：为这些接口提供对应的 Python 接口，并且让使用起来的感觉和 Python 一致**。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/ea/3d/fe1ab9eb.jpg" width="30px"><span>Marshal SHI</span> 👍（6） 💬（1）<div>之前我在medium上分享过比较PyO3和rust、python速度的文章，大家有兴趣可以看看。在release下PyO3可以提供和rust相似的速度
（不要忘记`--release`） 
文章链接：https:&#47;&#47;link.medium.com&#47;iWSbYCrS3kb</div>2021-11-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（1） 💬（1）<div>准备工作-&gt;&quot;创建 build.rs，并添入：&quot; 中，build.rs 的链接链到哪里了？</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cb/6f/b6693f43.jpg" width="30px"><span>Litt1eQ</span> 👍（0） 💬（2）<div>老师您好，想咨询一下，如果使用pyo3能否有什么比较方便的办法可以在mac上直接编译出来linux win mac可运行的package 现在我用的maturin 如果用借助docker官方给出了可以编译出来Linux可运行的package的方案，但是编译出win可用package我也没发现可用的方案，谢谢了。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（0） 💬（1）<div>作者你好，看到Makefile文件中，有一句mv xxx.dylib yyy.so
百度了下， dylib是macos平台下的，对这个格式不是很了解，看构建脚本，是可以直接将.dylib重命名为.so 文件使用的吗</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/c7/8c2d0a3d.jpg" width="30px"><span>余泽锋</span> 👍（0） 💬（1）<div>平时工作一直用python来做数据处理，老师说的这些对我来说太有用了，使用rust提供一些高性能库给python使用。真是太棒了。</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/bf/d990f851.jpg" width="30px"><span>雪无痕</span> 👍（0） 💬（1）<div>老师能否讲下，在rust下如何开发一个通用的插件框架？</div>2021-11-10</li><br/>
</ul>