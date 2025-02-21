你好，我是陈天。

Trait，trait，trait，怎么又是 trait？how old are you?

希望你还没有厌倦我们没完没了地聊关于 trait 的话题。因为 trait 在 Rust 开发中的地位，怎么吹都不为过。

其实不光是 Rust 中的 trait，任何一门语言，和接口处理相关的概念，都是那门语言在使用过程中最重要的概念。**软件开发的整个行为，基本上可以说是不断创建和迭代接口，然后在这些接口上进行实现的过程**。

在这个过程中，有些接口是标准化的，雷打不动，就像钢筋、砖瓦、螺丝、钉子、插座等这些材料一样，无论要构筑的房子是什么样子的，这些标准组件的接口在确定下来后，都不会改变，它们就像 Rust 语言标准库中的标准 trait 一样。

而有些接口是跟构造的房子息息相关的，比如门窗、电器、家具等，它们就像你要设计的系统中的 trait 一样，可以把系统的各个部分联结起来，最终呈现给用户一个完整的使用体验。

之前讲了trait 的基础知识，也介绍了如何在实战中使用 trait 和 trait object。今天，我们再花一讲的时间，来看看如何围绕着 trait 来设计和架构系统。

由于在讲架构和设计时，不免要引入需求，然后我需要解释这需求的来龙去脉，再提供设计思路，再介绍 trait 在其中的作用，但这样下来，一堂课的内容能讲好一个系统设计就不错了。所以我们换个方式，把之前设计过的系统捋一下，重温它们的 trait 设计，看看其中的思路以及取舍。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/35/6d/07a42f81.jpg" width="30px"><span>郑晔</span> 👍（7） 💬（3）<div>老师对单一职责的理解是错的，这一点是我特意在《软件设计之美》中纠正的，因为单一功能是一个永远为真的说法，单一职责是要把变化纳入考量。具体的可以参考《软件设计之美》和《架构整洁之道》中关于单一职责的讲解。</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（1） 💬（2）<div>doc: https:&#47;&#47;github.com&#47;yewstack&#47;yew&#47;blob&#47;master&#47;packages&#47;yew&#47;src&#47;html&#47;component&#47;mod.rs#L42

1. 不能, 返回类型有Self; 运行时type被erase掉了, 不知道Self具体是什么类型.
2. Message感觉有点像actor里面的message: op to change component state. 应该是用于定义交互的时候, dynamic change component的. Properties应该是DOM的property, 用于render view的…

比如impl Component for List https:&#47;&#47;github.com&#47;yewstack&#47;yew&#47;blob&#47;master&#47;packages&#47;yew&#47;src&#47;virtual_dom&#47;vlist.rs#L495
```
    #[derive(Clone, Properties, PartialEq)]
    pub struct ListProps {
        pub children: Children,
    }

impl Component for List {
      fn view(&amp;self, ctx: &amp;Context&lt;Self&gt;) -&gt; Html {
          html! { &lt;&gt;{ for ctx.props().children.iter() }&lt;&#47;&gt; }
      }
```
3. https:&#47;&#47;docs.rs&#47;yew&#47;0.18.0&#47;yew&#47;#example; 重点是`Sized` `+ &#39;Static` bound`. 实现的类型必须是Sized. 同时如果有reference element, 其lifetime必须是static的.

感觉virtual dom有必要了解了解...</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（2）<div>今天写了一段全局单例的代码，如下所示.

```
pub struct Monitor {
    sender: UnsafeCell&lt;Option&lt;mpsc::TxUnbounded&lt;Vec&lt;xxx&gt;&gt;&gt;&gt;,
}

impl Monitor {
    pub fn set_sender(&amp;self, sender: mpsc::TxUnbounded&lt;Vec&lt;xxx&gt;&gt;) {
        let self_sender_option: &amp;mut Option&lt;mpsc::TxUnbounded&lt;Vec&lt;xxx&gt;&gt;&gt; =
            unsafe { transmute(self.sender.get()) };
        self_sender_option.replace(sender);
    }

    pub fn send_monitor(&amp;self, info_vec: Vec&lt;xxx&gt;) {
        let self_sender: &amp;mut Option&lt;mpsc::TxUnbounded&lt;Vec&lt;xxx&gt;&gt;&gt; =
            unsafe { transmute(self.sender.get()) };
        ...
    }
}

unsafe impl Send for Monitor {}
unsafe impl Sync for Monitor {}

&#47;&#47;why we use Arc to contain Monitor is that lazy_static seems a const value.
&#47;&#47;rust can&#39;t change the const value unless new at first.
&#47;&#47;but Arc can share to use the value.
lazy_static! {
    pub static ref GLOBAL_MONITOR: Arc&lt;Monitor&gt; =
        Arc::new(Monitor { sender: UnsafeCell::new(None) });
}
```

