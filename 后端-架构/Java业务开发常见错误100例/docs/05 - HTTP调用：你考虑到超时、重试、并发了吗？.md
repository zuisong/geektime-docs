你好，我是朱晔。今天，我们一起聊聊进行HTTP调用需要注意的超时、重试、并发等问题。

与执行本地方法不同，进行HTTP调用本质上是通过HTTP协议进行一次网络请求。网络请求必然有超时的可能性，因此我们必须考虑到这三点：

- 首先，框架设置的默认超时是否合理；
- 其次，考虑到网络的不稳定，超时后的请求重试是一个不错的选择，但需要考虑服务端接口的幂等性设计是否允许我们重试；
- 最后，需要考虑框架是否会像浏览器那样限制并发连接数，以免在服务并发很大的情况下，HTTP调用的并发数限制成为瓶颈。

Spring Cloud是Java微服务架构的代表性框架。如果使用Spring Cloud进行微服务开发，就会使用Feign进行声明式的服务调用。如果不使用Spring Cloud，而直接使用Spring Boot进行微服务开发的话，可能会直接使用Java中最常用的HTTP客户端Apache HttpClient进行服务调用。

接下来，我们就看看使用Feign和Apache HttpClient进行HTTP接口调用时，可能会遇到的超时、重试和并发方面的坑。

## 配置连接超时和读取超时参数的学问

对于HTTP调用，虽然应用层走的是HTTP协议，但网络层面始终是TCP/IP协议。TCP/IP是面向连接的协议，在传输数据之前需要建立连接。几乎所有的网络框架都会提供这么两个超时参数：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/e3/81/29dd8167.jpg" width="30px"><span>徐典阳✔️</span> 👍（24） 💬（2）<div>朱老师，请问Feign声明式HTTP接口调用可以针对某服务单个接口配置读取超时参数吗？我们这边一个微服务有n个接口，有一些接口处理耗时长有一些处理耗时短，但调用方又不期望针对同一个微服务声明多个Feign client。我简单翻了源码没有找到。</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（11） 💬（1）<div>我们来分析一下源码。打开 RibbonClientConfiguration 类后，会看到 DefaultClientConfigImpl 被创建出来之后，ReadTimeout 和 ConnectTimeout 被设置为 1s：

&#47;**
 * Ribbon client default connect timeout.
 *&#47;
public static final int DEFAULT_CONNECT_TIMEOUT = 1000;

&#47;**
 * Ribbon client default read timeout.
 *&#47;
public static final int DEFAULT_READ_TIMEOUT = 1000;

@Bean
@ConditionalOnMissingBean
public IClientConfig ribbonClientConfig() {
   DefaultClientConfigImpl config = new DefaultClientConfigImpl();   &#47;&#47;此行打断点
   config.loadProperties(this.name);
   config.set(CommonClientConfigKey.ConnectTimeout, DEFAULT_CONNECT_TIMEOUT);
   config.set(CommonClientConfigKey.ReadTimeout, DEFAULT_READ_TIMEOUT);
   config.set(CommonClientConfigKey.GZipPayload, DEFAULT_GZIP_PAYLOAD);
   return config;
}

被死扣的毛病折腾着，以上这段描述和代码中，有两个疑问，烦老师解惑，谢谢。
1、使用默认配置，我在标注行打了断点，debug启动时未进断点。是不是表明默认值不是在此段代码设置的？
2、找到了feign配置的原始类FeignClientProperties，但是没找到ribbon的。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（24） 💬（1）<div>老师，我这边工作过程中遇到服务端 499 这块要怎么从链接超时和读取超时设置去分析呢？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（60） 💬（2）<div>试着回答下问题：
1、为什么很少见到写入超时，客户端发送数据到服务端，首先接力连接（TCP），然后写入TCP缓冲区，TCP缓冲区根据时间窗口，发送数据到服务端，因此写入操作可以任务是自己本地的操作，本地操作是不需要什么超时时间的，如果真的有什么异常，那也是连接（TCP）不上，或者超时的问题，连接超时和读取超时就能覆盖这种场景。
2、proxy_next_upstream：语法: proxy_next_upstream 
      [error|timeout|invalid_header|http_500|http_503|http_404|off]
      默认值: proxy_next_upstream error timeout
      即 error timeout会自动重试
