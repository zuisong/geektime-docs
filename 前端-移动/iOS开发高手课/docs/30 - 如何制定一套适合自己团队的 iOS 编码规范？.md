你好，我是戴铭。

如果团队成员的编码规范各不相同，那么你在接收其他人的代码时是不是总会因为无法认同他的代码风格，而想着去重写呢。但是，重写这个事儿不只会增加梳理逻辑和开发成本，而且重写后出现问题的风险也会相应增加。那么，这个问题应该如何解决呢？

在我看来，如果出现这种情况，你的团队急需制定出一套适合自己团队的编码规范。有了统一的编码规范，就能有效避免团队成员由于代码风格不一致而导致的相互认同感缺失问题。

那么，如何制定编码规范呢？在接下来的内容里，我会先跟你说说，我认为的好的编码规范。你在制定编码规范时，也可以按照这个思路去细化出更多、更适合自己的规范，从而制定出团队的编码规范。然后，我会再和你聊聊如何通过 Code Review 的方式将你制定的编码规范进行落地。

## 好的代码规范

关于好的代码规范，接下来我会从常量、变量、属性、条件语句、循环语句、函数、类，以及分类这8个方面和你一一说明。

### 常量

在常量的使用上，我建议你要尽量使用类型常量，而不是使用宏定义。比如，你要定义一个字符串常量，可以写成：

```
static NSString * const STMProjectName = @"GCDFetchFeed"
```

### 变量

对于变量来说，我认为好的编码习惯是：

1. 变量名应该可以明确体现出功能，最好再加上类型做后缀。这样也就明确了每个变量都是做什么的，而不是把一个变量当作不同的值用在不同的地方。
2. 在使用之前，需要先对变量做初始化，并且初始化的地方离使用它的地方越近越好。
3. 不要滥用全局变量，尽量少用它来传递值，通过参数传值可以减少功能模块间的耦合。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/33/c2/3a5b0d9f.jpg" width="30px"><span>clownfish</span> 👍（15） 💬（1）<div>前辈,我看了你说的大部分都是Effective 2.0里面的内容,有没有一些您在工作实践中的代码规范要求呢,例如我想到的使用#pragma 做代码分区等一些,</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/a4/17a2d602.jpg" width="30px"><span>棒棒彬👻</span> 👍（1） 💬（1）<div>「写代码的首要任务是能让其他人看得懂，千万不要优先过度工程化。」，过度工程化该怎么理解呢？是否能举个例子？</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/68/50c74080.jpg" width="30px"><span>肥仔</span> 👍（0） 💬（1）<div>这篇很有帮助，看来要花很多时间去实践一下才行，编码规范真的很重要</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/4d/107d8201.jpg" width="30px"><span>Geek_462d99</span> 👍（3） 💬（0）<div> 强累推荐[Clean Code](https:&#47;&#47;book.douban.com&#47;subject&#47;4199741&#47;)这本书，作者Bob在书中说出了很多代码规范和技巧。</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/85/8b221758.jpg" width="30px"><span>郑杰</span> 👍（2） 💬（1）<div>静态类型需要 变量名加类感觉没有必要吧</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0e/a7/9b79c245.jpg" width="30px"><span>null</span> 👍（1） 💬（0）<div>与其说是代码规范，不如说涵盖的是思想在里面。而国外一些经典的书籍已经给出答案了，建议程序员必读书籍《重构改善既有的代码设计》。</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/eb/4f/6a97b1cd.jpg" width="30px"><span>猪小擎</span> 👍（0） 💬（0）<div>少引用头文件，而用声明，这点真的有意义吗？头文件里全是声明，1万行的头文件，在我看来对编译期的消耗也近乎是0.</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/eb/4f/6a97b1cd.jpg" width="30px"><span>猪小擎</span> 👍（0） 💬（2）<div>一个团队为什么一定要使用相同的规范呢？每个人都是自己的规范，真的有问题吗？A 用小写下划线，B用驼峰。真的有什么影响吗？</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/15/ee/ea0ccef9.jpg" width="30px"><span>曦咻</span> 👍（0） 💬（0）<div>还可以定制统一代码模版和借助代码格式化插件</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6f/c8/4183a146.jpg" width="30px"><span>大头</span> 👍（0） 💬（0）<div>同意一楼的建议</div>2019-05-20</li><br/>
</ul>