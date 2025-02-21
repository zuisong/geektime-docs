你好，我是Chrono。

上一次的课程里我们一起学习了容器化的应用，也就是被打包成镜像的应用程序，然后再用各种Docker命令来运行、管理它们。

那么这又会带来一个疑问：这些镜像是怎么创建出来的？我们能不能够制作属于自己的镜像呢？

所以今天，我就来讲解镜像的内部机制，还有高效、正确地编写Dockerfile制作容器镜像的方法。

## 镜像的内部机制是什么

现在你应该知道，镜像就是一个打包文件，里面包含了应用程序还有它运行所依赖的环境，例如文件系统、环境变量、配置参数等等。

环境变量、配置参数这些东西还是比较简单的，随便用一个manifest清单就可以管理，真正麻烦的是文件系统。为了保证容器运行环境的一致性，镜像必须把应用程序所在操作系统的根目录，也就是rootfs，都包含进来。

虽然这些文件里不包含系统内核（因为容器共享了宿主机的内核），但如果每个镜像都重复做这样的打包操作，仍然会导致大量的冗余。可以想象，如果有一千个镜像，都基于Ubuntu系统打包，那么这些镜像里就会重复一千次Ubuntu根目录，对磁盘存储、网络传输都是很大的浪费。

很自然的，我们就会想到，应该把重复的部分抽取出来，只存放一份Ubuntu根目录文件，然后让这一千个镜像以某种方式共享这部分数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（79） 💬（2）<div>关于指令生成层的问题需要再补充哈：只有 RUN, COPY, ADD 会生成新的镜像层，其它指令只会产生临时层，不影响构建大小，官网的镜像构建最佳实践里面有提及

https:&#47;&#47;docs.docker.com&#47;develop&#47;develop-images&#47;dockerfile_best-practices&#47;
Only the instructions RUN, COPY, ADD create layers. Other instructions create temporary intermediate images, and do not increase the size of the build.</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/fb/7fe6df5b.jpg" width="30px"><span>陈卧虫</span> 👍（19） 💬（1）<div>1. 创建和修改文件：通过在写时复制实现；删除文件：通过白障实现，也就是通过一个文件记录已经被删除的文件。
2. 镜像分层的好处：可以重复使用未被改动的layer，每次修改打包镜像，只需重新构建被改动的部分</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/18/edc1b373.jpg" width="30px"><span>风飘，吾独思</span> 👍（18） 💬（1）<div>1.容器最上一层是读写层，镜像所有的层是只读层。容器启动后，Docker daemon会在容器的镜像上添加一个读写层。
2.容器分层可以共享资源，节约空间，相同的内容只需要加载一份份到内存。</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（13） 💬（1）<div>请问下docker pull时输出的layer的值为什么和docker inspect里面layer信息的sha256的值不一样呢？</div>2022-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9b/0f/ef415e32.jpg" width="30px"><span>CK</span> 👍（9） 💬（3）<div>还是没太理解构建上下文的意思，是指docker build的时候指定路径？比如文中示例docker build -f Dockerfile.busybox .  是一个.表示，我执行文末的课下作业时，显示COPY failed: file not found in build context or excluded by .dockerignore: stat default.conf: file does not exist，是不是docker build时的路径没指定好呢
</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（9） 💬（3）<div>ENTRYPOINT 和 CMD 的本质区别是什么的？ 什么时候用 ENTRYPOINT 什么时候用 CMD？</div>2022-06-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL6RvdCzKZCGibZqanPxlib453uP5oXvMTjR6uJsjfMZsib5ShMicDdgBUr6yHSibSKSKgiazqR6tNibDibibQ/132" width="30px"><span>Geek_666217</span> 👍（8） 💬（1）<div>构建包如果出错了，注意注释和内容不要再同一行，会将注释视为参数
</div>2022-09-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3Ey0Uq2w4wLhVNGGReZKLd06PCDU4ZeefZWFMNvf3LibtibDqzBBpzkYW5n5AkYuJGPa4KEdQ5qgA/132" width="30px"><span>Geek_f20da9</span> 👍（6） 💬（2）<div>老师有时间帮忙看一下，不知道写的对不对。

