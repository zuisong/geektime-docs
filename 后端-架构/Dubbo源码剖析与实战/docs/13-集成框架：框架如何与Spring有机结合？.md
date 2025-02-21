你好，我是何辉。上一讲我们纵览了框架在源码中是怎么体现的，今天来学习框架的集成。

如果你开发过以 Spring 框架为基础的应用，就会知道 Dubbo 框架常被当作第三方框架集成到应用中，这也是为什么你会经常看到 Spring 集成 Dubbo 框架、Spring Boot 集成 Dubbo 框架。

然而当 Spring 集成 Dubbo 框架后，为什么你在编写代码时，只用了 @DubboReference 注解就可以调用提供方的服务了呢？就像使用 Spring 的 @Autowired、@Resource 注解一样方便，究竟 Dubbo 框架是怎么与 Spring 无缝结合的呢？带着这个问题，我们开始今天的学习。

一切都要从日常开发过程中编写代码调用远程接口讲起。

## 现状 integration 层代码编写形式

假设我们正在开发一个已经集成了 Dubbo 框架的消费方系统，你需要编写代码远程调用下游提供方系统，获取业务数据。这是很常见的需求了。

当系统设计的层次比较鲜明，我们一般会把调用下游提供方系统的功能都放在 integration 层，也就意味着当前系统调用下游提供方系统的引用关系都封装在 integration 层。那你的代码可能会这么写：

```java
public interface SamplesFacade {
    QueryOrderRes queryOrder(QueryOrderReq req);
}
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/29/36/c6bb0893.jpg" width="30px"><span>胡月🌈</span> 👍（6） 💬（1）<div>感觉和spring集成的框架，feign、mybatis都是这个套路：自定义注解，扫描，动态代理生成目标类。</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/da/9a/ed524797.jpg" width="30px"><span>斯瓦辛武Roy</span> 👍（1） 💬（4）<div>你的源码里没看到这一节的代码呢</div>2023-01-16</li><br/>
</ul>