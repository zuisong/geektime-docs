你好，我是Chrono。

前两周我们从宏观的层面上重新认识了C++，从今天开始，我们将进入一个新的“语言特性”单元，“下沉”到微观的层面去观察C++，一起去见一些老朋友、新面孔，比如const、exception、lambda。

这次要说的，就是C++11里引入的一个很重要的语言特性：自动类型推导。

## 自动类型推导

如果你有过一些C++的编程经验，了解过C++11，那就一定听说过“**自动类型推导**”（auto type deduction）。

它其实是一个非常“老”的特性，C++之父Bjarne Stroustrup（B·S )早在C++诞生之初就设计并实现了它，但因为与早期C语言的语义有冲突，所以被“雪藏”了近三十年。直到C99消除了兼容性问题，C++11才让它再度登场亮相。

那为什么要重新引入这个“老特性”呢？为什么非要有“自动类型推导”呢？

我觉得，你可以先从字面上去理解，把这个词分解成三个部分：“自动”“类型”和“推导”。

- “自动”就是让计算机去做，而不是人去做，相对的是“手动”。
- “类型”指的是操作目标，出来的是编译阶段的类型，而不是数值。
- “推导”就是演算、运算，把隐含的值给算出来。

好，我们来看一看“自动类型推导”之外的其他几种排列组合，通过对比的方式来帮你理解它。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/02/198fc6d6.jpg" width="30px"><span>Mervin</span> 👍（18） 💬（1）<div>课后题：
1. 给程序作者带来了一些便利，但是给读者比较大的麻烦，所以我认为尽量还是应该在比较清晰明确的地方使用，并加以明确的注释。
2.auto推导的是编译器计算变量初始值得到类型的，decltype也是分析表达式但是不需要计算表达式，所以它与表达式本身有很大关系。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/17/89c3d249.jpg" width="30px"><span>下雨天</span> 👍（14） 💬（2）<div>decltype(auto) x1 = (x); &#47;&#47; 推导为int&amp;，因为(expr)是引用类型。老师，这里为什么是引用？x不是值吗？</div>2020-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK5icO2A4K7HYTYfQoagTz7VbtgxfS2ibBqLnKVWwQZgsePibZWFvFJEhPT8BtpQSaFx9IEodyp6c0dw/132" width="30px"><span>Geek_jg3r26</span> 👍（12） 💬（2）<div>老师， 总是在一些c++ 源码看到extern “C” 对这个关键字理解的不是很透</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/6d/85723167.jpg" width="30px"><span>张飞Dear</span> 👍（6） 💬（1）<div>1，算是一个缺点，但是就和容器、条件编译一样，尺有所短寸有所长。用的恰当就好，我现在工作用的的编译器不支持auto，只能自己实验这敲了，用auto 就不用再写那么长的迭代器名称了，很方便。还有使用decltype 来定义迭代器类型  真的是太好用，之前都是用typedef 来进行的。

2，① auto 的“自动推导”能力只能用在“初始化”的场合。不能用在类成员里面初始化。auto 总是推导出“值类型”，绝不会是“引用”。
② decltype 不仅能够推导出值类型，还能够推导出引用类型，也就是表达式的“原始类型”。可以定义类成员类型。</div>2020-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwjtaqgKfnSflr8zPuz6LzE1PsxYa59Cd2QsibbDE4SGxegO0UQpRrVCa4ds2Wx3DgMW1B9VOe4UQ/132" width="30px"><span>Geek_197dc8</span> 👍（6） 💬（2）<div>auto总是推导出“值类型”，但绝不会是“引用”，这句话怎么理解，难道不可以推导出引用的类型嘛？我看你的例子 auto&amp; x1＝x，不是推导出引用类型嘛。</div>2020-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erCibehm9W3tbhKic1RnbTvPVCgWDmludx9YQ97BneVRhyegkr13R6vrFPYol4IYEF98s07MicgOtS0g/132" width="30px"><span>hao</span> 👍（5） 💬（1）<div>罗老师，请问下，在函数内部定义了vector，push_back了很多数据，要将这些vector数据作为函数结果返回，也没释放vector，这样会不会有问题？</div>2020-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLatEq9SWSZv14dEvlhzBJmkhlxDn7iaSuTT1g28U7kRsSjpsuia95JTZQgSGSYVvWkG3ibOMu1gmIwQ/132" width="30px"><span>Geek_ca425d</span> 👍（4） 💬（1）<div>JavaScript弱语言类型就是不对类型做定义，运行时推导的，但这种缺点导致开发大型项目的时候各种困难，我觉得主要就是类型不明确锅，所以后来有了typescript这种js超集。前车之鉴，auto还是要少用的。</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（3） 💬（2）<div>我觉得auto 虽然方便了，但是代码不能都用auto吧，大量的auto反而让程序员摸不着头脑，这就像看一本书所有地方都花下划线就失去了下划线的意义。
auto对于减少冗赘的代码也很有用。比如：之前我们写代码是：
for(vector&lt;int&gt;::const_iterator itr = m_vector.begin(); itr != m_vector.end();++itr)
可以使用auto简化为：
for(auto itr = m_vector.begin(); itr != m_vector.end();++itr)这样写就简单多了。
所有的功能都是建立在好的方向发展的，所有的功能都是工具，工具只有利用对了才是好的，怎么能利用好这时候就看使用者的功底和经验丰富程度了。

