你好，我是吴咏炜。

我们已经讲过了容器。在使用容器的过程中，你也应该对迭代器（iterator）或多或少有了些了解。今天，我们就来系统地讲一下迭代器。

## 什么是迭代器？

迭代器是一个很通用的概念，并不是一个特定的类型。它实际上是一组对类型的要求（\[1]）。它的最基本要求就是从一个端点出发，下一步、下一步地到达另一个端点。按照一般的中文习惯，也许“遍历”是比“迭代”更好的用词。我们可以遍历一个字符串的字符，遍历一个文件的内容，遍历目录里的所有文件，等等。这些都可以用迭代器来表达。

我在用 output\_container.h 输出容器内容的时候，实际上就对容器的 `begin` 和 `end` 成员函数返回的对象类型提出了要求。假设前者返回的类型是 I，后者返回的类型是 S，这些要求是：

- I 对象支持 `*` 操作，解引用取得容器内的某个对象。
- I 对象支持 `++`，指向下一个对象。
- I 对象可以和 I 或 S 对象进行相等比较，判断是否遍历到了特定位置（在 S 的情况下是是否结束了遍历）。

注意在 C++17 之前，`begin` 和 `end` 返回的类型 I 和 S 必须是相同的。从 C++17 开始，I 和 S 可以是不同的类型。这带来了更大的灵活性和更多的优化可能性。

上面的类型 I，多多少少就是一个满足输入迭代器（input iterator）的类型了。不过，output\_container.h 只使用了前置 `++`，但输入迭代器要求前置和后置 `++` 都得到支持。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtVXiaJbfkpeXH4udkPUIlFte7z3HWMebdogk8jFpgFEkJ0ruGiawUMUcZj9RLpLkIWxV7QOzbHoSg/132" width="30px"><span>小一日一</span> 👍（31） 💬（4）<div>看了老师的代码再看自己学的代码，感觉我的C++是小学生水平。

以为自己看过几遍C++ PRIMER 5th, 看过并理解effective++, more effective c++, inside the c++ object model, 能应付平时的开发需要，也能看懂公司别人的代码，就觉得自己的C++不错了，看了老师github的代码后我是彻底服了，感叹C++太博大精深，永远不敢说自己精通C++。

我什么时候才能达到老师对C++理解并使用的高度呢，难道也需要20年么？</div>2019-12-11</li><br/><li><img src="" width="30px"><span>Geek_b68b74</span> 👍（10） 💬（3）<div>1、使用输入行迭代器  这一部分里，“ auto&amp;&amp; r = istream_line_reader(is);”  这里为什么要用右值引用呢？
2、还是使用输入行迭代器这里， 

for (const string&amp; line :
     istream_line_reader(is)) {
  &#47;&#47;  示例循环体中仅进行简单输出
  cout &lt;&lt; line &lt;&lt; endl;
}
“获取冒号后边的范围表达式的结果，并隐式产生一个引用，在整个循环期间都有效。注意根据生命期延长规则，表达式结果如果是临时对象的话，这个对象要在循环结束后才被销毁。”  
 第一句是说line在整个循环期间有效？这是想表达什么呢？还有第二句，指的是哪个临时对象呢？在哪个循环结束后销毁呢？期待您的解答
</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/1a/d1d44258.jpg" width="30px"><span>千鲤湖</span> 👍（10） 💬（1）<div>过来看看老师问的那两个问题，好奇中。。。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（6） 💬（1）<div>输入迭代器和输出迭代器，
这个入和出是相对于什么而言的？
感觉有点绕。

谢谢！</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/7c/12c571b6.jpg" width="30px"><span>Slience-0°C</span> 👍（4） 💬（6）<div>有个问题请教老师，工作中看到基于范围的for循环中，使用了auto &amp;&amp;来获取数据，而不是auto&amp;,有啥区别么？难道是为了使用移动构造函数？伪代码如下：std::vectors&lt;std::string&gt; vec;
for (auto&amp;&amp; : vec)</div>2022-04-21</li><br/><li><img src="" width="30px"><span>nelson</span> 👍（3） 💬（2）<div>如果stream_是nullptr会怎么样？</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（2） 💬（1）<div>课后思考
1.目前这个输入迭代器的行为，在干什么情况下可能导致意料之外的后果？
答：目前这个输入迭代器在构造里调用了++，所以，多一次构造就可能读到意料之外的结果了。

