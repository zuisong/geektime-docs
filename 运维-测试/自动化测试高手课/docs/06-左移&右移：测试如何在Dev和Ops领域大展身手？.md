你好，我是柳胜。

前面的几讲，你已经学习了ROI模型，它开始于一颗带有ROI DNA的种子，不断生长，直到长成一棵大树。从树根到枝干、从规律到原则，它贯穿了一个自动化测试项目，从生到死的完整生命周期：设立目标，制定策略，选择框架到代码的实现，上线的度量，再到衰竭退出。

我把价值篇讲过的内容加以整理，得到了下面的树结构。上面的绿色部分是收益，下面的红色部分是成本。ROI模型树从左到右，是从根到枝干，从ROI理论到实践的延伸和具象化。

![图片](https://static001.geekbang.org/resource/image/be/e2/bebf2e6673b64e11a0ff32703f7be0e2.jpg?wh=1920x1346 "ROI模型树")

ROI模型展开的这棵大树，告诉了我们健康的自动化测试项目长什么样子。但是还有一个现实的问题，我们怎么从这里到那里？换句话说，咱们怎么把自动化测试项目的节奏带起来，让它进入到一个不断提升ROI的轨道上去。

这里有一个很朴素的道理，好马是跑出来的，好钢是炼出来的。首先，要让自动化测试跑起来，增加它的运行次数，这是前提条件。在这个过程中，再修复它的问题，调整它的集合，提高它的可诊断性，整个项目就激活了。

所以，你要找到更多的土壤让自动化测试落地生长。如果你想在工作中推广自动化测试，哪些落地场景更容易出业绩呢？除了之前说过的回归测试领域，我们不妨把眼光从测试工作放宽到更多的领域，Dev和Ops领域，自动化测试在这些领域里一样可以发挥价值，我叫它自动化测试左移和自动化测试右移。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="" width="30px"><span>woJA1wCgAA3aj6p1ELWENTCq8KX2zC2w</span> 👍（4） 💬（1）<div>目前在开展接口测试，和开发工作并行，实际中有点难度的地方是开发的接口变化太频繁，可能出测试版本前才能确定下来。 并不是全意义上的并行。敏捷开发， 老师提到的持续更新维护和测试已经形成基线了。这里有了小的实践和积累</div>2022-04-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoApjXQ0ib4MDEmAsChPIhHQemEOTIkT6OvSq8D99MIAYfq6dGhhPoHlfDIZtibiaIz3Zrc08ibKBTsCQ/132" width="30px"><span>阿萨聊测试</span> 👍（3） 💬（1）<div>蓝绿部署的蓝是新版本，绿是线上正在运行的版本。当部分蓝版本的用户使用和测试验证通过，蓝变绿。
现在测试左移 api左移，UAT右移，稳定性测试右移。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/a9/ee6c8c9d.jpg" width="30px"><span>dakangz</span> 👍（2） 💬（2）<div>我们公司属于左移基本做不到，因为项目多，变化快，测试没法前期介入设计，只能参加产品评审；但是右移却一直在进行，我已经部署了十几个监控工具，简单来说运维只能保证服务探活，而右移是为了保证生产环境的业务数据正常</div>2022-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5GQZCecntmOibVjWkMWVnibqXEZhAYnFiaRkgfAUGdrQBWzfXjqsYteLee6afDEjvBLBVa5uvtWYTTicwO2jKia0zOw/132" width="30px"><span>Geek_a4cca6</span> 👍（2） 💬（1）<div>测试左移想法自然是好的，都是为了更早发现BUG，提交修复。 之前公司也尝试过一段时间，由于是业务人员写自动化脚本，最终还是搞得大伙都太累，整天加班，尤其是人力本来就紧张的情况下，更累。</div>2022-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7BNKxqREtUP9ZhWgic92pHKkaPLGPM4xVjnoyMhHoFiaMUq5L0cCgCEXbeibiaR7ONnXh3W72pJUH5lq5pmphs14sA/132" width="30px"><span>闲不住的令狐冲</span> 👍（1） 💬（1）<div>补充一下，实际情况很多并不是意识层面没转变，而是公司组织架构的阻力。开发和测试分开甚至是对立，想做到做好测试左移右移，必须是开发和测试齐心协力。</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d8/8b/d81769bf.jpg" width="30px"><span>chin</span> 👍（1） 💬（1）<div>问题一：
蓝绿部署，是一种可以保证系统在不间断提供服务的情况下上线的部署方式。
在系统升级的时候下，我们首先把一个集群（比如集群A）从负载列表中摘除，进行新版本的部署。集群B仍然继续提供服务。
当集群A升级完毕，我们把负载均衡重新指向集群A，再把集群B从负载列表中摘除，进行新版本的部署。集群A重新提供服务。
最后，当集群B也升级完成，我们把集群B也恢复到负载列表当中。这个时候，两个集群的版本都已经升级，并且对外的服务几乎没有间断过。

问题二：
我觉得不管左移还是右移，都是有空间的。但其实还是有一个依赖关系，先做好左移，右移才有基础。右移是所有测试人员应该仔细思考的事情，是提升测试人员影响力一个方向。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e4/e2/ea311979.jpg" width="30px"><span>七禾叶</span> 👍（0） 💬（1）<div>问题一：蓝绿升级类似公司的灰度环境，先让特定人群试用升级后的服务。如果有问题则回滚，没有问题则正式发布上线。
问题二：测试左移动：
            1.自动化左移动需要自上而下进行推广。
            2.对于测试人员技术能力以及综合素质有着更高的要求。
            3.对于项目而言不应有频繁的变动。
           测试右移：
            1.已使用平台进行接口自动化定时运行，更进一步的话对于生产环境各个性能指标进行监控，加深对用户行为画像绘制。</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c1/46/a81f7402.jpg" width="30px"><span>王大华</span> 👍（0） 💬（2）<div>老师您好
在生产环境的自动化集合中，我看包含了性能测试，请问性能自动化在线上执行的时候不会影响到线上用户的使用吗？</div>2022-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/57/e5/124c56f6.jpg" width="30px"><span>饿魔</span> 👍（0） 💬（1）<div>生产上做自动化要看情况的，有的业务可能不合适，比如互联网金融相关的，总不能在生产上一直去提交贷款和还款吧？</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/11/bdffffa6.jpg" width="30px"><span>派森</span> 👍（0） 💬（1）<div>领导讲了半年的持续交付，都不愿意在自动化领域多投入一个人力</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/26/48/c713f33e.jpg" width="30px"><span>余明栋</span> 👍（0） 💬（1）<div>红绿部署在网络游戏的实际运用和作者说的略有出入，并不是先准备一个环境验证是否绿色，而是原来的红环境暂停服务，备份，然后进行升级，验证是否绿色，最后对用户开放服务</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d6/09/e9bfe86f.jpg" width="30px"><span>夜歌</span> 👍（0） 💬（2）<div>测试左移，现在老板就给功能测试时间，还在压缩，哪里设计左移方案并提前实施呢…做都能做，但都是加班啊，9 10点那种</div>2022-04-12</li><br/><li><img src="" width="30px"><span>woJA1wCgAA3aj6p1ELWENTCq8KX2zC2w</span> 👍（0） 💬（1）<div>老师，您在既往项目中ROI能达到多少呢</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/d3/62/791d0f5e.jpg" width="30px"><span>鑫宝</span> 👍（0） 💬（0）<div>之前在做自动化的时候，老大提出了一个要求，要求新功能也使用自动化100% 测试。 一般测试新功能，都是手工测试先行，测试完成后再进行自动化。 老大说，其实在做测试用例的时候， 可以跟开发约定好预期的断言关键字段，类似于 前后端的连条。这样开发写好了开发代码，测试也写好了测试代码。就可以跑一遍试试了。 
这应该有点类似于测试左移吧。</div>2023-07-07</li><br/>
</ul>