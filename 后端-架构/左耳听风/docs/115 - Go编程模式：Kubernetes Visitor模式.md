你好，我是陈皓，网名左耳朵耗子。

这节课，我们来重点讨论一下，Kubernetes 的 `kubectl` 命令中的使用到的一个编程模式：Visitor（其实，`kubectl` 主要使用到了两个，一个是Builder，另一个是Visitor）。

本来，Visitor 是面向对象设计模式中一个很重要的设计模式（可以看下Wikipedia [Visitor Pattern词条](https://en.wikipedia.org/wiki/Visitor_pattern)），这个模式是将算法与操作对象的结构分离的一种方法。这种分离的实际结果是能够在不修改结构的情况下向现有对象结构添加新操作，是遵循开放/封闭原则的一种方法。这节课，我们重点学习一下 `kubelet` 中是怎么使用函数式的方法来实现这个模式的。

## 一个简单示例

首先，我们来看一个简单设计模式的Visitor的示例。

- 我们的代码中有一个`Visitor`的函数定义，还有一个`Shape`接口，这需要使用 `Visitor`函数作为参数。
- 我们的实例的对象 `Circle`和 `Rectangle`实现了 `Shape` 接口的 `accept()` 方法，这个方法就是等外面给我们传递一个Visitor。

```
package main

import (
    "encoding/json"
    "encoding/xml"
    "fmt"
)

type Visitor func(shape Shape)

type Shape interface {
    accept(Visitor)
}

type Circle struct {
    Radius int
}

func (c Circle) accept(v Visitor) {
    v(c)
}

type Rectangle struct {
    Width, Heigh int
}

func (r Rectangle) accept(v Visitor) {
    v(r)
}
```

然后，我们实现两个Visitor：一个是用来做JSON序列化的；另一个是用来做XML序列化的。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJtl3p4gcguAZy580SyoQAic79Z7QAvTcibnicV9K8x2Yzbxa8BlknwhquzTPPklaWPDDbrECQG3uurg/132" width="30px"><span>lumence</span> 👍（4） 💬（1）<div>使用装饰器，是不是该这样写哦
type VisitorDecorator func(VisitorFunc) VisitorFunc

type DecoratedVisitor struct {
	visitor    Visitor
	decorators []VisitorDecorator
}

func NewDecoratedVisitor(v Visitor, fn ...VisitorDecorator) Visitor {
	if len(fn) == 0 {
		return v
	}
	return DecoratedVisitor{v, fn}
}

&#47;&#47; Visit implements Visitor
func (v DecoratedVisitor) Visit(fn VisitorFunc) error {
	decoratorLen := len(v.decorators)
	for i := range v.decorators {
		d := v.decorators[decoratorLen-i-1]
		fn = d(fn)
	}
	return fn(v.visitor.(*Info), nil)
}</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/42/76eb78bd.jpg" width="30px"><span>hunknownz</span> 👍（0） 💬（0）<div>耗子哥，看最后「装饰器重构」这块，我的理解可能出了问题，你确认下。

k8s 中对于 Visitor 这块有两种结构：

一个是 VisiterList，它的 Visit 方法负责横向聚合各个 visitor 的 Visit 方法，把多个 visitor 合成一个 visitor，执行上存在父子 visitor 的关系，类似文章中把 LogVisitor，NameVisitor，OtherThingsVisitor 聚合成一个 visitor；

另一个是 DecoratedVisitor ，它的 Visit 方法负责纵向聚合多个 VisitorFunc 到一个 visitor 上，使 Visit 方法的逻辑更丰富，没有任何父子嵌套关系，它的 Visit 方法执行时先执行自己聚合的 decorators 方法们，然后再执行传入的 VisitorFunc。

我理解文章中「装饰器重构」是要完成 VisitorList 功能，但是使用了 DecoratedVisitor 这个结构，所以末尾的代码有一些执行不通。</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/4a/3d/b96f090c.jpg" width="30px"><span>黑白灰</span> 👍（0） 💬（4）<div>var v Visitor = &amp;info
  v = LogVisitor{v}
  v = NameVisitor{v}
  v = OtherThingsVisitor{v}

请教一下go的，那个特性可以支持这种嵌套赋值</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/bd/b83ad32d.jpg" width="30px"><span>shangyu</span> 👍（0） 💬（0）<div>耗子叔，最后那个NewDecoratedVisitor调用的传餐不对哦？</div>2021-02-05</li><br/>
</ul>