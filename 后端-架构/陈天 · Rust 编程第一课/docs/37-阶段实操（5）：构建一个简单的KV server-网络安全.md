你好，我是陈天。

上一讲我们完成了KV server整个网络部分的构建。而安全是和网络密不可分的组成部分，在构建应用程序的时候，一定要把网络安全也考虑进去。当然，如果不考虑极致的性能，我们可以使用诸如 gRPC 这样的系统，在提供良好性能的基础上，它还通过 [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) 保证了安全性。

那么，当我们的应用架构在 TCP 上时，如何使用 TLS 来保证客户端和服务器间的安全性呢？

## 生成 x509 证书

想要使用 TLS，我们首先需要 [x509 证书](https://en.wikipedia.org/wiki/X.509)。TLS 需要 x509 证书让客户端验证服务器是否是一个受信的服务器，甚至服务器验证客户端，确认对方是一个受信的客户端。

为了测试方便，我们要有能力生成自己的 CA 证书、服务端证书，甚至客户端证书。证书生成的细节今天就不详细介绍了，我之前做了一个叫 [certify](https://github.com/tyrchen/certify) 的库，可以用来生成各种证书。我们可以在 Cargo.toml 里加入这个库：

```rust
[dev-dependencies]
...
certify = "0.3"
...
```

然后在根目录下创建 fixtures 目录存放证书，再创建 examples/gen\_cert.rs 文件，添入如下代码：

```rust
use anyhow::Result;
use certify::{generate_ca, generate_cert, load_ca, CertType, CA};
use tokio::fs;

struct CertPem {
    cert_type: CertType,
    cert: String,
    key: String,
}

#[tokio::main]
async fn main() -> Result<()> {
    let pem = create_ca()?;
    gen_files(&pem).await?;
    let ca = load_ca(&pem.cert, &pem.key)?;
    let pem = create_cert(&ca, &["kvserver.acme.inc"], "Acme KV server", false)?;
    gen_files(&pem).await?;
    let pem = create_cert(&ca, &[], "awesome-device-id", true)?;
    gen_files(&pem).await?;
    Ok(())
}

fn create_ca() -> Result<CertPem> {
    let (cert, key) = generate_ca(
        &["acme.inc"],
        "CN",
        "Acme Inc.",
        "Acme CA",
        None,
        Some(10 * 365),
    )?;
    Ok(CertPem {
        cert_type: CertType::CA,
        cert,
        key,
    })
}

fn create_cert(ca: &CA, domains: &[&str], cn: &str, is_client: bool) -> Result<CertPem> {
    let (days, cert_type) = if is_client {
        (Some(365), CertType::Client)
    } else {
        (Some(5 * 365), CertType::Server)
    };
    let (cert, key) = generate_cert(ca, domains, "CN", "Acme Inc.", cn, None, is_client, days)?;

    Ok(CertPem {
        cert_type,
        cert,
        key,
    })
}

async fn gen_files(pem: &CertPem) -> Result<()> {
    let name = match pem.cert_type {
        CertType::Client => "client",
        CertType::Server => "server",
        CertType::CA => "ca",
    };
    fs::write(format!("fixtures/{}.cert", name), pem.cert.as_bytes()).await?;
    fs::write(format!("fixtures/{}.key", name), pem.key.as_bytes()).await?;
    Ok(())
}
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（12） 💬（1）<div>ca 证书和 tls什么关系呢？
另外为何以前做网站的时候证书都要向运营商购买申请？那个是什么证书</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>生成证书这块是我比较欠缺的知识，可以好好补充一下了。</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（0）<div>服务器这里不应该直接 ? 退出：let stream = tls.accept(stream).await?;
暂时可改成：
let stream = match tls.accept(socket).await {
    Ok(stream) =&gt; stream,
    Err(e) =&gt; {
        error!(&quot;failed to accept connection: {}&quot;, e);
        continue;
    }
};</div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>不太懂，但是代码能跑！</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/08/2b/7a1fb4ff.jpg" width="30px"><span>David.Du</span> 👍（0） 💬（0）<div>感谢大神！</div>2023-11-30</li><br/><li><img src="" width="30px"><span>新新人类</span> 👍（0） 💬（0）<div>思考题1: 将 ServerConfig 的 ClientCertVerifier 改成 AllowAnyAuthenticatedClient

pub fn new(cert: &amp;str, key: &amp;str, client_ca: Option&lt;&amp;str&gt;) -&gt; Result&lt;Self, KvError&gt; {
    let certs = load_certs(cert)?;
    let key = load_key(key)?;

    let mut root_store = match rustls_native_certs::load_native_certs() {
      Ok(store) | Err((Some(store), _)) =&gt; store,
      Err((None, err)) =&gt; {
        return Err(err.into());
      }
    };
    &#47;&#47; 如果有签署客户端的 CA 证书，则加载它，这样客户端证书不在根证书链
    &#47;&#47; 但是这个 CA 证书能验证它，也可以
    if let Some(cert) = client_ca {
      let mut buf = Cursor::new(cert);
      root_store.add_pem_file(&amp;mut buf).unwrap();
    }
    &#47;&#47; 加载 server cert &#47; CA cert，生成 ServerConfig
    let mut config = ServerConfig::new(AllowAnyAuthenticatedClient::new(root_store));

    &#47;&#47; 加载服务器证书
    config
      .set_single_cert(certs, key)
      .map_err(|_| KvError::CertificateParseError(&quot;server&quot;, &quot;cert&quot;))?;
    config.set_protocols(&amp;[Vec::from(&amp;ALPN_KV[..])]);

    Ok(Self {
      inner: Arc::new(config),
    })
  }</div>2022-05-14</li><br/>
</ul>