你好，我是景霄。

在前面的第一大章节中，我们一起学习了Python的函数基础及其应用。我们大致明白了，所谓的传参，就是把一些参数从一个函数传递到另一个函数，从而使其执行相应的任务。但是你有没有想过，参数传递的底层是如何工作的，原理又是怎样的呢？

实际工作中，很多人会遇到这样的场景：写完了代码，一测试，发现结果和自己期望的不一样，于是开始一层层地debug。花了很多时间，可到最后才发现，是传参过程中数据结构的改变，导致了程序的“出错”。

比如，我将一个列表作为参数传入另一个函数，期望列表在函数运行结束后不变，但是往往“事与愿违”，由于某些操作，它的值改变了，那就很有可能带来后续程序一系列的错误。

因此，了解Python中参数的传递机制，具有十分重要的意义，这往往能让我们写代码时少犯错误，提高效率。今天我们就一起来学习一下，Python中参数是如何传递的。

## **什么是值传递和引用传递**

如果你接触过其他的编程语言，比如C/C++，很容易想到，常见的参数传递有2种：**值传递**和**引用传递**。所谓值传递，通常就是拷贝参数的值，然后传递给函数里的新变量。这样，原变量和新变量之间互相独立，互不影响。

比如，我们来看下面的一段C++代码：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（100） 💬（3）<div>关于思考题：
第一题：
l2和l3是指向同一个对象，因为两者之间用等号赋值了，l1并不是，l1所指向的[1, 2, 3]是另外一块内存空间，大家可以通过id()这个函数验证

