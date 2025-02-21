你好，我是叶伟民。

开篇词里面我们提过，RAG是传统软件开发人员加入AI浪潮的最快之路，但是这条路里面又分三条小路。

第一条是最容易想到的，就是直接跳槽换一份RAG工作（比如做大模型应用开发），这条路成功率最小。第二条，就是在现有公司/团队里面开一个全新的RAG项目，这条路成功率高一点，但是还是有难度，这个方案我们下一章再探讨。

使用RAG改造自己所处的项目，这条路成功率最高，难度最小，因此我们安排在最前面讲解，也就是我们第一章要学习的实战案例——传统MIS系统的RAG改造。

今天这一讲，我们就先睹为快，看看传统MIS系统使用RAG改造前后的模样，同时搞定一些环境准备工作，方便我们把MIS系统乃至整个课程的配套代码运行起来。

## 用RAG改造传统MIS系统的收益

我们如果单纯出于自己想加入AI浪潮的私心，就想推进一个RAG改造项目，这样是很难获得上级或者客户等利益相关者同意的。我们必须要让他们看到改造系统所带来的收益，才可能让他们同意我们改造。

那么使用RAG改造传统MIS系统有什么收益呢？最直观的一个收益就是可以（大幅）减少用户的操作步骤和操作时间，提高用户的工作效率。

## 项目改造入手点

那么如何入手改造项目，才能减少用户的操作步骤和操作时间，提高用户的工作效率呢？我们先从日常最熟悉的查询操作说起。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（4） 💬（1）<div>第1讲打卡~
思考题：对于项目的RAG改造，可以采用渐进式迭代的方式，正如课程实例中的MIS系统，系统整体上可以仍然保留全部的原始功能，保证业务上可以正常使用。同时对系统按照优先级或业务模块进行划分，逐个进行RAG能力的升级，并增加适当的灰度、abTest、回滚等功能，保证系统的平滑升级。</div>2024-09-05</li><br/><li><img src="" width="30px"><span>Geek_003d7a</span> 👍（1） 💬（2）<div>请教一下老师，我目前是环境学院的研二学生，毕业方向是基于rag的##问答模型，然后发一篇中文核心，写一篇大论文，然后毕业，请问我可以选择这个课程吗</div>2024-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（1） 💬（1）<div>实战1的1-7节都看完了，在思考大模型在这个案例中起到了什么作用？我理解是将自然语言转化成程序语言，从而调用原有的服务端接口，并且将大模型返回结果进行封装后展示给用户。
在这个实战中，用户提问上下文算做外部知识，其他的就没了。</div>2024-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/UWpN1EIAJib8k5iaGISZD1PhjgKOL6I0q6pP8Dic6VEtnj42jzIfk9m89Lug2ROedc1LerrVIrtyVIthNMCq5rZDA/132" width="30px"><span>ティア（Erlin Ma）</span> 👍（1） 💬（1）<div>对于现有系统，使用原始界面和rag界面并存的方式，是个很好的选择。
到对于新系统，界面部分的开发和维护成本很高，应该提供展示交互过程的rag界面来解决自然语言单次输入的不完整问题。
同时，尽量复用系统和其它用户共享的样例以及用户自身成功操作记录，来提高单次输入的成功率。
还有就是功能粒度的调整，标准是输入难易度和操作流程的平衡。传统页面有的很重，需要适当拆分。
以上就是我参考mid journey的交互过程，正在实践的几点启发，欢迎大家讨论改进。</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/72/03/da1fcc81.jpg" width="30px"><span>overland</span> 👍（1） 💬（1）<div>请教下老师哈，对于这个传统MIS的改造，只是用RAG能力，后台怎么理解前台输入的自然语言呢，是不是有什么自然语言类似LLM模型的处理？这块不太懂</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（1） 💬（1）<div>老师请问对于Django完全不懂，是否影响这门课的学习？只对机器学习相关的库比较熟</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/22/a0ddf3ee.jpg" width="30px"><span>see</span> 👍（0） 💬（3）<div>老师，这一套代码，可以在mac上跑吗？</div>2024-09-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKawxntLfibLJD93j5Xib4dA0fLJ7xQaIRUSxTAFvvPb4TT9GMB3L4aaiaGibwA1OPH803HRsTNWuv1ug/132" width="30px"><span>杨阳</span> 👍（0） 💬（1）<div>改造后也是按照改造前一样的方式运行吗？</div>2024-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>恩 这才是python工程化包管理的正确姿势</div>2025-02-12</li><br/><li><img src="" width="30px"><span>Formater</span> 👍（0） 💬（0）<div>老师，示例代码中内嵌的JS代码无法从cdn.bootcdn.net下载，如何解决？</div>2024-12-11</li><br/>
</ul>