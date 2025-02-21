今天，我要跟你分享开发Windows游戏的第一步，建立窗体。

上一节，我讲解Python和C++的编译器，以及它们各自对应的IDE该如何选择，并且测试了C/C++的运行，编译了一个Lua静态库。准备工作基本上算是完成了。

如果你有一些编程功底，应该知道建立Windows的窗体所需的一些基础知识。如果你经验稍丰富一些，还应该知道Delphi、C++Builder、C#等等。这些工具都可以帮助你非常方便地做出一个空白窗体，但是这些窗体并没有游戏的绘图系统，所以它们只是“建立了一个标准窗体”而已。因此，虽然建立窗体是我们这一节的内容，但**我们要探讨的是，在窗体背后，Windows系统做了什么。**

## Windows窗体由哪些部分构成？

我们常规意义上的Windows窗体，由下列几个部分组成。

- **标题栏**：窗口上方的鼠标拖动条区域。标题栏的左边有控制菜单的图标，中间显示的是程序的标题。
- **菜单栏**：位于标题栏的下面，包含很多菜单，涉及的程序所负责的功能不一样，菜单的内容也不一样。比如有些有文件菜单，有些就没有，有一些窗体甚至根本就没有菜单栏。
- **工具栏**：位于菜单栏的下方，工具栏会以图形按钮的形式给出用户最常使用的一些命令。比如，新建、复制、粘贴、另存为等。
- **工作区域**：窗体的中间区域。一般窗体的输入输出都在这里面进行，如果你接触过Windows窗体编程，就知道在这个工作区域能做很多的事情，比如子窗体显示、层叠，在工作区域的子窗体内进行文字编辑等等。你可以理解成，游戏的图形图像就在此处显示。
- **状态栏**：位于窗体的底部，显示运行程序的当前状态。通过它，用户可以了解到程序运行的情况。比如的，如果我们开发出的窗体程序是个编辑器的话，我按了一下Insert键，那么状态栏就会显示Ins缩写；或者点击到哪个编辑区域，会在状态栏出现第几行第几列这样的标注。
- **滚动条**：如果窗体中显示的内容过多，不管横向还是纵向，当前可见的部分不够显示时，窗体就会出现滚动条，分为水平滚动条与垂直滚动条两种。
- **窗体缩放按钮**：窗体的缩放按钮在右上角，在窗体编程中属于System类目。这些缩放按钮依次为最小化、最大化和关闭按钮。

我们来看一张标准的Windows窗体截图，这个软件名是Notepad++。

![](https://static001.geekbang.org/resource/image/cc/af/cc1d248bd1c76405ad73792112c33faf.jpg?wh=735%2A700)

这是MSDN上对于窗体结构的说明：

```
typedef struct tagWNDCLASSEX {
  UINT      cbSize; //结构体大小，等于 sizeof(WNDCLASSEX)
  UINT      style;  //窗体的风格
  WNDPROC   lpfnWndProc; //窗体函数指针
  int       cbClsExtra;  //附加在窗体类后的字节数，初始化是零
  int       cbWndExtra;  //附加在窗体实例化的附加字节数。系统初始化是零，如果一个应用程序使用WNDCLASSEX注册一个通过在资源中使用CLASS指令建立的对话框时，必须把这个成员设成DLGWINDOWEXTRA。
  HINSTANCE hInstance; //该对象的实例句柄
  HICON     hIcon;     //该对象的图标句柄
  HCURSOR   hCursor;   //该对象的光标句柄
  HBRUSH    hbrBackground; //该对象的背景刷子
  LPCTSTR   lpszMenuName;  //菜单指针
  LPCTSTR   lpszClassName;  //类名指针
  HICON     hIconSm;       //与窗体关联的小图标，如果这个值为NULL，那么就把hIcon转换为大小比较合适的小图标
} WNDCLASSEX, *PWNDCLASSEX;
```

## 使用C/C++编写Windows窗体

接下来，我将使用C/C++IDE来编写代码，完成一个默认窗体的开发，并让它运行起来。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/ce/771c25b0.jpg" width="30px"><span>壬大师</span> 👍（1） 💬（1）<div>老师，python能开发手机游戏吗，游戏引擎用的是pygame吗？</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/05/582fd240.jpg" width="30px"><span>@浩</span> 👍（1） 💬（1）<div>用QT写窗口如何，MFC有点晦涩难懂。</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/4d/c57092e4.jpg" width="30px"><span>立春</span> 👍（1） 💬（1）<div>C++用的是MFC了……</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/cc/dfe92ee1.jpg" width="30px"><span>宋桓公</span> 👍（0） 💬（1）<div>最大化，加无边框等于全屏</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/ce/771c25b0.jpg" width="30px"><span>壬大师</span> 👍（0） 💬（1）<div>老师，那手游的开发目前也都是C++咯？像简单游戏比如手机棋牌类游戏一般用什么语言？</div>2018-06-13</li><br/><li><img src="" width="30px"><span>呵呵</span> 👍（0） 💬（1）<div>用c++建立窗体，默认用的什么图形库？</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/26/3f35f1f3.jpg" width="30px"><span>Geek_King@技术爱好者</span> 👍（10） 💬（0）<div>c++窗口那段程序，编译时需加上-mwindows或者-lgdi32,又或者在建工程的时候选择建立gui程序🙄🙄🙄</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ba/6d318c08.jpg" width="30px"><span>GS</span> 👍（4） 💬（0）<div>python3 要用小写的tkinter</div>2018-07-28</li><br/><li><img src="" width="30px"><span>呵呵</span> 👍（4） 💬（0）<div>要是能提供远嘛就好了，跟着后面敲太麻烦</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/f3/77223a8c.jpg" width="30px"><span>清新灬小柠檬</span> 👍（1） 💬（0）<div>直接将显示器的大小当作参数传到绘制窗体的函数中？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/b4/0808999d.jpg" width="30px"><span>白马</span> 👍（1） 💬（0）<div>是调用windows api中获取当前屏幕窗口尺寸的方法获得吗？</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-03-15</li><br/><li><img src="" width="30px"><span>Geek_569f22</span> 👍（0） 💬（0）<div>windows那个照着输入，生成不了窗口，python那个可以</div>2021-06-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（0） 💬（0）<div>python3导入模块要改小写，调用tk库的方法时也要改小写，就可以用了。一开始还担心要c++等一堆软件。</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/92/1e/c108b65a.jpg" width="30px"><span>louis</span> 👍（0） 💬（0）<div>把窗体的大小设置为屏幕大小，设置屏幕的起始位置设置为（0，0）吗？具体调用什么函数不清楚。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/65/c22b4415.jpg" width="30px"><span>风华神使</span> 👍（0） 💬（0）<div>楼上，cxx默认不用图形库，用winapi</div>2018-06-09</li><br/>
</ul>