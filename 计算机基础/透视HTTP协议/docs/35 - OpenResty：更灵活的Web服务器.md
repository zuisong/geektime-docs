在上一讲里，我们看到了高性能的Web服务器Nginx，它资源占用少，处理能力高，是搭建网站的首选。

虽然Nginx成为了Web服务器领域无可争议的“王者”，但它也并不是没有缺点的，毕竟它已经15岁了。

“一个人很难超越时代，而时代却可以轻易超越所有人”，Nginx当初设计时针对的应用场景已经发生了变化，它的一些缺点也就暴露出来了。

Nginx的服务管理思路延续了当时的流行做法，使用磁盘上的静态配置文件，所以每次修改后必须重启才能生效。

这在业务频繁变动的时候是非常致命的（例如流行的微服务架构），特别是对于拥有成千上万台服务器的网站来说，仅仅增加或者删除一行配置就要分发、重启所有的机器，对运维是一个非常大的挑战，要耗费很多的时间和精力，成本很高，很不灵活，难以“随需应变”。

那么，有没有这样的一个Web服务器，它有Nginx的优点却没有Nginx的缺点，既轻量级、高性能，又灵活、可动态配置呢？

这就是我今天要说的OpenResty，它是一个“更好更灵活的Nginx”。

## OpenResty是什么？

其实你对OpenResty并不陌生，这个专栏的实验环境就是用OpenResty搭建的，这么多节课程下来，你应该或多或少对它有了一些印象吧。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（26） 💬（1）<div>老师好，多路复用理解起来有点困难，主语是什么呢？ 多路  复用分别怎么理解呢？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（13） 💬（1）<div>看起来OpenResty的核心武器是协程模型和Lua语言嵌入融合，合理照顾到了开发效率和程序执行效率之间的平衡。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（12） 💬（1）<div>域名一般都是带www，也可以不带www，这两者有什么区别？www的作用是什么？</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（11） 💬（1）<div>老师好!
同步阻塞:代码同步顺序执行，等待阻塞操作完成继续往下走。
同步非阻塞:代码顺序执行，遇见阻塞操作时，CPU执行世间会让出去，得到结果时通过callBack继续回到之前阻塞的地方。
大概是这样么?
然后就是同步阻塞的话，在阻塞的时候会占用CPU执行时间么?
同步非阻塞的话，遇到阻塞操作，主线程直接让出CPU执行时间，上下文会切换么?上下文切换开销会很大吧，如果只是让出怎么实现阻塞数据没就绪时不被分配cpu，如果一直没回调这个线程会死锁么?
代码中请求，redis，数据库这些操作是同步阻塞，还是同步非阻塞?

</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（6） 💬（1）<div>老师不写OpenResty专栏亏才了</div>2019-08-23</li><br/><li><img src="" width="30px"><span>Aemon</span> 👍（4） 💬（1）<div>nginx reload不影响应用吧？秒级是认真的吗？</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（1）<div>同步非阻塞，是线程自己主动切换cpu给其他任务，但并没有让出cpu给其他线程或进程，因为在用户态，所以成本低，底层是epoll和Nginx的事件机制。

