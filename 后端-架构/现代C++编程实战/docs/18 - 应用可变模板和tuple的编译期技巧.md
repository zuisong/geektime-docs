你好，我是吴咏炜。

今天我们讲一个特殊的专题，如何使用可变模板和 tuple 来完成一些常见的功能，尤其是编译期计算。

## 可变模板

可变模板 \[1] 是 C++11 引入的一项新功能，使我们可以在模板参数里表达不定个数和类型的参数。从实际的角度，它有两个明显的用途：

- 用于在通用工具模板中转发参数到另外一个函数
- 用于在递归的模板中表达通用的情况（另外会有至少一个模板特化来表达边界情况）

我们下面就来分开讨论一下。

### 转发用法

以标准库里的 `make_unique` 为例，它的定义差不多是下面这个样子：

```c++
template <typename T,
          typename... Args>
inline unique_ptr<T>
make_unique(Args&&... args)
{
  return unique_ptr<T>(
    new T(forward<Args>(args)...));
}
```

这样，它就可以把传递给自己的全部参数转发到模板参数类的构造函数上去。注意，在这种情况下，我们通常会使用 `std::forward`，确保参数转发时仍然保持正确的左值或右值引用类型。

稍微解释一下上面三处出现的 `...`：

- `typename... Args` 声明了一系列的类型——`class...` 或 `typename...` 表示后面的标识符代表了一系列的类型。
- `Args&&... args` 声明了一系列的形参 `args`，其类型是 `Args&&`。
- `forward<Args>(args)...` 会在编译时实际逐项展开 `Args` 和 `args` ，参数有多少项，展开后就是多少项。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（7） 💬（1）<div>N--&gt;(N-1, N-1)--&gt;(N-2, N-2, N-1)--&gt;(1, 1 , 2 ....N-1)--&gt;(0, 0, 1, 2...N-1)</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（4） 💬（1）<div>compose那是完全没看懂唉，还有sequence那... </div>2020-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDH0RbXvDGVoyRtxs3kLmwSmibqqic4EYYwSH12KqsrrKgpGic7cZXfsicpDMShFTAIT6p3jTJ3ypKzg/132" width="30px"><span>Geek_845be1</span> 👍（3） 💬（1）<div>不用 index_sequence 来初始化 bit_count：

```
consteval int count_bits(unsigned char val)
{
    if (val == 0)
        return 0;
    return (val &amp; 1) + count_bits(val &gt;&gt; 1);
}

template &lt;std::size_t N&gt;
consteval std::array&lt;unsigned char, N&gt; get_bit_count()
{
    std::array&lt;unsigned char, N&gt; tbl{};
    for (auto i = 0; i != N; ++i)
        tbl[i] = count_bits(i);
    return tbl;
}
```</div>2020-12-24</li><br/><li><img src="" width="30px"><span>Geek_a16bbc</span> 👍（2） 💬（1）<div>用for loop來計算那２５６個count_bit()有什麼問題嗎？為什麼一定要在編譯期算好呢？</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>老师，我尝试写了make_integer_sequence，没有看专栏末尾的答案，您看下这段代码满足您思考题的要求吗？有不正确的地方，烦请老师指正。
#include &lt;iostream&gt;
#include &lt;utility&gt;
#include &lt;tuple&gt;
#include &lt;type_traits&gt;

template &lt;class T, T... Ints&gt;
struct integer_sequence {};

template &lt;size_t N, class T, T... Ints&gt;
struct integer_sequence_helper {
    typedef typename integer_sequence_helper&lt;N - 1, T, N - 1, Ints...&gt;::type type;
};

template &lt;class T, T... Ints&gt;
struct integer_sequence_helper&lt;0, T, Ints...&gt; {
    typedef integer_sequence&lt;T, Ints...&gt; type;
};

template &lt;size_t N, class T&gt;
using make_integer_sequence = typename integer_sequence_helper&lt;N, T&gt;::type;

template &lt;class F, class Tuple, class T, T... I&gt;
constexpr decltype(auto)
apply_impl(F&amp;&amp; f, Tuple&amp;&amp; t, integer_sequence&lt;T, I...&gt;)
{
    return f(std::get&lt;I&gt;(std::forward&lt;Tuple&gt;(t))...);
}

template &lt;class F, class Tuple&gt;
constexpr decltype(auto) apply(F&amp;&amp; f, Tuple&amp;&amp; t)
{
    return apply_impl(std::forward&lt;F&gt;(f), std::forward&lt;Tuple&gt;(t),
        make_integer_sequence&lt;std::tuple_size_v&lt;std::remove_reference_t&lt;Tuple&gt;&gt;, size_t&gt;{});
}

