> 本文由编辑整理自宋一玮老师在极客时间直播中的演讲《前端工程化的最佳实践与演进》，详细视频请在b站搜索观看，或直接点击[链接](https://www.bilibili.com/video/BV1Va411G7Wc/?spm_id_from=333.337.search-card.all.click&vd_source=9a6de1dbe4831e63618355e534516ee4)观看。以及，PPT获取地址[在这里](https://pan.baidu.com/s/1Qz-rT_3kJJ-p9zd1RC0F8A?pwd=63U8)，提取码为：63U8。

上节课我们通过软件开发生命周期，了解了前端开发为什么工程化，那么这节课，我就来相应地介绍一些我所亲身经历的前端工程化的最佳实践，希望能对你有所启发。

FreeWheel是我供职的公司，我们主要是一个视频广告平台，面向的是欧美客户，产品包括视频广告管理平台（这是一套非常复杂的UI）、Ad Serving、报表、预测。

从2014年开始，FreeWheel在前端架构层面就开始做一些与工程化相关的改进，所做的工作量很大，所以我会侧重介绍其中2-3个点，说明当时的痛点是什么，以及我们做工程化改进的初衷是什么。

## FreeWheel前端工程化的演进

在2014年时我们就已经开始做一些前后端分离的工作，引入React，并且开始做资源组件库了。因为当时整个应用非常复杂，有300多万行的代码（非常恐怖的代码量），这在当时来说算是比较有远见的一个举措了。

![](https://static001.geekbang.org/resource/image/2d/78/2ded43473122efce64679c2d304f0478.jpg?wh=2284x1225)

开始做自研组件库，一是市面上没有太多成型的组件库，另一个是我们这个行业，以及行业的这些用户也有一些特别的需求，所以我们当时用了一个构建工具，叫Browserify（如今已经退出历史舞台）。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/21/8c/e7241683.jpg" width="30px"><span>墨白™</span> 👍（6） 💬（1）<div>做过微前端+BFF，两者做完的感受就是，技术不是最难的，最难的是想清楚这些技术引入能不能为当前业务有一些增益部分。</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（2） 💬（1）<div>老师您觉得微前端具体解决什么问题呢？ 是应该奔着使用微前端为前提来开发应用， 还是从前期通过更好的约定或者工程来解决呢</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/f0/5d52d73e.jpg" width="30px"><span>Jy</span> 👍（0） 💬（1）<div>我认为微前端最大的优势是能解决不同组织带来的协作成本。如果说引用了微前端，没有带来分工上的优势，那么就要跟引入的成本权衡下了。</div>2023-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnRUibp7LV1l6RA5E8BcLjwLIaOoQxyicM3iaZXcPrJPdMkGmvFHWxBV6sbib7FQK6YMaOdKo6oiaBRaA/132" width="30px"><span>InfoQ_3906e8b6c95f</span> 👍（3） 💬（0）<div>现在web工程的复杂度已经和App工程有得一拼了</div>2022-10-23</li><br/>
</ul>