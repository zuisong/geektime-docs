你好，我是大圣，欢迎进入课程导读篇的第四讲。

在上一讲，我带你了解了Vue 3 的新特性。对于Vue 3 相比于 Vue 2 有哪些优势这个问题，相信你已经了解得很清楚了。那么在这一讲，我来教你如何把Vue 2 的项目升级到Vue 3。

把Vue 2 的项目升级到Vue 3，也是小圣一直关心的问题，今天早晨小圣还问我，既然Vue 3 如此优秀，是不是应该赶紧把项目都升级到Vue 3？

首先不要着急，并不是所有项目都适合升级。就像苹果出了新款手机，哪怕新特性被人们说得天花乱坠，但是，是不是把老手机换掉，也需要斟酌，毕竟升级总是需要成本的。

## 应不应该从Vue 2 升级到Vue 3

应不应该升级？这个问题不能一概而论。

首先，如果你要开启一个新项目，那直接使用Vue 3 是最佳选择。后面课程里，我也会带你使用Vue 3 的新特性和新语法开发一个项目。

以前我独立使用Vue 2 开发应用的时候，不管我怎么去组织代码，我总是无法避免在data、template、methods中上下反复横跳，这种弊端在项目规模上来之后会更加明显。而且由于vue-cli是基于Webpack开发的，当项目规模上来后，每执行一下，调试环境就要1分钟时间，这也是大部分复杂项目的痛点之一。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（25） 💬（5）<div>谢谢大圣老师的讲解，我还有一个小的疑惑，我们通常创建Vue应用，一个实例（new Vue({})）就能满足我们的使用场景了，而且也认为应该只存在一个。但是在课程里老师说（Vue2和Vue3启动不同）：有一个页面的多个应用的情况。所以想了解下，什么情况下会遇到这种场景呢？这个问题不是这节课的主题，但是还是很好奇，谢谢大圣老师解惑。</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/2f/f4adcb41.jpg" width="30px"><span>。。。</span> 👍（15） 💬（3）<div>有几个问题需求请教下：
1. Tree-shaking 清理代码 什么意思，什么时候用
2. 到底什么是  Composotion api ，vue 2 的是  Options api?
3.  vue3 周边，或者说是 vue 全家桶都包括哪些vue技术
4. AST 是什么，全称是什么
5. 虚拟 DOM 是什么，怎么理解
</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（13） 💬（1）<div>全面拥抱Vue 3会有更好的待遇，敲敲黑板，重点😎</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/83/f81e4403.jpg" width="30px"><span>码农初上路</span> 👍（12） 💬（1）<div>大圣好，vue2.7最低也能支持到IE9吗？</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（7） 💬（3）<div>讲的很细，很赞👍🏻，有个小需求，希望大圣老师加上推荐阅读这样类似的章节。</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（5） 💬（1）<div>打卡
目前部门的老项目用的@compositon&#47;api包使用vue3的composition api来重构和优化，新项目直接使用vue3来开发
开阔眼界了，使用ast语法编译来转换vue2代码，真是一劳永逸！</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/79/c5cfe88c.jpg" width="30px"><span>淡若清风过</span> 👍（4） 💬（1）<div>拐了，还以为已经录制好的视频拿来卖，看来是到明年都更新不完</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/e5/b6980a7a.jpg" width="30px"><span>无双</span> 👍（4） 💬（1）<div>麻烦问一下，在哪有vue2的支持周期？</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（3） 💬（1）<div>讲得很全面了，就是不太理解下面这段里，一个全局组件，有多个Vue实例，不就是全局组件吗，这里的“造成混淆”是指什么？
“我们在 Vue 上先注册了一个组件 el-counter，然后创建了两个 Vue 的实例。这两个实例都自动都拥有了 el-couter 这个组件，但这样做很容易造成混淆。”
```
Vue.component(&#39;el-counter&#39;,...)
new Vue({el:&#39;#app1&#39;})
new Vue({el:&#39;#app2&#39;})
```</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/14/94/fabb99cd.jpg" width="30px"><span>球球</span> 👍（3） 💬（3）<div>vue2升级成vue3 对应用到的element ui 也要升级是吗</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4c/3c/028dc8b1.jpg" width="30px"><span>Shane灬7</span> 👍（1） 💬（1）<div>先给大圣老师点赞，发现一个问题，“是否使用 Vue 3”那张图中的“是否要长期维护”的“是”和“否”的位置是不是反了？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fc/7b/791d0f5e.jpg" width="30px"><span>徐三宝</span> 👍（1） 💬（1）<div>老师您好，
我们在Vue2升级Vue3时遇到了一些问题，请指点～
1，Vue2项目中，我们会把一些数据绑定到Vue上，比如Vue.$reqList存放了请求中的异步请求，然后在axios.js的拦截器中去监听和处理，但是在Vue3中变更成了app.config.globalProperties.$reqList，但是却无法在普通的js文件中（比如axios.js）中拿到这个值。
</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/bb/9cf1266c.jpg" width="30px"><span>hyangteng</span> 👍（1） 💬（1）<div>请问下：vue2使用composition-api，涉及到vuex的如何处理 

