上一节课我跟你分享了数据挖掘的最佳学习路径，相信你对接下来的学习已经心中有数了。今天我们继续预习课，我会用三篇文章，分别对Python的基础语法、NumPy和Pandas进行讲解，带你快速入门Python语言。如果你已经有Python基础了，那先恭喜你已经掌握了这门简洁而高效的语言，这几节课你可以跳过，或者也可以当作复习，自己查漏补缺，你还可以在留言区分享自己的Python学习和使用心得。

好了，你现在心中是不是有个问题，要学好数据分析，一定要掌握Python吗？

我的答案是，想学好数据分析，你最好掌握Python语言。为什么这么说呢？

首先，在一份关于开发语言的调查中，使用过Python的开发者，80%都会把Python作为自己的主要语言。Python已经成为发展最快的主流编程语言，从众多开发语言中脱颖而出，深受开发者喜爱。其次，在数据分析领域中，使用Python的开发者是最多的，远超其他语言之和。最后，Python语言简洁，有大量的第三方库，功能强大，能解决数据分析的大部分问题，这一点我下面具体来说。

Python语言最大的优点是简洁，它虽然是C语言写的，但是摒弃了C语言的指针，这就让代码非常简洁明了。同样的一行Python代码，甚至相当于5行Java代码。我们读Python代码就像是读英文一样直观，这就能让程序员更好地专注在问题解决上，而不是在语言本身。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>米可哲</span> 👍（36） 💬（3）<div>online judge 会不会要求太高，一般水平的人刷leetcode就足够了吧？？</div>2018-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a2/c8/f8753e06.jpg" width="30px"><span>Hyperuniverse</span> 👍（139） 💬（3）<div>刷题网站:
1、LeetCode
2、Kaggel
3、老师推荐的Online Judge

Python入门：就看这本足够了——《Python编程：从入门到实践》

IDE：pycharm（写爬虫）、jupyter notebook+spyder3（数据分析主要IDE）、Sublime Text 3（牛逼的编辑器）

数据库：PGsql（挺好用的）、Mysql（开源，主流）

py版本：毫不犹豫选择py3（应为2020年py2停止维护了）

提升：没啥好说的，就是“干”，多写多练自然有感觉了，对，当你写多了代码，你看问题的层次也将不一样。所以，对自己狠心一点，不要一直在入门徘徊。
</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/50/d3b4f8c4.jpg" width="30px"><span>●</span> 👍（95） 💬（3）<div>Q1:不是python内置库
采用命令行安装库pip install scikit-learn
引用库 import scikit-learn
Q2:
方法一：sum函数
print(sum(range(1,100,2)))
方法二：if迭代
a = 0
for i in range(1,100,2):
	a += i 
print(a)
方法三：while循环
i = 1
b = 0
while i &lt; 100:
	if i % 2 != 0 :
		b += i
	i +=1
print(b)</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/e2/3640e491.jpg" width="30px"><span>小熊猫</span> 👍（47） 💬（3）<div>1. pycharm、sublime、jupyter都用过，个人认为Pycharm适合比较大一点的项目，平时自己开发一些小脚本什么的可以用sublime，比较简洁方便，目前一直在用Jupyter，比较适合做数据分析，显示图表之类的，可视化、一行代码一个结果都很方便，今天的课程已经用Jupyter全部写了一遍。
2. 求和：sum(range(1, 100, 2))
sum(iterable, start)，sum的输入是iterable对象，比如list、tuple、set等
range()的返回值就是一个iterable对象，可以直接作为sum的输入参数
3. 前面有位同学一直出现 ‘int’ object is not iterable.的错误，我今天用Jupyter也碰到了，应该是前面老师的例子中用了sum做变量，后面求和这道题再用sum()做函数，所以出错了， 重启下Jupyter就行了，或者用魔法命令%reset清除变量应该也可以。
4. 吐槽下极客时间里不能回复其他人的留言，只有老师才能，这个功能需要完善下
</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（20） 💬（2）<div>第一道题：
import scikie-learn

第二道题：
方法一：用for循环
sum=0
for number in range(1,100,2):
     sum = sum + number
print sum
方法二：用while
sum =0
number = 1
while number &lt; 100:
        sum = sum + number
        number = number +2
print sum</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a9/a7/de3ee890.jpg" width="30px"><span>拉我吃</span> 👍（19） 💬（1）<div>p1.
要先安装库
pip install -U scikit-learn

代码里写
import sklearn

