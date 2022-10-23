import uvicorn

from settings import Settings


def main():
    settings = Settings()
    uvicorn.run(
        "reaction_reader.app:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
        debug=settings.debug,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
