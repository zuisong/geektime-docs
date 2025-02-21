在我们日常的程序开发中，不只会用到整数。更多情况下，我们用到的都是实数。比如，我们开发一个电商App，商品的价格常常会是9块9；再比如，现在流行的深度学习算法，对应的机器学习里的模型里的各个权重也都是1.23这样的数。可以说，在实际的应用过程中，这些有零有整的实数，是和整数同样常用的数据类型，我们也需要考虑到。

## 浮点数的不精确性

那么，我们能不能用二进制表示所有的实数，然后在二进制下计算它的加减乘除呢？先不着急，我们从一个有意思的小案例来看。

你可以在Linux下打开Python的命令行Console，也可以在Chrome浏览器里面通过开发者工具，打开浏览器里的Console，在里面输入“0.3 + 0.6”，然后看看你会得到一个什么样的结果。

```
>>> 0.3 + 0.6
0.8999999999999999
```

不知道你有没有大吃一惊，这么简单的一个加法，无论是在Python还是在JavaScript里面，算出来的结果居然不是准确的0.9，而是0.8999999999999999这么个结果。这是为什么呢？

在回答为什么之前，我们先来想一个更抽象的问题。通过前面的这么多讲，你应该知道我们现在用的计算机通常用16/32个比特（bit）来表示一个数。那我问你，我们用32个比特，能够表示所有实数吗？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>lzhao</span> 👍（60） 💬（7）<div>在这样的浮点数表示下，不考虑符号的话，浮点数能够表示的最小的数和最大的数，差不多是 1.17×10−381.17×10−38 和 3.40×10383.40×1038。比前面的 BCD 编码能够表示的范围大多了


