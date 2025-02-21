你好，我是林世洪。2011年我加入京东，负责京东零售供应链研发架构工作，基于这些年我在京东的探索，我们来聊聊大型研发团队的 AOM 实践，这个话题或许听上去和团队管理的关系不大，但从我的实践角度看，它在团队效率、团队协作上都发挥了重要的作用，希望对你有帮助。

## 什么是AOM？

为了帮助你理解，在介绍 AOM 之前，我们先来看另一个你比较熟悉的概念 AOP，Aspect Oriented Programming，面向切面编程。利用 AOP 我们可以对业务逻辑的各个部分进行隔离，从而降低业务逻辑各个部分之间的耦合度，提高程序的可复用性，同时提高开发效率。AOM 和 AOP 有异曲同工之妙。

AOM 的全称是 Aspect-Oriented management，面向方面的管理。在软件开发过程管理中，需要对开发过程中的多个“切面”进行管理，即 AOM。**AOM的主要目的是把握质量，提高效率**，例如在进入开发前加入需求评审，在编码前加入方案设计指导、方案设计与评审，代码交付前加入代码评审等等。

![图片](https://static001.geekbang.org/resource/image/0e/9e/0e579029d2575409d84412d83b2c519e.png?wh=1920x713)

在不少大型开发团队中，开始设置专门的角色进行切面管理，这个角色大都是架构师来担任，有的公司甚至设置专门团队来管理，一般是横向架构团队。通过纵横交错的矩阵式组织架构，就可以在保障项目交付的同时，在各个环节以切面的形式保障质量及效率，让各个团队更加专注，而且整个架构的扩展性也非常强。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（1） 💬（0）<div>在长期架构上不能妥协，不过在具体实现业务上可以妥协，我不一定要做很多输出，但每个输出都是其他业务方紧急且重要的事情。有点考验老师傅的平衡之术了。</div>2022-12-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erms9qcIFYZ4npgLYPu1QgxQyaXcj64ZBicNVeBRWcYUpCZ9p0BGsrEcX8heibMLCV4Gde4P9pf7PjA/132" width="30px"><span>yanger2004</span> 👍（0） 💬（0）<div>上升到组织战略，和绩效挂钩。由虚拟团队出面更合适，因为虚拟团队对业务痛点更加了解。</div>2022-12-27</li><br/>
</ul>