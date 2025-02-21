你好，我是Mike。今天我们来聊一聊如何用Rust做一个基于大语言模型的聊天机器人。

大语言模型（LLM）是2023年最火的领域，没有之一。这波热潮是由OpenAI的ChatGPT在今年上半年发布后引起的，之后全世界的研究机构和科技公司都卷入了大模型的竞争中。目前业界应用大模型训练及推理的主要语言是Python和C/C++。Python一般用来实现上层框架，而C/C++一般起底层高性能执行的作用，比如著名的框架 PyTorch，它的上层业务层面是用Python写的，下层执行层面由C执行，因为GPU加速的部分只能由C/C++来调用。

看起来大语言模型好像和Rust没什么关系，必须承认，由于历史积累的原因，在AI这一块儿Rust的影响力还非常小。但从另一方面来讲呢，Rust是目前业界除Python、C++ 外，唯一有潜力在未来20年的AI 发展中发挥重要作用的语言了。为什么这么说呢？

首先Rust的性能与C/C++一致，并且在调用GPU能力方面也同样方便；其次，Rust强大的表达能力，不输于Python，这让人们使用Rust做业务并不难；然后，Rust的cargo编译成单文件的能力，以及对WebAssembly完善的支持，部署应用的时候非常方便，这比Py + C/C++组合需要安装的一堆依赖和数G的库方便太多。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyhbzdkFM64Npva5ZKf4IPwhy6rDAX0L77QNESbalnXhnGKibcTbwtSaNC0hO6z0icO8DYI9Nf4xwg/132" width="30px"><span>eriklee</span> 👍（6） 💬（1）<div>&quot;首先 Rust 的性能与 C&#47;C++ 一致，并且在调用 GPU 能力方面也同样方便&quot;
rust目前应该还不能直接访问cuda吧？毕竟cuda是c接口</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/e1/c8/c7ed7336.jpg" width="30px"><span>听雨</span> 👍（2） 💬（1）<div>老师，我下载到了window下的子Linux中运行，报OS error。请问是不是不支持在这里面运行啊</div>2023-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/57/a3daeaae.jpg" width="30px"><span>tan</span> 👍（1） 💬（2）<div>wsl: Error: No such file or directory (os error 2) . 处理：simple.rs中 tikenizer和model的参数写全[&#47;mnt&#47;xx&#47;xx&#47;openchat_3.5_tokenizer.json]</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c8/33/2d4c464b.jpg" width="30px"><span>zhuxiufenghust</span> 👍（0） 💬（2）<div>avx: false, neon: false, simd128: false, f16c: false
Error: unknown magic 0x6f64213c 这个错误要怎么解决</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/07/93/710c7ee2.jpg" width="30px"><span>不忘初心</span> 👍（0） 💬（1）<div>老师, AI 电销, 需要什么样的技术栈?</div>2024-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ef/030e6d27.jpg" width="30px"><span>xl000</span> 👍（0） 💬（2）<div>candle-core 0.4版本, 只需要改两处
tensor.ggml_dtype.blck_size() 改为 tensor.ggml_dtype.block_size()
from_gguf(model, &amp;mut file)那行改为 
let device = Device::cuda_if_available(0)?;
let mut model = quantized_model::ModelWeights::from_gguf(model, &amp;mut file, &amp;device)?;</div>2024-03-20</li><br/><li><img src="" width="30px"><span>Geek_3b58b9</span> 👍（0） 💬（1）<div>Candle 要是支持 ROCm 就更好了</div>2024-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/57/a3daeaae.jpg" width="30px"><span>tan</span> 👍（0） 💬（1）<div>WSL: linker `cc` not found 处理方式： sudo apt update &amp;&amp; sudo apt install build-essential</div>2024-01-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyhbzdkFM64Npva5ZKf4IPwhy6rDAX0L77QNESbalnXhnGKibcTbwtSaNC0hO6z0icO8DYI9Nf4xwg/132" width="30px"><span>eriklee</span> 👍（0） 💬（1）<div>老师能对比下candle和burn吗？
另外，感觉rust优势是边缘端推理，毕竟边缘侧资源紧张. 服务器端推理，毕竟还是比不过python生态</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（0） 💬（1）<div>老师，请问一下，可以下载别人训练好的模型，通过candle 来实现根据需求描述自动生成测试用例的这种功能吗？</div>2024-01-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>mac 2021 款 intel 芯片， 系统版本 Montery 12.5.1 会卡住， model built 之后输入一个 hello 就不动了， 要过 5 分钟以上才会有回复</div>2024-01-02</li><br/><li><img src="" width="30px"><span>Geek_54dac1</span> 👍（0） 💬（1）<div>该模型在 Candle 中还暂时不支持在 GPU 上运行，因为 Quantized models on Cuda 还不支持，参考：https:&#47;&#47;github.com&#47;huggingface&#47;candle&#47;issues&#47;1250；避免大家挖坑</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/26/35ef9bef.jpg" width="30px"><span>无限可能</span> 👍（0） 💬（3）<div>老师好，大模型小白有几个问题。通过 huggingface-cli scan-cache，扫描了一下 huggingface 下载过的文件，都是 7G 或者更大：
1. 这些模型文件里主要是什么内容，是包括了数据么？为啥会这么大？
2. 类似这么大的文件，一定要下载到本地么，是否可以云部署之类，可以用完销毁。
3. 我理解，我想要运行本节课的demo，这 7G 的空间就是要长期规划出去了吧</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/06/f8/09ad484b.jpg" width="30px"><span>学水</span> 👍（0） 💬（1）<div>这张感觉主要是给对rust有兴趣的mle，中间一些代码如果不是因为用过pytorch，完全不知道在干啥</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>老师，你好，请问能否推荐几个和 ChatGPT 交互的 Rust SDK ? 最好也能支持其它 LLM 。</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b7/71/f0d3a1af.jpg" width="30px"><span>Yanxiao羅</span> 👍（1） 💬（0）<div>使用GPU加速遇到问题及处理记录

1、candle版本升级到0.4.0，api变化需要调整两处。参考上面评论

2、candle官网提示GPU开启需使用 `--features cuda` ，结合查看`Device::cuda_if_available(0)` 内部判断条件为读取配置 `config == cuda` 。首先修改代码中CPU的设置

114行、132行

```rust
&#47;&#47;使用Device::new_cuda(0)替换Device::CPU
let input = Tensor::new(&amp;[next_token], &amp;Device::new_cuda(0)?)?.unsqueeze(0)?;
```
执行后报找不到对应的命令features

3、`Cargo.toml` ，查看官方文档example配置，添加对应配置

```toml
[features]
cuda = [&quot;candle&#47;cuda&quot;, &quot;candle-nn&#47;cuda&quot;, &quot;candle-transformers&#47;cuda&quot;]
```

4、执行后包candle报错，原因为官网使用workspace，包含了`candle-core`、`candle-transformes`、`candle-nn`。这里我们需要单独配置

```toml
[dependencies]
anyhow = &quot;1.0.75&quot;
candle-core = { version = &quot;0.4.0&quot; }
candle-transformers = &quot;0.4.0&quot;
candle-nn = &quot;0.4.0&quot;
clap = &quot;4.4.10&quot;
hf-hub = &quot;0.3.2&quot;
tokenizers = &quot;0.15.0&quot;

[features]
cuda = [&quot;candle-core&#47;cuda&quot;, &quot;candle-nn&#47;cuda&quot;, &quot;candle-transformers&#47;cuda&quot;]
```

4、执行后报找不到CUDA环境变量，参考以下文章，记得先查看当前机器CUDA版本，去NVIDA官网下载对应的cuda

[windows下安装cuda和cudnn - 苍茫误此生博客 (cangmang.xyz)](https:&#47;&#47;cangmang.xyz&#47;articles&#47;1682852371010)

5、执行后报找不到`Cannot find compiler &#39;cl.exe&#39; in PATH`，根据stackoverflow上排查，配置Visual Studio的bin目录到环境变量。注意新版本路径与stackoverflow上最佳回答不同，找到对应位置，大致如下：

`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.23.28105\bin\Hostx64\x64`

6、执行后报

```rust
DriverError(CUDA_ERROR_NOT_FOUND, &quot;named symbol not found&quot;) when loading dequantize_block_q8_0
```

极客时间后续评论为candle不支持，考虑到评论时间为去年。继续google，candle github官网issue中有相应的回答，已处理并合并到主干，时间为2024年3月份。跟踪3月份后，离3月份最近版本为`0.5.0` （避免API变化大，未使用最新版本）。更新`cargo.toml` 

```toml
[dependencies]
candle-core = { version = &quot;0.5.0&quot; }
candle-transformers = &quot;0.5.0&quot;
candle-nn = &quot;0.5.0&quot;
```

7、执行成功。</div>2024-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f3/22/9090dfc8.jpg" width="30px"><span>HanStrong</span> 👍（0） 💬（0）<div>不使用gpu 3秒钟生成一个token 这是正常的速度么 还是跟电脑有关系</div>2024-06-03</li><br/>
</ul>