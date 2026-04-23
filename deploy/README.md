# CHINAPLAS 发布与接入说明

## 仓库内发布链路

`main` 推送 -> GitHub Actions `release.yml` -> K8s Kaniko Job -> registry.144.91.77.245.sslip.io -> 回写 `deploy/overlays/prod/kustomization.yaml` -> ArgoCD 自动同步。

## 必需的 GitHub Secrets

- `KUBECONFIG_B64`

镜像默认推送到 `registry.144.91.77.245.sslip.io/chinaplas`，构建和运行统一复用集群内稳定的 `registry-push` 凭据副本。

## Cloudflare 与 Porkbun

1. 在 Cloudflare 添加 `chinaplas.lol` zone。
2. 把 Porkbun nameserver 改成 Cloudflare 分配的 nameserver。
3. 在 Cloudflare 为 `chinaplas.lol` 配置生产记录，指向实际 ingress/LB，并开启代理。
4. 将 SSL/TLS 设为 `Full (strict)`，开启 HTTP 到 HTTPS 跳转。

## GSC

1. 在 Google Search Console 中创建 `chinaplas.lol` Domain property。
2. 使用 Cloudflare DNS TXT 完成验证。
3. 提交 `https://chinaplas.lol/sitemap.xml`。

## 上线后验证

- `npm test`
- `npm run test:prod-browser`
- `curl -I https://chinaplas.lol`
- `curl https://chinaplas.lol/healthz`
