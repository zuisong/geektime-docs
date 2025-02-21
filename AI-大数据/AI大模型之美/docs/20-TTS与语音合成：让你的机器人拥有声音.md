你好，我是徐文浩。

上一讲里，我们通过Whisper模型，让AI“听懂”了我们在说什么。我们可以利用这个能力，让AI替我们听播客、做小结。不过，这只是我们和AI的单向沟通。那我们能不能更进一步，让AI不仅能“听懂”我们说的话，通过ChatGPT去回答我们问的问题，最后还能让AI把这些内容合成为语音，“说”给我们听呢？

当然可以，这也是我们这一讲的主题，我会带你一起来让AI说话。和上一讲一样，我不仅会教你如何使用云端API来做语音合成（Text-To-Speech），也会教你使用开源模型，给你一个用本地CPU就能实现的解决方案。这样，你也就不用担心数据安全的问题了。

## 使用Azure云进行语音合成

语音合成其实已经是一个非常成熟的技术了，现在在很多短视频平台里，你听到的很多配音其实都是通过语音合成技术完成的。国内外的各大公司都有类似的云服务，比如[科大讯飞](https://www.xfyun.cn/services/online_tts)、[阿里云](https://ai.aliyun.com/nls/tts)、[百度](https://ai.baidu.com/tech/speech/tts)、[AWS Polly](https://aws.amazon.com/cn/polly/)、[Google Cloud](https://cloud.google.com/text-to-speech)等等。不过，今天我们先来体验一下微软Azure云的语音合成API。选用Azure，主要有两个原因。

1. 因为微软和OpenAI有合作，Azure还提供了OpenAI相关模型的托管。这样，我们在实际的生产环境使用的时候，只需要和一个云打交道就好了。
2. 价格比较便宜，并且提供了免费的额度。如果你每个月的用量在50万个字符以内，那么就不用花钱。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/7c/12/7b9a2efb.jpg" width="30px"><span>胡萝卜</span> 👍（8） 💬（2）<div>这个英文转语音效果不错 https:&#47;&#47;github.com&#47;suno-ai&#47;bark</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（6） 💬（3）<div>尝试用百度的 PaddlePaddle，将语音文件(.wav) 转换成文字(语音识别)。

1. 语音中只含中文，实现代码如下:

from paddlespeech.cli.asr.infer import ASRExecutor
asr = ASRExecutor()
audio_file=&quot;.&#47;data&#47;BaiduTTS&#47;zh.wav&quot;
result = asr(audio_file=audio_file)
print(result)

输出结果:
我认为跑步最重要的就是给我带来了身体健康
语音原文:
我认为跑步最重要的就是给我带来了身体健康

2. 语音为中英文混合的文件 &quot;.&#47;data&#47;BaiduTTS&#47;paddlespeech_mix_1.wav&quot;，用上面的代码运行

输出结果: 
早上好哈沃尔姨百度他都斯一样能做中英文混合的语音合成
语音原文:
早上好, how are you? 百度 Paddle Speech 一样能做中英文混合的语音合成

处理中英文混合的语音文件，进行语音识别时，需要给 ASRExecutor() 添加参数，代码如下:

from paddlespeech.cli.asr import ASRExecutor
asr = ASRExecutor()
audio_file=&quot;.&#47;data&#47;BaiduTTS&#47;paddlespeech_mix_1.wav&quot;
result = asr(model=&#39;conformer_talcs&#39;, lang=&#39;zh_en&#39;, codeswitch=True, sample_rate=16000, audio_file=audio_file, config=None, ckpt_path=None, force_yes=False)
print(result)

输出结果:
早上好 how are you 百度它读 speech 一样能做中英文混合的语音合成

对照语音原文，ASRExecutor() 将语音 &quot;百度 Paddle Speech&quot; 转成了 &quot;百度它读 speech&quot;，并不完美。

期待更好的解决方案。

参考:
【PaddleSpeech】一键预测，快速上手Speech开发任务
https:&#47;&#47;aistudio.baidu.com&#47;aistudio&#47;projectdetail&#47;4353348?sUid=2470186&amp;shared=1&amp;ts=1660878142250

一文读懂 PaddleSpeech 中英混合语音识别技术
https:&#47;&#47;xie.infoq.cn&#47;article&#47;c05479afe4291255d91ed950f

Load specified model files for TTS cli #2225
https:&#47;&#47;github.com&#47;PaddlePaddle&#47;PaddleSpeech&#47;issues&#47;2225

PaddlePaddle&#47;PaddleSpeech
https:&#47;&#47;github.com&#47;PaddlePaddle&#47;PaddleSpeech&#47;blob&#47;develop&#47;demos&#47;audio_tagging&#47;README_cn.md
</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（2） 💬（3）<div>openai本身没有tts的api吗？期待下一讲。</div>2023-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/aa/54/bf64d522.jpg" width="30px"><span>劉仲仲</span> 👍（0） 💬（1）<div>老师，为甚么我用Azure语音服务，在jupyter notebook上已经跑通而且可以播放声音，但是一部署到hugging face上面就发不出声音呢</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/21/14/423a821f.jpg" width="30px"><span>Steven</span> 👍（0） 💬（1）<div>补充 Windows 下安装 portaudio 库：
1，下载安装 MSYS2：
     https:&#47;&#47;www.msys2.org&#47;
2，MSYS2 安装完成后在其命令行窗口中执行：
     pacman -S mingw-w64-x86_64-portaudio
</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/4e/82e9657c.jpg" width="30px"><span>jeff</span> 👍（1） 💬（1）<div>除去 PaddleSpeech 还有其他成熟方案吗？适合生产用的</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/4e/82e9657c.jpg" width="30px"><span>jeff</span> 👍（0） 💬（0）<div>M1 芯片可以跑起来 paddleSpeech 吗？
</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/4e/82e9657c.jpg" width="30px"><span>jeff</span> 👍（0） 💬（0）<div>paddlepaddle 在 colab 安装失败....</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/27/7c/aefc1ae2.jpg" width="30px"><span>蓝胖子</span> 👍（0） 💬（0）<div>老师，有没有克隆声音的比较好的开源库推荐，类似 MockingBird 的？</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（1）<div>老师，PaddleSpeech  转换语音很慢，有没有什么好办法</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（0）<div>老师，colab 安装pyaudio 报错ERROR: Could not build wheels for pyaudio, which is required to install pyproject.toml-based projects。是不是colab 不能安装pyaudio，老师您没有写colab或者类centos下安装portaudio的命令</div>2023-06-05</li><br/>
</ul>