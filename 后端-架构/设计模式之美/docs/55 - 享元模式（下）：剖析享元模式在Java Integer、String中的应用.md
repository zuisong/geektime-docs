上一节课，我们通过棋牌游戏和文本编辑器这样两个实际的例子，学习了享元模式的原理、实现以及应用场景。用一句话总结一下，享元模式中的“享元”指被共享的单元。享元模式通过复用对象，以达到节省内存的目的。

今天，我再用一节课的时间带你剖析一下，享元模式在Java Integer、String中的应用。如果你不熟悉Java编程语言，那也不用担心看不懂，因为今天的内容主要还是介绍设计思路，跟语言本身关系不大。

话不多说，让我们正式开始今天的学习吧！

## 享元模式在Java Integer中的应用

我们先来看下面这样一段代码。你可以先思考下，这段代码会输出什么样的结果。

```
Integer i1 = 56;
Integer i2 = 56;
Integer i3 = 129;
Integer i4 = 129;
System.out.println(i1 == i2);
System.out.println(i3 == i4);
```

如果不熟悉Java语言，你可能会觉得，i1和i2值都是56，i3和i4值都是129，i1跟i2值相等，i3跟i4值相等，所以输出结果应该是两个true。这样的分析是不对的，主要还是因为你对Java语法不熟悉。要正确地分析上面的代码，我们需要弄清楚下面两个问题：

- 如何判定两个Java对象是否相等（也就代码中的“==”操作符的含义）？
- 什么是自动装箱（Autoboxing）和自动拆箱（Unboxing）？

