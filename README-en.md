# Dynv6 IPv6 Updater

## Project Overview

`Dynv6Updater` is a Python script designed to automatically update the IPv6 address of a Dynv6 domain. It periodically retrieves the IPv6 address from a specified network interface and updates the Dynv6 domain's DNS record. The script is intended to be registered as a Windows service using NSSM to ensure long-term stable operation.

## Features

- **Automatic IPv6 Address Retrieval**: The script fetches the IPv6 address from the network interface associated with the provided MAC address.
- **Automatic Dynv6 Record Update**: The retrieved IPv6 address is sent to the Dynv6 platform to update the domain's IPv6 DNS record.
- **Scheduled Execution**: The script runs periodically (default every 30 seconds) to ensure the DNS record remains up-to-date.

## Usage

### Environment Dependencies

The script requires the following dependencies:

- Python 3.x
- `requests` library

To install the `requests` library:

Choose one of the following commands:

```bash
pip install requests
```

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Running the Script

Run the script using the following command:

```bash
python dynv6_updater.py --mac_address <MAC_ADDRESS> --token <Dynv6_Token> --domain <Domain>
```

### Parameters Description

- `--mac_address`: The MAC address of the network interface to identify the correct one for IPv6 address retrieval.
- `--token`: Your Dynv6 API Token, required for authorization to update the DNS record.
- `--domain`: The Dynv6 domain you want to update.

### Example

Suppose your network interface MAC address is `00:1A:2B:3C:4D:5E`, Dynv6 Token is `your_token_here`, and the domain is `example.dynv6.net`, you can start the script with the following command:

```bash
python dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net
```

**Note:** Refer to the **Appendix** section at the end of this document for details on obtaining the MAC address, Dynv6 Token, and domain.

### Log Output

Upon running the script, the console will display output similar to the following:

```plaintext
MAC address 00:1A:2B:3C:4D:5E corresponding IPv6 address: 240e::1a2b:3c4d:5e6f:7g8h
Constructed URL: http://dynv6.com/api/update?hostname=example.dynv6.net&token=your_token_here&ipv6=240e::1a2b:3c4d:5e6f:7g8h&ipv6prefix=240e::1a2b:3c4d:5e6f:7g8h
Dynv6 Response: OK
Waiting 30 seconds...
```

**Note:**

- Ensure the provided MAC address and Dynv6 Token are correct; otherwise, the script may not function properly.
- If the script fails to retrieve the IPv6 address, it may be due to an unmatched network interface or an unsuccessful `ipconfig` command.

## Registering as a Windows Service

### Step 1: Download and Install NSSM

