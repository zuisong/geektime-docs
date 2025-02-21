你好，我是Barry。

上节课我们一起学习了数据中心的数据业务需求、数据采集逻辑和数据呈现效果。在数据分析呈现的时候，我们用到了很多数据可视化的组件，有了这些组件，就能让我们轻松地实现数据可视化，直观展示出我们想要的分析结果，而且能帮用户清晰地看到数据间的关系。

其实在我们实际项目开发中，数据可视化的应用是非常多的。因此，如何熟练应用数据可视化组件，也是我们在日常开发中的一项必备技能，这样会让我们技术栈更加完善。这节课，我们就一起来认识学习应用一款轻量级数据可视化组件库——ECharts。

## 认识ECharts

我们先来认识一下ECharts，ECharts是一款基于JavaScript的数据可视化图表库。ECharts由百度团队开源，在2018年初捐赠给Apache基金会，成为ASF孵化级项目。

2021年1月，Apache基金会宣布 ECharts项目正式成为Apache顶级项目。同样在2021年1月，ECharts 5正式发布上线，在这个过程中ECharts不断地更新迭代，满足用户对数据可视化的各类需求。

提到前端可视化图表库，热度最高、也最常用的两个库就是D3.js和ECharts了，我们在课程中使用的也是ECharts。那为什么不选D3.js呢？这里我们简单分析一下，也让你有一个全面的了解。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：安卓端canva与HTML、CSS、Js有关吗？
老师的回答：“在安卓端，Canva则采用了完整的前端框架技术，包括HTML模板、JavaScript代码、组件等” 。我不确定。不过我感觉很惊讶，我潜意识里认为安卓的canva和这些没有关系，应该是利用底层绘制原理完成绘制的。我再搜搜。
Q2：Vue文件是被谁解析的？是VSCode自带的编译器解析的吗？ 还是Node解析的？
Q3：ECharts支持canvas、SVG等，那具体选哪个？是ECharts自主选择吗？
Q4：npm用来安装包，假如不需要安装，vue还需要node吗？
Q5：ECharts与node有关吗？与vue有关吗？</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/16/b525a71d.jpg" width="30px"><span>zgy</span> 👍（0） 💬（1）<div>搞反了吧，canvas 能兼容 IE6 吗？https:&#47;&#47;caniuse.com&#47;?search=canvas</div>2023-09-21</li><br/>
</ul>