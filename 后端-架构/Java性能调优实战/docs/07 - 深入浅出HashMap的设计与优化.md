你好，我是刘超。

在上一讲中我提到过Collection接口，那么在Java容器类中，除了这个接口之外，还定义了一个很重要的Map接口，主要用来存储键值对数据。

HashMap作为我们日常使用最频繁的容器之一，相信你一定不陌生了。今天我们就从HashMap的底层实现讲起，深度了解下它的设计与优化。

## 常用的数据结构

我在05讲分享List集合类的时候，讲过ArrayList是基于数组的数据结构实现的，LinkedList是基于链表的数据结构实现的，而我今天要讲的HashMap是基于哈希表的数据结构实现的。我们不妨一起来温习下常用的数据结构，这样也有助于你更好地理解后面地内容。

**数组**：采用一段连续的存储单元来存储数据。对于指定下标的查找，时间复杂度为O(1)，但在数组中间以及头部插入数据时，需要复制移动后面的元素。

**链表**：一种在物理存储单元上非连续、非顺序的存储结构，数据元素的逻辑顺序是通过链表中的指针链接次序实现的。

链表由一系列结点（链表中每一个元素）组成，结点可以在运行时动态生成。每个结点都包含“存储数据单元的数据域”和“存储下一个结点地址的指针域”这两个部分。

