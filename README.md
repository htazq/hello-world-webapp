# 云计算运维工程师面试题 - 实操部分

本项目旨在完成一个简单的 "Hello World" Web 应用程序的容器化部署和 CI/CD 流程。

## 架构设计与技术选型

* **应用程序:** 使用 Python Flask 框架编写的简单 "Hello World" 应用。
* **容器化:** 使用 Docker 将 Flask 应用打包成镜像，确保环境一致性。
* **容器镜像仓库:** 选择 Docker Hub 存储构建好的 Docker 镜像。**(请替换为你自己的 Docker Hub 仓库)**
* **部署环境:** **明确选择使用预先存在的、由多台 VPS 搭建的 K3s 集群**。选择 K3s 是因为它轻量、易于在现有 VPS 上部署，并且能充分展示 Kubernetes 的核心运维能力。
* **基础设施即代码 (IaC):**
    * **核心方法:** **使用 Kubernetes 原生的 YAML 文件 (`deployment.yaml`, `service.yaml`) 作为本次任务的 IaC 实现**。这些文件以声明式的方式定义了应用在 Kubernetes 集群中的部署状态（如副本数、镜像版本）和服务暴露方式（NodePort）。
    * **与传统 IaC 的关系:** 这符合 IaC 的核心理念，即用代码管理配置。虽然未使用 Terraform/CloudFormation 等工具来创建底层的 VPS 或 K3s 集群本身（因为它们是预置环境），但 K8s YAML 文件有效地自动化和管理了**应用层**的基础设施配置。如果任务要求从零在公有云创建所有资源，则会使用 Terraform 等工具管理 VM、网络等。
* **CI/CD:** 使用 GitHub Actions 实现自动化流程。当代码推送到 `main` 分支时，自动构建 Docker 镜像，推送到 Docker Hub，并使用 `kubectl` 更新 K3s 集群中的应用部署。
* **访问方式:** 通过 Kubernetes Service 的 `NodePort` 类型暴露应用。用户可以通过访问任一 K3s 集群节点的 `公网 IP:NodePort` 来访问应用。

## 部署方式选择说明

* **选择:** 本项目采用**在现有的 VPS K3s 集群上部署**的方式。
* **原因:**
    1.  **资源利用:** 充分利用已有的 VPS 资源，避免在公有云上产生额外的、可能超出免费额度的费用。
    2.  **技能展示:** 直接操作 Kubernetes 集群更能体现容器编排和管理的实际运维能力。
    3.  **符合要求:** 满足了任务中关于容器化、IaC (通过 K8s YAML)、CI/CD 和可访问性的核心要求，同时也是题目允许的备选方案精神的体现（利用现有或模拟环境）。

## 先决条件

1.  **Git:** 用于代码版本控制。
2.  **Docker:** 用于本地构建和测试 Docker 镜像 (可选，CI/CD 会处理)。
3.  **kubectl:** 用于与你的 K3s 集群交互 (需要预先配置好指向你的集群)。
4.  **一个可用的 K3s 集群:** 部署在你的 VPS 上，并且你的 CI/CD 环境 (GitHub Actions Runner) 或本地环境能够访问其 API Server。
5.  **Docker Hub 账号:** 用于存储 Docker 镜像。
6.  **GitHub 账号:** 用于托管代码和运行 GitHub Actions。

## 配置 GitHub Secrets

为了让 GitHub Actions 能够推送到 Docker Hub 和访问你的 K3s 集群，需要在你的 GitHub 仓库中配置以下 Secrets (`Settings -> Secrets and variables -> Actions -> New repository secret`):

