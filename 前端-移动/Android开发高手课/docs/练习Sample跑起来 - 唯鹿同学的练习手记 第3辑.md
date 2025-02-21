没想到之前的写的练习心得得到了老师的认可，看来我要更加认真努力练习了。今天来练习第22、27、ASM这三课的Sample。

[**Chapter22**](https://github.com/AndroidAdvanceWithGeektime/Chapter22)

> 尝试使用Facebook ReDex库来优化我们的安装包。

**准备工作**

首先是下载ReDex：

```
git clone https://github.com/facebook/redex.git
cd redex
```

接着是安装：

```
autoreconf -ivf && ./configure && make -j4
sudo make install
```

在安装时执行到这里，报出下图错误：

![](https://static001.geekbang.org/resource/image/40/fa/40ba14544153f1ef67bfd21a884c1efa.jpg?wh=1385%2A604)

其实就是没有安装Boost，所以执行下面的命令安装它。

```
brew install boost jsoncpp
```

安装Boost完成后，再等待十几分钟时间安装ReDex。

下来就是编译我们的Sample，得到的安装包信息如下。

![](https://static001.geekbang.org/resource/image/bc/0b/bcf38372f4d9315b9d288607e437040b.jpeg?wh=1446%2A899)

可以看到有三个Dex文件，APK大小为13.7MB。

**通过ReDex命令优化**

为了让我们可以更加清楚流程，你可以输出ReDex的日志。

```
export TRACE=2
```

去除Debuginfo的方法，需要在项目根目录执行：

```
redex --sign -s ReDexSample/keystore/debug.keystore -a androiddebugkey -p android -c redex-test/stripdebuginfo.config -P ReDexSample/proguard-rules.pro  -o redex-test/strip_output.apk ReDexSample/build/outputs/apk/debug/ReDexSample-debug.apk
```

上面这段很长的命令，其实可以拆解为几部分：

- `--sign` 签名信息
- `-s`（keystore）签名文件路径
- `-a`（keyalias）签名的别名
- `-p`（keypass）签名的密码
- `-c` 指定ReDex的配置文件路径
- `-P` ProGuard规则文件路径
- `-o` 输出的文件路径
- 最后是要处理APK文件的路径
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/92/f3dabcb1.jpg" width="30px"><span>小小代码</span> 👍（1） 💬（1）<div>试了下Redex去除Dex文件Debuginfo行号信息的功能，发现行号由正确的com.sample.redex.MainActivity.onCreate(MainActivity.java:20)变为不正确的com.sample.redex.MainActivity.onCreate(Unknown Source:13)，并没有像支付宝所说的变成-1</div>2019-04-13</li><br/>
</ul>