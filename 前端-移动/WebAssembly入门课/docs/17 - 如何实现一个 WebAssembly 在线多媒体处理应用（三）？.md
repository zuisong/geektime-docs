你好，我是于航。

在上一节课中，我们已经完成了本次实践项目的其中一个核心部分，也就是由 JavaScript 实现的滤镜函数。并且还同时完成了整个 Web 应用与用户的 UI 交互控制部分、视频图像的渲染和绘制逻辑，以及帧率计算逻辑及显示逻辑。

在这节课里，我们将一起来完成整个应用的另外一个核心部分，同时也是整个实践的主角。让我们来看看，相较于 JavaScript 滤镜函数，由 Wasm 实现的同版本滤镜函数会带来怎样的性能提升呢？

## 编写 C/C++ 函数源码

首先，为了能够得到对应 Wasm 字节码格式的函数实现，我们需要首先准备由 C/C++ 等高级语言编写的源代码，然后再通过 Emscripten 将其编译到 Wasm 格式。这部分代码的主要逻辑，与上一篇中的 JavaScript 版本滤镜函数其实现逻辑基本相同。代码如下所示：

```
// dip.cc
// 引入必要的头文件；
#include <emscripten.h>
#include <cmath>
// 宏常量定义，表示卷积核矩阵的高和宽；
#define KH 3
#define KW 3
// 声明两个数组，分别用于存放卷积核数据与每一帧对应的像素点数据；
char kernel[KH][KW];
unsigned char data[921600];
// 将被导出的函数，放置在 extern "C" 中防止 Name Mangling；
extern "C" {
  // 获取卷积核数组的首地址；
  EMSCRIPTEN_KEEPALIVE auto* cppGetkernelPtr() { return kernel; }
  // 获取帧像素数组的首地址；
  EMSCRIPTEN_KEEPALIVE auto* cppGetDataPtr() { return data; }
  // 滤镜函数；
  EMSCRIPTEN_KEEPALIVE void cppConvFilter(
    int width, 
    int height,
    int divisor) {
    const int half = std::floor(KH / 2);
    for (int y = half; y < height - half; ++y) {
      for (int x = half; x < width - half; ++x) {
        int px = (y * width + x) * 4;
        int r = 0, g = 0, b = 0;
        for (int cy = 0; cy < KH; ++cy) {
          for (int cx = 0; cx < KW; ++cx) {
            const int cpx = ((y + (cy - half)) * width + (x + (cx - half))) * 4;
            r += data[cpx + 0] * kernel[cy][cx];
            g += data[cpx + 1] * kernel[cy][cx];
            b += data[cpx + 2] * kernel[cy][cx];
          }
        }                 
        data[px + 0] = ((r / divisor) > 255) ? 255 : ((r / divisor) < 0) ? 0 : r / divisor;
        data[px + 1] = ((g / divisor) > 255) ? 255 : ((g / divisor) < 0) ? 0 : g / divisor;
        data[px + 2] = ((b / divisor) > 255) ? 255 : ((b / divisor) < 0) ? 0 : b / divisor;
      }
    }
  }
}
```

在这段代码中，我们将定义的所有函数均以 “cpp” 作为其前缀来命名，表明这个函数的实际定义来自于对应的 C/C++ 代码实现。其中，“cppConvFilter” 函数为主要的滤镜计算函数。在该函数中，我们保持着几乎与上一节课中，JavaScript 版滤镜函数同样的实现逻辑。

在代码的开始，我们首先以 “#include” 的方式，包含了很多需要使用到的 C/C++ 头文件。其中 “emscripten.h” 头文件便由 Emscripten 工具链提供，其中包含着众多与 Wasm 编译相关的宏和函数定义。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKNfFksicibcQH0juiaia16NdasApA9RoqIxA1p8yVU2hjjuYmQakyHmh1gu9bIHDT57atX2GpJobosnw/132" width="30px"><span>huge</span> 👍（2） 💬（1）<div>我照着例子，试着编译一段求md5的代码，
使用#include &lt;openssl&#47;md5.h&gt;

报错：fatal error: &#39;openssl&#47;md5.h&#39; file not found