* `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名。
* `DOCKERHUB_TOKEN`: 你的 Docker Hub 访问令牌 (在 Docker Hub `Account Settings -> Security -> New Access Token` 创建)。
* `K3S_KUBECONFIG`: 你的 K3s 集群的 `kubeconfig` 文件内容。通常可以在 K3s master 节点的 `/etc/rancher/k3s/k3s.yaml` 找到。**请确保 Kubeconfig 中的 `server` 地址是你的 K3s master 节点的公网 IP 或 GitHub Actions Runner 可访问的地址，并且 API Server 端口（默认为 6443）已在防火墙中对 Runner 开放访问。**

## 代码文件说明

* `app.py`: Flask "Hello World" Web 应用程序源代码。
* `requirements.txt`: Python 依赖列表 (仅 Flask)。
* `Dockerfile`: 用于构建应用 Docker 镜像的指令文件。
* `deployment.yaml`: Kubernetes Deployment 配置文件 (定义 Pod 模板)。
* `service.yaml`: Kubernetes Service 配置文件 (使用 NodePort 暴露服务)。
* `.github/workflows/main.yml`: GitHub Actions CI/CD 工作流配置文件。
* `README.md`: 本说明文档。

## 如何部署和访问

### 方法一：使用 CI/CD 自动部署 (推荐)

1.  **Fork/Clone 仓库:** 将此仓库 Fork 到你自己的 GitHub 账号，或者 Clone 到本地。
2.  **修改配置:**
    * 在 `deployment.yaml` 中，将 `image: your-dockerhub-username/your-repo-name:latest` 替换为你自己的 Docker Hub 镜像地址。
    * 在 `.github/workflows/main.yml` 中，将 `tags: your-dockerhub-username/your-repo-name:latest` (以及可选的 `set image` 命令中的镜像名) 替换为你自己的 Docker Hub 仓库名。
3.  **配置 Secrets:** 按照 "配置 GitHub Secrets" 部分的说明，在你的 GitHub 仓库中设置必要的 Secrets。
4.  **推送代码:** 将修改后的代码推送到你的 GitHub 仓库的 `main` 分支。
5.  **触发 Action:** GitHub Actions 将自动触发，执行构建、推送和部署流程。你可以在仓库的 "Actions" 标签页查看进度。

### 方法二：手动部署

1.  **构建并推送镜像:**
    ```bash
    # 登录 Docker Hub
    docker login -u YOUR_DOCKERHUB_USERNAME

    # 构建镜像 (确保在包含 Dockerfile 的目录下运行)
    # 将 your-dockerhub-username/your-repo-name 替换为你自己的仓库名
    docker build -t your-dockerhub-username/your-repo-name:latest .

    # 推送镜像
    docker push your-dockerhub-username/your-repo-name:latest
    ```
2.  **修改 Kubernetes 配置:**
    * 在 `deployment.yaml` 中，确保 `image` 字段指向你刚刚推送的镜像地址和标签。
3.  **连接 K3s 集群:** 确保你的 `kubectl` 已配置为指向你的 K3s 集群。
4.  **应用 Kubernetes 配置:**
    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

### 访问应用

1.  **获取 NodePort:** 执行以下命令查看 `url-fetcher-service` (或者你修改后的服务名) 分配到的 NodePort：
    ```bash
    # 假设你的 service 名称是 url-fetcher-service
    kubectl get svc url-fetcher-service
    ```
    输出会类似这样：
    ```
    NAME                  TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
    url-fetcher-service   NodePort   10.43.xxx.xxx   <none>        80:YYYYY/TCP   1m
    ```
    其中 `YYYYY` 就是分配的 NodePort (范围通常是 30000-32767)。

2.  **获取节点公网 IP:** 获取你 K3s 集群中**任意一个 Worker 节点**（或 Master 节点，如果它也承载工作负载）的公网 IP 地址。

3.  **访问:** 在浏览器中打开 `http://<节点公网IP>:<NodePort>` (例如 `http://123.45.67.89:YYYYY`)。

4.  **防火墙:** **确保你的 VPS 防火墙允许从公网访问该 NodePort 端口 `YYYYY`**。

## 成本估算

* **主要成本:** 你为现有 VPS 支付的租赁费用。
* **其他:** Docker Hub 和 GitHub Actions 在免费额度内通常足够用于此项目。

## 安全性考虑

* **Kubeconfig 安全:** `K3S_KUBECONFIG` Secret 包含集群的完全访问凭证，务必妥善保管，限制知晓范围。
* **K3s API Server 访问:** 确保只有受信任的 IP (例如 GitHub Actions Runner 的 IP 范围) 才能访问 K3s API Server 的端口 (默认 6443)。
* **Docker Hub Token:** 使用具有最小推送权限的访问令牌。
* **NodePort 暴露:** `NodePort` 会在所有节点上开放端口，请确保 VPS 的防火墙规则配置得当。生产环境中通常建议使用 Ingress Controller (如 K3s 自带的 Traefik) 配合 LoadBalancer 或其他方式进行更安全的暴露。
* **资源限制:** `deployment.yaml` 中设置了基本的资源请求和限制，防止应用异常时耗尽节点资源。
* **镜像安全:** 定期扫描构建的 Docker 镜像以发现潜在漏洞 (可以使用 GitHub Actions 市场中的扫描工具集成)。

