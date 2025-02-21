你好，我是徐文浩。

上一讲里我们看到大模型的确有效。在进行情感分析的时候，我们通过OpenAI的API拿到的Embedding，比T5-base这样单机可以运行的小模型，效果还是好很多的。

不过，我们之前选用的问题的确有点太简单了。我们把5个不同的分数分成了正面、负面和中性，还去掉了相对难以判断的“中性”评价，这样我们判断的准确率高的确是比较好实现的。但如果我们想要准确地预测出具体的分数呢？

## 利用Embedding，训练机器学习模型

最简单的办法就是利用我们拿到的文本Embedding的向量。这一次，我们不直接用向量之间的距离，而是使用传统的机器学习的方法来进行分类。毕竟，如果只是用向量之间的距离作为衡量标准，就没办法最大化地利用已经标注好的分数信息了。

事实上，OpenAI在自己的官方教程里也直接给出了这样一个例子。我在这里也放上了相应的GitHub的代码[链接](https://github.com/openai/openai-cookbook/blob/main/examples/Classification_using_embeddings.ipynb)，你可以去看一下。不过，为了避免OpenAI王婆卖瓜自卖自夸，我们也希望能和其他人用传统的机器学习方式得到的结果做个比较。

因此我重新找了一个中文的数据集来试一试。这个数据集是在中文互联网上比较容易找到的一份今日头条的新闻标题和新闻关键词，在GitHub上可以直接找到数据，我把[链接](https://github.com/aceimnorstuvwxz/toutiao-text-classfication-dataset)也放在这里。用这个数据集的好处是，有人同步放出了预测的实验效果。我们可以拿自己训练的结果和他做个对比。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/61/ef/ac5e914d.jpg" width="30px"><span>麦耀锋</span> 👍（32） 💬（2）<div>应该这么去理解embedding的使用。以前我们做机器学习的时候（或者相对于深度学习之前的“浅层学习”），不管是有监督还是无监督，一般我们需要做feature engineering，也就是需要data scientist，根据业务、专家领域，对数据提取有用的feature；而在NLP领域，那么就是通过word2vec等各种方式来提取feature。通过openai的embedding接口，实际上就是openai帮我们做了feature engineering这一步，将文本映射到一个合适的vector space，得到的embedding其实就是文本的feature，所以可以基于这个embedding即feature X来做传统的机器学习</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（18） 💬（9）<div>老师，你好！既然都调用open ai的接口，为什么不直接让chatgpt直接返回分类结果呢</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/73/fd1e37a2.jpg" width="30px"><span>良辰美景</span> 👍（10） 💬（1）<div>“调用了 Tiktoken 这个库，使用了 cl100k_base 这种编码方式，这种编码方式和 text-embedding-ada-002 模型是一致的。如果选错了编码方式，你计算出来的 Token 数量可能和 OpenAI 的不一样。” 老师， 问你一个学习上的问题， 像这种API 文档里这么细节的东西，你是如何获取这些信息的</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（5） 💬（1）<div>在执行这段代码时会报ParserWarning
df = pd.read_csv(&#39;data&#47;toutiao_cat&#47;toutiao_cat_data.txt&#39;, sep=&#39;_!_&#39;, names=[&#39;id&#39;, &#39;code&#39;, &#39;category&#39;, &#39;title&#39;, &#39;keywords&#39;])

ParserWarning: Falling back to the &#39;python&#39; engine because the &#39;c&#39; engine does not support regex separators (separators &gt; 1 char and different from &#39;\s+&#39; are interpreted as regex); you can avoid this warning by specifying engine=&#39;python&#39;.

原因是 &#39;c&#39; 引擎不支持分隔符sep=&#39;_!_&#39;表达式，可指定 engine=&#39;python&#39; 来避免此警告。
代码如下
df = pd.read_csv(&#39;data&#47;toutiao_cat&#47;toutiao_cat_data.txt&#39;, engine= &#39;python&#39;， sep=&#39;_!_&#39;, names=[&#39;id&#39;, &#39;code&#39;, &#39;category&#39;, &#39;title&#39;, &#39;keywords&#39;])</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/98/59/c2ce609d.jpg" width="30px"><span>怡仔</span> 👍（5） 💬（4）<div>github中的找不到途中列举的数据文件</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a9/ca/f216bece.jpg" width="30px"><span>lala</span> 👍（4） 💬（1）<div>现在chatGPT是通用的问答应用。请问如何根据ChatGPT结合公司业务的知识库和商品信息，如何打造服务客户和内部顾问的机器人？比如根据用户问题，推荐对应产品给用户。根据内部知识库，回答内部同事关于产品使用，运营信息相关的问题呢。谢谢</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（4） 💬（2）<div>训练一个能把从 1 分到 5 分的每一个级别都区分出来的机器学习模型.
使用下载的数据 fine_food_reviews_with_embeddings_1k.csv

随机森林模型，超参数 n_estimators=100 下跑的结果

              precision    recall  f1-score   support

           1       0.86      0.30      0.44        20
           2       1.00      0.38      0.55         8
           3       1.00      0.18      0.31        11
           4       1.00      0.26      0.41        27
           5       0.74      1.00      0.85       134

       accuracy                               0.76       200
    macro avg       0.92      0.42      0.51       200
weighted avg       0.81      0.76      0.71       200

极端随机森林模型 ExtraTreesClassifier() 下跑的结果

              precision    recall  f1-score   support

           1       1.00      0.20      0.33        20
           2       1.00      0.38      0.55         8
           3       1.00      0.18      0.31        11
           4       1.00      0.26      0.41        27
           5       0.73      1.00      0.84       134

      accuracy                                0.75       200
    macro avg       0.95      0.40      0.49       200
weighted avg       0.82      0.75      0.69       200
</div>2023-03-31</li><br/><li><img src="" width="30px"><span>Geek_513b7c</span> 👍（4） 💬（2）<div>老师，你能解释一下在ai中向量是什么意思吗？这几节看的云里雾里的</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/4b/4a622bdf.jpg" width="30px"><span>四月.  🕊</span> 👍（2） 💬（1）<div>请问一下老师，既然已经按照batch_size划分出来了prompt_batches，为什么在get_embeddings_with_backoff函数中还要划分一次batch呢？是不是重复了？</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/a9/791d0f5e.jpg" width="30px"><span>王平</span> 👍（2） 💬（1）<div>老师请问如果把时序数据，比如用户行为序列作为输入给openAI 的 embedding, 根据行为判断用户情感的效果会好吗？</div>2023-04-03</li><br/><li><img src="" width="30px"><span>高捷</span> 👍（1） 💬（1）<div>老师您好，想知道大概多久需要去同步一次embedding模型，大模型自己怎么更新迭代呢？</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（1） 💬（1）<div>花费多少token怎么算呢 
一个问题一个token吗</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/5b/fe7ebc2e.jpg" width="30px"><span>R9Go</span> 👍（1） 💬（1）<div>https:&#47;&#47;github.com&#47;xuwenhao&#47;geektime-ai-course&#47;blob&#47;main&#47;data&#47;20_newsgroup_with_embedding.parquet
这个数据是不是不全？</div>2023-05-02</li><br/><li><img src="" width="30px"><span>Geek_512735</span> 👍（1） 💬（1）<div>老师，请利用ChatGPT embedding的优势在什么地方？</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a3/bb/5cde4385.jpg" width="30px"><span>Bank</span> 👍（1） 💬（1）<div>在读数据的时候报了这个错，请问如何解决呢？内存应该是足够的
---------------------------------------------------------------------------
ArrowMemoryError                          Traceback (most recent call last)
Cell In[6], line 6
      3 from sklearn.model_selection import train_test_split
      4 from sklearn.metrics import classification_report, accuracy_score
----&gt; 6 training_data = pd.read_parquet(&quot;D:&#47;work&#47;data&#47;toutiao_cat_data_all_with_embeddings.parquet&quot;)
      7 training_data.head()
      9 df =  training_data.sample(50000, random_state=42)

。。。。。。
-&gt; 2517 table = self._dataset.to_table(
   2518     columns=columns, filter=self._filter_expression,
   2519     use_threads=use_threads
   2520 )
   2522 # if use_pandas_metadata, restore the pandas metadata (which gets
   2523 # lost if doing a specific `columns` selection in to_table)
   2524 if use_pandas_metadata:

File D:\anaconda3\lib\site-packages\pyarrow\_dataset.pyx:332, in pyarrow._dataset.Dataset.to_table()

File D:\anaconda3\lib\site-packages\pyarrow\_dataset.pyx:2661, in pyarrow._dataset.Scanner.to_table()

File D:\anaconda3\lib\site-packages\pyarrow\error.pxi:144, in pyarrow.lib.pyarrow_internal_check_status()

File D:\anaconda3\lib\site-packages\pyarrow\error.pxi:117, in pyarrow.lib.check_status()

ArrowMemoryError: malloc of size 134217728 failed</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/60/ad/03351e6e.jpg" width="30px"><span>xbc</span> 👍（1） 💬（1）<div>from openai.embeddings_utils import get_embeddings 用的是 text-similarity-davinci-001 吧.

openai.Embedding.create 可以选择用 text-embedding-ada-002</div>2023-03-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/z3nIITkhzRj9WApibhic524lQSJmqUCerpuqpntEe06LE3lRGKr6rGwPpPJtZ5Xj0NBPyvTatKtIk0hfyAnl9Hsg/132" width="30px"><span>Geek_378f83</span> 👍（0） 💬（1）<div>老师，同学们好，请教一下：
colab 中运行时报错：  &#47;lib&#47;x86_64-linux-gnu&#47;libstdc++.so.6: version `GLIBCXX_3.4.29&#39; not found (required by &#47;usr&#47;local&#47;lib&#47;python3.10&#47;site-packages&#47;sentencepiece&#47;_sentencepiece.cpython-310-x86_64-linux-gnu.so)；需要在colab中怎么解决？
询问gpt后目前仍未解决，求助</div>2023-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcwXucibksEYRSYg6icjibzGa7efcMrCsGec2UwibjTd57icqDz0zzkEEOM2pXVju60dibzcnQKPfRkN9g/132" width="30px"><span>Geek_93970d</span> 👍（0） 💬（1）<div>import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
# 换成正确的路径
df_all = pd.read_csv(&quot;..&#47;data&#47;fine_food_reviews_with_embeddings_1k.csv&quot;)
df_all[&quot;embedding&quot;] = df_all.embedding.apply(eval).apply(np.array)

# 其实没必要转换成 parquet
df_all.to_parquet(&quot;fine_food_reviews_with_embeddings.parquet&quot;, index=True)
training_data = pd.read_parquet(&quot;fine_food_reviews_with_embeddings.parquet&quot;)
training_data.head()

#df =  training_data.sample(50000, random_state=42)
#df = df_all
df = training_data

X_train, X_test, y_train, y_test = train_test_split(
    list(df.embedding.values), df.Score, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(n_estimators=300)
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
probas = clf.predict_proba(X_test)

report = classification_report(y_test, preds)
print(report)

------------结果如下-----------
              precision    recall  f1-score   support

           1       0.89      0.40      0.55        20
           2       1.00      0.38      0.55         8
           3       1.00      0.18      0.31        11
           4       1.00      0.26      0.41        27
           5       0.75      1.00      0.86       134

    accuracy                           0.77       200
   macro avg       0.93      0.44      0.53       200
weighted avg       0.82      0.77      0.72       200</div>2023-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcwXucibksEYRSYg6icjibzGa7efcMrCsGec2UwibjTd57icqDz0zzkEEOM2pXVju60dibzcnQKPfRkN9g/132" width="30px"><span>Geek_93970d</span> 👍（0） 💬（1）<div>data&#47;toutiao_cat_data_all_with_embeddings.parquet
这个文件找不到</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9d/2a/3e57b54a.jpg" width="30px"><span>地平线</span> 👍（0） 💬（1）<div>训练一个能把从 1 分到 5 分的每一个级别都区分出来的机器学习模型.
使用老师的数据 fine_food_reviews_with_embeddings_1k.csv

随机森林模型，参数 n_estimators=300下跑的结果

              precision    recall  f1-score   support

           1       1.00      0.30      0.46        20
           2       1.00      0.38      0.55         8
           3       1.00      0.18      0.31        11
           4       1.00      0.26      0.41        27
           5       0.74      1.00      0.85       134

    accuracy                           0.76       200
   macro avg       0.95      0.42      0.51       200
weighted avg       0.82      0.76      0.71       200</div>2023-05-17</li><br/><li><img src="" width="30px"><span>Geek_44df74</span> 👍（0） 💬（2）<div>老师，有个问题，上面只是用一些算法校验了准确和召回率，假使现在准确和召回率符合业务目标了，具体要如何应用啊，基于上面的文章分类的例子，给一个标题的embedding如何返回具体的分类？</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/5b/fe7ebc2e.jpg" width="30px"><span>R9Go</span> 👍（0） 💬（2）<div>&#39;DataFrame&#39; object has no attribute &#39;category&#39;</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5e/a9/cc943f81.jpg" width="30px"><span>Adoph</span> 👍（0） 💬（1）<div>data&#47;toutiao_cat_data.txt 这个文件在哪里呢</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/90/12/29148117.jpg" width="30px"><span>Rukit</span> 👍（0） 💬（4）<div>运行batch_embeddings = get_embeddings_with_backoff(prompts=batch, engine=embedding_model)这句代码一直显示这个错误RetryError[&lt;Future at 0x1e3a1819900 state=finished raised Timeout&gt;]
</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a9/ca/f216bece.jpg" width="30px"><span>lala</span> 👍（0） 💬（2）<div>请问我想利用chatGPT来结合公司的自己业务，打造公司自己的机器人，回答外部客户问题和内部同事问题。比如根据用户问题，直接推荐对应产品，</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a9/a2/3b44d3ca.jpg" width="30px"><span>疯狂的大石榴</span> 👍（0） 💬（2）<div>请问处理之后的数据github链接是正常的么，我点进去显示404呢（toutiao_cat_data_all_with_embeddings.parquet这个文件没办法获取）</div>2023-04-02</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（0） 💬（1）<div>标题”训练模型，看看效果怎么样“下的 GitHub 链接是404错误</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（0） 💬（1）<div>想问个问题 OpenAI embedding的时候 是不是跟ChatGPT的model没有关系 默认只会用embedding的ada002? 最近看llama index有点困惑 不知道他的API为什么在构建embedding的service context之前先确定model是3或者4</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（0） 💬（1）<div>embedding只能解决分类问题吗</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（1） 💬（3）<div>我对embedding的一些理解，就是在与用户交互时，它可以帮助你在不消耗token的情况下，把你当前需要的最相关的context信息从你的知识库提取出来。我个人觉得这个是目前，把自己的专有知识库和人工智能结合起来的最高效性价比最高的一个办法。不知道我这个看法有没有有一定道理，请老师和大家来指正。</div>2023-03-31</li><br/>
</ul>