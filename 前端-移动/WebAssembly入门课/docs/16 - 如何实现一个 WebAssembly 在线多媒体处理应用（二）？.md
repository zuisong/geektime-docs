你好，我是于航。

在上一节课中，我们介绍了本次实践项目在代码层面的大体组成结构，着重给你讲解了需要了解的一些基础性知识，比如“滤镜的基本原理及实现方法”以及“Emscripten 的基本用法”等等。而在这节课中，我们将继续构建这个基于 Wasm 实现的多媒体 Web 应用。

## HTML

首先，我们来构建这个 Web 应用所对应的 HTML 部分。这部分代码如下所示：

```
<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>DIP-DEMO</title>
    <style>
      * { font-family: "Arial,sans-serif"; }
      .fps-num { font-size: 50px; }
      .video { display: none; }
      .operation { margin: 20px; }
      button {
        width: 150px;
        height: 30px;
        margin-top: 10px;
        border: solid 1px #999;
        font-size: 13px;
        font-weight: bold;
      }
      .radio-text { font-size: 13px; }
    </style>
  </head>
  <body>
    <canvas class="canvas"></canvas>
    <div class="operation">
      <h2>帧率：<span class="fps-num">NaN</span> FPS</h2>
      <input name="options" value="0" type="radio" checked="checked"/> 
      <span class="radio-text">不开启渲染.</span> <br/>
      <input name="options" value="1" type="radio"/> 
      <span class="radio-text">使用 <b>[JavaScript]</b> 渲染.</span> 
      <br/>
      <input name="options" value="2" type="radio"/> 
      <span class="radio-text">使用 <b>[WebAssembly]</b> 渲染.</span> 
      <br/>
      <button>确认</button>
    </div>
    <video class="video" type="video/mp4"
      muted="muted" 
      loop="true" 
      autoplay="true" 
      src="media/video.mp4">
  </body>
  <script src='./dip.js'></script>
</html>
```

为了便于演示，HTML 代码部分我们尽量从简，并且直接将 CSS 样式内联到 HTML 头部。

其中最为重要的两个部分为 `“<canvas>`” 标签和 “`<video>`” 标签。`<canvas>` 将用于展示对应 `<video>` 标签所加载外部视频资源的画面数据；而这些帧数据在被渲染到`<canvas>`之前，将会根据用户的设置，有选择性地被 JavaScript 代码或者 Wasm 模块进行处理。

还有一点需要注意的是，可以看到我们为`<video>` 标签添加了名为 “muted”、“loop” 以及 “autoplay” 的三个属性。这三个属性分别把这个视频资源设置为“静音播放”、“循环播放”以及“自动播放”。

实际上，根据 Chrome 官方给出的 “Autoplay Policy” 政策，我们并不能够直接依赖其中的 “autoplay” 属性，来让视频在用户打开网页时立即自动播放。稍后你会看到，在应用实际加载时，我们仍会通过调用 `<video>` 标签所对应的 play() 方法，来确保视频资源可以在网页加载完毕后，直接自动播放。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/31/1c/51f4d08e.jpg" width="30px"><span>zly</span> 👍（2） 💬（2）<div>看到老师在chrome浏览器上没用启用渲染的情况下帧率有200+，然后跟着搞发现自己电脑输出只有60帧，后面发现这个还是跟系统设置有关系的，我的笔记本电脑设置的帧数就60帧，所以渲染视频最高只能到60帧</div>2020-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>对于不同的滤镜效果，是不是对应的卷积核都是有固定的模式的？

还有就是 对于现在的图像处理软件，比如 PS 的滤镜功能的实现是不是也使用的卷积核？</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（1）<div>是不是应该用一个新的数组而不是直接修改原有数组，否则前面卷积后的结果会影响后面的像素</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a5/4f/1107ae92.jpg" width="30px"><span>zzm</span> 👍（0） 💬（1）<div>您好，请问有没有完整的代码，我想运行看看，示例的代码在调用和传参方面有些不理解</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7e/c9/e64e29a1.jpg" width="30px"><span>陈。。。</span> 👍（0） 💬（1）<div>老师，有个问题
requestAnimationFrame在MDN上的描述是：
This will request that your animation function be called before the browser performs the next repaint. The number of callbacks is usually 60 times per second
也就是在浏览器重回前调用，一般帧率是60. 为什么案例中不开启渲染时能有300的fps呢？我不开起渲染的时候就只有40左右的fps了（用火焰图看还有60帧）</div>2023-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/42/e1757583.jpg" width="30px"><span>Jason Yu 于航</span> 👍（0） 💬（0）<div>源码可以参考这里：https:&#47;&#47;github.com&#47;Becavalier&#47;geektime-wasm-tutorial。</div>2021-04-29</li><br/>
</ul>