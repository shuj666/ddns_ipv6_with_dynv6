# Dynv6 IPv6 Updater

## 项目简介

`Dynv6Updater` 是一个用于自动更新 Dynv6 域名的 IPv6 地址的 Python 脚本。它会定期从指定的网卡中获取 IPv6 地址，并将其更新到 Dynv6 的域名解析记录中。本项目通过 NSSM 将 Python 脚本注册为 Windows 服务，以实现长期稳定运行。

## 特性

- **自动获取 IPv6 地址**: 根据提供的 MAC 地址，从系统中获取相应网卡的 IPv6 地址。
- **自动更新 Dynv6 记录**: 将获取到的 IPv6 地址发送到 Dynv6 平台，以更新域名的 IPv6 解析记录。
- **定时运行**: 脚本会每隔一段时间（默认30秒）运行一次，确保域名解析记录始终是最新的。

## 使用方法

### 环境依赖

运行该脚本需要以下依赖：

- Python 3.x
- `requests` 库

安装 `requests` 库：

以下2选一

```bash
pip install requests
```

```
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行脚本

编写脚本保存为`dynv6_updater.py`，不需要对脚本有任何更改。

```
import re
import subprocess
import requests
import time
import argparse

class Dynv6Updater:
    def __init__(self, mac_address, token, domain):
        self.mac_address = mac_address  # MAC地址
        self.token = token  # Dynv6的token
        self.domain = domain  # 域名

    def get_ipv6_address(self):
        try:
            # 使用ipconfig命令获取网卡信息
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout
                # 使用正则表达式匹配适配器段落
                adapters = re.findall(r'适配器 .*?:\n(.*?)\n\n', output, re.DOTALL)
                for adapter in adapters:
                    # 检查是否包含给定的MAC地址
                    if self.mac_address in adapter:
                        # 查找IPv6地址
                        ipv6_match = re.search(r'IPv6 地址.*?:(.*?)(?:\n|$)', adapter)
                        if ipv6_match:
                            ipv6_address = ipv6_match.group(1).strip().split('(首选)')[0]
                            return ipv6_address
                return "未找到匹配的网卡地址"
            else:
                return "无法执行ipconfig命令"
        except Exception as e:
            return f"发生错误：{str(e)}"

    def send_dynv6_update_request(self, ipv6):
        try:
            # 构建URL
            url = f"http://dynv6.com/api/update?hostname={self.domain}&token={self.token}&ipv6={ipv6}&ipv6prefix={ipv6}"
            print('构建URL:', url)

            # 发送GET请求
            response = requests.get(url)

            # 返回响应内容
            return response.text
        except Exception as e:
            return f"请求失败：{str(e)}"

    def run(self, interval=30):
        while True:
            try:
                # 获取IPv6地址
                ipv6_address = self.get_ipv6_address()
                print("MAC地址", self.mac_address, "对应的IPv6地址为:", ipv6_address)
                if ipv6_address and "未找到匹配的网卡地址" not in ipv6_address and "无法执行ipconfig命令" not in ipv6_address:
                    # 发送更新数据
                    response_text = self.send_dynv6_update_request(ipv6_address)
                    print("Dynv6响应:", response_text)
                else:
                    print("未获取到有效的IPv6地址:", ipv6_address)
            except Exception as e:
                print(f"运行时发生错误: {e}")
            finally:
                # 等待指定的时间间隔
                print(f"等待 {interval} 秒...")
                time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynv6 IPv6 Updater')
    parser.add_argument('--mac_address', required=True, help='网卡的MAC地址')
    parser.add_argument('--token', required=True, help='Dynv6的token')
    parser.add_argument('--domain', required=True, help='Dynv6的域名')

    args = parser.parse_args()

    # 创建Dynv6Updater对象并运行
    updater = Dynv6Updater(args.mac_address, args.token, args.domain)
    updater.run(interval=30)  # 运行，每30秒更新一次

