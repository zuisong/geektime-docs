你好，我是杨文坚。

上节课我们跳过了官方推荐的Vite，选择了Webpack来搭建Vue.js 3项目，这是因为我们看重Webpack丰富的技术生态，Webpack发展了近10年，沉淀了许多问题处理经验，企业级的应用打包编译方案也相当丰富。

但是，近两年Vue.js官方推出了Vite，很多新项目也开始使用Vite。Vite作为Vue.js 3官方标配的开发工具，代表了官方技术的发展方向，因此作为后续Vue学习和进阶，肯定是不可跳过的一环。

所以这一讲，我们就来尝试一下，如何用Vite来搭建Vue.js 3项目。不过，在开始之前，我还是需要给你简单介绍一下Vite。

## Vite：Vue.js 3的官方标配

首先我们要知道，Vue.js发展到现在，已经不是一个纯粹的前端页面代码库或者框架了，而是一整套技术体系。这里的技术体系是指围绕着Vue.js进行构建的技术生态，包括测试工具Vitest、文档工具VitePress等等。这些工具开箱即用的能力，目前都是基于Vite来进行打造的，这也说明了Vite在整个Vue.js生态中的重要位置。

Vite是Vue.js作者尤雨溪早年基于Rollup做的一个开发工具，核心是为了提高JavaScript项目的开发效率。那么相比同类型的开发工具来说，它的优势在哪呢？
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（1） 💬（1）<div>又双叒叕出新工具了---turbopack---采用Rust编写。自称webpack继任者，热更新比vite快10倍，比webpack快700倍。

尤达发文指出其有选择环境、选择数据之嫌。

不知其未来如何。</div>2022-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（2）<div>文中有一些不严谨的地方，比如npm run build后怎么就可以直接用浏览器访问？</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bf/52/59304c42.jpg" width="30px"><span>默默且听风</span> 👍（3） 💬（0）<div>vite的HTML 中 需要加上 type=&quot;module&quot; 不然会报错。完全体大概长这样 &lt;script type=&quot;module&quot; src=&quot;.&#47;src&#47;index.js&quot;&gt;&lt;&#47;script&gt;</div>2023-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（2） 💬（0）<div>Vite 开发模式下的 esbuild 的按需打包编译，真的是绝对比 Rollup 的 Bundle 打包方式快吗？如果不是，能否推演一下有哪些可能的打包慢场景？

vite核心是利用了esBuild打包（依赖GO） + 基于原生 ESM 按需编译；所以绝大部分场景web场景应该是vite要快于Rollup （毕竟后者是用node打包 + devServer）；
但是并不是所有的打包场景都是web，我认为在一些hybird-native 方案中，vite就不能使用，而传统的rollup基于强大的plugin就能处理。

我也不知道我观点对不对，还请作者解密一下回答一下这个问题。</div>2022-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>从文中的示例代码而言，Rollup的配置并没有比Webpack简单多少，从使用者的角度来说反而是Vite+Webpack的组合来说是一个普适性最好的方案，而且学习成本最低，不知道为啥从来见过这样的组合？如果为了兼容打包速度和学习成本而言，Rspack也是一个不错的选择啊！</div>2025-01-06</li><br/><li><img src="" width="30px"><span>米云鹏</span> 👍（0） 💬（0）<div>新手学习，mac端配置rollup的dev和build后报错，需要把后缀名改成cjs的，配置文件里也是，改了以后会好用，</div>2024-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/7c/51d07eff.jpg" width="30px"><span>李</span> 👍（0） 💬（0）<div>windward 下没有    NODE_ENV 可以安装
npm install cross-env --save-dev
 &quot;dev&quot;: &quot;cross-env NODE_ENV=development rollup -w -c .&#47;rollup.config.js&quot;,</div>2024-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/4b/07/33bc5bbd.jpg" width="30px"><span>文件</span> 👍（0） 💬（0）<div>文中有一处细节作者貌似忽略掉了，在配置完项目目录后需要运行 npm init -y 初始化项目后才能进行后期的安装依赖等操作</div>2024-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bf/52/59304c42.jpg" width="30px"><span>默默且听风</span> 👍（0） 💬（0）<div>因为win环境下没有设置NODE_ENV所以在启动的时候会有遇到“无法访问此网站”诸如此类的提示，可以修改一下Rollup中的设置  (process.env.NODE_ENV === &#39;development&#39; || !process.env.NODE_ENV) ? serve({
      port: 6001,
      contentBase: &#39;dist&#39;
    }) : null 我是这样改的</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3b/b2/f256d634.jpg" width="30px"><span>Samuel</span> 👍（0） 💬（0）<div>vite 能实现webpack模块联邦的功能不？</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/d1/1e8b6e52.jpg" width="30px"><span>avava</span> 👍（0） 💬（3）<div>跑不起来。。npm run dev后无法访问，windows平台，按理说作者不是windows平台开发的，没遇到NODE_DEV不是内部命令这些坑。。</div>2022-11-28</li><br/>
</ul>