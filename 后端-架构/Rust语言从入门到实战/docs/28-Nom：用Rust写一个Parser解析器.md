你好，我是Mike。今天我们来一起学习如何用Rust写一个Parser解析器。

说到解析器，非计算机科班出身的人会一脸懵，这是什么？而计算机科班出身的人会为之色变，曾经熬夜啃“龙书”的痛苦经历浮现眼前。解析器往往跟“编译原理”这个概念一起出现，谈解析器色变完全可以理解。

实际上，解析器也没那么难，并不是所有需要“解析”的地方都与编程语言相关。因此我们可以先把“编译原理”的负担给卸掉。在开发过程中，其实经常会碰到需要解析的东西，比如自定义配置文件，从网络上下载下来的一些数据文件、服务器日志文件等。这些其实不需要很深的背景知识。更加复杂一点的，比如网络协议的处理等等，这些也远没有达到一门编程语言的难度。

另一方面，虽然我们这门课属于入门级，但是对于未来的职业规划来说，如果你说你能写解析器，那面试官可能会很感兴趣。所以这节课我会从简单的示例入手，让你放下恐惧，迈上“解析”之路。

## 解析器是什么？

解析器其实很简单，就是把一个字符串或字节串解析成某种类型。对应的，在Rust语言里就是把一个字段串解析成一个Rust类型。一个Parser其实就是一个Rust函数。

这个转换过程有很多种方法。

1. 最原始的是完全手撸，一个字符一个字符吞入解析。
2. 对一些简单情况，直接使用String类型中的find、split、replace等函数就可以。
3. 用正则表达式能够解析大部分种类的文本。
4. 还可以用一些工具或库帮助解析，比如Lex、Yacc、LalrPop、Nom、Pest等。
5. Rust语言的宏也能用来设计DSL，能实现对DSL文本的解析。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/36/92d8eb91.jpg" width="30px"><span>Promise</span> 👍（1） 💬（1）<div>老师，请问解析器如何优化性能，比如解析器每天需要处理 PB 级别的文本。每个文件 100M并且需要匹配上百种规则。</div>2023-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（2）<div>思考题
```
use nom::{
    bytes::complete::is_not,
    character::complete::{char, line_ending},
    combinator::opt,
    multi::separated_list0,
    sequence::terminated,
    IResult,
};
use std::{fs, io::Error};

fn read_file(file_path: &amp;str) -&gt; Result&lt;String, Error&gt; {
    fs::read_to_string(file_path)
}

&#47;&#47; parse_csv =&gt; parser
fn parse_csv(input: &amp;str) -&gt; IResult&lt;&amp;str, Vec&lt;Vec&lt;&amp;str&gt;&gt;&gt; {
    println!(&quot;input csv file:&quot;);
    println!(&quot;{}&quot;, input);
    &#47;&#47; terminated =&gt; combinator
    &#47;&#47; line_ending =&gt; parser
    &#47;&#47; opt =&gt; combinator
    separated_list0(terminated(line_ending, opt(line_ending)), parse_line)(input)
}

&#47;&#47; parse_line =&gt; parser
fn parse_line(input: &amp;str) -&gt; IResult&lt;&amp;str, Vec&lt;&amp;str&gt;&gt; {
    &#47;&#47; separated_list0 =&gt; a combinator
    &#47;&#47; accepts 2 parser
    separated_list0(char(&#39;,&#39;), is_not(&quot;,\r\n&quot;))(input)
}

fn main() -&gt; Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt; {
    let file_content = read_file(&quot;&#47;path&#47;to&#47;my&#47;file.csv&quot;)?;
    match parse_csv(&amp;file_content) {
        Ok((_, rows)) =&gt; {
            for row in rows {
                println!(&quot;{:?}&quot;, row);
            }
        }
        Err(e) =&gt; println!(&quot;Failed to parse CSV: {:?}&quot;, e),
    }
    Ok(())
}
```
</div>2024-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epvZCxlwoJpxVgG4zCsCpsmqfqxHic82ukC3LOloI5OG7IgVEmNos7gnSYnN9LCjxRCicQxyjVhlx6w/132" width="30px"><span>tianyu0901</span> 👍（0） 💬（2）<div>老师，推荐一个SQL解析器</div>2023-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL8AP4vaWEiaZYQIBmn9n9eXJh8dkzluxMjMyMl1CbOcRzianpVXu5bWkCPJyj2sTfxHhpYOMOVTEjA/132" width="30px"><span>Geek_f9c361</span> 👍（0） 💬（0）<div>解析一个坐标这个写的不够健壮，逗号前后应该可以有任意空白，这里没有处理</div>2024-08-30</li><br/>
</ul>