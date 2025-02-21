你好，我是吴咏炜。

我们已经连续讲了几讲比较累人的编译期编程了。今天我们还是继续这个话题，但是，相信今天学完之后，你会感觉比之前几讲要轻松很多。C++ 语言里的很多改进，让我们做编译期编程也变得越来越简单了。

## 初识 constexpr

我们先来看一些例子：

```c++
int sqr(int n)
{
  return n * n;
}

int main()
{
  int a[sqr(3)];
}
```

想一想，这个代码合法吗？

看过之后，再想想这个代码如何？

```c++
int sqr(int n)
{
  return n * n;
}

int main()
{
  const int n = sqr(3);
  int a[n];
}
```

还有这个？

```c++
#include <array>

int sqr(int n)
{
  return n * n;
}

int main()
{
  std::array<int, sqr(3)> a;
}
```

此外，我们前面模板元编程里的那些类里的 `static const int` 什么的，你认为它们能用在上面的几种情况下吗？

如果以上问题你都知道正确的答案，那恭喜你，你对 C++ 的理解已经到了一个不错的层次了。但问题依然在那里：这些问题的答案不直观。并且，我们需要一个比模板元编程更方便的进行编译期计算的方法。

在 C++11 引入、在 C++14 得到大幅改进的 `constexpr` 关键字就是为了解决这些问题而诞生的。它的字面意思是 constant expression，常量表达式。存在两类 `constexpr` 对象：
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（12） 💬（1）<div>我觉得我学习这个专栏只是为了能看懂这些新特性，写是写不出来，规则太多太复杂了。</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/a6/3f15ba2f.jpg" width="30px"><span>czh</span> 👍（10） 💬（2）<div>老师好，有个小疑问，文中提到：

“上一讲的结尾，我们给出了一个在类型参数 C 没有 reserve 成员函数时不能编译的代码：”


这里提到使用 if constexpr，可以解决上述问题。这里没有过多的解释，我理解是：使用if constexpr之后，如果没有reserve成员，那就会在编译期跳过这个if中的内容，因此不会检查container.reserve()。

不知道理解是否正确？</div>2020-02-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NyFOEueITjaGLpakMEuWAqVQjo1uDIXlpDdpCxXGfaWiaXzibLQ3WgOFCe8D9FvCmyjsGT7jDsLUbkt8jt2aVs9g/132" width="30px"><span>geek</span> 👍（2） 💬（2）<div>试着回答一下两个思考问题：
1 我认为不用consexpr,就要用enable_if，类似于上一节的append方法那样，在有两种可能情况时，要写两个方法，做标签分发。这种方式的一个推广就是：有多少种可能，就要写多少个对应的分发方法。
2 不用constexpr的缺点，就是代码冗余而且不易读。那么用constexpr的优点就是代码无冗余，易读。</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/a6/96cee976.jpg" width="30px"><span>Jerry Tan</span> 👍（2） 💬（5）<div>您好老师, 请问想学C++ 您有什么比较好的推荐的开发工具吗  谢谢 </div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/7c/12c571b6.jpg" width="30px"><span>Slience-0°C</span> 👍（1） 💬（1）<div>常量区分编译期？和运行期？</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/7c/12c571b6.jpg" width="30px"><span>Slience-0°C</span> 👍（1） 💬（1）<div>老师好，现代C++如何优雅的定义字符串常量？直接使用const std::string var = &quot;xxxx &quot;有些静态代码检查工具会提示可能会抛出无法捕获的异常！</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c2/da/5818c896.jpg" width="30px"><span>心态正常</span> 👍（1） 💬（1）<div>吴老师，您好，有个问题想请教一下，文章开头的两个示例我在centos8上使用g++ 8.3.1的编译器编译通过了，因为没有用到constexpr的特性，预期在int a[n]这一行会报错，但是实际上并没有给出错误，这是编译器做了优化处理吗？</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f4/2b/f74346da.jpg" width="30px"><span>清水</span> 👍（1） 💬（1）<div>吴老师，你好，请教个问题

