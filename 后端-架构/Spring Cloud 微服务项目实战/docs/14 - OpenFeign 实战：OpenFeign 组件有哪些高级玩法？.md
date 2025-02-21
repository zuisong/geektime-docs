你好，我是姚秋辰。

在上一讲中，我们已经将OpenFeign组件集成到了实战项目中。今天我们来进一步深入OpenFeign的功能特性，学习几个OpenFeign的进阶使用技巧：异常信息排查、超时判定和服务降级。

异常信息排查是我们开发人员每天都要面对的事情。如果你正在开发一个大型微服务应用，你经常需要集成一些由其他团队开发的API，这就免不了要参与各种联调和问题排查。如果你是一个经验丰富的老码农，那你一定经常说这样一句话：“你的Request参数是什么？”这句台词在我们平时的API联调和线上异常排查中出镜率很高，因为**服务请求的入参和出参是分析和排查问题的重要线索**。

为了获得服务请求的参数和返回值，我们经常使用的一个做法就是**打印日志**。你可以在程序中使用log.info或者log.debug方法将服务请求的入参和返回值一一打印出来。但是，对一些复杂的业务场景来说就没有那么轻松了。

假如你在开发的是一个下单服务，执行一次下单流程前前后后要调用十多个微服务。你需要在请求发送的前后分别打印Request和Response，不仅麻烦不说，我们还未必能把包括Header在内的完整请求信息打印出来。

那我们如何才能引入一个既简单又不需要硬编码的日志打印功能，让它自动打印所有远程方法的Request和Response，方便我们做异常信息排查呢？接下来，我就来给你介绍一个OpenFeign的小功能，轻松实现**远程调用参数的日志打印**。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/da/67/73a0c754.jpg" width="30px"><span>gallifrey</span> 👍（18） 💬（1）<div>hystrix使用2.2.10.RELEASE的版本时，貌似需要在配置文件里面加上feign.circuitbreaker.enabled: true才行</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/20/88/41212eb9.jpg" width="30px"><span>Avalon</span> 👍（11） 💬（1）<div>老师，如果 TemplateServiceFallback 实现了 TemplateService 接口，那使用注解注入 TemplateService 时，Spring 如何判断要注入的是这个实现类还是动态代理类？</div>2022-01-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/m7fLWyJrnwEPoIefiaxusQRh6D1Nq7PCXA8RiaxkmzdNEmFARr5q8L4qouKNaziceXia92an8hzYa5MLic6N6cNMEoQ/132" width="30px"><span>alex_lai</span> 👍（8） 💬（1）<div>Openfeign client 不是non block的？如果我的框架基于reactive 风格写的是不是没有必要introduce openfeign了，我可以自己写wrap加future在client side。社区未来会提供支持么？openfeign的业界地位是什么样的, nice to have？</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/60/5e/b9624166.jpg" width="30px"><span>被圣光照黑了</span> 👍（4） 💬（1）<div>我在coupon-customer-serv的启动类上加了@EnableHystrix，yml里加了feign:hystrix:enabled: true，coupon-template-serv里有个自定义异常，调用报错了怎么不触发熔断啊</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（4） 💬（1）<div>好像是滑动窗口算法</div>2022-01-12</li><br/><li><img src="" width="30px"><span>Geek_0b93c0</span> 👍（2） 💬（1）<div>降级 放在客户端还是服务端好</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/29/cc30bd9d.jpg" width="30px"><span>逝影落枫</span> 👍（2） 💬（1）<div>是先有熔断，才有降级吗？熔断条件如何配置？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师3个问题：
Q1 容错时用Hystrix，是因为OpenFeign在基于Feign而Feign本来就能和Hystrix集成吗？  除了搭配Hystrix，OpenFeign能搭配Resilience4j吗？  
Q2 &quot;06&quot;篇中，思考题提到“3个模块分别部署到不同的集群上”，如果能分别部署，就不是单体应用了啊，而是像微服务了啊。单体应用就是难以分开部署，不是吗？
Q3：微服务需要有“监控系统”，这个专栏会讲“监控系统”吗？ 或者“02篇”中提到的某个组件充当了“监控系统”？（没有明确说它是监控系统，但具有此功能）
Q4：本专栏会讲“持续集成”吗？ 好像本专栏没有提这个方面。</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/43/3e/960d12cb.jpg" width="30px"><span>DY</span> 👍（1） 💬（1）<div>可能是 openfeign 版本的问题， 我用下面配置验证超时不生效
feign:
  client:
    config:
      # 全局超时配置
      default:
        # 网络连接阶段1秒超时
        connectTimeout: 1000
        # 服务请求响应阶段5秒超时
        readTimeout: 5000
      # 针对某个特定服务的超时配置
      coupon-template-serv:
        connectTimeout: 1000
        readTimeout: 2000

