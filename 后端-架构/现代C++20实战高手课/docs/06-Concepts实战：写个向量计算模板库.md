你好，我是卢誉声。

Concept之于C++泛型编程，正如class之于C++面向对象。在传统的C++面向对象编程中，开发者在写代码之前，要思考好如何设计“类”，同样地，在C++20及其后续演进标准之后，我们编写基于模板技术的泛型代码时，必须先思考如何设计好“concept”。

具体如何设计呢？今天我们就来实战体验一下，使用C++模板，编写一个简单的向量计算模板库。

在开发过程中，我们会大量使用Concepts和约束等C++20以及后续演进标准中的特性，重点展示如何基于模板设计与开发接口（计算上如何通过SIMD等指令进行性能优化不是关注的重心）。

完成整个代码实现后，我们会基于今天的开发体验，对Concepts进行归纳总结，进一步深入理解（课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)即可获取）。

好，话不多说，我们直接开始。

## 模块组织方式

对于向量计算模板库这样一个项目，我们首先要考虑的就是如何组织代码。

刚刚学的C++ Modules正好可以派上用场，作为工程的模块组织方式。后面是项目的具体结构。  
![](https://static001.geekbang.org/resource/image/2d/7f/2d7767067160c57b811b567423576e7f.jpg?wh=3820x2866)

实现向量计算库的接口时，我们会部分模仿Python著名的函数库NumPy。因此，向量库的模块命名为numcpp，namespace也会使用numcpp。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（1） 💬（1）<div>内容太干了。哈哈。
nits：concepts.cpp的line 38应该是IteratorMemberFunction(&amp;T::end)吧？</div>2023-01-29</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>我觉得concepts确实比modules有用多了。。。前者能改变编程思想，后者在我看来只是换汤不换药的语法糖，反而让语法看起来更复杂</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（0） 💬（1）<div>定义 creation 模块时用到的 fillContainerBuffer、makeContainerShape 和 ContainerValueTypeHelper 这些约束表达式，就利用了 concept 的“原子约束”特性选择不同的模版版本，实现了泛型编程中的“多态”特性。

没看懂哪里体现了泛型编程的多态</div>2023-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8aLz0tWdsZuMiaNUAd0dicSD9M6A77seMGFdHgvsQwOzN8ztYPiaJSo53DcbjQWUQpw4pf4rI2f7vg/132" width="30px"><span>Geek_7c0961</span> 👍（0） 💬（1）<div>concepts 这个feature太强了, 让我想起了rust中的traits 和 traits objects.</div>2023-01-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqDjaVmMr3nEFicazTso4spiae7icg4WjHTb8E2Y3n71PaGiaPqmCU3JsasmpAXB6dcIoXwy8LTn1aADQ/132" width="30px"><span>Geek_e04349</span> 👍（0） 💬（1）<div>感觉 SliceItem 的 getValidValue 使用 optional 返回会更符合其语义</div>2023-01-27</li><br/>
</ul>