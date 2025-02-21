你好，我是宫文学。

上一节课，我们已经探讨了设计一个虚拟机所要考虑的那些因素，并做出了一些设计决策。那么今天这一节课，我们就来实现一个初级的虚拟机。

要实现这个初级虚拟机，具体来说，我们要完成下面三方面的工作：

首先，我们要设计一些字节码，来支持第一批语言特性，包括支持函数、变量和整型数据的运算。也就是说，我们的虚拟机要能够支持下面程序的正确运行：

```plain
//一个简单的函数，把输入的参数加10，然后返回
function foo(x:number):number{
    return x + 10;
}
//调用foo，并输出结果
println(foo(18));
```

第二，我们要做一个字节码生成程序，基于当前的AST生成正确的字节码。

第三，使用TypeScript，实现一个虚拟机的原型系统，验证相关设计概念。

话不多说，开搞，让我们先设计一下字节码吧！

## “设计”字节码

说是设计，其实我比较懒，更愿意抄袭现成的设计，比如Java的字节码设计。因为Java字节码的资料最充分，比较容易研究，不像V8等的字节码，只有很少的文档资料，探讨的人也很少。另外，学会手工生成Java字节码还有潜在的实用价值，比如你可以把自己的语言编译后直接在JVM上运行。那么我们就先来研究一下Java字节码的特点。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（0） 💬（0）<div>看了老师后面的课程来回答一下:

可以在运行期来显示错误信息
把函数名称和函数签名的信息加进去，会有利于我们实现多模块的运行机制。也就是说，如果一个模块中的函数要调用另一个模块中的函数，那么我们可以创造一种机制，实现模块之间的代码查找。</div>2021-09-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（0） 💬（0）<div>函数符号被看作常量，是不是因为函数符号类似于函数地址，跟字符串常量和数字常量一样都不可以被更改？
这些符号信息是不是在需要调试或追踪程序运行信息时,方便了解程序运行的上下文信息？</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（0） 💬（0）<div>回答一下思考题，符号表信息可以实现函数式编程的支持</div>2021-08-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZoI5olaqlJMDK7saLAPIaZZFSZPOYHkicXk9ywXLlDwp6CsBj4CmtU1F61kPcHCnmu6IsGWicXrdA/132" width="30px"><span>bjuthang</span> 👍（0） 💬（0）<div>赞👍</div>2021-08-25</li><br/>
</ul>