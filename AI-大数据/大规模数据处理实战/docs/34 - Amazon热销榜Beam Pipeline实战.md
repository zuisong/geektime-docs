你好，我是蔡元楠。

今天我要与你分享的主题是“Amazon热销榜Beam Pipeline实战”。

两个月前，亚马逊（Amazon）宣布将关闭中国国内电商业务的消息你一定还记忆犹新。虽然亚马逊遗憾离场，但它依然是目前全球市值最高的电商公司。

作为美国最大的一家网络电子商务公司，亚马逊的总部位于华盛顿州的西雅图。类似于BAT在国内的地位，亚马逊也是北美互联网FAANG五大巨头之一，其他四个分别是Facebook、Apple、Netflix和Google。

亚马逊的热销商品系统就如下图所示。

![](https://static001.geekbang.org/resource/image/df/b0/dff4faae3353f26d7e413a0c1f7983b0.png?wh=1576%2A758)

当我搜索“攀岩鞋”时，搜索结果的第三个被打上了“热销商品”的标签，这样能帮助消费者快速做出购买决策。

当我点击这个“Best Seller”的标签时，我可以浏览“攀岩鞋”这个商品分类中浏览销量最高的前100个商品。

![](https://static001.geekbang.org/resource/image/a7/4c/a7a0b8187b1caf1b31fcda87720e494c.png?wh=1788%2A1262)

这些贴心的功能都是由热销商品系统实现的。

这一讲我们就来看看在这样的热销商品系统中，怎样应用之前所学的Beam数据处理技术吧。今天，我们主要会解决一个热销商品系统数据处理架构中的这几个问题：

1. 怎样用批处理计算基础的热销商品列表、热销商品的存储和serving设计？
2. 怎样设计每小时更新的热销榜单？
3. 怎样设计商品去重处理流水线和怎样根据商品在售状态过滤热销商品？
4. 怎样按不同的商品门类生成榜单？
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/42/ab/75fb1cd6.jpg" width="30px"><span>Tim</span> 👍（0） 💬（1）<div>总算追上进度了，mark下～整理点疑问继续追加过来～</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（10） 💬（0）<div>本讲是这个课程中信息量最高的文章之一 👍👍👍 

不过我相信具体实现中的细节应该还有很多。不知道作者有没有机会分享一下常见的实现误区和pitfall？

除此之外，不知道文章说的这些方案在并发的能力上如何？假如有adhoc+并发的大数据场景，常见的大数据方案似乎在成本上都很高。这算是个大数据上的固有(intrinsic)难题嚒？</div>2019-07-14</li><br/><li><img src="" width="30px"><span>Fiery</span> 👍（3） 💬（0）<div>&quot;按不同的商品门类生成榜单&quot;这个部分，文章只是简单说了一下怎么用API而已，但是实际使用中商品门类非常之多，如何使用合理的方案处理Amazon上千种门类，上万种商品（每种商品可能属于多个门类）的实时销量在pipeline中批量处理的情况？还请仔细讲一下，毕竟是“实战”不是只是过家家的toy app。</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/0a/5f2a9a4c.jpg" width="30px"><span>YZJ</span> 👍（3） 💬（1）<div>有人看明白为啥要用Distinct.withRepresentativeValueFn了么， 我理解就是个普通的转换，将productId转成producetUniqueId, 为什么要用Distinct呢？
</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/68/9468cab4.jpg" width="30px"><span>吴静</span> 👍（2） 💬（2）<div>老师你好，这里有两点疑问：
（1）isSuccessfulSale 和 inStock，不能总是去交易系统实时去查的吧？这样开销会很大。
（2）是否可以最后在处理这个状态？虽然是最后被合并后的值，这样只需要很少的调用次数就可以实现了效果</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5e/c1/cd721d46.jpg" width="30px"><span>_yiunia##远</span> 👍（1） 💬（0）<div>“怎样设计每小时更新的热销榜单”
滑动窗口一小时滚动一次，而数据流在一直拉取，这段时间内的数据都是存在内存里么？不会爆掉么？还是另外有聚合的逻辑</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b0/77e5f8c8.jpg" width="30px"><span>李孟聊AI</span> 👍（0） 💬（0）<div>老师我想问下， PCollection&lt;String&gt;这个种懒加载出来的集合怎么转存成临时的list集合？</div>2019-07-24</li><br/>
</ul>