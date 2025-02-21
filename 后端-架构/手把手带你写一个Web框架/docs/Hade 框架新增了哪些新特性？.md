你好，我是轩脉刃。

在专栏中，我们一起开发了一款名为Hade的Golang HTTP框架。Hade框架旨在为开发者提供一个高效、灵活且易于使用的开发工具，帮助他们更快速地构建高性能的Web应用。

在过去的两年间，我不断完善Hade框架，持续引入新的功能和特性。这些改进不仅提升了框架的性能和稳定性，还极大地扩展了其应用场景。

今天，我想借此机会，向你详细介绍一下Hade框架的改进，以及新增的主要特性和功能。

# 提供安全的 Go 封装

在业务代码开发过程中，我们经常使用goroutine关键字来创建一个协程执行一段业务，甚至开启多个goroutine并行执行多个业务逻辑。但是在实际开发过程中，很容易出现新启动的goroutine忘记捕获panic错误，而导致整个进程挂掉的情况。

所以，我为Hade框架增加了2个方法：goroutine.SafeGo和goroutine.SafeGoAndWait。

## SafeGo

SafeGo这个函数是一个安全的goroutine启动函数，主要用于包装普通的goroutine，增加了错误恢复（panic recovery）和日志记录功能。它主要适用于业务中需要开启异步goroutine业务逻辑调用的场景。