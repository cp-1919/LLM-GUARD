# LLM-GUARD 项目说明

## 0. 直接使用
从SourceForge中直接下载可执行文件。

[https://sourceforge.net/projects/llm-guard/files/latest/download](https://sourceforge.net/projects/llm-guard/files/latest/download)

运行后，应用程序及资源会自动解压在文件所在目录。再次运行时，直接运行 LLM-GUARD.exe。

## 1. 目录结构
```text
|--llm-guard
    |--app          软件后端&接口
    |--front        前端
    |--tests        测试脚本
    |--example      项目文件样例
```

## 2. 安装依赖
本项目基于 **python 3.12** 以及 **node v22.11.0**

下面脚本在项目根目录下运行
```bash
pip install -r requirements.txt
cd front
npm install
```

## 3. 启动
```bash
cd front
npm run dev
```
然后运行根目录下的 **main.py** 

## 4. 打包为exe
本项目需要打包前端ui文件以及Ollama可执行程序，详细说明见 **build.md**
