在[上一篇文章](https://time.geekbang.org/column/article/134284)中，我们对 Licode、Janus、Mediasoup以及Medooze 四个 WebRTC 开源流媒体服务器的实现进行对比，对于想研究音视频多方会议、录制回放、直播等流媒体技术的开发人员来说，Medooze 是很好的选择。因为它支持所有这些功能，通过它的源码及其 Demo 就可以对 Medooze 进行深入学习了。

从本文开始，在接下来的四篇文章我会向你详细讲述 Medooze 的架构、实现以及应用。而本文主要介绍Medooze是如何编译和构建的。

也许你会觉得Linux下的程序编译有什么可讲的呢，直接在Linux系统下执行一下 build 命令不就行了，还需要专门理解系统的编译过程和构建工具的使用吗？实际上，根据我多年的工作经验来看，理解项目的编译过程、熟悉各种构建工具的使用是非常有必要的。下面我就举几个例子，通过这几个例子，我想你就会对它们有一个深刻感悟了。

第一个例子，伴随着技术的飞速发展，构建工具也有了很大的变化，从最早的手动编写 Makefile，逐渐过渡到使用 Autotools、CMake、GYP 等构建工具来生成 Makefile，这些构建工具可以大大提高你的工作效率。比如，通过Andorid Studio 创建JNI程序时，在 Android Studio 底层会使用 CMake 来构建项目，你会发现使用 CMake 构建 JNI 非常方便。然而像Chrome浏览器这种大型项目也用 CMake构建就很不合适了，因为Chrome浏览器的代码量巨大，使用 CMake 构建它会花费特别长的时间（好几个小时），为了解决这个问题 Chrome 团队自己开发了一个新的构建工具，即GYP，来构建这种大型项目，从而大大提高了构建的效率。由此可见，不同的项目使用不同的构建工具对开发效率的提升是巨大的。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（4） 💬（1）<div>很赞，不但能学到视频知识，还熟悉了很多工具</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/a5/e0d96e36.jpg" width="30px"><span>helloa</span> 👍（3） 💬（1）<div>medooze支持手机吗？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/24/dbc4d29d.jpg" width="30px"><span>颜广杰</span> 👍（2） 💬（4）<div>老师，我用这个optimizations分支也编译失败，能麻烦帮我看一下吗？
root@iZwz9isydglfcdgnqd84a4Z:&#47;home&#47;media-server# make
mkdir -p &#47;home&#47;media-server&#47;build&#47;debug
mkdir -p &#47;home&#47;media-server&#47;build&#47;debug&#47;test
mkdir -p &#47;home&#47;media-server&#47;bin&#47;debug
[CXX] debug &#47;home&#47;media-server&#47;src&#47;mcu.cpp
In file included from &#47;home&#47;media-server&#47;include&#47;participant.h:14:0,
                 from &#47;home&#47;media-server&#47;include&#47;multiconf.h:9,
                 from &#47;home&#47;media-server&#47;include&#47;mcu.h:6,
                 from &#47;home&#47;media-server&#47;src&#47;mcu.cpp:5:
&#47;home&#47;media-server&#47;include&#47;rtpsession.h:10:10: fatal error: srtp2&#47;srtp.h: No such file or directory</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（1）<div>怎么这么多人叫李工啊😂</div>2020-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/da/c8/fc153ea2.jpg" width="30px"><span>火哥</span> 👍（1） 💬（1）<div>李工，你好，Medooze支持多路合成吗?</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/de/8d/4c10ba83.jpg" width="30px"><span>一支箭💯¹⁰²⁴</span> 👍（1） 💬（1）<div>Media-server-go这个项目有什么教程吗？</div>2019-10-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLAxia7JictXmRQ02VwuibKOpib5bMcWbQHZeeQhsV17KeGh5u7ySyibgMVLwcoqCA3ZiayI3dLaVOjibRg/132" width="30px"><span>Geek_82d1fd</span> 👍（0） 💬（1）<div>老师，medooze有没有什么集成开发工具可以断点调试</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/0c/a2/14c30983.jpg" width="30px"><span>阿良</span> 👍（0） 💬（1）<div>老师好，我需要浏览器端的WebRTC与小程序端进行视频通话，小程序端推拉流采用的是rtmp协议(使用的是node-media-server)，请问Medooze能否满足这个需求？</div>2021-04-23</li><br/><li><img src="" width="30px"><span>宇宙之王</span> 👍（0） 💬（1）<div>老师近期有计划整理一套在CentOS下的Medooze部署教程吗？？</div>2020-10-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3giaicn2VaDJicDD7WnaT9mB5VbaF6J7aQszN4W9BVmSWmKoVFxTuN7iaDDgrKhlFp49k1iacvjMYSH3eejVbaH0Vhw/132" width="30px"><span>sam</span> 👍（0） 💬（1）<div>在media-server-node目录下执行npm install medooze-media-server --save 出现这个错误

npm ERR! code ENOSELF
npm ERR! Refusing to install package with name &quot;medooze-media-server&quot; under a package
npm ERR! also called &quot;medooze-media-server&quot;. Did you name your project the same
npm ERR! as the dependency you&#39;re installing?
npm ERR! 
npm ERR! For more information, see:
npm ERR!     &lt;https:&#47;&#47;docs.npmjs.com&#47;cli&#47;install#limitations-of-npms-install-algorithm&gt;
</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/92/3fe36d79.jpg" width="30px"><span>平衡之美</span> 👍（0） 💬（1）<div>老师可以 弄个 centos7 安装的教程吗  我们服务器全部是centos7的</div>2020-06-15</li><br/><li><img src="" width="30px"><span>Geek_8a57ad</span> 👍（0） 💬（1）<div>medooze有c++客户端sdk吗?</div>2020-05-27</li><br/><li><img src="" width="30px"><span>taotao</span> 👍（0） 💬（1）<div>李工，你好 licode mcu 具体怎么配置了，我看源码 没看到支持多路合成了</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/da/c8/fc153ea2.jpg" width="30px"><span>火哥</span> 👍（0） 💬（2）<div>李工，你好，咨询一下，我们现在只是将点对点的两人音视频通话过程合成并录制。也是需要Medooze商业版吗？有没有开源的webrtc流媒体服务架构推荐一下，支持音视频通话&#47;合成&#47;录制.感谢！</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/ca/86d58e40.jpg" width="30px"><span>yang</span> 👍（0） 💬（2）<div>呃，坑大了，云上装的是centos7,  官方推荐编译环境ubuntu.一个一个源码下来编译吧。哎.....</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/aa/57/1997dd93.jpg" width="30px"><span>抹染流年听风</span> 👍（0） 💬（1）<div>gyp WARN EACCES user &quot;root&quot; does not have permission to access the dev dir &quot;&#47;root&#47;.node-gyp&#47;10.14.1&quot;
gyp WARN EACCES attempting to reinstall using temporary dev dir &quot;&#47;node_modules&#47;medooze-media-server&#47;.node-gyp&quot;
gyp WARN install got an error, rolling back install
gyp WARN install got an error, rolling back install
gyp ERR! configure error 
gyp ERR! stack Error: EACCES: permission denied, mkdir &#39;&#47;node_modules&#47;medooze-media-server&#47;.node-gyp&#39;
gyp ERR! System Linux 3.10.0-693.2.2.el7.x86_64
gyp ERR! command &quot;&#47;usr&#47;local&#47;node&#47;bin&#47;node&quot; &quot;&#47;usr&#47;local&#47;node&#47;lib&#47;node_modules&#47;npm&#47;node_modules&#47;node-gyp&#47;bin&#47;node-gyp.js&quot; &quot;configure&quot;
gyp ERR! cwd &#47;node_modules&#47;medooze-media-server
gyp ERR! node -v v10.14.1
gyp ERR! node-gyp -v v3.8.0
gyp ERR! not ok 
npm WARN enoent ENOENT: no such file or directory, open &#39;&#47;package.json&#39;
npm WARN !invalid#1 No description
npm WARN !invalid#1 No repository field.
npm WARN !invalid#1 No README data
npm WARN !invalid#1 No license field.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@2.1.2 (node_modules&#47;fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.1.2: wanted {&quot;os&quot;:&quot;darwin&quot;,&quot;arch&quot;:&quot;any&quot;} (current: {&quot;os&quot;:&quot;linux&quot;,&quot;arch&quot;:&quot;x64&quot;})

npm ERR! code ELIFECYCLE
npm ERR! errno 1
npm ERR! medooze-media-server@0.81.1 install: `test -f build&#47;Release&#47;medooze-media-server.node || (node-gyp configure &amp;&amp; node-gyp rebuild --jobs=max)`
npm ERR! Exit status 1
npm ERR! 
npm ERR! Failed at the medooze-media-server@0.81.1 install script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.

npm ERR! A complete log of this run can be found in:
npm ERR!     &#47;root&#47;.npm&#47;_logs&#47;2019-12-11T03_40_52_436Z-debug.log</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/de/8d/4c10ba83.jpg" width="30px"><span>一支箭💯¹⁰²⁴</span> 👍（0） 💬（1）<div>golang 版本的 编译后执行报
# github.com&#47;notedit&#47;media-server-go&#47;wrapper
&#47;usr&#47;local&#47;lib&#47;libsrtp2.a(hmac_ossl.o)：在函数‘srtp_hmac_dealloc’中：
hmac_ossl.c:(.text+0xd9)：对‘HMAC_CTX_free’未定义的引用
&#47;usr&#47;local&#47;lib&#47;libsrtp2.a(hmac_ossl.o)：在函数‘srtp_hmac_alloc’中：
hmac_ossl.c:(.text+0x223)：对‘HMAC_CTX_new’未定义的引用
collect2: error: ld returned 1 exit status</div>2019-10-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er5tJHYf1ica9LdMM5Q9BCfwBL7dPibTPwicbHpuGbicAS3MquenIs7x3VNW5ZbuJhYZBwA84ianfedprA/132" width="30px"><span>Geek_bang</span> 👍（0） 💬（4）<div>执行npm install medooze-media-server --save 有遇到这个问题嘛？
npm WARN optional Skipping failed optional dependency &#47;chokidar&#47;fsevents:
npm WARN notsup Not compatible with your operating system or architecture: fsevents@2.1.1
npm WARN enoent ENOENT: no such file or directory, open &#39;&#47;root&#47;workspace&#47;Medooze&#47;test&#47;package.json&#39;
npm WARN test No description
npm WARN test No repository field.
npm WARN test No README data
npm WARN test No license field.
npm ERR! Linux 4.15.0-20-generic
npm ERR! argv &quot;&#47;usr&#47;bin&#47;node&quot; &quot;&#47;usr&#47;bin&#47;npm&quot; &quot;install&quot; &quot;medooze-media-server&quot; &quot;--save&quot;
npm ERR! node v8.10.0
npm ERR! npm  v3.5.2
npm ERR! path &#47;root&#47;workspace&#47;Medooze&#47;test&#47;node_modules&#47;.staging&#47;@types&#47;prop-types-51921f0d
npm ERR! code ENOENT
npm ERR! errno -2
npm ERR! syscall rename

npm ERR! enoent ENOENT: no such file or directory, rename &#39;&#47;root&#47;workspace&#47;Medooze&#47;test&#47;node_modules&#47;.staging&#47;@types&#47;prop-types-51921f0d&#39; -&gt; &#39;&#47;root&#47;workspace&#47;Medooze&#47;test&#47;node_modules&#47;tap&#47;node_modules&#47;@types&#47;prop-types&#39;
npm ERR! enoent ENOENT: no such file or directory, rename &#39;&#47;root&#47;workspace&#47;Medooze&#47;test&#47;node_modules&#47;.staging&#47;@types&#47;prop-types-51921f0d&#39; -&gt; &#39;&#47;root&#47;workspace&#47;Medooze&#47;test&#47;node_modules&#47;tap&#47;node_modules&#47;@types&#47;prop-types&#39;
npm ERR! enoent This is most likely not a problem with npm itself
npm ERR! enoent and is related to npm not being able to find a file.
npm ERR! enoent

npm ERR! Please include the following file with any support request:
npm ERR!     &#47;root&#47;workspace&#47;Medooze&#47;test&#47;npm-debug.log</div>2019-10-24</li><br/><li><img src="" width="30px"><span>taotao</span> 👍（0） 💬（0）<div>李工，你好 请问licode怎么配置mcu了  我看了代码 没看到它支持多路合成了？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/da/c8/fc153ea2.jpg" width="30px"><span>火哥</span> 👍（0） 💬（1）<div>李工，咨询一下，我们只需要点对点两个人的音视频合成，现在Medooze开源版的支持吗？如果不支持有没有推荐一下支持webrtc并录音录像的流媒体服务框架。感谢！</div>2020-01-15</li><br/>
</ul>