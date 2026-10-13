from __future__ import annotations

from datetime import date, timedelta
import math
import time
from numbers import Real
from typing import Any, Iterable

import flask
import yfinance as yf

TARGET_DAYS = (7, 14, 21, 30, 60, 90, 180, 365)
SERVER_PORT = 5000


app = flask.Flask(__name__)


def valid_number(value: Any) -> bool:
    return isinstance(value, Real) and math.isfinite(float(value))


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    return number if math.isfinite(number) else None


def quote_value(ticker: Any, *names: str) -> float | None:
    for name in names:
        value = getattr(ticker, name, None)

        if valid_number(value):
            return float(value)

    return None


def underlying_price(ticker: Any) -> float | None:
    # Try Yahoo's fast_info first.
    fast_info = getattr(ticker, "fast_info", {}) or {}

    price = finite_float(fast_info.get("last_price"))

    if price is not None:
        return price

    # Fallback to recent historical data.
    history = ticker.history(period="5d", auto_adjust=False)

    if history.empty:
        return None

    return finite_float(history["Close"].dropna().iloc[-1])


def row_price(row: Any) -> tuple[float | None, float | None, float | None]:

    bid = finite_float(row.get("bid"))
    ask = finite_float(row.get("ask"))
    last = finite_float(row.get("lastPrice"))

    # Prefer bid/ask midpoint.
    if bid is not None and ask is not None and bid >= 0 and ask >= 0 and ask >= bid:
        return (bid + ask) / 2, bid, ask

    # Fall back to last traded price.
    return last, bid, ask


def parse_expirations(expirations: Iterable[str], today: date) -> list[date]:

    parsed = set()

    for value in expirations:
        try:
            normalized = str(value).replace("-", "")

            parsed.add(
                date(
                    int(normalized[:4]),
                    int(normalized[4:6]),
                    int(normalized[6:8]),
                )
            )

        except (TypeError, ValueError, IndexError):
            continue

    return sorted(expiry for expiry in parsed if expiry >= today)


def select_expirations(
    expirations: Iterable[str], today: date, targets: Iterable[int] = TARGET_DAYS
) -> list[dict[str, int | str]]:

    available = parse_expirations(expirations, today)

    selected: list[dict[str, int | str]] = []

    if not available:
        return selected

    used: set[date] = set()

    for target in targets:

        target_date = today + timedelta(days=target)

        nearest = min(available, key=lambda expiry: abs((expiry - target_date).days))

        actual = (nearest - today).days

        # Don't select an expiry that's wildly beyond
        # the requested maturity.
        if actual <= target * 1.5 and nearest not in used:
            selected.append(
                {
                    "expiry": nearest.strftime("%Y%m%d"),
                    "target": target,
                    "actual": actual,
                }
            )

            used.add(nearest)

    return selected


def nearest_row(frame: Any, underlying: float) -> Any | None:

    if frame is None or frame.empty or "strike" not in frame.columns:
        return None

    strikes = frame["strike"].map(finite_float)

    valid = frame.loc[strikes.notna()].copy()

    if valid.empty:
        return None

    valid["_distance"] = (valid["strike"] - underlying).abs()

    return valid.sort_values("_distance").iloc[0]


def fetch_options(symbol: str, today: date | None = None) -> dict[str, Any]:

    today = today or date.today()

    symbol = symbol.upper().strip()

    ticker = yf.Ticker(symbol)

    underlying = underlying_price(ticker)

    if underlying is None:
        raise ValueError(f"No price available for {symbol}")

    expirations = select_expirations(ticker.options, today)

    if not expirations:
        raise ValueError(f"No future option expirations available for {symbol}")

    results = []

    for expiry_info in expirations:

        expiry = str(expiry_info["expiry"])

        expiry_string = f"{expiry[:4]}-" f"{expiry[4:6]}-" f"{expiry[6:8]}"

        chain = ticker.option_chain(expiry_string)

        for right, frame in (
            ("C", chain.calls),
            ("P", chain.puts),
        ):

            row = nearest_row(frame, underlying)

            if row is None:
                continue

            price, bid, ask = row_price(row)

            if price is None or price < 0:
                continue

            results.append(
                {
                    "expiry": expiry,
                    "target_days": expiry_info["target"],
                    "actual_days": expiry_info["actual"],
                    "strike": float(row["strike"]),
                    "right": right,
                    "price": price,
                    "bid": bid,
                    "ask": ask,
                    "last": finite_float(row.get("lastPrice")),
                    "volume": finite_float(row.get("volume")),
                    "open_interest": finite_float(row.get("openInterest")),
                    "contract_symbol": row.get("contractSymbol"),
                }
            )

    if not results:
        raise ValueError(f"No option prices available for {symbol}")

    return {
        "ticker": symbol,
        "underlying": underlying,
        "timestamp": time.time(),
        "data_count": len(results),
        "data": results,
    }


@app.route("/options")
def options():

    ticker = flask.request.args.get("ticker", "").upper().strip()

    if not ticker:
        return {"error": "Missing ticker"}, 400

    try:
        return fetch_options(ticker)

    except ValueError as error:
        return {"error": str(error)}, 404

    except Exception:
        app.logger.exception("Yahoo Finance request failed for %s", ticker)

        return {"error": "Yahoo Finance request failed"}, 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=SERVER_PORT, debug=False)
