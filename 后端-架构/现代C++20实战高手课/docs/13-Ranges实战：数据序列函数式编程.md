你好，我是卢誉声。

通过前面的学习，我们已经了解到，C++ Ranges作为基础编程工具，可以大幅加强函数式编程的代码可读性和可维护性，解决了C++传统函数式编程的困境。在C++20的加持下，我们终于可以优雅地处理大规模数据了。

在讲解完Ranges的概念和用法后，我们还是有必要通过实战来融会贯通C++ Ranges。它的用法比较灵活，在熟练使用后，我相信你会在今后的代码实现中对它爱不释手。

在处理规模型数据时，函数式编程特别有用。为了让你建立更直观的感受，今天我为你准备了一个实战案例，设计一个简单的统计分析程序，用来分析三维视图中的对象。

好，话不多说，让我们从工程的基本介绍开始吧（课程完整代码，你可以从[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

## 模块设计

在这个实战案例里，我们主要是展示Ranges的强大功能，而非数据本身的严谨性和正确性。因此，你可以重点关注处理数据的部分。

那么，**要分析统计的数据长什么样子呢？**我们假设一个三维模型包含多个视图，每个视图包含一定量的三维对象。某个三维对象中的三角面片就组成了逻辑上的三维对象。同时，三维模型会将视图分成高精度视图和低精度视图。

我造了一份简单的数据，一个三维模型的统计分析表是后面这样。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>按照老师上次留言给出的指导意见，已修改代码，这里给出关键代码：
协程类修改成下面的代码，注意 final_suspend 的返回值需要修改成suspend_always，否则在我的这个使用场景中，协程退出时会抛异常：
export struct Coroutine {
    struct promise_type {
        std::string _value;
        
        Coroutine get_return_object() {
            return {
                ._handle = std::coroutine_handle&lt;promise_type&gt;::from_promise(*this)
            };
        }

        std::suspend_never initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        std::suspend_always yield_value(std::string value) {
            _value = RemoveNumber(value);
            return {};
        }

        void return_void() {}
        void unhandled_exception() {}
    };

    std::coroutine_handle&lt;promise_type&gt; _handle;
};

字符串的处理：
export string RemoveNumber(string&amp; input)
{
    return input | views::filter([](char ch) {
        return !isdigit(ch);
        }) | to&lt;string&gt;();
}

main.cpp中的调用：
Coroutine asyncStr()
{
    string input;
    while (getline(cin, input))
    {
        if (input == &quot;End&quot;)
        {
            break;
        }
        co_yield input;
    }
}


int main()
{
    auto h = asyncStr()._handle;
    auto&amp; promise = h.promise();
    while (!h.done())
    {
        cout &lt;&lt; &quot;处理结果：&quot; &lt;&lt; promise._value &lt;&lt; endl;
        h();
    }

    h.destroy();

    return 0;
}</div>2024-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（2）<div>分享一下我的思考题的答案，我这里只给出关键代码：
export module asyncString.stringHandle:handler;

import asyncString.utils;
import asyncString.task;
import &lt;ctype.h&gt;;
import &lt;ranges&gt;;
import &lt;algorithm&gt;;
import &lt;string&gt;;
import &lt;sstream&gt;;
import &lt;vector&gt;;
import &lt;numeric&gt;;

using std::vector;
using std::string;
using std::istringstream;

namespace asyncString::stringHandle {
    namespace views = std::ranges::views;
    namespace ranges = std::ranges;

    using asyncString::utils::views::to;
    using asyncString::task::asyncify;

    export vector&lt;string&gt; RemoveNumber(vector&lt;string&gt;&amp; vecInput)
    {
        return vecInput | views::transform(
                [](string&amp; str) {
                    istringstream iss{ str };
                    ranges::istream_view&lt;string&gt; isView{ iss };

                    auto resultStr = isView | views::transform([](string word) {
                        return word | views::filter([](char ch) {
                            return !isdigit(ch);
                            }) | to&lt;string&gt;();
                        }) | to&lt;vector&lt;string&gt;&gt;();

                    string iniStr;
                    string joinStr = std::accumulate(resultStr.begin(), resultStr.end(), iniStr, [](string prev, string&amp; val) {
                        return prev + &quot; &quot; + val;
                        });

                    return joinStr;
                }
        ) | to&lt;vector&lt;string&gt;&gt;();
    }

    export auto RemoveNumberAwaiter(vector&lt;string&gt;&amp; inputVec) {
        return asyncify([&amp;inputVec]() {
            return RemoveNumber(inputVec);
            });
    }
}
完整代码，请参阅gitee仓库：https:&#47;&#47;gitee.com&#47;devin21&#47;rangeAssignment&#47;tree&#47;master</div>2024-01-14</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（0）<div>还是更喜欢传统的方式，可以用不修改原来变量的方式去实现多线程处理</div>2023-10-19</li><br/>
</ul>