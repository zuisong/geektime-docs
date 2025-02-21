你好，我是Mike。今天我们来讲讲Rust语言设计的出发点——所有权，它也是Rust的精髓所在。

在第一节课中，我们了解了Rust语言里的值有两大类：一类是固定内存长度（简称固定尺寸）的值，比如 i32、u32、由固定尺寸的类型组成的结构体等；另一类是不固定内存长度（简称非固定尺寸）的值，比如字符串String。这两种值的本质特征完全不一样。而**怎么处理这两种值的差异，往往是语言设计的差异性所在**。

就拿数字类型来说，C、C++、Java 这些语言就明确定义了数字类型会占用内存中的几个字节，比如8位，也就是一个字节，16位，也就是两个字节。而JavaScript这种语言，就完全屏蔽了底层的细节，统一用一个Number表示数字。Python则给出了int整数、float浮点、complex复数三种数字类型。

Rust语言因为在设计时就定位为一门通用的编程语言（对标C++），它的应用范围很广，从最底层的嵌入式开发、OS开发，到最上层的Web应用开发，它都要兼顾。所以它的数字类型不可避免地就得暴露出具体的字节数，于是就有了i8、i16、i32、i64等类型。

前面我们说到，一种类型如果具有固定尺寸，那么它就能够在编译期做更多的分析。实际上固定尺寸类型也可以用来管理非固定尺寸类型。具体来说，Rust中的非固定尺寸类型就是靠指针或引用来指向，而指针或引用本身就是一种固定尺寸的类型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2c/5d/fc/2e5e2a90.jpg" width="30px"><span>二夕</span> 👍（28） 💬（3）<div>思考题 1: 无法通过编译，可以将第 5 行代码修改为：let tmp_s = s.clone();
思考题 2: 由于 Point 没有实现 Copy trait，所以在赋值过程中会产生 Move。 </div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/51/ea/d9a83bb3.jpg" width="30px"><span>古明地觉</span> 👍（12） 💬（2）<div>好奇一个问题：
fn main() {
    let s1 = &quot;hello world&quot;.to_string();
    let s2 = s1;  &#47;&#47; s1 不再有效，它的值发生了移动
}
显然上面代码很好理解，如果换一种方式。
fn main() {
    let arr = [&quot;hello world&quot;.to_string()];
    let s = arr[0];  &#47;&#47; 报错：String 没有实现 Copy trait
}
这里报错了，按理说不是应该会将所有权从 arr[0] 转移到 s 上面吗？但是 Rust 却提示 cannot move。我的理解是这样的，因为像数组这样的结构如果有效，那么它内部的每一个成员必须都要有效。如果数组中的某个元素发生了移动，那么会导致整个数组不可用，于是为了避免这种情况，Rust 要求数组里面的元素必须是可 Copy 的。如果需要转移所有权，那么 Rust 编译器就报错。否则会给用户造成一个错觉，好端端的数组为啥就不能用了。

如果用这个理论来解释的话，那么就又产生了一个问题。
fn main() {
    &#47;&#47; 元素
    let arr = (&quot;hello world&quot;.to_string(), &quot;hello world&quot;.to_string());
    let s = arr.0;  &#47;&#47; 此处不报错
    &#47;&#47; arr.1 可以正常打印
    println!(&quot;{}&quot;, arr.1);  &#47;&#47; hello world
    &#47;&#47; 但打印 arr.0 和打印 arr 则报错，提示发生了移动
}
所以我很好奇，为啥会产生这种情况。为什么元组（还有结构体）允许局部的元素发生移动，但数组却不可以呢？还请老师帮忙解答一下</div>2023-11-01</li><br/><li><img src="" width="30px"><span>Geek_147053</span> 👍（7） 💬（1）<div>看完了刚更新的前2篇，感觉挺适合新手的，虽然长，但看下来一点儿也不枯燥，讲的挺有意思</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d4/2e/d478a412.jpg" width="30px"><span>duwoodly</span> 👍（6） 💬（1）<div>1. String类型，实际数据在堆上存储。 let tmp_s = s 循环第一次的时候，会移动所有权，s在栈上的内存虽然还在，但是被编译器视为无效变量或无效状态，所以第二次及以后的循环就不能实验变量s了，编译器会报错。
2. 结构体类型默认没有实现Copy trait, 赋值过程也会移动所有权。
    当然从底层看，这个Point结构体的成员都是基本类型（基本类型实现了Copy）, 所以这个结构体的值是保存在栈上的，所以赋值操作，实际上底层是在栈上完整拷贝了一次Point结构体，但是编译器依然会把原来的Point结构体变量视为无效状态或无效变量。</div>2023-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIlnTfD7ZMqTydjgvNJWfOwEPjutftkuCtvjflHj10MtI0B3d4cvibCkAkPzoyqw3MWDnY1ib9IKgPg/132" width="30px"><span>Geek_582a5d</span> 👍（4） 💬（1）<div>目前看来感觉看着最舒服的rust相关系列文章了，催催更新。这个系列会持续跟进，感谢作者。</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/30/d9/323ba366.jpg" width="30px"><span>水不要鱼</span> 👍（3） 💬（1）<div>老师，关于移动还是复制的那段话，我有个迷惑。。我能不能理解其实都是复制了栈上的数据，比如
