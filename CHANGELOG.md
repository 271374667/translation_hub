# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.11](https://github.com/271374667/translatehub/compare/v0.2.6...v0.2.11) - 2024-12-10

- ⬆️ 升级(pyproject.toml)：将项目版本从0.2.7升级到0.2.11以反映新功能和修复。 [`154471b`](https://github.com/271374667/translatehub/commit/154471b4804a783147cac807065599e3e80472fd)
- ♻️ refactor(pyproject.toml)：将包名从translatehub更改为translation_hub以保持一致性 [`ba63350`](https://github.com/271374667/translatehub/commit/ba6335084e5929494c4ffd1ed32f4f835dc33e2a)
- 🔧 chore(python-publish.yml)：移除对release事件的支持 [`3ce7f93`](https://github.com/271374667/translatehub/commit/3ce7f93851b76ca6450af3abb49beca1813603c4)
- ✨ workflow: 添加手动触发工作流的支持 [`809cdbb`](https://github.com/271374667/translatehub/commit/809cdbb5e5255fc3478422ad6edc17237ea95255)
- 📝 docs：添加CHANGELOG.md文件以记录项目的显著变化 [`a38090f`](https://github.com/271374667/translatehub/commit/a38090f090a8876fba0bbf959703e58d79e58b95)

## v0.2.6 - 2024-12-10

- ✅ test(test_deepl_api.py)：修复测试用例以正确获取Deepl API密钥 [`225caaa`](https://github.com/271374667/translatehub/commit/225caaa9de6c53f705b94e75222e89e5bc23c070)
- 📝 docs(README.md)：更新项目名称，增加功能描述和安装说明 [`87256d1`](https://github.com/271374667/translatehub/commit/87256d1b1a3754e2fe21b78e1519fa36c103a4c3)
- 📝 docs(README.md)：更新示例代码以使用正确的语言枚举值 [`bf8fca5`](https://github.com/271374667/translatehub/commit/bf8fca5221c25bac05d93250b3b155224d3e48ff)
- Style: 统一了Language枚举类的风格 [`17bb047`](https://github.com/271374667/translatehub/commit/17bb047f0581ef30dfb39192a7955c6360493f0e)
- Create python-publish.yml [`52dc7e4`](https://github.com/271374667/translatehub/commit/52dc7e4d2b8e1514f682ae5a8d202a0ff3f84017)
- test: 更新了所有的测试 [`853b710`](https://github.com/271374667/translatehub/commit/853b710c079089100c797b3c76fb6cb13f554248)
- Version: 第一版完整版实现，同时实现了所有的测试，确保核心功能长期可用 [`c22858a`](https://github.com/271374667/translatehub/commit/c22858adf830a5726a53b06eaba97ba97b29bb34)
