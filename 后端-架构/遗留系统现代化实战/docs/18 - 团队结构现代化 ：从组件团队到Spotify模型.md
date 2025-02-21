你好，我是姚琪琳。

前面我们一起学习了现代化的三个方向：代码现代化、架构现代化和DevOps现代化，这三个方向都跟技术相关。接下来我们会学习遗留系统现代化的最后一个方向——团队结构现代化。

这个方向跟管理有关，但无论你是掌控全局的CTO、架构师，还是身处遗留系统一线战队的队员，都有必要了解现代化团队结构是什么样子的。这是因为遗留系统的现代化，除了技术调整，也离不开人的因素。

在我和团队过去大量的实践当中，我们总会发现，维护遗留系统的团队，结构往往并不合理。直接后果就是给软件开发的质量与速度拖后腿，长远来看，还会让我们的架构规划无法落地，回到满是泥潭的老路上。

## 遗留系统中的团队结构

你可以对照一下你所在的开发团队，看看跟后面的情况是否类似。

整个研发部门大体分为业务部、开发部、测试部和运维部。开发部门又可以细分成前端组、后端组、DBA组和架构组，不同部门或小组分别向不同的领导汇报。

除了这些常规、稳定的配置，还有一些为了灵活应变才组建的部门。比如本来没有DBA，但因为某段时间频繁产生数据库性能问题，而临时起意组建了一支DBA小组。而开发部内部也经常因为要开发新的项目，从各个组成抽调成员，而当项目完成之后，团队就原地解散。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（3） 💬（2）<div>目前我们是按业务分组，根据康威定律不适合领域模型的开发方式。原来要想DDD，首先要从分组做起！</div>2022-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/a0/15c82d8b.jpg" width="30px"><span>Triton</span> 👍（1） 💬（1）<div>非常感谢老师的课，受益匪浅，关于团队结构有什么书籍可以参考的？</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（0） 💬（1）<div>老师能不能再讲讲关于限界上下文相关的知识？</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/89/77829168.jpg" width="30px"><span>fliyu</span> 👍（1） 💬（0）<div>一人负责几个微服务</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f6/c3/926f2da9.jpg" width="30px"><span>Paradise丶朽木</span> 👍（0） 💬（0）<div>IPD，开发都是资源线，项目经理立项然后拉人 ... 后端开发大部分时间都是坐在一起的，应该算是职能团队？但是每个开发又都有一定的业务方向 ~</div>2022-06-14</li><br/>
</ul>