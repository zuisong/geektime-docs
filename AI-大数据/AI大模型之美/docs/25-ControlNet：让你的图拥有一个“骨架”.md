你好，我是徐文浩。

上一讲，我们体验了Stable Diffusion这个时下最流行的开源“AI画画”项目，不知道你有没有试着用它画一些你想要的图片呢？不过，如果仅仅是使用预训练好的模型来画图的话，我们对于画出来的图还是缺少必要的控制。这会出现一个常见的问题：我们只能通过文本描述来绘制一张图片，但是具体的图片很有可能和你脑海中想象的完全不一样。

尽管我们可以通过img2img的方式，提供一张底图来对图片产生一定的控制，但是实际你多尝试一下就会发现这样的控制不太稳定，随机性很强。

对于这个问题，繁荣的Stable Diffusion社区也很快给出了回应，就是今天我们要介绍的项目ControlNet。ControlNet是在Stable Diffusion的基础上进行优化的一个开源项目，它既对原本的模型架构进行了修改，又在此基础上进行了进一步地训练，提供了一系列新的模型供你使用。

## 体验使用ControlNet模型

那么，接下来我们就先来看看如何使用ControlNet。我们还是需要Colab这样的GPU环境，并且安装好一系列依赖包。

```plain
%pip install diffusers transformers xformers accelerate
%pip install opencv-contrib-python
%pip install controlnet_aux
```
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/d2/dc2ac260.jpg" width="30px"><span>wd</span> 👍（0） 💬（0）<div>这一讲里用到的 xformers 模块不支持 Mac，只能在 Windows 和 Linux 环境运行。参见这个讨论：https:&#47;&#47;github.com&#47;facebookresearch&#47;xformers&#47;issues&#47;740#issuecomment-1594080277

老师是不是可以在文章开头给出一些警告？</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（3） 💬（4）<div>利用 cv2 对图片边缘检测的功能，妥妥地将书法图变成了拓片图。再加上 Stable Diffusion 1.5 模型，pipeline 出来意想不到的铜版雕刻。

1. 书法图片变拓片

在百度百科上选了一幅宋徽宗的瘦金体供学习用，链接如下
image_file = &quot;https:&#47;&#47;bkimg.cdn.bcebos.com&#47;pic&#47;9f510fb30f2442a7f49178c1da43ad4bd1130232?x-bce-process=image&#47;watermark,image_d2F0ZXIvYmFpa2U4MA==,g_7,xp_5,yp_5&quot;
也可使用自己的图片。
宋徽宗牡丹诗的真迹收藏于台北故宫博物院，宋代墨寶　冊　宋徽宗書牡丹詩，链接如下:
https:&#47;&#47;digitalarchive.npm.gov.tw&#47;Image&#47;Stream?ImageId=522542&amp;code=435965022&amp;maxW=600&amp;maxH=600

调用函数 get_canny_image，参数调整为 low_threshold=200 和 high_threshold=300
original_image = load_image(image_file)
canny_image = get_canny_image(original_image)

然后显示生成的 canny_image，徽宗瘦金体拓片。

2. 铜版雕刻

依然用四个电影明星的名字作为提示词

prompt = &quot;, a close up portrait photo, best quality, extremely detailed&quot;
prompt = [t + prompt for t in [&quot;Audrey Hepburn&quot;, &quot;Elizabeth Taylor&quot;, &quot;Scarlett Johansson&quot;, &quot;Taylor Swift&quot;]]
generator = [torch.Generator(device=&quot;cpu&quot;).manual_seed(42) for i in range(len(prompt))]

output = pipe(
    prompt,
    canny_image,
    negative_prompt=[&quot;monochrome, lowres, bad anatomy, worst quality, low quality&quot;] * 4,
    num_inference_steps=20,
    generator=generator,
)

显示最后&quot;卷&quot;出来的结果:
draw_image_grids(output.images, 2, 2)

---------------
用 Scarlett Johanssona ... 生成的铜版字最清晰，字体突起明显。用不同的提示词，会有不同的展现。
AI 千变万化，无限可能。这里只是沧海一粟。

什么模型能够拆解中文字体的笔画顺序? 利用这类模型就有可能AI视频书法写起来。</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/74/7861f504.jpg" width="30px"><span>马听</span> 👍（0） 💬（1）<div>image_file = &quot;https:&#47;&#47;hf.co&#47;datasets&#47;huggingface&#47;documentation-images&#47;resolve&#47;main&#47;diffusers&#47;input_image_vermeer.png&quot;original_image = load_image(image_file)
这一行代码有误，多了original_image = load_image(image_file)</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/27/bca407e1.jpg" width="30px"><span>caicongyang</span> 👍（0） 💬（0）<div>买了很久才看到这篇，徐老师很用心</div>2024-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/4a/601fcbae.jpg" width="30px"><span>红烧肉</span> 👍（0） 💬（0）<div>有输出一段话，可以同时生成多张图嘛</div>2024-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>老师很奇怪自己找的图片则不可以生成骨骼图为什么呢？</div>2023-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/99/17/e25c3884.jpg" width="30px"><span>Eric.Sui</span> 👍（0） 💬（0）<div>敬仰，老师方便加V吗？</div>2023-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/94/e89ebc50.jpg" width="30px"><span>神毓逍遥</span> 👍（0） 💬（0）<div>哈哈哈</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/34/3f/4b6cd370.jpg" width="30px"><span>Viktor</span> 👍（0） 💬（3）<div>这个技术的出现，被很多骗子利用，用来生成各种图片用来注册那些需要真人照片的网站。</div>2023-05-08</li><br/>
</ul>