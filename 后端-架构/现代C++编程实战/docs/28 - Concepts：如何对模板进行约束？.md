你好，我是吴咏炜。

从这一讲开始，我们进入了未来篇，展望一下即将在 C++20 出现的新功能。我们第一个要讨论的，是 concepts（概念）——一个难产了很多年才终于进入 C++ 的新功能。

## 一个小例子

老规矩，要讲“概念”，我们先看例子。

我们知道 C++ 里有重载，可以根据参数的类型来选择合适的函数。比如，我们可以定义 `half` 对于 `int` 和 `string` 有不同的作用：

```c++
int half(int n)
{
  return n / 2;
}

string half(string s)
{
  s.resize(s.size() / 2);
  return s;
}
```

初看，似乎重载可以解决问题，但细想，不对啊：除了 `int`，我们还有差不多的 `short`、`long` 等类型，甚至还有 `boost::multiprecision::cpp_int`；除了 `string`，我们也还有 `wstring`、`u16string`、`u32string` 等等。上面的每个函数，实际上都适用于一族类型，而不是单个类型。重载在这方面并帮不了什么忙。

也许你现在已经反应过来了，我们有 SFINAE 啊！回答部分正确。可是，你告诉我你有没有想到一种很简单的方式能让 SFINAE 对整数类型可以工作？Type traits？嗯嗯，总是可以解决的是吧，但这会不会是一条把初学者劝退的道路呢？……
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>老师，您的这段代码，OutContainer是需要2个模板参数的，但是特化的时候只提供了一个类型作为模板参数，是不是漏写了一个模板参数？我回到13讲，是不是应该加上 allocator&lt;decay_t&lt;decltype(f(*begin(inputs)))&gt;&gt;&gt;?还是编译期会帮我们自动推断第二个类型？
template &lt;
  template &lt;typename, typename&gt;
  class OutContainer = vector,
  typename F, class R&gt;
auto fmap(F&amp;&amp; f, R&amp;&amp; inputs)
  -&gt; decltype(
    begin(inputs),
    end(inputs),
    OutContainer&lt;decay_t&lt;
      decltype(f(*begin(
        inputs)))&gt;&gt;());</div>2023-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/db/f1/1015328a.jpg" width="30px"><span>Geek_QiDian</span> 👍（1） 💬（1）<div>请问老师的 output_container 的概念实现版本有吗？想研究一下</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/c4/8679ca8a.jpg" width="30px"><span>廖熊猫</span> 👍（1） 💬（1）<div>c++里的泛型约束和java或者c#中的泛型约束很像，但是复杂了好多...不像后者只能约束泛型参数实现某一接口，c++可以通过很小的约束组合成需要的约束，感觉这就是函数式里面经常提的组合的力量吧</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（0） 💬（1）<div>个人认为好处就是1. 代码量减少，2. 代码变得更加易读，和老师说的3. 出错信息变得更友善了。

我对模板编程不是很熟练，所以之前很少通过SFINAE来直接规制函数的模板参数类型，反而是通过模仿java的做法，写模板类作为接口，包装实际的类型。如果需要的约束简单这样写也不麻烦，但是无法像concepts的写法那样随意的组合各种约束，要实现这节图中那种类似树状的结构麻烦得就不是一点半点了。

至于缺点，暂时没有想到，希望老师能提示提示</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（1）<div>如果是引入概念的话
1.从当前的标准库里可以抽取更多近似概念的操作（类似于itrerator），直接调用即可。
2.在class的设计上直接标记概念相关关键字就可以检查class的设计是不是符合原则

缺点:理解起来比较困难</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（0） 💬（2）<div>vs2019  c++17
template &lt;typename, typename&gt;
    class OutContainer = vector,
这里提示错误：	C2065	“vector”: 未声明的标识符	
</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/f2/912c9f9d.jpg" width="30px"><span>始之源稳于心</span> 👍（0） 💬（2）<div>吴老师，你好，我问一个与此文章无关的，一个GDB调试的问题：
一个网络多线程服务，一个socket一个线程。有一个共享变量用boost的unordered_map，同步也用boost的unique_lock
程序在运行时基本正常，但在gdb调试时只要打印共享变量(即使里面没有数据)，就会收到SIGSEG，调试其它变量或用下面的步骤就没事
1   handle SIGPIPE nostop noprint
2   set print elements 0
3   将共享的变量的类型变为 stl的map
问题：
  这种情况产生的主要原因是什么，用了boost的 hash map吗，和屏蔽管道关系有多大？</div>2020-02-05</li><br/>
</ul>