你好，我是卢誉声。

谈到编程范式，C++自诞生之初就自诩为一种“多范式”语言，而泛型编程，作为一种重要的编程范式，是C++诞生时就支持的一种核心特性。

也许你觉得自己离泛型很远，平时也没有在自己的库或者应用中，使用泛型编程作为模块接口或对外接口，其实不是，我们平时用的C++标准库STL，甚至最常使用的std::string，都是以泛型编程作为理念设计并实现的。

那泛型编程到底是什么？C++如何支持泛型能力，又存在哪些问题？这是我们今天要解决的问题。学完你就会明白，为何Concepts会是C++泛型编程中兼具颠覆性与实用性的一种新特性。

课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)即可获取。

## 模板：C++泛型编程的基石

长期以来，软件重用一直都是软件工程追求的目标，而泛型编程为软件重用创造了可能性。

**所谓泛型编程，指的是通过组件的灵活组合来实现软件，而这些组件通过对定义做出最小“假设”来实现最大灵活性。**在讨论泛型编程问题的时候，我们需要区分弱类型语言和强类型语言。

对于脚本语言，如Perl、PHP、Python、JavaScript或Ruby都属于弱类型语言，对它们来说，其变量本身并不区分类型，所有类型都是在运行时确定的，因此泛型能力被推迟到了运行时。这是一种语言设计的技巧，把这些复杂性交给运行时再决定。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师两个问题：
Q1：函数名称后面的尖括号是什么意思？
函数定义如下：
template &lt;size_t Size, class T, typename U&gt;
void fillContainer(T&amp; collection, U value) {
定义中，fillContainer后面没有尖括号&lt;&gt;

调用函数：
fillContainer&lt;10, std::deque&lt;int32_t&gt;, int32_t&gt;

调用时，后面加的尖括号&lt;&gt;是什么意思？

Q2：不定模板参数的递归怎么终止？
不定模板参数定义如下：
double sum(T value, Targs... Fargs) {    
return static_cast&lt;double&gt;(value) + sum(Fargs...);}
这个定义，似乎是递归，但怎么终止递归？看起来是无穷递归。</div>2023-01-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9cTfuIx7ptLU3RSZBiazicBEl426fWo4b7ZC5aKlicL1W8UnalpVdNShNBUHjibvPGB8n5S942xxqTQ/132" width="30px"><span>Geek_a343c9</span> 👍（0） 💬（1）<div>老师，Python应该是强类型语言吧？</div>2023-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/db/f1/1015328a.jpg" width="30px"><span>Geek_QiDian</span> 👍（0） 💬（1）<div>请问老师，Concepts 能将以上四个问题都解决了吗？</div>2023-01-24</li><br/>
</ul>