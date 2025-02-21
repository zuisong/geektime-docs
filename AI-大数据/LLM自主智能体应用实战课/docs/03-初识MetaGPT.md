你好，我是李锟。

这节课我们正式进入实战环节，开始学习本课程第一个 Autonomous Agent 开发框架——**MetaGPT，也是目前此类开发框架中最为成熟的一个。**

目前 Python 是 AI + LLM 应用开发的首选编程语言，我们这套课程中使用的编程语言是 Python，选择的开发框架也是 Python 开发框架。其他编程语言例如 Java、C#、JavaScript、Go 等语言的开发者，暂时无法兼顾，只能说抱歉了。

## 安装 Python、Node.js 和 Git

在 Linux 主机上需要确保有符合要求的 Python 版本。在 Ubuntu 上安装 Python 的方法很多，你可以自行搜索。理想情况下，Ubuntu 自带的 Python 版本即可满足要求。从兼容性的角度，Python 的版本我推荐使用官方的 3.10 版。

虽然 Python 最新的官方版本已经是 3.13 版，但仍然有很多 AI、LLM 开发库无法在 3.12 以上版本中使用。所以以后对于要学习的每个开发框架，除非我明确说明可使用 Python 3.12 以上版本，否则都使用 3.10 或 3.11 版。使用 Conda 安装的 Python 也是可以的，只要对应的 Python 版本满足上述要求。

在 Python 环境中，需要提前安装好 poetry，因为我们将使用 poetry 这个强大的工具来创建和管理 Python 虚拟环境。安装方法：
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/30/eb380376.jpg" width="30px"><span>月狼葱葱</span> 👍（1） 💬（1）<div>我使用win11，在执行poetry install --no-root &amp;&amp; poetry run pip install -e &quot;..&#47;MetaGPT&quot; --config-settings editable_mode=compat，会报错： ERROR: Failed building wheel for volcengine-python-sdk，原因是文件路径过长：Windows 系统默认对文件路径长度有限制，可能会导致某些文件无法正确创建。，用win的伙伴可以参考解决方案 https:&#47;&#47;github.com&#47;geekan&#47;MetaGPT&#47;issues&#47;1677</div>2025-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/e8/d01b90c3.jpg" width="30px"><span>种花家</span> 👍（1） 💬（1）<div>sudo npm install -g @mermaid-js&#47;mermaid-cli 之前加上 sudo apt install npm
然后检查 node -v
npm -v</div>2025-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/75/f221dbbf.jpg" width="30px"><span>蝈大虾</span> 👍（0） 💬（2）<div>如何配置metagpt调用通过vllm部署的qwen模型?


### 测试设置config.yaml配置如下：
llm:
  api_type: &quot;ollama&quot; 
  model: &quot;&#47;models&#47;Qwen2.5-72B-Instruct&quot;
  base_url: &quot;http:&#47;&#47;localhost:8000&#47;v1&quot;
  api_key: &quot;EMPTY&quot;
  temperature: 0

执行metagpt &quot;Create a 2048 game&quot;报错。

注：使用dashscope的qwen72b可以成功。

###vllm服务命令：
vllm serve &#47;models&#47;Qwen2.5-72B-Instruct \
              --host 0.0.0.0 \
              --port 8000 \
              --dtype bfloat16 \
              --tensor_parallel_size 2 \
              --max-num-seqs 1 \
              --enforce-eager \
              --gpu_memory_utilization 0.95 \
              --max_model_len 16384 \
              --max_seq_len_to_capture 16384 \
              --max-num-batched-tokens 16384 \
              --swap-space 8 \
              --disable-log-requests \
              --enable-auto-tool-choice \
              --tool-call-parser hermes
			  


