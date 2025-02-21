你好，我是茹炳晟。今天我和你分享的主题是“测试先行：测试驱动开发（TDD）”。

通过上一篇文章，我们已经深入理解了什么是探索式测试，以及如何用探索式测试开展具体的测试。今天我这次分享的目的，就是和你聊聊软件测试领域中的另一个很热门的话题：测试驱动开发，也就是Test-Driven Development，通常简称为TDD。

听上去有些迷惑是不是？测试怎么可能驱动开发呢？在传统软件的开发流程中，软件开发人员先开发好功能代码，再针对这些功能设计测试用例、实现测试脚本，以此保证开发的这些功能的正确性和稳定性。那么，TDD从字面上理解就是要让测试先行，这又是怎么一回事呢？

确切地说，TDD并不是一门技术，而是一种开发理念。它的核心思想，是在开发人员实现功能代码前，先设计好测试用例的代码，然后再根据测试用例的代码编写产品的功能代码，最终目的是让开发前设计的测试用例代码都能够顺利执行通过。

这样对于开发人员来说，他就需要参与到这个功能的完整设计过程中，而不是凭自己想象去开发一个功能。他有一个非常明确的目标，就是要让提前设计的测试用例都可以顺利通过，为此，他先实现测试用例要求的功能，再通过不断修改和完善，让产品代码可以满足测试用例，可以说是“小而美”的开发过程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/11/39/f7dcc2e6.jpg" width="30px"><span>叶夏立</span> 👍（3） 💬（1）<div>tdd怎么样做才能落实到项目中，我觉得这才是核心问题，当然不是所有的项目都适合tdd。不知道茹老师是否能分享一下tdd落地推动的做法？</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/0a/2ac3417a.jpg" width="30px"><span>伪专家</span> 👍（2） 💬（2）<div>没有强的coding能力，不行的</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/f0/38db74c9.jpg" width="30px"><span>subona</span> 👍（1） 💬（2）<div>tdd测试代码都是单元测试了吧</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/a7/c4de1048.jpg" width="30px"><span>涅槃Ls</span> 👍（1） 💬（1）<div>打卡44，国庆节后 好好学习</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/9f/788b964e.jpg" width="30px"><span>仰望星空</span> 👍（1） 💬（1）<div>老师讲的很系统，每篇都听，几乎涵盖了测试的方方面面。有一点就是设计安全性方面的测试能否也讲一讲呢</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>您是不是把TDD、BDD、ATDD混在一起了😄</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/90/c4/99e6f7cb.jpg" width="30px"><span>~黑凤梨~</span> 👍（0） 💬（1）<div>我们WEB项目也在要求做TDD，并将TDD与现有的CICD（其实只有CD）结合，不知道具体如何来管理TDD的test case那些东西。希望老师指点一下，谢谢。</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/7d/50fc447e.jpg" width="30px"><span>秦浩然</span> 👍（51） 💬（10）<div>虽然 TDD 并不适合所有项目，但是将 TDD 思想放大到整个开发流程上，我总结了一套开发流程，请大家参考。

所有人员参与需求评审 -&gt; 测试人员编写测试用例 -&gt; 所有人员参与用例评审 -&gt; 开发人员按照测试用例进行编码 -&gt; 开发人员执行用例，进行自测，所有用例通过后 -&gt; 开发人员提测 -&gt; 测试人员进行测试。

其中的好处个人觉得主要有两点：
1. 在编码前完成测试用例，可减少开发中需求变更带来的风险。因为在写测试用例的时候，会对需求进行深度分析，思考需求是否合理，在我的经验中，测试组一定会发现不合理的需求，如果这些不合理的需求在编码前就被发现，后面返工的几率就小很多；
2. 在自测环节，开发人员保证所有用例都通过，可以减少测试环节的轮次。因为如果提测质量太差，会增加测试人员和开发人员沟通成本，如果一些基本问题能在自测环节解决，那测试人员会有更多精力放在探索性测试、压力测试、整体功能回归等测试中。

