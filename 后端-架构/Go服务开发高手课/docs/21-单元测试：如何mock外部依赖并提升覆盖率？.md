你好，我是徐逸。

通过前面课程的学习，想必你已经掌握了从编码角度规避代码陷阱的方法，也了解了如何合理地打印日志与返回错误码。然而，即便我们在编码过程中十分谨慎，也无法完全杜绝代码出现问题的可能性。幸运的是，我们能够借助测试手段提前发现潜在的代码问题。而在众多测试手段之中，单元测试有着举足轻重的地位，它能为整个代码库的质量奠定一个坚实的基础。

所以，在今天的课程里，我们就来聊聊单元测试的相关知识，以及 Go 语言中用于单元测试的工具。

## 什么是单元测试？

**所谓单元测试（unit testing），是指对软件中的最小可测试单元进行检查和验证，在 Golang 编程语境里，这通常具体指代单个函数**。单元测试遵循着 AAA（Arrange-Act-Assert）的代码组织结构**，**就像下面的代码一样。

```go
func TestAdd(t *testing.T) {
    // Arrange(安排）
    a := 5
    b := 3
    expected := 8

    // Act（行动）
    result := Add(a, b)

    // Assert（断言）
    assert.Equal(t, expected, result)
}
```

首先在Arrange部分，我们需要准备测试所需的所有前置条件，比如初始化被测试对象、准备输入数据、创建模拟对象（如果有外部依赖）等。接着，在Act部分，我们需要调用被测试的函数或方法，触发实际的行为。最后在Assert部分，需要验证调用的结果是否符合预期。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（1） 💬（1）<div>思考题中说的是 TDD 吗？</div>2025-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/a0/085f8747.jpg" width="30px"><span>『WJ』</span> 👍（0） 💬（1）<div>mocky 比 gomonkey 更好用</div>2025-01-24</li><br/>
</ul>