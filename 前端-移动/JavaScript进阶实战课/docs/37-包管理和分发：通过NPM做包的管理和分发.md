你好，我是石川。

在前面几讲中，我们看到无论是响应式编程框架React，还是测试用的Jest、Puppeteer工具，亦或是做代码检查和样式优化的ESLint、Prettier工具，都离不开第三方库，而我们在之前的例子中，都是通过NPM下载和安装工具的。

所以，今天我们就来深入了解下NPM以及包的管理和发布。

## 包的发布

NPM（Node Package Manager）虽然它叫做 Node 包管理，但是其实你也可以用它管理或发布用 JavaScript 以外的语言编写的程序的包，只不过NPM最主要的受众还是 JavaScript 在Web和服务器端的开发者。在 NPM 中，有两个核心的概念，一个是包（package），另外一个是模块（module）。

**包**是一个含有 package.json 文件的文件夹。package.json 的作用是对包中的文件或目录的描述。一个包必须含有一个 package.json 文件才能发布到 NPM 的注册列表。

**模块**是任何可以被 Node.js 的 require() 加载的文件或目录。能够被成功加载的模块必须是一个带有 main 字段的 pakcage.json 的目录，或者一个JavaScript的文件。

一个包的发布很简单，首先在命令行通过创建 mkdir 和改变目录 cd 的命令，我们可以创建一个包的文件夹，并导航到包的根目录。在目录下，我们可以创建一个 package.json 的文件。package.js 文件的创建方式有两种，一种是直接创建，另外一种是在命令行上执行 npm init 的命令，通过提示输入后，生成 package.json 的文件。