你好，我是刘超。

上一讲中，我在讲List集合类，那我想你一定也知道集合的顶端接口Collection。在Java8中，Collection新增了两个流方法，分别是Stream()和parallelStream()。

通过英文名不难猜测，这两个方法肯定和Stream有关，那进一步猜测，是不是和我们熟悉的InputStream和OutputStream也有关系呢？集合类中新增的两个Stream方法到底有什么作用？今天，我们就来深入了解下Stream。

## 什么是Stream？

现在很多大数据量系统中都存在分表分库的情况。

例如，电商系统中的订单表，常常使用用户ID的Hash值来实现分表分库，这样是为了减少单个表的数据量，优化用户查询订单的速度。

但在后台管理员审核订单时，他们需要将各个数据源的数据查询到应用层之后进行合并操作。

例如，当我们需要查询出过滤条件下的所有订单，并按照订单的某个条件进行排序，单个数据源查询出来的数据是可以按照某个条件进行排序的，但多个数据源查询出来已经排序好的数据，并不代表合并后是正确的排序，所以我们需要在应用层对合并数据集合重新进行排序。

在Java8之前，我们通常是通过for循环或者Iterator迭代来重新排序合并数据，又或者通过重新定义Collections.sorts的Comparator方法来实现，这两种方式对于大数据量系统来说，效率并不是很理想。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/78/dc/0c9c9b0f.jpg" width="30px"><span>(´田ω田`)</span> 👍（15） 💬（1）<div>感觉这一节课已经值回了整个课程的票价，给老师点赞！

思考题：Stream并行执行，无法确认每个元素的处理顺序，最后parallelList中的数字是无序的</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/5d/c1105c12.jpg" width="30px"><span>一路看风景</span> 👍（13） 💬（2）<div>老师您好，在容器盛行的微服务环境下，以及大数据处理流行的潮流中，我觉得stream的应用空间多少有些尴尬呢，不知是不是我的理解有误。即：单核容器运行的环境下stream没了性能优势，大数据的处理又有大数据平台去完成使命，所以是不是意味着我们可以从stream得到的最大收益变成了流式编程和函数式编程带来的代码易读和易用性了呢？</div>2019-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6PbKL8YRE2wzqdoxcS5E88Wvot8Vv0Kuo92BUKPlWISPfGjSXCmK7vD12aBdibwY6q11gbkPxK4Weje2xCcCdEw/132" width="30px"><span>阿厚</span> 👍（8） 💬（1）<div>老师，请教2个问题：
1.有什么分表分库中间件推荐么？
2.分表分库以后，查询分页怎么办呢？</div>2019-06-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIy5ULaodUwsLoPuk1wd22hqXsaBbibNEqXM0kgrCTYDGKYQkZICYEyH9wMj4hyUicuQwHdDuOKRj0g/132" width="30px"><span>辉煌码农</span> 👍（7） 💬（1）<div>allMatch为什么是短路呢，短路的如何定义的呢</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/38/c3/f18411f9.jpg" width="30px"><span>圣西罗</span> 👍（6） 💬（2）<div>老师，现在网上有些说法做测试用lambda比普通for循环速度慢五倍，因此有人拒绝用。实际情况是什么样呢？如果我自己想测，应该怎么尽可能排除外因干扰，测一下他们的实际效率对比？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（5） 💬（1）<div>是不是该把思考题中的arraylist换成线程安全的copyOnwriteList就可以解决线程不安全问题?</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/59/c75cb36d.jpg" width="30px"><span>N</span> 👍（4） 💬（1）<div>老师有个问题请教一下，公司业务代码中有大量stream对集合遍历，过滤，聚合的用法，但都是串行的，因为大部分数据量不是很大，请问数据量多大的时候才有必要使用并行提高效率呢？</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/52/aa3be800.jpg" width="30px"><span>Loubobooo</span> 👍（4） 💬（1）<div>parallelList集合里呈现的是无序的数字，是这样吗？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/52/ad190682.jpg" width="30px"><span>Mr wind</span> 👍（3） 💬（1）<div>为什么聚合操作是线程安全的呢。</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1e/89/25b12054.jpg" width="30px"><span>Andy</span> 👍（3） 💬（1）<div>感觉stream这种中间操作和终结操作 跟spark中转换操作和处理操作 思想很像，懒加载</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/be/49d49db2.jpg" width="30px"><span>一路奔跑</span> 👍（3） 💬（1）<div>ArraryList是非线性安全的，并行流处理会出现越界或者重复或者少元素的情况！这个坑我踩过！</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/31/16/f2269e73.jpg" width="30px"><span>better</span> 👍（2） 💬（1）<div>目前刚毕业，读起这篇文章觉得有点吃力，特别是到了Stream的源码开始那里，后面基本都看不懂了，老师，是因为现在的实战经验还不够吗</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/56/65b05765.jpg" width="30px"><span>Allen</span> 👍（1） 💬（1）<div>对一个集合进行并行处理 我对比下来 使用显式的线程池进行多线程处理要快于使用 parallel stream  而且使用线程池应该能保证系统线程资源不被耗尽吧 </div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ca/0e/5009c5ff.jpg" width="30px"><span>遇见</span> 👍（1） 💬（1）<div>&quot;这个例子的需求是查找出一个长度最长，并且以张为姓氏的名字&quot;