p2. 
代码 sum(range(1, 99, 2)) 直接求和
print(sum(range(1, 99, 2))) 打印出来
</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d4/47/6d9f2da6.jpg" width="30px"><span>Miracle</span> 👍（12） 💬（2）<div>sklearn库是机器学习领域好用到哭的一个库，数据清洗，各种机器学习算法都给写好了，我们可以直接使用，学习sklearn感觉最好的方式就是通过官方文档学习：https:&#47;&#47;scikit-learn.org&#47;stable&#47;，但是在这之前最好先跟着教程过一遍sklearn，至少知道什么问题应该用什么算法等，然后再通过查阅文档进行补充。 使用的时候也很简单，pip install安装，然后import sklearn 或者 from sklearn import 模块等。  关于学习Python，我觉得可以找一个简单的教程（B站上好多）跟一遍，掌握基础的语法和使用，然后就是刷题或者项目中提高代码编程能力，在这个途中遇到不懂得可以查阅Python的官方文档进行知识补充。 我觉得官方文档是最好的学习方式。</div>2020-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/e4/7c16516d.jpg" width="30px"><span>大萌</span> 👍（10） 💬（1）<div>1、安装完成后 import sklearn
2、
（1）采用for循环
sum = 0
for i in range(1,100,2):
    sum+=i
print(sum)
（2）采用递归方法
def sum(x):
	if x&gt;99:
		return 0
	num = sum(x+2)
	return x+num
print(sum(1))
平常编程会用jupyter notebook，也可以推荐一下</div>2018-12-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（9） 💬（3）<div>实话说，这篇读起来“有点卡”，应该是没有编程基础的缘故。晚上下班回来鼓捣半天，最后给笔记本装了Anaconda，但是类似“Python中%的含义”就让我百度了半小时才搞懂。
逻辑不难懂，甚至看完这篇觉得貌似入门Python并不难，关键是想自己写出来就得花点功夫、在搞懂的基础上多做练习了。
买了从零学Python的视频课，也找到了《Python：从入门到实践》电子书，打算这周末先研究下再回来看。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/97/6f/3853f003.jpg" width="30px"><span>虎皮青椒</span> 👍（6） 💬（1）<div>1.如果我想在Python中引用scikit-learn库该如何引用？
1）scikit-learn安装
	Python中安装scikit-learn之前需要以下先决条件：
	- Python(&gt;= 2.6 or &gt;= 3.3)
	- NumPy (&gt;= 1.6.1)
	- SciPy (&gt;= 0.9)
	1.1）安装numpy
		sudo pip install numpy
	1.2）安装安装scipy
		需要先安装matplotlib、ipython、ipython-notebook、pandas、sympy
		sudo apt-get install python-matplotlib ipython ipython-notebook
		sudo apt-get install python-pandas python-sympy python-nose
		sudo pip install scipy
	1.3）安装scikit-learn
		sudo pip install -U scikit-learn
	1.4）测试
		查看pip安装是否有sklearn这一项
		pip list | grep sklearn		
2）导入scikit-learn库
	from sklearn import *
	
2.求1+3+5+7+…+99的求和，用Python该如何写？
sum = 0
for number in range(1, 100, 2):
	sum += number
print(&quot;1 + 3 + 5 + 7 + … + 99的求和为%d&quot; % sum)</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/27/791d0f5e.jpg" width="30px"><span>小林子</span> 👍（4） 💬（1）<div>第一题：
import sklearn

第二题：
sum([i for i in range(1,99,2)])</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/68/90/ca86abe3.jpg" width="30px"><span>CHEN</span> 👍（3） 💬（1）<div>print(sum([i for i in range(1,100,2)]))</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3d/e1/5279ea2f.jpg" width="30px"><span>鱼鱼鱼培填</span> 👍（3） 💬（1）<div>看错题目了，第二题应该是：
sum = 0
for i in range(1, 100, 2):
	sum += i
print(sum)</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5d/70/b44af625.jpg" width="30px"><span>nsyao</span> 👍（2） 💬（2）<div>关于ide选择部分，建议老师改一下。其实sunlime不合适新手，反而是anaconda套件更合适，spyder或jupyter对新手都很友好</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/75/1a/395242db.jpg" width="30px"><span>土豆</span> 👍（2） 💬（1）<div>正好疫情在家封闭期间读完了 learning python英文版本，这本书虽然比较厚，1500页，但是是我读过的最好的python入门服务。所以我算是pyrhon入门了，回头再刷刷老师推荐的oj题目</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ba/6d318c08.jpg" width="30px"><span>GS</span> 👍（2） 💬（1）<div>连加用高斯算法 
def sum(n):
  return（1+n）n&#47;2  </div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/6c/ee/8d0790e4.jpg" width="30px"><span>MASK</span> 👍（1） 💬（1）<div>1,引入库我会这样做
