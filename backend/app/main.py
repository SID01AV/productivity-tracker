from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .init_data import init_db
from .routers import auth as auth_router
from .routers import friends as friends_router
from .routers import leaderboard as leaderboard_router
from .routers import logs as logs_router
from .routers import stats as stats_router
from .routers import tasks as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Productivity Tracker API")

    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",  # simplify for development / mobile
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router.router)
    app.include_router(tasks_router.router)
    app.include_router(logs_router.router)
    app.include_router(friends_router.router)
    app.include_router(leaderboard_router.router)
    app.include_router(stats_router.router)

    @app.get("/")
    async def root():
        return {"message": "Productivity Tracker API"}

    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    init_db()

