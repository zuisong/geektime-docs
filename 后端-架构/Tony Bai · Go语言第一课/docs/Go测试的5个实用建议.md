你好，我是Tony Bai。

在[《Go语言第一课》](http://gk.link/a/10AVZ)专栏中，缺少专门讲解Go测试的章节，这无疑是一个遗憾。在工程实践中，针对代码的测试是确保代码执行逻辑正确和代码质量的重要手段。所以，Go测试内容的空缺可能会让一些小伙伴在学习和实践过程中感到困惑。

为了解决这个问题，我决定用一篇加餐详细补充说明。我将带你快速入门Go测试的基本知识点，并针对实际开发中的Go测试实践提供几点实用建议。这不仅仅是一篇加餐，更是帮助你完善Go语言知识体系的重要一环。

## Go测试快速入门

Go语言内置了一个轻量级的测试框架，该框架通过 **go test命令**和标准库的 **testing 包**来提供测试功能。

Go测试框架要求所有Go测试代码都要放在以\_test.go结尾的测试源文件中。Go测试被抽象为一个个测试函数，测试源文件中的测试函数必须以Test开头，并且接受一个名为testing.T的参数，比如下面示例代码中的TestAdd函数：

```plain
// go-testing/add/add_test.go
package add


import (
    "testing"
)


func TestAdd(t *testing.T) { 
    got := Add(2, 3)
    want := 5 
    if got != want { 
        t.Errorf("want %d, but got %d", want, got)
    } 
}
```