1)pip install scikit-learn
2）如果我嫌它太长我可以给它换一个简单一点的名字在应用的时候
from scikit-learn import as sc
2，我会利用一个循环来做，首先因为循环的次数是可以确定的，所以我会选择for 循环，循环不确定的呢话可以选择while，当然这题两种都可以，我就选择for循环来实现吧，
直接上代码
num = 0
for i in range(1,101):
    num += i
print (num)

</div>2020-07-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJ08FfEl3UAicj1gl00uo5LQibicBKKUf8AMUXueAaib0tLIdHMnDMorJCfsMMcwOUpkf400kXVVo8zQ/132" width="30px"><span>刘彬</span> 👍（1） 💬（1）<div>如果我想在 Python 中引用 scikit-learn 库该如何引用？
import scikit-learn

求 1+3+5+7+…+99 的求和，用 Python 该如何写？
 num = 0
 for i in range(100):
      if i &amp; 1 ==1:
            num += i
    print(num)</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/43/52/f3da994a.jpg" width="30px"><span>Claude Chen</span> 👍（1） 💬（1）<div>嗯应该是在国外读研的缘故，喜欢在Jupyter Notebook上鼓捣代码...</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（1） 💬（3）<div>1+3+5+……+99求和可以直接用等差数列求和，Sn=(a1+an)an&#47;2*n</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/55/00846acb.jpg" width="30px"><span>忠超</span> 👍（1） 💬（2）<div>while True:
       try:
              line = raw_input()
              a = line.split()
              print int(a[0]) + int(a[1])
       except:
              break
.................................................................
陈老师好，我想请教一个问题，在A+B problem中，根据这种写法，我输入&quot;3 5&quot;,得到8；
如果写成以下形式：
line = raw_input()
while True:
       try:
              a = line.split()
              print int(a[0]) + int(a[1])
       except:
              break
.........................................................................
同样输入&quot;3 5&quot;,却出现一个无限循环，也会得到8。

陈老师能讲解以下try...except..的用法吗？另外我这两种写法的不同在哪里？</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（1） 💬（1）<div>OnlineJudge的比赛题目。。。数学不好伤不起</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/00/3dbaf430.jpg" width="30px"><span>1e-43</span> 👍（1） 💬（1）<div>老师好，ACM里Vol1~Vol32的难度是逐渐增加吗的，怎么可以选出有易到难的题目？</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/fc/8ddeaccb.jpg" width="30px"><span>Hot   Heat</span> 👍（1） 💬（1）<div>sum(range(0, 100, 2)); 
(sum(range(1, 101))-50)&#47;2; 
reduce(operator.add, range(1, 100, 2)); </div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/26/4e1fd40b.jpg" width="30px"><span>龚梁生了没</span> 👍（1） 💬（1）<div>1.import sklearn
2.直接用sum求和..  sum(i for i in range(1,99,2))</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/69/d0fc88c1.jpg" width="30px"><span>小罗同学</span> 👍（1） 💬（1）<div>推荐两个：
1.pycharm,功能强大，缺点是耗内存。
2.ipython＋任意一个文本编辑器。</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e2/0f/19520317.jpg" width="30px"><span>frango</span> 👍（0） 💬（1）<div>def f(n):
	if n &gt; 1:
		return n + f(n-2)
	else:
		return 1</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（0） 💬（1）<div>思考题：
1. import sklearn调用scikie-learn库；
2. 1~100以内的奇数项求和：
a=0
for i in range(1,100):
    if i%2 !=0:
        a+=i
print(&#39;奇数项求和的结果是:&#39;, a)</div>2021-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（0） 💬（1）<div>第一题：打开windows搜索cmd→打开命令行→pip insatall scikit-learn→打开vs code→新建001.py→import sklearn→运行
第二题：
a =0
for i in range(1,100,2):
    a =a+i
print(a)
结果：2500
一年多没用过python了，居然可以一口气打出来解题，果然学会了的技能就是跟自己终身的。</div>2021-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/48/65/e8274238.jpg" width="30px"><span>Vim๑ºั</span> 👍（0） 💬（3）<div>Python 3:
1,如果我想在 Python 中引用 scikit-learn 库该如何引用？
import sklearn

2,求 1+3+5+7+…+99 的求和，用 Python 该如何写？
sum = 0
number = 1
while number &lt; 100:
       sum = sum + number
       number = number + 1
print (sum)</div>2021-03-20</li><br/>
</ul>