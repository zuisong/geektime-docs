你好，我是丁威。

这节课我们通过一个真实的业务场景来看看Dubbo网关（开放平台）的设计要领。

## 设计背景

要设计一个网关，我们首先要知道它的设计背景。

2017年，我从传统行业脱身，正式进入物流行业。说来也非常巧，我当时加入的是公司的网关项目组，主要解决泛化调用与协议转换代码的开发问题。刚进公司不久，网关项目组就遇到了技术难题。快递物流行业的业务量可以比肩互联网，从那时候开始，我的传统技术思维开始向互联网技术思维转变。

当时网关项目组的核心任务就是确保能够快速接入各个电商平台。我来简单说明一下具体的场景。

![图片](https://static001.geekbang.org/resource/image/yy/af/yya8c848bc0c0870d5bb5b6bb41268af.jpg?wh=1920x539)

解释一下上面这个图。

物流公司内部已经基于Dubbo构建了订单中心微服务域，其中创建订单接口的定义如下：​

![图片](https://static001.geekbang.org/resource/image/c4/61/c4yy4a46bcb07cbbfb6f0fe750de8861.jpg?wh=1920x936)

外部电商平台众多，每一家电商平台内部都有自己的标准，并不会遵循统一的标准。例如在淘宝中，当用户购买商品后，淘宝内部会定义一个统一的订单外派接口。它的请求包可能是这样的：

```plain
{
  "seller_id":189,
  "buyer":"dingwei",
  "order":[
    {
      "goods_name":"华为笔记本",
      "num":1,
      "price":500000
    },
    {
      "goods_name":"华为手表",
      "num":1,
      "price":200000
    }
  ]
}
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/2f/4518f8e1.jpg" width="30px"><span>放不下荣华富贵</span> 👍（2） 💬（3）<div>数字签名部分：
计算完sign再追加时间戳，时间戳就可能篡改，那还是避免不了重放攻击吧？</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（1） 💬（0）<div>其实这种配置话实体 用起来很灵活 比如我们对接第三方云厂商 就是将 接口传参 请求路径 返回结构 解析结构 鉴权 全部做成了配置话 之后接入其他云厂商 也就只是 配置和联调的工作</div>2022-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/78/b9/d8bb4c45.jpg" width="30px"><span>赤红热血</span> 👍（1） 💬（2）<div>根据这些元信息动态构建一个个消费者（服务调用者），进而通过创建的服务调用客户端发起 RPC 远程调用，最终实现网关应用的 Dubbo 服务调用。
1.这句话里面，消费者为啥是服务调用者？
2.啥叫“创建的服务调用客户端发起rpc远程调用”？这句话读的通吗</div>2022-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/eb/c3ff1e85.jpg" width="30px"><span>🐝</span> 👍（0） 💬（0）<div>如何进行协议转换呢，有什么方案</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/89/93a4019e.jpg" width="30px"><span>fantasyer</span> 👍（0） 💬（3）<div>老师，关于网关这块有三个问题想咨询一下
1、验证签名这块提到，时间戳不参与签名验证，为什么时间戳不参与签名验证，我理解时间戳参与签名可以防止时间戳被恶意篡改，进而可以防止交易恶意重复提交
2、代码invokerPams.put(&quot;class&quot;, &quot;net.codingw.oms.vo.OrderItemVo&quot;);中这里的对象是不是应该是net.codingw.oms.vo.OrderVo，整个报文映射的类？
3、网关这部分设计重点讲了网关内部如何通过泛化调用后端的dubbo服务，想咨询下老师，这个案例中网关对外的接口部分是如何设计的？即给不同的电商是如何暴露接口服务的，从而灵活做到基本不用修改、快速扩展支持？</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（0） 💬（1）<div>如果已经存在对应的 Invoker 对象，为了不影响现有调用，应该先用新的 Invoker 对象去更新缓存，然后再销毁旧的 Invoker 对象。
其中，不影响现有调用，请问如何理解？</div>2022-07-12</li><br/>
</ul>