2.请尝试一下改进这个输入行迭代器，看看能不能消除这种意外，如果可以，该怎么做？如果不可以，为什么？
答：可以啊，文章里提到了，这个输入行迭代器构造的使用了++，是为了与日常使用一致，如果想改进这个一块，我们也可以改构造的时候</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/de/6d/c0d049f2.jpg" width="30px"><span>旭东</span> 👍（2） 💬（1）<div>老师，您好，iterater中后置++的实现是不是应该返回const；避免（i++)++这样的代码通过编译？</div>2019-12-14</li><br/><li><img src="" width="30px"><span>晚风·和煦</span> 👍（2） 💬（1）<div>从 C++17 开始，I 和 S 可以是不同的类型。这带来了更大的灵活性和更多的优化可能性。   没太理解这句话😂</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/a3/0e56b4e5.jpg" width="30px"><span>doge</span> 👍（1） 💬（1）<div>第二个问题想了半天，好像做不到，根据begin的语义，拿到stream_对象后就必须取得第一行内容，否则返回的就是一个空string而不是文件的第一行。但是在iterator对象内好像没办法记录“第一次从strem_读”这样的一个状态。我尝试标记第一次，但是会忽视读的操作，这样还是会导致第一行内容的丢失。希望老师解惑。
    explicit iterator(istream&amp; is) : stream_(&amp;is) {}
    iterator begin() {
        cout &lt;&lt; &quot;first_ = &quot; &lt;&lt; first_ &lt;&lt; endl;
        if (first_) {
            first_ = false;
            return ++iterator(*stream_);
        } else {
            return iterator(*stream_);
        }
    }</div>2021-02-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep2gRIticwS6CiatsCiaU4QRjAODKibQevrhSciatrmd90lNIZFxywE9yyZgAxKTmWiaBSH4zZUcRIV46qQ/132" width="30px"><span>englefly</span> 👍（1） 💬（1）<div>&quot;从 C++17 开始，I 和 S 可以是不同的类型&quot; 意味着 &quot; r.begin() 和 r.end() 可以是不同类型了。&quot;
那么常见的循环遍历是不是就有问题了?比如下代码, it = r.begin() 此时 it是r.begin() 的类型,但it还要和r.end()比较,这时就是两个不同类型在比较了

auto it = r.begin(); 
auto end = r.end(); 
for (; it != end; ++it) {...}</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/3c/63bb1a53.jpg" width="30px"><span>公众号【xii说孔方兄】</span> 👍（1） 💬（1）<div>吴老师，您好，我对您的自建博客很感兴趣，https:&#47;&#47;yongweiwu.wordpress.com&#47;  ，看域名使用WordPress搭建的，想向您将请教这方面的问题。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/a3/23540579.jpg" width="30px"><span>robonix</span> 👍（1） 💬（1）<div>老师，iterator begin()函数返回一个iterator对象，这个对象还包含了string成员，这样就得拷贝了吧，效率会不会不高呢</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/96/c679bb3d.jpg" width="30px"><span>总统老唐</span> 👍（1） 💬（1）<div>吴老师，这一课有两个疑问：
1，“到底应该让 * 负责读取还是 ++ 负责读取”，该怎样理解？如果“读取”指的是在istream上读取一行，放入line_成员中，用++实现这个操作是最常见和直觉的，同时，用 * 返回读取的内容也在最容易想到的方式，反过来，什么情况下会需要”用*来负责读取“？
2，输入迭代器为什么要定义 iterator operator++(int) </div>2019-12-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKEyibia4u3kq3bia4ZiaARfvj7fRqyAN9DIqaQytdy5IsPsfpl9UCdgiaF88tTyia5w1dBynyzkatDt2A/132" width="30px"><span>我不生产bug，我只是bug的搬运工</span> 👍（1） 💬（1）<div>遍历一遍后，第二次调用begin会崩溃，stream_指针已经为空</div>2019-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibb1HJTBX85TuIYRQv3eUxib5Zdc5paH1mULBaLFZf0N6C1WxLrw6ZUc4oiaEPQEdfrQMkIjIYtTib66l8VfgrtHRQ/132" width="30px"><span>Geek_71d4ac</span> 👍（1） 💬（1）<div>在构造函数中使用this是否安全？万一构造中途失败了呢？</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/ce/ec3b8de9.jpg" width="30px"><span>淡漠落寞</span> 👍（0） 💬（2）<div>老师，请问下为什么iterator类构造函数参数不是用istream*而是要用istream&amp;？</div>2024-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/62/269aae3f.jpg" width="30px"><span>水月</span> 👍（0） 💬（1）<div>看了老师关于Python yield的那篇博客，体会非常深刻。一些小算法虽然用python确实慢，但是函数式编程配上yield+yield from能给代码简化到非常不人道的水平。非常期待C++也能把这些程序员友好型设计尽快收进来</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（0） 💬（1）<div>对于问题2，既然输入迭代器不禁止调用begin多次，那是否可以在每次调用begin时，重置输入流的位置到开头？不也正好符合begin的语义？</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/00/2007d2f3.jpg" width="30px"><span>zhengfan</span> 👍（0） 💬（3）<div>吴老师您好。
我对于对于后置++的实现有些疑问。
如果通过后置++获得了Itr并解引用，string内容其实已经是经过++的了吧？</div>2020-07-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dQQR8nfd3k8zO9Z7TjOxSneFmiarGct9o6JORPrzMyyic8ZnPB97SuvYp544UKCQ24dj2LOvsbUQE3zb1uAGWG7Q/132" width="30px"><span>The Answer........</span> 👍（0） 💬（1）<div>iterator begin()  {    return iterator(*stream_);  }  
iterator end() const noexcept  {    return iterator();  }

