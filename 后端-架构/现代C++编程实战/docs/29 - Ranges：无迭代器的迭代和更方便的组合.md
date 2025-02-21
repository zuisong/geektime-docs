你好，我是吴咏炜。

今天，我们继续上一讲开始的话题，讨论 ranges（范围）。

## Ranges 简介

像下面这样的代码：

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>

int main()
{
  using namespace std;
  int a[] = {1, 7, 3, 6,
             5, 2, 4, 8};
  copy(begin(a), end(a),
       ostream_iterator<int>(
         std::cout, " "));
  std::cout << std::endl;
  sort(begin(a), end(a));
  copy(begin(a), end(a),
       ostream_iterator<int>(
         std::cout, " "));
  std::cout << std::endl;
}
```

你应该已经见到过好多次了。有没有觉得这个代码有点重复、有点无聊呢？尤其是里面的 `begin` 和 `end`？

很多人都留意到了迭代器虽然灵活，但不是一个足够高级的抽象——尤其是我们已经对 C 数组都可以进行基于“范围”的循环之后。如果我们把数组看作一个抽象的“范围”，我们就可以得到下面的代码：

```cpp
#include <experimental/ranges/algorithm>
#include <experimental/ranges/iterator>
#include <iostream>

int main()
{
  using namespace std::
    experimental::ranges;
  int a[] = {1, 7, 3, 6,
             5, 2, 4, 8};
  copy(a, ostream_iterator<int>(
            std::cout, " "));
  std::cout << std::endl;
  sort(a);
  copy(a, ostream_iterator<int>(
            std::cout, " "));
  std::cout << std::endl;
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（5） 💬（1）<div>老师能讲一讲关于c++内存安全相关的编码规范和技巧吗，我觉得这个或许才是很多同学的刚需</div>2020-02-07</li><br/><li><img src="" width="30px"><span>Geek_a16bbc</span> 👍（3） 💬（1）<div>template 
bool operator!=(I i, null_sentinel)
{ return *i != 0;}

可以請老師說明一下null_sentinel在這邊的作用嗎？function body並沒有用到null_sentinel, null sentinel只出現在input parameter上。</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c9/e3/28c16afa.jpg" width="30px"><span>三味</span> 👍（3） 💬（1）<div>emmmmmmm... 
最后提到的这篇文章，我之前看到过，印象最深刻的一句话就是，没有C++博士学位还想写C++？
最近的未来篇三篇我基本上都是走马观花的在看。。对我个人来说，感觉收益和学习成本比值有点小，根据以往经验，C++20要想全面开花，还有好几年的路要走。。
感觉C++11也是到了C++14才算是稳定点。。至少给我的感觉，直到C++17都是在对C++11进行修补。
所以，这三讲一年后我再回来好好学习吧！本来我的主业是图形</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/80/e409fff6.jpg" width="30px"><span>Sochooligan</span> 👍（2） 💬（1）<div>一、看得云里雾里地，好的方面是所有例子都运行了。
二、发现两处分心的地方：
（1）我们可以在输出 r 之前插入下面这行： 
我们可以在输出 r 之前（15行之后，16行之前）插入下面这行：
（2）除了 view，vector 满足所有的 range 概念。
vector 满足除view外所有的 range 概念。
三、我的环境是 macOS+vscode+gcc9.2.0_3(Target: x86_64-apple-darwin19) +gdb8.3</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/a2/6c0ffc15.jpg" width="30px"><span>皮皮侠</span> 👍（0） 💬（1）<div>我大概能理解Bjarne Stroustrup最喜欢的C++特性为何有concepts:在高度统一的抽象中去繁就简。也在网上看了些对C++20中Ranges的反对意见，但我看到很多游戏开发者倒很喜欢这些新功能，感觉大多容器都能用ranges；）听老师读的那段，真是激情澎湃，魅力四射！</div>2020-03-02</li><br/>
</ul>