int main()
{
    auto func = [](int x, int y, int z) {
        std::cout &lt;&lt; x &lt;&lt; &quot;, &quot; &lt;&lt; y &lt;&lt; &quot;, &quot; &lt;&lt; z &lt;&lt; std::endl;
    };

    std::tuple&lt;int, int, int&gt; t{ 1,2,3 };

    apply(func, t);

    return 0;
}</div>2023-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2ibrq71Y5Ww3KDRibDxF1gt9YDEPuZkv4ITHEP1u4vvjpPDukkLoK4ngQy1hKKzccnsicLkUAda7sPpibR6Kyb0cfQ/132" width="30px"><span>chang</span> 👍（1） 💬（1）<div>反复看着教程才把make_integer_sequence写出来（应该是半抄半写）。感觉这节已经把模板用得很偏了。个人认为若在现实项目中，最后一个bit_count的例子还是不要用模板好，为了节省运行时时间，却大大降低了代码的可读性及可维护性，不值当。</div>2021-06-09</li><br/><li><img src="" width="30px"><span>Geek_a16bbc</span> 👍（1） 💬（1）<div>template &lt;class T, T... Ints&gt;
struct integer_sequence {};
為什麼需要class T?不能template&lt;T... Ints&gt;?

template &lt;size_t... Ints&gt;
using index_sequence =  integer_sequence&lt;size_t, Ints...&gt;;
同樣的，這裡可以寫成integer_sequence&lt;Ints...&gt;?</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/40/f10493ef.jpg" width="30px"><span>中山浪子</span> 👍（1） 💬（1）<div>写过一些模版，公司代码也涉及到模版，看了老师的模版代码以后，才发现自己还是不懂模版</div>2020-07-10</li><br/><li><img src="" width="30px"><span>宋强</span> 👍（1） 💬（1）<div>
template &lt;typename F&gt;
auto compose(F f)
{
  return [f](auto&amp;&amp;... x) {
    return f(
      forward&lt;decltype(x)&gt;(x)...);
  };
}
老师，请问下auto&amp;&amp;... x没有出现在入参里，这个怎么产生呢？</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（1） 💬（1）<div>template &lt;typename F&gt;
auto compose(F f)
{
    return [f](auto&amp;&amp;... x) {
        return f(x...);
    };
}

貌似用compiler(gcc version 4.8.5 20150623) 就会遇到下面编译错误
&#47;&#47; In function ‘auto compose(F)’: 
&#47;&#47; error: expansion pattern ‘auto&amp;&amp;’ contains no argument packs
&#47;&#47; return [f](auto&amp;&amp;... x) {

用compiler(gcc version 8.3.1 20190311)就不会有问题。

如果公司目前只允许用(gcc version 4.8.5 20150623)，请问有什么workaround?

谢谢！
</div>2020-01-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtVXiaJbfkpeXH4udkPUIlFte7z3HWMebdogk8jFpgFEkJ0ruGiawUMUcZj9RLpLkIWxV7QOzbHoSg/132" width="30px"><span>小一日一</span> 👍（0） 💬（1）<div>2：auto bit_count = bit_count_t&lt;0, 1, 2, 3, 4, 5, 6, 7&gt;{};
手动包参数展开</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ea/44/cf0b2541.jpg" width="30px"><span>Marc Chan</span> 👍（0） 💬（1）<div>吴老师，因为我的工作年限比较短，刚满一年。看到第18讲，觉得这么复杂的模板，好像在工作中也没碰到过，就感觉有点离自己太远了的感觉。虽说慢慢看也能够看懂，但是就是会感觉到看完以后也没地方用。
请教一下这些内容往往会在什么地方用的多呢？或者说有没有一些更加适合初级C++ er 看的内容推荐呢？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/d4/1e0bb504.jpg" width="30px"><span>Peter</span> 👍（0） 💬（1）<div>怎么证明确实已经在编译期间已经计算过了呢？看反汇编吗？</div>2021-11-30</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>auto bit_count = get_bit_count(make_index_sequence&lt;256&gt;());
&lt;256&gt;后面是不是多了一对圆括号()？
make_index_sequence&lt;256&gt;展开之后，代入get_bit_count(index_sequence&lt;V...&gt;)模板，并没有一对圆括号()啊？</div>2021-10-18</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>为什么一会儿是大写的Tuple，一会儿又是小写的tuple，C++库里的模板不是小写tuple吗？</div>2021-10-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2ibrq71Y5Ww3KDRibDxF1gt9YDEPuZkv4ITHEP1u4vvjpPDukkLoK4ngQy1hKKzccnsicLkUAda7sPpibR6Kyb0cfQ/132" width="30px"><span>chang</span> 👍（0） 💬（1）<div>吴老师，请问怎么查看某些代码是否在编译时计算的？比如以下代码（剽窃了Geek_845be1同学的），怎么确定get_bit_count&lt;8&gt;()是否在编译时计算的？