这里使用lazy_static进行全局实现静态变量，但是因为初始化的时候并没有办法指向一个其他的变量，因此这里考虑使用了Arc处理，但是这段代码其实还是有点问题的，因为并没有考虑到竞争并发的情况，但是这里似乎更加适合使用once cell。rust在这部分的实现，感觉还是有点欠缺的。</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a3/87/eb923eb3.jpg" width="30px"><span>0@1</span> 👍（0） 💬（1）<div>老师，想问下关于trait的一些问题, 下面是个代码例子，
struct MyStruct;
trait MyTrait{
    fn test(&amp;self);
}

impl MyTrait for MyStruct{
    fn test(&amp;self) {
        println!(&quot;MyStruct&quot;)
    }
}
impl MyTrait for &amp;MyStruct{
    fn test(&amp;self) {
        println!(&quot;&amp;MyStruct&quot;)
    }
}
impl MyTrait for *const MyStruct{
    fn test(&amp;self) {
        println!(&quot;*const MyStruct&quot;)
    }
}
fn main() {
   let my_struct = MyStruct;
    my_struct.test();
    &amp;my_struct.test();
    let my_struct_ptr = &amp;my_struct as *const MyStruct;
    my_struct_ptr.test();
}

1. impl MyTrait for &amp;MyStruct 和 impl MyTrait for MyStruct 这2个有什么区别，什么情况下适合
为引用实现trait, impl MyTrait for &amp;MyStruct

2. impl MyTrait for *const MyStruct 
这种方式，给裸指针实现trait, 有什么使用场景么



</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>接口的设计要注重用户体验，这太重要了。</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/08/2b/7a1fb4ff.jpg" width="30px"><span>David.Du</span> 👍（0） 💬（0）<div>Trait 对T的一些约束，同时也提醒了T的实现者，要按照这个去做，Fn的函数功能，同时也约束了自身，我感觉一套系统定义完一些列的Trait+数据结构后，剩下的就是实现了。</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>思考题：

Component trait 可以做 trait object 么？
做不了 trait object，因为其中的方法并不符合对象安全原则，要么返回  Self 对象，要么带有泛型参数

关联类型 Message 和 Properties 的作用是什么？
Message 的作用是用来和 Component 进行交互，使其获得动态能力的。 properties 则表达了 Component 的属性，当 Component 的父组件被重新渲染时，子组件要么重新生成，要么从传递给 changed 方法中的上下文接受新的 properties

做为使用者，该如何用 Component trait？它的 lifecycle 是什么样子的？
为自定义类型实现 Component trait 需要指定关联类型 Message 和 Properties，并提供 create 和 view 两个方法的自定义实现即可。它的 lifecycle 是静态生命周期，贯穿程序的始终</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/02/78/4d40b4b2.jpg" width="30px"><span>渡鸦10086</span> 👍（0） 💬（0）<div>思考题：
1. Component trait 的 create 方法会返回 Self，所以不能做 trait Object
2. 关联类型 Message 用于让 Components 类型动态化及可交互化，Component 可以使用 enum 或 () 来声明。 Properties 就是 Component 的属性，当 Component 的父组件被重新渲染时时，它将被重新创建，或者在传递给被改变的 life cycle 方法的上下文中接收新的属性。
3. YEW的官方实例：https:&#47;&#47;docs.rs&#47;yew&#47;0.18.0&#47;yew&#47;#example。life cycle ： `&#39;static` 代表静态生命周期
4. 没有前端经验。。
</div>2022-01-17</li><br/>
</ul>