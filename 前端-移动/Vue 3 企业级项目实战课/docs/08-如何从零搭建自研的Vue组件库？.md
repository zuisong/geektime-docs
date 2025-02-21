你好，我是杨文坚。

回顾我们之前的几节课，讲的都是Vue.js 3.x的入门级操作。从这节课开始，我们将以Vue.js 3.x 组件库的开发为线索，展开Vue.js 3.x企业级项目的进阶学习。

作为一个前端开发者，你肯定对前端组件库并不陌生。相信你在用Vue.js或者React.js开发实际项目时，或多或少都使用过相关开源组件库，例如Vue.js的ElementUI组件库和React的Ant Design组件库。

前端组件库的出现是为了方便我们实现更多的样式和交互效果。毕竟JavaScript + HTML + CSS的原生技术能力比较有限，如果基于原生技术能力来实现网页的样式和交互效果，要付出很大的工作量。而组件库能让前端开发者省去这部分工作量，直接进入页面的功能开发。

Vue.js 3.x 有很多现成的开源组件库，例如Element Plus和Ant Design Vue等都可以直接拿来用。为什么我们还要自己学Vue.js 3.x 的组件库开发呢？

## 自研开发Vue.js 3.x 组件库能带来什么？

**一方面是定制化的需要。**企业产品必定是根据客户或者业务的特色量身定制的，也就是说它有一定的自定义性质，而开源的组件库不一定能满足所有定制化的前端功能。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/27/74828c37.jpg" width="30px"><span>ZR-rd</span> 👍（9） 💬（3）<div>提个建议：这么多文件配置完了但最后怎么用还是不太清楚。建议可以编写一个简单的组件进行示例，然后打包，发布，再在其他项目中引入使用，这样能够更清晰的了解组件库开发的整个流程</div>2022-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（6） 💬（1）<div>按需加载实现方式，
1. 文中提及的方案，手动按需加载。
import { Comp001, Comp002 } from &#39;@my&#47;components&#39;
import &#39;@my&#47;components&#47;css&#47;index.css&#39;

2.社区还有一种方案，利用babel的能力，（babel-plugin-import）
代码的话就是 import { Comp001, Comp002 } from &#39;@my&#47;components&#39;，安装了这个插件，可以不写引入css的文件，但其实本质还是工具帮我们做了引入的事情的事情，将多个文件打包成一个文件。

不过类似全量引入的情况，例如引用elementUi 如果一开始你就直接Vue.use(ElementUi)这样就起不到按需加载的作用了就是全量使用了，所以需要注意.

3.我观察到loadsh关于按需加载的其他方案，例如loadsh.throttle，代码如下：import throttle from loadsh.throttle。看了一下代码，这块应该是开发者二次再上传loadsh.throttle到npm里了，所以这块也增加了维护负担，部署loadsh的时候需要二次部署

坦白的说我，我心目中更友好的是方案3，需要我们上传npm包的时候上传写一段脚本，执行上传子包的地部署方案。最后代码如下，然后开发者使用的时候也是按需加载就可以了
 import Comp001  from &#39;@my&#47;components.Comp001&#39;




</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/1b/6f/ee41e363.jpg" width="30px"><span>海是蓝天的倒影</span> 👍（2） 💬（2）<div>`scripts&#47;build-module.ts`
老师，源码打包编译成ES Module 和 CommonJS 模块两种代码的配置这块，可以详细讲下rollup执行过程吗？理解起来有点吃力</div>2022-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/96/4577c1ef.jpg" width="30px"><span>沉默的话唠</span> 👍（1） 💬（1）<div>到第二步主package.json没贴出来，确实pnpm i 后，啥都没有，直接 Already up-to-date。 

去看了下源代码的package.json 都是配好了的，第二步的时候是什么也不知道是什么。

