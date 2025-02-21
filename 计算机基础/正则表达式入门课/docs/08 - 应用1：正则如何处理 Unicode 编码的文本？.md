你好，我是伟忠。这一节我们来学习，如何使用正则来处理Unicode编码的文本。如果你需要使用正则处理中文，可以好好了解一下这些内容。

不过，在讲解正则之前，我会先给你讲解一些基础知识。只有搞懂了基础知识，我们才能更好地理解今天的内容。一起来看看吧！

## Unicode基础知识

**Unicode**（中文：万国码、国际码、统一码、单一码）是计算机科学领域里的一项业界标准。它对世界上大部分的文字进行了整理、编码。Unicode使计算机呈现和处理文字变得简单。

Unicode至今仍在不断增修，每个新版本都加入更多新的字符。目前Unicode最新的版本为 2020 年3月10日公布的13.0.0，已经收录超过 14 万个字符。

现在的Unicode字符分为17组编排，每组为一个平面（Plane），而每个平面拥有 65536（即2的16次方）个码值（Code Point）。然而，目前Unicode只用了少数平面，我们用到的绝大多数字符都属于第0号平面，即**BMP平面**。除了BMP 平面之外，其它的平面都被称为**补充平面**。

关于各个平面的介绍我在下面给你列了一个表，你可以看一下。

