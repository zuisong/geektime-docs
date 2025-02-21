你好，我是卢誉声。

在C++中，我们经常讨论一个看似简单的问题——**如何实现格式化字符串和格式化输出？**

这个问题核心在于字符串格式化，考虑到C++向下兼容的问题，想做出一个能让大家满意的字符串格式化标准方案，其实并不容易。在过去的标准中，C++标准委员会一直通过各种修修补补，尝试提供一些格式化的辅助方案，但始终没有一个风格一致的标准化方案。

好在C++20及其后续演进中，终于出现了满足我们要求的格式化方案。因此，在这一讲中，我们就聚焦于讲解这个新的字符串格式化方案。

好，话不多说，就让我们开始今天的内容吧(课程配套代码可以从[这里](https://github.com/samblg/cpp20-plus-indepth)获取)。

## 复杂的文本格式化方案

首先，我们要弄明白什么是“文本格式化”。

下面一个常见的HTTP服务的日志输出，我们结合这个典型例子来讲解。

```c++
www     | [2023-01-16T19:04:19] [INFO] 127.0.0.1 - "GET /api/v1/info HTTP/1.0" 200 6934 "http://127.0.0.1/index.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（0） 💬（4）<div>请教老师一个问题，下面的代码编译不过，报错信息是无法推导 std::formatter的模版参数，这是什么原因呢？
#include &lt;format&gt;
#include &lt;iostream&gt;

&#47;&#47; 非模板类
struct Box1 {
	bool bool_value;
	int int_value;
	const char* str;
};
template &lt;typename _CharT&gt;
struct std::formatter&lt;Box1, _CharT&gt; : std::formatter&lt;bool, _CharT&gt;
{	
	template &lt;typename _FormatContext&gt;
	typename _FormatContext::iterator format(const Box1&amp; v, _FormatContext&amp; format_context)
	{	
		typename _FormatContext::iterator Ite
			= std::formatter&lt;bool, _CharT&gt;::format(v.bool_value, format_context);
		
		return Ite;
	}
};
int main()
{
	Box1 box1{
		.bool_value = false,
		.int_value = 1,
		.str = &quot;box1&quot;
	};
	std::cout &lt;&lt; std::format(&quot;box1 = {}&quot;, box1);

	return 0;
}</div>2024-01-15</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>说实话，越改约难用，C++越走越偏了。。。</div>2023-10-23</li><br/>
</ul>