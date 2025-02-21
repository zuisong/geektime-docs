你好，我是庄振运。

我们今天继续探讨性能优化的实践，介绍一个系统方面的优化案例。这个案例涉及好几个方面，包括CPU的使用效率、地址映射、运维部署等。

开发项目时，当程序开发完成后，生成的二进制程序需要部署到服务器上并运行。运行这个程序时，我们会不断衡量各种性能指标。而生产实践中，我们经常发现一个问题：是指令地址映射的不命中率太高（High iTLB miss rate），导致程序运行不够快。我们今天就探讨这个问题。

在我过去的生产实践中，针对这一问题，曾经采取的一个行之有效的解决方案，就是同时进行**二进制程序的编译优化**和**采用大页面的部署优化**。我下面就详细地分享这两个优化策略，并介绍如何在公司生产环境中，把这两个策略进行无缝整合。

## 为什么要关注指令地址映射的不命中率？

我们先来看看**为什么需要关注iTLB的命中率**。

在以往从事的性能工作实践中，我观察到CPU资源是最常见的性能瓶颈之一，因此提高CPU性能，一直是许多性能工作的重点。

导致CPU性能不高的原因有很多，其中有一种原因就是**较高的iTLB不命中率**。这里的iTLB就是Instruction Translation Lookaside Buffer，也就是**指令转换后备缓冲区**。iTLB命中率不高，就会导致CPU无法高效运行。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（1） 💬（1）<div>请问像Java这类跑在vm上的语言该怎么做itlb优化呢？</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（1） 💬（1）<div>请问在linux上不改系统配置，如何手工为应用程序指定大页面呢？</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（1） 💬（1）<div>请问文中的指标，什么样的取值算正常，什么样的取值算有问题呢？比如下面我抓的mysql的输出算正常吗？
117,811,688,709      dTLB-loads                                                    (100.00%)
       804,095,370      dTLB-load-misses          #    0.68% of all dTLB cache hits   (100.00%)
       772,145,652      iTLB-loads                                                  
     1,179,670,139      iTLB-load-misses          #  152.78% of all iTLB cache hits

     125.454839041 seconds time elapsed</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>想问下老师：文中提到的“编译优化找到Hot Text区域，然后通过链接器脚本来优化二进制文件中的函数布局”，对于C++程序有对应的工具或具体方法么？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>文中提到“链接器脚本将根据访问顺序，优化二进制文件中的函数布局”，请问这个脚本基于什么方式优化函数布局？链接过程可以自己控制吗？</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（0）<div>开眼了，这个层次的优化，远远超出了一个业务研发的能力范围，平时的主要从程序逻辑、架构设计、调整组件参数的方式来搞，这种指令级的无能为力。
人外有人，天外有天，老师厉害。</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（0）<div>长见识了，居然能优化到这种地步。</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/71/3762b089.jpg" width="30px"><span>stevensafin</span> 👍（0） 💬（0）<div>能不能给个实际的案例</div>2023-09-06</li><br/>
</ul>