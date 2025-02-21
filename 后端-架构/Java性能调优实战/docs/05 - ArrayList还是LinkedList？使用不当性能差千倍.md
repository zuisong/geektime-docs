你好，我是刘超。

集合作为一种存储数据的容器，是我们日常开发中使用最频繁的对象类型之一。JDK为开发者提供了一系列的集合类型，这些集合类型使用不同的数据结构来实现。因此，不同的集合类型，使用场景也不同。

很多同学在面试的时候，经常会被问到集合的相关问题，比较常见的有ArrayList和LinkedList的区别。

相信大部分同学都能回答上：“ArrayList是基于数组实现，LinkedList是基于链表实现。”

而在回答使用场景的时候，我发现大部分同学的答案是：“ArrayList和LinkedList在新增、删除元素时，LinkedList的效率要高于 ArrayList，而在遍历的时候，ArrayList的效率要高于LinkedList。”这个回答是否准确呢？今天这一讲就带你验证。

## 初识List接口

在学习List集合类之前，我们先来通过这张图，看下List集合类的接口和类的实现关系：

![](https://static001.geekbang.org/resource/image/54/09/54f564eb63a2c74723a82540668fc009.jpg?wh=1000x1001)

我们可以看到ArrayList、Vector、LinkedList集合类继承了AbstractList抽象类，而AbstractList实现了List接口，同时也继承了AbstractCollection抽象类。ArrayList、Vector、LinkedList又根据自我定位，分别实现了各自的功能。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/91/50/6aceefec.jpg" width="30px"><span>Rain</span> 👍（76） 💬（1）<div>老师，为什么第二种就会抛出`ConcurrentModificationException`异常呢，我觉得第一种迭代器会抛这个异常啊</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（100） 💬（2）<div>对于arraylist和linkedlist的性能以前一直都是人云亦云，大家都说是这样那就这样吧，我也从来没有自己去验证过，没想过因操作位置的不同差异还挺大。
当然这里面有一个前提，那就是arraylist的初始大小要足够大。
思考题是第一个是正确的，第二个虽然用的是foreach语法糖，遍历的时候用的也是迭代器遍历，但是在remove操作时使用的是原始数组list的remove，而不是迭代器的remove。
这样就会造成modCound != exceptedModeCount，进而抛出异常。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/52/aa3be800.jpg" width="30px"><span>Loubobooo</span> 👍（36） 💬（2）<div>这一道我会。如果有看过阿里java规约就知道，在集合中进行remove操作时，不要在 foreach 循环里进行元素的 remove&#47;add 操作。remove 元素请使用 Iterator方式，如果并发操作，需要对 Iterator 对象加锁。
&lt;!-- 规约第七条 --&gt;</div>2019-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WtHCCMoLJ2DvzqQwPYZyj2RlN7eibTLMHDMTSO4xIKjfKR1Eh9L98AMkkZY7FmegWyGLahRQJ5ibPzeeFtfpeSow/132" width="30px"><span>脱缰的野马__</span> 👍（30） 💬（1）<div>老师您好，在我的认知里面，之所以数组遍历比链表要快，应该还有一个底层的原因，就是源于数组的实现是在内存当中是一块连续的内存空间，而链表所有元素可能分布在内存的不同位置，对于数组这种数据结构来说对CPU读是非常友好的，不管是CPU从内存读数据读到高速缓存还是线程从磁盘读数据到内存时，都不只是读取需要的那部分数据，而是读取相关联的某一块地址数据，这样的话对于在遍历数组的时候，在一定程度上提高了CPU高速缓存的命中率，减少了CPU访问内存的次数从而提高了效率，这是我结合计算机相关原理的角度考虑的一点。</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a6/10/3ff2e1a5.jpg" width="30px"><span>皮皮</span> 👍（18） 💬（1）<div>第一种写法正确，第二种会报错，原因是上述两种写法都有用到list内部迭代器Iterator，而在迭代器内部有一个属性是exceptedmodcount，每次调用next和remove方法时会检查该值和list内部的modcount是否一致，不一致会报异常。问题中的第二种写法remove（e），会在每次调用时modcount++，虽然迭代器的remove方法也会调用list的这个remove（e）方法，但每次调用后还有一个exceptedmodcount=modcount操作，所以后续调用next时判断就不会报异常了。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/e4/abb7bfe3.jpg" width="30px"><span>TerryGoForIt</span> 👍（16） 💬（2）<div>老师您好，我比较好奇的是为什么 ArrayList 不像 HashMap 一样在扩容时需要一个负载因子呢？</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/b2/29b4f22b.jpg" width="30px"><span>JasonZ</span> 👍（12） 💬（8）<div>linkedlist使用iterator比普通for循环效率高，是由于遍历次数少，这是为什么？有什么文档可以参考么？</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（10） 💬（1）<div>测试代码不严谨，建议使用JMH。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f6/df/a576bfce.jpg" width="30px"><span>建国</span> 👍（6） 💬（4）<div>老师，您好，linkList查找元素通过分前后半段，每次查找都要遍历半个list，怎么就知道元素是出于前半段还是后半段的呢？</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（5） 💬（1）<div>modCount属于ArrayList
expectedModCount属于Iterator

增强for循环  本质是iterator遍历
iterator循环  iterator遍历

增强for循环  调用list.remove() 不会修改到iterator的expectedModCount, 从而导致 迭代器的expectedModCount != ArrayList的modCound; 迭代器会抛出 concurrentModifiedException

而iterator遍历 的时候 用iterator. remove(); modCount 会被同步到expectedModCount中去，ArrayList的modCount == Iterator的exceptedModCount，所以不会抛出异常。


老师对其他同学的评论以及我的理解就是这样。</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/cf/b0d6fe74.jpg" width="30px"><span>L.</span> 👍（5） 💬（2）<div>老师，随机访问到底是什么意思？怎么个随机法？谢谢～</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/90/807689c3.jpg" width="30px"><span>Geek_9ius3m</span> 👍（3） 💬（1）<div>老师，什么场景会用到linkedlist呢？我好像只见过Arraylist的代码呢</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（3） 💬（1）<div>请问：List&lt;A&gt; list = new ArrayList&lt;&gt;();
for(int i=0;i++;i&lt;1000){
 A a = new A();
 list.add(a);
}
和
和  这个  List&lt;A&gt; list = new ArrayList&lt;&gt;();
A a;
for(int i=0;i++;i&lt;1000){
 a = new A();
 list.add(a);
}
效率上有差别吗？不说new ArrayList&lt;&gt;(); 初始化问题。单纯说创建对象这一块。谢谢！</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/c9/9a9d82ab.jpg" width="30px"><span>Aaron_涛</span> 👍（2） 💬（2）<div>arrayList，for循环访问快是因为内存连续，可以整个缓存行读取进cpu缓存中，遍历下个的时候无需去内存中获取。并不是实现什么随机获取接口</div>2019-07-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/U5tJTyH25kJA3eAtK0jKTmiaDGkFx4O1yOVjKnbnEQukTjDJCqhlKvLFaIZ6UVp3HcJK3GllMCRfDPU7wodslLQ/132" width="30px"><span>gavin</span> 👍（2） 💬（1）<div>老师好，怎么确定操作集合是从头部、中间、还是尾部操作的呢？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/d6/fbb8236d.jpg" width="30px"><span>DebugDog</span> 👍（2） 💬（1）<div>写法一正确。
虽然都是调用了remove方法，但是两个remove方法是不同的。
写法二是有可能会报ConcurrentModificationException异常。
所以在ArrayList遍历删除元素时使用iterator方式或者普通的for循环。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f0/07/92445721.jpg" width="30px"><span>李德强</span> 👍（1） 💬（5）<div>自己掉坑里了!
ArrayList&lt;String&gt; list = new ArrayList&lt;String&gt;();

        list.add(&quot;a&quot;);
        list.add(&quot;b&quot;);
        list.add(&quot;c&quot;);
        list.add(&quot;d&quot;);
        list.add(&quot;e&quot;);

        for (String item :  list) {
            if (item.equals(&quot;d&quot;)) {
                list.remove(item);
            }
        }

这种移除唯一且倒数第二个的不会报错。
原因时判断hasNext时就返回了false，没有机会去校验modCount了。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（1） 💬（1）<div>写法2不正确，使用for循环遍历元素的过程中，如果删除元素，由于modCount != expectedModCount，会抛出ConcurrentModificationException异常</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（1）<div>需要用迭代器方式删除
for循环遍历删除会抛并发修改异常</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（0） 💬（1）<div>看了老师如下的回答不是很明白，为什么数组过长新增数据的性能就下降了呢？因为数组越长hash碰撞的几率越小，那么性能越高才对。

老师您好，我比较好奇的是为什么 ArrayList 不像 HashMap 一样在扩容时需要一个负载因子呢？

作者回复: HashMap有负载因子是既要考虑数组太短，因哈希冲突导致链表过长而导致查询性能下降，也考虑了数组过长，新增数据时性能下降。这个负载因子是综合了数组和链表两者的长度，不能太大也不能太小。而ArrayList不需要这种考虑。</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>课后思考及问题
请问老师你仔细研究过ArrayList和LinkedList之后，你觉得他们在性能上是否做到了极致？是否还存在优化的空间？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（1）<div>先说思考题   写法1正确，在ForEach遍历，或者fori遍历时，是禁止在内部删除数据的，会报错。

还有就是添加元素和删除元素的问题。这个测试不严谨。没有写明测试环境和测试代码。也没有测试数据。
个人测试的结果是，全都是ArrayList更快。个人表示，也出乎我的意料。最起码在我个人的理解里，链表插入数据明显会更快。 因为不需要考虑数据扩容的问题。</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/06/0b327738.jpg" width="30px"><span>Gankki</span> 👍（0） 💬（1）<div>老师，您好。LinkedList 中 Node 是私有的静态内部类，除了防止内存泄露吗？还有其他的设计考虑吗？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/81/cfc17578.jpg" width="30px"><span>我戒酒了</span> 👍（0） 💬（1）<div>ArrayListTest 的这个测试方法笔误写错了吧	
public static void addFromMidTest(int DataNum) {
		ArrayList&lt;String&gt; list = new ArrayList&lt;String&gt;(DataNum);
		int i = 0;
		
		long timeStart = System.currentTimeMillis();
		while (i &lt; DataNum) {
			int temp = list.size();
			list.add(temp&#47;2+&quot;aaavvv&quot;); &#47;&#47;正确写法list.add(temp&#47;2, +&quot;aaavvv&quot;);
			i++;
		}
		long timeEnd = System.currentTimeMillis();

		System.out.println(&quot;ArrayList从集合中间位置新增元素花费的时间&quot; + (timeEnd - timeStart));
	}</div>2019-07-02</li><br/><li><img src="" width="30px"><span>吃胖了再减肥再吃再健身之谜之不瘦</span> 👍（0） 💬（1）<div>老师，我用的测试代码试了好多次，在“从集合尾部位置新增元素”这个场景下，我测试的结果是“ArrayList&gt;LinkedList”，你代码里面的1000000，一百万次遍历时，会有少量的情况出现“ArrayList&lt;LinkedList”，所以我讲遍历次数增加到10000000，一千万次遍历，测试结果如下
第一次：
ArrayList从集合尾部位置新增元素花费的时间4690
LinkedList从集合尾部位置新增元素花费的时间2942
第二次：
ArrayList从集合尾部位置新增元素花费的时间4655
LinkedList从集合尾部位置新增元素花费的时间2798
第三次：
ArrayList从集合尾部位置新增元素花费的时间5126
LinkedList从集合尾部位置新增元素花费的时间2960

从这个场景看来，大数据量遍历的情况下，LinkedList新增数据比较快，不知道我这个验证的结果是否正确，期待老师指教，谢谢！</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ac/15/935acedb.jpg" width="30px"><span>iusugar</span> 👍（0） 💬（1）<div>老师，可以在代码块多加一些注释吗？有些变量和方法不是很明白。原谅我比较菜...</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（1）<div>第二种remove后加个return就不报错了吧</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（1）<div>实际场景使用中linked list的效率应该还要更低吧？因为要考虑到内存结构紧凑的问题。array list在删除时候移动元素，很大可能是在一个cache line上操作，会很快，但linked list就未必了：写测试代码，linked list的元素总是连贯的。但实际使用场景一定是不连贯的。</div>2019-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLbBZ9iaHfebHH4kOzFvxvs8Hx5iaUruAZvE8Dj4nia0mk4uxLc2rRUZD0ic9uKdxLibib0dGSaibL6NGRUg/132" width="30px"><span>清风拂面</span> 👍（0） 💬（1）<div>文稿关于从头部和尾部插入新元素所用时间那一块反了</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/1d/1cb36854.jpg" width="30px"><span>小辉辉</span> 👍（0） 💬（1）<div>第一种是对的，第二种情况说的就是我之前干过的事情，而且当时出现有时报错，有时不报错。自己踩过的坑，记忆深刻😂😂😂</div>2019-05-30</li><br/>
</ul>