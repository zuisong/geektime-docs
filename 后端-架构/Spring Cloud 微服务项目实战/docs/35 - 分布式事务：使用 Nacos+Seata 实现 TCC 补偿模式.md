你好，我是姚秋辰。

上节课我们落地了一套Seata AT方案，要我说呢，AT绝对是最省心的分布式事务方案，一个注解搞定一切。今天这节课，我们来加一点难度，从Easy模式直接拉到Hard模式，看一个巨复杂的分布式事务方案：Seata TCC。

说TCC复杂，那是相对于AT来讲的。在AT模式下，你通过一个注解就能搞定所有事情，不需要对业务层代码进行任何修改。TCC难就难在它的实现方式上，它是一个基于“补偿模式”的解决方案。补偿的意思就是，你需要通过编写业务逻辑代码实现事务控制。

那TCC是如何通过代码来控制事务状态的呢？这就要说到TCC的三阶段事务模型了。

## TCC事务模型

TCC名字里这三个字母分别是三个单词的首字母缩写，从前到后分别是Try、Confirm和Cancel，这三个单词分别对应了TCC模式的三个执行阶段，每一个阶段都是独立的本地事务。

![图片](https://static001.geekbang.org/resource/image/70/ec/700119981d8a5bf14843d35c4b03ecec.jpg?wh=1920x559)

Try阶段完成的工作是**预定操作资源（Prepare），**说白了就是“占座”的意思，在正式开始执行业务逻辑之前，先把要操作的资源占上座。

Confirm阶段完成的工作是**执行主要业务逻辑（Commit）**，它类似于事务的Commit操作。在这个阶段中，你可以对Try阶段锁定的资源进行各种CRUD操作。如果Confirm阶段被成功执行，就宣告当前分支事务提交成功。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（14） 💬（2）<div>对于tcc 和 at 如果涉及到分布式事务  小公司 和 团队人数少的公司选择哪个好呢？还有别的更简单的方法吗</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（5） 💬（1）<div>老师能讲下 微服务的 后端接口 版本升级怎么控制的嘛，多个版本兼容怎么做的呢？是通过网关转发到不同的服务上吗。</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（1） 💬（1）<div>之前看过Seata文档，看了老师的文章后，发现理解更深了，问个问题，关于AT隔离性问题，默认是读提交，这是因为全局事务中，每个分支事务都是直接提交的，所以针对全局事务来说，是需要读到其他事物中部分分支已经提交的事务吗？</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（4）<div>请教老师几个问题：
Q1：接口类指向是什么意思？
文中有一句话“将 CouponTemplateServiceImpl 的接口类指向刚定义好的 CouponTemplateServiceTCC 方法”，怎么指向的？
Q2：阿里这种级别的公司，其入口是怎么做的？
网站最外面的入口，是怎么实现的？现有的外部网关，比如F5、Nginx、LVS等，处理速度都是有限的，对于阿里这种规模的公司，肯定是处理不过来的。那怎么解决这个问题？
Q3：tomcat连接数与CPU核数的矛盾问题。
tomcat服务器一般能够支持500个连接，好像最大支持1000个连接；一个连接一个线程，那就是500个线程。但一般服务器的CPU核数也就是10个左右。一般的规律是：线程的数量一般是核数的2倍，也就是20个。20个和500个不矛盾吗？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（1）<div>这个tcc的步骤怎么感觉跟2pc的一模一样啊？这两者有什么区别吗</div>2023-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwIgbTd3oy4ESHr6bX9iblONuwgU0MWHcgxndWwNNRQGXlhicduummSiamfTcxHsicicxR4nElxzj280Q/132" width="30px"><span>Geek_5c44aa</span> 👍（0） 💬（2）<div>老师问个问题：使用Seata的时候，是否必须用Nacos作为微服务的注册中心？</div>2023-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/et0qH6zf5icoo6YJoH2WDyia7MTtdQiasicFecfMupzT5VD18aOjzoiaym1OP9RGUEUvLsPRUmCZVSTbrmydpNicVAPA/132" width="30px"><span>GeekJohn</span> 👍（0） 💬（1）<div>要是新增操作，try阶段如何去锁定资源呢？那时数据库还没有生成记录。</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（0） 💬（0）<div>这一节感觉好马，没有后续的验证操作，自己实现了个接口发现总是不安预期来运行

基于2.x版本目前找到了以下问题点：
- @BusinessActionContextParameter 要注在实现上，不然BusinessActionContext的ID带不过来
- tcc有个client的表，需要在服务数据库建立

但是还是没按预期来，好像写入不了数据库</div>2024-09-28</li><br/>
</ul>