在[加餐一](https://time.geekbang.org/column/article/166698)中，我们讲到，Java为基本数据类型提供了对应的包装器类型。具体如下所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/25/40/4d68fa96.jpg" width="30px"><span>一丨丿丶乙</span> 👍（1） 💬（1）<div>享元---&gt;复用，线程池等。通过复用对象，以达到节省内存的目的
1.懒加载，dubble check
2.weak reference持有享元对象</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（1） 💬（1）<div>为什么说垃圾回收的时候如果保存了对象的&quot;引用&quot;就不友好，垃圾回收的依据不是只看这个对象还有没有被&quot;使用&quot;吗？ </div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（76） 💬（7）<div>享元池用weak reference持有享元对象</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（52） 💬（8）<div>如果IntegerCache不事先指定缓存哪些整形对象，那么每次用到的时候去new一个，这样会稍微影响一些效率，尤其在某些情况下如果常用到-128~127之间的数，可能会不停的new&#47;delete, 不过这个性能问题在大部分时候影响不是很大，所以按照string的设计思路也是可行的，
按照这个思路设计IntegerCache类的话，如下
private static class IntegerCache {

    public static final WeakHashMap&lt;Integer, WeakReference&lt;Integer&gt;&gt; cache = 
        new WeakHashMap&lt;Integer, WeakReference&lt;Integer&gt;&gt;(); &#47;&#47;也可以提前分配容量

    private IntegerCache(){}
}

public static Integer valueOf(int i) { 
    final WeakReference&lt;Integer&gt; cached = IntegerCache.cache.get(i);
    if (cached != null) {
        final Integer value = cached.get(i);
        if (value != null) {
            return value;
        }
    }
    WeakReference&lt;Integer&gt; val = new WeakReference&lt;Integer&gt;(i);
    IntegerCache.cache.put(i, val);
    return val.get(); 
}</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（48） 💬（7）<div>谢谢各位的讨论，今天学到了软引用，弱引用，和WeakHashMap。内存吃紧的时候可以考虑使用WeakHashMap。
https:&#47;&#47;www.baeldung.com&#47;java-weakhashmap
https:&#47;&#47;www.baeldung.com&#47;java-soft-references
https:&#47;&#47;www.baeldung.com&#47;java-weak-reference</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（32） 💬（0）<div>设计模式_55:
# 作业
原来还有个WeakHashMap，学习了。

# 感想
自己尝试了写了一个，然后分别测试了10,000次、100,000次，1,000,000次创建，value从1-100，100-200，10000-10100，发现不管哪个场景，总是JVM的Integer时间更短，我写的要3倍左右的时间，不禁感叹，Java二十几年了，大部分的优化应该都做了，不要期望自己花20分钟能改出超过JVM的性能。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（25） 💬（1）<div>课后题。因为整型对象长度固定，且内容固定，可以直接申请一块连续的内存地址，可以加快访问，节省内存？而String类不行。</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/dd/88fa7b52.jpg" width="30px"><span>Geek_41d472</span> 👍（14） 💬（0）<div>我勒个擦 ,这好像是我碰到的两道面试题,包装和拆箱这道题简直就是个坑,有踩坑的举个手</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（10） 💬（1）<div>抛砖引玉实现了一个有限范围的缓存（-128~2048383(127 * 127 * 127)）
public class IntegerCache {
    private static final int bucketSize = 127;
    private static final int level1Max = bucketSize * bucketSize;
    private static final int max = bucketSize * bucketSize * bucketSize;
    private static final WeakHashMap&lt;Integer, WeakHashMap&lt;Integer, WeakHashMap&lt;Integer,WeakReference&lt;Integer&gt;&gt;&gt;&gt; CACHE = new WeakHashMap&lt;&gt;();

    public static Integer intern(int integer) {
        if (integer &lt;= 127) {
            return integer;
        }

        if (integer &gt; max) {
            return integer;
        }

        synchronized (CACHE) {
            Integer l1 = 0;
            int tmp = integer;
            if(integer &gt;= level1Max){
                l1 = integer &#47; level1Max;
                integer -= level1Max;
            }
            Integer l2 = integer &#47; bucketSize;
            Integer mod = integer % bucketSize;
            WeakHashMap&lt;Integer, WeakHashMap&lt;Integer,WeakReference&lt;Integer&gt;&gt;&gt; level1 = CACHE.computeIfAbsent(l1, val -&gt; new WeakHashMap&lt;&gt;());
            WeakHashMap&lt;Integer,WeakReference&lt;Integer&gt;&gt; level2 =  level1.computeIfAbsent(l2, val -&gt; new WeakHashMap&lt;&gt;());
            WeakReference&lt;Integer&gt; cache = level2.computeIfAbsent(mod, val -&gt; new WeakReference&lt;&gt;(tmp));
            Integer val = cache.get();
            if (val == null) {
                val = integer;
                level2.put(mod, new WeakReference&lt;&gt;(val));
            }
            return val;
        }

    }

    public static int integersInCache() {
        synchronized (CACHE) {
            int sum = CACHE.size();
            for (Integer key : CACHE.keySet()) {
                WeakHashMap&lt;Integer, WeakHashMap&lt;Integer,WeakReference&lt;Integer&gt;&gt;&gt; tmp = CACHE.get(key);
                sum += tmp.size();
                for(Integer l2Key : tmp.keySet()) {
                    sum += tmp.get(l2Key).size();
                }
            }
            return sum;
        }
    }
}</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/00/7daa7403.jpg" width="30px"><span>Eden Ma</span> 👍（9） 💬（2）<div>突然理解OC中NSString等也用到了享元设计模式.</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/eb/e7127bb8.jpg" width="30px"><span>，</span> 👍（7） 💬（9）<div>补充 深入理解java虚拟机 里的两道有意思的题,请思考输出结果:
自动装箱 拆箱:
 public static void main(String[] args){
        Integer a = 1;
        Integer b = 2;
        Integer c = 3;
        Integer d = 3;
        Integer e = 321;
        Integer f = 321;
        Long g = 3L;
        System.out.println(c==d);
        System.out.println(e==f);
        System.out.println(c==(a+b));
        System.out.println(c.equals(a+b));
        System.out.println(g ==(a+b));
        System.out.println(g.equals(a+b));
    }

考察知识点:Integer缓存,equals和==
字符串:
 public static void main(String[] args) {
        String str1 = new StringBuilder(&quot;计算机&quot;).append(&quot;软件&quot;).toString();
        System.out.println(str1==str1.intern());
        String str2 = new StringBuilder(&quot;ja&quot;).append(&quot;va&quot;).toString();
        System.out.println(str2==str2.intern());
    }
考察知识点:1.intern的作用;2.玩</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/41/2d477385.jpg" width="30px"><span>柠檬C</span> 👍（5） 💬（0）<div>可以使用weakReference，当没有其他变量引用时，被JVM回收</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/47/f6c772a1.jpg" width="30px"><span>Jackey</span> 👍（5） 💬（0）<div>这节的例子可以拿来做笔试的题目😃</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/58/62/346dd248.jpg" width="30px"><span>Q罗</span> 👍（4） 💬（0）<div>享元模式讲解很透彻，赞👍</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/8d/d725d32c.jpg" width="30px"><span>李德政</span> 👍（3） 💬（0）<div>终于明白了Python中[-5,256)之间的整数的地址id都是一样的</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/5b/ff28088f.jpg" width="30px"><span>郑大钱</span> 👍（2） 💬（0）<div>听说过很多次字符串的常量池，却没有真正去理解过。原来就是享元模式</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（2） 💬（4）<div>新的一周开始了，坚持跟下去</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（2） 💬（4）<div>打卡 
做java 的我第一题竟然做错了
如果定义为int 就返回ture 了吧😂</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ef/0e/bbc35830.jpg" width="30px"><span>一杯绿绿</span> 👍（1） 💬（0）<div>性能的角度来看 IntegerCache，JDK 的加载类时创建好 Integer 缓存有如下的优势：
1. 不需要考虑并发问题（加锁）。
2. 可以直接使用 Integer cache[] 数组来存储，数组在计算机上有天然的空间、时间局部性，这对性能的提升会很大。

而且 JDK 的 Integer 有了上述优势后，设计上也简化了很多，不需要引入 map 等复杂的数据结构和考虑并发问题，只需要一个数组即可。</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/7a/d44df1d6.jpg" width="30px"><span>freesocean</span> 👍（1） 💬（0）<div>思考：
1.这里借鉴字符串常量池的话，我想到可以用一个HashMap保存使用过的Integer对象，其中key和value都是该Integer。在要创建Integer时，先判断Map中是否已经存在，如果有就复用，如果没有就新建一个，并放入Map.
2.考虑到很多Integer对象可能使用一次，随着时间推移，Map中会保存大量不会再使用的对象，而Map对其的引用如果是强引用，这些对象就不会被JVM垃圾回收。按照思考题的要求：要在没有任何代码使用时，进行回收，这种行为如果用软引用，可以减轻内存压力，但是jvm的垃圾回收并不保证一定回收软引用，只是在内存不够时，会优先回收软引用。</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/c8/15f055d3.jpg" width="30px"><span>图灵机</span> 👍（1） 💬（0）<div>曾经用== 比较两个Integer的值，用小于127的数测的仿佛没问题，险些酿成大祸</div>2020-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/43/3e/960d12cb.jpg" width="30px"><span>DY</span> 👍（1） 💬（0）<div>老师的文章越往后面越牛</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/e6/7808520d.jpg" width="30px"><span>Edward Lee</span> 👍（1） 💬（1）<div>我倒是想了解一下 String 常量池的最大能缓存的大小</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/be/5cf3f1a0.jpg" width="30px"><span>junshuaizhang</span> 👍（1） 💬（0）<div>终于弄明白困扰我多年的问题了。另外评论区很多精华呀</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（1） 💬（0）<div>&#47;&#47;调用例子
public class FlyweightExample {
    public static void main(String[] args) {
        Integer i = IntegerCache.intern(16129);
        System.out.println(&quot;16129:&quot; + i);

        i = IntegerCache.intern(1612);
        System.out.println(&quot;1612:&quot; + i);

        i = IntegerCache.intern(161);
        System.out.println(&quot;161:&quot; + i);

        i = IntegerCache.intern(127);
        System.out.println(&quot;127:&quot; + i);

        i = IntegerCache.intern(100);
        System.out.println(&quot;100:&quot; + i);

        i = IntegerCache.intern(16129);
        System.out.println(&quot;16129:&quot; + i);

        i = IntegerCache.intern(1612);
        System.out.println(&quot;1612:&quot; + i);

        i = IntegerCache.intern(161);
        System.out.println(&quot;161:&quot; + i);

        i = IntegerCache.intern(2048383);
        System.out.println(&quot;2048383:&quot; + i);

        i = IntegerCache.intern(16130);
        System.out.println(&quot;16130:&quot; + i);

        i = IntegerCache.intern(2048383);
        System.out.println(&quot;2048383:&quot; + i);

        i = IntegerCache.intern(16130);
        System.out.println(&quot;16130:&quot; + i);

        System.out.println(&quot;Integer objects in cache: &quot; + IntegerCache.integersInCache());
    }
}</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（1） 💬（0）<div>打卡 今天学习享元模式（下），收获进一步加深了对String类的字符串常量池的理解。在jdk中Integer和String都使用了享元模式来存储享元对象。
Integer类会存储-128~127之间的数字对应的包装类型对象，这些对象的创建时在类初始化阶段就创建好的。String类在运行时使用JVM提供的一块称之为“字符串常量池”的区域中来存储首次使用到的字符串常量，当后面再次使用到该常量时，直接去字符串常量池中取出引用使用即可。由于使用工厂来来存储享元对象，使得享元对象在JVM的根搜索算法中GC Roots可达，因此垃圾回收效果不友好。
课堂讨论题中的“并且能够做到在某个对象没有任何代码使用的时候，能被 JVM 垃圾回收机制回收掉” 对垃圾回收机制理解不深，不知道有啥好办法。</div>2020-03-09</li><br/><li><img src="" width="30px"><span>Geek_d99793</span> 👍（0） 💬（0）<div>&quot;String 类的享元模式的设计没法事先知道要共享哪些字符串常量，所以没办法事先创建好，只能在某个字符串常量第一次被用到的时候，存储到常量池中&quot;
享元模式前提是享元对象是不可变对象，这里又动态新增到常量池，是不是有点矛盾？</div>2024-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（0） 💬（0）<div>使用弱引用</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/dd/41614582.jpg" width="30px"><span>HomeyLiu</span> 👍（0） 💬（0）<div>最牛逼的做法是 linkHashMap&lt; Integer, SoftReference&lt; Integer &gt;&gt; ,实现LRU淘汰算法.
防止OOM.
Weak引用太弱了,gc就被回收,重复创建浪费cpu.
</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/90/0a/50f89814.jpg" width="30px"><span>dexia</span> 👍（0） 💬（1）<div>字符串常量池满了之后会OOM吗，GC不清理常量池的话那常量池满了怎么办？</div>2021-09-10</li><br/>
</ul>