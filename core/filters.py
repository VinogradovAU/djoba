from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

def ts_to_datetime(ts) -> str:
    return ts.strftime('%Y-%m-%d %H:%M')

templates.env.filters["ts_to_datetime"] = ts_to_datetime