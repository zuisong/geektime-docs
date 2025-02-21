你好，我是陈天。

学完上一讲，我们对 Future 和 async/await 的基本概念有一个比较扎实的理解了，知道在什么情况下该使用 Future、什么情况下该使用 Thread，以及 executor 和 reactor 是怎么联动最终让 Future 得到了一个结果。

然而，我们并不清楚为什么 async fn 或者 async block 就能够产生 Future，也并不明白 Future 是怎么被 executor 处理的。今天我们就继续深入下去，看看 async/await 这两个关键词究竟施了什么样的魔法，能够让一切如此简单又如此自然地运转起来。

提前说明一下，我们会继续围绕着 Future 这个简约却又并不简单的接口，来探讨一些原理性的东西，主要是 Context 和 Pin这两个结构：

```rust
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

这堂课的内容即便没有完全弄懂，也并不影响你使用 async/await。如果精力有限，你可以不用理解所有细节，只要抓住这些问题产生的原因，以及解决方案的思路即可。

## Waker 的调用机制
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（9） 💬（2）<div>我之前记录并翻译过无船同志（withoutboats）的一个讲座，供大家参考：https:&#47;&#47;gteng.org&#47;2021&#47;01&#47;30&#47;zero-cost-async-io&#47;</div>2021-11-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（3） 💬（1）<div>Pin了后的数据 所有者变成谁了?</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/12/e4/57ade29a.jpg" width="30px"><span>dva</span> 👍（1） 💬（1）<div>Box&lt;T&gt;是Unpin，因为Box&lt;T&gt;实现了Unpin trait</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/c8/d6f00a46.jpg" width="30px"><span>wowotuo</span> 👍（0） 💬（1）<div>讲得很牛逼，现在反反复复听了看了不下10次</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a4/97/bc269801.jpg" width="30px"><span>良师益友</span> 👍（0） 💬（1）<div>以前在这里卡住了，这次说明白了，感谢老师</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/09/afa3e112.jpg" width="30px"><span>清风徐来</span> 👍（1） 💬（2）<div>有了Pin为啥还有!UnPin</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d0/f7/401c20e2.jpg" width="30px"><span>Rustlab</span> 👍（0） 💬（0）<div>我越看越困惑，
write_hello_file_async(&quot;&#47;tmp&#47;hello&quot;).await?;这里，如果只是生成loop，那这就是同步代码了，能详细讲一讲，
write_hello_file_async(&quot;&#47;tmp&#47;hello&quot;).await?;在调用处是如何被处理，其如何注册到异步运行时、最后future的poll方法是怎么样被不断重复调用的吗？这里的poll里面有一个loop，我感觉真实场景不会这么干吧。</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d0/f7/401c20e2.jpg" width="30px"><span>Rustlab</span> 👍（0） 💬（0）<div>我越看越困惑，
write_hello_file_async(&quot;&#47;tmp&#47;hello&quot;).await?;这里，如果只是生成loop，那这就是同步代码了，能详细讲一讲，
write_hello_file_async(&quot;&#47;tmp&#47;hello&quot;).await?;在调用处是如何被处理，其如何注册到异步运行时、最后future的poll方法是怎么样被不断重复调用的吗？这里的poll里面有一个loop，我感觉真实场景不会这么干吧。</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（3）<div>有些凌乱，在第二个move_creates_issue示例（使用了Pin的那个）里，move_it无法调用是因为原来的SelfReference类型的data（值)被shadow了，如果把data改个名字，move_it依旧可以调用，和Pin没啥关系？
不过如果将move_it与它上面的那条语句互换下位置，确实会编译不通过，原因是在有借用的情况下移动，那这么说我不使用Pin，随便使用一个&amp;SelfReference或者&amp;mut SelfReference，也能阻止移动呢？</div>2022-11-23</li><br/><li><img src="" width="30px"><span>doubled</span> 👍（0） 💬（0）<div>老师能具体讲讲phantomdata么，在Waker中为什么marker要是phantomdata&lt;fn(&amp;&#39;a ())-&gt;&amp;&#39;a ()&gt;，能不能使用phantomdata&lt;&amp;&#39;a ()&gt;或者使用phantomdata&lt;&amp;&#39;a mut ()&gt;</div>2022-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/ad/4efd929a.jpg" width="30px"><span>老荀</span> 👍（0） 💬（0）<div>二刷…老师的课太良心了…</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/c3/abb7bfe3.jpg" width="30px"><span>JK.Ryan</span> 👍（0） 💬（0）<div>庖丁解牛，很赞~👍🏻</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（0）<div>从基础到原理好好研究 Future。</div>2021-11-29</li><br/>
</ul>