a = 10u32
b = a
由于 10u32 是放栈上的，实际上是把 a 的数据复制了一份，然后 b 绑定了这份数据，因为数据是独立的，所以所有权也是独立的，a 和 b 各自拥有各自数据的所有权。
而 String 也是一样，把 a 的数据复制了一份到 b 上，但是这时候 a 的数据实际上是堆上数据的地址，所以复制的数据是这个堆上数据的地址，而不是堆上的数据，所以实际数据只有一份，所有权也是一份，这时候 b = a 就会把这一份所有权同时交给 b</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（3） 💬（2）<div>思考题 1：编译报错；两处错误：变量 i 没有使用和 s 的所有权；
修改后如下：
fn main() {
    let s = &quot;I am a superman.&quot;.to_string();
    
    for _ in 1..10 {
        let tmp_s = s.clone();
        println!(&quot;s is {}&quot;, tmp_s);
    }
}

思考题 2：移动；如果结构体中包含实现了 Copy trait，则会进行复制而不是移动</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/ca/eefef69b.jpg" width="30px"><span>刘永臣</span> 👍（3） 💬（1）<div>问题1：本来以为坑在s 因为s在第一次遍历时已经转移了，所以第二次遍历肯定会出错，所以编译器会报错，没有问题；但是实际上循环条件中i 会被多次修改，所以声明i时也应该增加mut；

问题2：结构体数据复合结构，所以对其进行赋值是实际上进行了所有权的转移。</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/71/17/ce7d94ba.jpg" width="30px"><span>Test</span> 👍（2） 💬（3）<div>默认做复制所有权的操作： 
裸指针类型

裸指针类型也是copy语义吧</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/1d/14/fdb57ac7.jpg" width="30px"><span>咖啡☕️</span> 👍（2） 💬（1）<div>问题 1
改成
```
let tmp_s = &amp;s;
```
即可</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/df/be9ecb4e.jpg" width="30px"><span>linkscue</span> 👍（1） 💬（1）<div>验证了一下“一个由固定尺寸类型组成的结构体变量”，是使用移动的所有权的形式：

#[derive(Debug)]
struct Point {
    x: i64,
    y: i64,
    z: i64,
}