细节流程呀，任重道远~ </div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/20/9d/791d0f5e.jpg" width="30px"><span>善良的老王</span> 👍（1） 💬（1）<div>我们公司就是按这种方式把elementPlus引入二开 看完这篇文章 再看公司的组件库 感觉豁然开朗 👍</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/56/3bee284c.jpg" width="30px"><span>落叶🍂建良</span> 👍（0） 💬（2）<div>子项目package.json声明, 是需要自己写吗?还是有快捷命令帮忙生成?</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（0） 💬（1）<div>老师还有 side effect 的设置</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/3e/1f/661ac363.jpg" width="30px"><span>Nexus丶</span> 👍（0） 💬（1）<div>三个脚本的import文件来源是哪里，突然冒出来一堆引用文件很迷呀。向类似import { resolvePackagePath } from &#39;.&#47;util&#39;;这个方法是哪来的具体是干嘛用的，有点看不懂</div>2023-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/05/32/791d0f5e.jpg" width="30px"><span>青丘</span> 👍（0） 💬（1）<div>老师，为什么rollup打包的时候设置了 `treeshake: false`。</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5b/34/113c117e.jpg" width="30px"><span>ZH 小小浩</span> 👍（0） 💬（2）<div>提个建议：本来就是冲着学习一下怎么自己从零搭建一个组件库买的这个课程，看完这篇发现写的有点太粗略了，相关的设计、配置文件都直接粘代码，也不讲解下这么多配置分别用来干嘛的...就看的挺迷的。嗯嗯嗯...也可能是自己这方面的知识储备不够</div>2022-12-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/nJHZrATXphhzfqH1OydoOTOZTlj5Qe9fNqauQmsaPrATb5qsibM99lINaTSqicL8qm5vxlibA7jVf7qHcUk7S402A/132" width="30px"><span>Geek_b454df</span> 👍（0） 💬（1）<div>最外层的package.json没有东西， pnpm 报错了</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/e6/7f2c3702.jpg" width="30px"><span>withoutmeat</span> 👍（0） 💬（1）<div>老师, 一般情况下写vue组件, 样式代码都是直接写在了vue文件中, 要怎么满足这个呢？ 另外有个自己的问题，我使用了postcss+tailwindcss， 但是直接使用tailwindcss的api的方式去打包组件这个文档没有找到，有点苦恼～</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/b6/294dafbb.jpg" width="30px"><span>杜子</span> 👍（0） 💬（1）<div>看懵了，要多看几遍才行</div>2022-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rUqhSN2OVg5aHw10Hxib61nGv1SXxD6zowFl27oSm9Y6g8grRpTxCxwk7qg14a1TtmpzMTM2y810MnibBhwn75Mg/132" width="30px"><span>初烬</span> 👍（0） 💬（1）<div>学到很多原来不理解的组件库的知识，感谢老师。</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/4e/39/1dda96a7.jpg" width="30px"><span>早安！午安！晚安！</span> 👍（0） 💬（0）<div>github上拉取的代码执行pnpm i会一直提示@my不是公共库 在 pnpm-workspace.yaml 这个文件里，进行 monorepo 的项目配置这里这样写无作用诶</div>2024-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/ce/495dfc91.jpg" width="30px"><span>行云流水</span> 👍（0） 💬（0）<div>build.dts.ts 打包生成 ts类型文件这个，使用的包比较偏僻，貌似也可以通过 rollup或vite打包vue3组件库生成ts代码？ 为啥选择这个？ </div>2024-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d8/e3/987c9195.jpg" width="30px"><span>Spike Jim.Fun</span> 👍（0） 💬（0）<div>&quot;build:components&quot;: &quot;vite-node .&#47;scripts&#47;build-module.ts&quot;   容易卡死， 怎么排查错误</div>2023-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/b4/0808999d.jpg" width="30px"><span>白马</span> 👍（0） 💬（0）<div>老师你好，关于自研组件这部分内容，如果用vue2的话，是不是方法也是类似的？</div>2023-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/96/4577c1ef.jpg" width="30px"><span>沉默的话唠</span> 👍（0） 💬（0）<div>soory~ 打错目录名...</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（0）<div>给极客时间提个建议：（网页版）把代码块中的滚动条干掉，要不然鼠标在代码块上滚动阅读时，很难受。</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3c/1c/47e5b7aa.jpg" width="30px"><span>Johnson</span> 👍（0） 💬（0）<div>很实用😀</div>2022-12-09</li><br/>
</ul>