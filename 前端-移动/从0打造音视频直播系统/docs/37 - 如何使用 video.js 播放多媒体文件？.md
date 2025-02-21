在上一篇文章中，我们介绍了 flv.js 播放器。那今天我们再来介绍另一款非常有名的 JavaScript 播放器——video.js。

我们首先来比较一下这两款播放器，看看它们之间有什么不同？在我看来，flv.js 更聚焦在多媒体格式方面，其主要是将 FLV 格式转换为 MP4 格式，而对于播放器的音量控制、进度条、菜单等 UI 展示部分没有做特别的处理。而 video.js 对音量控制、进度条、菜单等 UI 相关逻辑做了统一处理，对媒体播放部分设计了一个插件框架，可以集成不同媒体格式的播放器进去。所以**相比较而言，video.js 更像是一款完整的播放器**。

video.js 对大多数的浏览器做了兼容。它设计了自己的播放器 UI，接管了浏览器默认的`<video>`标签，提供了统一的 HTML5/CSS 皮肤。因此，通过 video.js 实现的播放器，在大多数浏览器上运行时都是统一的风格和操作样式，这极大地提高了我们的开发效率。

除了上面介绍的特点外，video.js 还有以下优势：

- 开源、免费的。不管你是学习、研究，还是产品应用，video.js都是不错的选择。
- 轻量。浏览器 UI 的展现全部是通过 HTML5/CSS 完成，没有图片的依赖。
- 完善的 API 接口文档，让你容易理解和使用。
- 统一的 UI 设计，不管在哪个浏览器，你都看不出任何差异。
- 皮肤可以任意更换，很灵活。
- 开放灵活的插件式设计，让你可以集成各种媒体格式的播放器。
- 支持多种文字语言，如中文、英文等。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（4） 💬（1）<div>请问flv.js、video.js是否都支持2倍速、0.5倍速播放音视频？</div>2019-10-08</li><br/><li><img src="" width="30px"><span>serious</span> 👍（0） 💬（1）<div>
老师，您好，请教个问题哈，http:&#47;&#47;ip1&#47;hls&#47;camear_167_2_.m3u8
http:&#47;&#47;IP2&#47;live&#47;cameraid&#47;1000000%241&#47;substream&#47;3.m3u8
它俩协议相同，文件格式相同，为啥子用video.js前者可以播放后者不可以，后者在微信中是可以播放的
</div>2021-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLIjtoBftwZ3uado3Btc02l98W9cXqO08xiaLPn3r4otj0wjic57CVad7wCKqKaibiblVHtIS0arNj9A/132" width="30px"><span>林玲</span> 👍（0） 💬（2）<div>老师，我用video.js开发的一个web端播放器在chrome端可以，但是在微信或者钉钉的内置浏览器却无法播放</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/38/973fa3e7.jpg" width="30px"><span>潇湘落木</span> 👍（4） 💬（0）<div>HTML5上播放音视频的几种思路：
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;fcDWfOKeEpb_EcGx5-07iA</div>2019-11-05</li><br/><li><img src="" width="30px"><span>Geek_974707</span> 👍（0） 💬（0）<div>老师请问有什么播放器可以直接播放ts文件吗？如果ts文件列表是不断动态发请求拿到的，要怎么播放这个视频呢？</div>2022-04-08</li><br/>
</ul>