你好，我是孔令飞。从今天开始，我们就要进入实战第二站，开始学习如何设计和开发Go项目开发中的基础功能了。接下来两讲，我们一起来看下如何设计应用的API风格。

绝大部分的Go后端服务需要编写API接口，对外提供服务。所以在开发之前，我们需要确定一种API风格。API风格也可以理解为API类型，目前业界常用的API风格有三种：REST、RPC和GraphQL。我们需要根据项目需求，并结合API风格的特点，确定使用哪种API风格，这对以后的编码实现、通信方式和通信效率都有很大的影响。

在Go项目开发中，用得最多的是REST和RPC，我们在IAM实战项目中也使用了REST和RPC来构建示例项目。接下来的两讲，我会详细介绍下REST和RPC这两种风格，如果你对GraphQL感兴趣，[GraphQL中文官网](https://graphql.cn/)有很多文档和代码示例，你可以自行学习。

这一讲，我们先来看下RESTful API风格设计，下一讲再介绍下RPC API风格。

## RESTful API介绍

在回答“RESTful API是什么”之前，我们先来看下REST是什么意思：REST代表的是表现层状态转移（REpresentational State Transfer），由Roy Fielding在他的论文[《Architectural Styles and the Design of Network-based Software Architectures》](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)里提出。REST本身并没有创造新的技术、组件或服务，它只是一种软件架构风格，是一组架构约束条件和原则，而不是技术框架。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/47/bd/3c88b41b.jpg" width="30px"><span>Geek_zwip3b</span> 👍（46） 💬（4）<div>我觉得老师可以专门开个gin的专栏，看了一下iam源码写的真好。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/a9/9a/5df6cc22.jpg" width="30px"><span>h</span> 👍（8） 💬（1）<div>```避免层级过深的 URI。超过 2 层的资源嵌套会很乱，建议将其他资源转化为?参数，
比如：
&#47;schools&#47;tsinghua&#47;classes&#47;rooma&#47;students&#47;zhang # 不推荐
&#47;students?school=qinghua&amp;class=rooma # 推荐```
老师这句话，我想起来了我一个接口，是和用户组相关的。
我有一个组的接口，它本身有自己的增删查改等几个标准的接口
组表和用户表是个多对多关系，我要写三个接口，分别是：显示组用户，添加组用户，删除组用户。
没看这篇文章之前我写成了 get &#47;group&#47;user&#47;:uid  post &#47;group&#47;user&#47;:uid  delete &#47;group&#47;user&#47;:uid 并且还分别添加了groupid参数，看完老师说的层级过深那段话之后觉得我以前弄的确实有问题，思考之后新的想法如下：
显示组用户应该用 get &#47;group&#47;:gid?fields=user来显示组详情，这里可以通过你说的过滤功能只要显示用户，组其他字段不显示。
添加组用户和删除组用户好像正常情况来讲都是put &#47;group&#47;:gid  就是修改组的那个接口，但是仔细一想，增加用户和删除用户都用 put &#47;group&#47;:gid有点奇怪，而且没办法区分删除还是增加，或者把在后面把现在所有组列出来，比如现在组有用户1,2 增加用户3就是  put &#47;group&#47;:gid?users=1,2,3 ， 假如现在有用户1，2，3，删除3就是 put &#47;group&#47;:gid?users=1,2 
其实不止组，很多有外键关系的好像都存在我这个情况，比如作者表和书籍表，作者表和书籍表有自己的增删查改，那如果我要 查看某作者所有书籍，增加作者一本新书，删除作者一本书
其实说了这么多 就是想问下老师  显示组用户，添加组用户，删除组用户这三个例子你觉得该怎么设计接口，能指教一下如果是你会怎么设计这三个接口以及原因吗？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（7） 💬（6）<div>在过去的经验中，RESTful API对于动词性API不能很好的work，比如说修改密码，重置密码等，很难通过URL和HTTP方法表征出来。
但是对于Github，豆瓣等资源性API，大量的都是资源获取与删除，就特别适合RESTful。</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（3） 💬（1）<div>老师，再请教一下, 关于动词性接口  “是的，可以将这些动词抽象成一个属性”
这里 抽象为属性是什么意思。
比如 有一个视频  &#47;video&#47;12345.mp4 , 现在要提供一个 禁播的操作（非删除），该如何操作。
辛苦老师
</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（3） 💬（1）<div>感觉GraphQL API会比较适合接口变动比较频繁的开发环境，这种API设计看起来基本不用考虑版本兼容的问题，不知道在实际的使用场景中，是不是基于这个原因选择GraphQL，放弃RESTFul的。</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3c/bd/ea0b59f6.jpg" width="30px"><span></span> 👍（2） 💬（2）<div>像RESTful 中 对某个资源的获取 api 中，针对某个特定资源的获取是尽量精简还是需要详细？
如 需求是 获取最近十条的最新数据
应该是 GET: &#47;data?order=createdAt,desc 
还是使用 GET: &#47;last10data 
像在 前后端分离的埸景下
是尽量希望不要暴露太多细节给前端好
还是尽量提供更多的参数细节可让前端调用好？</div>2021-06-23</li><br/><li><img src="" width="30px"><span>Geek_e4ce15</span> 👍（1） 💬（1）<div>一直没有想明白  初期部署的iam到现在有什么用呢 一直是理论也米有涉及到跟iam有关的 除了目录结构</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/42/9f0c7fe4.jpg" width="30px"><span>何长杰Atom</span> 👍（1） 💬（1）<div>老师，关于接口的冥等性，一直不太理解其内涵，比如：
POST不是冥等的，网上说会N次调用会有N个资源创建，但如果不允许重复也不会创建N个资源。
这里说的资源的状态改变效果该怎么理解？
还有谈论的冥等的目的是啥？</div>2022-04-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/xfclWEPQ7szTZnKqnX9icSbgDWV0VAib3Cyo8Vg0OG3Usby88ic7ZgO2ho5lj0icOWI4JeJ70zUBiaTW1xh1UCFRPqA/132" width="30px"><span>Geek_6bdb4e</span> 👍（1） 💬（2）<div>想问一下如何理解“直接使用 POST 方式来批量删除，body 中传入需要删除的资源列表”这句话呢，我的理解POST是用来资源注册，也就是增删改查中的增，这个是在body中加入待删除的资源列表，然后内部代码处理这个逻辑吗，也就是其实内部是删除的逻辑？</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/44/82acaafc.jpg" width="30px"><span>无为</span> 👍（1） 💬（1）<div>老师, 有的时候一个请求不只是单纯某一种资源, 还需要一些关联资源, 这个时候怎么处理比较好?

返回结果通过参数有针对性的添加更多的信息? </div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（1） 💬（3）<div>请问老师为什么说批量删除可以用POST+body传入删除的资源列表，DELETE+body不行吗</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（1） 💬（2）<div>老师 再请教一下 关于动词性的接口，  “是的，可以将这些动词抽象成一个属性”</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（1） 💬（2）<div>老师，讲的太好了，
 想请教一下， 腾讯云和阿里云的 对外API都不是rest的， 基本是一个产品一个域名，后面带一个 action， 不同的action参数有相当于是不同的接口了。 这算是什么风格， 两个行业标杆这么做的好处是什么，</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/60/2f7eb4b5.jpg" width="30px"><span>dairongpeng</span> 👍（1） 💬（1）<div>get请求参数太多的话，通过?x=y&amp;a=b...这种就会有问题，拼接的过长会超过url的长度限制。这种情况，即使是资源获取的接口，我也还是设计成post请求</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1e/18/9d1f1439.jpg" width="30px"><span>liaomars</span> 👍（1） 💬（1）<div>一直没有Get 到 RESTful api风格里的PUT，在实际开发过程中这个被POST代替了。</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（1） 💬（1）<div>RESTful API，符合REST风格的API。
对比传统API风格的好处：简单、低耦合、轻量、自解释、无状态。</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/b1/fb117c21.jpg" width="30px"><span>先听</span> 👍（1） 💬（2）<div>request.Body只能读取一次。 有没有比较优雅的解决办法呢？ 网上查到的都是读取后再手动set回去</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（1） 💬（2）<div>先做个伸手党，iam如何支持流量暴增这种情况，或者说如果提高负载能力</div>2021-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（1） 💬（1）<div>如果比较复杂一点的查询，比如需要join表的情况，如何做扩展比较好呢？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/0d/e65ca230.jpg" width="30px"><span>👻</span> 👍（0） 💬（2）<div>restful的写法好看是好看  但是说实话实用性不好   徒增工作量</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/44/82acaafc.jpg" width="30px"><span>无为</span> 👍（0） 💬（1）<div>老师, 有的时候一个请求不只是单纯某一种资源, 还需要一些关联资源, 这个时候怎么处理比较好?

返回结果通过参数有针对性的添加更多的信息? </div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/30/7b658349.jpg" width="30px"><span>cxn</span> 👍（3） 💬（4）<div>URI中使用_踩过坑,谷歌业务中URI中不能出现_</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/81/d748b7eb.jpg" width="30px"><span>千锤百炼领悟之极限</span> 👍（2） 💬（0）<div>&#47;** 
 * http restful 接口 &#47;hello 打印Hello World
 * 运行 go run hello_world.go
 * 访问 curl http:&#47;&#47;localhost:50052&#47;hello
*&#47;
package main

&#47;&#47; 引入代码依赖
import (
    &quot;log&quot;
    &quot;net&#47;http&quot;
)

&#47;&#47; 启动http服务
func main(){
    http.HandleFunc(&quot;&#47;hello&quot;, hello)
    log.Println(&quot;Starting http server ...&quot;)
    log.Fatal(http.ListenAndServe(&quot;:50052&quot;, nil))
}

&#47;&#47; 打印Hello World
func hello(w http.ResponseWriter, r *http.Request){
    w.Write([]byte(&quot;Hello World&quot;))
}</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/89/77829168.jpg" width="30px"><span>fliyu</span> 👍（1） 💬（0）<div>涉及到敏感信息的Get请求，比如查询用户信息，就算敏感信息（例如手机号码已脱敏），在安全测试也是建议改用Post请求，因为请求的唯一标识一般会携带在url上。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（0）<div>感觉批量删除用post 会比较好一点,比如 post &#47;users&#47;batch 然后定义 ids list 即可</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/75/15/7b22b6c1.jpg" width="30px"><span>穿山乙</span> 👍（0） 💬（1）<div>感觉平时开发不是特别遵守rest规范，基本上通了就行</div>2022-09-24</li><br/>
</ul>