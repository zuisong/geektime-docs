Trigraphy 是一款图片处理应用。它不同于美图秀秀那种传统意义上的图片应用，没有磨皮或者美白瘦脸之类的效果，而更像是一个艺术工具。它会把照片变得强烈的风格化，加上很多艺术的元素，看起来更像是一个艺术作品。

**Trigraphy 值得分享的产品设计方法和原则共有三点。**

**第一点：利用设计，来管理用户对于进度的认知**

打开 Trigraphy，启动屏上除了Logo之外下面还有三个框，这是占位符。当应用完全打开之后，可以看到这三个格子里面填充了本地的图片。

看起来，结构已预先在启动时完成加载了，第二步才把这些内容加载到结构中，而实际上，启动屏上三个框是画出来的。对于一个 App 来说，点击它的图标打开应用开始加载，在完成加载之前，用户都没有办法参与。加载的过程究竟需要多长时间，用户没办法预期，这个过程对用户来说是失控的。

通过以上的设计，加上一些看起来是加载过程的反馈，这就管理了用户对于加载进度的认知。

举一反三，在所有产品设计的流程里面，我们都要去思考：如何保持对用户的反馈，让用户对系统有掌控感。

**第二点：如何将两个目的不同的页面更顺滑地连接起来**

打开 Trigraphy 之后，界面上有一张大的图片，下面可以看到本地的相册。这个页面的主界面像是一个画板，底下的照片是用户准备处理的素材，好像是用户调色盘一样，这是典型的工具操作页面。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/60/d534e33c.jpg" width="30px"><span>二爷</span> 👍（17） 💬（0）<div>@ 刘祯 作为使用者和作为产品经理看同一个应用的方式是不一样的，可以有侧重，也要总结自己的套路。比如先看信息架构再看核心路径再看交互细节等等。另外有个建议是可以去关注创作者的博客，看看他们自己的介绍，可以切换到服务提供方的视角看。</div>2017-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/60/d534e33c.jpg" width="30px"><span>二爷</span> 👍（41） 💬（0）<div>@ 等108人觉得很赞 推荐的 ui movement 是一个精彩的交互设计聚合社区，上面有很多灵感，大家可以访问 https:&#47;&#47;uimovement.com</div>2017-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/cb/a699ab95.jpg" width="30px"><span>吉吉</span> 👍（3） 💬（1）<div>感谢二爷的分享，作为一个希望从外企IT转型做产品的人来说收获良多，也感谢其他订阅者的留言，也会启发我的一些思考。有两点特别想分享：
1.占位符的作用除了管理用户对加载进度的反馈，由于提前告知用户一部分页面内容（结构布局），的确会产生一种加载速度十分迅速的感觉；
2.关于二爷说色子的随机功能能帮助区分不同层级的作用，一开始对于“层级”二字感觉很奇怪，以为是区分不同“类型”的用户，但看过评论后再细思，才品味了色子的奥秘。作为一个手机摄影爱好者，各种修图软件也尝试很多，所以一般都喜欢自己调控参数，但身边许多人认为这样使用成本过高，学习成本也高，耗时耗力，而Trigraphy这个色子功能的确能帮助用户逐步递进。但同样的，这对于软件自身的图片处理算法可能要求也比较高，我尝试了一下，色子处理的图片效果，直接能够接受的有限，对于一些对比强烈，主角突出的图片处理效果更佳。
</div>2018-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/bb/02d02a51.jpg" width="30px"><span>等108人觉得很赞</span> 👍（24） 💬（0）<div>关于交互可以看看「UI Movement」，非常赞</div>2017-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/bf/5c5e86bb.jpg" width="30px"><span>旺旺</span> 👍（15） 💬（0）<div>1、避免加载时的时空感，6秒原则（预加载中间态图片，Facebook的3个中间态）；
2、页面之间平滑过渡（Tri上下滑动过渡，微信朋友圈广告展开）；
3、不同级别的用户，不同的交互入口（交互冗余，满足不同层次或场景下的需求）
例：王者荣耀，quick start。</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8b/38b93ca0.jpg" width="30px"><span>听天由己</span> 👍（14） 💬（0）<div>首先，感谢二爷分享的三点启示，产品设计真的是一门艺术，有时我也忍不住惊叹于他们的奇思妙想，可是真的要自己去应用或是实践，却总是限于个人能力与技术资源，这一方面还有很长的路要走。

应用举例：Medium  网站中文章图片的模糊加载，时间块中通过滑动将事件记录半屏与全屏呈现巧妙结合。

其次，视频分享特别棒，我们能够直观体验并且随着说明深入了解，我还发现了讲解视频将极客时间的 Logo 完美融入，右上角的水印、相册中的极客时间的 Logo、视频开头与结尾的产品曝光，在细节上的设计真的要不停去思考与应用。

