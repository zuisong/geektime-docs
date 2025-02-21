你好，我是景霄。

在前面的学习中，我们其实已经接触到了很多 Python对象比较和复制的例子，比如下面这个，判断a和b是否相等的if语句：

```
if a == b:
    ...
```

再比如第二个例子，这里l2就是l1的拷贝。

```
l1 = [1, 2, 3]
l2 = list(l1)
```

但你可能并不清楚，这些语句的背后发生了什么。比如，

- l2是l1的浅拷贝（shallow copy）还是深度拷贝（deep copy）呢？
- `a == b`是比较两个对象的值相等，还是两个对象完全相等呢？

关于这些的种种知识，我希望通过这节课的学习，让你有个全面的了解。

## `'=='` VS `'is'`

等于（==）和is是Python中对象比较常用的两种方式。简单来说，`'=='`操作符比较对象之间的值是否相等，比如下面的例子，表示比较变量a和b所指向的值是否相等。

```
a == b
```

而`'is'`操作符比较的是对象的身份标识是否相等，即它们是否是同一个对象，是否指向同一个内存地址。

在Python中，每个对象的身份标识，都能通过函数id(object)获得。因此，`'is'`操作符，相当于比较对象之间的ID是否相等，我们来看下面的例子：

```
a = 10
b = 10

a == b
True

id(a)
4427562448

id(b)
4427562448

a is b
True
```

这里，首先Python会为10这个值开辟一块内存，然后变量a和b同时指向这块内存区域，即a和b都是指向10这个变量，因此a和b的值相等，id也相等，`a == b`和`a is b`都返回True。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（112） 💬（0）<div>关于思考题：
SCAR说的很对，程序会报错：&#39;RecursionError: maximum recursion depth exceeded in comparison&#39;。因为x是一个无限嵌套的列表，y深度拷贝x也是一个无限嵌套的列表，理论上x==y应该返回True，但是x==y内部执行是会递归遍历列表x和y中每一个元素的值，由于x和y是无限嵌套的，因此会stack overflow，报错</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/96/dd/0fb7667d.jpg" width="30px"><span>🍎🍎</span> 👍（11） 💬（1）<div>小结：
1.  ‘==’ 用于比较值的大小，‘is’用于比较对象的内存地址是否相同，指向同一个内存地址

2.  对与整数型，范围在（-5 ~ 256 ）之间的整形数，‘==’ 与 ‘is’ 结果相同，原因在于python建立了一个数组缓存，创建对象时直接引用缓存

3.  浅拷贝：定义：重新分配一片内存，生成新的对象，里面的元素是原对象中子对象的引用。
                  生成方法： 可以通过数据构造器（list、set）完成浅拷贝，对于可变序列可以使用切片完成浅拷贝，对于元组而言，tupletuple()和切片不创建浅拷贝，指向相同元组的引用，还可以使用import copy, 使用copy.copy()来进行浅拷贝。
                浅拷贝是对元素的引用，所以对于子对象，如果子对象是不可变，没有影响，如果是可变的序列，会带来一些影响

4.  深拷贝，重新分配一块内存，创建一个新的对象，将原对象中的元素以递归的方式全部拷贝。深拷贝中会维持一个字典，记录已经拷贝的对象以及对象的ID，防止出现无限递归。</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/62/f625b2bb.jpg" width="30px"><span>酸葡萄</span> 👍（0） 💬（3）<div>老师 你好 浅拷贝指向的应该也不是同一块内存吧，如果是的话为什么 is 在浅拷贝中会返回False呢？
is比较的不是地址吗？比如下面的例子


l1 = [1, 2, 3]
l2 = l1[:]

l1 == l2
True

l1 is l2
False</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（171） 💬（4）<div>应该会出错，因为x是一个无限嵌套的列表，y深拷贝于x，按道理来讲 x == y应该是True的，但进行比较操作符“==”的时候，&#39;==&#39;操作符则会递归地遍历对象的所有值，并逐一比较。而python为了防止栈崩溃，递归的层数是要限定的，不会无休下去，所以到了限定的层数，python解释器会跳出错误。执行了一下代码，也的确是跳出了 RecursionError: maximum recursion depth exceeded in comparison。
之前课中做阶乘的例子，如果大于一定的整数，也是会出现递归错误，究其原因也是python的递归层数是有限定的。
def factorial(n):
    return 1 if n &lt;=1 else n*factorial(n-1)
