# Brokeburg-terminal

A DIY financial analysis terminal built with Excel and Python. Like a Bloomberg Terminal, but from Temu.com. :D

---

One night, I was bored and looking for something interesting to do, so I opened Excel and remembered that investment bankers apparently build valuation models in this thing for a living.

So I opened Pepkor Ltd's 2026 financial statements and started larping as an investment banker.

Somewhere along the way, I discovered Power Query and realised I could automate the process of fetching financial data for US companies instead of manually typing everything into spreadsheets like some kind of medieval accountant.

And then I lost the plot.

What started as a bit of financial-statement analysis gradually evolved into a general-purpose investment analysis tool, complete with financial metrics, statistical measures, and automated data retrieval.

I'm not a financial adviser, so don't treat anything this spreadsheet tells you as financial advice. If you're new to investing or finance, though, feel free to give it a try. Just remember that a spreadsheet can do maths without necessarily being right about the market.

I may or may not update this project in the future. There's plenty of room for improvement, but somewhere along the way I misplaced some of my Accounting class notes and started building a financial terminal instead. Priorities, I guess.

# How It Works (Or Whatever)

## Requirements

- Microsoft Excel with macro support (`.xlsm`).
- Python 3.x.
- The Python dependencies required by `server.py` (see the setup instructions below).

## Getting Started

1. Make sure Python 3 is installed.
2. Start the Python backend by running `server.py`. The server fetches most of the external data used by the workbook, so it needs to be running while you use the terminal.
3. Open `Terminal.xlsm` in Excel.
4. Enable macros if you trust the workbook and have reviewed its contents. Some calculations depend on VBA macros.

## Inputs

The terminal currently has five main inputs:

- **Stock ticker:** Supports many US-listed companies. Some tickers may fail or return incomplete data. For supported South African listings, append `.JO` to the ticker where applicable.
- **Risk-free rate:** Defaults to 4%. Change this to suit your analysis; if you're unsure what to use, leave the default.
- **Market benchmark ticker:** Defaults to the S&P 500 benchmark. Keep the default if you're unsure which benchmark is appropriate.
- **Server IP address:** Leave the default unless you've changed the backend configuration.
- **Server port:** Leave the default unless you've changed the backend configuration.

The workbook uses these inputs to retrieve data and calculate various financial and statistical metrics. Results depend on data availability, the assumptions used, and the correctness of the underlying calculations.
