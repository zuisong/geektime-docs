你好，我是静远。

恭喜你完成了Serverless核心技术和扩展能力的学习，从这节课开始，我们就要运用之前所学的知识点，开始实战演练了。

前面我们讲到的触发器、冷启动、扩缩容、运行时、可观测等知识点，相信你都已经掌握得差不多了，随便拿出一个相关的问题，你也可以快速应对。但是，这些零碎的“武功招式”怎么才能在实战中运用起来呢？Serverless架构模式的开发和传统架构应用的开发如此不同，我们需要格外注意哪些“坑”呢？

今天，我就把平常“取经”得到的经验以及自己总结出来的“客户常见难题”，分成方案设计、资源评估、调用速度、开发技巧、线上运维等几个方面，跟你聊聊**如何用好“Serverless”**。

希望这节课，让你能够在选择合适的方案和开发手段这些方面得到启发，真正享受Serverless带来的红利。

## 方案选型

方案选型的时候，选错场景和技术大方向是比较忌讳的，不仅可能导致服务不稳定，还会导致修补工作量上升。那么，什么情况下适合用Serverless技术呢？

比较适合Serverless技术的场景，通常由**数据处理计算、应用后端服务、事件触发处理、有状态服务和传统服务升级** 5个维度组成。

![图片](https://static001.geekbang.org/resource/image/23/66/23f35b9eba72ac0e2yy8d79c52037a66.png?wh=1920x1060)

接下来，我们可以对每一个业务的特性做一个抽象总结，看看5个维度不同的侧重点，让你在日新月异的Serverless场景迭代下，也能够自己动手，丰富这张技术选型图谱。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/e4/81ee2d8f.jpg" width="30px"><span>Wisdom</span> 👍（2） 💬（1）<div>我是想构建自己的serverless平台，不直接使用云厂商的serverless平台.</div>2022-10-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmphicC0uibsr4fsbaZcjb7h4NmHLrpEFGibc1Jt7xv820ZQnAA79VgZRSK9jvL3dJgWMgVM1LkQQbw/132" width="30px"><span>初夏</span> 👍（0） 💬（1）<div>最近大模型火起来了，老师什么时候讲一讲怎么结合哈</div>2023-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/e4/81ee2d8f.jpg" width="30px"><span>Wisdom</span> 👍（0） 💬（1）<div>能不能有老师的联系方式？邮箱或是什么的，做一些交流呢</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>Serverless 平台是否支持 设置日记级别的？ 在开发的打印 debug ，生产的时候 不打印， 还是只能开发自己在代码中进行控制</div>2022-10-07</li><br/>
</ul>