这个范围怎么得来的</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/3e/abb7bfe3.jpg" width="30px"><span>小崔</span> 👍（28） 💬（14）<div>对于0.5，按照老师的说法，可以用s = 0、e = -1、f = 0来表示。
但是对照表格，似乎s = 0、e = 0、f = 5也可以表示？请解惑</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（13） 💬（2）<div>如果觉得没有理解老师讲的可以参考阮一峰的一篇文章
http:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2010&#47;06&#47;ieee_floating-point_representation.html</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/7b/191a2112.jpg" width="30px"><span>愤怒的虾干</span> 👍（7） 💬（1）<div>老师，我在java里验证了下，譬如1.9999999f，小数点后的位数，即“9999999”七个9是没办法用8个bit位表示的，我猜测会失去精度变成2.0f，但是调用Float.toHexString发现是0x1.fffffep0，fffffe怎么看都不可能是9999999。于是我换了个数1.5f，16进制浮点数表示为0x1.8p0，可以看到小数点后是8,16进制的一半。这样看的话，上面的小数部分十进制显示是：fffffe&#47;2^23 = 0.9999999，加上小数点前的1就是1.9999999了。
根据这个思路可以推算出规则浮点数最小1.0*2^（-126），最大(1 + (2^23 - 1)&#47;2^23)*2^(127)</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/ac/e5e6e7f3.jpg" width="30px"><span>古夜</span> 👍（7） 💬（1）<div>对于那个公式，底数怎么表示？32位都给了符号位，指数位，小数位，底数怎么办？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（6） 💬（1）<div>如果7位表示0-99的话，32位的取值范围是0-9999999.99。如果需要负数，第一位表示符号位，取值范围是-7999999.99-7999999.99</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/34/ba1c8fc7.jpg" width="30px"><span>任雪龙</span> 👍（5） 💬（1）<div>老师，感觉今天这个讲的太粗糙了，很多东西都是用结果解释结果，比如对 0.5 这个数 s 、e、f 的值，值是从哪里推导得来的都没有解释，希望可以详细解释下</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/00/3afbab43.jpg" width="30px"><span>88591</span> 👍（1） 💬（1）<div>老师，为什么公式定义是 s x 1.f x 2e ,不是s x 2ex 1.f （这种方式更容易对应位数 ：符号位，指数位，有效位数）。</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（1） 💬（1）<div>IEEE754?</div>2019-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（1） 💬（1）<div>老师可以扩展讲一下 移码 毕竟阶码部分并不是我们常见的原码或者补码 也不是移码的常见表示 还有非规格化表示法的由来</div>2019-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3B5MoC4DfBt00nnVshEBFHHkNVgbcBrXsd3SxFicdN3XX5ILOe7GJxKvtJKCY53xNCuxSV8ABxNulbhkibm1lXIw/132" width="30px"><span>林峰峰</span> 👍（0） 💬（1）<div>突然发现今天才知道什么是浮点数...</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/01/c5161563.jpg" width="30px"><span>Geek</span> 👍（13） 💬（1）<div>7个比特的话，99的二进制是1100011，32位里有四个7，那就是99999999，还剩4个比特，正好用来表示一个9，所以最大应该是9999999.99，如果表示负数，第一位是符号位，所以之前剩余的四位，最大是（正）0111和（负）1111，也即是±7，所以结果是-7999999.99-7999999.99</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/bf/5c5e86bb.jpg" width="30px"><span>旺旺</span> 👍（6） 💬（4）<div>0.3无法被精确表达：
1、首先想到会使用这种情况：s=0，e=0，f=11
但却触发了这个特殊规则：当s和e都为0，f不为0时，表达的是0.f
但是，0.f的时候，无论f怎么取值，都无法精确表达0.3。因为0.3的精确二进制表达式1.1</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（3） 💬（2）<div>突然发现，s f e不知道如何表示浮点数1了</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（2） 💬（1）<div>老师，这样一来，1用浮点数咋表示？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/21/c5/024e1ef1.jpg" width="30px"><span>X</span> 👍（1） 💬（0）<div>老师这一章节没有说清楚有效位是怎么来的。
在同学推荐的阮一峰老师的文章里明白了。
http:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2010&#47;06&#47;ieee_floating-point_representation.html
如何得到一个小数的符号位：s，有效位：f，以及指数位：e呢？
5.0为例：
5用二进制表示成：101
0用二进制表示成：0
所以5.0的二进制表示是：101.0
用科学计数法表示成：1.01 * 2 ^ 2 
由于是正数，所有符号位 s=0。
有效位就是 f = 1.01
指数位自然是 e = 2</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/43/e24212bb.jpg" width="30px"><span>o_O</span> 👍（1） 💬（0）<div>打卡，老师也算是领进门吧，想要深入的了解还需要自己查阅相关书籍</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/d7/db041954.jpg" width="30px"><span>haoly1989</span> 👍（1） 💬（0）<div>课后思考题解答：
如果使用7个比特表示连续两位的十进制数，则32个比特位可以划分为1个4比特位后跟着连续的4个7比特位的十进制数，且将最后一个7比特位作为小数部分，注意开头的4比特位可以表示的最大十进制数为9，那么这种表示方法可以表示的最大数为9999999.99；
如果要表示负数，则只需让开头的4比特位中的最高位表示符号位即可，即开头的4比特位可以表示的十进制数范围是-8到7，即整个32比特位可以表示的数值范围是-8999999.99到7999999.99；
</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（0）<div>如果指数位 e 位最大值 255 那么有效位 f 必须为 0，否则就不是一个数 NaN,  这是规定吗？还是有一定的依据的？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/29/58/e4a8093b.jpg" width="30px"><span>范宁</span> 👍（1） 💬（0）<div>老师可以讲一下计算机怎么识别规格化浮点数和非规格化浮点数吗</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/53/f4/8eb1cd8a.jpg" width="30px"><span>Hotin🤓</span> 👍（0） 💬（0）<div>学习了</div>2024-03-31</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>BCD虽然表示的范围小，但是直观，容易理解，并且相对精确；浮点表示法范围大，不容易理解，也不太精确</div>2023-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b5/1e/0e42696c.jpg" width="30px"><span>up</span> 👍（0） 💬（0）<div>列题 ：将（7.0）十进制转换成短浮点数格式。
把十进制转换成二进制。
(7.0)十进制 = （111.0）二进制

规格化二进制
111.0= 1.11✖️2^2

计算出阶码的移码（偏置值 + 阶码真值） 阶码真值就是上面2^k 中的k
127 + 2 = 1111111 + 10 = 10000001

以短浮点数格式存储该数
因为，
符号为 = 0 （正数为0，负数为1）
阶码（E） = 10000001
尾数 = 1100 0000 0000 0000 0000 000 （规格化二进制后小数点后面的数然后用零补齐23位数位）
所以，短浮点数代码为：
0，10000001，1100 0000 0000 0000 0000 000

思路参考：
版权声明：本文为CSDN博主「全 洛」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https:&#47;&#47;blog.csdn.net&#47;weixin_43347550&#47;article&#47;details&#47;110373302</div>2023-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/88/9c/cbc463e6.jpg" width="30px"><span>仰望星空</span> 👍（0） 💬（0）<div>https:&#47;&#47;www.binaryconvert.com&#47;，这个也很好用</div>2023-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/78/4c/61018b26.jpg" width="30px"><span>Suwian</span> 👍（0） 💬（0）<div>“宇宙内的原子的数量，大概在 10 的 82 次方左右，我们就用 1.0×1082 这样的形式来表示这个数值”排版错误了，应该是1.0 x 10^82</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/fb/e76855bc.jpg" width="30px"><span>慧敏</span> 👍（0） 💬（0）<div>我终于明白为什么浮点数无法精确计算小数点了！</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/e7/9ce305ec.jpg" width="30px"><span>Sancho</span> 👍（0） 💬（0）<div>【【CSAPP-深入理解计算机系统】2-4.浮点数(上)】 https:&#47;&#47;www.bilibili.com&#47;video&#47;BV1VK4y1f7o6?share_source=copy_web&amp;vd_source=eea49f3616bea428cb6315f9dcd55caa</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/21/c5/024e1ef1.jpg" width="30px"><span>X</span> 👍（0） 💬（0）<div>定点数：定的这个点就是小数点。如果32位比表示的是有两位小数的实数，那么就需要8位比特表示小数位，1位表示符号位，只剩23位表示数的范围。
浮点数：浮的这个点也是小数点。可以表示的精度更高。相同位的情况下表示的数据范围比定点数大很多很多。
</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/27/f2/50ba2f35.jpg" width="30px"><span>憨豆桑</span> 👍（0） 💬（0）<div>CSAPP上有道题：
求表达式是否总正确。
x==（int）（float）x（假定x的类型是int）。
答案说当x为TMax时表达式错了，没懂。
滴个聪明的老师帮我解答(๑•̀ㅂ•́)و✧</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（0） 💬（0）<div>「大概在 10 的 82 次方左右，我们就用 1.0×1082」，2 排版错误，没有放在指数位置。</div>2022-03-02</li><br/>
</ul>