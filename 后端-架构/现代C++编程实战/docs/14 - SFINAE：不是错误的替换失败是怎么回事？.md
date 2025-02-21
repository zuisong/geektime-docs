你好，我是吴咏炜。

我们已经连续讲了两讲模板和编译期编程了。今天我们还是继续这个话题，讲的内容是模板里的一个特殊概念——替换失败非错（substitution failure is not an error），英文简称为 SFINAE。

## 函数模板的重载决议

我们之前已经讨论了不少模板特化。我们今天来着重看一个函数模板的情况。当一个函数名称和某个函数模板名称匹配时，重载决议过程大致如下：

- 根据名称找出所有适用的函数和函数模板
- 对于适用的函数模板，要根据实际情况对模板形参进行替换；替换过程中如果发生错误，这个模板会被丢弃
- 在上面两步生成的可行函数集合中，编译器会寻找一个最佳匹配，产生对该函数的调用
- 如果没有找到最佳匹配，或者找到多个匹配程度相当的函数，则编译器需要报错

我们还是来看一个具体的例子（改编自参考资料 \[1]）。虽然这例子不那么实用，但还是比较简单，能够初步说明一下。

```c++
#include <stdio.h>

struct Test {
  typedef int foo;
};

template <typename T>
void f(typename T::foo)
{
  puts("1");
}

template <typename T>
void f(T)
{
  puts("2");
}

int main()
{
  f<Test>(10);
  f<int>(10);
}
```
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/c9/e3/28c16afa.jpg" width="30px"><span>三味</span> 👍（37） 💬（1）<div>emmmm....
这一节内容如果是半年前看到，应该能节省我好多时间去写序列化，真是我实实在在的需求啊！
我自己在写数据序列化为json文本的时候，就遇到了这样头疼的问题：如何根据类型，去调用对应的函数。
如果是简单的int，bool，float，直接特化就好了。
如果是自定义的结构体呢？我的做法就是判断自定义结构体中是否有serializable和deserializable函数，就用到了文中最开始的方法判断。
然而那会儿我写得还是太简单粗暴，在代码中用的是if去判断，对于不支持的类型，直接报错，并不能做到忽略。
看了本文之后，真是受益颇多啊！留言于此，告诉大家，别以为用不到这些内容，都是实实在在的干货！</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（16） 💬（2）<div>请问有编译器本身什么工具或者日志模式，可以显示模版实例化的过程？</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/89/da/e86b9932.jpg" width="30px"><span>_呱太_</span> 👍（6） 💬（1）<div>刚更新的时候看得头晕目眩，发现基础不够。回头抽空撸完了 STL 标准库 和 effective modern C++，回过头来看豁然开朗，真实受益匪浅</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c0/45/069cd477.jpg" width="30px"><span>好好虚度时光</span> 👍（6） 💬（2）<div>表示真的太烧脑了</div>2020-01-17</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（3） 💬（1）<div>标签分发那里的：
template void append(C&amp; container, T* ptr, size_t size)
{ _append( container, ptr, size, integral_constant&lt; bool, has_reserve&lt;C&gt;::value&gt;{});}
这个integral_constant&lt; bool, has_reserve&lt;C&gt;::value&gt;{}看不明白
integral_constant是上一讲的
template &lt;class T, T v&gt;
struct integral_constant {
  static const T value = v;
  typedef T value_type;
  typedef integral_constant type;
};
吧？
has_reserve&lt;C&gt;::value的::value是啥意思？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/60/8ea658a9.jpg" width="30px"><span>西加加</span> 👍（3） 💬（1）<div>看完了两课之后，正儿八经的想把各种 type_traits 用起来了。</div>2020-05-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NyFOEueITjaGLpakMEuWAqVQjo1uDIXlpDdpCxXGfaWiaXzibLQ3WgOFCe8D9FvCmyjsGT7jDsLUbkt8jt2aVs9g/132" width="30px"><span>geek</span> 👍（2） 💬（1）<div>老师，
template &lt;typename T,
          typename = void_t&lt;&gt;&gt;
