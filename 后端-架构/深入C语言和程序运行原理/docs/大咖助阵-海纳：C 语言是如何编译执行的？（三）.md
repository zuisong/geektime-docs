你好，我是海纳。今天是“C 语言是如何编译执行的？”这一加餐系列的最后一讲。

一个编译器通常分为前端、中端和后端三个典型模块。前端主要包括词法分析和文法分析两个步骤，它的作用是把源文件转换成抽象语法树（Abstract Syntax Tree, AST）。在前面两期加餐中，我讲解了预处理、词法分析、文法分析的编译过程基本步骤，带你实现了一个小型 C 语言编译器前端。它将源代码翻译成了AST，而且支持了变量定义和赋值，if语句和while语句。

中端则主要是将AST转成中间表示（Intermediate Representation, IR），常见的中间表示有三地址码、基于图的静态单赋值表示等等，例如LLVM IR就是最常见的一种中间表示。编译器的优化主要集中在中端。

而后端的作用是将中间表示翻译成目标平台的机器码，并生成相应平台的可执行程序。机器码是由CPU指令集决定的，例如x86平台就要使用x86指令集，而arm64平台就应该使用aarch64指令集。华为的鲲鹏平台也是采用了aarch64指令集。可执行程序的格式则是由操作系统决定，例如在Windows系统上，可执行程序是PE格式的，exe文件或者dll文件都是PE格式；而Linux系统上，可执行程序则是ELF文件。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/71/d6f79534.jpg" width="30px"><span>一个工匠</span> 👍（1） 💬（0）<div>悟了，感谢🙏</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/0a/9b2126ac.jpg" width="30px"><span>anqi</span> 👍（0） 💬（0）<div>强赞！</div>2022-05-25</li><br/>
</ul>