from fastapi import FastAPI
import sentry_sdk

# Configure SDK - Seguindo documentação oficial Sentry
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # To reduce the volume of performance data captured, change traces_sample_rate to a value between 0 and 1
    traces_sample_rate=0.1,
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "PRP Agent com Sentry - Funcionando!"}

@app.get("/sentry-debug")
async def trigger_error():
    """
    Verify Sentry integration
    Conforme documentação: https://docs.sentry.io/platforms/python/integrations/fastapi/
    """
    division_by_zero = 1 / 0