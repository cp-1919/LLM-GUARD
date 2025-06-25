# 项目打包

+ 所有操作在项目根目录下完成

## 1. 打包前端

```bash
cd front
npm run build
```

## 2. 构建可执行程序及目录
```bash
pyinstaller -D -w `
  -n LLM-GUARD `
  --add-data "app/models;models" `
  --add-data "app/ollama;ollama" `
  --add-data "app/config.json;." `
  --add-data "app/tiktoken_resource;tiktoken_resource" `
  --hidden-import=tiktoken_ext `
  --hidden-import=tiktoken_ext.openai_public `
  --hidden-import=chromadb.telemetry.product.posthog `
  --hidden-import=chromadb.api.rust `
  --collect-data=chromadb `
  --add-data "app/tesseract;tesseract" `
  --add-data "front/dist;front" `
  --runtime-tmpdir ./temp `
  -i ./llm-guard.ico `
  main.py
```