你好，我是王潇俊。今天我和你分享的主题是：利用Mock与回放技术助力自动化回归。

在《代码静态检查实践》和《越来越重要的破坏性测试 》这次的分享中，我介绍了对持续交付有重大影响的两个测试类型，即静态代码检查和破坏性测试。

你可能已经发现，这两种测试正好适用于持续集成和测试管理的一头、一尾：

- 静态代码检查，适合在所有其他测试类型开始之前优先进行，把住第一关；
- 破坏性测试，则适用于集成或验收测试之后，甚至是对系统进行持续长久的测试。

那么，我们现在再一起来看看，持续交付过程中还有哪些测试方法，以及还有哪些问题和难点吧。

## 持续交付中的测试难点

其实，对于持续交付中的测试来说，自动化回归测试是不可或缺的，占了很大的测试比重。而进行自动化回归测试，就始终会有“三座大山”横在你面前。

**“第一座大山”：测试数据的准备和清理。**

通常情况下，回归测试的用例是可以复用的，所以比较固定，结果校验也比较确定。而如果要实现回归测试的自动化，就需要保证每次测试时的初始数据尽量一致，以确保测试脚本可复用。

如果每次的数据都不同，那么每次的测试结果也会受到影响。为了做到测试结果的可信赖，就有两种方法：

- 一种是，每次全新的测试都使用全新初始化数据；
- 另一种是，在测试完成后，清除变更数据，将数据还原。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/8c/8fba0bdd.jpg" width="30px"><span>debugtalk</span> 👍（5） 💬（1）<div>很多流量是具有时效性，或者不可重复性的，对于这类流量你们是怎么复制回放的呢？</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/8c/f3ada7dc.jpg" width="30px"><span>zhf_sy</span> 👍（1） 💬（1）<div>第二种方案是，在集群中扩容一台服务器，在该服务器上启动一个软交换，由该软交换负责复制和转发用户请求，而真正的用户请求，仍旧由该服务器进行处理。

请问这个技术上怎么实现？复杂吗？</div>2018-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/db/a5/3a94e0bc.jpg" width="30px"><span>疯癫</span> 👍（0） 💬（1）<div>回放是对请求的记录和复制，主要是接口层面，那么app端的功能回归测试，有没有方法获得用户操作的真实场景呢？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/99/49/43bd37b4.jpg" width="30px"><span>孙瑜</span> 👍（1） 💬（0）<div>针对回过测试流程，公司项目中的接口和UI先不论，比较痛苦的是公司数据处理有大量存储过程，然后近半年用帆软reports开发了大量的报表 软件升级时人工回归测试工作量巨大。</div>2020-03-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/AaQknrwU7ltWcahiaEiaCXyYib2TEqocHBhZmAAxJ61oJibAUSrsxCSpdPO1pMZQpR7VJtmpNvQYaFoAibFa9jiaEqZw/132" width="30px"><span>zhongjia19900829</span> 👍（1） 💬（0）<div>生产和测试的环境的数据  怎么保持一致？ </div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/f0/0c4b1548.jpg" width="30px"><span>王毅</span> 👍（1） 💬（0）<div>流量拷贝算不算回放的一种？</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（0） 💬（0）<div>老师，[通过虚拟交换机，复制和记录生产用户的实际请求]，这个相当于用户所有请求的入口都要经过这个虚拟交换机，不会有单点或者性能瓶颈么？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/b0/f22017b0.jpg" width="30px"><span>楚耳</span> 👍（0） 💬（0）<div>回放这块，如果都是写的接口也进行回放吗，这样不会对生产环境数据产生影响吗</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/b4/6b6fb152.jpg" width="30px"><span>王凡</span> 👍（0） 💬（0）<div>”mock可以解决数据的准备和清理的工作”请问怎么做到的？我目前理解的mock只是对第依赖部分不产生真实数据，但mock的上下游服务如果有数据产生，则依旧会产生，还是需要额外去做数据准备和清理，不知道理解是否有偏差？</div>2019-06-16</li><br/>
</ul>