constexpr int factorial(int n)
{
  if (n == 0) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}
如果constexpr 修饰函数 这样是编译不过的，提示not a return-statement (至少c++11不行)
没有尝试过是否其他编译器 多行编译 通过
如果修改为一行表达式是没问题的，那么这是constexpr关键字 用法要求还是其他原因导致？</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/ee/211e86cd.jpg" width="30px"><span>talor</span> 👍（1） 💬（1）<div>您好，
constexpr int a = 42;
constexpr const int&amp; b = a;
这个例子编译不过，编译器是gcc 10.2.1</div>2020-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIQz0Micjv7w7z4vFcXvLSSzI3dVZLBDG83zfDWhMiaQqtkHzIWWSL276GqHGBRKWrR3xP5JjmhPpnA/132" width="30px"><span>g_boshu</span> 👍（1） 💬（1）<div>吴老师您好，我对以下代码有点儿疑惑：

&#47;&#47; Type trait to detect std::pair
template &lt;typename T&gt;
struct is_pair : std::false_type {};
template &lt;typename T, typename U&gt;
struct is_pair&lt;std::pair&lt;T, U&gt;&gt;
  : std::true_type {};
template &lt;typename T&gt;
inline constexpr bool is_pair_v =
  is_pair&lt;T&gt;::value;

template &lt;typename T, typename U&gt;
struct is_pair&lt;std::pair&lt;T, U&gt;&gt;: std::true_type {}; 看着应该是一个偏特化，模板的参数却变多了，一般偏特化不应该是参数变少吗？谢谢</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（1）<div>文中一开始用constexpr
改造的例子，之所以可以，一定是在使用constexpr的地方“就地”调用了赋值运算符右侧的函数，这样才能得到一个编译期的常量，所以，“内联”是constexpr的应有之意。但是在类外，必须加上inline才可以。

const本质是一个运行时常量，constexpr才是编译期常数，除了内联展开这个含义，再根据文中ODR的表述，说明constexpr变量是切实分配了内存空间的，是一个左值对象。综合上面的考虑，constexpr意味着被声明的对象是存放在数据段里面的。


constexpr 变量模板表达一个和某个类型相关的编译期常量，让变量也可以是模板，这句话在本课中，我觉得理解成“把模板对象用一个变量命名”更合适，即把所有符号都绑定到了一个实体上，这样if constexpr才变得可行。解决了上一讲中说的c++中不能像Python一样写代码的问题。</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/4c/08/96c8318a.jpg" width="30px"><span>Chillstep</span> 👍（0） 💬（1）<div>老师您好，这一段我发现有一些疑问：&quot;这是因为 ODR-use 的类静态常量也需要有一个定义，在没有内联变量之前需要在某一个源代码文件（非头文件）中这样写：const int magic::number = 42;  &quot;这一段我实验了下发现并不能过编译，我认为number已经是const的，应该是没办法在赋值的了，这里应该只需要const int magic::number;即可，这样是可以过编译的。</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/2e/376a3551.jpg" width="30px"><span>ano</span> 👍（0） 💬（1）<div>老师，我想请教一下。一个 function 标记为 inline, 但如果 function body 中有循环的话，编译器就不会在这个函数的调用处 inline? 编译器是出于什么考虑，不做这个 inline?</div>2021-10-18</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>
&#47;&#47; Type trait to detect std::pair
template &lt;typename T&gt;
struct is_pair : std::false_type {};
template &lt;typename T, typename U&gt;
struct is_pair&lt;std::pair&lt;T, U&gt;&gt;
  : std::true_type {};
template &lt;typename T&gt;
inline constexpr bool is_pair_v =
  is_pair&lt;T&gt;::value;

is_pair模板并没有定义value成员啊，为什么可以::value？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7d/a1/46c5293c.jpg" width="30px"><span>yuchen</span> 👍（0） 💬（2）<div>template &lt;typename T&gt;
struct is_pair : std::false_type {};
template &lt;typename T, typename U&gt;
struct is_pair&lt;std::pair&lt;T, U&gt;&gt;
  : std::true_type {};
