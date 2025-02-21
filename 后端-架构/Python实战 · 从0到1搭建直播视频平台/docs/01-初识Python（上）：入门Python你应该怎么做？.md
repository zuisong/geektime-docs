你好，我是Barry。

Python的语法简单易学、用途广泛，可以说是当下最火的一门语言。它被广泛地应用在数据分析、爬虫、自动化办公、后端开发、自动化测试、人工智能等领域，可以说上天入地，无所不能。

所以说，我们入门了Python，就等于拿到了开启很多知识的金钥匙。这节课，我们就来入门Python。今天要学的内容比较多，但是不要担心，只要你跟着我把学习思路整理好，掌握起来还是非常容易的。

## 初识Python

我们先简单了解一下Python。

Python 是由 Guido van Rossum 于八十年代末和九十年代初，在荷兰国家数学和计算机科学研究所设计出来的。Python 的设计具有很强的可读性，相比其他编程语言经常使用英文关键字，以及在编写上使用的一些标点符号，Python的语法结构更有特色。

![](https://static001.geekbang.org/resource/image/05/e0/055c989c8677c4a7ff724f6cdfdedee0.jpg?wh=1201x779)

目前Python常用的版本有2.X和3.X。3在2的基础上去繁从简，做了改进。不过，目前使用Python 2 的开发人员也越来越少了，所以我们只学习Python 3就可以了。

Python的语法非常简洁，下面我们尝试用Python输出一句话 “Hello, Python”，感受一下它的语法。

```python
#!/usr/bin/Python3
print ("Hello, Python!")
```
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/88/3814fea5.jpg" width="30px"><span>安静点</span> 👍（3） 💬（1）<div>split是可以根据指定字符来将字符串拆分成一个列表，
而replace则是替换指定字符串为想要的字符</div>2023-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpb7LbMtLNqTYdB04tx47liaZicib9Fy0P1iatp5BEayaiahJUrm6JZaVxSQZIicufrY568GpcuGmOTcVg/132" width="30px"><span>cronusqiu</span> 👍（3） 💬（1）<div>我用 Python 也有个5+年了，深刻感觉Python其实关键的还是在于项目的管理，例如 isort &#47; flake8 &#47; black ，mypy, pylint， unittest, coverage 这些工具的使用， tox工具, setuptools的使用， 遇到很多使用python好几年的，这些工具有些都没听说过， 既然是做项目，这方面感觉可以出一篇详解。看网上一堆教程，都是先教你基础知识，然后中间件，之后各种框架。基本没有人系统的介绍过这些管理工具。。。</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（3） 💬（1）<div>课程一般一周几更?啥时候更,快更新,我要看后面的</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>第一讲打卡~
Python对于初学者来说还是很友好的，基础语法上手很快~</div>2024-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJQYnrTXgWggD3KV8scrKpdupicFibhFzIAenfrBHaMwxibksHzFVaJU3VPTsmiaXfXWZ84FIQYbjCZA/132" width="30px"><span>Geek_7cc417</span> 👍（1） 💬（1）<div>请问作者，我阅读前篇以后，很想购买这个课程，我现在大三，说实话基础没有很好很牢固，想问下学习这门课程要做出这个在线直播平台，需要提前有什么基础吗？有推荐的学习基础的链接吗？我真的很想学完这个课程可以做出这个直播平台，很感兴趣！但是怕基础不够，听不懂</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f5/68/66ce1b44.jpg" width="30px"><span>名</span> 👍（0） 💬（1）<div>split 是拆分，replace  是替换，还有个 join 是添加</div>2024-03-10</li><br/><li><img src="" width="30px"><span>Geek_ffc</span> 👍（0） 💬（1）<div>list没有len方法吧。获取list长度用的是内置函数len()</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b9/50/30eea9a0.jpg" width="30px"><span>BigData～兰兴星</span> 👍（0） 💬（1）<div>文中运算符 is 和 is not的代码示例有两处不足之处，python 3的解释器对  ~~print &quot;data1和data2不包含相同的元素&quot;  ~~ 不支持，应添加（），即print (&quot;data1和data2不包含相同的元素&quot;) ，另外代码的运行结果是不是弄错了，应该是data1和data2不包含相同的元素</div>2023-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/16/b525a71d.jpg" width="30px"><span>zgy</span> 👍（0） 💬（2）<div>list 使用 len 方法提示错误 AttributeError: &#39;list&#39; object has no attribute &#39;len&#39;，我用的是 python 3.11.4 window电脑</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（1）<div>s = &quot;Python,Web,Web,Course&quot;
print(s.split(&quot;,&quot;, 1))                       # 输出：[&#39;Python&#39;, &#39;Web,Web,Course&#39;]
print(s.replace(&quot;Web&quot;, &quot;dev&quot;, 1))   # 输出：Python,dev,Web,Course


split 指定某个字符进行分割，返回一个列表，还可以指定分割几次
replace 是返回一个新的字符串，用指定的字符替换，也可以指定替换几次


splite</div>2023-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/99/44/b0f3a2cc.jpg" width="30px"><span>墨色</span> 👍（0） 💬（1）<div>数学相关的函数divmod不是divmode</div>2023-05-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（0） 💬（1）<div>MYLONG = 40
MyLat = 105
这两个变量命名没有错误吧，只能说是“不是好的命名方式”</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>我没有用过python，工作和直播也没有关系。老师是上市公司研发总监，大牛啊，就是冲着这个才学这门课的。

问题： 我笔记本是win10，装了Anaconda，可以在Anaconda下面练习本课的pythno语法吗？装完Anaconda以后，在哪里输入命令，不太会用啊。
</div>2023-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fho3je5VbEoTkanJOlJVFMp3bu14Bq21D9VGqKgqxvh2vmxwiaZ4EoZM5Ctwtnr3nkQ/132" width="30px"><span>Geek_22e5a7</span> 👍（0） 💬（4）<div>def func(i):    # 判断奇数
    return i % 2 == 1
lst = [1,2,3,4,5,6,7,8,9]
l1 = filter(func, lst)  #l1是迭代器
print(l1)  #&lt;filter object at 0x000001CE3CA98AC8&gt;
print(list(l1))  #[1, 3, 5, 7, 9] #为啥这里报错TypeError: &#39;list&#39; object is not callable</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>In [2]: url = &quot;time.geekbang.org&quot;

In [3]: url.split(&quot;.&quot;)
Out[3]: [&#39;time&#39;, &#39;geekbang&#39;, &#39;org&#39;]

In [4]: url.replace(&quot;.&quot;, &quot;-&quot;)
Out[4]: &#39;time-geekbang-org&#39;</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/73/46/b66c3e80.jpg" width="30px"><span>flybird007</span> 👍（0） 💬（1）<div>变量比较的图有点问题</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/04/3c/9f97f7bd.jpg" width="30px"><span>一米</span> 👍（0） 💬（1）<div># 使用 split() 函数将字符串分割成列表
fruits = &quot;apple,banana,orange&quot;
fruit_list = fruits.split(&quot;,&quot;)
print(fruit_list)  # 输出: [&quot;apple&quot;, &quot;banana&quot;, &quot;orange&quot;]

# 使用 replace() 函数替换字符串中的子字符串
greeting = &quot;Hello World!&quot;
new_greeting = greeting.replace(&quot;World&quot;, &quot;Python&quot;)
print(new_greeting)  # 输出: &quot;Hello Python!&quot;</div>2023-04-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（0） 💬（0）<div>d=10
d&#47;=5
print(d) #2

我这输出是 2.0</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（0） 💬（0）<div>内置函数 split 是字符串根据指定的某个字符(字段)切片会返回一个列表,replace 是将字符串中指定的某个字符替换为你指定的字符并且返回你想要的字符串,总结,Python是一个非常灵活的语言,比如,定义一个变量b=111,后面加个逗号打印出来,你猜会得到什么</div>2023-04-24</li><br/>
</ul>