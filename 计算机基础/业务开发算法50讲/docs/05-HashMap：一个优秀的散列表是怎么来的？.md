你好，我是微扰君。

过去四讲我们学习了STL中全部的序列式容器，数组、链表、队列、栈；今天来谈一谈另一类容器，关联式容器。所谓“关联式”，就是存储数据的时候，不只是存储元素的值本身，同时对要存储的元素关联一个键，形成一组键值对。这样在访问的时候，我们就可以基于键，访问到容器内的元素。

关联式容器本身其实是STL中的概念，其他高级语言中也有类似的概念。我们这次就以JDK为例，讲解几种关联式容器的原理和实现。

## 统计单词次数

我们就从一个实际需求讲起。现在有一篇很长的英文文档，如果希望统计每个单词在文档中出现了多少次，应该怎么做呢？

如果熟悉HashMap的小伙伴一定会很快说出来，我们开一个HashMap，以string类型为key，int类型为value；遍历文档中的每个单词 `word` ，找到键值对中key为 `word` 的项，并对相关的value进行自增操作。如果该key= `word` 的项在 HashMap中不存在，我们就插入一个(word,1)的项表示新增。

这样每组键值对表示的就是某个单词对应的数量，等整个文档遍历完成，我们就可以得到每个单词的数量了。用Java语言实现这个逻辑也不难。

```
import java.util.HashMap;
import java.util.Map;
public class Test {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        String doc = "aaa bbb ccc aaa bbb ccc ccc bbb ccc ddd";
        String[] words = doc.split(" ");
        for (String s : words) {
            if (!map.containsKey(s)) {
                map.put(s, 1);
            } else {
                map.put(s, map.get(s) + 1);
            }
        }
        System.out.println(map);
    }
}
```

**但是HashMap是怎么做到高效统计单词对应数量的？它设计思路的核心究竟是什么呢**？这个问题非常有意思，我们一起来思考一下。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（6） 💬（1）<div>负载因子定义了扩容时机，在容量和冲突数目取得均衡，一般默认值适合多数情况。个人猜测hashmap用在内存较小的情况下（例如嵌入式系统）应该调整loadfactor，因为这个时候的环境就不是通常环境，需要增加冲突来降低存储。
</div>2021-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOnpl8fRB9r2vED2s8j7Arwbn2K6M6HUBWNjgoqV4uqe94fTGK4WGpOJLeRxXcBXk3dp23eQR0AQ/132" width="30px"><span>吴钩</span> 👍（3） 💬（1）<div>我的理解是：load factor是时间空间权衡的经验参数，当我们明确有时间空间的侧重点时可以改。比如空间不是问题，get的场景多且性能要求高，put的扩容时间损失可以接受，就可以调低load factor，让HashMap多多扩容。</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>假设 n=3
i=0 -&gt; h = 31 * 0 + val[0]
i=1 -&gt; h = 31 * (31 * 0 + val[0]) + val[1]
i=2 -&gt; h = 31 * (31 * (31 * 0 + val[0]) + val[1]) + val[2]
       h = 31*31*31*0 + 31*31*val[0] + 31*val[1] + val[2]
       h = 31^(n-1)*val[0] + 31^(n-2)*val[1] + val[2]</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>
复习 : 如果是2^n 那么只有最高位为1，所以 num &amp; 2^n -1 
也就是 低位全是1 就获取到了取余的数据

11 % 2 

1011 &amp;
0001
= 1</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>31*i 可以直接转化为(i &lt;&lt; 5)- i 看到这句就想起csapp第二章（应该是第二章）</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/42/42/2a04ada9.jpg" width="30px"><span>毛小树</span> 👍（1） 💬（0）<div>为什么hashCode的计算选择31?  1. 一定要奇数。不能用偶数。
2. 素数不素数其实关系不大。
3. 用31是因为31=2^5-1。可以把乘法转换成开销更小的位移操作。提高效率。
</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（0）<div>为什么是31?
https:&#47;&#47;stackoverflow.com&#47;questions&#47;299304&#47;why-does-javas-hashcode-in-string-use-31-as-a-multiplier&#47;299748#299748
排名第一的回答给出了理论公式：31 * i == (i &lt;&lt; 5) - i，但对工程实践意义不大。

要结合排名第二的回答：
【Goodrich and Tamassia computed from over 50,000 English words (formed as the union of the word lists provided in two variants of Unix) that using the constants 31, 33, 37, 39, and 41 will produce fewer than 7 collisions in each case. This may be the reason that so many Java implementations choose such constants.】
正如 Goodrich 和 Tamassia 指出的那样，如果你对超过 50,000 个英文单词（由两个不同版本的 Unix 字典合并而成）进行 hash code 运算，并使用常数 31, 33, 37, 39 和 41 作为乘子，每个常数算出的哈希值冲突数都小于7个，所以在上面几个常数中，常数 31 被 Java 实现所选用也就不足为奇了。

可以看到31是乘子效果最好的最小值，因此选择31是理论+实践的完美数字
</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>哈希表目的是将巨大的稀疏的空间映射到小的连续空间，方法是散列化后再取模，遇到哈希冲突后，可以通过数组+链表的方式解决</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/e9/276b9753.jpg" width="30px"><span>SevenHe</span> 👍（0） 💬（2）<div>我有个疑问，当HashMap量足够大时，扩容所需的rehash开销可能会很大。如果为了保证HashMap的即时可用性，是不是要先在另外开个线程里扩容，在没ready之前，原有容器还可以继续对外提供hash服务。</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/26/4942a09e.jpg" width="30px"><span>猫头鹰爱拿铁</span> 👍（0） 💬（0）<div>resize方法里都会执行lotail=e和hitail=e这个和lotail=lotail.next和hitail=hitail.next是不是等价</div>2022-02-23</li><br/>
</ul>