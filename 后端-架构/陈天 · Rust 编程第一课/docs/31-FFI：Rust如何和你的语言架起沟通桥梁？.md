你好，我是陈天。

FFI（Foreign Function Interface），也就是外部函数接口，或者说语言交互接口，对于大部分开发者来说，是一个神秘的存在，平时可能几乎不会接触到它，更别说撰写 FFI 代码了。

其实你用的语言生态有很大一部分是由 FFI 构建的。比如你在 Python 下使用着 NumPy 愉快地做着数值计算，殊不知 NumPy 的底层细节都是由 C 构建的；当你用 Rust 时，能开心地使用着 OpenSSL 为你的 HTTP 服务保驾护航，其实底下也是 C 在处理着一切协议算法。

我们现在所处的软件世界，几乎所有的编程语言都在和 C 打造出来的生态系统打交道，所以，**一门语言，如果能跟 C ABI（Application Binary Interface）处理好关系，那么就几乎可以和任何语言互通**。

当然，对于大部分其他语言的使用者来说，不知道如何和 C 互通也无所谓，因为开源世界里总有“前辈”们替我们铺好路让我们前进；但对于 Rust 语言的使用者来说，在别人铺好的路上前进之余，偶尔，我们自己也需要为自己、为别人铺一铺路。谁让 Rust 是一门系统级别的语言呢。所谓，能力越大，责任越大嘛。

也正因为此，当大部分语言都还在吸血 C 的生态时，Rust 在大大方方地极尽所能反哺生态。比如 cloudflare 和百度的 [mesalink](https://github.com/mesalock-linux/mesalink) 就分别把纯 Rust 的 HTTP/3 实现 quiche 和 TLS 实现 Rustls，引入到 C/C++ 的生态里，让 C/C++ 的生态更美好、更安全。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/8c/a9b23fcc.jpg" width="30px"><span>卷王之王</span> 👍（2） 💬（2）<div>你好，我想用c语言调用rust，rust代码中用到了tokio。tokio的main函数中有 #[tokio::main] 的标记。这种情况不知道怎么提供给c语言接口了。


#[tokio::main]
async fn main() -&gt; Result&lt;()&gt; {
    &#47;&#47; Open a connection to the mini-redis address.
    let mut client = client::connect(&quot;127.0.0.1:6379&quot;).await?;</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（1） 💬（2）<div>私以为对FFI的理解, 重点还是对ABI的理解; 

C-ABI就像英语一样…不同母语的人可以通过英语交流…数据转换就相当于翻译的过程…中文 → 英文 → 法文; 目前很多机器翻译AI也是把target lang翻译成英语…英语有点像一个MIR了

ABI里面最重要的, 估计就是calling convention了: https:&#47;&#47;flint.cs.yale.edu&#47;cs421&#47;papers&#47;x86-asm&#47;asm.html;


- 阅读 std::ffi 的文档，想想 Vec 如何传递给 C？再想想 HashMap 该如何传递？有必要传递一个 HashMap 到 C 那一侧么？

如果用std::ffi的话, 需要把Vec&lt;T&gt;转成Vec&lt;u8&gt;再转成CString…能不能传, 还有个关键是T必须要有C representation和bindings, 不然到了C里面, 也不知道怎么用T…

HashMap没必要, 也需要做类似的serialization, 但是, 怎么做deserialization就没那么容易了; 毕竟从一个nul-terminated 的char*里面还原HashMap是不可能的


- 阅读 rocksdb 的代码，看看 Rust 如何提供 rocksDB 的绑定。

https:&#47;&#47;github.com&#47;rust-rocksdb&#47;rust-rocksdb&#47;blob&#47;master&#47;librocksdb-sys&#47;build.rs;
librocksdb-sys提供C bindings → unsafe crate → 挺复杂的, bind了很多库…
整个rocksdb crate提供safe rust api;</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（1） 💬（1）<div>Q: 有个小问题, 为啥bindings.h不需要以下这些header, 咋一build就自动添加这些header呢? 难道是ffi的scaffolding的代码需要?

    #include &lt;cstdarg&gt;
    #include &lt;cstdint&gt;
    #include &lt;cstdlib&gt;
    #include &lt;ostream&gt;
    #include &lt;new&gt;

Q: Swift call rust FFI 代码的时候,  发生了什么呢?
我猜想是: `dlopen` 找到rust代码编译成的dylib, 然后用dlsym 找到函数 `math::hello`;  `math_6c3d_hello` 封装好了这个流程.


    public func hello(name: String) -&gt; String {
        let _retval = try!
            rustCall {
                math_6c3d_hello(name.lower(), $0)
            }
        return try! String.lift(_retval)
    }
    ...
    private func makeRustCall&lt;T&gt;(_ callback: (UnsafeMutablePointer&lt;RustCallStatus&gt;) -&gt; T, errorHandler: (RustBuffer) throws -&gt; Error) throws -&gt; T {
        var callStatus = RustCallStatus()
        let returnedVal = **callback(&amp;callStatus)**
        &#47;&#47; ...
    }
</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（2）<div>&quot;正常情况下应该创建另一个 crate 来撰写这样的接口&quot;，如果发布到crates.io上，“另一个crate”需要单独发布吗？也就是说在使用时会有两个dependences需要加入toml吗？（一个abc-sys，还有一个abc-interface）</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（0） 💬（1）<div>&gt; The ABI for C is platform-specific (OS, processor) - it covers issues such as register allocation and calling conventions, which are obviously specific to a particular processor. 

https:&#47;&#47;stackoverflow.com&#47;questions&#47;4489012&#47;does-c-have-a-standard-abi

这样的话, 在之前评论里, 英语的那个类比就不恰当了...英语有很多dialect, 大家是可以用**标准**英语交流...和普通话一样的道理, 有个公认的标准...

那么问题来了, 既然C-abi并没有标准, 为什么大家喜欢选择它作为中间的bridge呢? 难道是因为它最简单通用, 没有标准也可以 (实现不用platform agonostic)?</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>如何在 build.rs 断点调试呢？</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/72/c1/59509397.jpg" width="30px"><span>沈畅</span> 👍（1） 💬（1）<div>
  thread &#39;main&#39; panicked at &#39;Unable to find libclang: &quot;the `libclang` shared library at &#47;home&#47;dev12&#47;llvm&#47;lib&#47;libclang.so.9 could not be opened: &#47;lib64&#47;libc.so.6: version `GLIBC_2.18&#39; not found (required by &#47;home&#47;dev12&#47;llvm&#47;lib&#47;..&#47;lib&#47;libc++abi.so.1)&quot;&#39;, &#47;home&#47;dev12&#47;.cargo&#47;registry&#47;src&#47;mirrors.zte.com.cn-e61ca787596def60&#47;bindgen-0.59.2&#47;src&#47;lib.rs:2144:31
这个问题大家遇见过吗？难道clang版本太低了？</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/13/77/1cd8e04f.jpg" width="30px"><span>Edwin</span> 👍（0） 💬（0）<div>目前我们正在做3的事情
</div>2022-02-27</li><br/>
</ul>