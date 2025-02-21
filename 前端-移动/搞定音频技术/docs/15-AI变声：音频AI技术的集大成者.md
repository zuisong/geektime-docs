你好，我是建元。

AI技术在音频领域发展十分迅速。除了我们之前讲的降噪、回声消除以及丢包补偿等方向可以用AI模型来提升音质听感之外，AI模型还有很多有趣的应用。其中比较常见的有ASR（Automatic Speech Recognition）可以理解为语音转文字，TTS（Text To Speech）文字转语音和VPR（Voice Print Recognition）声纹识别等。

在之前讲音效算法的时候，我们知道，要做到变声需要改变整个语音信号的基频，还需要改变语音的音色。传统算法是通过目标语音和原始语音，计算出基频差距和频谱能量分布的差异等特征，然后使用变调、EQ等方法来对语音进行调整，从而实现变声（Voice Conversition，VC）。

但这些特征的差异，在发不同的音，不同的语境中可能都是不一样的。如果用一个平均值来进行整体语音的调整，你可能会发现有的音变声效果比较贴近目标语音，而有的音，可能会有比较大的偏离。**整体听感上就会觉得变声效果时好时坏。**

甚至由于某些发音在改变了频谱能量分布后，共振峰发生了较大改变，连原本想表达的语意都发生了变化。所以为了获得比较好的变声效果，我们需要实时对语音做动态的调整，而这使用传统算法显然是无法穷尽所有发音、语境的对应变化关系的。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（1） 💬（1）<div>为什么不引入延迟变声的效果就会变差呢？

因为说话有语境，有上下文，说话不止需要前参考，还需要后参考，人在说话时，大脑已经预先处理了，说出来就很自然，但是机器不知道你的下一句是什么？所以只能依据前参考，预测后参考，有偏差，自然度就比较差。</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/3d/ae41c2b3.jpg" width="30px"><span>data</span> 👍（0） 💬（0）<div>老师想问一下 微信长按发送语音功能使用什么技术实现的，有相关文章吗</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（0） 💬（0）<div>Ligusitic Decoding and search algorithm 这里 Ligusitic 是不是应该是 Linguistic</div>2022-05-22</li><br/>
</ul>