可以修改默认值，在去掉error和timeout，这样在发生错误和超时时，不会重试
proxy_next_upstream_tries 这个参数决定重试的次数，0表示关闭该参数
Limits the number of possible tries for passing a request to the next server. The 0 value turns off this limitation.</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（33） 💬（1）<div>这已经不单单是一个坑了，而是N一个场景下，多种多样的坑。
Spring Boot 带来了【约定大于配置】的说法，但是，本文告诉我们，越是约定大于配置，越是要对那些“默认配置”心里有数才行。
HTTP请求，说到底，还是网络调用。某个老师曾说过，网络，就是不靠谱的。就存在拥塞，丢包等各种情况。从而使得排查的难度更大。要考虑的角度，宽度，都更广。不单是客户端，服务端，甚至还要考虑网络环境。这对程序员具备的技术深度，广度都有了更高的要求。
今天的收货：
首先，增长了经验。知道了有这么些坑，虽然不一定能记得住，最起码留个印象。以后碰到类似的问题了能想起来。
然后，不能盲目相信默认配置。条件允许的情况下，还是需要了解关注那些默认配置以及默认实现。
最后，对HTTP调用，的测试方式与模拟方式，也了解到了测试方式。如何分别设置超时时间来找问题。

其实，还希望能听听老师讲讲HTTP调用出问题的排查思路与方案。</div>2020-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIFgmmBXRltzTkfeajYGLptvvwEsMyiaCT5nJZNg4TZJWh02cgwxtrEIk6TWSbGpBibE7Bbvoicjciaiag/132" width="30px"><span>Geek_d7ede4</span> 👍（32） 💬（7）<div>老师您好，我之前对接过一个第三方支付接口，调用支付接口a账户对b账户进行了转账操作，我业务数据库也要做一个记账操作在数据库中，如何保证调用第三方支付接口和我本地的业务是一致性的呢？就是第三方支付接口有可能已经转账成功了，但是我业务代码可能抛异常，导致回滚了。</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/f0/708189aa.jpg" width="30px"><span>Unravel👾</span> 👍（8） 💬（2）<div>老师您好
前段时间遇到过一个连接超时的问题，在springboot中使用restTemplate(无论是不配置还是增大超时时间或是加入apache http client连接池)在业务中请求另外一个服务的接口经常会出connect timeout(经过nginx或是直接连接tomcat都会出现)
此时ping、telnet、curl都是成功的
但是如果另有一个任务定时一直请求接口，那么在业务中就不会出现connect timeout了。
一直没有成功解决这个问题，想问下老师可以从哪方面入手，谢谢老师</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（5） 💬（1）<div>花了两个晚上终于还是把这节啃了下来，准备运行环境，重现所有问题，翻看相关源码。
终于等到你，还好我没放弃。
个人感悟，这些坑对以后快速排查问题，肯定有帮助。就算以后淡忘了这节的内容，但至少还会有些许记忆的，哪个专栏，哪个老师，哪篇文章。感谢老师！</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（4） 💬（1）<div>老师，对于Http Client和Ok Http相比，是不是OkHttp支持得更好，而且HTTP2相比于HTTP1.1的新特性是不是也使得我们不用过去的一些配置了啊</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（3） 💬（3）<div>public class ClientReadTimeoutController {
    private String getResponse(String url, int connectTimeout, int readTimeout) throws IOException {
        return Request.Get(&quot;http:&#47;&#47;localhost:45678&#47;clientreadtimeout&quot; + url)
                .connectTimeout(connectTimeout)
                .socketTimeout(readTimeout)
                .execute()
                .returnContent()
                .asString();
    }
....
}


这第一段代码中Request这个类，是引用哪个包下的？找得好辛苦，老师第5节的代码也没上传到git</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（3） 💬（1）<div>好文章，好“坑”。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（2） 💬（1）<div>处理超时一定要搞清楚超时的阶段。到底是建连超时还是等待响应超时(读取超时)。针对不同的问题针对解决。对于写超时这个相当于写本地TCP缓冲区，速度应该很快，很少会出现socket无法写入导致的写超时问题。
很久没用用过HttpClient了。回忆了一下，以前确实没有搞清楚总并发(maxTotal)和单域名并发(defaultMaxPerRoute)的区别。通过这篇文章总算搞明白了，收货颇丰。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/e7/326d7515.jpg" width="30px"><span>一个想偷懒的程序坑</span> 👍（2） 💬（1）<div>虽然没处理过这块儿的东西，但看完了解了许多知识，赞！</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/85/3f161d95.jpg" width="30px"><span>Alpha</span> 👍（2） 💬（3）<div>非常同意选择Get还是Post应该依据API的行为。
但是有时数据查询的API参数确实不得已很长，会导致浏览器的长度限制，老师有好的办法吗？</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（3）<div>ribbon.ReadTimeout=4000
ribbon.ConnectTimeout=4000

这个参数的key命名不规范，是有故事，还是开发人员不够专业？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（1） 💬（2）<div>关于Feign读取超时必须同时配置连接超时才能生效的问题，貌似在spring-cloud-openfeign:2.2.4.RELEASE版本修复了，对应的springcloud版本Hoxton.SR7</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/d9/18acc2ee.jpg" width="30px"><span>星辰大海</span> 👍（1） 💬（1）<div>老师你好 想问下resttemplate可以单独针对sockettimeout exception进行处理吗 最近的一个项目中使用resttemplate方式调用下游 针对读取超时的情况不再进行重试 但resttemplate对异常进行了重新封装 无法进行单独识别 </div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0b/25/bee12452.jpg" width="30px"><span>justinzhong</span> 👍（1） 💬（1）<div>老师，针对发送短信的那个例子，解决重试问题的方法一：就是get请求换成post请求，我试了几次都是不行的，还是会重试一次，但是方法二是完全可以的。可以针对方法一的解决重试问题的思路再描述的清楚一些吗？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（1） 💬（1）<div>sendRequest(int count, Supplier&lt;CloseableHttpClient&gt; client) 这个方法中第二个参数为什么要用一个函数接口而不是直接用CloseableHttpClient类型呢？ 我看也没用到什么特性，只是调用了execute方法而已？
课后问题：1. 感觉写入超时已经包含在读取超时这个里面，没必要单独定义这么细的超时。
2. nginx真不是很了解，老师想加餐了吗？哈哈</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/39/72d81605.jpg" width="30px"><span>大尾巴老猫</span> 👍（1） 💬（1）<div>void server();
这一句什么意思？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（1） 💬（1）<div>老师我是做客户端的 ，我们这边还有个写超时概念这块老师方便分享下不</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（1） 💬（1）<div>老师总结的很有深度、很全面、很有业务实战</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（1）<div>对于数据写入，开发者都可以直接控制，要么先write然后再一次性flush，要么边write边flush，至于最后socket缓冲区中的数据如何发送，都交给了tcp。</div>2020-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（1） 💬（2）<div>按照老师解释的读取超时的概念：字节流放入socket---&gt;服务端处理-------&gt;服务端返回---&gt;取出字节流。
那写入超时估计就是字节流放入socket的时间，这个属于自己主动控制的可能没有必要吧，具体可能还需要了解一下网络编程才能知道。</div>2020-03-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ1VPGSQg7SqrN1Gutx31Kicks2icZjTCg1gZoDLfEcSSricYD6l5qQgE3MkMpqlhkM4gMicymOYzaudg/132" width="30px"><span>可可</span> 👍（0） 💬（1）<div>服务启动后经常会出现下面错误日志。请问是怎么回事啊？

[13:57:11.624] [influx-metrics-publisher] [ERROR] [io.micrometer.influx.InfluxMeterRegistry:146 ] - failed to send metrics to influx

[13:58:10.578] [influx-metrics-publisher] [ERROR] [io.micrometer.influx.InfluxMeterRegistry:106 ] - unable to create database &#39;mydb&#39;
</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/b0/9335798e.jpg" width="30px"><span>I</span> 👍（0） 💬（2）<div>想提一个ribbon的问题
文章中 有个配置 SmsClient.ribbon.listOfServers=localhost:45679,localhost:45678
是指定服务调用地址，不过这个配置在使用eureka做服务发现的时候就不生效了，有没有办法，在使用eureka的时候也可以指定服务调用地址呢，这个问题有点奇葩，不过还是想知道有办法吗</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/e7/b29afd20.jpg" width="30px"><span>Evan</span> 👍（0） 💬（1）<div>请教老师spring resttemplate如何设置单次请求的超时时间。比如不同的接口需要设置不同的读取超时时间。</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/d0/402be1e9.jpg" width="30px"><span>VIC</span> 👍（0） 💬（2）<div>feign默认用的urlconnection，有并发限制吗</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/2b/9db9406b.jpg" width="30px"><span>星夜</span> 👍（0） 💬（3）<div>老师是怎么理解上下游服务的，我一般将被调用方称为上游服务，查资料一般说两种叫法都是正确的，理解方式不同。</div>2020-06-28</li><br/><li><img src="" width="30px"><span>hwnly</span> 👍（0） 💬（1）<div>	我看了下我们这边的项目源码spring-cloud-netflix-core-1.3.5.RELEASE  jar版本是这样写的
        @Bean
	@ConditionalOnMissingBean
	public IClientConfig ribbonClientConfig() {
		DefaultClientConfigImpl config = new DefaultClientConfigImpl();
		config.loadProperties(this.name);
		return config;
	}

DefaultClientConfigImpl中设置的
public static final int DEFAULT_CONNECT_TIMEOUT = 2000;
public static final int DEFAULT_READ_TIMEOUT = 5000;
不知道作者用的什么版本呢</div>2020-06-10</li><br/>
</ul>