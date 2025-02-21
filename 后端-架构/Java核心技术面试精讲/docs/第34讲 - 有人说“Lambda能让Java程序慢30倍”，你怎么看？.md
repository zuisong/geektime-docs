在上一讲中，我介绍了Java性能问题分析的一些基本思路。但在实际工作中，我们不能仅仅等待性能出现问题再去试图解决，而是需要定量的、可对比的方法，去评估Java应用性能，来判断其是否能够符合业务支撑目标。今天这一讲，我会介绍从Java开发者角度，如何从代码级别判断应用的性能表现，重点理解最广泛使用的基准测试（Benchmark）。

今天我要问你的问题是，有人说“Lambda能让Java程序慢30倍”，你怎么看？

为了让你清楚地了解这个背景，请参考下面的代码片段。在实际运行中，基于Lambda/Stream的版本（lambdaMaxInteger），比传统的for-each版本（forEachLoopMaxInteger）慢很多。

```
// 一个大的ArrayList，内部是随机的整形数据
volatile List<Integer> integers = …
 
// 基准测试1
public int forEachLoopMaxInteger() {
   int max = Integer.MIN_VALUE;
   for (Integer n : integers) {
  	max = Integer.max(max, n);
   }
   return max;
}
 
// 基准测试2
public int lambdaMaxInteger() {
   return integers.stream().reduce(Integer.MIN_VALUE, (a, b) -> Integer.max(a, b));
}
```

## 典型回答

我认为，“Lambda能让Java程序慢30倍”这个争论实际反映了几个方面：

第一，基准测试是一个非常有效的通用手段，让我们以直观、量化的方式，判断程序在特定条件下的性能表现。

第二，基准测试必须明确定义自身的范围和目标，否则很有可能产生误导的结果。前面代码片段本身的逻辑就有瑕疵，更多的开销是源于自动装箱、拆箱（auto-boxing/unboxing），而不是源自Lambda和Stream，所以得出的初始结论是没有说服力的。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/4d/e24fc9e4.jpg" width="30px"><span>蔡光明</span> 👍（25） 💬（1）<div>杨老师，我今天去面试的时候，java基础知识答的还可以，就是面试官扩展着问，问到spring和springcloud框架时就有些懵了，请问我现在应该如何学习，spring一直都是懂得不是很多，仅限于会用，杨老师能推荐一些相关的学习资料吗</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/90/d63f8347.jpg" width="30px"><span>yushing</span> 👍（11） 💬（1）<div>请问杨老师，无效代码消除后，mul的计算不执行了，那left和right也就没有使用了，是不是left和right的赋值语句也会被判断为无效代码不执行了呢？</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/b0/9335798e.jpg" width="30px"><span>I</span> 👍（6） 💬（3）<div>那就是可以使用，凡涉及性能要求严格的情况下就不用。既然这样，Java费尽力气开发出一个性能不行的东西出来，只为了减少代码量和支持函数式吗，还有并行并没有带来想象中的优势吗，所谓的免费的并行，却不可以轻易免费使用，本人基础一般，望作者指点一二，谢谢！</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/fb/52a662b2.jpg" width="30px"><span>spark</span> 👍（14） 💬（8）<div>专栏写的好，像流水和故事。大概技术像作者的开发人员可以毕业了</div>2018-07-25</li><br/><li><img src="" width="30px"><span>ddv</span> 👍（6） 💬（0）<div>lambda这一块如果能够单独拎出来说一说
比如他的底层实现是如何决定了他的效率
以及java在函数引用这一块的尝试
这是一个很有意思的语言特点 希望作者有空可以做一个专集</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/13/0d3c5008.jpg" width="30px"><span>最好不过</span> 👍（4） 💬（0）<div>因为第一次调用lamda时初始化的开销比较大，会进行动态时生产lambda的相干类，加载额外的ASM框架，编译时间较长；因此如果我们测试本文的中的测试只是测试了第一次的调用的时间，当进行预热之后，lambda的测试时间和普通for循环相差不大。详细原因可以看这篇文章https:&#47;&#47;juejin.cn&#47;post&#47;6844904202439753741</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/13/8b/422997c5.jpg" width="30px"><span>twc</span> 👍（2） 💬（2）<div>“Of course it’s not always the case, but in this pretty common example, it showed it can be around 5 times worse.&quot; 
引用的文章说 lamda 在 &quot; 普通”情况下， lamda是慢了 5倍。
杨老师在质疑 测试的环境不够标准，通篇读下来没有看到结论？ 不知用了lamda 到底是快了还是慢了</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ba/ec/2b1c6afc.jpg" width="30px"><span>李飞</span> 👍（1） 💬（0）<div>对性能调优这块实操涉及的不多，先做学习吧，后期再回头学第二遍</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（0） 💬（0）<div>lambda看起来有太多的缺点，那我们为什么要用他呢？我理解的是函数式编程在并行计算上的优势</div>2019-04-09</li><br/>
</ul>