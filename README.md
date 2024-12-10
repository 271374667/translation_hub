# translation-hub

没有任何依赖的翻译库，API 统一简单易用，适合快速集成翻译功能而不想引入庞大的依赖库。

- 简单易用
- 支持多种翻译服务
- 仅使用标准库，连 requests 都没有，非常适合快速集成
- 屏蔽各大翻译api语言代码，内置了常用语言的映射
- 支持多种秘钥传入方式,无需每次都输入(直接传入，本地存储，环境变量)
- 更加直观的自定义报错类型提示(翻译服务报错，秘钥错误等)
- 详细的代码文档(包括免费额度, 如何开通和文档地址等)
- 完整的单元测试

目前支持的国内翻译服务(均为有免费额度)：

- [x] 百度翻译
- [x] 有道翻译
- [x] 腾讯翻译
- [x] 阿里翻译

目前支持的国外翻译服务：

- [x] deepl翻译
- [x] 支持谷歌翻译(无需秘钥)

## Installation 安装说明

Install the latest translation-hub version with:

```shell
pip install translation-hub
```

## QuickStart 快速开始

只需要定义一个翻译器对象，传入秘钥，然后调用 `translate` 方法即可。

同时支持直接传入,本地存储秘钥以及从环境变量获取秘钥

```python
from translation_hub import BaiduAPI

translator = BaiduAPI("your appid", "secret_key")
result = translator.translate("hello")

print(result)  # 你好
```

自定义翻译语言,使用 `Languages` 枚举类来实现屏蔽各大翻译api语言代码

```python
from translation_hub import GoogleApi, Languages

# 谷歌无需传入秘钥
translator = GoogleApi()

# 自动检测后翻译成中文
print(translator.translate("hello", Languages.Auto, Languages.Chinese))  # 你好

# 手动说明语言,然后翻译成日文
print(translator.translate("hello", Languages.English, Languages.Japanese))  # こんにちは
```

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