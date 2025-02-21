你好，我是何辉，很高兴能在这门Dubbo实战进阶课中和你相遇。

先自我介绍一下，我是一名擅长用Java / Python / Go封装插件或工具来解决通用性问题的一线架构师，也曾因为解决通用性问题先后申请了五十余项国家专利。

解决问题这件事，一直以来，我比较信奉爱因斯坦的一句话：“你无法在制造问题的同一思维层次上解决这个问题”。所以，既然能解决，我们要么依靠经验技巧，要么依靠方法流程、科学原理，或者是依靠哲学理念。

而问题，始终都会有的。对于Dubbo来说，每当我带领团队成员设计功能、代码编写、问题排查时，经常被问到：

- 我该怎么快速掌握Dubbo框架体系？
- Dubbo的知识点我都看了，为什么在实际应用的时候就想不到呢？
- 某些Dubbo特性我也知道，但是为什么需要有这样特性的存在？
- 看到Dubbo各种底层报错，如何根据问题反推用哪些特性来解决呢？

这些问题，你一定或多或少疑惑过。为了找到自己心中想要的答案，相信你也曾试图把Dubbo框架的代码翻个遍，**但随着时间的流逝，你还能记住多少，又或者说你理解了多少？这也是我当时学Dubbo的困境。**

因为Dubbo的学习说复杂也复杂，说简单也简单。

随着微服务的流行，现在好多项目要么起步就是微服务，要么就是在转微服务的过程中，但市场上微服务的框架为数不多，而属于Java开发的框架更加凤毛麟角了，Dubbo框架，恰巧就是其中一款。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL2N4mhzsvvUG8Wew1uvTHs531fsW5LfgWkv4782VtwRuMf0qicRPxWtKgIzxyFSNVKJ09FN5vcVjg/132" width="30px"><span>Geek_895efd</span> 👍（7） 💬（2）<div>对目前微服务框架的迷惑，期待老师答疑：
1、目前的微服务框架：springCloud体系、阿里的springCloudAlibaba体系、以dubbo为主的微服务框架
2、对微服务框架的疑惑点一：国内主流微服务栈基本是springCloudAlibaba，我看阿里官方的描述，dubbo也是springCloudAlibaba的组成部分，那dubbo现在也有服务治理能力，是可以替代springCloudAlibaba吗
3、对微服务框架的疑惑点二：springCloudAlibaba技术栈包括nacos、springCloud gateway、sentinel、Sleuth、Seata等，那末duboo微服务治理包括哪些，还是说跟pringCloudAlibaba是重叠的
4、对微服务框架的疑惑点三：springCloudAlibaba、dubbo各自的定位是什么
5、对微服务框架的疑惑点四：springCloudAlibaba、dubbo各自的使用场景是什么


期待老师的答疑：不然，课程学下来，学的目的都不知道是什么</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/b8/31c7e110.jpg" width="30px"><span>LVM_23</span> 👍（5） 💬（2）<div>老师，Dubbo我在其他地方看说是RPC框架，当前文中说是微服务框架。没理解好，求解惑，谢谢</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/bd/c1/992f6724.jpg" width="30px"><span>Andy</span> 👍（3） 💬（1）<div>看了《开篇词》，可以看出这是老师对于学习之“道”、解决之“道”的干货分享，我是先大致浏览了一下，发现有很多细节点，也就是一些思维，非常重要，也很契合我之前所想的，比如“问题驱动学习”、“卷面试”、“凡是理解的都会记住，凡是不理解的都会忘记”，而后，又重新精读了一遍。

整篇写得非常诚恳，也很务实，可以说，是一切后续学习实践的真正前提，所谓“工欲善其事，必先利其器”。方向和方法对了，接下来只是行动就完了。很多人总想一下子扎进知识干货的海洋里，熟不知海洋里不会游泳，是会淹死的。正如那句古话所言“吾生也有涯，而知也无涯，以有涯随无涯，殆己”。

希望，想要学习任何知识，想要收获真正解决问题的能力的同学，应该好好先看看这篇开篇词。</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（2） 💬（1）<div>赶上热乎的了。16年底开始用dubbo，不过后面通知不会维护了，加上换了公司，就开始用spring-cloud。现在所在的家公司又在用dubbo，再捡回来。</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（2） 💬（1）<div>Dubbo  源码篇是按3.0 以版解讲 ？Dubbo 确实非常优秀的，和Spring Cloud 相比缺少一定生态技术环境</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（2） 💬（1）<div>我是第一?</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>老师的课程不仅内容质量高，还很励志~</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/fd/45e90d04.jpg" width="30px"><span>Casin</span> 👍（1） 💬（1）<div>加油跟着老师一起学</div>2022-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6d/91/9745cf49.jpg" width="30px"><span>小天</span> 👍（1） 💬（1）<div>工作里一直有用到Dubbo，但也就只知道怎么用。希望能通过学习了解更多</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>目标是用 Dubbo 横着走</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（1） 💬（1）<div>最近在看dubbo的源码，希望这个课程可以从不同角度的有收获</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/29/c1/f7a3888a.jpg" width="30px"><span>胖虎</span> 👍（1） 💬（1）<div>加油！跟着老师学习</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/db/d6/cd266a84.jpg" width="30px"><span>Berton 👻</span> 👍（1） 💬（1）<div>希望能有所收获</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/5e/d1f78004.jpg" width="30px"><span>豪</span> 👍（1） 💬（1）<div>跟着老师一起学习</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/83/cf789e0e.jpg" width="30px"><span>慕华</span> 👍（0） 💬（1）<div>解决通用问题的代码，怎么生气专利</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/ae/66ae403d.jpg" width="30px"><span>熊猫</span> 👍（0） 💬（2）<div>老师，你好，不同版本的dubbo框架混用会有什么坑吗？如2. x.x和3. x. x版本的dubbo</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c2/94/441ad37f.jpg" width="30px"><span>夜尽天明</span> 👍（0） 💬（1）<div>跟着老师一起学习dubbo 💪🏻</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（1）<div>多数人为了逃避真正的思考，愿意做任何事情。~~~这个，太真实了！</div>2022-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6b/af7c7745.jpg" width="30px"><span>tiny🌾</span> 👍（0） 💬（1）<div>非JAVA程序员可以学吗</div>2022-12-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qDOnKs1c3q5dJs8h6UyVpHbV85Bl14fvlia7S4G0PduibsFzHvicyY3fetXyN4BVA0BdicNLRZx5VEMb4bZwDWjBqg/132" width="30px"><span>Geek_9eac3c</span> 👍（0） 💬（1）<div>跟着老师学</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cc/6e/c3c9ea88.jpg" width="30px"><span>别</span> 👍（0） 💬（1）<div>源码 + 官方文档 + 老师课程一起参照学习。</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/54/c2/17512f7a.jpg" width="30px"><span>banxiaobu</span> 👍（0） 💬（1）<div>先码一波👍向何总学习</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e2/c4/6a3bf77e.jpg" width="30px"><span>Nemure</span> 👍（0） 💬（1）<div>异步实践涉及全异步模型吗（请求的异步受理和下游调用异步）</div>2022-12-19</li><br/>
</ul>