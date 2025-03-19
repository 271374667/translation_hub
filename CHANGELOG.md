# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.12.4](https://github.com/271374667/translatehub/compare/v0.11.7...v0.12.4) - 2025-03-18

- ✨ feat(翻译服务)：添加搜狗翻译API支持 [`d482eef`](https://github.com/271374667/translatehub/commit/d482eef0cb35d40a165d9ae1df28d235982efb76)

## [v0.11.7](https://github.com/271374667/translatehub/compare/v0.6.14...v0.11.7) - 2025-03-17

- 📝 docs(README.md)：更新快速开始部分，添加无秘钥翻译示例 [`b5b7964`](https://github.com/271374667/translatehub/commit/b5b79641422c5adf78bb94c2605bcc9460e56d47)
- ✨ feat(bing_free_api.py)：添加Bing翻译API的实现及测试用例 [`3989148`](https://github.com/271374667/translatehub/commit/39891487d42086d5ea5332d604f027368c904d86)
- ✨ feat(baidu_free_api.py, bing_free_api.py)：为翻译API添加内容验证功能 [`d359c79`](https://github.com/271374667/translatehub/commit/d359c796fda9ae8b58adaf79bcd2b2cc0a9d4699)
- 📝 更新(CHANGELOG.md)：记录版本0.6.14的发布及变更 [`652b6a0`](https://github.com/271374667/translatehub/commit/652b6a0fd091b1e65ecaf3d6e2c5f67fed124f84)

## [v0.6.14](https://github.com/271374667/translatehub/compare/v0.6.13...v0.6.14) - 2025-03-15

- 🚀 release: 更新版本号至0.6.14并记录变更 [`60630eb`](https://github.com/271374667/translatehub/commit/60630ebb02c46e8f89ae95897e2bf91e81e2e180)

## [v0.6.13](https://github.com/271374667/translatehub/compare/v0.2.15...v0.6.13) - 2025-03-15

- ✨ feat: 添加百度翻译API支持，允许无需秘钥的翻译 [`e6e0c65`](https://github.com/271374667/translatehub/commit/e6e0c6510ca7aee3a4ec565920d6c23429788e6e)
- ✨ feat(README.md)：更新文档以反映Google翻译API的更改 [`309b23c`](https://github.com/271374667/translatehub/commit/309b23cd101edd6d71743abd21713bdd4417960a)
- ✨ feat(tests)：添加Google翻译API的单元测试 [`b31ebbc`](https://github.com/271374667/translatehub/commit/b31ebbc3f3fdf7664d5e8292ae4c20c0fdd0f151)
- 📝 docs(README.md)：更新文档以添加翻译服务支持和配置说明 [`c15f50b`](https://github.com/271374667/translatehub/commit/c15f50b0b7658577845da2dcc048e2955a9a71c2)

## [v0.2.15](https://github.com/271374667/translatehub/compare/v0.2.11...v0.2.15) - 2024-12-10

- 📝 docs(CHANGELOG.md)：更新CHANGELOG以记录v0.2.15版本的变化和改进 [`2888c7d`](https://github.com/271374667/translatehub/commit/2888c7dcc60aa319626d8bed388a83d515aae159)
- ✨ feat(python-publish.yml)：添加对发布事件的支持以触发工作流 [`772f393`](https://github.com/271374667/translatehub/commit/772f393364e022955d302bd756b119955f8b4be5)
- fix: 修复了打包之后只有INFO包的错误 [`9b016eb`](https://github.com/271374667/translatehub/commit/9b016eb3f1b7d68524358879532a990923b91108)
- 📝 docs(CHANGELOG.md)：更新CHANGELOG以记录v0.2.11版本的变化和改进 [`c2e8d0c`](https://github.com/271374667/translatehub/commit/c2e8d0c8360d7e3767df6d497bce5639c8d165f0)

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
