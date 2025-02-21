你好，我是Barry。

这节课，我们一起来学习如何在视频平台中实现自己的第一个视频播放器。

在视频网站中，播放器是不可或缺的存在，我们在日常开发中，用的大多是网页开发，很少用到播放器。相信通过这节课的学习，你对播放器的理解和使用会更上一个台阶。

今天，我将带你从“Hello World”起，**探索如何使用前端技术在网页上播放视频。**在开始实战之前，让我们先了解一下网页上播放视频的由来。

## 视频播放器的前世今生

说到播放器，就不得不提到HTML5的一些新的特性了。我们都知道HTML5在老版本的基础上加入了很多新特性，比如后面这些特性。

- 用于绘画的 canvas 元素。
- 用于媒介回放的 video 和 audio 元素。
- 对本地离线存储更好的支持。
- 新的特殊内容元素，比如 article、footer、header、nav、section。
- 新的表单控件，比如 calendar、date、time、email、url、search。

可以看到，其中一个重要的特性就是支持video标签在网页上播放视频。

下面这行代码就可以实现一个简单的HTML5的视频播放器demo。

```javascript
<video src="movie.ogg" controls="controls"></video>
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/95/f8/0906c158.jpg" width="30px"><span>宋小宋^_^!</span> 👍（0） 💬（2）<div>老师，我想先实现一个最简单播放器的例子，但是过程中一直报错，百度了一圈也没解决，现在是控制台报错 Uncaught TypeError: Cannot call a class as a function，下面是我的代码

&lt;template&gt;
  &lt;div&gt;
    &lt;div id=&quot;dplayer&quot;&gt;&lt;&#47;div&gt;
  &lt;&#47;div&gt;
&lt;&#47;template&gt;
&lt;script&gt;
import DPlayer from &#39;dplayer&#39; 
export default {
  name:&#39;PlayComponent&#39;, 
  mounted(){
    const dp = new DPlayer({
      container:document.getElementById(&quot;dplayer&quot;),
      video: {url: &#39;http:&#47;&#47;static.smartisanos.cn&#47;common&#47;video&#47;t1-ui.mp4&#39;}
      })}}
&lt;&#47;script&gt;
</div>2023-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/03/c5/b3364e49.jpg" width="30px"><span>佩慎斯予氪蕾沐</span> 👍（0） 💬（1）<div>我没有工作经验，如果是我，我会想办法通过监听点击的方式，或者watch监听某个和暂停相关变量，再使用v-if展示弹窗面板，或者直接写好弹窗面板，用点击来控制显示隐藏display为none等等。</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（3）<div>请教老师几个问题：
Q1: 用VSCode创建工程，创建vue文件。运行后浏览器能正常显示。此过程中，浏览器是直接解析vue文件吗？还是说vue文件先被编译成另外一种文件（比如html）然后被浏览器解析？
Q2: 网页端有canva，安卓端也有。这两种是同一种技术吗？或者更具体地说，是同一套源代码吗？
Q3: 对于前段工程，Node起什么作用？只是支持NPM吗？</div>2023-05-17</li><br/>
</ul>