factorial(5000)
RecursionError: maximum recursion depth exceeded in comparison
在sys模块中有个方法可以得到递归的层数:
import sys
sys.getrecursionlimit()
3000
当然你也可以重新设定递归的层数：
sys.setrecursionlimit(10000)
那是不是可以设定无穷大呢？理论上可以，但你的程序崩溃也是一定的，我的mac内存是16G，如果把递归层数设定到1百万，大概跑到35000层左右，我的服务就挂了。
</div>2019-06-12</li><br/><li><img src="" width="30px"><span>瞳梦</span> 👍（122） 💬（12）<div>这节没讲好，其实可以简单归纳的：
一、赋值:

在 Python 中，对象的赋值就是简单的对象引用，这点和 C++不同

 

二、浅拷贝(shallow copy):

 

浅拷贝会创建新对象，其内容非原对象本身的引用，而是原对象内第一层对象的引用。浅拷贝有三种形式:切片操作、工厂函数、copy 模块中的 copy 函数。


三、深拷贝(deep copy):

深拷贝只有一种形式，copy 模块中的 deepcopy()函数。深拷贝和浅拷贝对应，深拷贝拷贝了对象的所有元素，包括多层嵌套的元素。因此，它的时间和空间开销要高。


四、拷贝的注意点:

 

1、对于非容器类型，如数字、字符，以及其他的“原子”类型，没有拷贝一说，产生的都是原对象的引用。
2、如果元组变量值包含原子类型对象，即使采用了深拷贝，也只能得到浅拷贝。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/94/c8bc2b59.jpg" width="30px"><span>yshan</span> 👍（71） 💬（0）<div>浅拷贝，不可变的不可变，可变的依旧可变
深拷贝，都不可变</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/dc/1e1f28b4.jpg" width="30px"><span>Jason</span> 👍（18） 💬（3）<div>x.append(x)为什么会产生无限嵌套的列表呢？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/8b/0371baee.jpg" width="30px"><span>张丽娜</span> 👍（12） 💬（4）<div>a = 257
b = 257
print(id(a))
print(id(b))
在pycharm中运行结果中一致</div>2019-06-12</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（12） 💬（1）<div># 以下命令的输出是？
x == y
1. 出现如下错误信息，推测原因是x与y的列表进行一项一项比较，因无限嵌套，导致递归深度失败。
   RecursionError: maximum recursion depth exceeded in comparison
2. 两个问题，需要老师解答
    既然是无限嵌套，为什么x.append(x)没有报错？
    运行len(x),结果为2,更是不可理解
  
</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/aa/47f2e37d.jpg" width="30px"><span>随风の</span> 👍（7） 💬（0）<div>看到文章中对于元组的拷贝, 这里进行一下补充~.  某些情况浅&#47;深拷贝会失效: 
import copy

x = 1
y = copy.deepcopy(x)
x is y  # failed
True

x = &#39;1&#39;
y = copy.deepcopy(x)
x is y # failed
True

x = (1)
y = copy.deepcopy(x)
x is y  # failed
True

x = (1,[])
y = copy.deepcopy(x)
x is y  # succeed
False

当对数值、字符串、仅包含数值&#47;字符串的元组进行浅&#47;深拷贝会失效。 也就是文中所提到的,  会返回一个指向相同数值、字符串、元组的引用~</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJayib1ZcRfOaoLsdsWZokiaO5tLAdC4uNAicQJRIVXrz9fIchib7QwXibnRrsJaoh5TUlia7faUf36g8Bw/132" width="30px"><span>明月</span> 👍（4） 💬（1）<div>我的x超过256的还是is或者==为true 不知道是不是版本和机器的原因 我的是python3.5.3</div>2019-06-12</li><br/><li><img src="" width="30px"><span>Dynasterran</span> 👍（3） 💬（0）<div>没看源码，猜的：
1. 为什么 len(x) 是 2。
&gt;&gt; x = [1]
&gt;&gt; id(x)
4378931848
&gt;&gt; x.append(x)
&gt;&gt; id(x)
4378931848
&gt;&gt; id(x[0])
4304870656
&gt;&gt; id(x[1])
4378931848
&gt;&gt; x[1] is x
True
&gt;&gt; len(x)
2

