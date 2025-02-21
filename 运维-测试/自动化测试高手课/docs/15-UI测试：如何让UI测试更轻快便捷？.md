你好，我是柳胜。

恭喜你坚持到这里，我们顺着测试金字塔底层的单元测试一步步向上，现在终于到了金字塔顶部。按照我们的整体设计，其实脏活累活已经在底层干得差不多了。

爬上塔顶不容易，应该是一身轻松，纵览风光了。可以想象，如果没有前面的整体设计，没有单元测试来夯实基础，把测试工作全都压到端到端测试，它必然会垮掉。

不过，既然需要金字塔顶部这个UI测试层，一定是它不可替代，做得了其他层力所不能及的事儿。今天咱们就来梳理下UI测试要做什么，怎么做才能收割更高的ROI。

UI全名叫做User Interface，在当下，User这个概念已经被扩展，甚至被滥用，我倒觉得，UI叫做PI（People Interface）更为准确，专指和人格用户交互的界面。

从UI这个角度，主要有三个测试点需要去关注：第一，用户的行为；第二，UI的布局；第三是用户的易用性。当然，根据具体业务的需求，还有其他的点，比如Globalization全球化、Accessibility亲和力等等。

## 用户行为测试

用户的行为，指的是用户通过操作UI，获得他想要的功能。在FoodCome里，用户通过WebUI填好订单信息，然后点击“下订单”按钮，就能完成下单功能。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/e4/94b543c3.jpg" width="30px"><span>swordman</span> 👍（5） 💬（2）<div>分享一个亲身经历的UI测试案例，都是属于胖客户端：
1.Android客户端：未使用单元测试，单纯采用Appium做UI自动化测试，基于Appium做了二次封装，还采用了POM等多种技术手段，但测试效率的提升并不明显，稳定性也欠佳；
2.微信小程序：所有javascript的界面业务逻辑，都使用单元测试覆盖（jest框架）；在UI自动化方面，采用手工测试，仅验证页面跳转及典型业务场景串接（这些单元测试做不了）。测试效率明显提升，从版本上线情况看，质量保障的效果也很好。

虽然微信小程序的体量和复杂度，远无法和Android客户端相比，但可以总结出两点：1. UI测试中单元测试的重要性。2. 使用的自动化框架或技术再牛，也需要遵循背后的ROI规律。</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d8/8b/d81769bf.jpg" width="30px"><span>chin</span> 👍（1） 💬（1）<div>UI布局测试这块以前没有了解，学习一下</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/62/48045bee.jpg" width="30px"><span>Sarah</span> 👍（1） 💬（1）<div>有做单元测试
目前比较流行的前端单元测试框架是jest结合react testing library</div>2022-04-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoApjXQ0ib4MDEmAsChPIhHQemEOTIkT6OvSq8D99MIAYfq6dGhhPoHlfDIZtibiaIz3Zrc08ibKBTsCQ/132" width="30px"><span>阿萨聊测试</span> 👍（0） 💬（1）<div>关于UI自动化布局和界面测试运行时间过长，无法快速反馈质量。胜哥有没有高招？除了selenium grid</div>2022-04-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eperhqESS9OyTHeTvLrpE8HPPI3ZVdDQdYmZoQ7pKeaeicylcxuY0LjSBia0AqOjSEeicyHFSfYgViaNQ/132" width="30px"><span>jogholy</span> 👍（0） 💬（1）<div>老师您好，能不能推荐一些语音匹配测试的工具?我们有语音测试的需求。</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡
没做过前端测试</div>2024-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4k1x0lQm5iaSomncQia5hddWJ1HRA1QxciamRgYkJzuxo8R6OpeeWeZtmszYb6oUwiae8hMf1EDavjF4DBWdicaCjtia/132" width="30px"><span>Geek_eb7eec</span> 👍（0） 💬（0）<div>谢谢老师！非常有价值的内容！关于胖客户端，如果做Component testing，老师可以给一些建议和推荐一些学习资料吗？ 谢谢</div>2022-11-11</li><br/>
</ul>