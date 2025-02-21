你好，我是宋一玮，欢迎回到React应用开发的学习。

在前面两节课里，我们学习了应用状态管理的概念和代表性框架Redux，以及Redux的封装库Redux Toolkit + React Redux的用法。

同时，我们也分析了React应用中的三种状态：业务状态、交互状态和外部状态，以及从数据流层面区分的全局状态和局部状态。最后根据这些分类，我们对React项目什么时候使用Redux，什么时候混用React内建state和Redux提出了一些建议。

当React应用中的状态越来越多，越来越复杂时，你有可能遇到这样的痛点：

- 通过props、context传递状态数据时，时不时会用错数据的类型导致Bug；
- 把自己开发的组件给别人用，别人不知道你的组件props的数据类型；
- 当你用别人开发的组件时，虽然有文档，但你发现已经跟现在的版本对不上了；
- 当你去自己一个月前写的组件里修Bug时，实在记不清了，要读上下游的代码或者在浏览器中设断点调试，才能判断出某个props的数据类型。

这些痛点归根结底都是因为**JavaScript是弱类型的语言，变量类型在运行时才能确定，在开发阶段无法指定变量类型**。在大中型React项目中，引入类型系统是十分必要的。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/05/0b/9a877a15.jpg" width="30px"><span>恒`∞`真理</span> 👍（0） 💬（1）<div>回答一下第2个问题：
静态类型的好处是开发体验有保障、运行时类型错误少甚至可以完全避免，代价我认为有两个。其一是类型推断能力受限于编译器性能，有时不得不进行显式类型标注，稍显啰嗦；其二是静态类型一定程度上限制了扩展性，维护SemVer库需要格外注意不破坏类型接口。TypeScript算是在二者之间取得了一个不错的平衡，但是在遇到完全没有类型标注或者滥用动态性的JS库时还是会抓瞎。</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/80/52161b2f.jpg" width="30px"><span>Faith信</span> 👍（3） 💬（0）<div>TS type和interface的差异  interface可以extends； type再某些场景下会出现 unknown影响类型推导，所以开源使用interface会多于type</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/e1/15/bdea351e.jpg" width="30px"><span>36#</span> 👍（1） 💬（0）<div>&quot;TS 是在应用的开发期和编译期产生效果的，能帮开发者减少编程错误，但对运行时没有直接帮助。&quot;
所以，线上表单数据验证不能用 ts</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（0）<div>老师好，KanbanColumn这个组件在进行ts改造后，在返回的&lt;section&gt;上有个属性是css，ts会报错，css为不存在的属性，这个问题如何解决？</div>2024-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（1）<div>请问老师和各位同学，本节思考题的第1题，如何做线上表单的类型验证。平时开发中都是使用现有的组件库，配置一个属性就好了。如何用ts实现，还没想到什么办法。</div>2023-01-13</li><br/>
</ul>