2. 为什么 x == y 会报错。
‘==’ 搜到 x[1] 时发现 x[1] 指向一个列表 x&#39;，又去遍历这个列表 x&#39; 的每个值，然后发现这个列表里的 x&#39;[1] 又指向一个列表 x&#39;&#39;, ... 实际上 x, x&#39;, x&#39;&#39; 都是同一个，无限循环。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/f6/40c497a3.jpg" width="30px"><span>Jon徐</span> 👍（3） 💬（1）<div>a = 258
b = 258
在python解释器中使用id查看确实内存地址不同，但是使用vs code同样也是python解释器，内存地址是相同的。

思考题中 x 是循环嵌套的列表，比较时超过了递归限制报错
</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/8d/9081c227.jpg" width="30px"><span>小池</span> 👍（2） 💬（1）<div>x.append(x)会产生递归是因为list对象的append方法本质上是在list末尾追加x的引用，而不是直接添加x指向的实例。但为什么这样不会报栈溢出呢？请问老师，python支持[1, [...]]这种写法的机制是什么？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fe/9e/8165b0a0.jpg" width="30px"><span>路伴友行</span> 👍（2） 💬（0）<div>这样看就明白了：
print(id(x[1][1]))
print(id(x[1][1][1][1][1][1][1][1]))
x 和 y 各自形成了一个闭环</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/21/52e8267b.jpg" width="30px"><span>Hoo-Ah</span> 👍（2） 💬（0）<div>使用列表append自身的时候，没有报递归深度达到最大值的错误，然后我看了list类append方法的源码，里面有这句话Note: new_allocated won&#39;t overflow because the largest possible value is PY_SSIZE_T_MAX * (9 &#47; 8) + 6 which always fits in a size_t. 翻译过来就是新的重载方法不会溢出。使用深拷贝也不会溢出，看源码没看懂。出现错误的原因是因为使用了“==”操作符，因为该操作符会递归的比较里面的值。</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（2） 💬（4）<div>有几个问题：
1）a = 257
b = 257
print(id(a))
print(id(b))
---------
4526886832
4526886832 这个和环境有关么？我用VsCode编辑运行和jupter运行的结果不一致。juterNotebook返回的不一样的</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（0）<div>思考题：
一开始猜想是 print True，因为当 x append 自身的时候，程序是没有报错的，返回的结果是：[1, [...]]，我想程序既然没有报错，则 [...] 表示的应该是对应的一个最大限度的值，只是这里它没有将其表示出来；当我们 deepcopy 的时候 y 获得了同样的结果，表示深度拷贝成功；用 == 来比较两个 list 其实是比较里面的值是否相等，所以应该返回 True。

当然尝试的结果是报错 “RecursionError: maximum recursion depth exceeded in comparison”，我想应该是内部的比较函数递归比较的时候递归深度过长，也就是列表的递归嵌套超过了其限度</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/53/af/e5bf5d08.jpg" width="30px"><span>lllong33</span> 👍（1） 💬（1）<div>两个注意点，
a,b = 257,257 这种写法，引用的同一个地址，a is b 返回True，猜想是由于内部优化了，

