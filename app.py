import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/proxy")
async def proxy(
    url: str = Query(None),
):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": url,
    }
    try:
        with requests.get(url, timeout=60, headers=headers) as resp:
            if not resp or resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code)
            content_type = resp.headers.get("Content-Type")
            return StreamingResponse(resp, headers=resp.headers, media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/", StaticFiles(html=True, directory="./site"),  name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", workers=6, host="0.0.0.0", port=8091)
