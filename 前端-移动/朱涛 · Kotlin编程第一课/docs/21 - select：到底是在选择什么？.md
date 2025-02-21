你好，我是朱涛。今天我们来学习Kotlin协程的select。

select，在目前的Kotlin 1.6当中，仍然是一个**实验性的特性**（Experimental）。但是，考虑到select具有较强的实用性，我决定还是来给你介绍一下它。

select可以说是软件架构当中非常重要的一个组件，在很多业务场景下，select与Deferred、Channel结合以后，在大大提升程序的响应速度的同时，还可以提高程序的灵活性、扩展性。

今天这节课，我会从select的**使用角度**着手，带你理解select的核心使用场景，之后也会通过源码帮你进一步分析select API的底层规律。学完这节课以后，你完全可以将select应用到自己的工作当中去。

好，接下来，我们就一起来学习select吧！

## select就是选择“更快的结果”

由于select的工作机制比较抽象，我们先来假设一个场景，看看select适用于什么样的场景。

客户端，想要查询一个商品的详情。目前有两个服务：缓存服务，速度快但信息可能是旧的；网络服务，速度慢但信息一定是最新的。

![](https://static001.geekbang.org/resource/image/50/86/50f7c90d8a01e42834500bb5yy705486.jpg?wh=1576x707)

对于这个场景，如果让我们来实现其中的逻辑的话，我们非常轻松地就能实现类似这样的代码逻辑：
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（3） 💬（3）<div>作为一个 Android 开发同学，我感觉协程没 Kotlin 基础语法香。
因为在 Android 中，异步任务没那么多，也没什么嵌套，只要稍加封装，用起来也没那么痛。
所以协程没想象中的那么实用。</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（3） 💬（1）<div>所有的 onXX 都是回调
所有的异步都会用到回调</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/4b/95812b15.jpg" width="30px"><span>抱紧我的小鲤鱼</span> 👍（2） 💬（1）<div>不是很理解select的应用场景</div>2022-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（1） 💬（1）<div>配合Channel使用感觉变复杂了</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ef/c0/537b3905.jpg" width="30px"><span>L先生</span> 👍（1） 💬（2）<div>是不是类似于callback，包了一层，返回出去。内部可能每个包个async，然后谁先出数据就callback出去</div>2022-03-07</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>请问老师，是不是flow因为有了combine等操作符就不需要select了?</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（0） 💬（1）<div>onXXX 表示回调的多，另外也可以表示会自动执行的方法（看个人习惯）。
感觉源代码难读，大概读了一下，发现有个注册回调的地方，当回调执行时，会判断一下 isSelected，如 select 已选择，则后续的就不走了。不知道对不对</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（0） 💬（1）<div>是不是利用了onComplete和onStart进行计时，然后返回最快的一个？</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/a6/679b3c6b.jpg" width="30px"><span>Renext</span> 👍（0） 💬（1）<div>学习了</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/6d/f2354440.jpg" width="30px"><span>瞌睡的李先生</span> 👍（2） 💬（0）<div>学过go语言的同学会感觉到这一篇真的特别好理解。学到现在感觉kotlin的协程有种集百家之长的感觉，对于多种语言背景的同学都可以方便地学习上手。</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/71/ab/b19a1ba2.jpg" width="30px"><span>BUG君</span> 👍（1） 💬（0）<div>看到有小伙伴留言说不是很好理解，其实还是基础知识的问题，建议先去补补java得IO模型的基础知识，再回过头来看会更好理解一些</div>2023-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>看起来很像回调，问题是回调里怎么可以定义函数</div>2023-11-12</li><br/>
</ul>