dockerfile常用参数：
1.ARG：镜像层的环境变量
2.FROM：拉取基础镜像
3.COPY:拷贝文件
4.ADD：拷贝文件、URL、压缩文件等
5.EVN：镜像层和容器层参数
6.EXPOSE:暴露容器内部端口给外部使用
7.RUN：执行shell指令
8.CMD：构建完成时执行的指令

思考题：
1.docker采用UNION FS文件系统，将文件系统分为上层和下层。即上层为容器层，下层为镜像层。如果下层有修改，运行容器时，上层会同步修改。如果上层有数据修改（即容器层数据修改），不会影响到下层（即镜像层）。
2.好处：共享已存在的layer，如果有新的数据加入，只会增量在最上层新增layer层。减少了网络传输等一些成本。</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（5） 💬（1）<div>chatgpt的回答
1.容器运行时需要写入数据，但是Docker镜像的分层技术是只读的，这会导致冲突。为了解决这个问题，Docker采用了一种称为“容器层”的技术，用于在镜像的基础上创建一个可写的文件系统层，用于存储容器中的数据和修改。

具体来说，当创建一个新的Docker容器时，Docker会在镜像的基础上创建一个可写的文件系统层，称为“容器层”，用于存储容器中的数据和修改。容器层会覆盖镜像中相应的文件系统层，从而实现容器的个性化定制和隔离。

容器层是可写的，因此容器运行时可以向其中写入数据和修改文件。这些修改都是存储在容器层中的，而不会影响到镜像中的文件系统层。这样可以保证镜像的不变性和可重复性，从而方便镜像的管理和使用。

需要注意的是，容器层是临时的，当容器被删除时，容器层也会被删除。因此，容器层中存储的数据和修改都是临时的，不会对镜像产生影响。如果需要将容器中的数据持久化保存，可以使用Docker的数据卷或者绑定挂载等技术

2.镜像的分层结构带来了以下好处：

减小镜像的大小：镜像的分层结构可以将镜像拆分成多个只读的文件系统层，这些层可以共用相同的Layer，从而减小镜像的大小，提高镜像的构建和传输效率。

提高镜像的可重复性：镜像的分层结构可以保证镜像的不变性和可重复性，因为每个文件系统层都是只读的，不会被修改。这样可以方便镜像的管理和使用。

方便镜像的定制和扩展：镜像的分层结构可以方便镜像的定制和扩展，因为可以在镜像的基础上创建一个可写的容器层，用于存储容器中的数据和修改。这样可以实现容器的个性化定制和隔离。

提高镜像的安全性：镜像的分层结构可以提高镜像的安全性，因为每个文件系统层都是只读的，不会被修改。这样可以避免恶意软件或攻击者修改镜像中的文件，从而提高镜像的安全性。

方便镜像的共享和复用：镜像的分层结构可以方便镜像的共享和复用，因为可以将多个镜像共用相同的Layer，从而减小镜像的大小，提高镜像的构建和传输效率。这样可以方便镜像的共享和复用，提高镜像的可用性和可维护性。</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（4） 💬（1）<div>&quot;Dockerfile 里，第一个指令必须是 FROM，用来选择基础镜像&quot;

一直有个疑问，写Dockerfile都必须有个基础镜像，那么依赖的这些基础镜像 的最原始镜像是怎么制作的？

这里研究了一下文档，同步给大家：

https:&#47;&#47;docs.docker.com&#47;build&#47;building&#47;base-images&#47;#create-a-simple-parent-image-using-scratch

两个方式：

1、Create a full image using tar

2、Create a simple parent image using scratch

特别是 scratch 这个：

You can use Docker’s reserved, minimal image, scratch, as a starting point for building containers. Using the scratch “image” signals to the build process that you want the next command in the Dockerfile to be the first filesystem layer in your image.