第二题：
输出的是{&#39;a&#39;: 10, &#39;b&#39;: 20}，字典是可变的，传入函数后，函数里的d和外部的d实际上都指向同一个对象
d[idx] = value语句改变了字典对应key所指向的值
</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/2f/b29e8af8.jpg" width="30px"><span>轻风悠扬</span> 👍（2） 💬（7）<div>老师，最后一个代码示例，如果我把l2 = l2 + [4] 换成 l2 += [4]，l1会变成[1,2,3,4].不明白l2 = l2 + [4] 换成 l2 += [4]有什么不一样的地方，有点小困惑

def my_func5(l2):
  l2 += [4]

l1 = [1, 2, 3]
my_func5(l1)
l1
[1, 2, 3, 4]</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/11/9f09be94.jpg" width="30px"><span>mercy</span> 👍（2） 💬（1）<div>对象的id能否理解为指针</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/51/ea/d9a83bb3.jpg" width="30px"><span>古明地觉</span> 👍（88） 💬（8）<div>针对@小恶魔的问题，回复一下

python里面一切皆对象， 比如a=1。在java里面是int a = 1，相当于先声明了一个int类型的变量a，然后给这个变量赋值为1。但在python中，是先在内存中申请一份空间，存的值为1，然后再给这块空间贴上一个标签，叫变量a，因此python中变量实际上是一个便利贴，可以贴在任何地方。并且还可以通过值来推断出变量的类型，这一步是由解释器来完成的。所以python虽然不需要显式声明变量，但它其实是强类型语言。
def func(d):
    d[&#39;a&#39;] = 10
    d[&#39;b&#39;] = 20
    d = {&#39;a&#39;: 1, &#39;b&#39;: 2}


d = {}
func(d)
print(d)  # {&#39;a&#39;: 10, &#39;b&#39;: 20}

至于这里为什么会是这个结果，当我们将d传递给func的时候，其实func里面的d和外面的d指向的是同一片内存。相当于一开始d={},存放{}这份空间只有d这一个便利贴，但是func(d)的时候，这份空间又多了一个便利贴。尽管都叫d，但一个是全局变量d，一个是函数的参数d
当d[&#39;a&#39;] = 10和d[&#39;b&#39;]=20的时候，由于字典是可变类型，所以外面的d也被修改了，此时外面的d和函数里面的d都指向了{&#39;a&#39;: 10, &#39;b&#39;: 20}, 但是当d = {&#39;a&#39;: 1, &#39;b&#39;: 2}的时候，这是属于赋值。因此python会在内存中再开辟一份空间，空间存放{&#39;a&#39;: 1, &#39;b&#39;: 2}，然后让函数里面的局部变量d指向它，相当于将原本位于{&#39;a&#39;:10,&#39;b&#39;:20}上的便利贴撕下来，贴在了另一块空间。但这只是函数里面的d，对外面的d是没有影响的，所以外面的d依旧是{&#39;a&#39;: 10, &#39;b&#39;: 20}。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（24） 💬（0）<div>第一个比较简单，列表是可变对象，每创建一个列表，都会重新分配内存，因此 l1 和 l2 并不是同一个对象，由于 l3 = l2 表明 l3 指向 l2 的对象。

第二个 输出的结果应该是 {&#39;a&#39;: 10, &#39;b&#39;: 20} ，d = {&#39;a&#39;: 1, &#39;b&#39;: 2} 属于重新指向新的对象，并不改变原有的字典对象。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/94/c8bc2b59.jpg" width="30px"><span>yshan</span> 👍（11） 💬（2）<div>首先更正下，需要先定义d={}。
然后，局部变量与全局变量的区别，函数内定义的d为全局变量，在没有关键字声明的情形下不能改变全局变量，由于字典可变，遵循可变则可变的原则，输出为{&#39;a&#39;: 10, &#39;b&#39;: 20}。
最后，看实验：
def func(d):
    print(id(d))
    d[&#39;a&#39;] = 10
    d[&#39;b&#39;] = 20
    print(id(d))
    d = {&#39;a&#39;:1, &#39;b&#39;:2}
    print(id(d))
    print(d)

d = {}
print(id(d))
func(d)
print(d)
print(id(d))

执行结果：
3072243980
3072243980
3072243980
3072244108
{&#39;a&#39;: 1, &#39;b&#39;: 2}
{&#39;a&#39;: 10, &#39;b&#39;: 20}
3072243980

</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（8） 💬（1）<div>第一题，用id（）打印出来后可以证明，l1和l2不是同一个对象，l2和l3是同一个对象。由于列表是可变的，所以l1和l2指向不同的内存区域。
第二题，做了一下修改，如下：
def func(d):
    d[&#39;a&#39;] = 10
    d[&#39;b&#39;] = 20
    d={&#39;a&#39;:1,&#39;b&#39;:2}

d={}
func(d)
print(d)

执行结果：
{&#39;a&#39;: 10, &#39;b&#39;: 20}

d = {&#39;a&#39;: 1, &#39;b&#39;: 2}应该是指向了新的对象


</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/da/54c663f3.jpg" width="30px"><span>Wing·三金</span> 👍（7） 💬（0）<div># C++

- 按值传递：拷贝参数的值构建新的变量传递到函数
- 按引用传递：把参数的引用（i.e. 地址）传递到函数

# Python

- 按赋值传递&#47;按对象的引用传递
- 凡是对对象本身进行的操作，都会影响传递的原对象；凡是生成了新对象的操作，都不会影响传递的原对象
- 正如【一个人可以死两次，第一次是肉体死去，第二次是当没人记得它的时候】，python 中如果有多个变量指向同一个对象，那么当删除一个变量时并不会真正删除其所指定的对象；只有当所有指定该对象的变量都被删除时，python 才会回收该对象所占用的资源
- 一般原则：对于不可变的数据类型，operator 等操作会返回新的对象，不会影响原对象；对于可变的数据类型，任何对【对象本身】的操作都会影响所有指向该对象的变量
- 补充上一条：e.g. 对于 list 而言，l += [1] 和 l = l + [1] 不同！前者是在 l 本身的末尾添加新元素，后者是在 l 的基础上添加新的元素并返回新的对象
- 在工程上，偏爱类似于上一条后者的作法——即通过【创建新的对象+将其返回】的作法，来减少出错的概率

# 思考题

1. l1 与 l2 不同，l3 与 l2 同；
2. 严格来说，如果没有上下文，这是一段错误的代码，因为没有预先定义 d 变量；不妨假设在第 6 行之前补充语句 d = {}，则输出结果为 {&#39;a&#39;: 10, &#39;b&#39;: 20}，因为 func 中前两行才是改变了对象的操作。而第 3 行只是将函数中的局部变量 d 指向了新的字典 {&#39;a&#39;: 1, &#39;b&#39;: 2}，但全局变量 d 仍然指向着刚刚被修改过的字典对象。</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（5） 💬（0）<div>第一题：l2和l3指向同一个对象，l2和l1不指向同一个对象。这个题的关键要点是要了解list对象是没有“内存驻留”机制的，这点和整数对象对小于256的数采用的“内存驻留”是截然不同的，所以l1和l2不是指向同一对象。而l3=l2,这就是让l3指向l2指向的对象，很显然l3和l2指向的是同一个对象。
第二题：题目里的d = {&#39;a&#39;: 1, &#39;b&#39;: 2}应该是顶格的吧，估计是老师手误或是编辑器出问题了，不然没意义。如果是这样，print(d),输出应该是{&#39;a&#39;: 10, &#39;b&#39;: 20}。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（3） 💬（0）<div>总结:Python中参数传递既不是传值也不是传引用，而是赋值传递，或传对象的引用。不是指向一个具体的内存地址，而是指向具体的对象。
如果对象是不变的，改变对象会新建一个对象，并将其中一个变量指向该对象，其它变量不变。如果对象是可变的，改变一个变量时，其它所有指向该对象的变量都会受影响。要想在函数中改变对象，可以传入可变数据类型(列表，字典，集合)，直接改变；也可以创建一个新对象，修改以后返回。建议用后者，表达清晰明了，不易出错。
思考题1:
l2与l3指向同一对象，与l1不同。
# 思考题1
 l1 = [1,2,3,4]
 l2 = [1,2,3,4]
 l3 = l2
 print(id(l1), id(l2), id(l3))
思考题2
{&quot;a&quot;:10, &quot;b&quot;:20}
课程的练习代码: https:&#47;&#47;github.com&#47;zwdnet&#47;PythonPractice</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/0e/3fbc418d.jpg" width="30px"><span>youaresherlock</span> 👍（2） 💬（0）<div>Python应该是共享传参</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/d3/6ec3bfa1.jpg" width="30px"><span>1cho糖糖</span> 👍（2） 💬（1）<div>遇到了下面一个问题

```
def demo1(array):
    array += [4, 5]
    return array


def demo2(array):
    array = array + [4, 5]
    return array


a = [1, 2, 3]
b = [1, 2, 3]

c = demo1(a)
print(&#39;a list is {}\nc list is {}\na is c :{}&#39;.format(a, c, a is c))  # True
# 输出结果
a list is [1, 2, 3, 4, 5]
c list is [1, 2, 3, 4, 5]
a is c :True

d = demo2(b)
print(&#39;b list is {}\nd list is {}\nb is d :{}&#39;.format(b, d, b is d))  # False
# 输出结果
b list is [1, 2, 3]
d list is [1, 2, 3, 4, 5]
b is d :False

# 函数内部为什么 array += [4, 5] 与 array = array + [4, 5] 对传入的列表影响结果不同
```</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/3d/2a3b67f8.jpg" width="30px"><span>catshitfive</span> 👍（2） 💬（0）<div>第一题：本例中，对于列表对象而言，l1和l2是不同的对象，l3指向的是l2，属于同一对象；对于列表内的immutable元素对象而言，这三个列表指向的都是相同的对象
第二题 使用数据结构中内置的方法或者切片操作会直接修改可变元素的内容而保持内存地址不变，如果是二个对象直接操作，则会创建新对象，所以本例中变量指向的字典内容会被函数更新
对于一维列表可以浅拷贝保存数据，对于二维及以上的，应该用深拷贝保存数据才安全</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（2） 💬（0）<div>1. l2和l3是一个，l1不是。可以通过id(l2),id(l1),id(l3)验证。
2. d不是没有初始化么。输出错误吧。如果在使用函数func(),将d初始化为d={},输出{&#39;a&#39;:10, &#39;b&#39;:20}.原因：前两个改变了对象的值。后面是创建了新对象赋值给了本地对象。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/d7/5b1b09fd.jpg" width="30px"><span>Jacky</span> 👍（1） 💬（0）<div>不可变对象，赋值给变量时，如果两个对象的值相同，则指向同一个对象。
两个变量指向同一对象，如果其中一个对象的值改变，则新建对象赋值给变量。
可变对象，赋值给变量时，如果两个对象的值相同，则指向不同对象。
两个变量指向同一对象，如果其中一个对象的值改变，两个变量的值都发生改变。（指向统一对象）</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/8b/0371baee.jpg" width="30px"><span>张丽娜</span> 👍（1） 💬（0）<div>def my_func2(b):
    print(&#39;a的值是{}&#39;.format(a))
    print(&#39;b的值是{}&#39;.format(a))
    b = 2
    print(&#39;b的值是{}&#39;.format(b))
    return b


a = 1
a = my_func2(a)  #这句话so 重要，重新用返回值对于a进行了赋值，看起来debug来逐步分析很重要啊
print(&#39;a的值是{}&#39;.format(a))</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/42/bd500d0f.jpg" width="30px"><span>小恶魔</span> 👍（1） 💬（1）<div>看了这么多关于问题2回复都是结果。我想知道python中对参数赋值不会影响外部的值，这是设定语法，还有什么深层次的原因或设计考虑么，谢谢老师。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第16讲打卡~</div>2024-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e2/81/2cbb88b1.jpg" width="30px"><span>这只鸟不会飞</span> 👍（0） 💬（1）<div>关于思考题：
第一题：l1 和 l2 不指向同一个对象，l2 和 l3 指向同一个对象。 
从题干来看，l1和l2分别是创建了新对象来指向地址的，使用 l1 is l2 就能分辨出来。而l2 和 l3 指向的是同一个对象引用地址，所以 l2 和 l3 指向同一个对象。

第二题:  会报错， d[&#39;b&#39;] = 20 这个已经不在函数内，所以此时会报d未定义的错误。
如果此时定义的函数如下：
def func(d): 
    d[&#39;a&#39;] = 10 
    d[&#39;b&#39;] = 20
由于外部调用的 d是可变变量，所有最后得到的结果会是: {&#39;a&#39;:10, &#39;b&#39;:20}
</div>2023-01-18</li><br/><li><img src="" width="30px"><span>晁生贵</span> 👍（0） 💬（0）<div>第一个 ，都是指向同一个对象
第二个，打印
{&#39;a&#39;: 10, &#39;b&#39;: 20}
</div>2022-08-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoAlkIjytYG8MqOtDf7n7pF3rXJnoMNL9ebRXluPvGh2e2A9TxyMoQxPyYQ1dInAFIeltwo8zuvhg/132" width="30px"><span>Geek_145846</span> 👍（0） 💬（0）<div>特别喜欢老师的专栏，把很多教程中没有说透的知识点说清楚了！</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/8d/03cac826.jpg" width="30px"><span>徐李</span> 👍（0） 💬（0）<div>这个参数传递，python和java 简直一样</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e4/cf/906f47c9.jpg" width="30px"><span>含章</span> 👍（0） 💬（0）<div>
def my_func1(b):
  b = 2

a = 1
my_func1(a)
a
1

这里的参数传递，使变量 a 和 b 同时指向了 1 这个对象。但当我们执行到 b = 2 时，系统会重新创建一个值为 2 的新对象，并让 b 指向它；而 a 仍然指向 1 这个对象。所以，a 的值不变，仍然为 1。

这里的解释是不是有问题啊？</div>2022-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrIyCrRXMPXUQTR5IHNOh6niaY3MRr2mtv6W6WXcT1FHK1aic3NOhfzdaqfx3u8mmFAmibgX8xDdB2g/132" width="30px"><span>王俊</span> 👍（0） 💬（0）<div>编程规范里都不推荐吧可变对象作为方法的参数了</div>2022-01-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/SXhZVacJlNR0lBbPib7peJbVlhsX8iaiaw2AdkfO8RTn0V7zoBvm5dWy4uvBehqTuOzlRFTG1r46Wz9GIiaMAHMvfA/132" width="30px"><span>qiu123456</span> 👍（0） 💬（0）<div>思考题1
l1和l2不是同一个对象，l2和l3引用同一个对象
思考题2
由于d是字典，属于可变对象，因此函数内部的d不会新建一个对象，而是原有的对象，最后的结果是{&#39;a&#39;: 10, &#39;b&#39;: 20}</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/31/da42b783.jpg" width="30px"><span>苏苏</span> 👍（0） 💬（0）<div>python 这里是不是可以理解为如果是不可变对象，其实传递的是副本，如是可变对象传递的是引用地址</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/63/b8/4db57533.jpg" width="30px"><span>小博主</span> 👍（0） 💬（0）<div>和上一届的浅拷贝和深拷贝一个道理吧</div>2021-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OwZuBRbVUkziazePs2xTKskNpZachRtCBZLHlv4dAUgaBC5qHI292xaxvg3atGnHlDwjIOXPKEbc7zOrtMyicSNg/132" width="30px"><span>罗辑</span> 👍（0） 💬（1）<div>请问老师：dict自带的copy方法是浅拷贝还是深拷贝？
d = {&#39;a&#39;: 1, &#39;b&#39;: 2}
f=d
g =d.copy()
print(id(d),id(f),id(g))
得到的结果。d和f指向同一个对象，g指向另外的对象。</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/3e/874ec3c1.jpg" width="30px"><span>cooper</span> 👍（0） 💬（1）<div>为啥评论第二道思考题都会看错呢？明明写法是这样的：
def func(d):
    d[&#39;a&#39;] = 10
    d[&#39;b&#39;] = 20

d = {&#39;a&#39;: 1, &#39;b&#39;: 2}
func(d)
print(d)

前面赋值了，都看不懂题目吗</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/7d/f7c3b0c5.jpg" width="30px"><span>Ekko_松松</span> 👍（0） 💬（0）<div>第一题：
尝试了 list，dict，set，变量l2，l3指向同一个对象，l1指向另一个对象。
尝试 str，tuple，int，变量l1，l2，l3均指向同一个对象
第二题：
打印d输出｛‘a’: 10, ‘b’:20}</div>2021-02-27</li><br/>
</ul>