你好，我是蒋宏伟。

上一讲我们说到，React/React Native 开启了“基于组件”构建应用的潮流。

在工作中，特别是业务类的开发需求，绝大多数都是写页面。写页面分为两步，第一步是搭建静态页面，第二步是给静态页面添加交互让它动起来。这第一步至关重要，它决定了 UI 设计稿要拆分成哪些组件，这些组件又是如何组织起来的，这些都会影响程序的可扩展性和可维护性，甚至还有团队的合作方法。

我们这一讲的目的，就是让你有一个正确的基于组件搭建静态页面的思路，不让第一步走偏。要知道，如果后面再去纠正，要花费的成本就大了去了。

## 组件：可组合、可复用的“拆稿”方式

在开始使用组件这种方式构建静态页面之前，请你先思考一个问题，为什么 React/React Native 选择了基于组件的架构方式呢？

理论上，除了组件这种方式外，常见的构建应用方式还有：类似 HTML/CSS/JavaScript 这种的分层架构、基于 MVC 的分层架构。那为什么 React/React Native 没有选择这两种架构方式呢？

**这是因为，基于组件的架构模式，或许是现在重展示、重交互应用的最好选择。**

记得我 2015 年刚入门的时候，还有一种岗位叫做网页重构工程师，我还面过这种岗位。那个时候，架构模式就是把 UI 设计稿拆成 3 层：HTML、CSS、JavaScript。网页重构工程师负责 HTML、CSS 部分，前端工程师负责 JavaScript 部分。但是后来我发现网页重构工程师这种岗位越来越少了，也庆幸自己没有上错车。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/3e/82b7deca.jpg" width="30px"><span>huangshan</span> 👍（8） 💬（2）<div>我之前写组件库的时候，是很坚持单一职责和OCP的，认为组件无状态灵活性很高。但是复杂组件经过组合和增强之后，感觉dom节点层数过多、数据流维护和状态更新成本变高。请问蒋老师对这一块有什么建议吗？</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/36/d6/343ab8c7.jpg" width="30px"><span>Asterisk</span> 👍（1） 💬（1）<div>应该讲一下clas风格组件和 function风格组件</div>2022-10-12</li><br/><li><img src="" width="30px"><span>Geek_ce9101</span> 👍（0） 💬（3）<div>你好，github 的项目我用安卓的没跑起来，有个疑问，package 里面并没有 install-android-hermes script，但 readme 里面却第一步就是：yarn install-android-hermes ？</div>2022-05-23</li><br/><li><img src="" width="30px"><span>Geek_51b2dc</span> 👍（1） 💬（0）<div>https:&#47;&#47;github.com&#47;facebook&#47;react-native&#47;issues&#47;33698 有同学搭建andriod环境的时候遇到这个问题 吗？怎么解决的能告知一下吗？</div>2022-07-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lAh4B90czPhrrEChF51akicyeasnDiaOlvEGibc0mPGhHtibJwzKVKwCEzuSlZK5sRvsniaszf3uKEyZUq4No3U4d8g/132" width="30px"><span>Geek_140294</span> 👍（0） 💬（0）<div>有没有环境搭建的内容啊？我跑项目都还跑不起来</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d7/f5/df6b6b60.jpg" width="30px"><span>angelajing</span> 👍（0） 💬（0）<div>因为我本地环境npm等各种软件包的版本和github上下载的代码版本不一致（参见package.json），需要适当的更新dependencies的版本信息。例如，
---- package.json-----
19  &quot;@apollo&#47;client&quot;:&quot;^3.5.6&quot;
--------------------
----- terminal ------
$ npm search @apollo&#47;client
@apollo&#47;client 3.8.7
------------------
命令行查看本地环境中 @apollo&#47;client包的版本是 3.8.7，所以把 package.json文件中相关包的版本改一下。所有包的版本都改好后，执行下面的命令。记得启动 device simulator。
------ terminal ----
$ npm install
$ npm start
-----------------</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/98/1491b4a3.jpg" width="30px"><span>kittyE</span> 👍（0） 💬（0）<div>MVC的数据流向是C(5, 2) * 2
优点是：代码颗粒度小
缺点是：数据流向复杂，组件越多可能的数据流向更多</div>2023-07-23</li><br/><li><img src="" width="30px"><span>Geek_ae84e1</span> 👍（0） 💬（0）<div>居然是音频课，大家要小心</div>2023-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/36/d6/343ab8c7.jpg" width="30px"><span>Asterisk</span> 👍（0） 💬（1）<div>确实只讲了一个思虑，我还需要再看看 https:&#47;&#47;reactjs.org&#47;docs&#47;components-and-props.html</div>2022-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJtSTXn4Da0luMYHFCricC9lJz5CeUTxLFibTp10uKbiaOq4IoFcZSOhB1qGMv51ZyXSWuSrlcal19mQ/132" width="30px"><span>Geek_b056e8</span> 👍（0） 💬（5）<div>我下载了课件，但是怎么才能运行Demo里不同章节的代码呀？</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/67/abb7bfe3.jpg" width="30px"><span>涂海生</span> 👍（0） 💬（1）<div>实战例子是否可以多来些</div>2022-06-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJtSTXn4Da0luMYHFCricC9lJz5CeUTxLFibTp10uKbiaOq4IoFcZSOhB1qGMv51ZyXSWuSrlcal19mQ/132" width="30px"><span>Geek_b056e8</span> 👍（0） 💬（2）<div>大神 由于我是刚学习RN，所以有个环境配置的问题想问一下。
 我这边按照官网的环境配置完成后。可以运行AwesomeProject 模版项目。
 但是从GitHub 上下的Demo工程 运行yarn android命令
一直报错：

error Failed to install the app. Make sure you have the Android development environment set up: https:&#47;&#47;reactnative.dev&#47;docs&#47;environment-setup.
Error: Command failed: .&#47;gradlew app:installDebug -PreactNativeDevServerPort=8081

 info Run CLI with --verbose flag for more details.
error Command failed with exit code 1.
info Visit https:&#47;&#47;yarnpkg.com&#47;en&#47;docs&#47;cli&#47;run for documentation about this command.

这是什么原因呀？</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/e7/646bd9f1.jpg" width="30px"><span>worm</span> 👍（0） 💬（2）<div>老师您好，registerComponent() 第二个参数为什么设计为传入一个函数(ComponentProvider)？这样比设计为直接传入 Component 的好处是什么呢？ 
</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/23/73af9e5c.jpg" width="30px"><span>山丘smith18651579836</span> 👍（0） 💬（2）<div>ProductTable.js中不需要通过数组的map函数来循环生成生成列表吗？</div>2022-04-01</li><br/>
</ul>