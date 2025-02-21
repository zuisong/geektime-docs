上周六，我详细介绍了[HTML5技术相比Flash技术的优势](https://time.geekbang.org/column/article/9298)，相信你已经对HTML5技术有一个大致的了解。下周六，我会带你编写一个HTML5游戏，在这之前，我们需要先了解几种常见的HTML5游戏引擎。

一些比较成熟的引擎，比如Cocos2d-JS、白鹭等，它们都提供有系列化的工具，比如编辑器、IDE等周边。但是其实**大部分HTML5游戏引擎都只有图形引擎**而已，比如legend.js。而且很多HTML5引擎只是个人编写的开源引擎，所以漏洞还是比较多的。

HTML5游戏引擎在编写的时候，除非用DOM（Document Object Model）纯原生编写，绝大部分都是使用JavaScript编写的。但是为了考虑各种程序员的需求，现在也有使用TypeScript、CoffeeScript、LiveScript等语言编写的HTML5引擎。

## 几款常见的HTML5游戏引擎

我们现在来看一下几款常见的HTML5游戏引擎。

### Construct 2

这是一款收费的引擎，当然也有免费的版本，但是免费的版本不可用于商业用途。那么既然是商用引擎，那它一定会比免费开源的产品更加完善和易用。这里有一幅Construct 2的截图，你可以看一下它的界面。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/61/ac/e6b58c18.jpg" width="30px"><span>chen</span> 👍（6） 💬（1）<div>资源从网络上加载</div>2018-06-23</li><br/><li><img src="" width="30px"><span>Geek_2yt3sd</span> 👍（4） 💬（1）<div>白鹭，cocos都快凉了，目前国内稍微好一些的是laya了</div>2018-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/dc/5214bdf7.jpg" width="30px"><span>叶Da</span> 👍（0） 💬（1）<div>cocos creator不谈论吗</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/9e/4bb83b4e.jpg" width="30px"><span>💦 Peter Pan</span> 👍（2） 💬（0）<div>LayaAir引擎怎么样</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/59/989f65c8.jpg" width="30px"><span>jacky</span> 👍（1） 💬（0）<div>请问有可以用做gis引擎吗？</div>2020-05-12</li><br/><li><img src="" width="30px"><span>三硝基甲苯</span> 👍（1） 💬（0）<div>那些图形材质，声音文件可以选择需要时再从网络下载到本地   本地的缓存好像可以到10M，每次加载的时候 都先清除不需要的。</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>资源动态加载</div>2024-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/ec/337077d5.jpg" width="30px"><span>神马*涛💋</span> 👍（0） 💬（0）<div>这个课程初的时候。CocosCreator应该还没诞生！</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/d8/3326d7c0.jpg" width="30px"><span>LFR</span> 👍（0） 💬（0）<div>实时从远程按需加载</div>2018-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/25/eaa3132e.jpg" width="30px"><span>小宝儿</span> 👍（0） 💬（0）<div>只留下最基本加载，其余的包括图片，声音和脚本全部下载</div>2018-07-02</li><br/>
</ul>