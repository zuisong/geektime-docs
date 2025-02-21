你好，我是陈旭，今天我们来说说App开发过程中获取数据的配置。

数据配置是应用开发三部曲（布局、交互、数据）中的第三个环节，根据App的不同，它与数据之间的关系也不同：有的App可以产生数据（信息采集类）；有的App则是数据消费者，或者兼而有之。数据采集+推送，包括文件上传的方式总体来说都比较简单，不在今天的讨论范围内，这一讲我们主要讨论**组件如何获取和渲染数据**。

而且，由于我们这个专栏所说的低代码平台生成的App都是B/S架构的，App首选的获取数据方式当然是HTTP通道，实际上，即使是C/S架构的App，HTTP通道也依然是一个非常好的选项。所以，这一讲我们就只讨论通过HTTP通道来获取数据的情况。

## 请求参数、数据结构修正、数据模型

我们先来讨论数据获取的最基本动作，从请求发出去到数据展示到UI上，全程会涉及参数设置、返回的数据结构修正、数据模型映射等几个主要环节。

你要注意，这几个环节不包含获取数据的异常处理流程。异常处理是相对简单的一部分，只要别忘了在配置界面上增加对应的出错处理配置，生成的代码注意捕获HTTP异常即可。

**第一个基本动作是HTTP请求的参数配置。**HTTP协议允许我们在多个不同的位置设定参数，可能传参的位置至少有三处：通过url传参、通过请求头传参，通过请求body传参。你在设计参数配置界面的时候，别忘了要给这3个可能传参的位置留出配置界面。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/52/d67f276d.jpg" width="30px"><span>轩爷</span> 👍（1） 💬（0）<div>数据打桩这里也有好些应用可以直接mock出模拟数据，yapi、apipost等。</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5d/74/2762a847.jpg" width="30px"><span>流乔</span> 👍（1） 💬（0）<div>浏览器插件可以解决跨域问题的</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/f7/2fe4c1a1.jpg" width="30px"><span>洛河</span> 👍（1） 💬（0）<div>老师，你好：
请问一下，有哪些思路在提效、赋能两个方面给老板画饼呢。感谢！！！
</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/f7/2fe4c1a1.jpg" width="30px"><span>洛河</span> 👍（1） 💬（0）<div>老师，你好：
数据模型的消费是在什么阶段和什么场景下呢</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ef/ed/90d0199d.jpg" width="30px"><span>李凯</span> 👍（1） 💬（0）<div>老师能先简单提一下跨域策略是怎么解决的吗? 我能想到的服务端层面有一个通用的代理服务器, 通过它做了一层转发. 浏览器层面只知道2个点可以绕开, 一个把Chrome浏览器的允许跨域访问限制打开, 一个是利用script或者img这种标签没有跨域限制对第三方服务进行访问.</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/57/7e092d62.jpg" width="30px"><span>做你的暖手宝</span> 👍（0） 💬（0）<div>老师请问，低代码平台生成的代码仅限于app端么？后端的比如java代码怎么办呢？是提前开始好服务么？</div>2022-11-29</li><br/>
</ul>