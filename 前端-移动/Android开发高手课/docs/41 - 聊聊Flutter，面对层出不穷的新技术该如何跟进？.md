“天下苦秦久矣”，不管是H5、React Native，还是过去两年火热的小程序，这些跨平台方案在性能和稳定性上总让我们诟病不已。最明显的例子是React Native已经发布几年了，却一直还处在Beta阶段。

Flutter作为今年最火热的移动开发新技术，从我们首次看到Beta测试版，到2018年12月的1.0正式版，总共才经过了9个多月。Flutter在保持原生性能的前提下实现了跨平台开发，而且更是成为Google下一代操作系统Fuchsia的UI框架，为移动技术的未来发展提供了非常大的想象空间。

高性能、跨平台，而且更是作为Google下一个操作系统的重要部分，Flutter已经有这么多光环加身，那我们是否应该立刻投身这个浪潮之中呢？新的技术、新的框架每一年都在不断涌现，我们又应该如何跟进呢？

## Flutter的前世今生

大部分所谓的“新技术”最终都会被遗忘在历史的长河中，面对新技术，我们首先需要持怀疑态度，在决定是否跟进之前，你需要了解它的方方面面。下面我们就一起来看看Flutter的前世今生。

Flutter的早期开发者Eric Seidel曾经参加过一个访谈[What is Flutter](https://www.youtube.com/watch?v=h7HOt3Jb1Ts)，在这个访谈中他谈到了当初为什么开发Flutter，以及Flutter的一些设计原则和方向。  
﻿﻿  
![](https://static001.geekbang.org/resource/image/ac/5c/aca58328ba1b4f1463d1b2b806c5ad5c.png?wh=1920%2A1061)
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/a9/e251ace7.jpg" width="30px"><span>张绍文</span> 👍（22） 💬（0）<div>字节跳动客户端基础技术负责人元硕招聘啦，有兴趣的高手们可以尝试一下，

字节跳动(今日头条)客户端，邮箱: zhuyuanshuo@bytedance.com</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/92/f3dabcb1.jpg" width="30px"><span>小小代码</span> 👍（2） 💬（2）<div>最近也在学习Flutter，对没有像Android一样，将UI布局写成单独的XML文件，做到UI和逻辑的分离，用的很不爽</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/48/83/d19078dc.jpg" width="30px"><span>明妃</span> 👍（1） 💬（1）<div>张老师，从一年前购买您的专栏这么久了第一次评论，现在我有个很大的疑惑，我的目标始终是偏底层，可是现实中我却必须会一个跨平台开发的技术，帮助我更好的适应未来的潮流(因为我底层至今不知道如何入门)。最近我一直在纠结选择flutter还是rn，张老师能给点意见吗？谢谢您</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/ef/70bfc099.jpg" width="30px"><span>less</span> 👍（0） 💬（1）<div>多说无益.实践至上.跟邵文老师学习到现在.不仅获得了很多实实在在的干货.而且开了很多眼界.继续努力.向邵文老师学习.加油加油送给自己</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/e2/c21553c4.jpg" width="30px"><span>HYM</span> 👍（0） 💬（1）<div>说说自己在实践中碰到的几个问题：
1、官方推出的混合开发方案侵入性较强，业内偏爱闲鱼的方案，但是要有hack精神、肯折腾。
2、对iOS的支持真心差，Flutter Engine的初始化和ViewController的创建有冲突，而且还有很多内存泄漏问题
3、图片加载问题比较多，除了文中提到的没有磁盘缓存外，还有就是内存缓存回收不及时导致内存占用很高，在iOS平台上问题尤为严重。
4、很多需要访问底层接口的功能仍然要借助插件来完成，这块会多很多工作量。

</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/51/9073faa5.jpg" width="30px"><span>seven</span> 👍（0） 💬（1）<div>期待很久的文章！对于要不要学 flutter，多想无益，干就是了</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（2） 💬（1）<div>目前实现了三端Android，iOS，Flutter工程独立，开发Flutter的小伙伴切换为源码依赖，其他小伙伴切换为AAR，Framework依赖。打包脚本把iOS对Flutter的依赖产物放到CDN，脚本会自动扫描依赖的插件，打包业务Bundle到CDN，实现两端的自由开发。</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（0）<div>实践至上。项目组已经开始着手Flutter了，开干就完事</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/52/97/8f960ce9.jpg" width="30px"><span>xx鼠</span> 👍（0） 💬（0）<div>我也在做出海应用，考虑接入RN，有什么建议？谢谢</div>2023-02-09</li><br/><li><img src="" width="30px"><span>文培定</span> 👍（0） 💬（0）<div>为啥我用Flutter开发的app，启动速度明显比原生的慢，白屏时间很明显。而且发现gongle在android中另外开发了一套compose UI，在内容上跟Flutter非常近似，感觉是Flutter要被抛弃了？</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/46/43/7545067a.jpg" width="30px"><span>秋水无痕</span> 👍（0） 💬（0）<div>没必要追新，那样很被动也很累感觉</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/46/df595e4a.jpg" width="30px"><span>CatTalk</span> 👍（0） 💬（0）<div>去年在团队引入，实现了结合当前插件加载框架，实现以插件的形式加载起来。实现了一个完整的Flutter业务插件。但苦于人力支持不足，灰度测试阶段，一直没上线...</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/46/5e/c0ea1ffb.jpg" width="30px"><span>留白</span> 👍（0） 💬（0）<div>跟大佬们简单对比一下就深刻的认识到了自己的不足，接触flutter两个月时间，对其认知还是不够深入，得加把劲了</div>2019-04-11</li><br/>
</ul>