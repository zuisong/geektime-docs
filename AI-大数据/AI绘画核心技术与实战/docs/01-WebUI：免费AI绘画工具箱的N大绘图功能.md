你好，我是南柯。

欢迎和我一起探索AI绘画的魅力。热身篇这一章相当于整个学习过程里的“新手村”，我会带你一起熟悉各种各样免费开源的AI绘画工具和模型，帮助你全面掌握AI绘画的无限潜能。

今天是课程的第一讲，我们先从Stable Diffusion和WebUI说起。学完今天的内容，你不但能够知道Stable Diffusion的来龙去脉，还能解锁WebUI里的特色功能，来实现各种富有想象力的视觉创意。

## 初识WebUI

想必你一定听说过Stable Diffusion，其背后的技术便是人们常说的扩散模型。扩散模型这个概念源自热力学，在图像生成问题中得以应用。

简言之，Stable Diffusion是这样一个过程：你不妨想象一下，任何一张图像都可以通过不断添加噪声变成一张完全被噪声覆盖的图像；反过来，任何一张噪声图像通过逐步合理地去除噪声，变得清晰可辨。

Stable Diffusion（以下简称SD）在AI绘画领域中闪耀着耀眼的光芒，SD背后的方法在学术界被称为Latent Diffusion，论文发表于2022年计算机顶会CVPR，相关知识在后面的课程中我们会涉及，这里先按下不表。此时你只需要知道，SD模型可以输入文本，生成图像。这里提到的文本，就是我们常说的prompt。比如下面这张图，就是由SD模型生成的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>yanyu-xin</span> 👍（20） 💬（2）<div>在https:&#47;&#47;space.bilibili.com&#47;12566101下载了Stable Diffusion整合包，win版安装很简单。内置了很多模型和扩展，秋叶aaaki的一键启动器很好用。
我的MateBook笔记本只有内置显卡，在启动器性能设置选择硬件引擎为CPU后也能绘图，CPU绘图一幅图都要20多分钟左右。尝试一下新技术勉强可以，只是确实太慢了。
找了一个云算力市场，不用翻墙，价格低廉，国内的“揽睿星舟”。https:&#47;&#47;www.lanrui-ai.com&#47;register?invitation_code=1643301013。
该云在云应用市场中，直接内置了最新版的基于Stable Diffusion Web UI打包的应用。已预装所有依赖和常见模型，一键即可启动。如果家里有矿，可以直接选A100-80G显卡的。我选了特价3090-24G显卡，速度挺快。用来学习或者训练自己的小模型也是挺香的。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/a4/7a45d979.jpg" width="30px"><span>IT蜗壳-Tango</span> 👍（19） 💬（2）<div>Win11 搭建笔记：https:&#47;&#47;xie.infoq.cn&#47;article&#47;62e1d389d8a0c4c7638ba610d
Mac M1版本搭建笔记：https:&#47;&#47;xie.infoq.cn&#47;article&#47;5fd4d53d1ed467f51c4c7f7a2

Mac 的版本是很早前的笔记了，如果使用win11中的方法，大概率应该也不会再报那些奇怪的错误了。</div>2023-07-18</li><br/><li><img src="" width="30px"><span>Geek_ac422d</span> 👍（6） 💬（1）<div>推荐几个低成本体验ai绘画的方式：https:&#47;&#47;note.youdao.com&#47;s&#47;XwhBsykQ</div>2023-07-18</li><br/><li><img src="" width="30px"><span>互联网砖瓦匠</span> 👍（4） 💬（3）<div>我的3080终于要在AI这块排上用场了，不知道老师了解RTX4090对AI这块提升大不大。</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（2） 💬（2）<div>一次性安装成功，但是老师省略了耗时步骤，我说一下
1，win11 第一次运行webui.bat  会要安装 Installing torch and torchvision  （2.6GB） 耗时一会儿
2，前面成功，会要求更新pip ,根据提示操作python.exe -m pip install --upgrade pip
3，更新pip后， 再次运行webui.bat 则可以启动成功</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（2） 💬（1）<div>强调 prompt 的关键词 这个部分中，右边图片的指令，：a photo of boy with (((curly hair))), Greg Rutkowski

