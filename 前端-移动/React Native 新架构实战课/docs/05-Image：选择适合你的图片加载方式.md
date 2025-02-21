你好，我是蒋宏伟。

今天我们来讲解 React Native 框架中的 Image 组件。顾名思义，图片组件 Image 就是用来加载和展示图片的。

你可能会觉得，图片组件的基础用法非常简单呀，学起来也很容易上手，这有什么好讲的呢？没错，正因为它很简单，有时候，我们可能会忽视对这些基础知识的琢磨。在日常开发中，图片是影响用户体验的关键因素之一，它很常见，基本上哪里都有它。而且相对于文字，图片也更容易抓住用户的眼球。图片组件很重要，但要用好却不那么容易。

React Native 的 Image 组件一共支持 4 种加载图片的方法：

- 静态图片资源；
- 网络图片；
- 宿主应用图片；
- Base64 图片。

这4种方案给我们业务提供了更灵活的选择空间，但同时也让不少同学犯了选择困难症，不同情况下我该怎么选呢？今天，我们就来深度剖析这 4 种方案分别的适用场景是什么，并给你介绍一下我推荐的最佳实践。

## 静态图片资源

静态图片资源（Static Image Resources）是一种**使用内置图片**的方法。静态图片资源中的“静态”指的是每次访问时都不会变化的图片资源。站在用户的视角看，App 的 logo 图片就是不会变化的静态图片资源，而每次访问新闻网站的新闻配图就是动态变化的图片。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/7b/ebe8451e.jpg" width="30px"><span>极客时间用户</span> 👍（0） 💬（1）<div>发布包的时候打包的bundle和images都在包里面，如果动态更新的话怎么处理bundle和images？</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/d0/6875ea5a.jpg" width="30px"><span>小天儿</span> 👍（0） 💬（1）<div>第一题题意没有太理解；
第二题的话，如果是我，应该会使用 node 来开发一个命令行工具，以文件夹划分项目，通过添加一个 json 配置文件的方式关联项目与其配置（上传地址、秘钥等等），然后只需要执行同步命令，就可以快速对本地存在而远程不存在的图片进行上传</div>2022-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ergUHnv5Vl1G10iaSiaGZ2FDJ4f3qCAWvQzLRkmxLAtfMPuDial5fI8tjSOsMNMicUMAeQKTibEbx71EbA/132" width="30px"><span>yuxizhe</span> 👍（0） 💬（1）<div>老师，你好，请问这里“编译后的 Bundle 和静态图片资源，会在构建时内置到 App 中”，内置到App哪个目录下呢？</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/59/8b/8cdeac4e.jpg" width="30px"><span>沐</span> 👍（0） 💬（1）<div>老师有没有遇到过一个页面最多只能加载15张uri格式的图片，超出就会显示为空白</div>2022-04-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erje3495m1a2Go8c801c8OwtEzaHicomaEfcIal5jQSH2I1QrfSgBKoZzsGcRiaIv2Fj5ibNTCj3c0Mg/132" width="30px"><span>潇潇暮雨</span> 👍（0） 💬（1）<div>老师是否遇到过Image加载不出来远程图片的情况，宽高都有设置，偶现，ios出现的频率高些，RN0.59版本。后来我们就不用RN的Image了，桥接了原生网络图片库。</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/fa/b88b8b4e.jpg" width="30px"><span>郭浩</span> 👍（1） 💬（0）<div>如果有讲到@2x @3x这些不同图片是怎么在不同手机分辨率自动适配的，就更好一点😁</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/ed/f1/1ee1d707.jpg" width="30px"><span>三好大兄弟</span> 👍（0） 💬（0）<div>老师，你好，react native官方UI库，和ant-design&#47;react-native、react-native-elements这些有什么区别呢，是否存在性能差异？react native官方UI库是调用安卓、iOS原生绘制的UI库？ant-design&#47;react-native、react-native-elements这些是纯网页的UI库吗？</div>2024-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/7b/ebe8451e.jpg" width="30px"><span>极客时间用户</span> 👍（0） 💬（0）<div>动态更新的话，bundle和images作为一个压缩包，app通过网络下载然后解压到手机沙盒里面，这样加载bundle的时候，images也有了。</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8b/6e/d3feb1cd.jpg" width="30px"><span>佰亿</span> 👍（0） 💬（0）<div>iOS图片缓存我记得是用了nscache，缓存大小20M</div>2022-06-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/KRaFF1vD8IlFg8uD8mGRbq7c7PKWDlm1Xyicrv7BfSOSDITTHUQvmf1bGoDlDuu74yHdoacZMj7z5KxZqj5dU6Q/132" width="30px"><span>周文硕</span> 👍（0） 💬（0）<div>这篇讲的很清晰，点赞</div>2022-06-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuOgTn2sQvEonB1Nibo2ZYMVuljYL4LvXZtAfibgBASniakRwU1PP3Qom1iaxEqiahGwvre8SltpyOBmQ/132" width="30px"><span>Geek_a96f3d</span> 👍（0） 💬（0）<div>我想知道 大家怎么实现图片管理工具的</div>2022-04-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKXDEvzzjFrgTLou3Bib81IEFiatoiaFx7d5h1PS94CKicdkicGobjk1rLOkhGcfQG0xFXRyjWfiaCNr0vw/132" width="30px"><span>ReturnTrue</span> 👍（0） 💬（1）<div>“这种加载图片的方法没有任何的安全检查，一不小心就容易引起线上报错。”
这里安全检查，老师能具体说下需要哪些安全检查吗？还有就是报错的类型及原因，在日常开发中遇到也好解决</div>2022-04-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKXDEvzzjFrgTLou3Bib81IEFiatoiaFx7d5h1PS94CKicdkicGobjk1rLOkhGcfQG0xFXRyjWfiaCNr0vw/132" width="30px"><span>ReturnTrue</span> 👍（0） 💬（3）<div>“字面常量&#39;.&#47;dianxin.jpg&#39;提供的是一个直接的明确的图片相对路径，打包工具很容易根据字面常量&#39;.&#47;dianxin.jpg&#39; 找到真正的图片，提取图片信息。而变量path 提供的是一个间接的可变化的图片路径，你光看require(path) 这段代码是不知道真正的图片放在哪的，打包工具也一样，更别提自动提取图片信息了。”
看了这些，还是没明白为什么字面量可以，变量不可以。是不是可以从request的原理实现来讲下传入字面量和变量时的差别？
图片加载的三步大致看不明白了，但是好像没有讲这里，还是我漏看了哪里吗？麻烦老师解答下。</div>2022-04-08</li><br/>
</ul>