## 该服务经测试正常调用。
from openai import OpenAI
client = OpenAI(api_key=&quot;EMPTY&quot;, base_url=&quot;http:&#47;&#47;localhost:8000&#47;v1&quot;)
model_type=&quot;&#47;models&#47;Qwen2.5-72B-Instruct&quot;
...
response = client.chat.completions.create(
    model=model_type,
    messages=messages,
    temperature=0,
    stream=True
)
...</div>2025-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/98/d5e08eb7.jpg" width="30px"><span>yangchao</span> 👍（0） 💬（1）<div>思考题
在 build_customized_multi_agents.py 中，不同的 Agent（即 Role 的子类实例）通过消息传递和动作执行来进行协作，具体就是每个角色都有特定的职责和可以执行的操作。角色之间通过_watch机制建立联系，形成工作流。</div>2025-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/e6/50c5b805.jpg" width="30px"><span>欠债太多</span> 👍（0） 💬（1）<div>老师，如果推荐的配置机器没有，使用mac air替代是否可行，现在机器的配置是Apple M3 16g内存？会有哪些影响
</div>2025-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cf/11/3128bf4d.jpg" width="30px"><span>蓝天</span> 👍（0） 💬（1）<div>Linux 5.4.0-117-generic
npm ERR! argv &quot;&#47;usr&#47;bin&#47;node&quot; &quot;&#47;usr&#47;bin&#47;npm&quot; &quot;install&quot; &quot;-g&quot; &quot;@mermaid-js&#47;mermaid-cli&quot;
npm ERR! node v8.10.0
npm ERR! npm  v3.5.2
npm ERR! code EMISSINGARG

npm ERR! typeerror Error: Missing required argument #1
npm ERR! typeerror     at andLogAndFinish (&#47;usr&#47;share&#47;npm&#47;lib&#47;fetch-package-metadata.js:31:3)
npm ERR! typeerror     at fetchPackageMetadata (&#47;usr&#47;share&#47;npm&#47;lib&#47;fetch-package-metadata.js:51:22)
npm ERR! typeerror     at resolveWithNewModule (&#47;usr&#47;share&#47;npm&#47;lib&#47;install&#47;deps.js:456:12)
npm ERR! typeerror     at &#47;usr&#47;share&#47;npm&#47;lib&#47;install&#47;deps.js:190:5
npm ERR! typeerror     at &#47;usr&#47;share&#47;npm&#47;node_modules&#47;slide&#47;lib&#47;async-map.js:52:35
npm ERR! typeerror     at Array.forEach (&lt;anonymous&gt;)
npm ERR! typeerror     at &#47;usr&#47;share&#47;npm&#47;node_modules&#47;slide&#47;lib&#47;async-map.js:52:11
npm ERR! typeerror     at Array.forEach (&lt;anonymous&gt;)
npm ERR! typeerror     at asyncMap (&#47;usr&#47;share&#47;npm&#47;node_modules&#47;slide&#47;lib&#47;async-map.js:51:8)
npm ERR! typeerror     at exports.loadRequestedDeps (&#47;usr&#47;share&#47;npm&#47;lib&#47;install&#47;deps.js:188:3)
npm ERR! typeerror This is an error with npm itself. Please report this error at:
npm ERR! typeerror     &lt;http:&#47;&#47;github.com&#47;npm&#47;npm&#47;issues&gt;
</div>2025-02-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oCx7GX9P4w5cml1cpbFD1x21Biad3MLCTOhTPJvicRW3xp9C8xTgdiaOSdpFyvibKSfcD1LL4miaT7VtqqKms6rgujg/132" width="30px"><span>zshanjun</span> 👍（0） 💬（2）<div>运行报错，跑不通。老师帮忙看看

poetry run metagpt &quot;write a cli blackjack game&quot;
2025-02-10 17:24:03.997 | INFO     | metagpt.team:invest:93 - Investment: $3.0.
2025-02-10 17:24:03.998 | INFO     | metagpt.roles.role:_act:403 - Alice(Product Manager): to do PrepareDocuments(PrepareDocuments)
2025-02-10 17:24:04.062 | INFO     | metagpt.utils.file_repository:save:57 - save to: &#47;Users&#47;zhangsj190&#47;ai&#47;MetaGPT&#47;workspace&#47;20250210172403&#47;docs&#47;requirement.txt
2025-02-10 17:24:04.062 | INFO     | metagpt.roles.role:_act:403 - Alice(Product Manager): to do WritePRD(WritePRD)
2025-02-10 17:24:04.062 | INFO     | metagpt.actions.write_prd:run:86 - New requirement detected: write a cli blackjack game
2025-02-10 17:24:04.091 | ERROR    | metagpt.utils.common:log_it:554 - Finished call to &#39;metagpt.actions.action_node.ActionNode._aask_v1&#39; after 0.028(s), this was the 1st time calling it. exp: &#39;dict&#39; object has no attribute &#39;lower&#39;
2025-02-10 17:24:05.011 | ERROR    | metagpt.utils.common:log_it:554 - Finished call to &#39;metagpt.actions.action_node.ActionNode._aask_v1&#39; after 0.948(s), this was the 2nd time calling it. exp: &#39;dict&#39; object has no attribute &#39;lower&#39;
2025-02-10 17:24:15.394 | WARNING  | metagpt.utils.common:wrapper:673 - There is a exception in role&#39;s execution, in order to resume, we delete the newest role communication message in the role&#39;s memory.
2025-02-10 17:24:15.402 | ERROR    | metagpt.utils.common:wrapper:655 - Exception occurs, start to serialize the project, exp:
Traceback (most recent call last):
  File &quot;&#47;Users&#47;zhangsj190&#47;Library&#47;Caches&#47;pypoetry&#47;virtualenvs&#47;learn-metagpt-eQkDn61w-py3.10&#47;lib&#47;python3.10&#47;site-packages&#47;tenacity&#47;_asyncio.py&quot;, line 50, in __call__
    result = await fn(*args, **kwargs)
  File &quot;&#47;Users&#47;zhangsj190&#47;ai&#47;MetaGPT&#47;metagpt&#47;actions&#47;action_node.py&quot;, line 442, in _aask_v1
    parsed_data = llm_output_postprocess(
AttributeError: &#39;dict&#39; object has no attribute &#39;lower&#39;



</div>2025-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/30/eb380376.jpg" width="30px"><span>月狼葱葱</span> 👍（0） 💬（1）<div>win11用户无法使用 命令
mkdir ~&#47;.metagpt
vi ~&#47;.metagpt&#47;config2.yaml 
假设你的用户名是 username，转换命令如下
mkdir C:\Users\username\.metagpt
notepad C:\Users\username\.metagpt\config2.yaml</div>2025-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/4f/01a64939.jpg" width="30px"><span>花前不枉此生壹梦</span> 👍（0） 💬（1）<div>poetry add pysocks socksio 

The currently activated Python version 3.12.3 is not supported by the project (&gt;=3.9, &lt;3.12).
Trying to find and use a compatible version. 

Poetry was unable to find a compatible version. If you have one, you can explicitly use it via the &quot;env use&quot; command.

执行的时候报错，应该怎么搞
</div>2025-01-15</li><br/><li><img src="" width="30px"><span>Geek_9708db</span> 👍（0） 💬（2）<div>用qwen:14b运行报错JSON parse的问题，应该是解析出了问题；换成llama3:latest好用了。这个怎么解决呢，总觉得如果不能支持大部分模型就不太好用呀</div>2025-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/0c/a261048b.jpg" width="30px"><span>木法沙</span> 👍（2） 💬（0）<div>➜  learn_metagpt python3 main.py
Welcome to Blackjack!
Player&#39;s hand: (&#39;Hearts&#39;, 3)
Player&#39;s hand: (&#39;Spades&#39;, &#39;Jack&#39;)
Do you want to hit or stand? (h&#47;s): h
Player&#39;s hand: (&#39;Hearts&#39;, 3)
Player&#39;s hand: (&#39;Spades&#39;, &#39;Jack&#39;)
Bust! You lose this round.
➜  learn_metagpt python3 main.py
Welcome to Blackjack!
Player&#39;s hand: (&#39;Spades&#39;, 8)
Player&#39;s hand: (&#39;Spades&#39;, 7)
Do you want to hit or stand? (h&#47;s): s
Dealer busts! You win this round!</div>2025-01-08</li><br/>
</ul>