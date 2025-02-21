你好，我是秦粤。上一讲我们介绍了FaaS的两种进程模型：用完即毁型和常驻进程型，这两种进程模型最大的区别就是在函数执行阶段，函数执行完之后函数实例是否直接结束。同时，我还给你演示了用完即毁型的应用场景，数据编排和服务编排。

这里我估计你可能会有点疑虑，这两个场景用常驻进程型，应该也可以实现吧？当然可以，但你还记得不，我多次强调用完即毁型是FaaS最纯正的用法。那既然介绍了两种进程模型，为什么我要说用完即毁型FaaS模型比常驻进程型纯正？它背后的逻辑是什么？你可以停下来自己想想。

要真正理解这个问题，我们需要引入进来复杂互联网应用架构演进的一个重要知识点：扩缩容，这也是我们这节课的重点。

为了授课需要，我还是会搬出我们之前提到的创业项目“待办任务”Web网站。这一次，需要你动动手，在自己本地的机器上运行下这个项目。项目的代码我已经写好了，放到GitHub上了，你需要把它下载到本地，然后阅读README.md安装和启动我们的应用。

GitHub地址：[https://github.com/pusongyang/todolist-backend](https://github.com/pusongyang/todolist-backend)

我给你简单介绍下我们目前这个项目的功能。这是一个后端项目，前端代码不是我们的重点，当然如果你有兴趣，我的REAME.md里面也有前端代码地址，你可以在待办任务列表里面创建、删除、完成任务。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/56/89952257.jpg" width="30px"><span>蒲松洋</span> 👍（8） 💬（0）<div>看来很多同学都没有了解过egg.js框架，这里我需要补充一下，我Node.js的主进程和子进程的例子，其实是用了egg.js的进程模型，想跟大家解释这点知识内容。但我代码中的Express.js框架，要使用子进程要额外使用node.js的cluster模块。Node.js是单线程的，但实际它是用event loop让内核的线程去处理事件，响应时再回调handle，其实协程。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（14） 💬（11）<div>我比较好奇老师在实践Serverless的过程中踩了多少坑.

# 我来说说我昨天在阿里云上体验Faas时的采坑记录

## 1. `fun build` 命令无法做到幂等性
相同的输入,经过相同的处理,得到的结果却具有不确定性.
症状是:
借助git命令,保证目录下的文件完全一致,但是执行`fun build`命令的结果却会具有不确定性.

说实话,这个功能对我没任何影响,我只是来体验FC的功能的.他们的基础服务有问题,修不修复对我来说不重要.
但我觉得吧,像这种大厂的用户会比较多,以后难保其他用户不会遇到这种问题.

本着方便后来人的角度,我还是花时间研究了下,如何成功在我本地大概率的复现该问题.
这个问题给他们反馈了,也提供了视频和日志,不确定他们是否会重视这个问题.

## 2. 命令行工具`fun`与VSCode插件行为不太一致
在命令行中使用fun deploy部署时,实际是优先使用的` .fun&#47;build&#47;artifacts&#47;template.yml`文件
而VSCode插件中默认使用的是项目根目录下的`.&#47;template.yml`
前者是使用`fun build`命令自动生成的.

我之前其实在命令行中已经照着官方文档把服务部署好了,但是我为了体验VSCode的插件,我又搭建了一次.
这次就遇到了VSCode上部署的服务无法正常工作,提示缺少依赖项.

后来在钉钉群里咨询,才知道现在需要用`fun install`安装依赖.
使用`fun install`安装依赖的方式,再在VSCode上一键部署的服务就是可用的了.

# 最近几天体验函数计算的感悟
## 看上去确实很方便
只要你把服务调通了,几乎不用你操心剩下的运维等工作,现在还有免费额度用,个人肯定是用不完的.

## 排查问题会比较困难
特别是跟服务提供方相关的,对于开发者来说,完全是黑盒操作.
自身代码的调试,还可以借助本地调试功能来排查.
但是一旦提交到了函数计算平台,想查问题就非常难了.

例如:
1. 服务在本地可以正常运行,为什么在远程会提示缺少依赖项?
   其实在执行`fun deploy`的过程中,它会帮你把本地目录打包成zip文件,上次到云上,使用zip包内的文件部署函数服务.
   而`fun deploy`打包了哪些文件,其实我们是很难知道的.

   我上面提到的第二个坑就跟这个有关系.
   fun build把依赖包安装到了一个隐藏的目录,与fun install安装的目录并不相同
   而fun deploy会根据使用的template.yml文件来确定待压缩文件的路径.
   恰巧`fun deploy`又比较`智能`,会优先使用`.fun&#47;build&#47;artifacts&#47;template.yml`,若该文件不存在,才会使用`.&#47;template.yml`.
   这样,我用fun build安装的依赖文件, 在VSCode上通过一键部署时, 并未打包到zip文件中.

   这个也是我自己琢磨出来的.

2. 函数计算的冷启动时间如何优化?
   现在连具体的冷启动时间是多长,都无法确定,更无法谈如何优化了.
   不清楚 node.js python 的冷启动为什么只有600-800ms, 而用`Custom Runtime`打包的golang服务却要2.5s.

3. 函数的具体单次执行时间如何确定?
   目前只能借助云平台的日志,查看函数的平均执行时间.
   自己最多只能在函数执行的入口和出口加入时间统计.
   我就发现,我用`Custom Runtime`打包的golang服务
   显示的函数平均执行时间始终是100ms,而node.js和python的服务耗时时间就是动态的,只有20ms+,远没有到100ms.

</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（5） 💬（2）<div># 对于 用完即毁型和常驻进程型 的体会
以前我做游戏时,很多状态都是维护在内存中.
这种服务如果迁移到FaaS就很困难.需要做改造,把需要持久化的数据存储到其他地方.

现在做的服务,是基于接口对外提供的服务.
本身不存储状态,都是根据数据库中的数据库反馈结果.

现在的服务,理论上其实可以很方便的迁移到FaaS.
虽然是常驻进程型的,但本身并不存储状态.
就是在初始化阶段,需要连各种数据库,会耽误点时间.

# 对于并发访问的思考
昨天晚上还在想,明天要抽时间用ab压测一下函数计算提供的接口.
看看所谓的`并发度`到底是什么.
之前在文档上看过,一个函数实例可以配置允许的同时并发度,如果不够了,就会冷启动新的实例.

我之前测试的服务都是常驻进程型的,我就想搞个定时任务,每分钟请求一次,保证服务进程不会被回收.
其实每分钟请求一次的消耗也不大,但如果能消除冷启动,绝对是划算的.

但后来一想,这个只针对单实例有效,如果想保证同时有N个实例,如何才能保证定时请求可以将N个实例都访问到呢?
这个需要用再实践一下.

# 课后作业
由于前几天已经配置了阿里云的fun本地环境,自己也有备案了域名,所以实践老师的作业只需要简单的几部.
[我在老师的专栏开始之前完全未接触过node.js 现在也只是跟着老师部署了几个简单的node.js服务]

1. 克隆代码
	git clone https:&#47;&#47;github.com&#47;pusongyang&#47;todolist-backend
2. 拷贝文件
	cp index-faas.js index.js
3. 安装依赖
	npm install
4. 创建template.yml文件
```
ROSTemplateFormatVersion: &#39;2015-09-01&#39;
Transform: &#39;Aliyun::Serverless-2018-04-03&#39;
Resources:
  todolist-backend:
    Type: &#39;Aliyun::Serverless::Service&#39;
    Properties:
      Description: &#39;helloworld&#39;
    todolist-backend:
      Type: &#39;Aliyun::Serverless::Function&#39;
      Properties:
        Handler: index.handler
        Runtime: nodejs10
        CodeUri: &#39;.&#47;&#39;
      Events:
        httpTrigger:
          Type: HTTP
          Properties:
            AuthType: ANONYMOUS
            Methods:
              - GET
              - POST
```
5. 部署服务
	fun deploy -y
6. 绑定自定义域名
	需要把路径&#47;*都绑定到该服务上
7. 验证效果
	可以重现老师的服务: http:&#47;&#47;todo.jike-serverless.online&#47;list

# 扩展思考
如果只是测试,可以配合NAS服务来持久化部分数据.
我之前写demo时,用这个功能,简单的记录我函数计算服务的访问日志和时间.

仅仅只是测试,并未考虑到多实例并发访问的问题.

</div>2020-04-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/fUDCLLob6DFS8kZcMUfxOc4qQHeQfW4rIMK5Ty2u2AqLemcdhVRw7byx85HrVicSvy5AiabE0YGMj5gVt8ibgrusA/132" width="30px"><span>NO.9</span> 👍（1） 💬（1）<div>今天终于有空做作业。我是aws Lambda+api Gateway 。说实话 我没看懂应该部署哪个文件。我先尝试用aws的示例代码 invoke了一次 成功了？但是把index.js的内容贴进去(是的，我只粘贴了这一个文件内容) 显示失败。。。</div>2020-06-19</li><br/><li><img src="" width="30px"><span>Geek_f7f72f</span> 👍（1） 💬（1）<div>对于传统数据库那块，还有一点疑问。文中提到传统数据库同样的操作会比 HTTP 快，同时又提到FaaS直连数据库增加了冷启动时间。那么改造后的BaaS又是如何避免这个问题的？</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（10）<div>用 fun 部署完成只会，访问 报错啊
The CA process either cannot be started or exited:ContainerStartDuration:25516062312， 又没用用 https 咋还有CA证书了？</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（3）<div>当 Nodejs 处理并发请求的并不会自动创建子进程，利多核CPU的的特性。 Nodejs一直都是单线程的
A single instance of Node.js runs in a single thread. To take advantage of multi-core systems, the user will sometimes want to launch a cluster of Node.js processes to handle the load
如果想利用多核 就要使用 cluster 模块

还有就是 并发 是在一个 CPU 核心上交替执行， 在多个 CPU 核心上执行这叫做并行</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（1）<div>看了下代码似乎并没有开node多进程...如果是挂在nginx上面的话nginx确实会创建worker进程，但也不是每次请求来都会创建新进程...</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/34/c1/4e4917f5.jpg" width="30px"><span>有一种踏实</span> 👍（0） 💬（1）<div>用的阿里云，配置自定义域名太麻烦了，还要花钱，我注意到生成的函数 url 不能通过浏览器直接访问，但可以通过 script 以 http api 的形式访问，所以本地起个 express，做一个透传 server 即可看到一样的效果

&#47;&#47; 透传 server 代码
const express = require(&#39;express&#39;);
const bodyParser = require(&#39;body-parser&#39;);
const axios = require(&#39;axios&#39;);

const port = 3001;
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.all(&quot;&#47;*&quot;, async (req, res) =&gt; {
  const { method, query, body, headers, _parsedUrl: { pathname } } = req;
  
  const targetHost = &#39;todolist-xxxxxxxxxxx.cn-hangzhou.fcapp.run&#39;;
  const targetBaseURL = `https:&#47;&#47;${targetHost}`;

  const tartgetRes = await axios({
    baseURL: targetBaseURL,
    url: pathname,
    data: body,
    params: query,
    headers: {
      ...headers,
      host: targetHost,
    },
    method: method || &#39;get&#39;,
    responseType: &#39;stream&#39;,
  });

  const { status } = tartgetRes;
  if (status === 200) {
    tartgetRes.data.pipe(res);
  }
});

app.listen(port, () =&gt; {
  console.log(`Example app listening at http:&#47;&#47;localhost:${port}`);
});
</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/96/3f/7c8a8676.jpg" width="30px"><span>周科</span> 👍（0） 💬（2）<div>Node.js处理请求，并不是来一个请求就创建一个子进程去处理啊，应该说是来一个请求就创建一个context。4核机器跑egg.js应用，默认也是4个子进程吧，而且Node.js进程一直常驻内存的，不会根据请求动态创建或回收。</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（1）<div>问一个问题，后端存储变为BaaS后，传统的数据库事务怎么处理呀？</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/36/93/7dc76b32.jpg" width="30px"><span>PP-CIPDS-GRC</span> 👍（0） 💬（1）<div>所以其实是每个调用阶段的管控颗粒度更细了，stateful 服务调用采用 BaaS 服务和数据持久化，费用单独算。前端的数据编排接口采用 FaaS 按次数调用，可以这么理解？静态的还是静态，动态的保持动态。整个调用 Pipeline 的各个动静部分解耦。</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>BaaS 的数据库， 可以像FaaS 一样按使用量收费吗？</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/27/805786be.jpg" width="30px"><span>笨笨</span> 👍（0） 💬（1）<div>个人感悟：GraphQL就是BaaS的一种实践。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/63/bfbee4ac.jpg" width="30px"><span>深黑色</span> 👍（0） 💬（1）<div>老师，请教一下在阿里云上貌似没有看见用完即毁型和常驻型的区分选项呢？</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/69/d5a28079.jpg" width="30px"><span>Bora.Don</span> 👍（0） 💬（2）<div>按照这种思路，faas也不需要了，直接前端代码里的js调用baas，一把梭哈，全部搞定。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（0） 💬（1）<div>在传统的服务话架构中，BFF后面的服务是有蛮重的业务逻辑在，BFF本身会做的很薄。在servless中，BASS是否只是对数据层的接口包装？还是也会包含逻辑？谢谢了！</div>2020-04-24</li><br/>
</ul>