总而言之，如果能达到“缩短发布周期，提高发布质量”的目的，都是好方法。</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/b9/347e9704.jpg" width="30px"><span>刘海贤</span> 👍（4） 💬（3）<div>做到TDD这样的流程，目前国内我是不知道有哪些公司。另外，这样的研发改革，是不是开发可有可无了？因为实现这些功能测试同学都可以去完成了哈。。。</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/7d/50fc447e.jpg" width="30px"><span>秦浩然</span> 👍（3） 💬（1）<div>确实要考虑项目的适用性，如果对于试水项目、用户需求不确定的，就不太合适了。后期需求频繁变更的话，测试的维护成本也是很高的。</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/6d/25b6554f.jpg" width="30px"><span>a坚果</span> 👍（2） 💬（0）<div>有一本书就是《测试驱动开发》，老外写的，使用python需要，TDD的思想开发的一个项目，对这方面有需要了解和学习的可以去看看。
欢迎大家关注我的微信公众号「软件测试艺术」，一起交流，一起学习。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7a/7f/4bce9aff.jpg" width="30px"><span>东方不败之鸭梨</span> 👍（1） 💬（0）<div>感觉TDD是在需求和开发的代码之间介入，用测试用例代码来引导开发代码的实现</div>2021-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b8/35/65196a66.jpg" width="30px"><span>棱角</span> 👍（1） 💬（0）<div>这样会不会增加开发周期？在这个敏捷开发盛行的时代，tdd真的合适吗。开发人员或许会花更多时间去阅读用例。</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/4b/c09c60e6.jpg" width="30px"><span>Yin</span> 👍（1） 💬（0）<div>有一点不太理解，以文中计算距离下一次生日天数的例子来说，在我理解看来，所编写的测试代码也正是要实现的业务代码啊，有些困惑，岂不是测试干了开发的工作</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/3d/2fc84343.jpg" width="30px"><span>我是谁</span> 👍（1） 💬（0）<div>tdd感觉就是详细的单元测试，那对于测试用例的项目建立，包括持续集成，都是由测试来做。开发人员是不是就不需要写单元测试了，那开发自测用测试人员写的测试用例吗，是拉去测试这边项目吗</div>2019-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKYfcUOVhf3vhEBUNGHgtIcw8ujMZnkabicLzzjn3xwdeeic2PJSe7ibJgMx2UjF0d7L4B4gsRpaqe2A/132" width="30px"><span>郭小菜</span> 👍（1） 💬（0）<div>个人认为先写测试代码比较适合单一场景，如果是较为复杂业务场景先去写测试代码是很复杂的，测试代码的数量甚至多余系统代码</div>2018-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/be/723738df.jpg" width="30px"><span>喵呜呀呵嘿🌈</span> 👍（1） 💬（0）<div>测试人员的综合能力强于开发人员，感觉TDD会更好推行也适合使用。相反则不然吧。</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>成本真高</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（0）<div>测试用例是测试写吗？如果是的话，测试在写测试用例的时候，就把接口、pojo等等都定义好了，那开发岂不是只要实现就行。那这对测试的要求岂不是很高很高了。</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（0）<div>没经历过，学习啦</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/80/d1d9b493.jpg" width="30px"><span>宋琦</span> 👍（0） 💬（0）<div>要是能讲一讲如何在项目中落实BDD就更好了。
</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（0） 💬（0）<div>本文总计

### 什么是测试驱动开发（TDD）

TDD 并不是一门技术，而是一种开发理念

在实现功能代码前先设计好测试用例的代码

根据测试用例的代码编写产品的功能代码

让开发前设计的测试用例代码都能够顺利执行通过



### TDD 的优势

保证开发的功能符合需求

更加灵活的迭代方式

保证系统的可扩展性

更好的质量保证

测试用例即文档



### 测试驱动开发的实施过程

- 为需要实现的新功能添加一批测试

- 运行所有测试，看看新添加的测试是否失败

- 编写实现软件新功能的实现代码

- 再次运行所有的测试，看是否有测试失败

- 重构代码

- 重复以上步骤直到所有测试通过



**三个注意点**

需要控制测试用例的粒度

要注意代码的简洁和高效

通过重构保证代码的优雅和简洁</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/11/bdffffa6.jpg" width="30px"><span>派森</span> 👍（0） 💬（0）<div>感觉特别适合研发之间的交叉测试，测试驱动开发，并不是说测试人员驱动开发人员开发，这个测试用例也可以是研发写的，我理解有问题吗？</div>2021-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/85/e2/540b91fa.jpg" width="30px"><span>凯耐</span> 👍（0） 💬（0）<div>TDD对接口测试不适用，测试无法根据需求文档编写测试用例。TDD适用于UI层次的测试，可以根据需求文档编写测试用例，开发参与用例评审确保开发的功能符合测试用例的标准</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/90/d4/1fec25d2.jpg" width="30px"><span>Geek_sst</span> 👍（0） 💬（0）<div>我感觉有点像冒烟测试。只是它在完成代码前。  其实开发在完成自己大概的代码。再根据冒烟用例一样的可以的</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（0） 💬（1）<div>在开发不熟悉场景的时候，是不是可以由测试人员编写测试用例，然后提供给开发人员参考。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（0） 💬（1）<div>虽然说不是所有的项目都适合TDD，但是其实在开发的过程中是有运用TDD思想的，开发每次写一个分支判断，很可能就是针对一种场景或者一条用例，只是没有很正规地写出来，可能只是在大脑思考了一下，实现这个功能分哪几种情况，就动手敲代码。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/92/eaafff96.jpg" width="30px"><span>Amos</span> 👍（0） 💬（1）<div>老师你好，有一点不明白，BirthdayCaculator.caculate(String brithday) 该方法未实现之前，测试代码里面就包含了这个方法了吗？ 那怎么会测试通过的呢 ？ </div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ec/58/a8e35513.jpg" width="30px"><span>mingo</span> 👍（0） 💬（0）<div>我们写java单元测试时候都是需要注册到主测试类，这样每个人都改主测试类，提交不拼频繁，容易冲突，有没有好的团队写单元测试，避免冲突的方法？</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/ba/424be2c8.jpg" width="30px"><span>Geek_p79wqo</span> 👍（0） 💬（0）<div>TDD这件事情实话我觉得应该是在开发自己对业务更加了解的情况下来做，现在的情况下“测试”驱动开发的话之前需要定义好规则尤其在GUI测试上，相对来说接口也还好因为前置条件是后端开发出接口文档，那么这个就是测试依据，也就是说能够先出用例，然后上持续集成平台让开发自己上测试服务自己进行测试 。在通过所有用例以后基本上也就能快测试了。</div>2019-10-29</li><br/>
</ul>