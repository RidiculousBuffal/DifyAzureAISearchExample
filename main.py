from fastapi import FastAPI
from app.api.endpoints.retrieval import router as retrieval_router
import uvicorn
app = FastAPI()

# Include the retrieval router
app.include_router(retrieval_router)
# 定义入口函数
def main():
    # 使用 uvicorn 启动应用
    uvicorn.run(app, host="127.0.0.1", port=8000)

# 如果脚本被直接执行，则调用 main 函数
if __name__ == "__main__":
    main()