1. Visit the [NSSM website](https://nssm.cc/download) to download the appropriate NSSM version for your system (`win64` or `win32`), and extract it to a folder, such as `C:\nssm`.

### Step 2: Prepare Python Environment and Script

1. **Ensure Python is Installed**:
   - Make sure Python is installed on your system, and all required libraries (such as `requests`) are installed.

2. **Save Python Script**:
   - Save your Python script to a specific directory, such as `C:\scripts\dynv6_updater.py`.

### Step 3: Register the Script as a Service Using NSSM

1. **Open Command Prompt**:

   - Open Command Prompt as an administrator.

2. **Navigate to the NSSM Directory**:

   - Navigate to the NSSM directory, for example:

     ```cmd
     cd C:\nssm\win64
     ```

   **Alternatively, you can open a PowerShell window by holding down the Shift key and right-clicking inside the NSSM directory, then selecting "Open PowerShell window here."**

3. **Register the Service**:

   - Run the following command to register your Python script as a service:

     ```cmd
     .\nssm.exe install UpdateIpv6Service
     ```

     This will open the NSSM service configuration window.

4. **Configure the Service**:

   - In the NSSM service configuration window, set the following options:

     - **Application Path**: Specify the path to the Python interpreter, e.g., `C:\Python39\python.exe`.
     - **Startup Directory**: Specify the directory where the Python script is located, e.g., `C:\scripts\`.
     - **Arguments**: Enter the script path and parameters, e.g., `dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net`.

     The final command will look like this:

     ```cmd
     C:\Python39\python.exe C:\scripts\dynv6_updater.py --mac_address 00:1A:2B:3C:4D:5E --token your_token_here --domain example.dynv6.net
     ```

     **Note:** Before installation, it is recommended to check if the constructed command runs correctly in the PowerShell window.

     Use the following command in the Command Prompt to find the Python interpreter path:

     ```cmd
     where python
     ```

5. **Set Service Startup Type**:

   - Switch to the **"Details"** tab and find the **"Startup type"** option. Set it to **"Automatic"**, so the service starts automatically when the system boots.

6. **Save the Service**:

   - After configuring, click the **"Install service"** button. NSSM will register the service in Windows.

### Step 4: Start the Service and Verify

1. **Start the Service**:

   - In the Command Prompt, start the service with the following command:

     ```cmd
      .\nssm.exe start UpdateIpv6Service
     ```

   - You can also manually start the service via the **Windows Services Manager** (`services.msc`).

2. **Verify Service Operation**:

   - Open the **Windows Services Manager** (`services.msc`), press "U" to locate the service named `UpdateIpv6Service`, and confirm that its status is "Running".
   - Ensure the **Startup type** is set to "Automatic".

### Step 5: Configure Logging (Optional)

1. **Configure Log Output**:

   - To set up logging, open the NSSM configuration window with the following command:

     ```cmd
     .\nssm.exe edit UpdateIpv6Service
     ```

   - In the **"I/O"** tab, you can set the paths for the standard output (stdout) and standard error (stderr) log files to record the service's output.

### Step 6: Restart the System and Verify

1. **Restart the Computer**:
   - Restart the computer to ensure the service starts automatically with the system.

2. **Check Service Status**:
   - After rebooting, open the **Windows Services Manager** (`services.msc`) again to confirm that the `UpdateIpv6Service` is "Running".

By following these steps, your Python script is now successfully registered as a service on Windows that runs automatically on system startup and can be managed and monitored using NSSM.

## Appendix: Additional Operations

### Uninstalling the Service

```cmd
.\nssm.exe stop UpdateIpv6Service
.\nssm.exe remove UpdateIpv6Service
```

## Obtaining a Dynv6 Token

### Dynv6 Website

Dynv6 website:  
[https://dynv6.com/zones](https://dynv6.com/zones)

### Creating a Domain

![Creating a Domain](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717122836273-2cac6b45-640e-4261-9373-0335a158fad0.png#averageHue=%23fcfbfb&clientId=ue3935f30-cfb9-4&from=paste&height=413&id=u3ec12dc5&originHeight=516&originWidth=1468&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=39804&status=done&style=none&taskId=ua6c76285-3dbf-4c31-be40-bc84e561fb1&title=&width=1174.4)

### Creating a Token

![Creating a Token](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717123765947-477c7de1-9caa-4943-935b-33fd3c709965.png#averageHue=%23fcfbfb&clientId=ue3935f30-cfb9-4&from=paste&height=298&id=u7c275fca&originHeight=373&originWidth=1467&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=34074&status=done&style=none&taskId=uecb84c5b-6202-483b-b0f6-5eb32d37026&title=&width=1173.6)

![Token Creation](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717123926477-b3cb96c2-d949-4727-9e80-9db7cbab6c65.png#averageHue=%23fbfaf9&clientId=ue3935f30-cfb9-4&from=paste&height=510&id=u5f7a7add&originHeight=637&originWidth=1554&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=72460&status=done&style=none&taskId=ua304812a-4fdc-4c89-b5d0-cbcb2848adc&title=&width=1243.2)

![Token Generation](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717124286577-3775d72f-a784-46ce-8553-2d654d3acb7b.png#averageHue=%23f7f6f6&clientId=ue3935f30-cfb9-4&from=paste&height=389&id=u61b2595e&originHeight=486&originWidth=1207&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=66345&status=done&style=none&taskId=ufff31c91-cd2e-4a28-b1b9-35441a95501&title=&width=965.6)

![Token Confirmation](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717124465263-a6f2778a-44aa-43c7-9145-0a86b97e3d1f.png#averageHue=%23f9f7f7&clientId=ue3935f30-cfb9-4&from=paste&height=342&id=u79f67c7b&originHeight=427&originWidth=985&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=32174&status=done&style=none&taskId=ue799d9d6-5f02-4dab-85ff-ef6318762be&title=&width=788)

---

## Installing Python Environment

### Downloading and Installing Python

Download Python from the official website:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)  
Click "Download" and install it by following the on-screen instructions.

![Python Installation](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717126558070-59b8c4ac-a1b3-4c33-8b7f-585a4af984e4.png#averageHue=%23f9f7f2&clientId=ue3935f30-cfb9-4&from=paste&height=404&id=uc3159b3b&originHeight=505&originWidth=820&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=187834&status=done&style=none&taskId=u8fc78166-59e7-4400-821a-93b6f71234f&title=&width=656)

### Installing Python Third-Party Libraries

**Requests**

- **Introduction**: The `requests` library is a popular third-party Python library used for handling HTTP requests.
- **Purpose**: It is used to send GET, POST, and other HTTP requests and to handle response data.
- **Installation Method**: You need to use `pip` to install the `requests` library.

```bash
pip install requests
```

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Obtaining the Network Interface MAC Address

**Used for locating the correct network interface.**

Run `cmd` in Windows, and in the command prompt, execute the `ipconfig /all` command to view the MAC address of the network interface.

![MAC Address](https://cdn.nlark.com/yuque/0/2024/png/39063479/1717125689275-4c8d2c07-8299-47ca-b99d-3f6e648174dc.png#averageHue=%231a1a1a&clientId=ue3935f30-cfb9-4&from=paste&height=526&id=u4446c405&originHeight=658&originWidth=688&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=57604&status=done&style=none&taskId=u3b752930-c459-4559-b9e8-672086ff605&title=&width=550.4)



