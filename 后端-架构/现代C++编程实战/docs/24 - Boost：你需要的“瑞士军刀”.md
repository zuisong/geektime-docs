你好，我是吴咏炜。

我们已经零零碎碎提到过几次 Boost 了。作为 C++ 世界里标准库之外最知名的开放源码程序库，我们值得专门用一讲来讨论一下 Boost。

## Boost 概览

Boost 的网站把 Boost 描述成为经过同行评审的、可移植的 C++ 源码库（peer-reviewed portable C++ source libraries）\[1]。换句话说，它跟很多个人开源库不一样的地方在于，它的代码是经过评审的。事实上，Boost 项目的背后有很多 C++ 专家，比如发起人之一的 Dave Abarahams 是 C++ 标准委员会的成员，也是《C++ 模板元编程》一书 \[2] 的作者。这也就使得 Boost 有了很不一样的特殊地位：它既是 C++ 标准库的灵感来源之一，也是 C++ 标准库的试验田。下面这些 C++ 标准库就源自 Boost：

- 智能指针
- thread
- regex
- random
- array
- bind
- tuple
- optional
- variant
- any
- string\_view
- filesystem
- 等等

当然，将来还会有新的库从 Boost 进入 C++ 标准，如网络库的标准化就是基于 Boost.Asio 进行的。因此，即使相关的功能没有被标准化，我们也可能可以从 Boost 里看到某个功能可能会被标准化的样子——当然，最终标准化之后的样子还是经常有所变化的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/49/29/bbeccb9f.jpg" width="30px"><span>风羽星泉</span> 👍（7） 💬（1）<div>老师的文章里提到：“实现类似（Boost.ScopeExit）的功能在 C++11 里相当容易“。能教我怎么实现吗？</div>2020-01-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/k9xeicX1iasjoNmVMTPcKIuvn0Uf8hWHraQicz8AHK8Ewb1icWUrQ0pwUp5MsyGxv5EgvjH6CpUzKvL53bkaaALqgg/132" width="30px"><span>Geek_Frank</span> 👍（1） 💬（3）<div>您好，POCO库您觉得怎么样？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（1）<div>老师，通过看某些源代码来学习现代C++，看Boost库的，是一个好的开始不？</div>2020-01-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtVXiaJbfkpeXH4udkPUIlFte7z3HWMebdogk8jFpgFEkJ0ruGiawUMUcZj9RLpLkIWxV7QOzbHoSg/132" width="30px"><span>小一日一</span> 👍（0） 💬（1）<div>使用低版本的 G++ 编译器编译老师提供的 Hana 例子，需要加 -std=c++17</div>2024-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/45/ac/3dc59a5e.jpg" width="30px"><span>Ben</span> 👍（0） 💬（1）<div>吴老师，我希望分享一个踩坑经历。在mac brew 安装之后大概率要使用pkg-config 这个命令告诉编译器 Armadillo的位置。要不然安装之后cmake 找不到。</div>2022-08-26</li><br/><li><img src="" width="30px"><span>weing</span> 👍（0） 💬（1）<div>老师，有推荐的C++ 内存池库吗？
想在C++代码里使用内存池进行内存管理</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/80/e409fff6.jpg" width="30px"><span>Sochooligan</span> 👍（0） 💬（0）<div>来了，来了。</div>2020-01-20</li><br/>
</ul>