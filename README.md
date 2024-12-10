# translatehub

没有任何依赖的翻译库，API 统一简单易用，适合快速集成翻译功能而不想引入庞大的依赖库。

- 简单易用
- 支持多种翻译服务
- 没有任何依赖(连 requests 都没有)
- 屏蔽各大翻译api语言代码，内置了常用语言的映射
- 支持多种秘钥传入方式,无需每次都输入(直接传入，本地存储，环境变量)
- 完整的单元测试

目前支持的国内翻译服务(均为有免费额度)：

- [x] 百度翻译
- [x] 有道翻译
- [x] 腾讯翻译
- [x] 阿里翻译

目前支持的国外翻译服务：

- [x] deepl翻译
- [x] 支持谷歌翻译

## Installation 安装说明

```shell
pip install translatehub
```

## QuickStart 快速开始

只需要定义一个翻译器对象，传入秘钥，然后调用 `translate` 方法即可。

同时支持直接传入,本地存储秘钥以及从环境变量获取秘钥

```python
from translatehub import BaiduAPI

translator = BaiduAPI('your appid', 'secret_key')
result = translator.translate('hello')

print(result)  # 你好
```

自定义翻译语言,使用 `Languages` 枚举类来实现屏蔽各大翻译api语言代码

```python
from translatehub import GoogleApi, Languages

# 谷歌无需传入秘钥
translator = GoogleApi()

# 自动检测后翻译成中文
print(translator.translate("hello", Languages.AUTO, Languages.CHINESE))  # 你好

# 手动说明语言,然后翻译成日文
print(translator.translate("hello", Languages.ENGLISH, Languages.Japanese))  # こんにちは
```