decltype 和 auto 一起使用会更为有用。auto 变量的类型只有编译器知道，而 decltype 对于大量运用运算符重载和特化的类型的代码的表示也非常有用。
</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6c/5b/d9ae4fbb.jpg" width="30px"><span>X.</span> 👍（2） 💬（3）<div>请问老师，for (const auto&amp; i : v) {...}这里，为什么说“常引用方式访问元素，避免拷贝代价”  ？为什么不考虑用 for (auto i : v) {...} 呢？</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（2） 💬（2）<div>我倒是觉得auto可以多用啊，隐藏的真正类型完全可以使用vscode的cpp插件或者ide工具直接查看到，不算大的缺点。如果要说C ++11让我最舒服的地方就是auto和using了。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（2） 💬（2）<div>&quot;auto 和 decltype 虽然很方便，但用多了也确实会“隐藏”真正的类型，增加阅读时的理解难度。&quot;
我觉得这很算缺点，它们应该只用在确实很难手动推导出变量类型的地方。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a2/54/49dfb810.jpg" width="30px"><span>宵练2233</span> 👍（1） 💬（1）<div>举一个不适合用auto的例子 Eigen，由于它内部大量使用了Expression Template，用auto会产生很多奇怪的bug。</div>2021-07-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9X140JXPuaKOwmvYb8YFloVXpIakbBCuBBgSepO81ibibZPrFLrHpJevQMdy2hXQc0HRoA75b5u5w/132" width="30px"><span>201201150</span> 👍（1） 💬（1）<div>我想auto 和decltype的引入，关键还是因为C++语言有着一个完善而且强大的type system，在编译阶段就有很多信息可以确定下来。
泛型编程里面，auto关键字确实帮助程序员省去很多工作，这是最大的优点。但是如果auto 关键字满天飞，也会给程序的可读性带来很多问题。使用好关键还是一个度的把握。
auto和decltype两者最大的区别应该是，一个根据值的类型来推导出来变量类型，一个根据表达式的类型推导出来变量类型。</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（1） 💬（1）<div>1. 大量使用auto和delctype确实会有这种问题。所以产量定义和初始化的时候原类型定义还是不错的.auto其实循环展开上用比较合理。delctype在类定义里使用，不传递到外部。
2.auto和delctype其实更多是语法糖的效果。实际类型确定都在编译期。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/23/33/89db6a90.jpg" width="30px"><span>幽殇</span> 👍（0） 💬（1）<div>老师，上面的一个例子：
auto x = 10L; &#47;&#47; auto推导为long，x是long
auto&amp; x1 = x; &#47;&#47; auto推导为long，x1是long&amp;
auto* x2 = &amp;x; &#47;&#47; auto推导为long，x2是long*

这里为什么说x2的auto推导为long而不是long*，因为我使用
auto x2 = &amp;x;
输出的结果与上述结果一样，说明推导出的结果就是long*，为什么还要在auto后加*</div>2023-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b3/7b/95adaf84.jpg" width="30px"><span>学习者</span> 👍（0） 💬（1）<div>好的代码，一定是易读的，而且好的代码，一定带好的注释的，我认为这不算 auto 的缺点，auto 关键字对开发者是非常友好的。</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2c/a7/7f702c49.jpg" width="30px"><span>liy</span> 👍（0） 💬（1）<div>听君一席话胜读十年书！！</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e0/ca/adfaa551.jpg" width="30px"><span>孙新</span> 👍（0） 💬（1）<div>一般用在迭代器，用在接收map查找结果，或者lambda表达式之类的比较省事，也就是临时变量用这个省事。</div>2022-01-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKRpicl9Uy2ia14qefwoibRgdv30xpWpFibJ2fia3KCHUZhXOUKoZCIU6bILyYRibCIcyibyqcXcUgWSRF2A/132" width="30px"><span>Wa7T</span> 👍（0） 💬（1）<div>C++11的标准里写auto无法带走cv操作符，所以在
auto        x = 10L;    &#47;&#47; auto推导为long，x是long
auto&amp;       x1 = x;      &#47;&#47; auto推导为long，x1是long&amp;
auto*       x2 = &amp;x;    &#47;&#47; auto推导为long，x2是long*
const auto&amp; x3 = x;        &#47;&#47; auto推导为long，x3是const long&amp;
auto        x4 = &amp;x3;    &#47;&#47; auto推导为const long*，x4是const long*
这里面，x4应该没有const属性吧？</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/22/11/cab6ca42.jpg" width="30px"><span>Geek_358817</span> 👍（0） 💬（1）<div>auto*       x2 = &amp;x;    &#47;&#47; auto推导为long，x2是long*，

