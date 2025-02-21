上一节我讲了Python的基本语法，今天我来给你讲下Python中一个非常重要的第三方库NumPy。

它不仅是Python中使用最多的第三方库，而且还是SciPy、Pandas等数据科学的基础库。它所提供的数据结构比Python自身的“更高级、更高效”，可以这么说，NumPy所提供的数据结构是Python数据分析的基础。

我上次讲到了Python数组结构中的列表list，它实际上相当于一个数组的结构。而NumPy中一个关键数据类型就是关于数组的，那为什么还存在这样一个第三方的数组结构呢？

实际上，标准的Python中，用列表list保存数组的数值。由于列表中的元素可以是任意的对象，所以列表中list保存的是对象的指针。虽然在Python编程中隐去了指针的概念，但是数组有指针，Python的列表list其实就是数组。这样如果我要保存一个简单的数组\[0,1,2]，就需要有3个指针和3个整数的对象，这样对于Python来说是非常不经济的，浪费了内存和计算时间。

## 使用NumPy让你的Python科学计算更高效

为什么要用NumPy数组结构而不是Python本身的列表list？这是因为列表list的元素在系统内存中是分散存储的，而NumPy数组存储在一个均匀连续的内存块中。这样数组计算遍历所有的元素，不像列表list还需要对内存地址进行查找，从而节省了计算资源。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（64） 💬（8）<div>#!&#47;usr&#47;bin&#47;python
#vim: set fileencoding:utf-8
import numpy as np

&#39;&#39;&#39;
假设一个团队里有5名学员，成绩如下表所示。
1.用NumPy统计下这些人在语文、英语、数学中的平均成绩、最小成绩、最大成绩、方差、标准差。
2.总成绩排序，得出名次进行成绩输出。
&#39;&#39;&#39;

