你好，我是徐文浩。

过去一年，是整个AI领域风驰电掣的一年。希望「AI大模型之美」这门课程，让你对大模型领域有了一个完整的认识。而随着AI大模型领域的进一步发展，无论是OpenAI开放的API能力，还是开源领域百花齐放的各种模型，都有了长足的进步和发展。

所以，在这新的一年里，我会对「AI大模型之美」这门课程做一个更新。一方面，是查漏补缺，修订一下已经上线的内容。因为无论是OpenAI提供的GPT，还是llama-index和LangChain这样的开源项目，在API上都发生了很大的变化。另一方面，则是提供一些更深入的内容，因为OpenAI和百花齐放的开源领域，都提供更丰富的AI能力，让我们开发AI的应用更加方便了。

## 废弃Completions接口，使用Chat Completions接口

在这个课程一开始的时候，我就以一个给跨境电商的商品写标题的例子向你展示了 GPT-3.5 模型的能力。

```python
from openai import OpenAI
import os

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)
COMPLETION_MODEL = "text-davinci-003"

prompt = """
Consideration proudct : 工厂现货PVC充气青蛙夜市地摊热卖充气玩具发光蛙儿童水上玩具

1. Compose human readale product title used on Amazon in english within 20 words.
2. Write 5 selling points for the products in Amazon.
3. Evaluate a price range for this product in U.S.

Output the result in json format with three properties called title, selling_points and price_range
"""

def get_response(prompt, model=COMPLETION_MODEL):
    completions = client.completions.create (
        model=COMPLETION_MODEL,
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.0,        
    )
    message = completions.choices[0].text
    return message

print(get_response(prompt)) 
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/a9/791d0f5e.jpg" width="30px"><span>王平</span> 👍（1） 💬（1）<div>老师如果需要输出是一种自定义的数据结构，有什么好的方法吗？</div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/27/1f/42059b0f.jpg" width="30px"><span>HXL</span> 👍（0） 💬（0）<div>老师 您好 ! 最近遇到个问题 调用openai的接口 发现一直超时不知道是啥原因 ? 

&quot;cause: FetchError: request to https:&#47;&#47;api.openai.com&#47;v1&#47;chat&#47;completions failed, reason:&quot;</div>2024-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（0）<div>试了一下，以期得到每次输出的结果都完全一样，这是概率模型输出的难点。
调用的参数是 temperature=0.0, seed=12345, 相同的 fingerprint。试了多次，一致性达到前4个卖点都相同已是我得到的最佳结果。

结果1:
fp_2b778c6b35
{
    &quot;title&quot;: &quot;Inflatable Frog Night Market Hot Selling Toy with LED for Kids&quot;,
    &quot;selling_points&quot;: [
        &quot;工厂现货，质量可靠&quot;,
        &quot;可充气，易携带&quot;,
        &quot;发光设计，吸引眼球&quot;,
        &quot;适合水上玩耍，增加乐趣&quot;,
        &quot;可作为地摊销售，商机多&quot;
    ],
    &quot;price_range&quot;: &quot;$10 - $20&quot;
}

结果2:
fp_2b778c6b35
{
    &quot;title&quot;: &quot;Inflatable Frog Night Market Hot Selling Toy with LED for Kids&quot;,
    &quot;selling_points&quot;: [
        &quot;工厂现货，质量可靠&quot;,
        &quot;可充气，易携带&quot;,
        &quot;发光设计，吸引眼球&quot;,
        &quot;适合水上玩耍，增加乐趣&quot;,
        &quot;可用于夜市地摊销售&quot;
    ],
    &quot;price_range&quot;: &quot;$10 - $20&quot;
}

用英文输出，一致性也无明显提高。
在本例中，提示词中要求给出相关商品的5个卖点，输出结果保持完全一致对概率模型而言并不容易，当然在本示例中也无必要，但它却提供一个很好的观察点。</div>2024-03-03</li><br/>
</ul>