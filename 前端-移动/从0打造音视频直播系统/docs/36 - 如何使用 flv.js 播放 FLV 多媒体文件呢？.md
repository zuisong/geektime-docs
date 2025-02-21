flv.js 是由 bilibili 公司开源的项目。它可以解析FLV文件，从中取出音视频数据并转成 BMFF片段（一种MP4格式），然后交给HTML5 的`<video>`标签进行播放。通过这种方式，使得浏览器在不借助 Flash 的情况下也可以播放 FLV 文件了。

目前，各大浏览器厂商默认都是禁止使用Flash插件的。之前常见的 Flash 直播方案，到现在已经遇到极大的挑战。因为它需要用户在浏览器上主动开启 Flash 选项之后才可以正常使用，这种用户体验是非常糟糕的，而 flv.js 的出现则彻底解决了这个问题。

flv.js 是由 JavaScript 语言开发的，该播放器的最大优势是，即使不安装 Flash 插件也可以在浏览器上播放 FLV 文件。虽说 Adobe 公司早已不再为 Flash 提供支持了，但 FLV 多媒体文件格式不会就此而消亡。因此，在没有 Flash 的时代里，能实现在浏览器上播放 FLV 文件就是 flv.js 项目的最大意义。

## flv.js 基本工作原理

flv.js 的工作原理非常简单，它首先将 FLV 文件转成 ISO BMFF（MP4 片段）片段，然后通过浏览器的 Media Source Extensions 将 MP4 片段播放出来。具体的处理过程如下图所示：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（3） 💬（2）<div>感觉软件世界就是数据，抽象和算法，一马平川，其他各种障碍只有各种公司或者软件提供的糟糕接口，以及缺少人去填补这些接口衔接。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/df/9f/6db75dff.jpg" width="30px"><span>Random</span> 👍（2） 💬（2）<div>老师你好，我现在渲染视频的方案，是把原生端收到的视频流用YUV的格式渲染在canvas上的，性能不是特别好，有什么好的方式直接把视频流用video标签播放吗？一个electron 应用</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/45/63/005d03b2.jpg" width="30px"><span>QD账号</span> 👍（0） 💬（1）<div>老师，请问一下在浏览器直接播放rtmp流，需要开启flash，现在想到有一个方式是拉hls，或者还有什么方式可以解决这个问题吗？</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/da/4174ed8e.jpg" width="30px"><span>为城</span> 👍（0） 💬（1）<div>老师，WebRTC如何推流至直播服务器没有篇幅介绍，能提供多一些这方面内容的介绍吗？</div>2019-10-07</li><br/><li><img src="" width="30px"><span>Geek_0b5414</span> 👍（1） 💬（0）<div>老师，请问一下有没有支持H265格式的流氏播放</div>2022-04-28</li><br/>
</ul>