```



使用以下命令运行脚本：

```bash
python dynv6_updater.py --mac_address <MAC地址> --token <Dynv6 Token> --domain <域名>
```

### 参数说明

- `--mac_address`：网卡的 MAC 地址，用于识别需要获取 IPv6 地址的网卡。
- `--token`：您的 Dynv6 API Token，用于授权更新操作。
- `--domain`：您希望更新的 Dynv6 域名。

### 示例

假设您的网卡 MAC 地址为 `00:1A:2B:3C:4D:5E`，Dynv6 Token 为 `your_token_here`，域名为 `example.dynv6.net`，您可以使用如下命令启动脚本：

```bash
python dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net
```

**注意事项**

你可以通过文章最后 **附** 部分了解MAC地址，Dynv6 Token，Dynv6 Token，域名的获取方法

### 日志输出

运行脚本后，您会在控制台看到类似以下的输出：

```plaintext
MAC地址 00:1A:2B:3C:4D:5E 对应的 IPv6 地址为:  240e::1a2b:3c4d:5e6f:7g8h
构建 URL: http://dynv6.com/api/update?hostname=example.dynv6.net&token=your_token_here&ipv6= 240e::1a2b:3c4d:5e6f:7g8h&ipv6prefix=240e::1a2b:3c4d:5e6f:7g8h
Dynv6 响应: OK
等待 30 秒...
```

**注意事项**

- 请确保您提供的 MAC 地址和 Dynv6 Token 是正确的，否则脚本可能无法正常工作。
- 如果脚本未能获取 IPv6 地址，可能是因为未找到匹配的网卡，或未能成功执行 `ipconfig` 命令。

## Windows 服务注册 

### 步骤 1: 下载并安装 NSSM

1. 访问 [NSSM 官网](https://nssm.cc/download) 下载适用于您的系统的 NSSM 版本（通常是 `win64` 或 `win32`），并解压缩到一个文件夹中，比如 `C:\nssm`。

### 步骤 2: 准备 Python 环境和脚本

1. **确保 Python 已安装**:
   - 确保您的系统已经安装了 Python，并且所有需要的库（如 `requests`）都已经安装。

2. **保存 Python 脚本**:
   - 将您的 Python 脚本保存到一个特定的目录，比如 `C:\scripts\dynv6_updater.py`。

### 步骤 3: 使用 NSSM 注册服务

1. **打开命令提示符**:

   - 以管理员身份打开命令提示符。

2. **导航到 NSSM 所在目录**:

   - 进入 NSSM 所在的目录，例如：

     ```cmd
     cd C:\nssm\win64
     ```

   **以上1、2步骤也可以在资源管理器中进入到nssm.exe 所在目录后按住shift键不动右键选择`在此处打开 Powershell 窗口(S)`**

3. **注册服务**:

   - 运行以下命令来注册您的 Python 脚本为服务：

     ```
     .\nssm.exe install UpdateIpv6Service
     ```

     这会弹出 NSSM 的服务配置窗口。

4. **配置服务**:

   - 在 NSSM 服务配置窗口中，进行以下设置：
     - **Application Path**: 指定 Python 解释器的路径，例如 `C:\Python39\python.exe`。
     - **Startup directory**: 指定 Python 脚本所在的目录，例如 `C:\scripts\`。
     - **Arguments**: 输入 Python 脚本的路径和参数，例如 `dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net`。
     
     最终构建的结果如下
     
     ```
     C:\Python39\python.exe C:\scripts\dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net
     ```
     
     **注意事项**
     
     建议install前先检查构建的结果在`Powershell 窗口(S)`下是否能正常运行
     
     在cmd使用以下命令获取python解释器路径
     
     ```
     where python
     ```
     
     部分电脑的`C:\Users\你的用户名\AppData\Local\Microsoft\WindowsApps\python.exe`路径它可能可能有一些限制，比如不能使用某些命令行参数。无法使用的。
     `where python`查不到也没有关系
     python.exe真实目录一般位于C:\Users\你的用户名\AppData\Local\Programs\Python\Python39\目录下
     
     若是指定安装则写指定安装目录

5. **设置服务启动类型**:

   - 切换到 **"Details"** 标签页，找到 **"Startup type"** 选项，并将其设置为 **"Automatic"**，这将使服务在系统启动时自动启动。

6. **保存服务**:

   - 配置完成后，点击 **"Install service"** 按钮，NSSM 会将该服务注册到 Windows 服务中。

### 步骤 4: 启动服务并验证

1. **启动服务**:

   - 在命令提示符中，使用以下命令启动服务：

     ```cmd
      .\nssm.exe start UpdateIpv6Service
     ```

   - 您也可以在 **Windows 服务管理器** (`services.msc`) 中手动启动服务。

2. **验证服务运行**:

   - 打开 **Windows 服务管理器** (`services.msc`)，按U键查找名为 `UpdateIpv6Service` 的服务，并确认其状态为“正在运行”（Running）。
   - 确认服务的 **启动类型** 显示为“自动”（Automatic）。

### 步骤 5: 设置日志记录（可选）

1. **配置日志输出**:

   - 打开 NSSM 的配置窗口：

     ```cmd
     .\nssm.exe edit UpdateIpv6Service
     ```

   - 在 **"I/O"** 标签页中，可以设置标准输出（stdout）和标准错误（stderr）的日志文件路径，以便记录服务的输出信息。

### 步骤 6: 重启系统并验证

1. **重启计算机**:
   - 重新启动计算机，确保服务在系统启动时自动启动。

2. **检查服务状态**:
   - 重启后，再次打开 **Windows 服务管理器** (`services.msc`)，确认服务 `UpdateIpv6Service` 的状态为“正在运行”（Running）。

通过这些步骤，您的 Python 脚本现在已经成功注册为一个在 Windows 系统启动时自动运行的服务，并且可以通过 NSSM 进行管理和监控。

# 附：以下为帮助操作

## 卸载服务

```
.\nssm.exe stop UpdateIpv6Service
.\nssm.exe remove UpdateIpv6Service
```

## 获取dynv6的token

dynv6<br />网站：<br />[https://dynv6.com/zones](https://dynv6.com/zones)
<a name="hy5TW"></a>

### 创建域名

![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717122836273-2cac6b45-640e-4261-9373-0335a158fad0.png#averageHue=%23fcfbfb&clientId=ue3935f30-cfb9-4&from=paste&height=413&id=u3ec12dc5&originHeight=516&originWidth=1468&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=39804&status=done&style=none&taskId=ua6c76285-3dbf-4c31-be40-bc84e561fb1&title=&width=1174.4)
<a name="JOqrJ"></a>

### 创建token

![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717123765947-477c7de1-9caa-4943-935b-33fd3c709965.png#averageHue=%23fcfbfb&clientId=ue3935f30-cfb9-4&from=paste&height=298&id=u7c275fca&originHeight=373&originWidth=1467&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=34074&status=done&style=none&taskId=uecb84c5b-6202-483b-b0f6-5eb32d37026&title=&width=1173.6)<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717123926477-b3cb96c2-d949-4727-9e80-9db7cbab6c65.png#averageHue=%23fbfaf9&clientId=ue3935f30-cfb9-4&from=paste&height=510&id=u5f7a7add&originHeight=637&originWidth=1554&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=72460&status=done&style=none&taskId=ua304812a-4fdc-4c89-b5d0-cbcb2848adc&title=&width=1243.2)<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717124286577-3775d72f-a784-46ce-8553-2d654d3acb7b.png#averageHue=%23f7f6f6&clientId=ue3935f30-cfb9-4&from=paste&height=389&id=u61b2595e&originHeight=486&originWidth=1207&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=66345&status=done&style=none&taskId=ufff31c91-cd2e-4a28-b1b9-35441a95501&title=&width=965.6)<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717124465263-a6f2778a-44aa-43c7-9145-0a86b97e3d1f.png#averageHue=%23f9f7f7&clientId=ue3935f30-cfb9-4&from=paste&height=342&id=u79f67c7b&originHeight=427&originWidth=985&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=32174&status=done&style=none&taskId=ue799d9d6-5f02-4dab-85ff-ef6318762be&title=&width=788)

<a name="VKY9x"></a>

<a name="PvEWE"></a>

## 安装python环境。

下载地址<br />[https://www.python.org/downloads/](https://www.python.org/downloads/)<br />点击downlaod下载安装即可<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717126558070-59b8c4ac-a1b3-4c33-8b7f-585a4af984e4.png#averageHue=%23f9f7f2&clientId=ue3935f30-cfb9-4&from=paste&height=404&id=uc3159b3b&originHeight=505&originWidth=820&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=187834&status=done&style=none&taskId=u8fc78166-59e7-4400-821a-93b6f71234f&title=&width=656)
<a name="a9IsC"></a>

### 安装python第三方库

**requests**

-  **简介**: `requests` 库是一个流行的第三方库，用于处理 HTTP 请求。 
-  **用途**: 发送 GET、POST 等 HTTP 请求，处理响应数据。 
-  **安装方法**: 你需要使用 `pip` 来安装 `requests` 库。 

```bash
pip install requests
```

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

<a name="PK34s"></a>

## 获得网卡mac地址

**用于定位解析那张网卡**<br />在win运行cmd，在cmd终端执行ipconfig /all 命令查看网卡的mac地址<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717125689275-4c8d2c07-8299-47ca-b99d-3f6e648174dc.png#averageHue=%231a1a1a&clientId=ue3935f30-cfb9-4&from=paste&height=526&id=u4446c405&originHeight=658&originWidth=688&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=57604&status=done&style=none&taskId=u3b752930-c459-4559-b9e8-672086ff605&title=&width=550.4)
<a name="SiCul"></a>