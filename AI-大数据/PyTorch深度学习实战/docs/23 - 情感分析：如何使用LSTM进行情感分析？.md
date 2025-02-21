你好，我是方远。

欢迎来跟我一起学习情感分析，今天我们要讲的就是机器学习里的文本情感分析。文本情感分析又叫做观点提取、主题分析、倾向性分析等。光说概念，你可能会觉得有些抽象，我们一起来看一个生活中的应用，你一看就能明白了。

比方说我们在购物网站上选购一款商品时，首先会翻阅一下商品评价，看看是否有中差评。这些评论信息表达了人们的各种情感色彩和情感倾向性，如喜、怒、哀、乐和批评、赞扬等。像这样根据评价文本，由计算机自动区分评价属于好评、中评或者说差评，背后用到的技术就是情感分析。

如果你进一步观察，还会发现，在好评差评的上方还有一些标签，比如“声音大小合适”、“连接速度快”、“售后态度很好”等。这些标签其实也是计算机根据文本，自动提取的主题或者观点。

![](https://static001.geekbang.org/resource/image/ef/6f/ef69caa72565c50d98b63e20f499ea6f.jpg?wh=2572x2473)

情感分析的快速发展得益于社交媒体的兴起，自2000年初以来，情感分析已经成长为自然语言处理（NLP）中最活跃的研究领域之一，它也被广泛应用在个性化推荐、商业决策、舆情监控等方面。

今天这节课，我们将完成一个情感分析项目，一起来对影评文本做分析。

## 数据准备

现在我们手中有一批影评数据（IMDB数据集），影评被分为两类：正面评价与负面评价。我们需要训练一个情感分析模型，对影评文本进行分类。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（1） 💬（0）<div>如果是使用torchtext==0.8.1以下的版本建议看官网文档：
https:&#47;&#47;pytorch.org&#47;text&#47;0.8.1&#47;datasets.html</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/73/0b/0f918fa2.jpg" width="30px"><span>快乐小夜曲</span> 👍（1） 💬（1）<div>packed_embedded = torch.nn.utils.rnn.pack_padded_sequence(embedded, length.to(&#39;cpu&#39;), batch_first=True,  enforce_sorted=False)
这里length必须转为成cpu，否则会报错。</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/48/3a981e55.jpg" width="30px"><span>林于翔</span> 👍（1） 💬（1）<div>LSTM模型定义中:
 if self.lstm.bidirectional:
            hidden = self.dropout(torch.cat([hidden[-1], hidden[-2]], dim=-1))
这里不太理解，最后连接的不是最后一层hidden的第一个时间步和最后一个时间步嘛？另外dim为什么会是-1。</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（0） 💬（1）<div>torchtext可以支持中文分词吗</div>2022-06-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOMHZ2zMTQty2ToyS9Hc6lZQ1ibzwEnW2psEhyvZ1vNdh9kgermDycCJtp6xX725u1fpsH8CFe6vg/132" width="30px"><span>Geek_a82ba7</span> 👍（0） 💬（4）<div>import torchtext
train_iter = torchtext.datasets.IMDB(root=&#39;.&#47;data&#39;, split=&#39;train&#39;)
next(train_iter)
&#39;MapperIterDataPipe&#39; object is not an iterator
为什么说这个不是一个迭代器，查了很多资料都没有解决，老师能回答一下吗？
c</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/30/46/19f203cc.jpg" width="30px"><span>Sarai青霞</span> 👍（0） 💬（1）<div>方老师，我试了代码，输出显示：
&quot;\n输出：[&#39;here&#39;, &#39;is&#39;, &#39;the&#39;, &#39;an&#39;, &#39;example&#39;, &#39;!&#39;]\n&quot;
是断行出现问题了吗？
谢谢！</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/76/60/4be280d7.jpg" width="30px"><span>Ringcoo</span> 👍（0） 💬（1）<div>老师好，请问
packed_output, (hidden, cell) = self.lstm(packed_embedded)       
 output, output_length = torch.nn.utils.rnn.pad_packed_sequence(packed_output)
为什么从lstm层出来以后 会有(hidden, cell) ，我不太理解，以及为什么lstm层出来以后还有在进RNN层，底下的流程图上明明是lstm层出来以后进入了fc全连接层。麻烦您讲解一下</div>2022-05-01</li><br/><li><img src="" width="30px"><span>赵心睿</span> 👍（0） 💬（1）<div>请问使用的torchtext是哪个版本的呢？
</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（0） 💬（1）<div>请问这是那个版本的torchtext</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/50/34/172342fd.jpg" width="30px"><span>吴十一</span> 👍（1） 💬（0）<div>def predict_sentiment(text, model, tokenizer, vocab, device):
    max_length = 256
    pad = text_pipeline(&#39;&lt;pad&gt;&#39;)
    processed_text = text_pipeline(text)[:max_length]
    ids, length = [],[]
    ids.append((processed_text+pad*max_length)[:max_length])
    length.append(len(processed_text))
    ids_t,length_t = torch.tensor(ids, dtype = torch.int64), torch.tensor(length, dtype = torch.int64)
    print(ids_t,length_t)
    ids_t.to(device)
    length_t.to(device)
    pred = model(ids_t,length_t)
    return pred
vocab_size = len(vocab)
embedding_dim = 300
hidden_dim = 300
output_dim = 2
n_layers = 2
bidirectional = True
dropout_rate = 0.5
device = torch.device(&quot;cuda:0&quot; if torch.cuda.is_available() else &quot;cpu&quot;)
model = LSTM(vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout_rate)
model = model.to(device)
model.load_state_dict(torch.load(&quot;.&#47;lstm.pt&quot;))
model.eval()
text = &quot;This film is terrible!&quot;
pred = predict_sentiment(text, model, tokenizer, vocab, device)
&#39;&#39;&#39;
输出：(&#39;neg&#39;, 0.8874172568321228)
&#39;&#39;&#39;
tips：一定要安装torchtext 稍微新点的版本，0.6.0 IDMB数据set跑报错，会一直要求用tensorflow v1 版本兼容</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（1） 💬（0）<div>import torch
import torchtext
torchtext.__version__
dir(torchtext)
from torchtext import data
dir(data)

# 读取IMDB数据集


# 读取IMDB数据集

TEXT = data.Field(lower=True, include_lengths=True, batch_first=True)
LABEL = data.Field(sequential=False)

# make splits for data 划分数据
train, test = torchtext.datasets.IMDB.splits(TEXT, LABEL)

# build the vocabulary
from torchtext.vocab import GloVe
TEXT.build_vocab(train, vectors=GloVe(name=&#39;6B&#39;, dim=300))
LABEL.build_vocab(train)

# make iterator for splits
train_iter, test_iter = data.BucketIterator.splits(
    (train, test), batch_size=3, device=0)</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>最后一块代码跑出错
版本 torchtext
print(torchtext.__version__)  # 0.13.1
出错的代码
for epoch in range(n_epochs):
    train_loss, train_acc = train(train_dataloader, model, criterion, optimizer, device)

错误log
training...:   0%|          | 0&#47;2969 [00:00&lt;?, ?it&#47;s]
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
&lt;ipython-input-23-3dd500bd7dd1&gt; in &lt;module&gt;
      8 
      9 for epoch in range(n_epochs):
---&gt; 10     train_loss, train_acc = train(train_dataloader, model, criterion, optimizer, device)

      7     epoch_losses = []
      8     epoch_accs = []
----&gt; 9     for batch in tqdm.tqdm(dataloader, desc=&#39;training...&#39;, file=sys.stdout):
     10         (label, ids, length) = batch

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;tqdm&#47;std.py in __iter__(self)
   1127 
   1128         try:
-&gt; 1129             for obj in iterable:

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torch&#47;utils&#47;data&#47;dataloader.py in __next__(self)
    680                 self._reset()  # type: ignore[call-arg]
--&gt; 681             data = self._next_data()
    682             self._num_yielded += 1

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torch&#47;utils&#47;data&#47;dataloader.py in _next_data(self)
    720         index = self._next_index()  # may raise StopIteration
--&gt; 721         data = self._dataset_fetcher.fetch(index)  # may raise StopIteration
    722         if self._pin_memory:
~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torch&#47;utils&#47;data&#47;_utils&#47;fetch.py in fetch(self, possibly_batched_index)
     51             data = self.dataset[possibly_batched_index]
---&gt; 52         return self.collate_fn(data)

&lt;ipython-input-12-6fc8a353bed8&gt; in collate_batch(batch)
     10         length_list.append(len(processed_text))
---&gt; 11         text_list.append((processed_text + max_length)[:max_length])

TypeError: can only concatenate list (not &quot;int&quot;) to list</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>torchtext.datasets.IMDB 改为如下可以正确运行

# pip install torchtext
# pip install torchdata
import torchtext
# 读取IMDB数据集
train_iter = torchtext.datasets.IMDB(root=&#39;.&#47;data&#39;, split=&#39;train&#39;)
train_iter = iter(train_iter)
next(train_iter)</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（0） 💬（0）<div>torchtext说明文档：https:&#47;&#47;pytorch.org&#47;text&#47;stable&#47;index.html</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>用自己的电脑训练一个端午节，结果如下：
(&#39;neg&#39;, 0.9985383749008179)</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>import torch
import torchtext

from LSTM import LSTM

device = torch.device(&quot;cuda&quot; if torch.cuda.is_available() else &quot;cpu&quot;)

def predict_sentiment(text, model, tokenizer, vocab, device):
    tokens = tokenizer(text)
    ids = [vocab[t] for t in tokens]
    length = torch.LongTensor([len(ids)])
    tensor = torch.LongTensor(ids).unsqueeze(dim=0).to(device)
    prediction = model(tensor, length).squeeze(dim=0)
    probability = torch.softmax(prediction, dim=-1)
    predicted_class = prediction.argmax(dim=-1).item()
    predicted_probability = probability[predicted_class].item()
    predicted_class_title = [&#39;neg&#39;, &#39;pos&#39;]
    return predicted_class_title[predicted_class], predicted_probability

if __name__ == &quot;__main__&quot;:
    text = &quot;This film is terrible!&quot;

    train_iter = torchtext.datasets.IMDB(root=&#39;.&#47;data&#39;, split=&#39;train&#39;)
    # 创建分词器
    tokenizer = torchtext.data.utils.get_tokenizer(&#39;basic_english&#39;)


    # 构建词汇表
    def yield_tokens(data_iter):
        for _, text in data_iter:
            yield tokenizer(text)


    vocab = torchtext.vocab.build_vocab_from_iterator(yield_tokens(train_iter), specials=[&quot;&lt;pad&gt;&quot;, &quot;&lt;unk&gt;&quot;])
    vocab.set_default_index(vocab[&quot;&lt;unk&gt;&quot;])

    # 加载模型
    vocab_size = len(vocab)
    embedding_dim = 300
    hidden_dim = 300
    output_dim = 2
    n_layers = 2
    bidirectional = True
    dropout_rate = 0.5
    model = LSTM(vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout_rate)
    model.load_state_dict(torch.load(&#39;.&#47;lstm.pt&#39;))
    model.to(device)
    model.eval()
    print(predict_sentiment(text, model, tokenizer, vocab, device))

参考：
https:&#47;&#47;github.com&#47;bentrevett&#47;pytorch-sentiment-analysis&#47;blob&#47;master&#47;2_lstm.ipynb</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>import torchtext
train_iter = torchtext.datasets.IMDB(root=&#39;.&#47;data&#39;, split=&#39;train&#39;)
print(next(iter(train_iter)))
在PyCharm里面这样跑没问题，JupyterLab这样就跑不动了</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（0） 💬（0）<div>我的版本太低了
</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（0） 💬（0）<div>我安装了torchtext==0.6跟老师的版本估计不一致
</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/1d/4641c012.jpg" width="30px"><span>reatiny</span> 👍（0） 💬（0）<div>我感觉模型部分数据流动不太明白，建议多一点解释</div>2021-12-04</li><br/>
</ul>