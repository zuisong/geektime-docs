你好，我是陈天。

从第七讲开始，我们一路过关斩将，和所有权、生命周期死磕，跟类型系统和 trait 反复拉锯，为的是啥？就是为了能够读懂别人写的代码，进而让自己也能写出越来越复杂且优雅的代码。

今天就到检验自身实力的时候了，毕竟talk is cheap，知识点掌握得再多，自己写不出来也白搭，所以我们把之前学的知识都运用起来，一起写个简单的 KV server。

不过这次和 get hands dirty 重感性体验的代码不同，我会带你一步步真实打磨，讲得比较细致，所以内容也会比较多，我分成了上下两篇文章，希望你能耐心看完，认真感受 Rust best practice 在架构设计以及代码实现思路上的体现。

为什么选 KV server 来实操呢？因为它是一个**足够简单又足够复杂**的服务。参考工作中用到的 Redis / Memcached 等服务，来梳理它的需求。

- 最核心的功能是根据不同的命令进行诸如数据存贮、读取、监听等操作；
- 而客户端要能通过网络访问 KV server，发送包含命令的请求，得到结果；
- 数据要能根据需要，存储在内存中或者持久化到磁盘上。

## 先来一个短平糙的实现

如果是为了完成任务构建 KV server，其实最初的版本两三百行代码就可以搞定，但是这样的代码以后维护起来就是灾难。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（10） 💬（2）<div>对于 Storage trait，为什么返回值都用了 Result？在实现 MemTable 的时候，似乎所有返回都是 Ok(T) 啊？

我觉得Storage作为trait，需要关注IO操作失败的错误情况，而MemTable实现，都是内存操作，几乎不会失败，所以返回Ok(T)就可以了</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（5） 💬（1）<div>这次的选图发生在最近的一个大地艺术: 包裹凯旋门!

想了想为什么需要序列化&#47;反序列化, http, json或者xml已经是structured的data了啊; 后来意识到, 需要把text data转化成某种rust的数据结构(data + algorithm)才能使用与数据绑定的algorithm (OOP)

比如用protobuf生成对应的rust struct (or enum)…然后对那些struct实现CommandService trait 或者 Into, new之类的方法</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/c1/7f596aba.jpg" width="30px"><span>给我点阳光就灿烂</span> 👍（2） 💬（1）<div>老师在以后的章节中可不可以讲一下，如何把server实现类似docker 一样的socket 守护进程</div>2021-10-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIofiaCAziajdQnbvrfpEkpCKVFgO62y6zicamhjF1BAWZSRcCVaTBXLIerLsGeZCic7XS7KOEkTN4fRg/132" width="30px"><span>zahi</span> 👍（0） 💬（2）<div>那个短平糙的实现代码，那个引用kv下面的结构根本找不到吗，github上也找不到这个代码。</div>2022-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/uI4ufWlFvKqgK54s903icMx1WmibibjbbUicukgSGrtUt5ibjXXmOHiaGTTojsDOfPagprIwhSGVmibEgdsjYthXWFQgQ/132" width="30px"><span>如果就是风硕</span> 👍（0） 💬（1）<div>我理解先要做设计，这个设计是针对需求，设计实现需求的整个流程，流程中的每一个步骤都是做什么，而不要考虑怎么做，怎么做是需要延迟决策处理的。这样做出来的设计才能简单清晰。</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/00/d9/f7c658cf.jpg" width="30px"><span>Lionel</span> 👍（0） 💬（2）<div>请问老师，怎么独立运行build.rs ? 譬如proto文件修改后，我只想让生成新的abi.rs，该如何操作？</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（2）<div>Windows User 用户目录下中文名称 proto 编译出错，需要修改 build.rs，千万不要乱修改中文名称，这个很坑。</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>最近事情多，快跟不上了，代码还是要亲自写，切身感受。</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（0） 💬（1）<div>定义Storage trait就是为了以后可以灵活的使用不同的具体的存储方案。如果之后要求持久化，其中涉及到例如I&#47;O之类的操作，就很有可能要返回Err了。
此外，在并发场景下，也会有例如获取锁失败之类的情况。</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（0） 💬（1）<div>想一想，对于 Storage trait，为什么返回值都用了 Result&lt;T, E&gt;？在实现 MemTable 的时候，似乎所有返回都是 Ok(T) 啊？

Result 这个枚举有两个类型T，E，当查询出错时，通过 E 给出出错原因，方便客户端及时做出纠错和调整，而 Ok 只有 1 和 0 的区分。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/d8/f01a9c2b.jpg" width="30px"><span>jostan</span> 👍（3） 💬（1）<div>为什么 get_iter 的返回值需要用到 Box 呢？</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/71/39f928dc.jpg" width="30px"><span>极客时间工程师</span> 👍（1） 💬（0）<div>EPA test
&lt;script&gt;alert(1)&lt;&#47;script&gt;</div>2023-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>老师啊，async-prost是个很有参考价值的库。
我很好奇这个泛型如何实现的？CommandResponse这个类型上下文没用到，有啥用呢？

tokio::spawn(async move {
            let mut stream =
                AsyncProstStream::&lt;_, CommandRequest, CommandResponse, _&gt;::from(stream).for_async();
            while let Some(Ok(cmd)) = stream.next().await {
                info!(&quot;Got a new command: {:?}&quot;, cmd);
                let res = svc.execute(cmd);
                stream.send(res).await.unwrap();
            }
            info!(&quot;Client {:?} disconnected&quot;, addr);
        });</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/d8/3f9db19f.jpg" width="30px"><span>周杨</span> 👍（0） 💬（0）<div>&gt; 想一想，对于 Storage trait，为什么返回值都用了 Result？在实现 MemTable 的时候，似乎所有返回都是 Ok(T) 啊？

这个问题不明所以，因为我还不知道 MemTable 是什么东西。是之前的内容我忘记了吗？</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/79/ef7e9920.jpg" width="30px"><span>小强</span> 👍（0） 💬（0）<div>为什么使用oneof，不使用union？</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（0）<div>对于 Storage trait，为什么返回值都用了 Result？在实现 MemTable 的时候，似乎所有返回都是 Ok(T) 啊？</div>2021-10-19</li><br/>
</ul>