struct has_reserve : false_type {};

template &lt;typename T&gt;
struct has_reserve&lt;
  T, void_t&lt;decltype(
       declval&lt;T&amp;&gt;().reserve(1U))&gt;&gt;
  : true_type {};
第二个是一个类特化，但我理解，第二个中void的模板参数的推导结果和第一个是一样的。那此处 更特殊 这个意思是体现在 void的模板参数推导过程（无错）吗？</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/36/88/20b6a6ee.jpg" width="30px"><span>Simon</span> 👍（1） 💬（1）<div>typename = void_t&lt;&gt; 这个写法是什么意思？类型名是不重要的？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（1） 💬（2）<div>
template &lt;typename T,
          typename = void_t&lt;&gt;&gt;
struct has_reserve : false_type {};
这里的冒号是什么语法？</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/a5/28/125b172a.jpg" width="30px"><span>。</span> 👍（0） 💬（1）<div>用 void_t 实现的 has_reserve 函数有一些问题，它没法判断类型的reserve 方法的返回值是否是 void，所以可以修改一下：

template &lt;typename T, typename = void&gt;
struct has_reserve : std::false_type {};

template &lt;typename T&gt;
struct has_reserve&lt;T, std::__void_t&lt;decltype(std::declval&lt;T&amp;&gt;().reserve(1U))&gt;&gt;
    : std::is_void&lt;decltype(std::declval&lt;T&amp;&gt;().reserve(1U))&gt; {};</div>2024-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（0） 💬（2）<div>void_t代码例子后边没有解释void_t的作用，或者没有typename=void_t&lt;&gt;这部分 为什么不行。
另外typename=void_t&lt;&gt;这个是什么神仙语法？</div>2023-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7d/a1/46c5293c.jpg" width="30px"><span>yuchen</span> 👍（0） 💬（3）<div>请问，为什么 ‘declval&lt;T&amp;&gt;().reserve(1U)’中为什么要使用T&amp;而不是T？</div>2023-06-16</li><br/><li><img src="" width="30px"><span>Roblaboy</span> 👍（0） 💬（1）<div>我这边提示 enable_if_t 不是模板C&#47;C++(864) 是为什么，我这边用的是C++17</div>2022-09-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK418DKQ4eFh00D6vwqE7nJEX1Ou9DWDHKV2Zj21lq00qK6RzpY6SP3ic0I1hMnbvxQBQSCzzOomNg/132" width="30px"><span>Geek_fa7226</span> 👍（0） 💬（1）<div>auto append(C&amp; container, T* ptr, size_t size) -&gt; decltype（...）中的-&gt;是什么语法？</div>2022-09-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/JWoFanyWDk7lWL7g8rLYI0icH1XOVoCyjR9HoMzliauxggPSWWeYVleqKwiaUnBEChfIctoFzVoBqqVT3Lot18Srg/132" width="30px"><span>Geek_fd78c0</span> 👍（0） 💬（1）<div>

请问老师这个-&gt;是什么意思，不太懂这个语法？
template &lt;typename C, typename T&gt;
auto append(C&amp; container, T* ptr,
            size_t size)
  -&gt; decltype(
    declval&lt;C&amp;&gt;().reserve(1U),
    void())
</div>2022-06-30</li><br/><li><img src="" width="30px"><span>Geek_7ce030</span> 👍（0） 💬（2）<div>模板本身图灵完备但是语法极其晦涩丑陋，既然如此，为何不用Python语法代替现有模板语法，本质上是暴露编译期接口，当前用模板暴露，也可以用正常的语言暴露，让用户更轻松地控制编译过程。可能是积重难返吧。</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/2e/376a3551.jpg" width="30px"><span>ano</span> 👍（0） 💬（1）<div>老师，我有个疑问，关于这一句
静态多态的限制？
“在 C 类型没有 reserve 成员函数的情况下，编译是不能通过的，会报错。这是因为 C++ 是静态类型的语言，所有的函数、名字必须在编译时被成功解析、确定”
if (has_reserve&lt;C&gt;::value)

