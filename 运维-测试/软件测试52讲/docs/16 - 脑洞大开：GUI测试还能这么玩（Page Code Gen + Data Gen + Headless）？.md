在前面的几篇文章中，我介绍了GUI自动化测试的数据驱动测试、页面对象（Page Object）模型、业务流程封装，以及测试数据相关的内容。

今天这篇文章，我将从页面对象自动生成、GUI测试数据自动生成、无头浏览器三个方面展开，这也是GUI测试中三个比较有意思的知识点。

## 页面对象自动生成

在前面的文章中，我已经介绍过页面对象（Page Object）模型的概念。页面对象模型，是以Web页面为单位来封装页面上的控件以及控件的部分操作，而测试用例基于页面对象完成具体操作。最典型的模式就是：XXXPage.YYYComponent.ZZZOperation。

基于页面对象模型的伪代码示例，如图1所示。

![](https://static001.geekbang.org/resource/image/8f/df/8f49888b1fbae32994f3e4f8c5e77adf.png?wh=1058%2A424)

图1 基于页面对象模型的伪代码示例

如果你在实际项目中已经用过页面对象模型，你会发现开发和维护页面对象的类（Page Class），是一件很耗费时间和体力的事儿。

- 你需要打开页面，识别出可以唯一确定某元素的属性或者属性集合，然后把它们写到Page Class里，比如图1的第2行代码username\_input=findElementByName(“username”)，就是通过控件的名字（username）来定位元素的。
- 更糟糕的是，GUI的页面会经常变动，如果开发人员开发前端代码时没有严格遵循可测试性的要求，Page Class的维护成本就会更高。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/e5/66f38361.jpg" width="30px"><span>Geek_84a77e</span> 👍（26） 💬（1）<div>老师，是每篇文章有时间限制吗？可否细致的讲解一下，如何自动化生成页面对象，如何自动化生成测试数据？我们现在的理解很大部分是停留在概念上，来这儿学习的理由也是老师能够给我们一个直观的认识关于这些技术，或者每篇文章能否提供个链接供我们看看源码，切身体验一下封装等其他文章中提到的技术，多谢</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（24） 💬（2）<div>1.如果使用 selenium + xpath，应该可以解决大部分的控件识别，chrome 支持右键一键拷贝 xpath，贼方便；
2.关于测试数据的自动生成，个人感觉目前测试中，场景测试重要性是最高的，但是自动生成可能解决不了场景覆盖的问题，不过如果借鉴最新的机器学习算法，说不定有新发现；
3.对于无头浏览器，我的疑问是，既然是 GUI 测试，无头浏览器怎么保证测试效果的可靠性呢，测试结果是和常规浏览器一样可信么？毕竟自动化的目的还是为了测试，而不是为了自动。
欢迎沟通交流，公众号「sylan215」</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/71/3c/adf514f7.jpg" width="30px"><span>猪猪</span> 👍（7） 💬（1）<div>老师讲一下如何自动生成页面模型的原理，不要一带而过</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/84/7f584cb2.jpg" width="30px"><span>杜艳</span> 👍（5） 💬（1）<div>建议可以不可以不要伪代码。写一个真实可用的java代码</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2c/3a/5504ed70.jpg" width="30px"><span>kaiserin</span> 👍（2） 💬（1）<div>Katalon Studio现在的普及率怎么样？感觉大多数人还是用的robotframework</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cc/9c/ec71155f.jpg" width="30px"><span>胖虫子</span> 👍（1） 💬（1）<div>为什么大家用类似katalon这样的工具热情不高，但自己去写自动化框架的热情高</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/c6/35cc7c7c.jpg" width="30px"><span>Robert小七</span> 👍（1） 💬（1）<div>企业实战中，无头浏览器的应用程度如何？是否可以用多线程来替代grid集群
</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/72/8f77ddb0.jpg" width="30px"><span>johnny</span> 👍（0） 💬（1）<div>老师，希望能在git提供部分章节的代码实现。比如第14节的内容看完还是只停留在概念，如果有示例代码就比较方便理解</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/17/a2d9d515.jpg" width="30px"><span>星</span> 👍（0） 💬（1）<div>如何生成页面对象？</div>2018-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cc/1c/069b7e96.jpg" width="30px"><span>橄榄</span> 👍（0） 💬（1）<div>没有实际应用过</div>2018-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibnibklicJqGJ18L2iaiaP4k3bYbianW2Ka8s1Ck5Oxic9BNia2S5Y9TndSHkv9dSmBIwiaamYo79ENeOXbfCZkRgl0AmTg/132" width="30px"><span>凌焱洋</span> 👍（9） 💬（0）<div>关于使用selenium+xpath做web自动化的，我觉得可能大家都觉得直接使用Chrome  copy xpath会很方便，但是从长远来看，copy的xpath绝大多数是绝对路径，当开发在界面加一层封装或者换个位置就很容易定位失败，还是自己写，通过轴定位会节省后期的维护成本</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/f0/38db74c9.jpg" width="30px"><span>subona</span> 👍（3） 💬（0）<div>希望老师能深入地讲解下怎么去做，感觉这几节课都是概念性的知识点，太表面了。听完对于怎样运用到项目中，把工作做得更好没有太多帮助</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/15/49acb5cc.jpg" width="30px"><span>我的summer</span> 👍（3） 💬（0）<div>GUI测试数据的自动生成中第二种情况，可以使用PICT小工具。使用一定限制条件对笛卡尔积结果筛选出已经剔除的部分组合，然后再人工确认，可以提高一些些效率</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/99/95b36e98.jpg" width="30px"><span>【涛涛】不绝</span> 👍（1） 💬（0）<div>katalon开始收费了，可以弃了，用久了缺点也是蛮多的</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/26/154f9578.jpg" width="30px"><span>口水窝</span> 👍（1） 💬（0）<div>没有深入实践自动化测试，更无从谈起提高测试效率。</div>2019-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FGeCDgpXdhsXseIGF3GCzZibDJlOfO4KDqPJkMra2e0TJj3QVQk4t1oEd1BuQPtYOeavFyYxicd5fTZ33tIbPOZQ/132" width="30px"><span>付晓杰</span> 👍（0） 💬（0）<div>1.页面对象自动生成
商用自动化工具，比如 UFT；目前国内应用还不算多、免费的 Katalon Studio。
2.GUI 测试数据自动生成
3.无头浏览器页面对象自动生成
PhantomJS 的创建者 Ariya Hidayat 停止了它的后续维护，Headless Chrome 成了无头浏览器的首选方案。</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（0）<div>这门课都出了四年了，我才刚知道无头浏览器…</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e1/15/c9ec6fb0.jpg" width="30px"><span>于艳美</span> 👍（0） 💬（0）<div>最近有没有新的页面对象自动生成的工具 
</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/88/5f/31aa3141.jpg" width="30px"><span>歆雪</span> 👍（0） 💬（0）<div>1.自动生成页面对象，个人感觉还是半自动的，因为需要手动去操作页面，然后工具才会录制操作的元素及元素事件，对于熟悉xpath语法，且只有部分页面元素发生变化的情况下，直接写比录制感觉更方便。
2.自动生成测试数据，感觉对于一些文本框，边界值这种很有参考建议，开拓思路了，谢谢！
3.无头浏览器第一次听说，不知道对于一些需要一段时间才能加载好的元素的操作是否会有影响？如果可用，感觉可以省很多执行机</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（0） 💬（0）<div>老师文章中提到的“依赖于数据的动态页面对象”，不大理解。

自动生成页面对象，是会自动生成页面全部的对象吧，其实有些对象并不需要。

GUI 测试数据自动生成，这是新接触的知识。这方面有什么开源的工具可以自动生成测试数据吗？</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>无头浏览器真炫酷！一直头疼的问题解决了。十分感谢！</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/25/ef7330de.jpg" width="30px"><span>叶子</span> 👍（0） 💬（0）<div>都2019了不知道是否还能收到老师的回复
比较好奇一个问题 关于页面对象自动生成中的版本管理   工具如何识别两个版本间对象的关联性？例如版本1中有个对象A，在版本2中这个对象变更为对象B了，那么工具如何识别到原来调用对象A的地方现在应该调用对象B?</div>2019-12-18</li><br/><li><img src="" width="30px"><span>Geek_007</span> 👍（0） 💬（0）<div>你好 请问关于GUI测试 还有一些桌面应用软件（非浏览器），应该怎么来做自动化测试呢？</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>1，＂无头浏览器＂、＂页面对象自动生成＂，以及 ＂GUI 测试数据自动生成＂这三个技术现在在企业中用得多吗？
2、＂selenium for Java中的htmlunit是不是属于无头浏览器？</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c6/8e/48287140.jpg" width="30px"><span>欧晓鸥</span> 👍（0） 💬（0）<div>关于数据自动化生成有例子吗？</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c6/8e/48287140.jpg" width="30px"><span>欧晓鸥</span> 👍（0） 💬（0）<div>对于一个即将被替代的项目，要做自动化，覆盖率是最主要的吗？</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cb/bc/fe68899c.jpg" width="30px"><span>雪哥</span> 👍（0） 💬（0）<div>茹老师，请问自己实现页面元素自动生成，一般用什么技术，指点一下大概方向就可以</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/82/5cb984b5.jpg" width="30px"><span>soul</span> 👍（0） 💬（0）<div>Katalon Studio 已经操作 不错</div>2018-08-04</li><br/>
</ul>