由于链表不用必须按顺序存储，所以链表在插入的时候可以达到O(1)的复杂度，但查找一个结点或者访问特定编号的结点需要O(n)的时间。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（130） 💬（6）<div>2的幂次方减1后每一位都是1，让数组每一个位置都能添加到元素。
例如十进制8，对应二进制1000，减1是0111，这样在&amp;hash值使数组每个位置都是可以添加到元素的，如果有一个位置为0，那么无论hash值是多少那一位总是0，例如0101，&amp;hash后第二位总是0，也就是说数组中下标为2的位置总是空的。
如果初始化大小设置的不是2的幂次方，hashmap也会调整到比初始化值大且最近的一个2的幂作为capacity。
</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/28/4dcfa376.jpg" width="30px"><span>giserway</span> 👍（58） 💬（4）<div>1）通过将 Key 的 hash 值与 length-1 进行 &amp; 运算，实现了当前 Key 的定位，2 的幂次方可以减少冲突（碰撞）的次数，提高 HashMap 查询效率；
2）如果 length 为 2 的次幂，则 length-1  转化为二进制必定是 11111…… 的形式，在于 h 的二进制与操作效率会非常的快，而且空间不浪费；如果 length 不是 2 的次幂，比如 length 为 15，则 length-1 为 14，对应的二进制为 1110，在于 h 与操作，最后一位都为 0，而 0001，0011，0101，1001，1011，0111，1101 这几个位置永远都不能存放元素了，空间浪费相当大，更糟的是这种情况中，数组可以使用的位置比数组长度小了很多，这意味着进一步增加了碰撞的几率，减慢了查询的效率！这样就会造成空间的浪费。</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/77/423345ab.jpg" width="30px"><span>Sdylan</span> 👍（43） 💬（4）<div>装载因子0.75是怎么算出来了，是经验值还是什么？ 另外为什么链表长度8就要转红黑树呢</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/64/6e458806.jpg" width="30px"><span>大虫子</span> 👍（34） 💬（5）<div>老师您好，能解答下，为什么JDK1.8之前，链表元素增加采用的是头插法，1.8之后改成尾插法了。1.8之前采用头插法是基于什么设计思路呢？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/bb/5cf70df8.jpg" width="30px"><span>嘉嘉☕</span> 👍（30） 💬（3）<div>加载因子那块儿，感觉有点跳跃，为什么加载因子越大，对空间利用越充分呢？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ad/31193b83.jpg" width="30px"><span>孙志强</span> 👍（22） 💬（1）<div>以前看源码，我记得好像链表转换红黑树不光链表元素大于8个，好像还有一个表的大小大于64</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bc/52/52745d32.jpg" width="30px"><span>小小征</span> 👍（13） 💬（10）<div>0 的话索引不变，1 的话索引变成原索引加上扩容前数组。  这句有点不理解 老师</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（11） 💬（2）<div>老师好。hashmap的put和get的时间复杂度算多少啊?最好O(1)。最坏复杂度是O(log(n))平均是O(1)么?。。。treeMap的,treeMap，putO(n)，getO(1)?之前面试被问了，不晓得哪错了</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/3e/c39d86f1.jpg" width="30px"><span>Chocolate</span> 👍（8） 💬（2）<div>老师，您好，请教一个问题，为什么 HashMap 的容量等于数组长度？但是扩容的时候却是根据 Map 里的所有元素总数去扩容，这样会不会导致数组中的某一个 node 有很长的链表或红黑树，数组中的其他位置都没有元素？谢谢</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（4） 💬（1）<div>Hash字典发生扩容时，需要复制元素，请问这个过程是一次完成的吗？redis里的字典是准备了两个字典，一个原始字典，一个rehash字典，扩容后，不是一次完成数据迁移的，每次操作字典都考虑两个数组并复制数据，扩容完毕后交换两个数组指针
</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/56/4e/60e50534.jpg" width="30px"><span>M.c</span> 👍（3） 💬（1）<div>“这是因为链表的长度超过 8 后，红黑树的查询效率要比链表高，所以当链表超过 8 时，HashMap 就会将链表转换为红黑树”，此处转换为红黑树少了个条件吧？MIN_TREEIFY_CAPACITY要同时大于64</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/fa/1cde88d4.jpg" width="30px"><span>大俊stan</span> 👍（3） 💬（1）<div>作者如果把扩容的源码贴出来，可能更好理解是如何扩容，以及为什么多线程hashmap会产生闭环</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bd/13/6424f528.jpg" width="30px"><span>luzero</span> 👍（3） 💬（1）<div>使用2的次幂是因为进行&amp;运算的时候，每次都能落到tables数组内，并且2的次幂进行&amp;运算和直接模运算（%）的值是一样的，也就是说（n-1）&amp;hash==hash%n，如果直接使用（%）模运算最终也会转换成二进制的去计算性能不如&amp;运算，还有就是&amp;计算分布均匀，减少哈希冲突，如果是2的次幂,假设n=16，（16-1）&amp;0==0、（16-1）&amp;1==1、16-1)&amp;2==2、........、（16-1)&amp;19==3、（16-1)&amp;20==4、（16-1)&amp;21==5、。如果不是2的次幂的话，假设是n=15，（15-1）&amp;1==0、（15-1）&amp;1==2、（15-1)&amp;3==2、......、（15-1)&amp;4==4、（15-1)&amp;5==4.    哈哈、不知道我回答的沾不沾边？望老师您点评一下哈</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/df/fc0a6709.jpg" width="30px"><span>WolvesLeader</span> 👍（3） 💬（1）<div>hashmap在多线程情况下数据丢失，大师，能不能分析分析原因</div>2019-06-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/JVOiclOoyFvgJHNXRgqB9RL9UUcQ7k4PByzbDiclrUR4rrSXQBEPpPOQoTSmO90RMPbfeT8d57UDlrOJ6b2gZiaRA/132" width="30px"><span>Geek_n5jcko</span> 👍（3） 💬（1）<div>要是早一天发这个就好了，昨天面试被问到哈希函数给问懵了。老师很棒！这几乎是我在极客跟的最紧的课。</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/57/82f1a3d4.jpg" width="30px"><span>吾爱有三</span> 👍（2） 💬（1）<div>老师您好，1.8中hashmap解决了并发场景的死循环，那么为什么在高并发还是不建议使用hashmap？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/c5/0a727162.jpg" width="30px"><span>曾泽伟</span> 👍（2） 💬（1）<div>再哈希--如果我们不考虑添加元素的时间成本，且对查询元素的要求极高，就可以使用此法
我没太明白，为什么再哈希会提高查询？如果再哈希了，我第一次哈希的位置没查到，得再次哈希查找位置，如果还没有又要再哈希，循环往复，感觉查询性能并不高啊，老师能解释一下吗？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/3b/a1f7e3a4.jpg" width="30px"><span>ZOU志伟</span> 👍（1） 💬（1）<div>假设链表中有4、8、12，他们的二进制位00000100、00001000、00001100，而原来数组容量为4，则是 00000100，以下与运算：