我的理解是，在编译时，if 语句中的 has_reserve 进行模板匹配，决议，发现那个特化的 true_type has_reserve, 产生 substitution failure, 然后就会回到那个 false_type 的 has_reserve, 最终实例化成 false_type 的 has_reserve，然后 value 是 false, 所以这个 if 语句中始终为 false，但是不应该会编译错误呀。
不知道我哪里理解的不对？
</div>2021-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2ibrq71Y5Ww3KDRibDxF1gt9YDEPuZkv4ITHEP1u4vvjpPDukkLoK4ngQy1hKKzccnsicLkUAda7sPpibR6Kyb0cfQ/132" width="30px"><span>chang</span> 👍（0） 💬（4）<div>
template &lt;typename T&gt;
struct has_reserve {
  struct good { char dummy; };
  struct bad { char dummy[2]; };
  template &lt;class U,
            void (U::*)(size_t)&gt;
  struct SFINAE {};
  template &lt;class U&gt;
  static good
  reserve(SFINAE&lt;U, &amp;U::reserve&gt;*);
  template &lt;class U&gt;
  static bad reserve(...);
  static const bool value =
    sizeof(reserve&lt;T&gt;(nullptr))
    == sizeof(good);
};

这个貌似对标准库的vector无效？因为参数类型不匹配？</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b5/d4/147abdaa.jpg" width="30px"><span>乐意至极</span> 👍（0） 💬（2）<div>class GoodClass {
    void reserve(size_t x);
};

class BadClass {
};

    std::cout &lt;&lt; has_reserve&lt;BadClass&gt;::value &lt;&lt; std::endl;
    std::cout &lt;&lt; has_reserve&lt;GoodClass&gt;::value &lt;&lt; std::endl;


template &lt;typename T&gt;
struct has_reserve {
  struct good { char dummy; };
  struct bad { char dummy[2]; };
  template &lt;class U,
            void (U::*)(size_t)&gt;
  struct SFINAE {};
  template &lt;class U&gt;
  static good
  reserve(SFINAE&lt;U, &amp;U::reserve&gt;*);
  template &lt;class U&gt;
  static bad reserve(...);
  static const bool value =
    sizeof(reserve&lt;T&gt;(nullptr))
    == sizeof(good);
};

老师，请问has_reserve该怎么用呢？两者输出都是0啊</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/29/57/aaa8612e.jpg" width="30px"><span>AlphaCat</span> 👍（0） 💬（1）<div>老师，替换失败非错（substituion failure is not an error）， &quot;substituion&quot; 掉了一个 t，应该是 Substitution </div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/60/8ea658a9.jpg" width="30px"><span>西加加</span> 👍（0） 💬（2）<div>利用 variant 的 std::get 方法，写一个 sfine 用于判断一个 variant 类型里是否联合了 float. 代码和问题如下：
template &lt;typename T, typename ...&gt;
struct CheckVariant {
    static constexpr int value =  1;
};
template &lt;typename T&gt;
struct CheckVariant&lt;T,
    decltype(get&lt;float&gt;( declval&lt;T&gt;() ))
    &gt;
{
    static constexpr int value = 2;
};
...
    if constexpr (CheckVariant&lt;decltype(v)&gt;::value == 1) {
        cout &lt;&lt; get&lt;float&gt;(v) &lt;&lt; endl;
    }
...

可是发现这样的 SFINAE 不起作用，把模板特化代码改为利用 逗号表达式，让 decltype 取值就可以了：

template &lt;typename T&gt;
struct CheckVariant&lt;T,
    decltype((get&lt;float&gt;( declval&lt;T&gt;() ), void()))
    &gt;
{
    static constexpr int value = 2;
};

这是为什么呢？  
</div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（2）<div>https:&#47;&#47;en.cppreference.com&#47;w&#47;cpp&#47;types&#47;enable_if
&quot;
Possible implementation
template&lt;bool B, class T = void&gt;
struct enable_if {};
 
template&lt;class T&gt;
struct enable_if&lt;true, T&gt; { typedef T type; };
&quot;

