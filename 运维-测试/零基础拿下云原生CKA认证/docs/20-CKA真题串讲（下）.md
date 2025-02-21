你好，我是雪飞。

上节课我和你一起学习了 CKA 真题的上半部分，这节课，我们继续真题串讲的下半部分。

## 第十题 PV

#### 题目

创建名为 “app-config” 的 Persistent Volume，容量为 1Gi，访问模式为 ReadWriteMany。Volume 类型为 hostPath，位于 /srv/app-config。

#### 答题要点

这道题主要考 hostPath 类型的 PV，知识点参考专栏[第 11 课](https://time.geekbang.org/column/article/795256)，下面我给出参考答案。

#### 参考答案

1. 按照题目要求，编写 PV 的 YAML 文件（pv.yaml）。

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 1Gi  # 题目要求 1Gi
  accessModes:
    - ReadWriteMany  # 题目要求 ReadWriteMany
  hostPath:
    path: "/srv/app-config"   # 注意有引号

```

2. 部署 PV。

```bash
kubectl apply -f pv.yaml
```

#### 验证

查看 PV 状态，检查是否符合题目要求。

```bash
kubectl get pv app-config
```

## 第十一题 PVC

#### 题目

创建一个新的 PersistentVolumeClaim：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（0） 💬（1）<div>可以建个考试的群吗？方便交流下</div>2024-09-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（0） 💬（1）<div>cka 2024 升级，老师可以出更新吗？</div>2024-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/c7/8c2d0a3d.jpg" width="30px"><span>余泽锋</span> 👍（0） 💬（4）<div>老师，昨晚我去考试了，发现家里考试过程网络经经常掉线，考到一半就被退出了，而且感觉 psi 软件很难用，复制粘贴很卡</div>2024-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/c9/6c32bb22.jpg" width="30px"><span>呱呱呱</span> 👍（0） 💬（1）<div>建议再多整点题目串讲的加餐～多谢
</div>2024-09-03</li><br/>
</ul>