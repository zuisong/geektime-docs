你好，我是陈旭。

今天我们来聊聊低代码平台实现可视化开发过程中一个难点功能：**可视化编程**。可视化编程解决的是应用开发三部曲（布局、交互、数据）中的交互环节。

但这样说有点狭隘，如果低代码平台同时支持开发后端Rest服务，那可视化编程的方法可以完全复用到后端的Rest服务开发中，而不仅限于前端交互逻辑的开发。因此，这一讲的内容实际上同时覆盖了前后端的低代码实现，**如果没有特别的说明，这讲的所有内容都适用于前后端低代码场合下使用**。

在开始之前，我想请你想一想这个问题：编码难在哪？

作为一个写了近20年代码的职业码农，面对这个问题，我的第一感觉是难点很多，数都数不清，但要列个一二三来，又觉得不好下手。仔细一想，编码就像艺术创作，比如绘画，虽然绘画有一定的套路，但从开始到最终完成，有着巨大可自由发挥的空间，而填满这些自由发挥空间的，只能是作者的经验。并且，决定一幅画是否有灵魂的，也只能是作者的经验。

编码何尝不是这样呢？大概套路是有的，但细到每一个函数、每一个类如何编写，则完全由开发人员的经验决定。专家写的代码不仅性能好，bug少，而且可读性非常高，反之，缺乏经验的开发人员能按预期把功能跑通就不错了，哪还顾得上可读性或性能。那有没有一种方法，可以让新手也可以写出专家级的代码呢？这正是我们今天要解决的问题。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/39/a6e1cb2a.jpg" width="30px"><span>imonk</span> 👍（9） 💬（0）<div>一图胜千言：希望老师在文章中多搭配产品原型图、应用架构设计图、技术架构设计图等。现在通篇的文字描述有点不好理解。</div>2022-04-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/agvVN5wGlGbjmVl86cXByDJFHoQBlyN9SI9hqvSkmr5e5z7cKvCyTuwXuZjx5gft9OzPt7AnRS9IHjV9QPQTug/132" width="30px"><span>Geek_b66b01</span> 👍（2） 💬（0）<div>很鸡肋的一个设计，开发人员不愿用，业务人员不会用。花那么大精力做WebIDE也很没必要，可以按你公司的代码架构一键导出，需要改的自己导到工程里面去改。不要觉得是异想天开，华为已经实现了</div>2024-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/64/9f404dd2.jpg" width="30px"><span>iron</span> 👍（0） 💬（0）<div>按照“功能”去识别节点，这个如果是编排后端逻辑，估计很不适合，至少从“复用”角度看也不可行；
节点应该是按照“对象”、“组件”等视角去识别，（具体识别方法，ooa的方法论很多就不展开了），功能是节点间的“连接线”可能更合适，可以看一下阿里的BizWork，或者uml的画图规则；</div>2023-02-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIstR9CfEytdeJyicODHOe6cYGt4icg8cNVam9mE0s7picUsInZvwvia1hEtKsyHETfic0jrAddjt0wXdA/132" width="30px"><span>Geek_d68bf9</span> 👍（0） 💬（1）<div>通篇看下来，有个疑问，这么复杂的逻辑编排，业务人员真的通用&#47;会用吗？开发的人员如果不是搞这块的，看起来都头大</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（0） 💬（1）<div>异步功能节点：如果是流程中的异步，可能就要用到网关了吧。用网关控制往下的流程；界面元素可能就需要维护一个广播机制。
功能节点：判断是不是可以维护成相对固定的模式，更灵活复杂的还是直接写代码吧。毕竟一个很大的公式(各种优先级)用代码表达比较简单，各种鼠标维护出来的配置，耗时不说，修改也是一个灾难。也不容易保证能配的对。
</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/f7/2fe4c1a1.jpg" width="30px"><span>洛河</span> 👍（0） 💬（0）<div>还是没有弄明白，直接式和融合式的区别已经差异是什么</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/f7/2fe4c1a1.jpg" width="30px"><span>洛河</span> 👍（0） 💬（0）<div>老师：
可视化编排的逻辑怎么和页面功能交互绑定的呢。有可参考的开源项目嘛。感谢</div>2022-05-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrjwowQB5WFAuPzAib4aLJaT1kV4RLd7kqYpSB687lISFsoXiaUvgL7O6DjFLVIFos6147ialVSSLIQ/132" width="30px"><span>Geek_06eefc</span> 👍（0） 💬（0）<div>两进两出</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ef/ed/90d0199d.jpg" width="30px"><span>李凯</span> 👍（0） 💬（0）<div>老师, 请教一个问题,  逻辑编排过程中, 会遇到当前逻辑依赖上一步逻辑操作的返回值, 这个时候怎么获取这个值以及它应该存储到哪里?</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ef/ed/90d0199d.jpg" width="30px"><span>李凯</span> 👍（0） 💬（0）<div>整个逻辑操作的事件流能否包装一下, 全部采用Promise返回值的方式?</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c4/4d/85014aab.jpg" width="30px"><span>一叉树</span> 👍（0） 💬（0）<div>思考题一：还有循环语句，也很基础。

思考题二：异步，意味着从当前的流程中跳出来。异步功能节点的输出应该有两个“空”：
1. 完成自己的异步工作之后，接着开启哪一个流程。
2. 下一个流程的初始输入。这里可以填异步功能模块的某个结果变量。
这样，异步功能节点，依旧是“填空即开发”的游戏了。

思考题二我也不知道该怎么编码，只是根据自己理解规划的，望老师指点一下。</div>2022-04-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8QrKpDnOIamdkVrTAdY6sJtGPE61B0y31MzkDXyz1yDCPmNtKzibPqzw95M2l7kSibS72dFEiaEjqoBS1DGf2SszA/132" width="30px"><span>Geek_jigang</span> 👍（0） 💬（0）<div>老师，想请教一下，逻辑流程图在出码的时候，对if,还有循环，是怎样处理这些 不是顺序流转的情况的</div>2022-04-16</li><br/>
</ul>