你好，我是李锟。

前面几节课我们系统学习了 MetaGPT，对于开发 Autonomous Agent 应用已经有了一些认知。今天我们开始学习第二个开发框架 AutoGPT，也是此类开发框架的开创者。我将会分成四节课来带你系统学习 AutoGPT。

## AutoGPT官方文档导读

AutoGPT 最初名叫 EntreprenurGPT，由英国游戏开发者 Toran Bruce Richards 开发，于 2023年3月16日在 GitHub 上发布。

项目的源代码在：[https://github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)

官方文档在：[https://docs.agpt.co/platform/getting-started/](https://docs.agpt.co/platform/getting-started/)

AutoGPT 发展得很快，新版本（称作 AutoGPT Platform）与老版本（称作 AutoGPT Classic）**完全不兼容**。国内一些爱好者翻译的中文版 AutoGPT 官方文档，都是老版本的文档，延迟有一年以上，已经过时了。同样的，**所有中文版**的 AutoGPT 教程也都已经过时。阅读这些中文文档很容易被误导，因此我强烈建议你直接阅读 AutoGPT 新版本的英文文档，配备 DeepL 等强大的网页翻译插件，其实也非常容易。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（1） 💬（1）<div>老师，您好。我对您的脚本顺序进行了调整。可以跑通了：


brew install supabase&#47;tap&#47;supabase
cd ~&#47;work&#47;AutoGPT&#47;autogpt_platform&#47;backend
supabase init

# 插入以下修复脚本
cp .env.example .env
# 仅 修改 DB_PORT, DB_PASS, SUPABASE_URL  三个项目即可
vi .env
# 就后面的代码提前了：
cd ~&#47;work&#47;AutoGPT&#47;autogpt_platform&#47;backend
PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install
poetry run prisma generate --schema schema.prisma
poetry run prisma migrate dev --schema schema.prisma

# 最后执行这行 脚本
cp ..&#47;supabase&#47;supabase&#47;seed.sql supabase&#47;
sudo supabase start</div>2025-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（1） 💬（1）<div>我跑通了，但感觉还是用docker方便些。 跑一下简单demo的话，这个过程有点漫长。 </div>2025-02-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（0） 💬（2）<div>failed to send batch: ERROR: relation &quot;meetups&quot; does not exist (SQLSTATE 42P01)
------------------------------------
请问老师, meetups 表是在哪一步生成的呢? 我看看可以不可以自己创建一下</div>2025-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（0） 💬（1）<div>老师您好，有个小错误， 安装brew的脚本中右括号是中文字符，直接复制不行。我复制后一直报错：
```shell
-bash: &#47;home&#47;an&#47;.profile: line 28: unexpected EOF while looking for matching `&quot;&#39;
```
将这行：
```
echo &#39;eval &quot;$(&#47;home&#47;linuxbrew&#47;.linuxbrew&#47;bin&#47;brew shellenv）&quot;&#39; &gt;&gt; ~&#47;.profile
```

替换为：
```
echo &#39;eval &quot;$(&#47;home&#47;linuxbrew&#47;.linuxbrew&#47;bin&#47;brew shellenv)&quot;&#39; &gt;&gt; ~&#47;.profile 
```
后好了。</div>2025-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（0） 💬（2）<div>老师，注册(signup)的时候显示
The provided email may not be allowed to sign up.
- AutoGPT Platform is currently in closed beta. You can jointhe waitlist here.
- Make sure you use the same email address you used to sign up for the waitlist.
- You can self host the platform, visit ourGitHub repository.
</div>2025-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/17/8cc195cc.jpg" width="30px"><span>小叶</span> 👍（0） 💬（6）<div>执行sudo supabase start --debug 启动失败，抛异常，不存在meetup表。我看seed.sql 脚步里确实只有insert into meetups 语句，没有建表语句。这个需要怎么处理呢，大家有遇到吗？错误日志如下：
2025&#47;01&#47;23 17:54:05 PG Send: {&quot;Type&quot;:&quot;Parse&quot;,&quot;Name&quot;:&quot;lrupsc_1_3&quot;,&quot;Query&quot;:&quot;insert into meetups\n  (title, country, launch_week, start_at, is_published)\nvalues\n  (&#39;New York&#39;, &#39;USA&#39;, &#39;lw12&#39;, now(), true),\n  (&#39;London&#39;, &#39;UK&#39;, &#39;lw12&#39;, now(), true),\n  (&#39;Singapore&#39;, &#39;Singapore&#39;, &#39;lw12&#39;, now(), true)&quot;,&quot;ParameterOIDs&quot;:null}
2025&#47;01&#47;23 17:54:05 PG Send: {&quot;Type&quot;:&quot;Describe&quot;,&quot;ObjectType&quot;:&quot;S&quot;,&quot;Name&quot;:&quot;lrupsc_1_3&quot;}
2025&#47;01&#47;23 17:54:05 PG Send: {&quot;Type&quot;:&quot;Sync&quot;}
2025&#47;01&#47;23 17:54:05 PG Recv: {&quot;Type&quot;:&quot;ErrorResponse&quot;,&quot;Severity&quot;:&quot;ERROR&quot;,&quot;SeverityUnlocalized&quot;:&quot;ERROR&quot;,&quot;Code&quot;:&quot;42P01&quot;,&quot;Message&quot;:&quot;relation \&quot;meetups\&quot; does not exist&quot;,&quot;Detail&quot;:&quot;&quot;,&quot;Hint&quot;:&quot;&quot;,&quot;Position&quot;:13,&quot;InternalPosition&quot;:0,&quot;InternalQuery&quot;:&quot;&quot;,&quot;Where&quot;:&quot;&quot;,&quot;SchemaName&quot;:&quot;&quot;,&quot;TableName&quot;:&quot;&quot;,&quot;ColumnName&quot;:&quot;&quot;,&quot;DataTypeName&quot;:&quot;&quot;,&quot;ConstraintName&quot;:&quot;&quot;,&quot;File&quot;:&quot;parse_relation.c&quot;,&quot;Line&quot;:1392,&quot;Routine&quot;:&quot;parserOpenTable&quot;,&quot;UnknownFields&quot;:null}
2025&#47;01&#47;23 17:54:05 PG Recv: {&quot;Type&quot;:&quot;ReadyForQuery&quot;,&quot;TxStatus&quot;:&quot;I&quot;}
2025&#47;01&#47;23 17:54:05 PG Send: {&quot;Type&quot;:&quot;Terminate&quot;}
Stopping containers...
Pruned containers: [bec0ee92d959acf9d20b111ff8186539e36d3f4afd329239d53adf4aef416c05]
Pruned volumes: [supabase_db_backend supabase_config_backend]
Pruned network: [supabase_network_backend]
failed to send batch: ERROR: relation &quot;meetups&quot; does not exist (SQLSTATE 42P01)

</div>2025-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3d/b5/98/64f1f835.jpg" width="30px"><span>AI助手</span> 👍（0） 💬（1）<div>老师，部署到最后一步不成功，要怎么解决呢
poetry run app
2025-01-16 18:56:52,926 INFO  Scheduler started
2025-01-16 18:56:52,929 INFO  [PID-3457667|THREAD-3458081|ExecutionManager|Pyro-2c9fdd09-0f3f-45c4-9c64-281bc88f730d] Starting Pyro Service started...
2025-01-16 18:56:52,936 INFO  [ExecutionManager] Connected to Pyro; URI = PYRO:ExecutionManager@192.168.0.16:8002
2025-01-16 18:56:52,981 INFO  [ExecutionManager] Started with max-10 graph workers
2025-01-16 18:56:59,790 ERROR  [PID-3457588|THREAD-3457588|AgentServer|Prisma-8152560d-4601-4014-9b4f-be5abd675a95] Acquiring connection failed: Could not connect to the query engine. Retrying now...
2025-01-16 18:57:00,801 INFO  [PID-3457588|THREAD-3457588|AgentServer|Prisma-8152560d-4601-4014-9b4f-be5abd675a95] Acquiring connection completed successfully.
ERROR:    Traceback (most recent call last):
  File &quot;&#47;root&#47;.cache&#47;pypoetry&#47;virtualenvs&#47;autogpt-platform-backend-2D3T6tem-py3.10&#47;lib&#47;python3.10&#47;site-packages&#47;starlette&#47;routing.py&quot;, line 693, in lifespan
    async with self.lifespan_context(app) as maybe_state:
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.10&#47;contextlib.py&quot;, line 199, in __aenter__
    return await anext(self.gen)
  File &quot;&#47;root&#47;.cache&#47;pypoetry&#47;virtualenvs&#47;autogpt-platform-backend-2D3T6tem-py3.10&#47;lib&#47;python3.10&#47;site-packages&#47;fastapi&#47;routing.py&quot;, line 133, in merged_lifespan
    async with original_context(app) as maybe_original_state:
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.10&#47;contextlib.py&quot;, line 199, in __aenter__
    return await anext(self.gen)
  File &quot;&#47;root&#47;.cache&#47;pypoetry&#47;virtualenvs&#47;autogpt-platform-backend-2D3T6tem-py3.10&#47;lib&#47;python3.10&#47;site-packages&#47;fastapi&#47;routing.py&quot;, line 133, in merged_lifespan
    async with original_context(app) as maybe_original_state:
  File &quot;&#47;root&#47;miniconda3&#47;lib&#47;python3.10&#47;contextlib.py&quot;, line 199, in __aenter__
    return await anext(self.gen)
</div>2025-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（1）<div>做成可分享的docker镜像</div>2025-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/63/112780b3.jpg" width="30px"><span>晓波</span> 👍（0） 💬（0）<div>### apt 采用默认源安装 docker 和 docker-compose【不推荐】

# 更新安装源
sudo apt update

# 采用apt 安装 docker 和 docker-compose 以及所有Docekr相关的package
sudo apt install docker.io docker-compose

# 启动docker
sudo systemctl enable docker
sudo systemctl start docker

# 将当前用户加入到docker，使得当前环境可以使用docker服务
sudo usermod -aG docker $USER


在 Ubuntu 22.04 LTS 版本采用apt 安装docker-compose 的版本过低 &lt;= 1.29.2 ，存在兼容的问题（有些docker-compose的yaml配置选项不支持）。不建议用此方式安装
ubuntu@VM-0-136-ubuntu:~&#47;work&#47;AutoGPT&#47;autogpt_platform$ docker-compose up -d --build
ERROR: The Compose file &#39;&#47;home&#47;ubuntu&#47;work&#47;AutoGPT&#47;autogpt_platform&#47;docker-compose.platform.yml&#39; is invalid because:
Unsupported config option for services.executor: &#39;develop&#39;


### apt 采用官方源安装 docker 和 docker-compose【推荐】

参考资料： Ubuntu | Docker Docs ： https:&#47;&#47;docs.docker.com&#47;engine&#47;install&#47;ubuntu&#47;

## 卸载就的apt安装包
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove -y $pkg; done

# Add Docker&#39;s official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d &#47;etc&#47;apt&#47;keyrings
sudo curl -fsSL https:&#47;&#47;download.docker.com&#47;linux&#47;ubuntu&#47;gpg -o &#47;etc&#47;apt&#47;keyrings&#47;docker.asc
sudo chmod a+r &#47;etc&#47;apt&#47;keyrings&#47;docker.asc

# Add the repository to Apt sources:
echo \
  &quot;deb [arch=$(dpkg --print-architecture) signed-by=&#47;etc&#47;apt&#47;keyrings&#47;docker.asc] https:&#47;&#47;download.docker.com&#47;linux&#47;ubuntu \
  $(. &#47;etc&#47;os-release &amp;&amp; echo &quot;${UBUNTU_CODENAME:-$VERSION_CODENAME}&quot;) stable&quot; | \
  sudo tee &#47;etc&#47;apt&#47;sources.list.d&#47;docker.list &gt; &#47;dev&#47;null
sudo apt-get update

# 安装 docker 和 docker-compose
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动docker
sudo systemctl enable docker
sudo systemctl start docker

# 将当前用户加入到docker，使得当前环境可以使用docker服务
sudo usermod -aG docker $USER</div>2025-02-20</li><br/>
</ul>