#include &lt;array&gt;
#include &lt;iostream&gt;

using namespace std;

constexpr std::size_t count_bits(std::size_t val) {
  if (!val) {
    return 0;
  }
  return 1 + count_bits(val &amp; (val - 1));
}

template &lt;std::size_t N&gt; constexpr std::array&lt;std::size_t, N&gt; get_bit_count() {
  std::array&lt;std::size_t, N&gt; counts{};
  for (std::size_t i = 0; i &lt; N; ++i) {
    counts[i] = count_bits(i);
  }
  return counts;
}

int main() {
  auto counts = get_bit_count&lt;8&gt;();
  for (auto n : counts) {
    cout &lt;&lt; n &lt;&lt; &quot; &quot;;
  }
  cout &lt;&lt; endl;
}</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（0） 💬（3）<div>老师，我写了一个能在编译器计算出N以内的素数列表的代码，但在编译时提示“C1202 递归类型或函数依赖项上下文太复杂” (N=1000) ， 尝试过N=100时是可以编译成功的。 不知道有没有可以让N=1000也通过的办法（比如让编译器能递归更深的层）？</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/06/8c/6b1f88ec.jpg" width="30px"><span>某某某</span> 👍（0） 💬（1）<div>Tuple一下让我回到了vc6下写typelist的时代。但是现在的新代码反倒是看不太懂了，bit_count_t里面最后调用count_bits后的...是如何展开的。</div>2021-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/27/3d/48340c0b.jpg" width="30px"><span>闲着也是贤者</span> 👍（0） 💬（1）<div>老师， auto squared_sum = compose(sum_list, square_list);将这两个实参的位置替换后就不能工作呢，这是为什么呢？应该能正常工作，但是却出错了？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9a/ee/f996f864.jpg" width="30px"><span>吃鱼</span> 👍（0） 💬（1）<div>只能大概看懂，最后的例子想尝试编译一下，结果 auto bit_count = get_bit_count(make_index_sequence&lt;256&gt;()); 这一句报错了 匹配不到模板，读到这么晚好伤心。。。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/60/8ea658a9.jpg" width="30px"><span>西加加</span> 👍（0） 💬（1）<div>当时学习模板的时候，试着写了一个玩耍性质的定义并初始化 array 为0...N， 正好和第三问的思路应该是一致的，也是一种展开 0...N 的写法吧。
template &lt;typename T&gt;
struct DefineArray&lt;T, true&gt; {
    static constexpr auto m_res_arr = DefineArray&lt;typename T::next_type, T::cond_val&gt;::m_res_arr;
};

template &lt;typename T&gt;
struct DefineArray&lt;T, false&gt; {
    static constexpr auto m_res_arr = T::m_expand_arr;
};

template &lt;typename T, T N, T... ELES&gt;
struct ExpandArray {
    static constexpr array&lt;T, sizeof...(ELES)+1&gt; m_expand_arr = {N, ELES...};
    static constexpr bool cond_val = (N-1 != 0);
    using next_type = ExpandArray&lt;T, N-1, N, ELES...&gt;;
};

主要利用递归，不停的在前面加数就好了。
</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c9/e3/28c16afa.jpg" width="30px"><span>三味</span> 👍（0） 💬（1）<div>17和18讲可以说，真是劝退不少非c++读者吧。。。
个人认为，如果不是需要写库，这两节的内容应该用得也不多吧。
作为一名图形工作者，我看这些东西，其实是因为好多图形库（说的就是你，CGAL）都是模板代码，看得眼疼。。。
实用更优先。当然，理解这些这几讲的内容还是很有帮助的。
顺便说一句，留言区贴代码实在是太费劲了。。。极客时间不好好搞搞Markdown回复格式么？好多问题还要贴代码的，有的就是挺长的。。
试着回答一下问题：
1. compose不带任何参数，
template&lt;class... Args&gt;
auto compose() {
	return [](auto&amp;&amp;... args) { return compose&lt;Args...&gt;(); };
}
关于不带参数的意义，我理解的是，没有参数，那么就没有要执行的操作，那么就什么都不执行，返回个空。再深挖掘我就想不到了。。。这里我是为了形式上的统一，返回了一个依然什么都不做的自身。

