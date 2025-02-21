你好，我是Mike，今天我们一起来学习Rust语言中有关宏的知识。

宏是一套预处理设施。它的输入是代码本身，对代码进行变换然后输出新的代码。一般来说，输出的新代码必须是合法的当前语言的代码，用来喂给当前语言的编译器进行编译。

宏不是一门语言的必备选项，Java、Go等语言就没有宏，而C、CPP、Rust等语言有宏，而且它们的宏工作方式不一样。

在Rust语言中，宏也属于语言的外围功能，用来增强Rust语言的核心功能，让Rust语言变得更方便好用。宏不属于Rust语言的核心，但这并不是说宏在Rust中不重要。其实在Rust代码中，宏随处可见，掌握宏的原理和用法，有助于我们编写更高效的Rust代码。

在Rust中，宏的解析和执行是在Rust代码的编译阶段之前。你可以理解成，在Rust代码编译之前有一个宏展开的过程，这个过程的输出结果就是完整版的Rust代码，然后Rust编译器再来编译这个输出的代码。

## Rust语言中的宏

当前版本的Rust中有两大类宏：声明宏（declarative macro）和过程宏（procedure macro），而过程宏又细分成三种：派生宏、属性宏和函数宏。

下面我们分别介绍一下它们。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（3） 💬（1）<div>allow、warn、deny、forbid: 编译器的警告级别</div>2023-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/14/83867b58.jpg" width="30px"><span>Distance</span> 👍（3） 💬（2）<div>macro_rules! add {
    &#47;&#47; 第一个分支，匹配两个元素的加法
    ($a:expr, $b:expr)=&gt;{
        {
            $a+$b
        }
    };
    &#47;&#47; 第二个分支：当只有一个元素时，也应该处理，这是边界情况
    ($a:expr)=&gt;{
        {
            $a
        }
    }
}

为什么第二个分支匹配不需要分号呢？ 我看第一个示例只有单个匹配也是分号结尾的</div>2023-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（3）<div>cargo expand 宏展开这个网站地址是什么啊</div>2024-02-05</li><br/><li><img src="" width="30px"><span>Taozi</span> 👍（0） 💬（1）<div>过程宏本质上是编译器的扩展插件</div>2023-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（1）<div>感觉和注解有点像</div>2023-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>macro_export 的示例代码中的 inner 模块的宏调用代码有点问题，需要在函数或方法中：
mod inner {
    super::m!();
    crate::m!();
}
应该类似于：
mod inner {
    pub fn foo() {
        super::m!();
        crate::m!();
    }
}</div>2024-04-25</li><br/>
</ul>