你好，我是Chrono。

上节课我提到了计算机界的经典公式“算法 + 数据结构 = 程序”，公式里的“数据结构”就是C++里的容器，容器我们已经学过了，今天就来学习下公式里的“算法”。

虽然算法是STL（标准库前身）的三大要件之一（容器、算法、迭代器），也是C++标准库里一个非常重要的部分，但它却没有像容器那样被大众广泛接受。

从我观察到的情况来看，很多人都会在代码里普遍应用vector、set、map，但几乎从来不用任何算法，聊起算法这个话题，也是“一问三不知”，这的确是一个比较奇怪的现象。而且，很多语言对算法也不太“上心”。

但是，在C++里，算法的地位非常高，甚至有一个专门的“算法库”。早期，它是泛型编程的示范和应用，而在C++引入lambda表达式后，它又成了函数式编程的具体实践，所以，**学习掌握算法能够很好地训练你的编程思维，帮你开辟出面向对象之外的新天地**。

## 认识算法

从纯理论上来说，算法就是一系列定义明确的操作步骤，并且会在有限次运算后得到结果。

计算机科学里有很多种算法，像排序算法、查找算法、遍历算法、加密算法，等等。但是在C++里，算法的含义就要狭窄很多了。

C++里的算法，指的是**工作在容器上的一些泛型函数**，会对容器内的元素实施的各种操作。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/72/52/8e81daf1.jpg" width="30px"><span>屈肖东</span> 👍（17） 💬（2）<div>学习C++最蛋疼的地方之一，就是总要去确定哪些内容是C++11以及之后才具有的，哪些是C++11之前就有的，像我们公司，根本不支持C++11，C++11再牛逼也没用。只能在学习C++的时候刻意的去记C++11才有的功能，然后在开发时不去使用。这一点比C差太多了，C几乎完全不会考虑版本问题，因为最常用的C标准是C99和C89，现在系统自带的GCC基本不可能不支持。</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/99/27/15d2c4f5.jpg" width="30px"><span>Zivon</span> 👍（7） 💬（1）<div>for_each是不是无法返回pos，在需要得到元素位置的情况不太合适？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/63/30/6f4b925c.jpg" width="30px"><span>Luca</span> 👍（6） 💬（5）<div>回答一下第一个问题，不知是否正确：for_each循环不能完全代替for循环，比如在for循环中可以使用break跳出，而在for_each中在语法层面是没有跳出的，如果要跳出的话，可能需要借助异常机制了。
当然，应用for_each的函数式设计思想，也不应出现需要跳出循环的情况。
请老师与大家指正！</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/9c/1a750bc7.jpg" width="30px"><span>l c</span> 👍（5） 💬（1）<div>是从Java&#47;Python转的c++，之前对c++其实是抱有一些成见的，大概就是难学难写，很古板很“笨重”。但是越学越发现c++是一个非常全能的语言，有一种什么都给你了随便你干什么的感觉，而且随着协议不断在更新这些工具。
觉得c++远没有到过时的时候，依然有它的活力啊。
</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/67/057e5d93.jpg" width="30px"><span>flying</span> 👍（4） 💬（1）<div>老师，对于多层map有没有好的解决方案：
比如：
typedef std::map&lt;sd::string, std::map&lt;std::string, std::map&lt;string, Info&gt;&gt; Firm2Cus2CommInfo;
然后对这个三级map中的Info进行操作，同时还会用到第一级、第二级的key。
感觉用for_each不太好实现。
用map的原因是，方便查询，通过key就能获取到结果。
但是用for的话，就是好多层for，看着难受。