![](https://static001.geekbang.org/resource/image/8c/61/8c1c6b9b87f10eec04dbc2224f755d61.png?wh=1660%2A684)

Unicode标准也在不断发展和完善。目前，使用4个字节的编码表示一个字符，就可以表示出全世界所有的字符。那么Unicode在计算机中如何存储和传输的呢？这就涉及编码的知识了。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/39/8c/ff48ece3.jpg" width="30px"><span>小乙哥</span> 👍（10） 💬（6）<div>有点看着蒙圈了，unicode和utf-8不都是编码吗？不都是对字符的编码？他们之间的关系没有搞太清楚</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（10） 💬（12）<div>我的答案：
客重复3次，如果重复的是最后一个字节，就这样‘极(客){3}’, 给客加个括号分组。
请老师指正？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/6e/cd8fea9f.jpg" width="30px"><span>RecordLiu</span> 👍（5） 💬（1）<div>解释一下UTF-8的编码规则，会比较好理解文章中提到的Unicode和UTF-8的转化：
对于单个字节的字符，第一位设为 0，后面的 7 位对应这个字符的 Unicode 码点。因此，对于英文中的 0 - 127 号字符，与 ASCII 码完全相同。这意味着 ASCII 码那个年代的文档用 UTF-8 编码打开完全没有问题。

对于需要使用 N 个字节来表示的字符（N &gt; 1），第一个字节的前 N 位都设为 1，第 N + 1 位设为 0，剩余的 N - 1 个字节的前两位都设位 10，剩下的二进制位则使用这个字符的 Unicode 码点来填充。</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/af/351a9fe7.jpg" width="30px"><span>天蓬太帅</span> 👍（3） 💬（1）<div>请问例子里有一个表达式是findall(r’(?a)^.$’, ‘学’)，这里面的?a是啥意思？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9d/49/372ced1b.jpg" width="30px"><span>Blue D</span> 👍（1） 💬（1）<div>python2中的str等同于python3中的bytes类型，
而python2中的unicode等于python3中的str类型</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/8b/5340fb27.jpg" width="30px"><span>gsz</span> 👍（1） 💬（1）<div>Unicode和gbk编码时，即刻，时间两个词都包含相同的16位数，为什么unicode匹配不了，而gbk的可以匹配？</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/58/102835d4.jpg" width="30px"><span>jooe</span> 👍（1） 💬（2）<div>感谢老师加了 js 的代码示例，对于不会后端语言的还是很友好的</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/51/9d5cfadd.jpg" width="30px"><span>好运来</span> 👍（1） 💬（1）<div>    print(u&#39;正&#39;.encode(&#39;utf-8&#39;))
    # 全角正则和全角字符串，不能匹配到
    print(re.findall(r&#39;＼ｗ＋&#39;, &#39;ａｂｃｄｅｆ&#39;)) # 输出[]
    # 半角正则和全角字符串，能够匹配到
    print(re.findall(r&#39;\w+&#39;, &#39;ａｂｃｄｅｆ&#39;)) # 输出[&#39;ａｂｃｄｅｆ&#39;]
    # 半角正则和半角字符串，能够匹配到
    print(re.findall(r&#39;\w+&#39;, &#39;abcdef&#39;)) # 输出[&#39;abcdef&#39;]
    # 同上
    print(re.findall(r&#39;＼ｄ＋&#39;, &#39;１２３４５６&#39;)) # 输出[]
    print(re.findall(r&#39;\d+&#39;, &#39;１２３４５６&#39;)) # 输出[&#39;１２３４５６&#39;]
    print(re.findall(r&#39;\d+&#39;, &#39;123456&#39;)) # 输出[&#39;123456&#39;]
    # 同上
    print(re.findall(r&#39;＼ｓ＋&#39;, &#39;　　&#39;)) # 输出[]
    print(re.findall(r&#39;\s+&#39;, &#39;　　&#39;)) # 输出[&#39;\u3000\u3000&#39;]
    print(re.findall(r&#39;\s+&#39;, &#39;  &#39;)) # [&#39;  &#39;]

    # “极客{3}”的时候，代表是“客”这个汉字重复 3 次
    re.compile(r&#39;极客{3}&#39;, re.DEBUG)
    print(re.findall(r&#39;极客{3}&#39;, &#39;极客客客&#39;))

    # 思考题没有想到好的解决方法
    print(re.compile(str(u&#39;极客&#39;.encode(&#39;utf-8&#39;)[-1:]).replace(&#39;b&#39;, &#39;&#39;)), re.DEBUG)
</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/03/5b/3cdbc9fa.jpg" width="30px"><span>宁悦</span> 👍（1） 💬（1）<div>py3下测试
re.findall(&#39;极客{3}&#39;, &#39;极客客客客气气气&#39;)
结果：[&#39;极客客客&#39;]</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（1） 💬（1）<div>对编码知识一直模棱两可的，顺着这个再梳理一下吧</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ef/59/6eda594b.jpg" width="30px"><span>octopus</span> 👍（0） 💬（2）<div>客重复三次，如果要极客重复三次‘(极客){3}’</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/ba/304a9a4a.jpg" width="30px"><span>Juntíng</span> 👍（0） 💬（1）<div>JS 语言里, 客重复三次，
重复的是最后一个字节的话,将“客”独立为组再进行</div>2020-08-03</li><br/><li><img src="" width="30px"><span>岁月轻狂</span> 👍（0） 💬（1）<div>老师，点好通配那里，（？a）是什么意思？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/50/c348c2ea.jpg" width="30px"><span>吕伟</span> 👍（0） 💬（1）<div>老师，为什么在sublime text3的正则搜索中输入\p{Han}，没有显示匹配结果。</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/50/c348c2ea.jpg" width="30px"><span>吕伟</span> 👍（0） 💬（1）<div>极(客){3}</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>对于 emoji 表情 ， unicode 没有一个属性可以表示的吗？ 比如 \p{P} 标点符号</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/21/b3394aa2.jpg" width="30px"><span>Robot</span> 👍（0） 💬（3）<div>本来想把python3、pyhon2统一处理为 re.findall(ur&#39;极客{3}&#39;, u&#39;极客客客&#39;)

碰到Unicode类型的统一加u

结果在python3下报错

&gt;&gt;&gt; re.findre.findall(ur&#39;极客{3}&#39;, u&#39;极客客客&#39;)
  File &quot;&lt;stdin&gt;&quot;, line 1
    re.findre.findall(ur&#39;极客{3}&#39;, u&#39;极客客客&#39;)
                        ^
SyntaxError: invalid syntax

</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/21/b3394aa2.jpg" width="30px"><span>Robot</span> 👍（0） 💬（2）<div>课后思考：re.findall(ur&#39;极{3}&#39;, u&#39;极极极&#39;)
</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/28/c0a8f859.jpg" width="30px"><span>Thinker</span> 👍（0） 💬（0）<div>极(?:客){3}</div>2023-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>在使用时一定尽可能地使用 Unicode 编码。--记下来</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>Unicode（中文：万国码、国际码、统一码、单一码）是计算机科学领域里的一项业界标准。它对世界上大部分的文字进行了整理、编码。Unicode 使计算机呈现和处理文字变得简单。</div>2020-10-24</li><br/>
</ul>