为什么是三个括号？不是一个括号？</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/72/63c94eee.jpg" width="30px"><span>黄马</span> 👍（2） 💬（1）<div>老师哪里有免费的GPU可以做实验</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/59/97/9b7a412c.jpg" width="30px"><span>Aā 阳～</span> 👍（1） 💬（2）<div>老师，生成出来得图片黑屏是什么原因啊</div>2023-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e0/c8/4ad13219.jpg" width="30px"><span>啥也不会</span> 👍（1） 💬（1）<div>麻烦请问老师，是否可以使用 java 来调用Stable Diffusion模型实现类似 WEBUI 的效果呢？没有检索到相关的资料。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/65/6016b046.jpg" width="30px"><span>清风明月</span> 👍（1） 💬（2）<div>webui是通过调用sd API还是自己本地集成了模型？</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ae/0f/4743bf1d.jpg" width="30px"><span>Short Hair Girl</span> 👍（0） 💬（1）<div>我可能比较小白，我就没看到这Python 3.10.6安装包再哪里找？</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（0） 💬（1）<div>Mac 执行.&#47;webui.sh 后终端提示Warning: caught exception &#39;Torch not compiled with CUDA enabled&#39;, memory monitor disabled,然后打开页面一堆报错提示这个Error
Expecting value: line 1 column 1 (char 0),请问老师这个怎么解决?</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/16/179e4fce.jpg" width="30px"><span>Zeke</span> 👍（0） 💬（1）<div>执行 .&#47;webui.sh后，Downloading torch-2.0.1-cp310-none-macosx_10_9_x86_64.whl 到一半报错
ERROR: Exception:
Traceback (most recent call last):
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;pip&#47;_vendor&#47;urllib3&#47;response.py&quot;, line 438, in _error_catcher
    yield
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;pip&#47;_vendor&#47;urllib3&#47;response.py&quot;, line 561, in read
    data = self._fp_read(amt) if not fp_closed else b&quot;&quot;
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;pip&#47;_vendor&#47;urllib3&#47;response.py&quot;, line 527, in _fp_read
    return self._fp.read(amt) if amt is not None else self._fp.read()
  File &quot;&#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;pip&#47;_vendor&#47;cachecontrol&#47;filewrapper.py&quot;, line 90, in read
    data = self.__fp.read(amt)
  File &quot;&#47;usr&#47;local&#47;Cellar&#47;python@3.10&#47;3.10.12_1&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.10&#47;lib&#47;python3.10&#47;http&#47;client.py&quot;, line 466, in read
    s = self.fp.read(amt)
  File &quot;&#47;usr&#47;local&#47;Cellar&#47;python@3.10&#47;3.10.12_1&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.10&#47;lib&#47;python3.10&#47;socket.py&quot;, line 705, in readinto
    return self._sock.recv_into(b)
  File &quot;&#47;usr&#47;local&#47;Cellar&#47;python@3.10&#47;3.10.12_1&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.10&#47;lib&#47;python3.10&#47;ssl.py&quot;, line 1274, in recv_into
    return self.read(nbytes, buffer)
  File &quot;&#47;usr&#47;local&#47;Cellar&#47;python@3.10&#47;3.10.12_1&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.10&#47;lib&#47;python3.10&#47;ssl.py&quot;, line 1130, in read
    return self._sslobj.read(len, buffer)