这里为什么auto推导不是long *类型，而是long类型？auto的值推导，是不管值前面的符号吗？</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/71/c83d8b15.jpg" width="30px"><span>一个坏人</span> 👍（0） 💬（1）<div>老师好，请问如何判定 auto 推导的类型对不对，有类似JS typeof 方法？</div>2021-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/17/9f6d67dc.jpg" width="30px"><span>超越杨超越</span> 👍（0） 💬（1）<div>请问老师，auto这种类型推断如果用的非常多，会不会影响编译效率</div>2021-03-04</li><br/><li><img src="" width="30px"><span>企鹅君需要充电</span> 👍（0） 💬（1）<div>auto在特性开发的时候很方便，现在作为range idx&#47;迭代器是简洁明了的常见用法，但如果类型涉及自定义类，又或者只是标准库的简单类型，最好还是明确写出来，若是替代复杂类型最好加点备注。decltype很少用，函数指针用它比较常见吧，其他的引用或者指针考虑可读性我还是习惯写出来；</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/2c/06375913.jpg" width="30px"><span>宇天飞</span> 👍（0） 💬（1）<div>auto 和 decltype 虽然很方便，但用多了也确实会“隐藏”真正的类型，增加阅读时的理解难度，你觉得这算是缺点吗？是否有办法克服或者缓解？
是的
变量的名字中包含类型


说一下你对 auto 和 decltype 的认识。你认为，两者有哪些区别呢？（推导规则、应用场合等）
auto更简单，除了类的属性等不可以用以外，一般用于变量初始化时类型的推导
decltype更通用，任何地方都可以使用，比如自带表达式</div>2020-09-01</li><br/><li><img src="" width="30px"><span>常丁方2</span> 👍（0） 💬（1）<div>老师, c++不是弱类型语言吗? 我在知乎上看到很多人都说c++是弱类型的
https:&#47;&#47;www.zhihu.com&#47;question&#47;19918532</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/d2/9ef1e70d.jpg" width="30px"><span>鲁滨逊</span> 👍（0） 💬（1）<div>没看明白这里：
auto*       x2 = &amp;x;    &#47;&#47; auto推导为long，x2是long*
const auto&amp; x3 = x;        &#47;&#47; auto推导为long，x3是const long&amp;
auto        x4 = &amp;x3;    &#47;&#47; auto推导为const long*，x4是const long*
都是&amp;x，x2的auto推导为long，x4的auto却是long*呢？看到这种问题就意识到自己基础不好了</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/3c/f6e7ebf1.jpg" width="30px"><span>陈英桂</span> 👍（0） 💬（1）<div>就像python的变量的数据类型随时可以改变，根据右值推导出来，这样代码可读性很差。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/3c/f6e7ebf1.jpg" width="30px"><span>陈英桂</span> 👍（0） 💬（1）<div>用auto和decltype给写代码的带来一些便捷性，但是会降低代码的可读性，给维护者的阅读带来一些障碍。
对于迭代器，可以用auto来简化代码，尽量不要用在函数的返回值和入参。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/9c/46/a2c1a99f.jpg" width="30px"><span>yelin</span> 👍（0） 💬（1）<div>2.
推导规则：auto值总是值类型，decltype 不仅能够推导出值类型，还能够推导出引用类型。&amp;,*,const的属性也会被decltype取得
应用场景：auto除了不能在定义类时使用，还有一种不关心具体类型的目的在range-based for的场景尤其明显，在；decltype则没有义类的使用限制，decltype会尤其关心具体的类型值，推导计算得到后才会返回</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/9c/46/a2c1a99f.jpg" width="30px"><span>yelin</span> 👍（0） 💬（1）<div>1. 类型推导用起来方便，代码里都用auto的话，那个感觉应该和python是一样的吧，所以不知道有没有好的解决方案，我在python里的习惯是在命名加前缀，还有就是注释了吧，如果是协作开发的模块，auto我一般也就是用来内部遍历&#47;range-based for之类的场景。请教下老师，还有没有更好的办法。</div>2020-05-27</li><br/>
</ul>