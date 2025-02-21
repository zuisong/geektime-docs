你好，我是蒋宏伟。

传说中，比尔盖茨在飞机上顺手撸一个 BASIC 解释器，不 Debug 就能直接跑起来。虽然比尔盖茨是“传说级”的程序员，但他写代码也是需要调试的。我们可以在维基百科的 [Altair BASIC](https://www.quora.com/Are-there-programmers-who-write-virtually-bug-free-code) 词条看到：

> 盖茨和艾伦从波士顿的分时租赁服务中购买了电脑上机时间来完成 BASIC 程序的调试。

但现实中，我们大部分情况都很难做到不 Debug，不调试就能把代码顺利上线，更多情况下，我们都需要和 Bug 做一番搏斗。

从搭建环境时 Gitlab 拉下来的代码跑不起来，到开发过程修改一段代码逻辑总是报错，再到产品上线后也时不时地有产品、测试、老板找过来反馈线上问题。无论是已经存在的、还是潜在的 Bug，这些都需要我们去发现和解决。不是有调侃的话么？我们程序员“不是在解决 Bug 的路上，就是在写 Bug 的路上”。

这话虽然只是一句调侃，但是这也侧面印证了两点：一方面是，我们会遇到很多 Bug，也会花很多时间去解决 Bug；另一方面是，我们直接裸写的代码可能存在较多的潜藏 Bug，我们得花精力把这些潜藏的 Bug 给找出来。那面对这些 Bug，有没有什么通用的解决思路呢？

这正是今天我要和你介绍的，我把它概括为“1+2+3”，也就是一个模型，两个原则，三条思路。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ergUHnv5Vl1G10iaSiaGZ2FDJ4f3qCAWvQzLRkmxLAtfMPuDial5fI8tjSOsMNMicUMAeQKTibEbx71EbA/132" width="30px"><span>yuxizhe</span> 👍（0） 💬（4）<div>老师，你好，进入一个RN页面，该页面的useEffect偶现没有执行，把useEffect中的逻辑延迟300ms，就解决了，请问有没有遇到过这种问题？</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ad/92/98a1fd3c.jpg" width="30px"><span>Geek_e4a05b</span> 👍（0） 💬（1）<div>老师，文章中提到“在本地开发时，需要针对开发的新增的模块写一个新的单元测试。”这个是不是只有业务模块单一或者复用性强才做这样的单元测试？RN的业务模块迭代比较快复用性不强的，或者功能耦合比较紧密的是不是不适用单元测试了？</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/1c/29d0bc42.jpg" width="30px"><span>五十米深蓝，</span> 👍（1） 💬（1）<div>老师能具体讲讲 Flipper 的使用方法吗?  完全无法上手啊</div>2023-07-25</li><br/><li><img src="" width="30px"><span>Treasure</span> 👍（1） 💬（1）<div>您日常开发中有借助这个库[why-did-you-render](https:&#47;&#47;github.com&#47;welldone-software&#47;why-did-you-render)吗?</div>2022-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/64/4b488e16.jpg" width="30px"><span>breeze</span> 👍（0） 💬（0）<div>折腾了两天flipper还是没有跑起来，有什么办法指导么</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/b5/777ba52b.jpg" width="30px"><span>侯同学</span> 👍（0） 💬（0）<div>蒋老师好

项目中使用 axios 怎么配置可以支持 Charles 抓包
配置了 proxy : { host, port }
现在原生项目请求可以抓包 
React Native 请求不能抓包</div>2023-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（0） 💬（0）<div>老师，为什么不推荐React Native Debugger呢？</div>2023-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/ab/981ca927.jpg" width="30px"><span>雷声大</span> 👍（0） 💬（0）<div>你好，我初学rn，调试的时候手机开启live reloading 以后经常红屏报错堆栈溢出是什么原因啊，我启动开发者工具的时候增加了堆栈大小不管用，我用的rn是比较老的0. 51版本
maximum call stack size exceeded.</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/20/0c61760b.jpg" width="30px"><span>house</span> 👍（0） 💬（0）<div>请问这种混合工程怎么调试，比如调试安卓的java代码。尝试直接用android studio启动失败</div>2022-12-16</li><br/><li><img src="" width="30px"><span>Geek_9a4011</span> 👍（0） 💬（0）<div>代码跑不起来啊，苦恼</div>2022-10-07</li><br/><li><img src="https://thirdqq.qlogo.cn/qqapp/101423631/0FD57A9C0C5BFBDA3DA69AE26B3514FB/100" width="30px"><span>下一刻。</span> 👍（0） 💬（0）<div>React Native Debugger是支持抓包请求，右键需要开启 Enable Network Inspect</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/15/74/bb2661ef.jpg" width="30px"><span>诸思码纪(Merrill)</span> 👍（0） 💬（1）<div>老师，你好，rn怎么访问不了不安全的https，请问下这个该怎么解决呢</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ae/36/30fb4c3b.jpg" width="30px"><span>孙树</span> 👍（0） 💬（0）<div>有没有老哥watchman 配置好环境变量之后，Flipper 检查这一项还是 报叹号的</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/5f/06671a0d.jpg" width="30px"><span>python4</span> 👍（0） 💬（1）<div>咱们课程的后续部分, 有没有关于单元测试的部分? 如果没有, 有没有相关的课程或者学习材料推荐. 很期待. 我们平常业务开发基本上都不写测试...</div>2022-04-20</li><br/>
</ul>