TimeoutError: The read operation timed out</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/16/4dd77397.jpg" width="30px"><span>a</span> 👍（0） 💬（1）<div>你好，我在M2版的MacbookPro上安装了webUI，但是生成一张图片需要两个多小时，是什么原因呢</div>2023-09-03</li><br/><li><img src="" width="30px"><span>谭小龙</span> 👍（0） 💬（1）<div>请问自己配置台式 AMD的主板和CPU对软件的支持怎么样呢，是否存在限制？哪些型号是由限制的？</div>2023-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/18/2af6bf4b.jpg" width="30px"><span>兔2🐰🍃</span> 👍（0） 💬（2）<div>生产过程中图片显示正常，一旦结束就会出现图片变成紫色的X光照片一样。请问老师，这是啥原因么？</div>2023-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/da/79/9b093890.jpg" width="30px"><span>大秦皇朝</span> 👍（0） 💬（1）<div>老师麻烦请教一下，webui一定需要Python v3.10.6吗？v3.10.0行吗？</div>2023-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e1/30/56151c95.jpg" width="30px"><span>徐大雷</span> 👍（0） 💬（2）<div>老师你好，我有个问题咨询一下，我在civitai里面选择的模型，然后在这个模型下面的gallery里面有很多图片，我点进去按照图片的提示词和采样方法等自己本地跑，为啥画出来的图片会不一样呢？谢谢老师的回复</div>2023-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（0） 💬（2）<div>发现一个常见的错误：NansException: A tensor with all NaNs was produced in VAE. This could be because there&#39;s not enough precision to represent the picture. Try adding --no-half-vae commandline argument to fix this. Use --disable-nan-check commandline argument to disable this check.  希望老师指点一下</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/21/53/41a08531.jpg" width="30px"><span>·幸</span> 👍（0） 💬（1）<div>venv &quot;D:\AIGC\stable-diffusion-webui-master\venv\Scripts\Python.exe&quot;
Python 3.10.6 (tags&#47;v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)]
Version: ## 1.4.1
Commit hash: &lt;none&gt;
Traceback (most recent call last):
  File &quot;D:\AIGC\stable-diffusion-webui-master\launch.py&quot;, line 38, in &lt;module&gt;
    main()
  File &quot;D:\AIGC\stable-diffusion-webui-master\launch.py&quot;, line 29, in main
    prepare_environment()
  File &quot;D:\AIGC\stable-diffusion-webui-master\modules\launch_utils.py&quot;, line 268, in prepare_environment
    raise RuntimeError(
RuntimeError: Torch is not able to use GPU; add --skip-torch-cuda-test to COMMANDLINE_ARGS variable to disable this check
请按任意键继续. . .


请问出现以上内容应该怎么解决？</div>2023-08-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ccCGDRLarBQWib8tSOpV4jgh7x86BjI4AjWWbaiaWuwzbibzh4OWU0IxvjVmvEhEkzCB8fn2CyJpauH7mSVAXQFVA/132" width="30px"><span>Geek_a7f70d</span> 👍（0） 💬（1）<div>这个课程没有视频直播吗？都是文字的？？
</div>2023-07-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKPjJg1rdQ0DyIlibflLQqE5k744wdHAwFOTBtGGwRoiar5AZMyBkoW3Mle30l8NZD6QibYeKOYRHdvA/132" width="30px"><span>Geek_336bd7</span> 👍（0） 💬（1）<div>Something went wrong
Expecting value: line 1 column 1 (char 0)
打开http:&#47;&#47;127.0.0.1:7860&#47;后，页面弹框出现这个问题</div>2023-07-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKPjJg1rdQ0DyIlibflLQqE5k744wdHAwFOTBtGGwRoiar5AZMyBkoW3Mle30l8NZD6QibYeKOYRHdvA/132" width="30px"><span>Geek_336bd7</span> 👍（0） 💬（2）<div>作者能有个ubuntu20.04 docker环境的安装方法么？？？？</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>很高兴老师的回复，也很想和老师讨论一下这个问题，希望编辑老师看见和老师说一下，先在此谢谢了。：网络上出现了一个秋叶的一键包，当然这不是重点，重点是：我一个朋友笔记本，显卡3080ti，显存6GB，在生成高分辨率的时候毫无压力（就是速度慢一点），但是不会失败，而我就直接报错，他说会不会是启动器的问题？但是显然我不是很理解这个提示，这也是我觉得可以讨论且有机会解决的。

我也查阅了 GitHub issue，但是并不能解决（有可能我的阅读能力不足）也希望老师能辅助解答一下，不然我感觉 1.6万买的整机有点拉垮，不知道是不是台式机的问题（联想）现在还支持七天无理由退换货），期待老师的回复。</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/a2/454fd9f0.jpg" width="30px"><span>Angelevil</span> 👍（0） 💬（1）<div>已经安装torch，执行.&#47;webui.sh 还是报错</div>2023-07-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDqDqBBy9yghEiaXicBCarEJFYKdToVTOY5l2bznG4BEKjJRFJCl3Zyia92EX4s9x812GyUZTRlAPOw/132" width="30px"><span>Geek_542548</span> 👍（0） 💬（1）<div>loading stable diffusion model: FileNotFoundError
FileNotFoundError: No checkpoints found. When searching for checkpoints, looked at:
 - file &#47;Users&#47;zhangyu&#47;workspace&#47;stable-diffusion-webui&#47;model.ckpt
 - directory &#47;Users&#47;zhangyu&#47;workspace&#47;stable-diffusion-webui&#47;models&#47;Stable-diffusionCan&#39;t run without a checkpoint. Find and place a .ckpt or .safetensors file into any of those locations.
这几个报错 影响使用吗</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/9c/25dea911.jpg" width="30px"><span>计划生肉</span> 👍（0） 💬（1）<div>MacPro 15年版，启动报如下错
Launching Web UI with arguments: --skip-torch-cuda-test --upcast-sampling --no-half-vae --use-cpu interrogate
No module &#39;xformers&#39;. Proceeding without it.
Warning: caught exception &#39;Torch not compiled with CUDA enabled&#39;, memory monitor disabled
Loading weights [6ce0161689] from &#47;Users&#47;cher&#47;ai&#47;webui&#47;new&#47;stable-diffusion-webui&#47;models&#47;Stable-diffusion&#47;v1-5-pruned-emaonly.safetensors
Exception in thread Thread-3 (first_time_calculation):
Traceback (most recent call last):
  File &quot;&#47;Users&#47;cher&#47;miniconda3&#47;lib&#47;python3.10&#47;threading.py&quot;, line 1016, in _bootstrap_inner
    self.run()
  File &quot;&#47;Users&#47;cher&#47;miniconda3&#47;lib&#47;python3.10&#47;threading.py&quot;, line 953, in run
    self._target(*self._args, **self._kwargs)
  File &quot;&#47;Users&#47;cher&#47;ai&#47;webui&#47;new&#47;stable-diffusion-webui&#47;modules&#47;devices.py&quot;, line 170, in first_time_calculation
    linear(x)
  File &quot;&#47;Users&#47;cher&#47;ai&#47;webui&#47;new&#47;stable-diffusion-webui&#47;venv&#47;lib&#47;python3.10&#47;site-packages&#47;torch&#47;nn&#47;modules&#47;module.py&quot;, line 1501, in _call_impl
    return forward_call(*args, **kwargs)
  File &quot;&#47;Users&#47;cher&#47;ai&#47;webui&#47;new&#47;stable-diffusion-webui&#47;extensions-builtin&#47;Lora&#47;lora.py&quot;, line 400, in lora_Linear_forward
    return torch.nn.Linear_forward_before_lora(self, input)
  File &quot;&#47;Users&#47;cher&#47;ai&#47;webui&#47;new&#47;stable-diffusion-webui&#47;venv&#47;lib&#47;python3.10&#47;site-packages&#47;torch&#47;nn&#47;modules&#47;linear.py&quot;, line 114, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: &quot;addmm_impl_cpu_&quot; not implemented for &#39;Half&#39;</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>老师这个后期能教学么：3D 骨架模型编辑 （3D Openpose）</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（3）<div>还有一个问题，希望老师解答：我的台式机：4070ti，显存12G，选择老师的模型，参数设置都一样。除了图片大小设置为1080、1080或2048、2040，均无法启动，都会报错。
OutOfMemoryError: CUDA out of memory. Tried to allocate 1.25 GiB (GPU 0; 11.99 GiB total capacity; 9.86 GiB already allocated; 0 bytes free; 10.28 GiB reserved in total by PyTorch) If reserved memory is &gt;&gt; allocated memory try setting max_split_size_mb to avoid fragmentation. See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
Time taken: 2.29sTorch active&#47;reserved: 10419&#47;10848 MiB, Sys VRAM: 12282&#47;12282 MiB (100.0%)
查不到资料，希望老师能帮忙解决一下。sos
</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>Batch count 和 Batch size 其中 Batch count 作者没有讲解，和 count 的区别呢？</div>2023-07-23</li><br/>
</ul>