下列的测试代码可以编译，运行
&quot;
#include &lt;type_traits&gt;
#include &lt;iostream&gt;

template &lt;typename X, typename T, typename Y&gt;
typename std::enable_if&lt;std::is_same&lt;T, int&gt;::value&gt;::type update(X x, T t, Y y)
{
    std::cout &lt;&lt; &quot;int&quot; &lt;&lt; std::endl;
}

int main () {
    float a = 1.4;
    int b = 1;
    double c =2.2;
    update(a, b, c);
}
&quot;

其中我用的是std::enable_if&lt;std::is_same&lt;T, int&gt;::value&gt;， 并没有提供参数来推导T，
这是不是意味着对于true这种情况的偏特化implementation是
template&lt;class T = void&gt;
struct enable_if&lt;true, T&gt; { typedef T type; };

而不是

template&lt;class T&gt;
struct enable_if&lt;true, T&gt; { typedef T type; };

谢谢！</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/29/c0/86fa3e92.jpg" width="30px"><span>贾陆华</span> 👍（0） 💬（1）<div>吴老师，写的满满干货，之前模板并没有深入学习，才知道模板可以这么花，用途可以这么多</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/4d/90ea92f8.jpg" width="30px"><span>光城~兴</span> 👍（0） 💬（1）<div>假设U是一个Class,内部有foo方法与bar方法，那么U::*表示的是所有成员函数的指针吧，而U::foo*是foo成员函数指针，还请老师指点。</div>2020-01-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（0） 💬（1）<div>没看这几篇文章前，以为理解模板了，现在才知道模板博大精深👍</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/96/c679bb3d.jpg" width="30px"><span>总统老唐</span> 👍（0） 💬（2）<div>吴老师，关于这一课，有 3 个问题
1，在最开始定义 has_reserve 类时，两个 reserve 模板函数实际上只是声明了，但是并没有真正的函数体，而最后的 value 成员实际上是用 nullptr 调用了 reserve 函数，这就相当于调用一个没有只有声明没有定义的函数，为什么没有报错？
2，关于模板函数的调用
假设有如下模板
template &lt;typename T1, typename T2&gt;
int add(T1 a, T2 b);
既可以add&lt;int, double&gt;(1, 2.5)调用，也可以add(1, 2.5)调用，两者的差别是不是第一种方式相当于先声明了一个特化版本，在用这个特化版本来调用，后一种方式是编译器自行推断？但若是没有定义对应的特化版本，第一种方式和第二种方式是不是完全没有区别？
3，在 void_t 的部分，模板定义时，第二个参数是这样写的：typename = void_t&lt;&gt;， 我试了一下，直接写成 typename = void，也是可以的，你采用这种写法是有什么特殊考虑吗？</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（3）<div>“
template &lt;typename T, typename = void_t&lt;&gt;&gt;
struct has_reserve : false_type {};

template &lt;typename T&gt;
struct has_reserve&lt;T, void_t&lt;decltype(declval&lt;T&amp;&gt;().reserve(1U))&gt;&gt; : true_type {};

declval().reserve(1U) 用来测试 C&amp; 类型的对象是不是可以拿 1U 作为参数来调用 reserve 成员函数
“
请问
- 如果是, decltype(declval&lt;T&amp;&gt;().reserve(1U))&gt; 返回的是void，这个好理解，因为void_t会把任何数目（包括零个）的类型转换为类型void
- 如果不是, 编译器看到decltype(declval&lt;T&amp;&gt;().reserve(1U))&gt; 会做什么？
                  然后编译器看到void_t&lt;decltype(declval&lt;T&amp;&gt;().reserve(1U))&gt; 又会做什么？
</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/0e/29/fa3601d3.jpg" width="30px"><span>🐶的巴普洛夫</span> 👍（0） 💬（0）<div>人生苦短，我不会用C++</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/89/207cc841.jpg" width="30px"><span>HI</span> 👍（0） 💬（0）<div>666</div>2022-08-22</li><br/>
</ul>