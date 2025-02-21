你好，我是独行。

前面听我讲了这么多，相信你也很想上手试一试了。从这节课开始，我们进入一个新的章节，这部分我们会学习如何部署开源大模型ChatGLM3-6B，本地搭建向量库并结合LangChain做检索增强（RAG），并且我会带你做一次微调，从头学习**大模型的部署、微调、推理**等过程。

这节课我们就来讲一下如何本地化部署ChatGLM3-6B（后面我们简称为6B）。讲6B之前我们先整体看一下目前国内外大模型的发展状况，以便我们进行技术选型。

## 大模型的选择

当前环境下，大模型百花齐放。我筛选出了一些核心玩家，你可以看一下表格。非核心的其实还有很多，这里我就不一一列举了。厂商虽然很多，但真正在研究技术的没多少，毕竟前面我们讲过，玩大模型投入非常大，光看得见的成本，包括人才、训练和硬件费用，一年就得投入几个亿，不是一般玩家能玩得起的。

![图片](https://static001.geekbang.org/resource/image/a4/a0/a4e540e0b41d3d58e2cec92ae15d38a0.png?wh=2532x1340)

当然，也有不少厂商是基于LLaMA爆改的，或者叫套壳，不是真正意义上的自研大模型。

ChatGLM-6B和LLaMA2是目前开源项目比较热的两个，早在2023年年初，国内刚兴起大模型热潮时，智谱AI就开源了ChatGLM-6B，当然130B也可以拿过来跑，只不过模型太大，需要比较多的显卡，所以很多人就部署6B试玩。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（15） 💬（1）<div>1. 网络问题，可以用国内的地址，https:&#47;&#47;gitee.com&#47;mirrors&#47;chatglm3和 https:&#47;&#47;www.modelscope.cn&#47;ZhipuAI&#47;chatglm3-6b.git，注意不要用 hf 的，模型不全报错
2. 显卡驱动问题，需要把N 卡驱动最低升级到11.8，要先卸载干净旧驱动，再升级。
3. chatglm 如果没有找到 GPU，就会使用 CPU 运算，响应速度会非常慢，用 TOP 查看 CPU 使用率
4. 注意 cuda 版本和pytorch的版本一定要匹配，这里我踩了坑</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/dd/f2/3513c633.jpg" width="30px"><span>张 ·万岁！</span> 👍（8） 💬（1）<div>现在是24年7月15，刚刚结束这个模型部署模块。我使用的是阿里云的PAI平台，如果有人和我一样希望我能帮到你们。
1.git clone https:&#47;&#47;github.com&#47;THUDM&#47;ChatGLM3换成git clone https:&#47;&#47;gitee.com&#47;mirrors&#47;chatglm3。因为阿里云不支持HF
2.下载模型不要用git clone https:&#47;&#47;huggingface.co&#47;THUDM&#47;chatglm3-6b，我尝试过各种各样的lfs，都不好用。先pip install modelscope，然后使用python代码from modelscope import snapshot_download
model_dir = snapshot_download(&quot;ZhipuAI&#47;chatglm3-6b&quot;, revision = &quot;v1.0.0&quot;)，他会下载到cache区，使用linux基本指令移过来就好
3.MODEL_PATH = os.environ.get(&#39;MODEL_PATH&#39;, &#39;..&#47;model&#39;)这里，一定要用绝对地址！！！！
4.UnicodeDecodeError: &#39;utf-8&#39; codec can&#39;t decode byte 0xe8 in position 24: invalid continuation byte如果有编码问题，命令行改编码export LANGUAGE=en_US.UTF-8，因为他一开始是zh_CN.UTF-8，一定要改成en_US.UTF-8。输入locale检查一下，确保都是en_US.UTF-8
5.使用综合web那个案例中，记得去client中改一下# MODEL_PATH = os.environ.get(&#39;MODEL_PATH&#39;, &#39;THUDM&#47;chatglm3-6b&#39;)
MODEL_PATH = os.environ.get(&#39;MODEL_PATH&#39;, &#39;&#47;mnt&#47;workspace&#47;modelscope&#47;hub&#47;ZhipuAI&#47;chatglm3-6b&#39;)
而且，这里transformers和huggingface_hub版本不能太高，我的transformer是4.30.2，huggingface_hub是0.19.0</div>2024-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/8f/80443115.jpg" width="30px"><span>微笑的向日葵</span> 👍（5） 💬（2）<div>我本地跑起来了   redmi G 2020  Windows 环境 ，  显卡： RTX 3060 laptop  参考 的是 
https:&#47;&#47;www.bilibili.com&#47;video&#47;BV1ce411J7nZ&#47;?p=33&amp;spm_id_from=pageDriver&amp;vd_source=c16aa13fad5b13a7c51efcfcad58e883

https:&#47;&#47;www.bilibili.com&#47;read&#47;cv29866295&#47;

很详细 </div>2024-07-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/xfclWEPQ7szTZnKqnX9icSbgDWV0VAib3Cyo8Vg0OG3Usby88ic7ZgO2ho5lj0icOWI4JeJ70zUBiaTW1xh1UCFRPqA/132" width="30px"><span>Geek_6bdb4e</span> 👍（3） 💬（1）<div>国产也能成为推荐理由吗</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/44/0ec958f4.jpg" width="30px"><span>Eleven</span> 👍（2） 💬（1）<div>大模型的参数指的是在模型训练过程中需要学习和确定的变量或数值。这些参数决定了模型如何处理输入数据并生成相应的输出。在深度学习和自然语言处理领域，模型的参数数量通常与模型的复杂性和功能强大程度有关。</div>2024-06-12</li><br/><li><img src="" width="30px"><span>Geek_5203b4</span> 👍（2） 💬（1）<div>学习打卡~想请教老师一个问题，temperature和top_p对生成的结果影响大吗？如何测试到最佳的数值呢？谢谢老师！</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/96/23/a5cd0e1b.jpg" width="30px"><span>go home</span> 👍（1） 💬（1）<div>爲什麽不用LLaMA3呢，它在推理上面更加具有優勢。</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（1） 💬（1）<div>「如果你的电脑有 GPU，但是显存不够，也可以通过修改模型加载脚本，在 4-bit 量化下运行，只需要 6GB 左右的显存就可以进行流程推理。」如果没有GPU呢，怎么跑量化？

win本，32G mem，纯cpu 跑还是挺吃力的，速度慢到怀疑人生。今天折腾了下使用 chatglm.cpp 成功部署了量化版，速度杠杠滴。</div>2024-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/44/0ec958f4.jpg" width="30px"><span>Eleven</span> 👍（1） 💬（5）<div>RuntimeError: Internal: could not parse ModelProto from ..&#47;model&#47;tokenizer.model</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>第4讲打卡~
关于思考题，问了下ChatGPT，回答如下：
大模型的参数指的是模型中的可调整的变量，这些变量决定了模型如何处理输入数据并生成输出。在人工智能和机器学习中，参数是模型学习和适应新数据的关键部分。常见的参数如权重（w）和偏置（b）。</div>2024-06-12</li><br/><li><img src="" width="30px"><span>Geek_0a4616</span> 👍（0） 💬（1）<div>老师 大模型 最终推理出来的是个数字，数字和词汇的映射关系 是存在权重文件 https:&#47;&#47;huggingface.co&#47;THUDM&#47;chatglm3-6b 里面的吗？</div>2024-09-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJVo4SoLPrD4iauzuPMy4F63fsUhicZTeGbYrQTc9rB1kkMgoSGgTgxkLCRSKbFc0GicXBwq4hU9tH4EClnwWIYrp6ARalcvayQiauzWlZrQS0GAA/132" width="30px"><span>赵鹏</span> 👍（0） 💬（1）<div>pip3 install -r requirements.txt 执行报错，日志如下，请问如何解决？谢谢！

  ERROR: Command errored out with exit status 1:
   command: &#47;Library&#47;Developer&#47;CommandLineTools&#47;usr&#47;bin&#47;python3 &#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;pip&#47;_vendor&#47;pep517&#47;in_process&#47;_in_process.py get_requires_for_build_wheel &#47;var&#47;folders&#47;d_&#47;zyrnlk3j65l1rrm5vlz_khnm0000gn&#47;T&#47;tmpi1loqnkg
       cwd: &#47;private&#47;var&#47;folders&#47;d_&#47;zyrnlk3j65l1rrm5vlz_khnm0000gn&#47;T&#47;pip-install-axuijjbp&#47;vllm_bde8e7d4069844fcbf5e5312fb56958f
  Complete output (20 lines):
  fatal: not a git repository (or any of the parent directories): .git
  setup.py:56: RuntimeWarning: Failed to get commit hash:
  Command &#39;[&#39;git&#39;, &#39;rev-parse&#39;, &#39;HEAD&#39;]&#39; returned non-zero exit status 128.
    embed_commit_hash()
  Traceback (most recent call last):
    File &quot;&#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;pip&#47;_vendor&#47;pep517&#47;in_process&#47;_in_process.py&quot;, line 349, in &lt;module&gt;
      main()
    File &quot;&#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;pip&#47;_vendor&#47;pep517&#47;in_process&#47;_in_process.py&quot;, line 331, in main
      json_out[&#39;return_val&#39;] = hook(**hook_input[&#39;kwargs&#39;])
    File &quot;&#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;pip&#47;_vendor&#47;pep517&#47;in_process&#47;_in_process.py&quot;, line 117, in get_requires_for_build_wheel
      return hook(config_settings)
    File &quot;&#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;setuptools&#47;build_meta.py&quot;, line 154, in get_requires_for_build_wheel
      return self._get_build_requires(
    File &quot;&#47;Library&#47;Developer&#47;CommandLineTools&#47;Library&#47;Frameworks&#47;Python3.framework&#47;Versions&#47;3.9&#47;lib&#47;python3.9&#47;site-packages&#47;setuptools&#47;build_meta.py&quot;, line 135, in _get_build_requires</div>2024-08-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4Tkl5dibyG2Wriah2P5FR2dib3KiarXOmoVONicO2yGkoDwLtC0XIjYCiaziaEjYTte3cOuAdxAv5xkCNGdYq841DZePI/132" width="30px"><span>废物点心的黄金时代</span> 👍（0） 💬（1）<div>为啥不直接用ollama部署本地模型呢？</div>2024-07-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1G2rlRgNalXbcUnHibRNMibAeHQhWoKNl4e4EgkiawDynZZiaO4W3vSSMtlYEKrt6e7GW4mcu1sjcs7bGKjl0vRhWQ/132" width="30px"><span>Twein</span> 👍（0） 💬（1）<div>执行pip install -r requirements.txt报错：Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─&gt; [20 lines of output]
      Traceback (most recent call last):
        File &quot;D:\tools\python\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py&quot;, line 353, in &lt;module&gt;
          main()
        File &quot;D:\tools\python\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py&quot;, line 335, in main
          json_out[&#39;return_val&#39;] = hook(**hook_input[&#39;kwargs&#39;])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File &quot;D:\tools\python\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py&quot;, line 118, in get_requires_for_build_wheel
          return hook(config_settings)
                 ^^^^^^^^^^^^^^^^^^^^^
        File &quot;C:\Users\twein\AppData\Local\Temp\pip-build-env-y57aktmf\overlay\Lib\site-packages\setuptools\build_meta.py&quot;, line 327, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File &quot;C:\Users\twein\AppData\Local\Temp\pip-build-env-y57aktmf\overlay\Lib\site-packages\setuptools\build_meta.py&quot;, line 297, in _get_build_requires
          self.run_setup()
        File &quot;C:\Users\twein\AppData\Local\Temp\pip-build-env-y57aktmf\overlay\Lib\site-packages\setuptools\build_meta.py&quot;, line 313, in run_setup
          exec(code, locals())
        File &quot;&lt;string&gt;&quot;, line 12, in &lt;module&gt;
        File &quot;C:\Users\twein\AppData\Local\Temp\pip-build-env-y57aktmf\overlay\Lib\site-packages\torch\__init__.py&quot;, line 143, in &lt;module&gt;
          raise err
      OSError: [WinError 126] 找不到指定的模块。 Error loading &quot;C:\Users\twein\AppData\Local\Temp\pip-build-env-y57aktmf\overlay\Lib\site-packages\torch\lib\fbgemm.dll&quot; or one of its dependencies.
</div>2024-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/d9/9058e13c.jpg" width="30px"><span>黄蓉 Jessie</span> 👍（0） 💬（3）<div>MAC M2 pro的电脑安装ChatGLM3的依赖报错， AssertionError: vLLM only supports Linux platform (including WSL).应该是vllm这个包不支持</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/8f/80443115.jpg" width="30px"><span>微笑的向日葵</span> 👍（0） 💬（1）<div>我的电脑是 redmi G 2020  RTX 3060 laptop  </div>2024-07-06</li><br/><li><img src="" width="30px"><span>Geek_e9e5f5</span> 👍（0） 💬（1）<div>老师请教您个问题，大模型本地部署的情况，再部署动作结束后，只是部署了大模型代码呢？还是也包括大模型训练之后它拥有的所有记忆知识节点（这块不知道这么描述是不是准确）</div>2024-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（1）<div>请问下载的模型和下载的代码有什么区别</div>2024-07-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erG6I79WlHDjs51JOff9GBibD4Fh2PhITQMvmh2aTUVzH2BKia1tFLLoQr7VFeZddywwRoZlVUyhDDQ/132" width="30px"><span>Geek_frank</span> 👍（0） 💬（1）<div>打卡第四课。 大模型的本地部署使用源码本地部署可以是可以，但是感觉就是太麻烦。是不是可以用ollama这种工具来托管大模型，部署和运行都由ollama来实现。而且可以实现不同模型的切换</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/24/14/4b9add72.jpg" width="30px"><span>夏龙飞</span> 👍（0） 💬（2）<div>安装模型之后，这个报错咋搞啊
root@autodl-container-966c4d9eb4-c83428bd:~&#47;chatglm&#47;chatglm3&#47;basic_demo# python cli_demo.py
Traceback (most recent call last):
  File &quot;cli_demo.py&quot;, line 8, in &lt;module&gt;
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;transformers&#47;models&#47;auto&#47;tokenization_auto.py&quot;, line 847, in from_pretrained
    return tokenizer_class.from_pretrained(
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;transformers&#47;tokenization_utils_base.py&quot;, line 2089, in from_pretrained
    return cls._from_pretrained(
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;transformers&#47;tokenization_utils_base.py&quot;, line 2311, in _from_pretrained
    tokenizer = cls(*init_inputs, **init_kwargs)
  File &quot;&#47;root&#47;.cache&#47;huggingface&#47;modules&#47;transformers_modules&#47;chatglm3-6b&#47;tokenization_chatglm.py&quot;, line 109, in __init__    self.tokenizer = SPTokenizer(vocab_file)
  File &quot;&#47;root&#47;.cache&#47;huggingface&#47;modules&#47;transformers_modules&#47;chatglm3-6b&#47;tokenization_chatglm.py&quot;, line 18, in __init__
    self.sp_model = SentencePieceProcessor(model_file=model_path)
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;sentencepiece&#47;__init__.py&quot;, line 468, in Init
    self.Load(model_file=model_file, model_proto=model_proto)
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;sentencepiece&#47;__init__.py&quot;, line 961, in Load
    return self.LoadFromFile(model_file)
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.8&#47;site-packages&#47;sentencepiece&#47;__init__.py&quot;, line 316, in LoadFromFile
    return _sentencepiece.SentencePieceProcessor_LoadFromFile(self, arg)
RuntimeError: Internal: could not parse ModelProto from ..&#47;chatglm3-6b&#47;tokenizer.model</div>2024-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/ab/7ba4218a.jpg" width="30px"><span>JACOB</span> 👍（0） 💬（1）<div>本文介绍了单机部署非常好，请问分布式部署怎么搞，多机多GPU</div>2024-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELtOO0HKrj5SI5JSlmwiaCvaF6GLiaTmf5NX88OZaO3HymTAGTeIoicBUjqzmMF6sF5raPFjuqLFibrrw/132" width="30px"><span>gesanri</span> 👍（0） 💬（1）<div>请问下，这篇文章里举的例子，和gpt进行对话也需要gpu吗？还是说训练和微调的时候才需要gpu呢？</div>2024-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/02/6f/7e125dd5.jpg" width="30px"><span>元气🍣 🇨🇳</span> 👍（0） 💬（5）<div>操作系统必须是Linux 环境吗？windows 行不行？</div>2024-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/a2/f9efd9dc.jpg" width="30px"><span>春和景明</span> 👍（0） 💬（1）<div>root@eais-bjeg6jkdvfi9w77spgwf-cc9d4cd9f-9n8q6:&#47;mnt&#47;workspace&#47;ChatGLM3# python basic_demo&#47;cli_demo.py 
Loading checkpoint shards: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7&#47;7 [00:03&lt;00:00,  2.01it&#47;s]
欢迎使用 ChatGLM3-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序

用户：你是谁

ChatGLM：2024-06-21 17:02:25.171267: I tensorflow&#47;core&#47;platform&#47;cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2024-06-21 17:02:26.264294: W tensorflow&#47;compiler&#47;tf2tensorrt&#47;utils&#47;py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
Traceback (most recent call last):
  File &quot;&#47;mnt&#47;workspace&#47;ChatGLM3&#47;basic_demo&#47;cli_demo.py&quot;, line 59, in &lt;module&gt;
    main()
  File &quot;&#47;mnt&#47;workspace&#47;ChatGLM3&#47;basic_demo&#47;cli_demo.py&quot;, line 45, in main
    for response, history, past_key_values in model.stream_chat(tokenizer, query, history=history, top_p=1,
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;torch&#47;utils&#47;_contextlib.py&quot;, line 35, in generator_context
    response = gen.send(None)
  File &quot;&#47;root&#47;.cache&#47;huggingface&#47;modules&#47;transformers_modules&#47;chatglm3-6b&#47;modeling_chatglm.py&quot;, line 1075, in stream_chat
    response = tokenizer.decode(outputs)
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;transformers&#47;tokenization_utils_base.py&quot;, line 3809, in decode
.....
UnicodeDecodeError: &#39;ascii&#39; codec can&#39;t decode byte 0xe6 in position 0: ordinal not in range(128)</div>2024-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/19/29/4a8214b7.jpg" width="30px"><span>Bug Killer</span> 👍（0） 💬（3）<div>执行pip install -r requirements.txt 一直报错
Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─&gt; [18 lines of output]
      Traceback (most recent call last):
        File &quot;&#47;Users&#47;liuga&#47;ai&#47;ChatGLM3&#47;path&#47;to&#47;venv&#47;lib&#47;python3.12&#47;site-packages&#47;pip&#47;_vendor&#47;pyproject_hooks&#47;_in_process&#47;_in_process.py&quot;, line 353, in &lt;module&gt;
          main()
        File &quot;&#47;Users&#47;liuga&#47;ai&#47;ChatGLM3&#47;path&#47;to&#47;venv&#47;lib&#47;python3.12&#47;site-packages&#47;pip&#47;_vendor&#47;pyproject_hooks&#47;_in_process&#47;_in_process.py&quot;, line 335, in main
          json_out[&#39;return_val&#39;] = hook(**hook_input[&#39;kwargs&#39;])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File &quot;&#47;Users&#47;liuga&#47;ai&#47;ChatGLM3&#47;path&#47;to&#47;venv&#47;lib&#47;python3.12&#47;site-packages&#47;pip&#47;_vendor&#47;pyproject_hooks&#47;_in_process&#47;_in_process.py&quot;, line 118, in get_requires_for_build_wheel
          return hook(config_settings)
                 ^^^^^^^^^^^^^^^^^^^^^
        File &quot;&#47;private&#47;var&#47;folders&#47;nb&#47;kdvtrmzj52q1c5pq4brf50y00000gp&#47;T&#47;pip-build-env-arr1_sd0&#47;overlay&#47;lib&#47;python3.12&#47;site-packages&#47;setuptools&#47;build_meta.py&quot;, line 325, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[&#39;wheel&#39;])
</div>2024-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/f2/41f3907d.jpg" width="30px"><span>jimmy</span> 👍（0） 💬（3）<div>不支持MAC M3Pro本地部署,安装依赖时错误信息 AssertionError: vLLM only supports Linux platform (including WSL).</div>2024-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/16/65/ae88c7ad.jpg" width="30px"><span>任帅兵</span> 👍（1） 💬（1）<div>requirements.txt 中有一个 vllm&gt;=0.4.2，这个包安装时报错：

AssertionError: vLLM only supports Linux platform (including WSL).

搜索了一下这个包目前不支持windows环境，请问一下这个该如何解决啊？</div>2024-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/5d/b4/9d2c2e03.jpg" width="30px"><span>Percy Hon</span> 👍（0） 💬（1）<div>我在AWS的EC2上部署的，实例规格是16核，64GiB内存，显卡是NVIDIA T4 Tensor Core GPUs。部署没问题，但是整个应答过程非常慢，大概一分钟生成一个字</div>2025-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/2c/180075e0.jpg" width="30px"><span>小豪</span> 👍（0） 💬（0）<div>我是4070s的显卡
第一次跑的时候，模型加载代码如下：
AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map=&quot;auto&quot;).eval()
运行起来后，终端会显示：“Some parameters are on the meta device because they were offloaded to the cpu”, 并且推理速度比较慢，怀疑是在用CPU进行推理。
第二次把device_map改成了&quot;cuda&quot;：
AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map=&quot;cuda&quot;).eval()
推理速度明显加快了
这是什么原因呢</div>2025-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/ca/6173350b.jpg" width="30px"><span>神奇小懒懒</span> 👍（0） 💬（0）<div>使用glm-4-9b-chat模型。需要10G显存。
在Intel(R) Core(TM) i5-10500 CPU
32g内存
3060 12G显卡的情况下异常卡顿</div>2025-01-16</li><br/>
</ul>