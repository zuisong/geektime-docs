你好，我是柳胜。

今天是设计篇的最后一讲，从第十七讲到现在，我们围绕Job元数据模型讲了很多内容。毕竟，这个Job模型设计，是一个新的设计方法论，需要从模型推演、设计方法、不同场景的设计案例等各个方面来学习理解。虽然过程中有点像盲人摸象一样，但我们最后终于勾勒出了一个全面的理解。

不过，一种新的设计方法想要生根发芽，不光要在理论层面讲得通，还要让使用者轻松快速地掌握它，并且学以致用。沿着这个思路，今天我们把基于Job模型的框架实现梳理一遍，明确都需要实现什么，以及怎么实现。

经历了这个思考过程，对你把Job模型在团队里推广和使用大有帮助，而且对你去设计、推广自己的框架也同样适用。一个设计方法要在工作里落地，它就必须要和日常的设计活动，开发维护活动结合在一起，有3个关键场景：

1.自动化测试设计的评审和交流（设计文档化）；  
2.自动化测试设计和实现的一致性维护（设计代码化）；  
3.自动化测试的报告呈现（结果可视化）。

## Job设计文档化

我们先从设计评审和交流说起，这离不开一份清晰易读的设计文档。在软件技术迅猛发展的今天，开发人员可以用Swagger来表达API的接口设计，运维人员可以用YAML来表达部署的方案，但**测试人员却没有一个表达自动化设计的文档格式，真是遗憾**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/65/fbdf4fc1.jpg" width="30px"><span>羊羊</span> 👍（5） 💬（1）<div>测试报告的对象有：项目经理，不同测试部门的主管，测试流程的管理人员，再到具体的自动化测试人员。每个角色关注的内容都不同，设计report之前，需要收集不同角色的需求：
项目经理比较关心项目总的情况，希望看到每个版本迭代的历史曲线图，case数量的曲线，bug（还需要细化到bug等级）数量的曲线，每个版本case pass&#47;fail率的曲线等，
功能测试部门主要关注，case的自动化率，发现bug的数量，一轮regression的时间，自动化是否提高的regression的效率。
性能测试的报告，更是各式各样，要能看出版本迭代后的性能有没有下降。
测试流程的管理人员，要看每次regression的进度；自动化&#47;手工测试的进度；bug情况，有没有critical的bug，用于判断是否要终止这个版本的迭代。
case owner 就是要看详细的执行过程，log，截图，有些case还需要录屏。
以前我们是用Django开发的测试平台，case的信息从测试用例管理系统获取，自动化的数据从代码管理系统获取，然后在mysql中做关联。每次case的执行都会向mysql中插入一条执行的动态数据，动态数据中有case静态数据的ID。最后根据这些信息，用Django的template+bootstrap+datatable做report。report可以一层一层进去，直到最详细的日志信息。</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ed/c5/0d908da3.jpg" width="30px"><span>微笑的起点</span> 👍（1） 💬（1）<div>看了老师的课程，受益匪浅，结合github JobFramework深入学习和实践，但是com.sheng.jobframework.observer.ObserverSubscriber 这个类在github中没有，辛苦老师看下</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/e4/94b543c3.jpg" width="30px"><span>swordman</span> 👍（0） 💬（2）<div>这一讲的信息量很大，花了不少的时间阅读。有两个问题：1. 能否介绍一下JobRunner调用TestJobFile.xml的实现思路，如果能举一个例子，讲一下JobRunner调用TestJobFile.xml，完成selenium实体job的测试用例调用流程，就更好了。2.在“我们再把 Job 的设计态、运行态、结果态理一遍。通过下图，你会更清楚地看到这个数据采集到聚合的过程。”下面，漏了一个比较重要的图。</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/4c/ef1b0f05.jpg" width="30px"><span>Duxuebing</span> 👍（0） 💬（3）<div>看不懂，达不到这个境界吧</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-28</li><br/>
</ul>