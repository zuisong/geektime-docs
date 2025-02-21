你好，我是王沛。今天这节课我们来学习如何对 Hooks 进行单元测试。

在课程的一开始，我想首先强调一下单元测试的重要性。因为我发现很多同学在实现业务功能的时候，干劲十足，非常感兴趣。但是一旦要去写测试用例，就顿时觉得枯燥和无趣。

产生这种现象的原因，正是因为**没有意识到测试的重要性**，以及测试能给你带来的好处。要知道，最终应用的质量和稳定性在很大程度上决定着项目的成败，而**为了保证软件的质量，唯一的途径其实就是测试**。

当然，测试带来的好处不仅体现在能够保证最终发布的应用的质量，更为重要的是，它能\*\*让你在开发新功能，或者修复 Bug 时，**对自己做的改动更有信心**。只要有足够的测试覆盖率，那么你就不用太担心自己的改动可能会破坏已有的功能。同时，单元测试还能够帮助你在开发过程中，更好地组织代码，追求模块的松耦合。

因为如果你时刻有意识地去思考自己的每一段代码该如何去测试，那么在实现代码时，就会自觉地去做模块的隔离，反过来提升了代码的质量。这也是为什么很多团队会推崇测试驱动开发的原因。

好了，测试的重要性就不多说了。接下来我们就进入正题，看看对于自定义Hooks，应该怎么进行单元测试。课程的学习目标仍然是以总体把握为目标，更多地还是思考测试代码是如何运行的，以及测试框架提供了哪些能力帮助我们运行单元测试。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>GK</span> 👍（9） 💬（1）<div>请问如何在业务项目中推动单元测试的落地，大家都觉得单元测试重要，可最终都输给了业务的忙碌。</div>2021-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/11/fc/80256cc8.jpg" width="30px"><span>心若水，则长安</span> 👍（4） 💬（1）<div>我司的服务端要求单测覆盖率100%，但前端可以说几乎没有写单测的先例，如何系统性的学习前端单测这方面的知识呢？需要了解哪些东西</div>2021-07-31</li><br/><li><img src="" width="30px"><span>QL</span> 👍（1） 💬（1）<div>根据我的理解，react hook和redux它们似乎都推荐函数式用法，
在实际业务模块开发中，因为封装的需要，我们可能会去封装一些模块类，或工具类，
不知道在你们的实践过程中，对于前端开发，
你们的单元测试更多的是在写类的单元测试还是在写函数的单元测试？
什么情况下推荐将方法封装成类，什么情况下直接以纯函数的方式调用更佳？</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/03/86/c9051c6a.jpg" width="30px"><span>Bug般的存在</span> 👍（26） 💬（1）<div>道理我都懂，但就是不想写，测试代码比业务代码还多，看着都累。。。</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/5c/f5f24221.jpg" width="30px"><span>发芽的紫菜</span> 👍（13） 💬（0）<div>如果要求写单元测试，那是不是在开发前，也要把写单元测试的工作量规划进去？还有后续维护单元测试的工作量？我司目前只是自测+测试来测，感觉业务都写完，根本不可能给多的时间专门让你来写单元测试的</div>2021-07-06</li><br/><li><img src="" width="30px"><span>Geek_4116d8</span> 👍（3） 💬（1）<div>把工作留给测试，增加社会就业岗位。</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/4b/36396a18.jpg" width="30px"><span>独钓寒江雪</span> 👍（3） 💬（0）<div>从示例来看，act之后马上进行同步断言，那么，act是如何保证在回调函数执行完成后，还会等 React 组件的生命周期都执行完毕的呢？</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/23/1cc7d190.jpg" width="30px"><span>Brave</span> 👍（1） 💬（0）<div>hook只能在函数组件或者自定义hook中使用，因此这里的callback函数应该是被当做自定义hook调用的</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/32/43595745.jpg" width="30px"><span>鲁滨逊</span> 👍（0） 💬（1）<div>renderHook内部难道还生成了 wrapper 节点，然后返回节点的 ref ? 为什么要这样做呢 ？ 直接像第二种写法一样，返回 Hook 的结果不是很简易吗？</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（0） 💬（2）<div>老师我有个问题，就是项目使用 create-react-app 创建的，当我在根目录 tests 目录下，创建一个 xxx.test.js ，我试图通过绝对路径引用一个组件 InputNumber，对它进行测试：

```
import InputNumber from &quot;src&#47;components&#47;InputNumber&quot;;
```

这时候 npm run test 就会报错：

```
 FAIL  tests&#47;InputNumber.test.js
  ● Test suite failed to run

    Cannot find module &#39;src&#47;components&#47;InputNumber&#39; from &#39;tests&#47;InputNumber.test.js&#39;
```

绝对路径 src 我配置了，在 App.js 能够使用的。


想问 xxx.test.js 是不是不能使用绝对路径，只能相对路径引用，如果相对路径引用，这好麻烦。</div>2021-08-26</li><br/>
</ul>