这种依赖第三方库的情况，怎么处理呢</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e8/31df61df.jpg" width="30px"><span>军秋</span> 👍（1） 💬（1）<div>编译提示：clang-6.0: error: unsupported option &#39;--no-entry&#39; 是我版本太低了吗？ clang的官方文档也没找到--no-entry 选项。
emcc -v
emcc (Emscripten gcc&#47;clang-like replacement + linker emulating GNU ld) 1.39.4
clang version 6.0.1 (https:&#47;&#47;github.com&#47;emscripten-core&#47;emscripten-fastcomp-clang 98df4be387dde3e3918fa5bbb5fc43e1a0e1daac) (https:&#47;&#47;github.com&#47;emscripten-core&#47;emscripten-fastcomp 6c7e775325067e33fa60611e619a8b987b6d0c35) (emscripten 1.38.44 : 1.38.31)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: &#47;emsdk_portable&#47;clang&#47;tag-e1.39.4&#47;build_tag-e1.39.4_64&#47;bin
Found candidate GCC installation: &#47;usr&#47;lib&#47;gcc&#47;x86_64-linux-gnu&#47;6
Found candidate GCC installation: &#47;usr&#47;lib&#47;gcc&#47;x86_64-linux-gnu&#47;6.3.0
Selected GCC installation: &#47;usr&#47;lib&#47;gcc&#47;x86_64-linux-gnu&#47;6.3.0
Candidate multilib: .;@m64
Selected multilib: .;@m64
shared:INFO: (Emscripten: Running sanity checks)</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b4/bb/73586c43.jpg" width="30px"><span>张凯</span> 👍（1） 💬（1）<div>大致思路表述明白了，WebAssembly.instantiate这个函数是我们写在JS中?</div>2020-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（0） 💬（1）<div>基于 OpenGL 编写的 C&#47;C++ 应用编译成 Wasm Web 应用，而无需做任何源代码上的修改。Emscripten 会通过相应的 JavaScript 胶水代码来处理好 OpenGL 与 WebGL 的调用映射关系，让你真正地做到“无痛迁移”。
请问目前有没有开源的例子啊？</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/79/3f/a6f93afe.jpg" width="30px"><span>Andy</span> 👍（0） 💬（1）<div>老师：
如果有一个cc文件，要编出来wasm，如下这些写非常简单
emcc dip.cc -s WASM=1 -O3 --no-entry -o dip.wasm

但是如果有很多cc文件，并且在不同的路径中，上面这个命令应该怎么写？
如果这些cc依赖第三方库，比如opencv，应该怎么编译？
如果我们自己的cc文件之前都是用cmake编译的，现在要想编译出来wasm，应该怎么做？

谢谢啦</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/69/27/b6358f79.jpg" width="30px"><span>champ</span> 👍（0） 💬（3）<div>我是这样计算帧率的：

const records = []
let lastDrawTime = 0

function draw() {
    if (lastDrawTime !== 0) {
        const duration = Date.now() - lastDrawTime
        records.push(duration)
    }
    lastDrawTime = Date.now()

    &#47;&#47;...

    setTimeout(draw, 0)
}
这样算出来的帧率，在不开启渲染的情况下为170FPS左右，js渲染为80FPS左右，wasm渲染为95FPS左右，好像性能提升并不是很明显。

另外，我发现同样的算法，wasm算出来的图像显示效果要比js算出来的好很多，不知道是什么原因？
老师能解答下吗？</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/c3/9f/2a2d302f.jpg" width="30px"><span>humanwin</span> 👍（1） 💬（0）<div>有2个疑问：
1）c&#47;c++的全局变量编译为wasm后内存是对应到线性内存段，这个规则在哪个文档中可以看到呢？（搜索了一圈好像没找到）。
2）wasm不是有个global section嘛，为什么c&#47;c++的全局变量不是放到那里呢？</div>2023-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d5/b0/8c60ac4c.jpg" width="30px"><span>Zion</span> 👍（1） 💬（0）<div>2019年的时候，了解了几个月webassembly，由于自身原因当时的感觉就是：webassembly只能做些数据转换加密.希望作者再出一些实用webassembly的课程</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>数据不能有更好地传递方式吗？我觉得通过直接设置线性内存的内容我不太能接受，不能直接把数据通过 WASM 方法的参数送进去吗？</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/42/e1757583.jpg" width="30px"><span>Jason Yu 于航</span> 👍（0） 💬（1）<div>源码可以参考这里：https:&#47;&#47;github.com&#47;Becavalier&#47;geektime-wasm-tutorial。</div>2021-04-29</li><br/>
</ul>