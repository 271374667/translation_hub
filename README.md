# translation-hub

没有任何依赖的翻译库，API 统一简单易用，适合快速集成翻译功能而不想引入庞大的依赖库。

- 简单易用
- 支持多种翻译服务
- 仅使用 requests 与 urllib 实现，适合快速集成
- 屏蔽各大翻译api语言代码，内置了常用语言的映射
- 支持多种秘钥传入方式,无需每次都输入(直接传入，本地存储，环境变量)
- 更加直观的自定义报错类型提示(翻译服务报错，秘钥错误等)
- 详细的代码文档(包括免费额度, 如何开通和文档地址等)
- 完整的单元测试

## Installation 安装说明

translation-hub 的安装非常简单，只需要使用 pip 安装即可

```shell
pip install translation-hub
```

## QuickStart 快速开始

可以直接使用无需秘钥的版本进行翻译，使用此类方法需要注意获取频率，频率过快会被服务器封禁

```python
from translation_hub import BingFreeApi

translator = BingFreeApi()
result = translator.translate("hello")

print(result)  # 你好
```



如果需要使用 API 的付费版本则可以用更高的频率请求服务器，方法也很简单，只需要定义一个翻译器对象，传入秘钥，然后调用 `translate` 方法即可。

同时支持直接传入,本地存储秘钥以及从环境变量获取秘钥

```python
from translation_hub import BaiduAPI

translator = BaiduAPI("your appid", "secret_key")
result = translator.translate("hello")

print(result)  # 你好
```

通过传入 `Languages` 枚举类实现将文本翻译成不同的语言版本，同时您也可以自行传入翻译平台支持的字符串

```python
from translation_hub import BingFreeApi, Languages

# bing 无需传入秘钥
translator = BingFreeApi()

# 自动检测后翻译成中文
print(translator.translate("hello", Languages.Auto, Languages.Chinese))  # 你好

# 手动说明语言,然后翻译成日文
print(translator.translate("hello", Languages.English, Languages.Japanese))  # こんにちは
```

## Supported Translation Services 支持的翻译服务

<center>表1 无需秘钥的翻译服务(需要注意访问频率限制,反爬随时可能更新导致失效)</center>

|      翻译名称      |   API 名称    |
| :----------------: | :-----------: |
|      百度翻译      | BaiduFreeApi  |
|     bing 翻译      |  BingFreeApi  |
| 谷歌翻译(需要翻墙) | GoogleFreeApi |

<center>表2 目前支持的国内翻译服务(均为有免费额度)</center>

| 翻译名称 |  API名称   |
| :------: | :--------: |
| 百度翻译 |  BaiduAPI  |
| 有道翻译 | YoudaoApi  |
| 腾讯翻译 | TencentApi |
| 阿里翻译 | AliyunApi  |

<center>表3 目前支持的国外翻译服务</center>

| 翻译名称  | API名称  |
| --------- | -------- |
| deepl翻译 | DeeplApi |



## Supported Languages 支持的语言

每一个翻译 API 对应语言的缩写形式不同，比如简体中文在百度翻译中是 `zh`，在谷歌翻译中是 `zh-CN`，在有道翻译中是 `zh-CHS`
。为了方便使用，我定义了一个枚举类 `Languages` 来屏蔽这些细节，直接使用枚举类即可。

目前支持的通用语言如下,我为这些语言定义了一个枚举类 `Languages` 来屏蔽各大翻译api的语言代码:

- 中文 Language.Chinese
- 英语 Language.English
- 日语 Language.Japanese
- 韩语 Language.Korea
- 俄语 Language.Russia
- 自动选择 Language.Auto

如果您需要其他语言，可以自行前往查看每一个翻译服务的支持语言,然后手动传入语言代码即可。比如

```python
from translation_hub import DeeplApi

deepl = DeeplApi("your api key")

# 翻译成德语
print(deepl.translate("hello", "EN", "DE"))  # hallo
```

## Configuration 配置说明

每一个翻译服务除了能直接传入 api_id 和 api_key 之外，还支持从本地文件中读取秘钥以及从环境变量中读取秘钥

### 本地文件

在 C 盘的用户目录,下会创建一个 `TranslateHubConfig.json` 文件，您可以在这个文件中存储您的秘钥，下一次创建翻译器对象便可以不传入秘钥

文件的默认路径为: `C:\Users\Administrator\TranslateHubConfig.json`，此时也可能会因为权限问题无法创建文件，您可以手动创建一个文件，然后将秘钥写入即可。
其中的 Administrator 替换成您的用户名即可

```json
{
  "Aliyun": {
    "AliyunAppId": "",
    "AliyunSecretKey": ""
  },
  "Baidu": {
    "BaiduAppId": "",
    "BaiduSecretKey": ""
  },
  "Deepl": {
    "DeeplApiKey": ""
  },
  "Tencent": {
    "TencentAppId": "",
    "TencentSecretKey": ""
  },
  "Youdao": {
    "YoudaoAppId": "",
    "YoudaoSecretKey": ""
  }
}
```

### 环境变量

环境变量是一种更加安全的存储方式，翻译器对象会自动读取环境变量中的秘钥

您需要自行设置环境变量，变量名如下:

```text
AliyunAppId
AliyunSecretKey
BaiduAppId
BaiduSecretKey
DeeplApiKey
TencentAppId
TencentSecretKey
YoudaoAppId
YoudaoSecretKey
```

#### 如何设置环境变量

**在 Windows 系统中，您可以使用如下操作来设置环境变量**

1. 右键点击"此电脑"/"我的电脑" -> 点击"属性"
2. 点击"高级系统设置"
3. 在"系统属性"窗口中，选择"高级"选项卡
4. 点击右下角的"环境变量"按钮
5. 在"环境变量"窗口中:
    - 上半部分是"用户变量"(仅对当前用户有效)
    - 下半部分是"系统变量"(对所有用户有效)
6. 点击"新建"添加新变量，或选择已有变量点击"编辑"
7. 输入变量名和变量值
8. 连续点击"确定"保存所有更改

**在 Linux 系统中，您可以使用如下操作来设置环境变量**

```shell
# 编辑 ~/.bashrc 文件
nano ~/.bashrc

# 在文件末尾添加
export VARIABLE_NAME="value"

# 保存并应用更改
source ~/.bashrc
```

**在 MacOS 系统中，您可以使用如下操作来设置环境变量**

```shell
# 编辑 /etc/profile
sudo nano /etc/profile

# 添加
export VARIABLE_NAME="value"

# 应用更改
source /etc/profile
```