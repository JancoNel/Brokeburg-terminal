# Brokeburg-terminal

A DIY financial analysis terminal built with Excel and Python. Like a Bloomberg Terminal, but from Temu.com. :D

---

One night, I was bored and looking for something interesting to do, so I opened Excel and remembered that investment bankers apparently build valuation models in this thing for a living.

So I opened Pepkor Ltd's 2026 financial statements and started larping as an investment banker.

Somewhere along the way, I discovered Power Query and realised I could automate the process of fetching financial data for US companies instead of manually typing everything into spreadsheets like some kind of medieval accountant.

And then I lost the plot.

What started as a bit of financial-statement analysis gradually evolved into a general-purpose investment analysis tool, complete with financial metrics, statistical measures, and automated data retrieval.

I'm not a financial adviser (yet), so don't treat anything this spreadsheet tells you as financial advice. If you're new to investing or finance, though, feel free to give it a try. Just remember that a spreadsheet can do maths without necessarily being right about the market.

I may or may not update this project in the future. There's plenty of room for improvement, but somewhere along the way I misplaced some of my Accounting class notes on equity analysis, sooooo.

# How It Works (Kinda)

## Requirements

- Microsoft Excel with macro support (`.xlsm`).
- Python 3.x.
- Flask and yfinance, along with any other dependencies listed in `requirements.txt`.

## Getting Started

1. Install Python 3 if you haven't already.
2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the Python backend by running `server.py`. The server fetches most of the external data used by the workbook, so it needs to be running while you use the terminal.
4. Open `Terminal.xlsm` in Excel.
5. Enable macros only after you've reviewed and trust the workbook's VBA code. Some calculations depend on macros.

## Inputs

The terminal currently has five main inputs:

- **Stock ticker:** Supports many US-listed companies. Some tickers may fail or return incomplete data. For supported South African listings, append `.JO` to the ticker where applicable.
- **Risk-free rate:** Defaults to 4%. Change this to suit your analysis, or leave the default if you're unsure.
- **Market benchmark ticker:** Defaults to the S&P 500 benchmark. Keep the default if you're unsure which benchmark is appropriate.
- **Server IP address:** Leave the default unless you've changed the backend configuration.
- **Server port:** Leave the default unless you've changed the backend configuration.

The workbook uses these inputs to retrieve data and calculate various financial and statistical metrics. Results depend on data availability, the assumptions used, and the correctness of the underlying calculations.

Once everything is ready, press the big **Calculate** button and let the magic happen. Give it a minute or two; the backend has some work to do.

# Usage

Once the calculations finish, you can browse all the nerdy numbers and look up anything you don't understand. Alternatively, you can embrace laziness and head straight to the **Metrics** tab.

The metrics are colour-coded to make the results easier to interpret:

- 🟢 **Green:** The metric passes its configured check.
- 🟡 **Yellow:** The result needs further investigation.
- 🔴 **Red:** The metric fails its configured check.

If the cells are all green or yellow, the stock might be *kinda* worth investigating further.

**Important:** These checks are analytical flags, not buy or sell recommendations. A stock can pass every check and still be a terrible investment. I'm an idiot, the market is unpredictable, and this spreadsheet is not a substitute for your own research (Just something that might help your research). :D
