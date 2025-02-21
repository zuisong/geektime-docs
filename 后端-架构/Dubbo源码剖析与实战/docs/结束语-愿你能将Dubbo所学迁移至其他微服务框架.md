你好，我是何辉。

首先，恭喜你完成了这门课程！

从课程一开始，我就非常强调要抓主干、重思考，在课程的学习过程中，也带你从常见问题一步步深挖，完成了很多次源码探索。不知道你有没有好奇过，为什么会这么设计学习思路？

其实这和我的Dubbo学习经历有关。我第一次接触 Dubbo 的时候，完全是懵圈的状态，当时整个项目在往 Dubbo 转型，但是之前我没接触过这个框架，对 Dubbo 的各种参数设置、各种高级特性，几乎是一窍不通，在陌生的 Dubbo 微服务框架体系中，我每天以赶鸭子上架的状态，迭代需求。

时间紧，项目急，这是我们 IT 行业的常态。面对 Dubbo 框架中需要迭代的第一个需求，很多人求快，选择火急火燎地投入到编码开发中，但是这种方式往往是最慢的，也是最后患无穷的。

虽然没有Dubbo开发经验，但是有着丰富项目经验（踩坑经验）的我，在理解清楚需求后，选择花很多时间，查阅其他系统分支代码，希望找到成功的Dubbo相关配置案例代码，找到相对正确的编码开发姿势。

花了大半天，我看了公司十几个系统的代码，主要关注三个方面。你想迅速了解一个系统，也可以参考这个思路。

1. 暴露的接口（即各种 XxxFacade）以及接口在系统中被哪些地方使用了。
2. 调度的入口以及触发调度的配置。
3. MQ 的入口以及监听 MQ 的配置。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/02/5e/d1f78004.jpg" width="30px"><span>豪</span> 👍（2） 💬（1）<div>多谢老师的陪伴，第一遍学的磕磕碰碰，准备二刷了</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（1） 💬（1）<div>需要沉下心来，再撸第二遍；书读百遍、其义自见</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/dc/55/e4453abd.jpg" width="30px"><span>旧衣回收</span> 👍（0） 💬（1）<div>   1.先思考，这个技术知识点有什么用，到底带来了什么便利性，又或者帮我们解决了什么问题。
   2.然后，我会站在框架设计者的角度去思考，怎么设计功能并解决这样的问题，自己尝试一步步推出解决方案。
   3.最后，才深入源码，边探索，边思考和自己设计方案之间的偏差，逐渐理解框架设计者的意图。
   真实相见恨晚的三句话！</div>2023-06-29</li><br/><li><img src="" width="30px"><span>杨老师</span> 👍（0） 💬（1）<div>感谢老师，第一遍过了一下，等第二遍开刷了。</div>2023-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>感谢老师的陪伴，然后继续第二遍</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f2/26/a8ac6b42.jpg" width="30px"><span>听风有信</span> 👍（0） 💬（0）<div>第二遍开启</div>2025-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>唯有学习，不负于我！</div>2024-11-22</li><br/>
</ul>