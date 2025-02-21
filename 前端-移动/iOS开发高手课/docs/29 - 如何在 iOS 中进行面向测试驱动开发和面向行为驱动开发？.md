你好，我是戴铭。今天，我要和你分享的话题是，如何在 iOS 中进行面向测试驱动开发和面向行为驱动开发。

每当你编写完代码后，都会编译看看运行结果是否符合预期。如果这段代码的影响范围小，你很容易就能看出结果是否符合预期，而如果验证的结果是不符合预期，那么你就会检查刚才编写的代码是否有问题。

但是，如果这段代码的影响范围比较大，这时需要检查的地方就会非常多，相应地，人工检查的时间成本也会非常大。特别是团队成员多、工程代码量大时，判断这段代码的影响面都需要耗费很多时间。那么，每次编写完代码，先判断它的影响面，然后再手动编译进行检查的开发方式，效率就非常低了，会浪费大量时间。

虽说一般公司都会有专门的测试团队对产品进行大量测试，但是如果不能在开发阶段及时发现问题，当各团队代码集成到一起，把所有问题都堆积到测试阶段去发现、解决，就会浪费大量的沟通时间，不光是开发同学和测试同学之间的沟通时间，还有开发团队之间的沟通时间也会呈指数级增加。

那么，有没有什么好的开发方式，能够提高在编写代码后及时检验结果的效率呢？

所谓好的开发方式，就是开发、测试同步进行，尽早发现问题。从测试范围和开发模式的角度，我们还可以把这种开发模式细分出更多类型。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVegfjqa0gM4hcRrBhZkIf7Uc5oeTMYsg6o5pd76IQlUoIIh2ic6P22xVEFtRnAzjyLtiaPVstkKug/132" width="30px"><span>xilie</span> 👍（17） 💬（0）<div>看到这个 “正在手淘推动BDD😄” 就放心了，原来大家都不做单元测试的哈</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/51/870a6fcb.jpg" width="30px"><span>Trust me ҉҉҉҉҉҉҉❀</span> 👍（15） 💬（3）<div>正在手淘推动BDD😄</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/be/970590a0.jpg" width="30px"><span>故胤道长</span> 👍（7） 💬（0）<div>戴老师讲得非常全面。我个人认为TDD最大的问题是只关注单个功能的正确性，却无法保证设计上的性能。从整体设计角度来看TDD并没有促进作用。</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1b/40/68e59e53.jpg" width="30px"><span>小万叔叔</span> 👍（7） 💬（0）<div>没有采用TDD或BDD的原因： 一来很多业务迭代的比较快，没有时间是一个原因。 二来，能够TDD是建立在编写TDD的场景足够，也就是能模拟细粒度模块的外围环境，对于小项目而言想要的往往就是快速出产品，一开始就关注细粒度模块化的很少，对于大项目，受历史原因业务之间的强耦合导致很难去构建Mock场景。 挺赞同从基础模块和对外的 SDK 结合业务的发展去编写TDD可能更合适。
</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3f/d0/5bd853ea.jpg" width="30px"><span>赶紧学起来</span> 👍（4） 💬（0）<div>大都不用TDD&#47;BDD，觉得原因有三
1、 流程不够规范
2、迭代快时间紧
3、开发完给测试</div>2019-05-28</li><br/><li><img src="" width="30px"><span>不知名的iOS网友</span> 👍（4） 💬（0）<div>课程一些笔记：https:&#47;&#47;github.com&#47;CrusherWu&#47;iOSRoadMap</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/e9/6c5191ea.jpg" width="30px"><span>时间都去哪了</span> 👍（3） 💬（1）<div>TDD,OC有什么好用的推荐框架吗?</div>2019-05-16</li><br/><li><img src="" width="30px"><span>文培定</span> 👍（1） 💬（0）<div>一直在小公司待，发现我这TDD都是相反的，一般都是先开发，后写测试用例。而对于BDD，一般涉及到纯逻辑的东西，例如某种算法的实现，才会去写测试code，因为有时候也不确定自己的算法是否写对了。</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/05/b2776d73.jpg" width="30px"><span>Geek</span> 👍（1） 💬（0）<div>感觉内容高大上，和我们小公司不沾边，不过作为了解内容，还是不错的，感谢大神</div>2019-05-27</li><br/><li><img src="" width="30px"><span>程序员讲道理</span> 👍（0） 💬（0）<div>无论是 TDD、TDD，测试逻辑还是有办法可以做，但是可能需要做好分层，mock数据啥的。但是测试视图目前比较困难，比较好的实践就是 FB 的 iOSSnapshotTest</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/42/2b6313ec.jpg" width="30px"><span>Tiger Nong</span> 👍（0） 💬（0）<div>戴老师，如果这个UI是在SDK中的话，好像是获取不到控件的。还有可以将一些mock这块的东西吗？</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（0） 💬（0）<div>很多情況都是一開始都想說先實現幾項功能再補測試，然後就一直補一直寫，要避免這樣的情況最好使用 TDD &#47; BDD 同步測試代碼，確保整體質量，也管理測試用例。也為 CI 做好充足的準備。</div>2019-05-16</li><br/>
</ul>