2. 想不到其他方法。。要再预编译阶段就展开256个数值。。我还是等等答案吧。。

3. 自己实现是不可能的。这辈子都不可能。之前我看别人的代码，有通过借助写了一个辅助的PushBack操作来实现。这个自然不是我原创，拿来主义：
template &lt;class T, T... Ints&gt;
struct integer_sequence {};

template &lt;size_t... Ints&gt;
using index_sequence = integer_sequence&lt;size_t, Ints...&gt;;

template &lt;size_t, typename T&gt;
struct push_back{};

template &lt;size_t N, size_t... Ints&gt;
struct push_back&lt;N, index_sequence&lt;Ints...&gt;&gt; {
	using type = index_sequence&lt;Ints..., N&gt;;
};

template &lt;size_t N&gt;
struct index_sequence_helper {
	using type = typename push_back&lt;N-1, typename index_sequence_helper&lt;N-1&gt;::type&gt;::type;
};

template &lt;&gt;
struct index_sequence_helper&lt;1&gt; {
	using type = index_sequence&lt;0&gt;;
};

template &lt;size_t N&gt;
using make_index_sequence = typename index_sequence_helper&lt;N&gt;::type;</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（0） 💬（1）<div>1、看了老师的nvwa：
inline auto compose()
{
    return [](auto&amp;&amp; x) -&gt; decltype(auto)
    {
        return std::forward&lt;decltype(x)&gt;(x);
    };
}

感觉还是为了使用方便，真的需要还可以这样：compose(std::identity{})

第3题在网上查了些资料，发现很复杂。

本节的思考题都好难，求老师解答。</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（1）<div>#1
template &lt;typename F,
          typename... Args&gt;
auto compose(F f, Args... args)
{
  return [f, args...]() {
    return f(
      compose(args...)());
  };
}


template &lt;typename F&gt;
auto compose(F f)
{
    return f；
}

如果这些函数都在函数体内操作一个公用的数据，而且这些函数依次执行的顺序反应了一定的工程需求，那么就是有意义的吧。</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（0）<div>回过头来看这一课，才发现在make_index_sequence的例子中，最终的目标竟然是实例化后的模板的非类型实参而不是实例化后的模板对象本身。然后把这些非类型实参包用get&lt;&gt;模板展开。

仔细想想，这当然是可以的，因为可变参数模板处理的就是参数包啊，而参数包可以是非类型相关的</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/01/95/fd09e8a8.jpg" width="30px"><span>布拉姆</span> 👍（0） 💬（0）<div>template&lt;class F, class Tuple, size_t ...I&gt;
inline constexpr decltype(auto) apply_impl(F &amp;&amp; f, Tuple &amp;&amp; t, index_sequence&lt;I...&gt;)
{
  return f( get&lt;I&gt;(forward&lt;Tuple&gt;(t)) ... );
}
这里对于index_sequence&lt;I...&gt;里面 I 有多少项目, 就展开多少项. 假如tuple一共2项, 则展开为:
return f(std::get&lt;0UL&gt;(std::forward&lt;std::pair&lt;int, int&gt; &gt;(t)), std::get&lt;1UL&gt;(std::forward&lt;std::pair&lt;int, int&gt; &gt;(t)));


和下面原理一样:
template &lt;typename T, typename... Args&gt;
inline unique_ptr&lt;T&gt; make_unique(Args&amp;&amp;... args)
{
  return unique_ptr&lt;T&gt;(new T(forward&lt;Args&gt;(args)...));
}
forward&lt;Args&gt;(args)... 会在编译时实际逐项展开 Args 和 args ，参数有多少项，展开后就是多少项。</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a2/54/49dfb810.jpg" width="30px"><span>宵练2233</span> 👍（0） 💬（0）<div>贴一个也用到sequence的std::string enum编译期互转的例子
https:&#47;&#47;tao-fu.gitee.io&#47;2020&#47;11&#47;09&#47;C++%E6%9D%82%E8%B0%88&#47;EnumStringConversion&#47;</div>2021-06-28</li><br/>
</ul>