深拷贝中，对不可变的元素，会直接引用
import copy
l1 = [[1,2],(3,4),[257,258]]
l2 = copy.deepcopy(l1)
print([id(i) for i in l1], [id(i) for i in l2], , sep=&#39;\n&#39;)
print([id(i) for j in l1 for i in j], [id(i) for j in l2 for i in j], sep=&#39;\n&#39;)  # 这里地址都相同</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/d4/bdd3ed27.jpg" width="30px"><span>converse✪</span> 👍（1） 💬（0）<div>https:&#47;&#47;i.loli.net&#47;2019&#47;06&#47;19&#47;5d09e0647377872742.png 我画了一个关于浅拷贝的理解。老师看是否合适？此外，求解答为什么会出现x的无限递归？还有为什么len(x)是2</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（1） 💬（0）<div>1，没有执行代码的时候，觉得会打印True
2，执行了代码以后，如评论一样RecursionError: maximum recursion depth exceeded in comparison，递归层次过深
3，然后把代码 x.append(x) 注释掉，程序就正常返回True。也就是说问题在这行代码上。
4，网上search了一下，x.append(x)会产生一个无限嵌套列表（评论也有这么说），y深拷贝了x，也就是y拷贝了每一个x的自对象。
5，而==操作符会递归遍历对象所有值，所以出现了递归过深的错误。
不知道我的分析对不对？请老师指点</div>2019-06-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epbRibsic15KXfGEN3SSjnLhXGyhK2Uyrj5ibBJsKAjicNqtafDaQOLH4xpSJRZD1vmibFPJER1ySmwP9A/132" width="30px"><span>farFlight</span> 👍（1） 💬（0）<div>deepcopy创建一个新的对象，并且将原对象中的元素，以递归的方式，通过创建新的子对象拷贝到新对象中。因此&#39;x == y&#39;会无限递归对比，出现stack overflow。

实际运行：
x == y
Traceback (most recent call last):
  File &quot;&lt;stdin&gt;&quot;, line 1, in &lt;module&gt;
RecursionError: maximum recursion depth exceeded in comparison
</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第15讲打卡~</div>2024-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJMW3f6jeDLDVaZODBwJmZOrHRT31bZ0bHLibTRF8xBmfQ6PjfbmqWbw5P92vcEFMAoYSkV4Vt1iarg/132" width="30px"><span>luxuabc</span> 👍（0） 💬（0）<div>RecursionError: maximum recursion depth exceeded in comparison</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d7/64/cb1ca65f.jpg" width="30px"><span>李少辉</span> 👍（0） 💬（0）<div>老师上面用的是list转换后给新的l2,如果直接l2=l1，应该算是深度拷贝吧？</div>2023-03-09</li><br/><li><img src="" width="30px"><span>晁生贵</span> 👍（0） 💬（0）<div>
用== 比较实际是执行两个列表的 a.__eq__(b)，底层比较两个列表的数据及引用的值。列表是无线嵌套数据所以会报错（RecursionError: maximum recursion depth exceeded in comparison），超过最大队列深度。
</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/64/7a/90284972.jpg" width="30px"><span>sudo rm -rf *</span> 👍（0） 💬（0）<div>1</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/23/6800a1b6.jpg" width="30px"><span>麥白</span> 👍（0） 💬（0）<div>2022&#47;03&#47;14 第2遍 ✅</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/24/36/0829cbdc.jpg" width="30px"><span>TheOne</span> 👍（0） 💬（0）<div>浅拷贝：如果是嵌套对象，只复制最外层，里层的对象全部是引用
深拷贝：全部复制，除了不可变对象</div>2021-09-16</li><br/><li><img src="" width="30px"><span>Geek_f6bfca</span> 👍（0） 💬（0）<div># https:&#47;&#47;www.runoob.com&#47;w3cnote&#47;python-understanding-dict-copy-shallow-or-deep.html 参考菜鸟教程

l1 = [[1, 2], (30, 40)]
l2 = list(l1) #浅拷贝(拷贝父对象，不会拷贝对象的内部的子对象), l2 和 l1 是一个独立的对象，但他们的子对象还是指向统一对象（是引用）

print(l1)
print(l2)
print(id(l1))
print(id(l2))

l1.append(100)
print(&#39;第1次&#39;)
print(l1) # 修改对象l1 ，内存指向 [[1, 2], (30, 40), 100] 这个新对象
print(l2) # l2 拷贝原始对象的父对象，内存仍然指向 [[1, 2], (30, 40)]
print(id(l1))
print(id(l2))


l1[0].append(3)
print(&#39;第2次&#39;)
print(l1) # 修改对象 l1 中的子对象，内存指向 [[1, 2, 3], (30, 40), 100]
print(l2) # l2 拷贝原始对象的父对象；但子对象是可变类型，浅复制的前提下， l1 和 l2 指向同一个子对象 [1, 2, 3]
print(id(l1))
print(id(l2))

l1[1] += (50, 60)
print(&#39;第3次&#39;)
print(l1) # 修改对象 l1 中的子对象，内存指向 [[1, 2, 3], (30, 40, 50, 60), 100]
print(l2) # l2 拷贝原始对象的父对象； 子对象1是可变类型， 指向同一个对象 [1, 2, 3]； 子对象2是不可变类型， l1 和 l2 指向不同的子对象 ,分别为(30, 40, 50, 60)，(30, 40)
print(id(l1))
print(id(l2))
</div>2021-08-31</li><br/>
</ul>