吴老师我这里对istream_line_reader类中的成员函数begin()和end()有一个疑问.
为什么begin()没有加const标注成一个accessor, 而end()函数加了一个const标注成了accessor.
begin()函数构建了一个以*istream为参数的iterator, 不是也没有改变istream_line_reader私有成员istream_指针的state吗. 有变化的只是istream_指针指向的输入流对象. 但是指针的状态并没有发生改变. 这不是还是符合accessor的定义吗.</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/12/15558f28.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>针对第二个问题，我回头想这是一个输入迭代器，不需要满足多次访问，所以两次begin不是它的职责范围吧，使用新标准的for循环就不会出现意外结果。老师是这样吗？想了一晚上，哈哈</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/1a/d1d44258.jpg" width="30px"><span>千鲤湖</span> 👍（0） 💬（1）<div>１．可能是operator==中，比较时没有获取当前文件流位置，这样的话，无法比较不同istream(同一个文件)创建的iterator?　

2  采用ftell获取当前文件流位置</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（1）<div>#1 目前这个输入行迭代器的行为，在什么情况下可能导致意料之外的后果？
    auto x  = istream_line_reader();
    auto xit = x.begin(); 
   这个函数会调用istream_line_reader:: iterator::operator++() {
   getline(*nullptr, _M_line); &lt;----  死翘翘 }
但是用户觉得，我只是调用了x.begin, 不至于死的这么突然吧：（

#2 请尝试一下改进这个输入行迭代器，看看能不能消除这种意外。如果可以，该怎么做？如果不可以，为什么？
看了您的git代码, 看到了对nullptr的识别和抛出异常的处理，这是个解决方案。或者我们可以istream_line_reader() = delete? 没想到我们需要构造函数istream_line_reader() 的场景。</div>2019-12-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BDK5t6TTCibvGI2GiccmrkROwHE7BKHOVd5O9wpmuB7AR0Ecao6ECsZTkDHWYSExJD7S72UBO4RuWibNp270IpF7w/132" width="30px"><span>MT</span> 👍（0） 💬（1）<div>老师，这次是上次关于那个例子的补充：
1. 在进行迭代的时候，begin()和end()方法，即你所说的，编译器会自动生成指向数组头尾的指针
2. 在end()方法内返回了struct null_sentinel{} 的一个对象，即 I 和 S 的类型不同
3.通过使用 struct null_sentinel{}；所提供的operator!=() 从而达到对字符串遍历的截至
如有不对，请老师指出
之后我尝试过，在 c_string_view{} 中的 end 方法，返回一个它本身的对象，并为NULL，同时重载它的 ！= 运算符，但是失败了。
我想问下，这便算是属于一种更多的优化可能性吗？在之后，若需要只需要修改struct null_sentinel{}；即可？</div>2019-12-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（0） 💬（1）<div>iterator operator++(int)    {      iterator temp(*this);      ++*this;      return temp;    }

这个拷贝构造，是否会出问题？ 如果失败，this继续读取下一行，但temp是异常的。</div>2019-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BDK5t6TTCibvGI2GiccmrkROwHE7BKHOVd5O9wpmuB7AR0Ecao6ECsZTkDHWYSExJD7S72UBO4RuWibNp270IpF7w/132" width="30px"><span>MT</span> 👍（0） 💬（1）<div>老师，可以讲以下为什么可以将I 和 S 设置成不同的类型吗？具体使用在那些方面?</div>2019-12-12</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（0） 💬（1）<div>我的理解是istream_line_reader的iterator在到达end时，再++会直接crash，这个和STL里面主流容器的行为是不一致的。
可以在get_line之前，判断一下stream_是否为nullptr，不是才调用，对end的iterator反复进行++都一直返回自己本身。</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>意料之外的后果，是不是主要就是资源发生了不可控或不可知的泄露或状态改变？

这里的资源我觉得一是string对象，一个是istream对象，那么在这两个对象的内存管理上会引起问题？

比如构造函数中传入的istream指针没有被管理起来，它指向的对象如果被析构就会发生异常？</div>2019-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtVXiaJbfkpeXH4udkPUIlFte7z3HWMebdogk8jFpgFEkJ0ruGiawUMUcZj9RLpLkIWxV7QOzbHoSg/132" width="30px"><span>小一日一</span> 👍（0） 💬（1）<div>1. 我能想到的一点是，istream_line_reader在构造时没有对输入流的状态做检测，如果在输入流处于错误状态时调用getline()，会抛 ios_base::failure异常。
2. 我把带输入流检查的构造贴一下：
    istream_line_reader() noexcept : stream_(nullptr) {}                                                                                   
    explicit istream_line_reader( istream&amp; is) noexcept {                                                                                  
        if (is.good()) stream_ = &amp;is;                                                                                                      
        else stream_ = nullptr;                                                                                                            
    }</div>2019-12-11</li><br/>
</ul>