scoretype = np.dtype({
    &#39;names&#39;: [&#39;name&#39;, &#39;chinese&#39;, &#39;english&#39;, &#39;math&#39;],
    &#39;formats&#39;: [&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;]})

peoples = np.array(
        [
            (&quot;zhangfei&quot;, 66, 65, 30),
            (&quot;guanyu&quot;, 95, 85, 98),
            (&quot;zhaoyun&quot;, 93, 92, 96),
            (&quot;huangzhong&quot;, 90, 88, 77),
            (&quot;dianwei&quot;, 80, 90, 90)
        ], dtype=scoretype)

#print(peoples)

name = peoples[:][&#39;name&#39;]
wuli = peoples[:][&#39;chinese&#39;]
zhili = peoples[:][&#39;english&#39;]
tili = peoples[:][&#39;math&#39;]

def show(name,cj):
    print name,
    print &quot; |&quot;,
    print np.mean(cj),
    print &quot; | &quot;,
    print np.min(cj),
    print &quot; | &quot;,
    print np.max(cj),
    print &quot; | &quot;,
    print np.var(cj),
    print &quot; | &quot;,
    print np.std(cj)

print(&quot;科目  | 平均成绩 | 最小成绩 | 最大成绩 | 方差 | 标准差&quot;)
show(&quot;语文&quot;, wuli)
show(&quot;英语&quot;, zhili)
show(&quot;数学&quot;, tili)

print(&quot;排名:&quot;)
ranking =sorted(peoples,cmp = lambda x,y: cmp(x[1]+x[2]+x[3],y[1]+y[2]+y[3]), reverse=True)
print(ranking)</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cd/10/ea77600b.jpg" width="30px"><span>么春‮脸小的你了亲并‭</span> 👍（110） 💬（9）<div>排名第一的同学是用 Python 2 的写法，我用 Python 3 也写一遍，供大家参考。

# -*- coding: utf-8 -*-
&quot;&quot;&quot;
Created on Sun Jan 20 00:51:28 2019

@author: Dachun Li
&quot;&quot;&quot;
import numpy as np
a = np.array([[4,3,2],[2,4,1]])
print(np.sort(a))
print(np.sort(a, axis=None))
print(np.sort(a, axis=0))
print(np.sort(a, axis=1))

print(&quot;\npart 6 作业\n&quot;)

persontype = np.dtype({
    &#39;names&#39;:[&#39;name&#39;, &#39;chinese&#39;,&#39;english&#39;,&#39;math&#39; ],
    &#39;formats&#39;:[&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;]})
peoples = np.array([(&quot;ZhangFei&quot;,66,65,30),(&quot;GuanYu&quot;,95,85,98),
       (&quot;ZhaoYun&quot;,93,92,96),(&quot;HuangZhong&quot;,90,88,77),
       (&quot;DianWei&quot;,80,90,90)],dtype=persontype)
#指定的竖列
name = peoples[:][&#39;name&#39;]
chinese = peoples[:][&#39;chinese&#39;]
english = peoples[:][&#39;english&#39;]
math = peoples[:][&#39;math&#39;]
#定义函数用于显示每一排的内容
def show(name,cj):
    print(&#39;{} |   {}  |   {}   |   {}   |   {}    |    {}   &#39;
          .format(name,np.mean(cj),np.min(cj),np.max(cj),np.var(cj),np.std(cj)))

print(&quot;科目 | 平均成绩 | 最小成绩 | 最大成绩 | 方差 | 标准差&quot;)
show(&quot;语文&quot;, chinese)
show(&quot;英语&quot;, english)
show(&quot;数学&quot;, math)

print(&quot;排名:&quot;)
#用sorted函数进行排序
ranking = sorted(peoples,key=lambda x:x[1]+x[2]+x[3], reverse=True)
print(ranking)

</div>2019-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/02/4f4484f6.jpg" width="30px"><span>Zahputor</span> 👍（68） 💬（6）<div>老师你好，我想问一下axis=0,axis=1,这个应该怎么理解？看得不是很明白</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a2/81/1cd7fc02.jpg" width="30px"><span>Kylin</span> 👍（44） 💬（4）<div>基本上…没听懂，一脸懵逼的听完了，老师还能抢救一下吗？是缺点什么基础知识？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（12） 💬（1）<div>关于axis参数的问题，我也有点模糊，后来知乎上看到这篇文章，思路清晰多了，也推荐大家看一下：https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;30960190</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/a9/e24380a0.jpg" width="30px"><span>何楚</span> 👍（12） 💬（7）<div>#!&#47;usr&#47;bin&#47;env python3
# -*- coding: utf-8 -*-

import numpy as np
persontype = np.dtype({
    &#39;names&#39;: [&#39;name&#39;,  &#39;chinese&#39;, &#39;math&#39;, &#39;english&#39;],
    &#39;formats&#39;: [&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;]})
peoples = np.array([(&quot;ZhangFei&quot;, 66, 65, 30), (&quot;GuanYu&quot;, 95, 85, 98),
                    (&quot;ZhaoYun&quot;, 93, 92, 96), (&quot;HuangZhong&quot;, 90, 88, 77),
                    (&quot;DianWei&quot;, 80, 90, 90)],
                   dtype=persontype)
for col in peoples.dtype.names:
#    print(col)
    if col is &quot;name&quot;:
        continue
    print(&quot;mean of {}: {}&quot;.format(col, peoples[col].mean()))
    print(&quot;min of {}: {}&quot;.format(col, peoples[col].min()))
    print(&quot;max of {}: {}&quot;.format(col, peoples[col].max()))
    print(&quot;var of {}: {}&quot;.format(col, peoples[col].var()))
    print(&quot;std of {}: {}&quot;.format(col, peoples[col].std()))

report = np.empty([0, 0])
for i in range(peoples.size):
    sum_score = peoples[&#39;chinese&#39;][i] + peoples[&#39;english&#39;][i] + peoples[&#39;math&#39;][i]
    #print(sum_score)
    report = np.append(report, [ sum_score])
report = -np.sort(-report)
print(&quot;sorted score:&quot;)
print(report)

怎么在 numpy 里作成绩求和还不是很清楚。另外，想把成绩和名字按排序后打印出来，要用索引，赶时间没研究，等看别人的结果。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/5d/430ed3b6.jpg" width="30px"><span>从未在此</span> 👍（9） 💬（2）<div>根据我在网上找的学习资料，axis＝0，代表跨行；=1代表跨列，这样很容易理解。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/01/5aaaf5b6.jpg" width="30px"><span>Ben</span> 👍（7） 💬（1）<div>scoretype = np.dtype({&#39;names&#39;: [&#39;name&#39;, &#39;chinese&#39;, &#39;english&#39;, &#39;math&#39;],
                      &#39;formats&#39;: [&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;]})
peoples = np.array(
    [
        (&quot;zhangfei&quot;, 66, 65, 30),
        (&quot;guanyu&quot;, 95, 85, 98),
        (&quot;zhaoyun&quot;, 93, 92, 96),
        (&quot;huangzhong&quot;, 90, 88, 77),
        (&quot;dianwei&quot;, 80, 90, 90)
    ], dtype=scoretype)
print(&quot;科目 | 平均成绩 | 最小成绩 | 最大成绩 | 方差 | 标准差&quot;)
courses = {&#39;语文&#39;: peoples[:][&#39;chinese&#39;],
           &#39;英文&#39;: peoples[:][&#39;english&#39;], &#39;数学&#39;: peoples[:][&#39;math&#39;]}
for course, scores in courses.items():
    print(course, np.mean(scores), np.amin(scores), np.amax(scores), np.std(scores),
          np.var(scores))
print(&#39;Ranking&#39;)
ranking = sorted(peoples, key=lambda x: x[1]+x[2]+x[3], reverse=True)
print(ranking)</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3c/a2/09a2215c.jpg" width="30px"><span>夕子</span> 👍（5） 💬（2）<div>一、为什么用numpy而不用list？
①存储上，list需要同时存储元素和指针，而numpy数组只存储元素，节省内存和计算时间。
②list的元素在系统内存中分散存储，而numpy数组存储在一个均匀连续的内存块中，遍历元素时不需要查找内存地址，节省计算资源。
③在内存访问模式中，缓存会直接把子节块从RAM加载到CPU寄存器中。因为数据连续的存储在内存中，numpy直接利用现代CPU的矢量化指令计算，加载寄存器中的多个连续浮点数。另外numpy中的矩阵计算可以采用多线程的方式，充分利用多核CPU计算资源，大大提升了计算效率。

二、其他数据结构类型：字典、元组、字符串

三、练习题
scoretype = np.dtype({&#39;names&#39;:[&#39;name&#39;,&#39;chinese&#39;,&#39;english&#39;,&#39;math&#39;,&#39;total&#39;], &#39;formats&#39;:[&#39;S32&#39;,&#39;i&#39;, &#39;i&#39;, &#39;i&#39;,&#39;i&#39;]})
peoples = np.array([(&#39;ZhangFei&#39;,66,65,30,0),(&#39;GuanYu&#39;,95,85,98,0),(&#39;ZhaoYun&#39;,93,92,96,0),(&#39;HuangZhong&#39;,90,88,77,0),(&#39;DianWei&#39;,80,90,90,0)], dtype=scoretype)
chineses = peoples[:][&#39;chinese&#39;]
englishes = peoples[:][&#39;english&#39;]
maths = peoples[:][&#39;math&#39;]
print(&#39;语文成绩：&#39;)
print(&#39;平均成绩&#39;,np.mean(chineses))
print(&#39;最小成绩&#39;,np.amin(chineses))
print(&#39;最大成绩&#39;,np.amax(chineses))
print(&#39;方差&#39;,np.var(chineses))
print(&#39;标准差&#39;,np.std(chineses))
print(&#39;-&#39;*30)
print(&#39;英语成绩：&#39;)
print(&#39;平均成绩&#39;,np.mean(englishes))
print(&#39;最小成绩&#39;,np.amin(englishes))
print(&#39;最大成绩&#39;,np.amax(englishes))
print(&#39;方差&#39;,np.var(englishes))
print(&#39;标准差&#39;,np.std(englishes))
print(&#39;-&#39;*30)
print(&#39;数学成绩：&#39;)
print(&#39;平均成绩&#39;,np.mean(maths))
print(&#39;最小成绩&#39;,np.amin(maths))
print(&#39;最大成绩&#39;,np.amax(maths))
print(&#39;方差&#39;,np.var(maths))
print(&#39;标准差&#39;,np.std(maths))
peoples[:][&#39;total&#39;] = peoples[:][&#39;chinese&#39;]+peoples[:][&#39;english&#39;]+peoples[:][&#39;math&#39;]
print(np.sort(peoples,order=&#39;total&#39;))

输出结果为：
语文成绩：
平均成绩 84.8
最小成绩 66
最大成绩 95
方差 114.96000000000001
标准差 10.721940122944169
------------------------------
英语成绩：
平均成绩 84.0
最小成绩 65
最大成绩 92
方差 95.6
标准差 9.777525249264253
------------------------------
数学成绩：
平均成绩 78.2
最小成绩 30
最大成绩 98
方差 634.56
标准差 25.19047439013406

[(b&#39;ZhangFei&#39;, 66, 65, 30, 161) (b&#39;HuangZhong&#39;, 90, 88, 77, 255)
 (b&#39;DianWei&#39;, 80, 90, 90, 260) (b&#39;GuanYu&#39;, 95, 85, 98, 278)
 (b&#39;ZhaoYun&#39;, 93, 92, 96, 281)]

我对结构数组不太熟悉，求总分那里试了对切片求和报错了，看了评论里老师的解答才知道在定义里做，这个要注意多练习。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/98/630fa899.jpg" width="30px"><span>抢地瓜的阿姨</span> 👍（4） 💬（1）<div>Dataframe 即将登场！哈哈哈</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/77/754a127b.jpg" width="30px"><span>王张</span> 👍（3） 💬（2）<div> &#39;formats&#39;:[&#39;S32&#39;,&#39;i&#39;, &#39;i&#39;, &#39;i&#39;, &#39;f&#39;] 是什么意思？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a1/91/207f88b5.jpg" width="30px"><span>小葱拌豆腐</span> 👍（3） 💬（1）<div>老师，请问一下您，没学过高数，没接触过计算机语言，要提前去把各种函数搞清楚吗？有没有推荐的办法，书籍，课程？</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（2） 💬（2）<div>import numpy as np

people_type = np.dtype({&#39;names&#39;: [&#39;name&#39;, &#39;chinese&#39;, &#39;math&#39;, &#39;english&#39;, &#39;total&#39;],
                        &#39;formats&#39;: [&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;f&#39;, &#39;f&#39;]})
peoples = np.array([(&#39;ZhangFei&#39;, 60, 65, 30, 0), (&#39;GuanYu&#39;, 95, 85, 98, 0),
                    (&#39;ZhaoYun&#39;, 93, 92, 96, 0), (&#39;HuangZhong&#39;, 90, 88, 77, 0),
                    (&#39;DianWei&#39;, 80, 90, 90, 0)], dtype=people_type)

chinese = peoples[:][&#39;chinese&#39;]
math = peoples[:][&#39;math&#39;]
english = peoples[:][&#39;english&#39;]

peoples[:][&#39;total&#39;] = chinese + math + english
print(&quot;rank of total scores is \n %s&quot; % np.sort(peoples, order=&#39;total&#39;))
print(&quot;\n&quot;)

for key in list(people_type.fields.keys())[1:4]:
    print(&quot;mean of %s is %s&quot; % (key, np.mean(peoples[:][key])))
    print(&quot;max of %s is %s&quot; % (key, np.amax(peoples[:][key])))
    print(&quot;min of %s is %s&quot; % (key, np.amin(peoples[:][key])))
    print(&quot;std of %s is %s&quot; % (key, np.std(peoples[:][key])))
    print(&quot;var of %s is %s&quot; % (key, np.var(peoples[:][key])))
    print(&quot;\n&quot;)</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（2） 💬（1）<div>#简易学生成绩档案管理
import numpy as np
student_type = np.dtype({&#39;names&#39;:[&#39;studentname&#39;,&#39;Chinese&#39;,&#39;English&#39;,&#39;Math&#39;,&#39;Total&#39;],&#39;formats&#39;:[&#39;U10&#39;,&#39;i&#39;,&#39;i&#39;,&#39;i&#39;,&#39;f&#39;]})
students = np.array([ (&quot;张飞&quot;,66,65,30,None),(&quot;关羽&quot;,95,85,98,None),(&quot;赵云&quot;,93,92,96,None),(&quot;黄忠&quot;,90,88,77,None),(&quot;典韦&quot;,80,90,90,None)]
                    ,dtype = student_type)
Chinese = students[:][&#39;Chinese&#39;]
English = students[:][&#39;English&#39;]
Math = students[:][&#39;Math&#39;]

#指标分析
score_analy={&#39;平均成绩&#39;:{&#39;语文&#39;:np.mean(Chinese),&#39;英语&#39;: np.mean(English),&#39;数学&#39;:np.mean(Math)}
            ,&#39;最小成绩&#39;:{&#39;语文&#39;:np.amin(Chinese),&#39;英语&#39;: np.amin(English),&#39;数学&#39;:np.amin(Math)}
            ,&#39;最大成绩&#39;:{&#39;语文&#39;:np.amax(Chinese),&#39;英语&#39;: np.amax(English),&#39;数学&#39;:np.amax(Math)}
            ,&#39;标准差&#39;  :{&#39;语文&#39;:np.std(Chinese) ,&#39;英语&#39;: np.std(English) ,&#39;数学&#39;: np.std(Math)}
            ,&#39;方差&#39;    :{&#39;语文&#39;:np.var(Chinese) ,&#39;英语&#39;: np.var(English) ,&#39;数学&#39;: np.var(Math)}}

#统计总成绩
for i in range(len(students)):
    students[i][&#39;Total&#39;] = sum(list(students[i])[1:-1])

#输出分析指标
print(&quot;  指标项  \t\t   语文   \t\t   英语   \t\t   数学   &quot;)
print((&quot;-&quot; * 10 +&quot;\t\t&quot;)*4)
for index in score_analy:
    report = f&quot;{index:10}&quot;.format(index) + &quot;\t\t{语文:&gt;10.2f}\t\t{英语:&gt;10.2f}\t\t{数学:&gt;10.2f}&quot;
    print(report.format_map(score_analy[index]))

print((&quot;-&quot; * 82))

#按总成绩输出排名
print(&quot;名次\t\t姓名\t\t总分&quot;)
print((&quot;-&quot; * 4 +&quot;\t\t&quot;)*3)
    
s = np.sort(students,order=&#39;Total&#39;)
for i in range(len(s)):
    k=-1 * (i+1)
    print(&#39;{rank:4}\t\t{name:4}\t\t{score:&gt;4}&#39;.format(rank=i+1,name=s[k][&#39;studentname&#39;],score=s[k][&#39;Total&#39;]))
</div>2019-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqmqDPzn9q0YM0CgSicVD215GibbOpyC52vJ5LUbDicwoI7n3biapWls4qd7ENwH4tJyJibgGcyrM5kCzQ/132" width="30px"><span>Geek_ce3c1f</span> 👍（2） 💬（1）<div>import numpy as np
persontype = np.dtype({
    &#39;names&#39;:[&#39;name&#39;, &#39;chinese&#39;, &#39;english&#39;, &#39;math&#39;],
    &#39;formats&#39;:[&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;f&#39;]})
peoples = np.array([(&quot;ZhangFei&quot;,66,65,30),(&quot;GuanYu&quot;,95,85,90),
                    (&quot;ZhaoYun&quot;,93,92,96),(&quot;HuangZhong&quot;,90,88,77),
                    (&quot;Dianwei&quot;,80,90,90)],dtype=persontype)

chineses = peoples[:][&#39;chinese&#39;]
maths = peoples[:][&#39;math&#39;]
englishs = peoples[:][&#39;english&#39;]

print(&quot;语文平均分%.2f，最小成绩%d，最大成绩%d，方差%.2f，标准差%.2f&quot; %(np.mean(chineses),np.amin(chineses),np.amax(chineses),np.var(chineses),np.std(chineses)))
print(&quot;数学平均分%d, 最小成绩%d，最大成绩%d，方差%d，标准差%d&quot; %(np.mean(maths),np.amin(maths),np.amax(maths),np.var(maths),np.std(maths)))
print(&quot;英语平均分%d, 最小成绩%d，最大成绩%d，方差%d，标准差%d&quot; %(np.mean(englishs),np.amin(englishs),np.amax(englishs),np.var(englishs),np.std(englishs)))

# chengji = np.array([[66,65,30],[95,85,90],[93,92,96],[90,88,77],[80,90,90]])

rank = np.sort(peoples, axis=None, kind=&#39;mergesort&#39;, order=(&#39;chinese&#39;,&#39;english&#39;,&#39;math&#39;))
print(rank)</div>2019-03-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIYDCC8ZjLrfbdn6UdDLdfia3059dOicfHjnia5ib8uPwjibyRfJuyfj8ibtmndsSibGbMWnuM2k0gFOq7KQ/132" width="30px"><span>Blaise</span> 👍（2） 💬（1）<div>subjects = np.dtype({&#39;names&#39;: [&#39;name&#39;, &#39;Chinese&#39;, &#39;English&#39;, &#39;Math&#39;],                     
                     &#39;formats&#39;: [&#39;S32&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;]
                    })

people = np.array([(&#39;ZhangFei&#39;,66,65,30), (&#39;GuanYu&#39;,95,85,98),
                   (&#39;ZhaoYun&#39;,93,92,96), (&#39;HuangZhong&#39;,90,88,77),
                   (&#39;DianWei&#39;,80,90,90), 
                  ], dtype=subjects)

print(np.mean(people[:][&#39;Chinese&#39;]))
print(np.mean(people[:][&#39;English&#39;]))
print(np.mean(people[:][&#39;Math&#39;]))


print(np.amin(people[:][&#39;Chinese&#39;]))
print(np.amin(people[:][&#39;English&#39;]))
print(np.amin(people[:][&#39;Math&#39;]))

print(np.amax(people[:][&#39;Chinese&#39;]))
print(np.amax(people[:][&#39;English&#39;]))
print(np.amax(people[:][&#39;Math&#39;]))

print(np.std(people[:][&#39;Chinese&#39;]))
print(np.std(people[:][&#39;English&#39;]))
print(np.std(people[:][&#39;Math&#39;]))

print(np.var(people[:][&#39;Chinese&#39;]))
print(np.var(people[:][&#39;English&#39;]))
print(np.var(people[:][&#39;Math&#39;]))

# summarytype = np.dtype({&#39;names&#39;: [&#39;ZhangFei&#39;, &#39;GuanYu&#39;, &#39;ZhaoYun&#39;, &#39;HuangZhong&#39;, &#39;DianWei&#39;], &#39;formats&#39;: [&#39;i&#39;,&#39;i&#39;, &#39;i&#39;, &#39;i&#39;, &#39;i&#39;],})
summary = np.array([], dtype=np.int32)

for i, person in enumerate(people):
    person = list(person)
    print(person[:])
    total = (np.sum(person[1:]))
    print(total)
    summary = np.append(summary, [total], axis=0)

# 每人的总成绩
print(summary)

# 对每人的总成绩排序
print(np.sort(summary))

本来还想在总成绩数组上标明是谁的成绩，还没弄出来。</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/ee/f7f45ca9.jpg" width="30px"><span>吃鱼</span> 👍（1） 💬（1）<div>想问一下，练习题中用结构数组表示成绩，之后如果想把总成绩添加进该列表，应该怎么操作呢？
尝试直接用people[:][&quot;total&quot;] = people[:][&quot;chinese&quot;]+people[:][&quot;english&quot;]+people[:][&quot;math&quot;]，结果报错了，“no field of name total&quot;</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fe/83/b2e833ff.jpg" width="30px"><span>笨鸟的GPS</span> 👍（1） 💬（1）<div># 对于每门课来说，最高最低成绩、平均成绩、方差、标准差¶
import numpy as np
persontype = np.dtype({
    &#39;names&#39;:[&#39;name&#39;,&#39;chinese&#39;,&#39;english&#39;,&#39;math&#39;,&#39;total&#39;],
    &#39;formats&#39;:[&#39;S32&#39;,&#39;i&#39;,&#39;i&#39;,&#39;i&#39;,&#39;i&#39;]})
peoples = np.array([(&#39;zhangfei&#39;,66,65,30,0),(&#39;guanyu&#39;,95,85,98,0),(&#39;zhaoyun&#39;,93,92,96,0),(&#39;huangzhong&#39;,90,88,77,0),(&#39;dianwei&#39;,80,90,90,0)],dtype=persontype)
# 指定的竖列
name = peoples[:][&#39;name&#39;]
chinese = peoples[:][&#39;chinese&#39;]
english = peoples[:][&#39;english&#39;]
math = peoples[:][&#39;math&#39;]
# 定义函数用于显示每一排的内容
def show(name,cj):
    print(&#39;{}|{}|{}|{}|{}|{}&#39;.format(name,np.mean(cj),np.min(cj),np.max(cj),np.var(cj),np.std(cj)))
print(&quot;科目|平均成绩|最小成绩|最大成绩|方差|标准差&quot;)
show(&quot;语文&quot;,chinese)
show(&quot;英语&quot;,english)
show(&quot;数学&quot;,math)

peoples[:][&#39;total&#39;]=peoples[:][&#39;chinese&#39;]+peoples[:][&#39;english&#39;]+peoples[:][&#39;math&#39;]
print(&#39;每个按三科总分排序：&#39;,np.sort(peoples,order=&#39;total&#39;))


但是对于每个人来说解法还没思路</div>2021-03-20</li><br/><li><img src="" width="30px"><span>RM</span> 👍（1） 💬（1）<div>您好，麻烦问一下 把（）改为[]加上,dtype=persontype为什么会报错呢？如下：
peoples = np.array([[&quot;ZhangFei&quot;,75,100,90],[&quot;GuanYu&quot;,85,96,88], [&quot;ZhaoYun&quot;,85,92,96],[&quot;HuangZhong&quot;,65,85,100]],dtype=persontype)
print(peoples)
ValueError: invalid literal for int() with base 10: &#39;ZhangFei&#39;</div>2020-04-12</li><br/><li><img src="" width="30px"><span>十六。</span> 👍（1） 💬（1）<div>当我做到求所有同学成绩和时，我卡主了，我想到了sum，到老师教程看发现没有提到，我也为没有，上网搜了一下numpy中有sum的用法也是用来求和的，但在这里好像很难做到将每一个同学的语数外成绩取出来，暂时还没有想到方法，如果有同学老师知道的，还望指教！！！谢谢
留言第一名同学的输出总成绩排序使用sorted方法，让我受益匪浅
sort 与 sorted 区别：
sort 是应用在 list 上的方法，sorted 可以对所有可迭代的对象进行排序操作。
list 的 sort 方法返回的是对已经存在的列表进行操作，无返回值，而内建函数 sorted 方法返回的是一个新的 list，而不是在原来的基础上进行的操作。key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。摘自菜鸟教程中sorted的用法

我写的代码较low就不发了</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/19/78/e5b3c009.jpg" width="30px"><span>Helen</span> 👍（1） 💬（1）<div>请问老师能不能详细讲下dtype和key=lambda是什么意思，怎么用。谢谢。</div>2019-08-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI45zO9GOMquk9JymTibN9sC25Sy4WtsDGRQzIRVIoIzPnaJGKmGe3jXqxP0zKZyTYazrXHBGYjBzw/132" width="30px"><span>柚子</span> 👍（1） 💬（1）<div>学习笔记：https:&#47;&#47;blog.csdn.net&#47;hahaha66888&#47;article&#47;details&#47;86523526
练习题代码如下
import numpy as np
dt = np.dtype({&#39;names&#39;:[&#39;name&#39;,&#39;chinese&#39;,&#39;english&#39;,&#39;math&#39;],
             &#39;formats&#39;:[&#39;S32&#39;,&#39;i&#39;,&#39;i&#39;,&#39;i&#39;]})
person = np.array([(&#39;zhangfei&#39;,66,65,30),(&#39;guanyu&#39;,95,85,98),(&#39;zhaoyun&#39;,93,92,96),(&#39;huangzhong&#39;,90,88,77),(&#39;dianwei&#39;,80,90,90)],dtype = dt)

chinese = person[:][&#39;chinese&#39;]
english = person[:][&#39;english&#39;]
maths = person[:][&#39;math&#39;]

#平均成绩
print(np.mean(chinese))
print(np.mean(english))
print(np.mean(maths))

#最大成绩
print(np.amax(chinese))
print(np.amax(english))
print(np.amax(maths))

#最小成绩
print(np.amin(chinese))
print(np.amin(english))
print(np.amin(maths))

#方差
print(np.std(chinese))
print(np.std(english))
print(np.std(maths))

#标准差
print(np.var(chinese))
print(np.var(english))
print(np.var(maths))

成绩之和排序：
def fun(a):
    return a[1]+a[2]+a[3]
print(sorted(person,key = fun,reverse=True))</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e2/0f/19520317.jpg" width="30px"><span>frango</span> 👍（0） 💬（1）<div>import numpy as np
import pandas as pd
score = pd.DataFrame({
    &#39;chinese&#39;:[66,95,93,90,80],
    &#39;math&#39;:[65,85,92,90,90],
    &#39;english&#39;:[30,98,96,77,90]
}, index=[&#39;张飞&#39;, &#39;关羽&#39;, &#39;赵云&#39;,&#39;黄忠&#39;,&#39;典韦&#39;],)
func = [&#39;min&#39;,&#39;max&#39;,&#39;mean&#39;,&#39;var&#39;,&#39;std&#39;]
table = np.round(score.agg(func),1)
sort = np.sum(score, axis=1).sort_values()</div>2021-04-08</li><br/><li><img src="" width="30px"><span>薛倩斐</span> 👍（0） 💬（1）<div>import numpy as np
performance = np.dtype([(&quot;name&quot;,str),(&quot;yuwen&quot;,int),(&quot;yingyu&quot;,int),(&quot;shuxue&quot;,int)])
peoples = np.array([(&quot;ZhangFei&quot;,66,65,30),(&quot;GuanYu&quot;,95,85,98),
        (&quot;ZhaoYun&quot;,93,92,96),(&quot;HuangZhong&quot;,90,88,77),(&quot;dianwei&quot;,80,90,90)],dtype=performance)
print (&quot;      平均  最大  最小   方差   标准差&quot;)
def show(name1):
    print (name1,end=&#39;:&#39;)
    print (&#39;%4.2f&#39;%np.mean(peoples[name1]),end=&#39; &#39;)
    print (&#39;%4.2f&#39;%np.amax(peoples[name1]),end=&#39; &#39;)
    print (&#39;%4.2f&#39;%np.amin(peoples[name1]),end=&#39; &#39;)
    print (&#39;%4.2f&#39;%np.std(peoples[name1]),end=&#39; &#39;)
    print (&#39;%4.2f&#39;%np.var(peoples[name1]))
show (&#39;yuwen&#39;)
show (&#39;yingyu&#39;)
show (&#39;shuxue&#39;)
ranking = sorted(peoples,key=lambda x: x[1]+x[2]+x[3],reverse=True)
print (ranking)

请问一下，为何这段代码在最后排序输出不了name，显示都是空</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/48/a3/2df11999.jpg" width="30px"><span>Boom clap!!!</span> 👍（0） 💬（1）<div>numpy里有许多自带的函数库，帮助我们简化代码。
这是list所不具备的。</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fe/83/b2e833ff.jpg" width="30px"><span>笨鸟的GPS</span> 👍（0） 💬（1）<div>其实课后题看起来有两种理解:一种是对于人，三门课程的最大最小平均成绩；另一种是对于科目来说，哪个人的最大最小平均成绩。等我回去把两种都写一下</div>2021-03-18</li><br/><li><img src="" width="30px"><span>Runing</span> 👍（0） 💬（2）<div>在“同样 axis 默认是 -1，即沿着数组的最后一个轴进行排序”中，请问数组的最后一个轴是指哪个轴？</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/73/6e/5ba988a6.jpg" width="30px"><span>泡泡跑吧</span> 👍（0） 💬（1）<div>讲的挺好的，语速要是能自行调整就好了，听着稍微有点快，有压力感。</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/6e/cd8fea9f.jpg" width="30px"><span>RecordLiu</span> 👍（0） 💬（1）<div>老师，在结构数组的例子中，为什么要用切片的方式取元素呢？试了一下peoples[:][&#39;age&#39;]和peoples[&#39;age&#39;]结果是一样的，结果返回的都是一个列表，老师使用切片方式的原因是什么呢？</div>2020-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL4j3xXIeQr2lFrbG6icUj1L9ibSqEgzCMa76v6wboTTSibyPYSCbjIJZp76O51H3XODg80IAsfJgVzw/132" width="30px"><span>Geek_Chain</span> 👍（0） 💬（1）<div>同样，percentile() 代表着第 p 个百分位数，这里 p 的取值范围是 0-100，如果 p=0，那么就是求最小值，如果 p=50 就是求平均值，如果 p=100 就是求最大值。同样你也可以求得在 axis=0 和 axis=1 两个轴上的 p% 的百分位数。
50分位的意思不是中位数吗？</div>2020-11-25</li><br/>
</ul>