你好，我是柳胜。

说起交付流水线，你可能立马想到的是Jenkins或CloudBees这些工具，它们实现了从Code Build到最终部署到Production环境的全过程。

但Jenkins只是工具，一个Pipeline到底需要多少个Job，每个Job都是什么样的，这些问题Jenkins是回答不了的，需要使用工具的工程师去思考去设计。在实践中，通常是DevOps工程师来做这个设计。

既然我们学习了微测试Job模型，也知道了它能帮助我们去做自动化测试设计，那用这个模型，能不能帮我们做Pipeline设计呢？**其实，Pipeline本质上也是一个自动化测试方案，只不过它解决的场景是把软件从代码端到生产端的自动化。**

掌握设计思维是测试工程师向测试架构师的必由之路，假设今天你需要设计一个Pipeline，把一个Example Service的代码，最终部署成为生产环境的一个服务进程。完成这个工作，你不仅能弄明白CICD的原理和实现，而且对自动化测试Job怎么集成到CICD，也将了如指掌。

![图片](https://static001.geekbang.org/resource/image/fc/bd/fc734fc77fcac6773de057d5d7437dbd.jpg?wh=1920x791)

## Example Service的Pipeline的目标

还是按照Job模型的设计原则，先理出Pipleline的第一个根Job。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/e7/25f01030.jpg" width="30px"><span>Rachel</span> 👍（1） 💬（1）<div>为啥我感觉老师说的这个job模式的pipline和我们实际实施的持续交付的pipline一样呢？但是理论好像有差别，没太分辨清楚他们的关系</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/65/fbdf4fc1.jpg" width="30px"><span>羊羊</span> 👍（0） 💬（1）<div>以前公司的CI流水线是3个团队共同完成的，每个团队负责一个大的Job，每个Job通过rest api来通信。一个Job完成之后，会通过rest api发送下一个job需要的信息，来激活下流job。但是实践中，总是会遇到各种问题，使pipeline中断，希望老师能分享一些，能让pipeline更加稳定的经验。</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/42/238dd211.jpg" width="30px"><span>孙中原</span> 👍（0） 💬（1）<div>感谢老师的分享。这里我有一个问题，像我们这边设计ci pipeline的时候，是以制品的视角来设计，描述了一个制品从被开发者提交到最终上线，质量等级不断提升的过程。您的Job设计，是以需求的角度来设计的。那么，Job树怎么与CI pipeline结合呢？</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/e4/94b543c3.jpg" width="30px"><span>swordman</span> 👍（0） 💬（1）<div>原先我们jenkins pipeline的设计比较low，直接在绘图工具或纸上，绘制stage，然后就开工写代码了。当pipeline脚本越来越多，参与编写的人也越来越多时，脚本非常难维护，也很难做Review，这估计就是没有设计带来的“附属品”。

今天终于知道pipeline的设计方法了，可以解决以上的痛点，接下来，就是将它用于实践！</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c7/7f/c2b5f1f2.jpg" width="30px"><span>。。。</span> 👍（0） 💬（1）<div>这个git地址登不进去呀</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-02-26</li><br/>
</ul>