While scratch appears in Docker’s repository on the hub, you can’t pull it, run it, or tag any image with the name scratch. Instead, you can refer to it in your Dockerfile.</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/db/921367d6.jpg" width="30px"><span>jone</span> 👍（4） 💬（1）<div>【课下作业】 ，用docker build打好镜像后，即使使用-d，也是会自动退出。如果想要看容器里面刚刚copy和生成的a.txt文件，只能采用： docker run -it ngx-app:1.0 sh ，这样就进入到容器里面了，当然exits之后，就会退出容器了。  老师，这个要怎么理解呢。即使用了-d，也是一次性执行容器。</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（3） 💬（1）<div>老师，课程里面讲的是编写一个docker file，那dockerfile中 FROM的镜像是怎么生成的呢</div>2023-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（2） 💬（1）<div>说实话，容器的内部结构讲解还是没看太明白</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/4c/abb7bfe3.jpg" width="30px"><span>萝卜头王</span> 👍（2） 💬（1）<div>文章中的dockerfile里面的注释信息(以#开头的内容)，是不是应该放在单独的一行？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/3f/4d/7ee1b9e8.jpg" width="30px"><span>宇宙的大洞</span> 👍（1） 💬（1）<div>我可以这样理解 build context, DockerFile 这个构建镜像的逻辑正常执行 所依赖的 文件系统资源</div>2025-01-19</li><br/><li><img src="" width="30px"><span>jingtong</span> 👍（1） 💬（2）<div>虽然这些文件里不包含系统内核（因为容器共享了宿主机的内核），但如果每个镜像都重复做这样的打包操作，仍然会导致大量的冗余。

-----

共享宿主机内核这里如果是Mac上面跑Linux，这个没法共享内核吧，包括不同版本的内核也没法共享？</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（1） 💬（2）<div>1: 构建上下文使用相对路径，是不是当前就是顶层，限制通过 ..&#47; 的方式去到构建上下文的上一层

2. run的指令会生成新的一层，但是如果 【run之前的指令不一样，例如from】【run里面的东西太多】，是不是大部分run生成的这一层都不能重用呢？这一块比较好奇

3. build后的名字为  =&gt; =&gt; naming to docker.io&#47;library&#47;homework。      前面的这个docker.Io&#47;library 这个是默认的吗？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（1） 💬（2）<div>罗老师，我练习了结尾的作业，有一个问题。为什么构建出来的 ngx-app ，通过 docker inspect xxx 查看，它的 Layers 有 8 层呢？在我看来 Dockerfile 只有 7 个命令。还有一个问题，FROM 是否会构建一个层？如果会，为什么之前的 docker build -f Dockerfile.busybox . 的 image 产物通过 docker inspect 查看只有一层 Layer 呢？</div>2022-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/4e/35/d5d1aec8.jpg" width="30px"><span>九暮</span> 👍（1） 💬（1）<div>RUN cd &#47;usr&#47;share&#47;nginx&#47;html \    &amp;&amp; echo &quot;hello nginx&quot; &gt; a.txt
老师，这句话在容器执行，我进入到容器内部结果没有保存下来呢，没有这个文件
</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b8/6a/d37ed9ab.jpg" width="30px"><span>今天你学习了吗？</span> 👍（1） 💬（2）<div>没看到说cow的方法呀，这个从哪说到了呢
</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（1） 💬（2）<div>老师有个问题 层数多少会影响镜像总大小吗 还是不影响 </div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（1） 💬（2）<div>1: docker在挂载镜像文件的时候除了镜像文件的只读层，还会挂载一个‘可读写层’，在容器运行是，它以copy-on-write的方式，记录容器中的“写”操作；
2: a: 镜像分层的好处在于他可以减少制作成本，从而迅速迭代，它使得我们能以一种增量的方式对现有已经存在的镜像做改造，而不是每一次都从0开始重复制作，
        降低了技术人员之间的操作成本；
    b: 占用空间更下，每次拉取和推送都只操作增量的部分，省时省力；</div>2022-06-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（1） 💬（3）<div>作业：
1.写的时候往上叠加一层
2.避免重复打包

课后思考：
万一打包层数过高怎么办？</div>2022-06-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/6F3SZJXIPt9sic45ZoZW0EbPHJnlMaqdXs8iaR39tQNKng7jgT9LqGzBKhc7v6E9BY02nA20dj5xzlpBXCLibCqjQ/132" width="30px"><span>Geek_88f2fe</span> 👍（0） 💬（1）<div>COPY .&#47;a.txt  &#47;tmp&#47;a.txt    # 把构建上下文里的a.txt拷贝到镜像的&#47;tmp目录
请问老师这一行怎么理解呢，构建上下文我的理解是就是要打包的镜像的根目录，那为啥还要再拷贝到镜像中别的地方？为什么不一开始就把需要拷贝的文件放在它的目标目录呢。感觉我对于构建上下文理解的还有问题</div>2025-01-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoREZlw6JWh1OXYvcKhOToBPCSqVr33Vhc0gmW9jNT3JHtW7NtaiaiaNJicjjxyVia7Oec3Qq1bzLGreQ/132" width="30px"><span>Geek_07ead6</span> 👍（0） 💬（1）<div>老师您好，创建dockerfile时都有一个基础镜像，假如我创建了一个dockerfile是基于Ubuntu的，然后里面添加进去的Redis镜像又是基于Centos的，那我这个镜像运行成容器时，里面的Redis是运行在Ubuntu环境的还是centos环境的？</div>2024-03-14</li><br/><li><img src="" width="30px"><span>ZebByte</span> 👍（0） 💬（1）<div> 我想养一条鱼(构建一个自定义镜像)
 我的操作步骤(dockerfile)
 1.上网购买养鱼套餐 (基础镜像)
 2.从套餐里取出资源 (分配好CPU、内存、容量资源)
 3.放好鱼缸
 4.放水
 5.放金鱼	(4、5、6是自定义镜像的过程)
 6.完成养鱼梦想 (构建好了自定义镜像)
 
 此时，我想养些水草 (构建另外一个自定义镜像)
 我的操作步骤(dockerfile)
 1.上网购买养鱼套餐 (基础镜像)
 2.从套餐里取出资源 (分配好CPU、内存、容量资源)
 3.放好鱼缸
 4.放水
 5.放水草	(4、5、6是自定义镜像的过程)
 6.完成养水草梦想 (构建好了自定义镜像)
 
 基于UnionFS（联合文件系统）
 docker不需要重复以上1-4步骤，可以直接在之前养鱼的鱼缸放置水草即可，节省了资源。
 
 水草和鱼  可类比成  redis和nginx等镜像，可以这么理解吗</div>2023-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>default.conf只要在构建的临时目录中存在就可以，不会检查这个文件内容是否真的正确对吧，是否是不是nginx的正确语法配置文件？</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（1）<div>Dockerfile解释

1.构建一个nginx:1.21-alpine的基础镜像；
2.拷贝配置文件到容器的&#47;etc&#47;nginx&#47;conf.d&#47;目录下；
3.切换到&#47;usr&#47;share&#47;nginx&#47;html目录下，并生成一个a.txt文件，内容是hello nginx;
4.暴露容器的8081，8082，8083端口；</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/31/e5/8d45547d.jpg" width="30px"><span>随遇而安</span> 👍（0） 💬（1）<div>老师，您好，想问下镜像的层怎么才算一层？比如乌班图的镜像，那整个乌班图就是镜像中的一层吗？</div>2023-01-31</li><br/><li><img src="" width="30px"><span>Geek_596972</span> 👍（0） 💬（1）<div>生成的镜像放哪呢，跟远程仓库又是什么关系呢</div>2023-01-27</li><br/>
</ul>