但是换种方式就可以生效：
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            connect-timeout: 8000
            read-timeout: 8000
          coupon-template-serv:
            connect-timeout: 1000
            read-timeout: 2000

springcloud 用的版本是 2022.0.0， 对应的 spring-cloud-starter-openfeign 的版本是 4.0.0</div>2023-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e7/74/69fe068c.jpg" width="30px"><span>简</span> 👍（1） 💬（1）<div>我有点不明白，这个项目结构单独的把API给抽离出来了，如果说引入了第三方的API JAR包后，为什么不能直接使用这个API呢？这个引入的第三方API和我们实现的 @FeignClients 接口几乎一模一样，能利用起来吗？</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/7b/2c/5566d795.jpg" width="30px"><span>春</span> 👍（0） 💬（1）<div>老师你文档里面没有写
feign:
  circuitbreaker:
    enabled: true    &#47;&#47;开启服务降级</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/7b/2c/5566d795.jpg" width="30px"><span>春</span> 👍（0） 💬（1）<div>网上有人说用ErrorDecoder配置错误处理，但是我配了根本没生效是怎么回事</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（0） 💬（1）<div>老师,整个项目有github链接吗? 想clone下来跑跑看</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/e7/326d7515.jpg" width="30px"><span>一个想偷懒的程序坑</span> 👍（0） 💬（3）<div>“FULL：在 HEADERS 级别的基础上，还记录了服务请求和服务响应中的 Body 和 metadata，FULL 级别记录了最完成的调用信息。”，这句话中应该是“记录了最完整的调用信息”吧。</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/5d/c5dc789a.jpg" width="30px"><span>珠穆写码</span> 👍（0） 💬（2）<div>按步骤配置了fallback, 且customer服务配置了feign.circuitbreaker.enabled=true 
template模块里面让线程sleep之后，还是之前readTimeout 没有触发降级。这是缺少了啥么？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（0） 💬（1）<div>OpenFeign+spring-cloud-starter-alibaba-sentinel 的 Client 端降级方案也可以吧</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/43/3e/960d12cb.jpg" width="30px"><span>DY</span> 👍（0） 💬（0）<div>超时没降级， 研究了一天了， 没查到原因
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            connect-timeout: 8000
            read-timeout: 8000
          coupon-template-serv:
            connect-timeout: 1000
            read-timeout: 2000
      circuitbreaker:
        enabled: true

    circuitbreaker:
      hystrix:
        enabled: true

application 上添加 @EnableHystrix 注解

@FeignClient(value = &quot;coupon-template-serv&quot;, path = &quot;&#47;template&quot;,
        fallback = CouponTemplateServiceFallback.class
&#47;&#47;        fallbackFactory = CouponTemplateServiceFallbackFactory.class
)
public interface CouponTemplateService {
...
}

@Slf4j
@Component
public class CouponTemplateServiceFallback implements CouponTemplateService {

    @Override
    public CouponTemplateInfo getTemplate(Long id) {
        log.info(&quot;fallback getTemplate&quot;);
        return null;
    }

    @Override
    public Map&lt;Long, CouponTemplateInfo&gt; getTemplateInBatch(Collection&lt;Long&gt; ids) {
        log.info(&quot;fallback getTemplateInBatch&quot;);
        return null;
    }
}</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8d/f2/3b122904.jpg" width="30px"><span>小猪丶快跑</span> 👍（0） 💬（0）<div>如果openfeign配置了http-client做连接池，需要怎么配置指定某个服务的超时时间？</div>2023-02-14</li><br/><li><img src="" width="30px"><span>Geek_0b93c0</span> 👍（0） 💬（0）<div>超时判定应该是加了个Timer 计时器 从配置读取超时时间 计时器在超时时间后过去该次请求的状态 未执行置为超时状态</div>2022-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq6pWvKsV4rzQ62z5MDEjaEU5MbDfmzbA62kUgoqia2tgKIIxw4ibkDhF7W48iat5dT8UB9Adky2NuzQ/132" width="30px"><span>小仙</span> 👍（0） 💬（0）<div>超时判定
res = future.get(timeout, TimeUnit.MILLISECONDS);
信号量
semaphore = new Semaphore(semaphoreValue);</div>2022-01-12</li><br/>
</ul>