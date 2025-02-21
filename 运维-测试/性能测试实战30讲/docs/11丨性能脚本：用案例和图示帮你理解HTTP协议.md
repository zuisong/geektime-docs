当前使用得最为广泛的应用层协议就是HTTP了。我想了好久，还是觉得应该把HTTP协议写一下。

因为做性能测试分析的人来说，HTTP协议可能是绕不过去的一个槛。在讲HTTP之前，我们得先知道一些基本的信息。

HTTP（HyperText Transfer Protocol，超文本传输协议），显然是规定了传输的规则，但是它并没有规定内容的规则。

HTML（HyperText Marked Language，超文本标记语言），规定的是内容的规则。浏览器之所以能认识传输过来的数据，都是因为浏览器具有相同的解析规则。

希望你先搞清楚这个区别。

我们首先关注一下HTTP交互的大体内容。想了很久，画了这么一张图，我觉得它展示了我对HTTP协议在交互过程上的理解。

![](https://static001.geekbang.org/resource/image/5f/ba/5fe0f2607000183eb8375cb66cfd41ba.jpg?wh=1526%2A656)

在这张图中，可以看到这些信息：

1. 在交互过程中，数据经过了Frame、Ethernet、IP、TCP、HTTP这些层面。不管是发送和接收端，都必须经过这些层。这就意味着，任何每一层出现问题，都会影响HTTP传输。
2. 在每次传输中，每一层都会加上自己的头信息。这一点要说重要也重要，说不重要也不重要。重要是因为如果这些头出了问题，非常难定位（在我之前的一个项目中，就曾经出现过TCP包头的一个option因为BUG产生了变化，查了两个星期，一层层抓包，最后才找到原因）。不重要是因为它们基本上不会出什么问题。
3. HTTP是请求-应答的模式。就是说，有请求，就要有应答。没有应答就是有问题。
4. 客户端接收到所有的内容之后，还要展示。而这个展示的动作，也就是前端的动作。**在当前主流的性能测试工具中，都是不模拟前端时间的，**比如说JMeter。我们在运行结束后只能看到结果，但是不会有响应的信息。你也可以选择保存响应信息，但这会导致压力机工作负载高，压力基本上也上不去。也正是因为不存这些内容，才让一台机器模拟成千上百的客户端有了可能。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/0f/ee37a7fe.jpg" width="30px"><span>zuozewei</span> 👍（47） 💬（2）<div>思考题：你能说一下为什么压力机不模拟前端吗？

目前的压力工具大部分是针对服务端，即模拟「网络 API 请求」，而前端程序基本上是由一系列的「用户交互事件」所驱动，其业务状态是一颗 DOM 树。

通常来讲，前端性能关注的是浏览器端的页面渲染时间、资源加载顺序、请求数量、前端缓存使用情况、资源压缩等内容，希望借此找到页面加载过程中比较耗时的操作和资源，然后进行有针对性的优化，最终达到优化终端用户在浏览器端使用体验的目的。

目前获取和衡量一个页面的性能，主要可以通过以下几个方面：Performance Timing API、Prpfile 工具、页面埋点计时、资源加载时序图分析；
- Performance Timing API 是一个支持 Internet Explorer 9 以上版本及 WebKit；
内核浏览器中用于记录页面加载和解析过程中关键时间点的机制，它可以详细记录每个页面资源从开始加载到解析完成这一过程中具体操作发生的时间点，这样根据开始和结束时间戳就可以计算出这个过程所花的时间了；
- Profile 是 Chrome 和 Firefox 等标准浏览器提供的一种用于测试页面脚本运行时系统内存和 CPU 资源占用情况的 API；
- 通过脚本埋点计时的方式来统计没部分代码的运行时间；
- 借助浏览器或其他工具的资源加载时序图来帮助分析页面资源加载过程中的性能问题。这种方法可以粗粒度地宏观分析浏览器的所有资源文件请求耗时和文件加载顺序情况。</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/40/7c/43bafeb8.jpg" width="30px"><span>善行通</span> 👍（18） 💬（1）<div>1、听完这样一节才知道http协议在交互过程中，数据经过了 Frame、Ethernet、IP、TCP、HTTP 这些层面，还会再每一次传输都会增加自己的信息头，而且还了解了应答模式；

2、之前一直没有思考【客户端接收到所有的内容之后，还要展示。而这个展示的动作，也就是前端的动作。在当前主流的性能测试工具中，都是不模拟前端时间的，比如说 JMeter。我们在运行结束后只能看到结果，但是不会有响应的信息。你也可以选择保存响应信息，但这会导致压力机工作负载高，压力基本上也上不去。也正是因为不存这些内容，才让一台机器模拟成千上百的客户端有了可能】 听完这一次后，明白了很多细节；

3、明白Nginx【压缩级别【1-9】值越大，压缩率就越高】之前只知道有压缩，但不知道再什么地方压测，今天看了老师写 Ngix 配置才明白再这里配置；

4、明白各个浏览器厂商在处理并发限制不一样，之前一直不知道，今天增加自己知识积累。

5、之前不知道https也是影响性能的，听完了这一篇增加了知识；

6、感谢老师总结【性能分析中，主要关心的部分就是传输字节的大小、超时的设置以及压缩等内容。在编写脚本的时候，要注意 HTTP 头部，至于 Body 的内容，只要能让业务跑起来即可。】


为什么压力机不模拟前端
1、客户端接收到所有的内容之后会在前端浏览器渲染，如果在本地渲染会增加压力机性能消耗，当消耗过大会影响压力发压能力，如果下载资源保存到本地，会增加IO操作压力机性能。
2、前端js&#47;css&#47;img等静态资源都走CDN.</div>2020-01-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLAhj2fB8NI2TPI1SNicgiciczuMUHyAb9HHBkkKJHrgtR162fsicaTqdAneHfuVX7icDXaVibDHstM9L47g/132" width="30px"><span>Geek_0c1732</span> 👍（4） 💬（1）<div>前端渲染是客户端的工作，客户端一般不存在什么并发压力。所以没有必要通过jmeter模拟。想要知道前段渲染性能，可以使用chrome的performance工具</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（3） 💬（1）<div>今日思考题：

你能说一下为什么压力机不模拟前端吗？
模拟前端时间则需要保存响应信息，而保存响应信息会导致压力工具负载变大，进而导致压力上不去，压力上不去就没办法做压力机了……


我的感悟：

感谢高老师结合JMeter工具来讲解HTTP协议，我之前从没点开过HTTP Request Sampler的advanced部分……不过我还是不太明白客户端实现（Client Implementation）这个参数能干啥，或者说什么场景需要用到这个参数。

前几天看了本书，书里介绍了一些前端性能测试的内容，其中有一个前端性能优化方法就是开启GZIP，给的例子是在Apache的配置文件中设置，现在看来这个其实应该属于服务器端性能优化的方法。（但是好像对前端优化也是起作用的，毕竟内容压缩之后变小了，前端展示也会更快）</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/61/985f3eb7.jpg" width="30px"><span>songyy</span> 👍（3） 💬（1）<div>你能说一下为什么压力机不模拟前端吗：因为模拟前端消耗的计算资源太大，相比之下意义可能并不大。
计算消耗大，是说去Parse这个前端的HTML，需要一些计算量；如果需要把这些内容给render出来，需要更多的内存。
一个HTML页面，Load之后会load更多的一些API，这些API可以通过估算，进行混合测试；而那些固态资源，通常会被 浏览器Cache &#47; 网络中的一些路由器给cache，且是从一个静态资源的server单独serve，不用太担心。
需要测的是产生的压力，前端产生
 无意义。</div>2020-01-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ermm498iaT8hp4xmMu51AGoq20UOEwhZeE0wuHkaEsPQ461x1sib0WPwyV5ypQeYJZQ906piaQ4icf9eQ/132" width="30px"><span>Geek_b76638</span> 👍（2） 💬（1）<div>高老师，测试100个用户并发时无报错，测试200-300用户时超时报错很多？是需要设置超时时间吗？</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/41/d8/5a9fbb71.jpg" width="30px"><span>晴空</span> 👍（2） 💬（1）<div>你能说一下为什么压力机不模拟前端吗？
在当前主流的性能测试工具中，都是不模拟前端时间的，比如说 JMeter。我们在运行结束后只能看到结果，但是不会有响应的信息。你也可以选择保存响应信息，但这会导致压力机工作负载高，压力基本上也上不去。也正是因为不存这些内容，才让一台机器模拟成千上百的客户端有了可能。

另外前端页面展示还有部分是静态的图片或文字等，这些可以列在性能测试范围内也可以列在性能测试范围外。</div>2020-01-08</li><br/><li><img src="" width="30px"><span>章鱼</span> 👍（1） 💬（1）<div>【在当前主流的性能测试工具中，都是不模拟前端时间的，比如说 JMeter。我们在运行结束后只能看到结果，但是不会有响应的信息。你也可以选择保存响应信息，但这会导致压力机工作负载高，压力基本上也上不去。也正是因为不存这些内容，才让一台机器模拟成千上百的客户端有了可能。】---- 模拟前端，会导致压力机负载高，压力大，进行性能测试的意义也不大，因为多了不必要的资源消耗。</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>前端也就是 客户端会有各种各样的情况，比如：网络不行 等等，是不可控的。，所以没有必要进行模拟的，只需要压测出后端服务的实际处理能力就可以</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/0f/26c38307.jpg" width="30px"><span>HE明伟</span> 👍（1） 💬（1）<div>高老师，我有点不明白了，压力机不模拟前端，那jmeter进行录制的时候，不是模拟了前端吗，模拟前端不是更加符合用户的真实操作吗，虽然这样会造成压力机的压力很大</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/fb/ecae913a.jpg" width="30px"><span>小安</span> 👍（0） 💬（1）<div>你能说一下为什么压力机不模拟前端吗？
1、压力测试主要是针对服务端进行调优，如何需要对客户端进行调优有专门的客户端调优工具
2、压力机渲染html&#47;css&#47;js会消耗大量的压力机资源，没有必要</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/98/fab9bd2a.jpg" width="30px"><span>Mingyan</span> 👍（0） 💬（1）<div>所以请问选implementation选java还是选httpclient4？还是没看懂两者区别，有个项目用httpclient4会报socket closed的error 但是选java的就不会。请问这种怎么区别？</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b5/72/bb10f3d0.jpg" width="30px"><span>bolo</span> 👍（0） 💬（1）<div>你能说一下为什么压力机不模拟前端吗？

文中有答案，哈哈。 当前的主流性能测试工具中，都不模拟前端时间的，比如Jmeter。我们在运行结束时，只能看到接口响应的结果。但是不会响应信息保存下来。如果保存涉及了大量的文件读写操作，会加大压力机的负载，压力也就上不去。也正是因为这样，一个压力机才能更好的模拟成百上千的客户端。

如果想保存可以写一些文件读写的代码将数据进行提取后保存下来（或者也可以用数据库？）。

附：
FileWriter fstream = new FileWriter(&quot;C:\\Users\\xxx\\Desktop\\result.csv&quot;, true);
BufferedWriter out = new BufferedWriter(fstream);
out.write( vars.get(&quot;seq&quot;) +&quot;\n&quot; );
out.close();
fstream.close();

不过我用来保存数据，不是用来做性能测试的，而仅仅是把jmeter 作为接口调用的工具，数据保存是用来做数据统计的（涉及的项目是一个分流链接项目，支持配置比例）。</div>2021-02-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFMU0wXIHE51jLWGrfEI9fpgyYcSYqJXSRicO55SXibJ9dgpudavKia0OMIjkx08M6beSYDtYQF360g/132" width="30px"><span>胡戎</span> 👍（0） 💬（1）<div>高老师:
目前很多项目信息化建设项目。由于经费等原因，只有一套硬件环境，测试需要在生产开展。项目通常进度比较紧，前期主要保功能，待功能研发的差不多时候用户也开始使用，这时还可以注入部分测试数据。一旦用户正式使用后基本不可能用性能测试工具注入数据。对于这种信息化建设项目如何开展性能分析和测试。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/33/cdea4bca.jpg" width="30px"><span>zwm</span> 👍（0） 💬（1）<div>老师有个问题，这里说的关注请求头信息，我在网页访问和开发提供的api访问，拿到的请求头跟多在jmeter中加不加不影响我的请求正常发出，这点应该怎么考虑呢</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>1，JMeter中cookies几种类型可介绍下吗？2，可否介绍yahoo前端优化30条建议？</div>2020-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/51/50/f5f2a121.jpg" width="30px"><span>律飛</span> 👍（0） 💬（1）<div>为什么压力机不模拟前端吗？
性能测试的目的是获得系统性能指标，利用断言判断业务是否成功即可，并不关注前端页面显示内容，所以无需保存响应信息。
测试工具时，必须多了解参数，知其然并要知其所依然，才能更高效地更自如地配置参数，准确地满足测试要求。</div>2020-01-08</li><br/>
</ul>