00000100 &amp; 00000100 = 0 保持原位
00001000 &amp; 00000100 = 1 移动到高位
00001100 &amp; 00000100 = 1 移动到高位

这段不理解，为何&amp;运算是0或者1？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/7d/7b9fd831.jpg" width="30px"><span>Fever</span> 👍（1） 💬（1）<div>Hash冲突，那么可以把 key 存放到冲突位置的空位置上去，这里是不是写错了，应该是冲突位置后面的空位置吧？
</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8ibhsSDmHmichVKzxW6vN6Ln2sy8ibOcG8O8akwPDnia98cqLwO29qk4mUqNScwMSlVgOAlgUNw0YnbyosjIJGAibIg/132" width="30px"><span>jimmy</span> 👍（1） 💬（1）<div>请问下为什么链表转换成红黑树的阈值是8？</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/c6/513df085.jpg" width="30px"><span>强哥</span> 👍（1） 💬（1）<div>最主要的原因是位运算替代%取模操作，提高运算性能，说什么降低冲突的，是否比较过质数和偶数冲突概率呢？</div>2019-06-04</li><br/><li><img src="" width="30px"><span>赵玉闯</span> 👍（0） 💬（1）<div>老师，我想问一下，如果数组扩容，是不是应该是基于原来数组尾部继续申请连续的内存空间，也就是原来的二倍，那如果基于原来数组的尾部没有连续的这么大的空间了，怎么办。会去一个新的地方申请原来的二倍空间，然后把这些数据都挪过去吗？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（1）<div>很棒

1.就是被hashmap中链表的 头部 和 尾部搞晕了，老师，是数组里的元素是链表头部还是尾部啊？

2.扩容方法，呜呜呜… 有点想老师也能贴一下扩容源码分析。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/0d/0e65dee6.jpg" width="30px"><span>FelixFly</span> 👍（0） 💬（1）<div>老师，实际应用中，我们设置初始容量，一般得是 2 的整数次幂，这个HashMap在初始化容量的时候会重新计算，会重新计算为2 的整数次幂
我们设置初始容量的要考虑加载因子，设置的初始容量是预知数据量 &#47; 加载因子，假如预知容量是20，算出来的结果是26.6，这样设置的初始容量应该为27，但是计算出来的容量是32（也就是2的5次幂），也就是说这时候的默认边界值为32*0.75=24
还有另一种方法是设置加载因子改为1.0，预售容量是20，设置初始容量为20，加载因子为1.0，这样计算出来的容量是32，也就是说默认边界值是32
这两种方法在实际应用中哪种比较好点</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（0） 💬（1）<div>”这种方法存在着很多缺点，例如，查找、扩容等，所以我不建议你作为解决哈希冲突的首选。”

老师能否讲讲为什么扩容时候有缺点？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（1）<div>老师，这句&quot;因此加载因子越大，对空间的利用就越充分，这就意味着链表的长度越长”，为什么加载因子越大链表长度越长？</div>2019-10-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，hashmap里判断两个对象相不相等先是比较hash函数，而hash函数是hashcode右移16位异或得到的，那么hash函数相同，hashcode一定相同么</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（2）<div>作者回复: 假设链表中有4、8、12，他们的二进制位00000100、00001000、00001100，而原来数组容量为4，则是 00000100，以下与运算：

00000100 &amp; 00000100 = 0 保持原位
00001000 &amp; 00000100 = 1 移动到高位
00001100 &amp; 00000100 = 1 移动到高位

老师，您这个例子的结果说错了吧？
结果应该是1   0   1  吧？
00000100这个也不代表1吧。换算成十进制是4啊。
这个问题，一直不理解，希望老师</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bd/13/6424f528.jpg" width="30px"><span>luzero</span> 👍（0） 💬（1）<div>老师请教一个问题，HashMap 获取元素优化这个章节中的 “例如，重新 key 值的 hashCode() 方法”，是重写？还是重新？ 哈哈哈、我有点搞蒙了哦
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/0c/22cf60a9.jpg" width="30px"><span>Forwardジ</span> 👍（0） 💬（1）<div>老师，hashmap的大小看文章里没讲解，这块怎么总结？</div>2019-06-27</li><br/>
</ul>