老师，这块没太明白，同步和非阻塞原本是矛盾的，一个大动作由多个小动作组成，如果其中一个小动作是一个慢动作，而且是同步模式，下面的动作必然会被阻塞住吧？
你上面解释说“线程自己主动切换CPU给其他任务”，
1：那线程什么时候主动切换CPU给其他任务？
2：这里的其他任务指什么？
3：线程主动切换CPU给其他任务后处于什么状态？为什么？
5：还有我的假设中慢动作后面的动作不是被阻塞了吗？
6：还是说维度与层次不同，同步非阻塞的主体是线程，而不是线程中的一系列动作？</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（4） 💬（1）<div>2、“阶段式处理”，我的理解这个与“流水线”很像，许多的业务流程模型其实都可以抽象为流水线，通过配置化的方法，可以定制化地把各个模块组成业务流水线</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（3） 💬（1）<div>老师，既然OpenResty这么厉害，为什么现在大部分公司还是用的Nginx啊？我公司都有Lua程序员，但是Web服务器还是用的Nginx。是不是学习和运维成本都挺高的啊？</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（1）<div>老师你好，可以说一下OpenResty 和 nginx njs 有什么区别吗？</div>2019-08-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVR2wY9icec2CGzZ4VKPdwK2icytM5k1tHm08qSEysFOgl1y7lk2ccDqSCvzibHufo2Cb9c2hjr0LIg/132" width="30px"><span>dahai</span> 👍（2） 💬（1）<div>Nginx 的服务管理思路延续了当时的流行做法，使用磁盘上的静态配置文件，所以每次修改后必须重启才能生效。
Nginx 有reload 命令，只是不是自动reload。</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（2） 💬（1）<div>老师好!看完回复好像明白了一点
同步非阻塞:nginx，是单线程模型，主线程类似一个多路复用器(和NIO的IO模型类似?)，所有的请求是以任务形式被受理，任务是交给协程程处理。任务结束，主线程检测到事件进行对应操作。主线程和协程一直都在处理任务，所以不会涉及到线程的上下文切换。传统的web服务器，Tomcat这些都是线程池形式的。一个请求交给一个线程，请求阻塞了这个线程就会被切换出去开销很大。nginx协程开销已经小了，又通过事件+异步非阻塞模型减少了上下文切换所以吞吐量就能很大。</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（2） 💬（1）<div>谈一下这些天你对实验环境里 OpenResty 的感想和认识。
我感觉有些时候，写代码比写配置文件更加灵活，OpenResty 通过Lua脚本就可以达到这个效果。

你觉得 Nginx 和 OpenResty 的“阶段式处理”有什么好处？对你的实际工作有没有启发？
阶段式处理，有点类似一个类的生命周期，又有点类似责任链模式。实际工作中编写前端组件，也可以采取类似的方式，把组件渲染分阶段，生命周期细分，使组件更专注更内聚。</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>都是硬货</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（1）<div>老师，我上一个问题是这样，wget --no-check-certificate &quot;https:&#47;&#47;www.baidu.com&quot; -e use_proxy=yes -e https_proxy=ip:port 或者
export https_proxy=http:&#47;&#47;proxyhost:proxyport 然后再curl

客户服务器使用上面这两种命令才可以访问百度，如果用OpenResty做可以做吗，是用Lua实现吗？</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（1）<div>老师，我们公司最近给客户部署项目遇到个问题，客户的服务器访问互联网，它中间有一个代理服务器，可能是一个硬件代理，通过代理服务器访问互联网。通过改我们Java应用可以实现给http请求设置代理。我想问的是是不是可以通过OpenResty的lua脚本去做这个事情？</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d6/16/107f0d04.jpg" width="30px"><span>山青</span> 👍（0） 💬（1）<div>这个跟Nginx+lua 感觉跟 Golang的思想有点像啊、</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，请教一个openresty的问题，实现一个主worker向rabbitmq发送消息，在其他worker将消息发送给主worker，由主worker保持tcp连接。在init_worker_by_lua_block阶段用的定时器ngx.timer.at(0, handler)处理tcp连接，同时在这里注册回调函数，回调函数里发送数据，但是回调函数里面的连接却失效了？怎么回事呢？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f6/c4/e14686d4.jpg" width="30px"><span>shk1230</span> 👍（0） 💬（1）<div>epoll 和协程有什么关系？</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>io口多路复用和多线程是我拿c写网络编程用的最多的方法。</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（1）<div>也可能是nginx已经解决了大部分的问题，openresty对很多公司并没有体现出相比nginx的优势，导致用不起来，不是很流行，大家都知道nginx，但是未必都知道openresty。</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/77/b2ab5d44.jpg" width="30px"><span>👻 小二</span> 👍（0） 💬（1）<div>多路复用， 这种是需要操作系统底层提供支持吗？感觉自己的代码再怎么写， 也是多开一个线程在那边等， </div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/17/e63e50f3.jpg" width="30px"><span>彩色的沙漠</span> 👍（0） 💬（2）<div>老师您在一个同学回复中说“同步阻塞的时候是这个线程被阻塞了，操作系统会把这个线程切换出去干别的，不会耗cpu，相当于这个线程没有充分利用cpu资源”，安卓系统用的单线程模型，如果主线程阻塞超时，就会报ANR</div>2019-08-22</li><br/>
</ul>