最后，我一直有个疑问：即便是手机中的常用产品，我们也无法了解或是掌握它的全部功能或是细节，而产品不断迭代更新，我们可能总是处于未知状态，产品设计者也罢、狂热爱好者也罢、普通用户也罢，大部分人都要看攻略、看教程、看视频等，因为通过自己的摸索远远不够，我们应当如何面对这样的窘境呢？</div>2017-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/cf/5cbccd62.jpg" width="30px"><span>ibrothergang</span> 👍（10） 💬（1）<div>我是一个软件开发者，今天刚刚订阅了二爷的专栏，希望能够培养自己的一些产品思维，融入到自己的开发过程一中。</div>2017-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/de/1ae1a14f.jpg" width="30px"><span>棒冰</span> 👍（6） 💬（0）<div>第一点其实是苹果设计原则中推荐的，就像很多苹果自带应用，启动页就是一个标题栏加空白页，结果就是给用户感觉是秒开。</div>2017-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/fa/1f5bf642.jpg" width="30px"><span>未来的胡先森</span> 👍（3） 💬（0）<div>产品的学习成本越低，纳新成本也会降低。</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/2d/95/f2ddbe0f.jpg" width="30px"><span>0075</span> 👍（2） 💬（0）<div>感觉有点明白了，做产品需要先分许抓住用户的心理</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/7e/c38ac02f.jpg" width="30px"><span>北冥Master</span> 👍（1） 💬（0）<div>留言中提到的信息架构具体指什么？</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/53/32/0dbc71f1.jpg" width="30px"><span>yaya</span> 👍（1） 💬（0）<div>感谢二爷的分享，我刚接触产品，订阅了您的专栏，很受启发，现在看app的角度已经不再是用户，而是向产品经理方向靠了，懂得去分析一个app的交互，为什么这么做了，继续向您学习，继续深入，加油。</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/42/76eb78bd.jpg" width="30px"><span>hunknownz</span> 👍（1） 💬（0）<div>细节</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/ee/8451dfc4.jpg" width="30px"><span>Dylan</span> 👍（1） 💬（0）<div>功能流程确定后，在前端上如何通过设计，有效链接页面，不触发用户的潜意识抵触，“丝滑过度”，也是门艺术。毫无疑问最近微信的文章浮窗就是这样的设计，用户右滑返回上一级页面悬停，出现浮窗选项，此时用户顺势滑到右下角浮窗区域，浮窗动画效果还会表明是否已到达该区域，到达就松开即可。
此外，降低用户使用成本也是个必要思考，通过新手任务是个方法，通过确定性点击-随机性奖励也是个方法，要看你负责的业务是什么形态。</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/c2/17/97ba2087.jpg" width="30px"><span>77</span> 👍（0） 💬（0）<div>提问：交互效果是需要产品经理考虑的吗？那交互设计师的发挥空间呢？</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f6/d3/d78815c6.jpg" width="30px"><span>关尔</span> 👍（0） 💬（0）<div>希望可以试用一下clubhouse</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>我们现在做Kubernetes 的体验也是用了类似的想法，首先用户手写spec 太复杂了，所以会通过templates 有向导通过填写一些最简单的参数帮助用户开始；然后因为集群过多，我们通过构建index 服务降低用户在不同对象之间navigation 的成本并加快浏览速度，RBAC 权限管理不应该是一个单独的页面而是对每一个对象都应该一键到达RBAC 权限管理。</div>2020-12-06</li><br/><li><img src="" width="30px"><span>0057</span> 👍（0） 💬（0）<div>可以</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/56/252208bb.jpg" width="30px"><span>阚雪娇</span> 👍（0） 💬（1）<div>在需要的阶段，产品设计应该更多的关注功能细节，产品的精致之处就来源于这些细小的交互体验</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（0） 💬（0）<div>优雅的等待设计，增加用户可控性，减少失控感
合理设计页面的链接，通过动效增加效果
</div>2019-10-17</li><br/><li><img src="" width="30px"><span>13761642169</span> 👍（0） 💬（0）<div>这么好的产品经理，智商高情商高心眼也不坏，羡慕</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/82/749a3609.jpg" width="30px"><span>何田田</span> 👍（0） 💬（0）<div>网上比较多的是硬件外设的测评，ZEALER等
当然也有APP的使用推荐，少数派等
产品经理测试软件的交互设计，应该是二爷等吧</div>2018-12-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIqNNJJc9yicL0yR9egm8q0ro8BSiacMFXpXoKUl2mSKqAvhojHHa4o9v4jYnsDtcqibIH6z2B6uQIjw/132" width="30px"><span>Grace</span> 👍（0） 💬（0）<div>感谢二爷的分享！曾经是工程师刚转战到产品经理的小白，在产品方面还有很多的不解和困惑，由于目前公司的产品团队只有三个人，业务比较多，感觉自己磨练的机会很多，但是却没有mentor经常指导，很多事情都得自己摸索，有时候还是挺痛苦的😭
另外想问二爷，是如何培养自己去发现生活中的好的产品设计的呢？例如朋友圈的广告的交互设计，为什么我从来没有留意到？这是产品经理本身自带的特质还是有意为之？</div>2018-03-11</li><br/>
</ul>