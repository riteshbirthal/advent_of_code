from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import importlib.util
import os, re
from typing import Dict, Any

app = FastAPI(title="Advent of Code UI")

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

ROOT = os.path.dirname(os.path.dirname(__file__))
YEARS_DIR = ROOT


class YearManager:
    def __init__(self, years_root: str):
        self.years_root = years_root
        self._cache: Dict[str, Any] = {}

    def available_years(self):
        """Return a sorted list of available year directory names.
        Accepts directories like `2025` or `Y2025` (case-insensitive).
        Sorting is numeric based on the digits portion.
        """
        candidates = [d for d in os.listdir(self.years_root) if os.path.isdir(os.path.join(self.years_root, d))]
        years = []
        for d in candidates:
            # match '2025' or 'Y2025' or 'y2025'
            m = re.match(r'^(?:[Yy])?(\d+)$', d)
            if m:
                years.append(d)
        # sort by numeric value of the year-part
        years.sort(key=lambda y: int(re.match(r'^(?:[Yy])?(\d+)$', y).group(1)))
        return years

    def available_days(self, year: str):
        year_path = os.path.join(self.years_root, year)
        days = []
        if not os.path.isdir(year_path):
            return days
        for entry in os.listdir(year_path):
            if entry.startswith('Day_') and os.path.isdir(os.path.join(year_path, entry)):
                try:
                    n = int(entry.split('_', 1)[1])
                    days.append(n)
                except Exception:
                    continue
        return sorted(days)

    def _load_module(self, year: str):
        if year in self._cache:
            return self._cache[year]
        year_main = os.path.join(self.years_root, year, 'main.py')
        if not os.path.exists(year_main):
            raise FileNotFoundError(f"Year module not found: {year_main}")
        spec = importlib.util.spec_from_file_location(f"aoc_{year}_main", year_main)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self._cache[year] = {'module': mod, 'path': os.path.join(self.years_root, year)}
        return self._cache[year]

    async def solve(self, year: str, day: int, data=None):
        info = self._load_module(year)
        mod = info['module']
        base_path = info['path']
        aoc_cls = getattr(mod, 'AoC', None)
        if aoc_cls is None:
            raise RuntimeError(f"Year {year} has no AoC class")
        aoc = aoc_cls()
        if data is None:
            input_file = os.path.join(base_path, f"Day_{day}", 'input.txt')
            if os.path.exists(input_file):
                with open(input_file, 'r', encoding='utf-8') as f:
                    data = f.read()
            else:
                data = ''
        try:
            result = await asyncio.to_thread(aoc.solve_problem, day, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return result


mgr = YearManager(YEARS_DIR)


@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    years = mgr.available_years()
    return templates.TemplateResponse('index.html', {'request': request, 'years': years})


@app.get('/{year}', response_class=HTMLResponse)
async def year_view(request: Request, year: str):
    if year not in mgr.available_years():
        raise HTTPException(status_code=404, detail='Year not found')
    days = mgr.available_days(year)
    return templates.TemplateResponse('year.html', {'request': request, 'year': year, 'days': days})


@app.get('/{year}/day/{day}', response_class=HTMLResponse)
async def day_get(request: Request, year: str, day: int):
    if year not in mgr.available_years():
        raise HTTPException(status_code=404, detail='Year not found')
    if day not in mgr.available_days(year):
        raise HTTPException(status_code=404, detail='Day not found')
    result = await mgr.solve(year, day)
    return templates.TemplateResponse('day.html', {'request': request, 'result': result, 'provided_input': None, 'year': year})


@app.post('/{year}/day/{day}', response_class=HTMLResponse)
async def day_post(request: Request, year: str, day: int, input_text: str = Form(''), input_file: UploadFile | None = File(None)):
    if year not in mgr.available_years():
        raise HTTPException(status_code=404, detail='Year not found')
    if day not in mgr.available_days(year):
        raise HTTPException(status_code=404, detail='Day not found')
    provided_input = None
    if input_file is not None and input_file.filename:
        raw = await input_file.read()
        try:
            provided_input = raw.decode('utf-8')
        except Exception:
            provided_input = raw.decode('utf-8', 'replace')
    elif input_text:
        provided_input = input_text

    result = await mgr.solve(year, day, data=provided_input)
    return templates.TemplateResponse('day.html', {'request': request, 'result': result, 'provided_input': provided_input, 'year': year})


@app.get('/api/{year}/day/{day}')
async def api_get_day(year: str, day: int):
    if year not in mgr.available_years():
        raise HTTPException(status_code=404, detail='Year not found')
    if day not in mgr.available_days(year):
        raise HTTPException(status_code=404, detail='Day not found')
    result = await mgr.solve(year, day)
    return JSONResponse(result)


@app.post('/api/{year}/day/{day}')
async def api_post_day(year: str, day: int, payload: dict):
    if year not in mgr.available_years():
        raise HTTPException(status_code=404, detail='Year not found')
    if day not in mgr.available_days(year):
        raise HTTPException(status_code=404, detail='Day not found')
    provided = payload.get('input') if isinstance(payload, dict) else None
    result = await mgr.solve(year, day, data=provided)
    return JSONResponse(result)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    accept = request.headers.get('accept', '')
    if 'text/html' in accept:
        return templates.TemplateResponse('error.html', {'request': request, 'error': exc.detail}, status_code=exc.status_code)
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print('Unhandled error:', exc)
    accept = request.headers.get('accept', '')
    msg = 'Internal server error'
    if 'text/html' in accept:
        return templates.TemplateResponse('error.html', {'request': request, 'error': msg}, status_code=500)
    return JSONResponse({'detail': msg}, status_code=500)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('web.main:app', host='127.0.0.1', port=8000, reload=True)