fn main() {
    let p = Point { x: 1, y: 2, z: 3 };
    for i in 1..10 {
        let tmp = p;
        println!(&quot;p is {:#?}&quot;, tmp);
    }
}
</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/36/33/3411df0d.jpg" width="30px"><span>seven9t</span> 👍（1） 💬（1）<div>1. 引入所有权是为了自动管理资源，类似uniq_ptr
2. 引入move是为了防止使用无效资源、重复释放
3. 如果不想move, 只能借用, 引出borrow checker和lifetime.</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/9f/de/09e62135.jpg" width="30px"><span>^ ^</span> 👍（1） 💬（1）<div>所以说上面那些默认使用copy复制所有权的变量类型，其实都是rust为他们实现了copy trait的是吗</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/30/d9/323ba366.jpg" width="30px"><span>水不要鱼</span> 👍（1） 💬（2）<div>老师，关于 let 默认不可变的解释我还是有点迷惑，加 mut 增加了可变性的使用成本这个我可以理解，但是我没明白为啥要有 let 和 const 同时存在，理论上去掉 const 关键字，用 let 代替也是一样的，要可变的时候加 mut 变成变量，这样是不是也没啥问题</div>2023-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（1） 💬（1）<div>老师，你好！不可变引用类型，是不是相当于复制了一份地址，还是指向原来的对象，然后因为是只读的，不会影响外面那个变量的所有权</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3e/e8/3736f3cd.jpg" width="30px"><span>冷石</span> 👍（1） 💬（1）<div>可以说讲的很清楚了，👍</div>2023-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/fLI3NSG6qScRzrMBQzuXHzAY0QyialcvoadMd662U7hxhJe7jlpAPgjtRPTicE91lWWSJx80TRrXXaVja59YJQ9g/132" width="30px"><span>Geek_07ce33</span> 👍（1） 💬（2）<div>问一下，这个课程有时间限制吗？？我学的慢，</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b5/5f/4ac4d6c7.jpg" width="30px"><span>不值得</span> 👍（1） 💬（1）<div>好像懂了，应该不会有性能问题，因为不可变，所以应该仅仅只是指针复制</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a0/23/4668496b.jpg" width="30px"><span>馍馍汉宝</span> 👍（1） 💬（1）<div>2的解决方法：
```rs
#[derive(Debug, Clone, Copy)]
struct Point { x: i64, y: i64, z: i64}
```</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a0/23/4668496b.jpg" width="30px"><span>馍馍汉宝</span> 👍（1） 💬（1）<div>2. Move</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a0/23/4668496b.jpg" width="30px"><span>馍馍汉宝</span> 👍（1） 💬（1）<div>1. 会报错，甚至在编译之前，VSCode 就已经提前知道错误信息：use of moved value: `s` value moved here, in previous iteration of loop。并给出了对应的解决方案，加上 .clone（if the performance cost is acceptable）</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9e/15/e499fc69.jpg" width="30px"><span>Andylinge</span> 👍（1） 💬（1）<div>1. 编译器报错，提示s已经move。
error[E0382]: use of moved value: `s`
2. 编译器报错，提示如下：
error[E0382]: borrow of moved value: `p1`
 --&gt; src&#47;main.rs:9:25
  |
7 |  let p1 = Point{x:1, y:1, z:1};
  |      -- move occurs because `p1` has type `Point`, which does not implement the `Copy` trait
8 |  let p2 = p1;
  |           -- value moved here
9 |  println!(&quot;{:?}, {:?}&quot;, p1, p2);
  |                         ^^ value borrowed here after move</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（1） 💬（1）<div>思考题1：编译报错。因为在第一次循环的时候，s 的所有权已经转移到 tmp_s 了，后面 s 已经是无效状态了，不能再转移所有权。
思考题2：移动。</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（1） 💬（1）<div>思考题1：编译报错。因为 s 的所有权在第一次循环的时候已经移动到 tmp_s 了，s 已经是处于无效状态了。</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（1）<div>&quot;变量名加了 mut，多打了 4 个字符&quot;，为什么是4个字符？算上空格吗？</div>2024-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>是否可以这样认为？

在 Rust 中，默认情况下所有权都是不共享的（这里先不讨论高级篇的共享所有权的特殊情况），任何情况下一个资源（值）都只有一个变量拥有它的所有权，所有权的赋予有两种方式：

1、基本数据类型及由它们组成的元组、数组，还有不可变引用&amp;：这些都是固定且明确尺寸的，它们的所有权赋予方式是“资源（值）复制，新变量拥有复制后的资源（值）的所有权，旧变量依然拥有原资源（值）的所有权”；

2、其他类型：这些都不是固定尺寸的（或者说是可变的），它们的所有权赋予方式是“资源（值）不动，所有权发生转移（move：移动、转移）”，新变量获得所有权，可以访问资源（值），而旧变量没有所有权了，就不能再访问原有资源（值）了。如果需要旧变量能继续访问原有资源，除非是把所有权借用给别人（&amp;-borrow，好比借钱给你 - 是要还的，送钱给你 - 是不用还的），当别人使用完返还给你之后，你依然可以访问那个资源，还有一种方法就是把资源（值）复制多一份给别人(clone()，或实现 Copy trait，当然复制的成本也要考虑在内， 复制资源（值）的方式是否合适），新变量可以拥有复制的资源（值）的所有权，从而不影响我对原有资源（值）的所有权。</div>2024-03-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DqpibYJwatzEKhicLSaD6xDyIibLh0kHJM9RX88YOpgIXfbSoERzgKQiaN18KIO9VcNfBPjzPuD07aRH9T6P3EibT5w/132" width="30px"><span>Geek_de2f36</span> 👍（0） 💬（1）<div>思考题1： 无法通过编译，可以将let tmp_s=&amp;s;
思考题2： 移动，结构体没有实现Copy trait，无法复制</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/8c/a3ca2f3d.jpg" width="30px"><span>焉知非鱼</span> 👍（0） 💬（1）<div>看完作者的讲解，感觉我又会了 ^_</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/2e/e8/9dc046af.jpg" width="30px"><span>舒灿</span> 👍（0） 💬（1）<div>这篇文章所有权讲的很清楚了，给作者大大点赞。</div>2024-01-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>思考题1： 无法通过编译
思考题2： 移动（一般 struct 都不会是 Copy 的， 只有栈上的原生数据才有 Copy)</div>2023-12-12</li><br/>
</ul>