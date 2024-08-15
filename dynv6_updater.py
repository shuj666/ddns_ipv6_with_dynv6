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
