你好，我是Tony Bai。

刚刚完成专栏结束语，我又马不停蹄地开始撰写这篇加餐，因为在结束语中我曾提到过对专栏没有介绍指针类型的不安，如果你是编程初学者，或者只有动态语言的经验，又或者只有像Java这类不支持指针的静态语言编程的经验，缺少指针的讲解就可能会给你的学习过程带来一些困惑。

因此，在这一篇加餐中，我就来补上指针类型这一课。**不过，我建议你不要把这篇当作加餐，而是当作本专栏必学的一节课**。

那么什么是指针呢？它和我们常见的Go类型，比如int、string、切片类型等有什么区别呢？下面我们就来一探究竟!

## 什么是指针类型

和我们学过的所有类型都不同，指针类型是依托某一个类型而存在的，比如：一个整型为int，那么它对应的整型指针就是\*int，也就是在int的前面加上一个星号。没有int类型，就不会有\*int类型。而int也被称为\*int指针类型的**基类型**。

我们泛化一下指针类型的这个定义：**如果我们拥有一个类型T，那么以T作为基类型的指针类型为\*T**。

声明一个指针类型变量的语法与非指针类型的普通变量是一样的，我们以声明一个\*T指针类型的变量为例：

```plain
var p *T
```

不过Go中也有一种指针类型是例外，它不需要基类型，它就是**unsafe.Pointer**。unsafe.Pointer类似于C语言中的void\*，用于表示一个通用指针类型，也就是**任何指针类型都可以显式转换为一个unsafe.Pointer，而unsafe.Pointer也可以显式转换为任意指针类型**，如下面代码所示：
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（7） 💬（2）<div>看完整个专栏，只能说一句，老师来极客时间开专栏，太晚了，期待新课</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/e5/f3df7b02.jpg" width="30px"><span>ly</span> 👍（5） 💬（2）<div>看完老师的课，对go的喜欢又多了一分，老师能不能出一门实战的课，系统设计加代码实现，感觉就这一门看不过瘾</div>2022-03-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qeL7fNxa4BVLoVicIHwH221lM8EVsKlDSNmn6iaa18ALvpiaRFuesLk4aq3q11BpAIFwMR5nebDQK5ldZykZkK5Pw/132" width="30px"><span>xiaoru</span> 👍（4） 💬（1）<div>二级指针例子中foo函数返回会栈桢空间不是应该被回收吗？为什么还能取到b中的值？</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>tony bai 老师，文中的这句话：“如果我们需要跨函数改变一个指针变量的指向，我们就不能选择一级指针类型作为形参类型了。因为一级指针只能改变普通变量的值，无法改变指针变量的指向。”

没有太理解，我通过传递一个变量的指针到另外一个函数中，然后在另外一个函数中，用另一个变量的指针地址是可以赋值的，但是函数外，传递的变量的指针没有改变，不知道为什么？ 这块能在解释一下么？</div>2023-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/35/82915b9b.jpg" width="30px"><span>五彩斑斓的輝</span> 👍（2） 💬（2）<div>指针无论是在 Go 中，还是在其他支持指针的编程语言中，存在的意义就是为了是“可改变”。在 Go 中，我们使用 *T 类型的变量调用方法、以 *T 类型作为函数或方法的形式参数、返回 *T 类型的返回值等的目的，也都是因为指针可以改变其指向的内存单元的值。

可改变，怎么理解啊？如果不用指针也是可以改变的吧？</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>Tony bai 老师 ，文中有一处小错误。

在“多个指针变量可以指向同一个变量的内存单元的，这样通过其中一个指针变量对内存单元的修改，是可以通过另外一个指针变量的解引用反映出来的，比如下面例子：”

这段文字下面的代码中 ： p2指向变量b所在内存单元 应该改为 p2指向变量a所在内存单元 的吧？</div>2023-05-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epaH1gHotWQumjRxuX89vHeak6NvLjcrrWApsFkcXTpmh7SOVN5bUO6OPiaEMia5MZjKv2yhTt42icEg/132" width="30px"><span>crazyball</span> 👍（1） 💬（1）<div>催更大白老师进阶或实战课~</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e1/9e/4107db55.jpg" width="30px"><span>Elroy</span> 👍（1） 💬（1）<div>最开始看到课程的名字，误以为很基础，就随意翻了几篇感兴趣的看看，没想到干货满满，又从头看了一篇。讲的真好！</div>2022-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（1）<div>go2 会把macro加回来吗？</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（1） 💬（1）<div>期待白老师出一个实战课</div>2022-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/KZN2M9CPvWZtjfUblowkxaYdHCfhq6mUOFcKkOAzzR9PVJm4IYUsVP47rHbwZNQT6qxavazjJzn14wpiawKPTaA/132" width="30px"><span>Geek_4b9101</span> 👍（1） 💬（1）<div>结束了，不够看啊，还有吗</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（1） 💬（1）<div>惊喜。谢谢老师的加餐</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/2e/02/7f151e08.jpg" width="30px"><span>听说昵称太长了躲在树后面会被别人看见的</span> 👍（0） 💬（1）<div>看我老师的 go，对 c 语言的好感又增加了，谁说 c 只能面向过程，简直是背了个世纪大锅</div>2023-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>go是怎么区分变量应该是分配在堆上还是栈上的</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（4）<div>老师太良心了，又是一篇质量教学。
突然想到一个问题， 为什么很多语言都选择 默认值传递 方式。比如 c，python，go，java。 都是值传递。
请教老师 默认值传递的 好处是什么，为什么这些大佬设计语言时 不默认为 引用传递。
值传递 要copy数据 不是麻烦了吗</div>2022-02-26</li><br/>
</ul>