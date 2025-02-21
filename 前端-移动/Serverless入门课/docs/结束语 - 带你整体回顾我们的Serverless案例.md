你好，我是秦粤。在经过了11节课的学习后，相信此刻，你对Serverless一定有了一些新的认识。那到了尾声，今天这节课我们就结合“待办任务”Web服务的演进过程，带你整体回顾一下本专栏的内容，希望能对你自身沉淀知识有所助益。

一路认真学习并动手实践课后作业的同学其实很容易发现，这个专栏并不是教大家写代码的，而是一堂服务端技术架构课。我们的实践内容和作业，主要也是让你通过部署项目代码体验一下运维的工作，更深刻地理解**“Serverless是对服务端运维的极端抽象”**这句话。

下面我们就分几个阶段去回顾“待办任务”Web服务这个大案例。

## “待办任务”Web服务

我们的代码都在[GitHub](https://github.com/pusongyang/todolist-backend)上，我建议你一定要跟着我的节奏run一下。

## All-in-one

第一个版本[master分支](https://github.com/pusongyang/todolist-backend/tree/master)，以下是这个版本的示意图。

![](https://static001.geekbang.org/resource/image/27/2d/2780a9325c2f6622f1df2f5beb5e0d2d.png?wh=2758%2A870)

你可以看到这个master分支的版本，采用的是Express.js框架，这是一个典型的MVC架构。而且所有的请求，无论index.html、数据API请求，还是静态资源，都放在了一个文件index.js中处理。

这里我特意给出了2个文件：index.js和index-faas.js。index.js是用于本地开发和调试的，而index-faas.js是用于部署到阿里云函数服务的。我们可以对比一下，其实不难发现这2个文件只有细微的差别。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（8） 💬（1）<div>&quot;这个专栏是一堂服务端技术架构课&quot;
这个描述一点也不夸张.

从一个简单项目的多次变迁,可以看清架构是如何演变的.
新引入的技术解决了原有中的什么问题.

其实在平常的工作中,很难有这种完整的经历.
特别是在业务比较平稳的企业,或业务规模不大的小企业中,原有的架构可能并不会遇到瓶颈.
领导可能并没有优化架构的意愿.

也许以后的人,都是直接基于云原生云平台来开发了.
但理清了历史的变迁过程,才能更好的用好当下,和展望未来.

-----
看了老师的答疑,我有了新的认识.
虽然现在的Serverless大多都是Node.js或TypeScript的案例,但并不代表就只适合这个.
后面还有很大的想象空间,我们可以基于自己熟悉的语言,熟悉的场景,来用好Serverless.
为以后的人提供一些经验和参考.

-----
感谢老师在此期间的辛苦付出!
</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/17/0bb45a21.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>经过老师的案例分析，对Serverless有了一个新的认识！</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>江湖再见</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/69/d5a28079.jpg" width="30px"><span>Bora.Don</span> 👍（0） 💬（1）<div>谢谢老师的课程，虽然后半段有很多没看懂的地方。。。
很赞同最后的预测，Serverless不是只服务于网页前端的服务，IoT一样可以直接调用Serverless服务</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/ed/d8776b9c.jpg" width="30px"><span>文蔺</span> 👍（0） 💬（3）<div>安装knative时 总是遇到gcr.io镜像拉取失败的问题，请教老师有没有比较好用的解决办法</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/46/dfe32cf4.jpg" width="30px"><span>多选参数</span> 👍（1） 💬（0）<div>Serverless 不仅工业界在探索，学术界也在探索之中，工业界探索的更多可能是应用场景，而学术界探索更多可能是性能，比如启动时延、安全等。最近准备做 Serverless 下相关的工作，所以把老师这个课都给看了一下。虽然看得不是很懂，这个主要是因为自己没接触过这么多的场景。但是看完之后更加确信 Serverless 是云计算的下一场，也就跟张磊老师说的那样，容器没有用，但是基于容器的编排才是有用的。同样，单独的容器是没有用的，但是将其用到 Serverless 中却大有作为。</div>2020-10-14</li><br/>
</ul>