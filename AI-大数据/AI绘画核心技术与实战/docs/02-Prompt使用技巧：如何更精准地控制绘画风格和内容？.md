你好，我是南柯。

之前我们解锁了Web UI的七大特色功能，如果拿烹饪来做比喻，前一讲的内容大概只是把菜做熟的程度，还无法产出“色香味”俱全的图像作品。实际应用的时候，你很可能遇到后面这些困扰。

- 图生图如何优化，如何生成具有特定特征或内容的图像？
- 输入了提示词，但AI模型不太“听话”，要怎么做参数调优？
- 怎样生成多样风格的图像作品？

这一讲我们就来解决这些问题，学习影响图像风格、内容和质量的重要参数。熟练掌握应用和优化这些参数的技巧以后，你就可以随心所欲地控制AI绘画的构图、内容和风格，制作出更符合自己心意的专属内容了。

## WebUI咒语指南：prompt入门

想要控制 **Stable Diffusion** 创作我们喜好的图像，熟练运用 **prompt**（提示词）至关重要。在开源社区中，prompt甚至因为对AI绘画的神秘影响，被赋予了“咒语”或“魔法”的称号。

不过prompt其实并没那么玄乎，学完它的使用方法和实用技巧以后，你也能成为AI绘画界的杰出“魔法师”。

### 初阶咒语：直接描述

prompt最简单且常见的用法，就是直接在prompt区域描述我们想要创作的图像，例如输入 `a happy dog and a cute girl`。通过这样的描述，我们可以生成后面这样的图像。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（11） 💬（3）<div>思考题:
如果你想绘制一幅精细化的人物肖像，AI 绘画生成的图像在手部和脸部细节存在瑕疵。这种情况下，有哪些方法可以改善这些问题？

我尝试了下面的提示词:

a beautiful women, medium shot, studio light, Realism Portrait

当使用 &quot;a utral detailed portrait of ...&quot; 时，效果与 &quot;close up&quot; 接近:
a utral detailed portrait of a beautiful women,

应对手部和脸部的瑕疵，使用了下面的负面提示词:

mutated hands, fused fingers, too many fingers, missing fingers, poorly drawn hands, blurry eyes, blurred iris, blurry face, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, out of frame, multiple faces, long neck, nsfw, 

请大家补充好的想法。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/a4/7a45d979.jpg" width="30px"><span>IT蜗壳-Tango</span> 👍（8） 💬（2）<div>介绍两个插件，方便小伙伴们更好的使用webui和提示词
http:&#47;&#47;gk.link&#47;a&#47;1277p</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（5） 💬（1）<div>找到一个还不错的提示词网站
https:&#47;&#47;stablediffusion.fr&#47;prompts</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/50/a4b2adf4.jpg" width="30px"><span>Guanpj</span> 👍（3） 💬（1）<div>prompt 中使用 lora 时文本必须与文件名一致吗？</div>2023-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/e6/9dd5c011.jpg" width="30px"><span>我就是我，烟火不一样的我</span> 👍（0） 💬（1）<div>盲盒使用的基础模型sd1.5是啥？在webui绘画的时候，上面基础模型选择啥？</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3e/90/c86ec4ca.jpg" width="30px"><span>Chengfei.Xu</span> 👍（0） 💬（2）<div>思考题（简易版）：
1、在webUI中发现有相关“面部修复”、“高清修复”功能
2、通过promet和negative promet尝试

——
另外作者的SD 基础模型选择为 realv1.3是怎么选择的，我的默认只能使用“v1-5-pruned-emaonly.safetensors”</div>2023-08-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ccCGDRLarBQWib8tSOpV4jgh7x86BjI4AjWWbaiaWuwzbibzh4OWU0IxvjVmvEhEkzCB8fn2CyJpauH7mSVAXQFVA/132" width="30px"><span>Geek_a7f70d</span> 👍（0） 💬（1）<div>希望可以教一下civitai和hugging face两个社区的使用方法</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/6b/a6a40607.jpg" width="30px"><span>刘泓呈</span> 👍（0） 💬（1）<div>我用的SD是整合安装包，后半篇的内容跟我使用的有点割裂了。。。</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>文中提到的1.1倍强度等，这些从哪里可以查询到？范围是什么？</div>2023-07-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlicd6xoiaozzsTEH0l2s4epW4zXacqmwAlOrVApGCSIIdReaKwibqxhicqvlEK2vh56sCDvVhEFOlLQ/132" width="30px"><span>Seeyo</span> 👍（0） 💬（1）<div>老师 请问一下后续会讲 stable diffusion的部署吗？找了一圈跟control net相关的量化资料 都没找到</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ad/09/36cdc274.jpg" width="30px"><span>永远积极向上的韩冬</span> 👍（0） 💬（1）<div>可以用局部重绘</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>期待下一节课。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5b/d7/d88c1850.jpg" width="30px"><span>和某欢</span> 👍（0） 💬（1）<div>希望老师再多增加一些关于 CFG Scale的讲解</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/4f/4c12de43.jpg" width="30px"><span>syp</span> 👍（3） 💬（0）<div>思考题：面部，手部瑕疵如何处理
re：常用方式
1.sd中开启面部修复
2.蒙版局部重绘
3.利用sd插件After Detailer（最推荐）</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/6c/3a2db6f7.jpg" width="30px"><span>学习吧技术储备</span> 👍（0） 💬（0）<div>有推荐的好书吗</div>2024-01-09</li><br/>
</ul>