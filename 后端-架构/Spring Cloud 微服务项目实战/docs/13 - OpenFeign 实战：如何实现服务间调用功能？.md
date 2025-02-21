你好，我是姚秋辰。

在上一讲中，我带你了解了OpenFeign组件的设计目标和要解决的问题。今天我们来学习如何使用OpenFeign实现**跨服务的调用**，通过这节课的学习，你可以对实战项目中的WebClient请求做大幅度的简化，让跨服务请求就像调用本地方法一样简单。

今天我要带你改造的项目是coupon-customer-serv服务，因为它内部需要调用template和calculation两个服务完成自己的业务逻辑，非常适合用Feign来做跨服务调用的改造。

在集成OpenFeign组件之前，我们需要把它的依赖项spring-cloud-starter-OpenFeign添加到coupon-customer-impl子模块内的pom.xml文件中。

```
<!-- OpenFeign组件 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

在上面的代码中，你并不需要指定组件的版本号，因为我们在顶层项目中定义的spring-cloud-dependencies依赖项中已经定义了各个Spring Cloud的版本号，它们会随着Maven项目的继承关系传递到子模块中。

添加好依赖项之后，我们就可以进行大刀阔斧的OpenFeign改造了。在coupon-customer-impl子模块下的CouponCustomerServiceImpl类中，我们通过WebClient分别调用了template和calculation的服务。这节课我先来带你对template的远程调用过程进行改造，将其替换为OpenFeign风格的调用。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/7e/29/2fc94ee7.jpg" width="30px"><span>金灶沐</span> 👍（29） 💬（4）<div>服务提供方提取一层接口出来， 由服务提供方维护请求路径，    服务消费方，直接声明一个接口extends消费方的接口， 加上@FeignClients即可
</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（15） 💬（2）<div>每个服务提供方单独添加一个openfeign的模块，服务调用方添加对应的openfeign模块即可</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（8） 💬（1）<div>老师，我用spring cloud alibaba搭建了公司的一个项目，服务启动后，接口的首次请求需要2-3秒钟，后续请求都在100ms左右，请问有哪些优化措施可以提高首次接口请求速度？之前使用ribbon可是设置为饿汉式加载，但是spring cloud loadbalancer好像没有饿汉式加载的配置。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bd/f6/558bb119.jpg" width="30px"><span>ᯤ⁵ᴳ</span> 👍（6） 💬（1）<div>请求异常，多次重试等使用Webclient会比较方便，@FeignClient 如何处理呢</div>2022-01-11</li><br/><li><img src="" width="30px"><span>Geek_e93c48</span> 👍（6） 💬（1）<div>关于老师的思考题：
做成将提供方的OpenFeign做成中间件抽离出来。
个人建议：老师是否可以在后边的文章中不仅仅讲技术落地，加入一些使用该技术在生产上的遇到的问题和排查思路，这些才是我们需要的（手动滑稽）</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b1/4f/61a98c13.jpg" width="30px"><span>欢沁</span> 👍（4） 💬（1）<div>老师你好，微服务的数据库分库后，如果A服务要展示的数据需要和B数据库的表关联，微服务划分后，数据库层面就没法做join操作，企业现在通用的方式是怎么处理的。我目前的解决方法是通过feign来调用其他服务获取数据，再插到A服务的对象中，如果遇到关联的表多，就需要feign调用多次，我不认为这是一个好的解决方法，这样的话代码量会堆积非常多，如果没有划分数据库的话，只要通过join就解决问题了。


所以概括就是，我需要关联到其他服务的数据库的表，没法join，我应该怎么做，谢谢老师。</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d7/9a/38d14e5f.jpg" width="30px"><span>mars</span> 👍（4） 💬（3）<div>老师，能问下微服务下调用其他服务，其他服务是其他厂商的web接口，只提供过输入输出和请求地址这种，注册中心也不在一个，这种常规的http请求在微服务架构下的最佳调用实践是咋样的呢？还是继续open feign做url吗？</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（3） 💬（1）<div>要加自定义的header头怎么办？</div>2022-02-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib7ymR5sdB4GVSx3DBHV0fpDP877zs3ia0ia0j0DAI9UDuZtxssgknyyUgmgfmqnXJdMVCkA5ll6NZvIl0w4NmZ7g/132" width="30px"><span>Geek_a5c816</span> 👍（2） 💬（1）<div>这种原始openFegin的实现消费者调用提供者的时候,无法传递headers中的参数,怎么处理呢?</div>2022-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eou1BMETumU21ZI4yiaLenOMSibzkAgkw944npIpsJRicmdicxlVQcgibyoQ00rdGk9Htp1j0dM5CP2Fibw/132" width="30px"><span>寥若晨星</span> 👍（1） 💬（1）<div>为啥不可以直接在服务实现的接口上加@FeignClient注解呢</div>2022-03-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/3icaaUibVCz5gYiaj5gZ4wV8ick5RhEMpe47XKkdK1nAhA9qic6rwhSrpiasDSQYAwfiaIulhE4YKsbwoOXUfvL76EPSw/132" width="30px"><span>Geek_f76b23</span> 👍（1） 💬（1）<div>cusmter服务通过openFeign调用template提供的服务，@FeignClient(value = &quot;coupon-template-serv&quot;), @FeignClient的value指定了调用服务的名称？

如果我把项目里的template-serv复制一份命名为template-serv-copy,用来模拟集群，这个时候copy的服务名称也要叫coupon-template-serv</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/96/fb/af39abb1.jpg" width="30px"><span>黄叶</span> 👍（1） 💬（2）<div>老师，命名方面，我喜欢写成TestServiceFeign进行命名（方面我知道这是个Feign远程调用接口），但看老师是TestService来命名，想请问 这两种方式那种更好</div>2022-01-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cjichzNjhghHD9DJEXCBrh1PqmmlfBwC84NKbn9obLYEGCBDiaqufEArL26Qy0YiaibVbhcnYON7oqh7v6HgCjmk3g/132" width="30px"><span>Geek_eca226</span> 👍（0） 💬（2）<div>openfeign是rpc框架吗，和dubbo那个用的多呢</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/14/85/73e55be5.jpg" width="30px"><span>~</span> 👍（0） 💬（1）<div>思考题：既然每个业务方都要自行维护一套 OpenFeign 接口，还容易出现沟通不利接口出错的问题，不如业务提供方自行创建一套 OpenFeign 接口，单独抽出作为一个依赖，调用方只需要依赖这个就可以调用了。以后业务有改动也可以提供方自行维护，有变动或者需求更改直接给通知就可以了
但是一旦是重大的 bug 需要改动已经被多个调用方使用的依赖，会不会通知起来很麻烦，配合改动也很麻烦？这样改动也不是直接删除吧，新添加一个，之前的改为不建议使用就可以了吧</div>2022-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/45iaRt3S6936b6KLRgpHnonnxXW4vbdMdJdgJX1TAKaN1Xv3GV0ziaN0hHRBicU6FcPKicnZd2M75ViaWqZ3Fjr6Wsw/132" width="30px"><span>tornado</span> 👍（0） 💬（3）<div>能讲讲feign的负载均衡么？查了一下了解的是feign集成了robbin？那robbin和LoadBalancer之间有什么关系呢？</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e2/2b/5eab1490.jpg" width="30px"><span>会飞的鱼</span> 👍（0） 💬（1）<div>老师，这个课程啥时候可以全部更新完咧，有点着急。。。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>由服务提供者，把自己的服务接口封装成一个 jar 包，把 jar 提供给调用方使用即可</div>2022-01-11</li><br/>
</ul>