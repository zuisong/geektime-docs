你好，我是邢云阳。

在上节课，我从理论的角度，为你讲解了 Wasm 相关的一些知识，包括 Wasm、Wasm VM、用于编写 Wasm 的 SDK，以及跨虚机通信等等。让你对于 Wasm 有了一个初步的认识。

那从本节课开始呢，我们就进入到具体的编码部分。我会先用两节课的时间，让你了解一下如何编写 Wasm 程序。之后便会带领你做 AI 插件。

## Higress Wasm

原生的基于 proxy-wasm-go-sdk 的 Wasm 插件开发比较繁琐，因此 Higress 在这之上封装了一层，从而简化插件开发并且可以增强原生 sdk 的功能。打开 [Higress Wasm 的代码](https://github.com/alibaba/higress/tree/main/plugins/wasm-go/pkg)，可以看到文件结构如下：

```plain
tree
.
├── matcher
│   ├── rule_matcher.go
│   ├── rule_matcher_test.go
│   └── utils.go
└── wrapper
    ├── cluster_wrapper.go
    ├── cluster_wrapper_test.go
    ├── http_wrapper.go
    ├── log_wrapper.go
    ├── plugin_wrapper.go
    ├── redis_wrapper.go
    └── request_wrapper.go
    └── response_wrapper.go
```