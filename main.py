from fastapi import FastAPI
from src.app.routers import inventory, order, notification, user
from src.app.database.connectivity import engine
from sqlmodel import SQLModel

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

app.include_router(inventory, prefix="/inventory", tags=["Inventory"])
app.include_router(order, prefix="/order", tags=["Order"])
app.include_router(notification, prefix="/notification", tags=["Notification"])
app.include_router(user, prefix="/user", tags=["User"])

@app.get("/")
def root():
    return {"message": "Mart Management System is running!"}



# from src.app.routers.main_routes import app
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run(app=app)