文稿中的代码只能获取到名字最长的长度吧? 是获取不到名字最长的名字的, 最后的toString只能得到 &quot;OptionalInt[4]&quot; 得不到 &quot;张五六七&quot;

改成:

&quot;names.stream()
                .filter(name -&gt; name.startsWith(&quot;张&quot;)).max(Comparator.comparingInt(String::length))
                .ifPresent(System.out::println);&quot;

才可以打印出来名字</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/6b/8034959a.jpg" width="30px"><span>迎风劲草</span> 👍（1） 💬（1）<div>老师，为什么stream操作，就比自己循环的效率高呢，没看懂。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/41/83275db5.jpg" width="30px"><span>乐</span> 👍（1） 💬（1）<div>那请问老师，思考题中如何解决这种并发时的线程安全问题？是使用 CopyOnWriteArrayList 还是使用 .collect(Collectors.toList())？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（1） 💬（1）<div>并发操作一个ArrayList，会有线程安全问题？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（0） 💬（1）<div>并行操作中，采用的ArrayList容器是线程不安全的，会造成共享数据错误的问题。</div>2019-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（0） 💬（1）<div>ArrayList是非线程安全的，在多线程环境下会出现无需，数据不全，异常等情况</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/8c/5c92c95e.jpg" width="30px"><span>张健</span> 👍（0） 💬（1）<div>老师，拿你的测试代码，测试的时候，发现在1.00E+8 大小下，速度快慢和执行代码的顺序有关，调整顺序执行后，结果完全不一样，最先执行的永远最慢
SerialStreamTest.SerialStreamForObjectTest(studentsList);
ParallelStreamTest.ParallelStreamForObjectTest(studentsList);
IteratorTest.IteratorForObjectTest(studentsList);
</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/8b/76c27279.jpg" width="30px"><span>师志强</span> 👍（0） 💬（1）<div>通过对比发现（在多核场景），能用stream并行就用，不能用就用常规，stream串行好像没有任何优势可言。是不是多有场景中都不建议使用stream串行呢？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/00/c7/59caefa7.jpg" width="30px"><span>ok绷</span> 👍（0） 💬（1）<div>parallelList是非线程安全的，可以使用线程安全的集合类，但是不知道到使用stream的collect方法可以吗？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（1）<div>首先是测试结果，无序的问题是其一，不过也不算问题。另一个问题是，有可能会最后结果只有47~49个值的现象（实际值应该为50个）。并且多次循环的话会报下标越界。
自认为是ArrayList的并发问题。</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/82/374f43a1.jpg" width="30px"><span>假装自己不胖</span> 👍（0） 💬（1）<div>例子中查询长度最长并且以张为姓氏的名字,如果有两个会怎么样</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（0） 💬（1）<div>是因为并行处理并且List是非线程安全的缘故吗？那段代码执行几次后会出现null，把parallel去掉就好了</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/27/a6873bc9.jpg" width="30px"><span>我知道了嗯</span> 👍（0） 💬（1）<div>思考题结果是无序的并且有null值?  这是为什么</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/38/db/6825519a.jpg" width="30px"><span>梁小航航</span> 👍（0） 💬（2）<div>老师，我有一个疑问，就是在例子中查询长度最长并且以张为姓氏的名字。代码在实际运行中maxLenStartwithZ 值为：OptionalInt.empty</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/c9/adc1df03.jpg" width="30px"><span>哲</span> 👍（0） 💬（1）<div>老师，我按你这例子写了一下，执行直接抛数组下标的异常了，这是为何？而且多执行几次，并不是每次都异常，期待您解一下我的疑惑</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（0） 💬（1）<div>老师，我一般使用stream的原因是它这种DSL风格使代码很简洁，并且封装了map，reduce一些操作，最重要的是可并行。
但是stream高效这块我很疑惑，虽然它是在终止操作之前执行中间操作，但它在迭代那些filter不是也是使用的传统的方式吗，而且在数据量不是很大的情况下还会比传统方式要慢一些。</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/74/21/6c64afa9.jpg" width="30px"><span>奔跑的猪</span> 👍（84） 💬（1）<div>实践中大量采用stream大概有2年了吧，先是在Team内推广，后来在CodeReview中强制要求。
个人以为，出发点并不是出于性能考虑，而是结合lambda，在编程思维上的转变，将大家对代码的关注点放在“行为传递”上面，而不是参数传递，阅读时也能省去模板语法产生的“噪音”。</div>2019-07-26</li><br/>
</ul>