例如：
如何获取vuex中的状态
 如何提交mutation和action</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/94/afd0919c.jpg" width="30px"><span>起風了</span> 👍（1） 💬（2）<div>老师好,手头上有个项目,是基于vue2的ant design pro vue来迭代的,还使用了一些其他例如表格组件库等,都是vue2的. 如果要升级vue3的话,使用@vue&#47;compat的同时,其他的那些插件或组件库也要升级vue3版本对应的?如果其他插件或组件库没有vue3版本的是不是升级就比较困难或者不可行了?</div>2021-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK95MP7iatc1WcDdusl6mWibiaGXQebI2WFbfTjANfH2eaQX07u7nTnQ6JGOaYKibXYOjPwXDT2FBhUXg/132" width="30px"><span>Geek_614299</span> 👍（0） 💬（1）<div>升级！绝不惯着ie(11)</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/4e/51896855.jpg" width="30px"><span>落风</span> 👍（0） 💬（1）<div>vue2 开发公用逻辑时候的各种mixins，足够让人头大</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/06/97/fe937d40.jpg" width="30px"><span>人生如戏</span> 👍（0） 💬（1）<div>vue2.7 Composition API、vue2原来语法可以同时混用吗？因为有个项目大部分模块我在做，但有一个模块分给其他同事了，我个人想用 Composition API</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/fe/55/de39267a.jpg" width="30px"><span>速冻鱼</span> 👍（0） 💬（1）<div>虽然公司一直在使用vue3，但还是能学到很多，蟹蟹大圣老师</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4a/75/51435f4b.jpg" width="30px"><span>@</span> 👍（0） 💬（1）<div>我们的项目也需要升级了</div>2021-10-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erDeOuPaaRAgWLLIdarW4RI2xrgdDkaPVLNuyba5kVFtCrqOialpOjkCgqZyOfxfxXJKd8a6jDI98g/132" width="30px"><span>Mserke</span> 👍（2） 💬（0）<div>思考题：有需要升级的地方，项目越来越大了，要拆分成微服务</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a1/89/3c865bd0.jpg" width="30px"><span>T1M</span> 👍（1） 💬（1）<div>打个卡----我用的ruoyi框架，准备尝试把前端升级到vue3。</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/c9/5decc0a3.jpg" width="30px"><span>章剑</span> 👍（1） 💬（2）<div>大圣老师，我最近也在升级vue3中，总体来说compositionApi 还是比较舒服的， 但是mixin有个特性，就是引入页的同名方法可以替换mixin 的方法，在之前的vue 2框架里，这个特性能让部分逻辑更容易修改，打个比方，有一套表单提交的mixin ，其中有个逻辑是提交完表单后重置表单，正常就是调用自定义的resetform 方法，如果需要有特殊操作的话，直接在引入页重新定义一个同名方法重写这个逻辑就可以了。但是在vue3 中我就不知道怎么比较好的处理这种情况了。还请指点下</div>2021-11-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLL5KuxVibyxbVwuPaOXN3YQLEBTlb22cV05M3P8DFGpQxFOTNBMLHRYfPHwS9UsQyUicAo92FketrA/132" width="30px"><span>InfoQ_cd01f1df2496</span> 👍（0） 💬（0）<div>这讲内容我最大的收获是vue2升级vue3，可以使用@vue&#47;compat帮助我们更好的升级，因为它能把所有vue2相关的升级信息提示出来；再来就是可以使用gogocode帮助我们自动化的完成vue2到vue3的升级</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4b/98/20ff3f6a.jpg" width="30px"><span>这个需求做不了</span> 👍（0） 💬（0）<div>老师你的element3 官方文档呢？</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/b0/d32c895d.jpg" width="30px"><span>熊能</span> 👍（0） 💬（1）<div>vue2.7能支持IE6么？</div>2022-01-23</li><br/><li><img src="" width="30px"><span>请去学习吧</span> 👍（0） 💬（0）<div>离开舒适圈，体验新框架，打卡学习Vue 3</div>2021-10-28</li><br/><li><img src="" width="30px"><span>Geek_525762</span> 👍（0） 💬（0）<div>更新的很慢啊！</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f5/b4/0facc7f3.jpg" width="30px"><span>Aybuai</span> 👍（0） 💬（0）<div>就我目前的项目来说有两点需要
1、Composition API 组合语法，项目过于庞大，有的页面上千行。维护起来特别麻烦。
2、自定义渲染器，随着项目的外推，可能不单单公司内部使用，可能会出现各种多端支持。</div>2021-10-25</li><br/>
</ul>