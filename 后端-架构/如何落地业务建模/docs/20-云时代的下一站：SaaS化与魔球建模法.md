你好，我是徐昊。今天我们来聊聊SaaS（Software as a Service）化。

按理说，SaaS化与业务建模无关，本不应该出现在这门课程中。但是，SaaS化却与云平台、微服务有着千丝万缕的联系。而且，我是通过建立一个模型解决了SaaS化服务设计的问题，所以勉强算是沾边吧。

那么今天就来讲一讲为什么我们需要在现在关注SaaS化，以及如何通过服务设计，对已经存在的产品进行SaaS化。

## 微服务真的能帮助创新吗？

很多企业上微服务，都是听信了这样的愿景：**微服务可以促进企业内创新，未来只需要编排存在的服务，就能满足一堆创新的需求。**微服务的确可以实现这个愿景，但是有个实现的前提：**微服务需要以开放服务的形式，被其他应用或服务调用**。

所谓开放服务，即：这个服务不是为某个特定应用或服务构建的，而是面向生态中所有可能的客户端构建的。

微服务并不是服务化的应用后台，它封装了企业的业务能力。任何需要用到这个业务能力的应用，都会对这个服务进行调用。因而微服务与应用后台在概念上就存在巨大的差异。应用后台仅仅服务于应用前台，只要满足前台的需求就可以了。而微服务不仅需要服务于当前已知的应用，还要服务于未来可能需要用到对应业务能力的应用。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/81/56/253f17e9.jpg" width="30px"><span>zhizhi</span> 👍（5） 💬（2）<div>大致学习了一遍，感觉没完全整明白😂，，老师，要不要考虑开个训练营。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（1）<div>1.都说波士顿矩阵过于简单粗暴，对其的优化一般也都是升维，比如通用电气矩阵。老师这个魔球直接再给降维了一波。 
2.尴尬客户这一块，上无门下无用，离队可能也会是个选项。毕竟向下能满足不会处于尴尬，商业模式运营向好也不会停留在尴尬。就是因为收益不景气加差异化问题多才处在尴尬阶段，而这个现状上下无门。
3.下一章(下一站)，不知道云时代能带来什么奇迹。2045年奇点在即，不知道会不会有云时代的一笔，翘首以盼，拭目以待。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/7a/abb7bfe3.jpg" width="30px"><span>ZQ</span> 👍（1） 💬（0）<div>抛开技术看，在SaaS化策略执行时还是主要从企业运营考虑（利润和成本）</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（1） 💬（0）<div>魔球 SaaS 选项建模法，有意思👍</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>下一章看起来像元宇宙，进入后可以搭建自己的业务能力，提供服务，碰碰运气</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（0）<div>serverless(lambda)方面，any thing？</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/7a/55618020.jpg" width="30px"><span>马若飞</span> 👍（0） 💬（0）<div>本课心得：庙小妖风大池浅王八多。。。</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/93/32/e11fcd33.jpg" width="30px"><span>Oops!</span> 👍（0） 💬（0）<div>终于学完啦，即将开启SaaS化的工作，有什么建议的书籍和资料可以推荐一下吗？Let&#39;s move forward.</div>2021-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7rprdxQqcea53sw1HCz1YZjQNlSvWg7GETnWYicZLYOQR2GUMOwUnrhAIYzUKJt1zZhUv9icOCztQ/132" width="30px"><span>鸭补一生如梦</span> 👍（0） 💬（0）<div>产品是企业价值的载体，是企业与消费者进行价值交换，实现企业增长赋能的重要容器。
产品架构与技术架构是企业价值的一体两面，不知徐老师能否推荐产品架构的专栏，让我们继续进入“下一章”。谢谢</div>2021-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erD8CwHKGGIia1HwRBxy5GxMLTfGGzOeLjrmZ6ich9Ng7bbPia89iaSibbldnV4uiaKNXFcO2vQ3ztibCrDw/132" width="30px"><span>Williamleelol</span> 👍（0） 💬（0）<div>催更徐老师八叉说～(￣▽￣～)~</div>2021-08-18</li><br/>
</ul>