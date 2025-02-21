你好，我是于航。

本节课，我们将不再“拘泥”于 Wasm 的实现细节，而是要从技术标准走向生产实践。作为应用篇中的第二节课，我们将一起来看看从 2017 年 Wasm MVP 标准的确定，直到如今 WASI 出现，使得 Wasm 走出 Web 的这几年时间里，现实世界中有哪些已经投入生产的 Wasm 真实案例？而这些案例又是怎样利用 Wasm，解决了哪方面实际问题的呢？（这节课里介绍的几个案例，均由我总结于网络上相关公司发布的文章或视频分享。）

## eBay - Barcode Scanner

第一个我们要介绍的实际案例来自于 eBay 在 Wasm 上的一次尝试。

eBay 是一家知名的线上拍卖与购物网站，人们可以通过 eBay 来在线出售自己的商品。作为一家知名的购物网站，为了优化用户录入待售商品的操作流程，eBay 在自家的 iOS 与 Android 原生应用中提供了“条形码扫描”功能。

通过这个功能，应用可以利用移动设备的摄像头扫描产品的 UPC 条形码，然后在后台数据库中查找是否有已经提交过的类似商品。若存在，则自动填写“商品录入清单”中与该物品相关的一些信息，从而简化用户流程，优化用户体验。

### 问题所在

在 iOS 与 Android 原生应用中，eBay 借助了自研的、使用 C++ 编写的条形码扫描库，来支持 UPC 条形码的扫描功能。而这对于诸如 iOS 与 Android 等 Native 平台来说，条形码的实际扫描性能得到了不错的保障，应用表现良好。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（1）<div>可以总结一下，webassembly 非常适合迁移有其它语言沉淀的类库到 web 平台</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/7a/d7c26cf2.jpg" width="30px"><span>李冬杰</span> 👍（3） 💬（1）<div>老师，c++、c、rust，它们能编译到wasm的前提是什么？随便一个c++项目都可以吗？</div>2020-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKNfFksicibcQH0juiaia16NdasApA9RoqIxA1p8yVU2hjjuYmQakyHmh1gu9bIHDT57atX2GpJobosnw/132" width="30px"><span>huge</span> 👍（2） 💬（1）<div>这个画图的软件是啥</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>目前llvm主流是拿c语言开发。那是不是可以在js或者ts里用wasm来调用llvm来开发</div>2022-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4d/10/5c9bc771.jpg" width="30px"><span>懒懒想睡觉</span> 👍（0） 💬（1）<div>前端的Blazor和WASM是什么关系呢。</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（0） 💬（2）<div>老师，请教一下，wasm可以用来前端加密嘛？我是这样想的，传统的js即使压缩后下载到本地其实也能看懂，但是wasm这种字节码应该看还是比较困难的，是不是可以应用在机密场景？</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（0） 💬（2）<div>我们公司直播页面也是基于wasm的，感觉native和web上主要是编译库，好多特性在wasm不支持。</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>现在国内有哪些知名的团队在使用 WebAssembly 技术， 国内的案例？ 去招聘网站看了一下，几乎没有对应的职位的</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>为什么 js 版本的库居然可以超过 wasm 版本？</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ec/cf/8c1f8d38.jpg" width="30px"><span>xgqfrms</span> 👍（0） 💬（0）<div>@极客时间 音频播放器为什么不支持音量调节呀？</div>2023-02-21</li><br/><li><img src="" width="30px"><span>Geek_b52b68</span> 👍（0） 💬（0）<div>Figma 是不是也使用了 Wasm 做绘图的优化。</div>2021-07-18</li><br/>
</ul>