template &lt;typename T&gt;
inline constexpr bool is_pair_v =
  is_pair&lt;T&gt;::value;
吴老师好，请问这里template &lt;typename T, typename U&gt;
struct is_pair&lt;std::pair&lt;T, U&gt;&gt;是特化还是偏特化呢？</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7c/34/cd10f00b.jpg" width="30px"><span>O</span> 👍（0） 💬（1）<div>老师好，我想问一下，想容器嵌套类似vector&lt;vector&lt;&gt;&gt;之类的，output如何判断</div>2020-07-16</li><br/><li><img src="" width="30px"><span>zKerry</span> 👍（0） 💬（1）<div>
int sqr(int n)
{
  return n * n;
}

int main()
{
  const int n = sqr(3);
  int a[n)];
}
其中：int a[n)] 没有问题？</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/4d/90ea92f8.jpg" width="30px"><span>光城~兴</span> 👍（0） 💬（3）<div>对老师的输出函数进行修改：如下

template&lt;typename T, typename Cont&gt;
auto output_element(std::ostream &amp;os, const T &amp;element,
                    const Cont &amp;)
-&gt; typename std::enable_if&lt;is_pair&lt;typename Cont::value_type&gt;::value, bool&gt;::type {
    os &lt;&lt; element.first &lt;&lt; &quot; =&gt; &quot; &lt;&lt; element.second;
    return true;
}

template&lt;typename T, typename Cont&gt;
auto output_element(std::ostream &amp;os, const T &amp;element,
                    const Cont &amp;)
-&gt; typename std::enable_if&lt;!is_pair&lt;typename Cont::value_type&gt;::value, bool&gt;::type {
    os &lt;&lt; element;
    return false;
}

调用处：
output_element(os, elem, container);

这个方法学习自老师之前讲过的SFINAE！

另外，针对老师的代码有些疑问：
老师代码调用处：
output_element(os, *it, container, is_pair&lt;element_type&gt;());
实际上在这里就确定了element_type是不是pair，也就是这里传递进去直接就是true_type或者false_type，针对,map&#47;vector&#47;set等直接就可以区分开来，不需要写：std::declval&lt;typename Cont::key_type&gt;()。
也是可以正常完成输出的，但是当传递的是true_type且容器没有key_type的时候就是SFINAE问题，调用另一个重载函数。
问题是，一个容器元素是pair，那么is_pair&lt;element_type&gt;()就是true_type，而既然是pair了，也就有了key_type，所以这个必然成立，也就是写与不写都可以。另外，当不是pair，就是false_type，肯定调false_type的output_element重载咯，所以我得出这里写这个std::declval&lt;typename Cont::key_type&gt;()没有啥子用，并且代码测试过确实可以不写，望老师指点！</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/4d/90ea92f8.jpg" width="30px"><span>光城~兴</span> 👍（0） 💬（1）<div>constexpr变量仍是const这一块的例子：
```cpp
constexpr int a = 42;
constexpr const int&amp; b = a;
```
第二行会报错 需要一个常量表达式
去掉constexpr是不是更好？ 貌似对这一块解释没影响～
</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/eb/2285a345.jpg" width="30px"><span>花晨少年</span> 👍（0） 💬（2）<div>为什么文章开头提到的两个例子，都是合法的吗，编译运行都没问题。
第一个例子理所当然的像应该有问题，但是仔细想了下，为什么要有问题呢，数据大小为什么就要编译器确定呢，运行期确定不行吗。而结果是确实没有问题，这里面的玄机是什么呢
第二个例子应该是 int a[n];吧
第二个例子是因为const常量的原因，编译器会强制sqr函数编译器运行特定参数吗
</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（0） 💬（1）<div>如果没有consrexpr条件语句那输出函数就应该写两个吧，也是用sfinae，用那种enable_if形式，true or false</div>2019-12-30</li><br/>
</ul>