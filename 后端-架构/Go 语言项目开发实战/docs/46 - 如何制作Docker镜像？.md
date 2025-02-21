你好，我是孔令飞。

要落地云原生架构，其中的一个核心点是通过容器来部署我们的应用。如果要使用容器来部署应用，那么制作应用的Docker镜像就是我们绕不开的关键一步。今天，我就来详细介绍下如何制作Docker镜像。

在这一讲中，我会先讲解下Docker镜像的构建原理和方式，然后介绍Dockerfile的指令，以及如何编写Dockerfile文件。最后，介绍下编写Dockerfile文件时要遵循的一些最佳实践。

## Docker镜像的构建原理和方式

首先，我们来看下Docker镜像构建的原理和方式。

我们可以用多种方式来构建一个Docker镜像，最常用的有两种：

- 通过`docker commit`命令，基于一个已存在的容器构建出镜像。
- 编写Dockerfile文件，并使用`docker build`命令来构建镜像。

上面这两种方法中，镜像构建的底层原理是相同的，都是通过下面3个步骤来构建镜像：

1. 基于原镜像，启动一个Docker容器。
2. 在容器中进行一些操作，例如执行命令、安装文件等。由这些操作产生的文件变更都会被记录在容器的存储层中。
3. 将容器存储层的变更commit到新的镜像层中，并添加到原镜像上。

下面，我们来具体讲解这两种构建Docker镜像的方式。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5suA7q5mM40ULTY5OlQpoerPRMQD8NcMbKxDHhNmjQNUCngkSJEzRvMVDibAHw2whGZxAFlibzribOA/132" width="30px"><span>jxlwqq</span> 👍（28） 💬（1）<div>自荐一个dockerfile的写法：

```Dockerfile
# 多阶段构建：提升构建速度，减少镜像大小

# 从官方仓库中获取 1.17 的 Go 基础镜像
FROM golang:1.17-alpine AS builder

# 设置工作目录
WORKDIR &#47;workspace

# 安装项目依赖
COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

# 复制项目文件，这一步按需复制
COPY . .

# 构建名为&quot;app&quot;的二进制文件
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -o app main.go

# 获取 Distroless 镜像，只有 650 kB 的大小，是常用的 alpine:latest 的 1&#47;4
FROM gcr.io&#47;distroless&#47;static:nonroot
# 设置工作目录
WORKDIR &#47;
# 将上一阶段构建好的二进制文件复制到本阶段中
COPY --from=builder &#47;workspace&#47;app .
# 设置监听端口
EXPOSE 8080
# 配置启动命令
ENTRYPOINT [&quot;&#47;app&quot;]
```</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（7） 💬（1）<div>官方文档中最佳实践有介绍，RUN, COPY, ADD 三个指令会创建层，其他指令会创建一个中间镜像，并且不会影响镜像大小。这样我们说的指令合并也就是以这三个指令为主。当然了docker history查看构建历史与镜像大小，更为易读和简约</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（2） 💬（1）<div>感觉介绍IAM项目本身的相关内容少了点，像Docker相关的知识，其实给大家推荐一下资料就可以了。</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/84/5b7d4d95.jpg" width="30px"><span>冷峰</span> 👍（0） 💬（1）<div>go get 依赖 git 的吧， 不装 git , go get 能运行吗？ </div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（0） 💬（1）<div>老师想确认下，第二阶段的FROM busybox是会覆盖掉第一阶段的FROM是嘛，只是用第一阶段进行编译而已，然后用第二阶段的镜像去运行app</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（0）<div>总结：
容器镜像的构建主要是通过Dockerfile来完成，构建过程如下：
1. 创建一个临时目录，将Context中的文件解压到该目录；
2. 执行Dockfile中的命令，一般是顺序执行，如果是多阶段构建，也会并行执行指令。
3. Docker Daemon 会为每条指令创建一个临时容器，执行该指令，生成镜像层，并缓存该镜像层。
4. 最终，将所有镜像层进行合并，生成最后的容器镜像。

最佳实践：
Dockerfile指令大写；From 选择官方容器镜像，指定镜像的tag；
使用尽量少地层：构建时将相同指令的内容放到一层；不要在Dockerfile中修改文件权限；采用多阶段构建，大幅减少容器镜像的体积。
充分利用缓存：不易修改的指令放在前面。
推荐使用COPY而非ADD；ENTRYPOINT和CMD结合使用。</div>2021-12-05</li><br/>
</ul>