老师有没有好的解决方法呢？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（4） 💬（2）<div>用c++很多年了，确实会遇到手写类似标准库的函数，手写完之后才发现标准库有同样功能高效的函数，简直让人感觉是闭门造车，哭笑不得。
既然老师文章都提到以后尽量用for_each，我也觉得就可以替代for，以后尽量用老师教的，还有就是小技巧很实用！</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（4） 💬（1）<div>这个标题成功吸引了我。</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（3） 💬（1）<div>老师，在实践中遇到的2个问题：
1. 一个线程中，每间隔几秒调用sort，对vector中的元素进行排序。其他N个线程依据某种条件，从该vector容器中取出元素。对着这样的操作，vector容器作为公共资源需要上锁吗？也就是说sort是只读算法吗？
2. set&#47;map中的lower_bound和upper_bound成员函数，也都是二分查找法吗？它们和find成员函数的查找效率哪个更高，或者哪个更好？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/e3/b9/9a934f5c.jpg" width="30px"><span>KevinJ</span> 👍（1） 💬（1）<div>C++17 允许并行策略 但是gcc9下需要引进intel TBB。也可以使用gnu自带的并行算法库拓展 但是必须开启fopenmp。但是在gcc11下就不用了 直接开启C++20标准然后include execution就好。</div>2022-05-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（1） 💬（2）<div>1.感觉for_each不能够完全替代for循环,就像if-else,break,continue这些for_each没法用.
2.根据自己的需求选择合适的算法:
排序中:
只是找出前几名的,选择partial_sort;而如果选出第一名和最后一名采用minmax_element;对于list容器,使用成员函数sort;有序容器map,set已经排好序了,直接迭代就可.
查找中:
需要先排好序的:
二分查找binary_search只能够告知元素是否存在;真正好用的还是lower_bound和upper_bound分别是返回该值的下界位置和上界位置(后一个位置);
有序的set&#47;map,提供等价的成员函数find&#47;lower_bound&#47;upper_bound.
不需要排序的:
find,search</div>2021-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlgy0OxSZOQIqfgZLoSVMjG7OrgBVtpVEOTUtWKhG62BYccoXvUD4KcGJ8c7Lpo7QflYceBaOJSg/132" width="30px"><span>Geek_5dc295</span> 👍（1） 💬（1）<div>有时候find 如果未找到对应位置不是会返回值有时候和npos对比判断，想问一下npos和迭代器之间是什么关系呀</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1c/0e/f2954d1c.jpg" width="30px"><span>hy</span> 👍（1） 💬（1）<div>lambda表达式里面发生错误或者是出现异常外面是不是无法捕获的呀???</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/57/3a729755.jpg" width="30px"><span>灯盖</span> 👍（0） 💬（1）<div>确实对于算法用的少
</div>2024-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/df/c6/d8f9d33a.jpg" width="30px"><span>辰</span> 👍（0） 💬（1）<div>老师，sort()底层并不是纯粹的快速排序。我记得在元素少时用插入排序，元素多时可能使用堆排序或者快速排序</div>2023-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/fRVxJWw4SfXbfIHHdVzrQpV8oUqWqiatH0IlS3hf2WLaENTwBiblx36UukXyY6tSewqIMJFibz6HlCiaGGT4a6xwicQ/132" width="30px"><span>发烫的椰子</span> 👍（0） 💬（1）<div>注意 lower_bound 的查找条件是“大于等于”，而不是“等于”，所以它的真正含义是“大于等于值的第一个位置”。相应的也就有“大于等于值的最后一个位置”，算法叫 upper_bound，返回的是第一个“大于”值的元素。
您好，老师，“大于等于值的最后一个位置”和返回的是第一个“大于”值的元素 我的理解两者是不一样的。[3,3,3,3,5],比如“大于等于值的最后一个位置”是指最后一个3的位置，返回的是第一个“大于”值的元素是指5的位置，所以我怎么也想不通两者是相等的，还请老师解惑。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（0） 💬（1）<div>老师给我打开了新世界的大门，C++的算法用得还是比较少，以后工作中要多尝试用起来</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师你好，问你一个最近面试遇到的问题，希望可以解答。一个100G的URL文件，如何哈希分为1000个小文件呢？内存不超过1G。是否可以用文件映射，依次读是否效率太低了？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3d/30/9e5e5d4d.jpg" width="30px"><span>巴菲特不非</span> 👍（0） 💬（1）<div> “lower_bound 的查找条件是“大于等于”，而不是“等于”，所以它的真正含义是“大于等于值的第一个位置”。相应的也就有“大于等于值的最后一个位置”，算法叫 upper_bound，返回的是第一个“大于”值的元素。”
这里下半部分有矛盾吧，upper_bound应该是“大于值的第一个位置”。</div>2021-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（0） 💬（2）<div>“不过，我建议你使用更加通用的全局函数 begin()、end()，虽然效果是一样的，但写起来比较方便，看起来也更清楚”。从代码长度上来看，老师我感觉全局函数写的更多啊。</div>2021-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>自我感觉c++标准库普及的不够。</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/2c/06375913.jpg" width="30px"><span>宇天飞</span> 👍（0） 💬（1）<div>你觉得 for_each 算法能完全替代 for 循环吗？
1、可以
如果要计数的话，for会更方便，i++

试着自己总结归纳一下，这些排序和查找算法在实际开发中应该如何使用。
1、业务需要的数据是否有顺序要求，选用对用的数据结构
2、场景：最热门的10个影片，成绩最好，满足什么条件的用户</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/b9/af5db174.jpg" width="30px"><span>andi轩</span> 👍（0） 💬（2）<div>老师，lower_bound示例里:
found = (pos != cend(v)) &amp;&amp; (*pos == 7); &#47;&#47; 可能找不到，所以必须要判断
应该是
found = (pos != cend(v)) &amp;&amp; (*pos &gt;= 7); &#47;&#47; 可能找不到，所以必须要判断
对吧？
因为是要找第一个&gt;=7的位置，有可能没有7，找到个8也是对的</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（1）<div>1.用的比较多的是auto
2.for each range for看起来更像Python的语法糖，提高编程效率</div>2020-06-06</li><br/><li><img src="" width="30px"><span>TC128</span> 👍（0） 💬（3）<div>老师好，请问为什么有些算法可以传入数组地址，有些却不可以？比如：
  int myints[] = { 10, 20, 30, 40 };
  int * p;
  p = std::find (myints, myints+4, 30);
但for_earch就不可以。</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/a3/23540579.jpg" width="30px"><span>robonix</span> 👍（0） 💬（1）<div>老师，如果将二分查找算法应用在普通类元素上，是不是还得手写比较函数？</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/54/87/3b1f9de4.jpg" width="30px"><span>Confidant.</span> 👍（0） 💬（3）<div>向问老师一个和今天内容没有关系的问题

#include &lt;iostream&gt;
#include &lt;filesystem&gt;

using namespace std;
using namespace filesystem;

int main()
{
    string s(&quot;log&quot;);
    shared_ptr&lt;path&gt; p = make_shared&lt;path&gt;(s);
    return 0;
}

这段代码在Linux下跑的时候，析构path就会崩溃，智能指针不能管理path类吗？在log文件存在于当前运行目录下</div>2020-06-04</li><br/>
</ul>