## This is a documentation on how to implement the finance-query endpoint to the 
@stonksapi/finance-query folder 

## Data Type 

# Hours endpoint 
https://finance-query.onrender.com/hours

# JSON format the endpoint returns 
{
  "status": "open",
  "reason": "Regular trading hours.",
  "timestamp": "2021-09-22T14:00:00.000Z"
}

# Detailed data for stocks endpoint
https://finance-query.onrender.com/v1/quotes?symbols=PSIX <-- the symbol should
be dynamic - no hardcode on the package 

# JSON format the endpoint returns 
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": "145.00",
    "preMarketPrice": "145.50",
    "afterHoursPrice": "145.50",
    "change": "+1.00",
    "percentChange": "+0.69%",
    "open": "144.00",
    "high": "146.00",
    "low": "143.00",
    "yearHigh": "150.00",
    "yearLow": "100.00",
    "volume": 1000000,
    "avgVolume": 2000000,
    "marketCap": "2.5T",
    "beta": 1.23,
    "pe": "30.00",
    "eps": "4.50",
    "dividend": "0.82",
    "yield": "1.3%",
    "exDividend": "Feb 5, 2024",
    "netAssets": "10.5B",
    "nav": "100.00",
    "expenseRatio": "0.05%",
    "category": "Large Growth",
    "lastCapitalGain": "10.00",
    "morningstarRating": "★★",
    "morningstarRiskRating": "Low",
    "holdingsTurnover": "5.00%",
    "earningsDate": "Apr 23, 2024",
    "lastDividend": "0.82",
    "inceptionDate": "Jan 1, 2020",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "about": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
    "employees": "150,000",
    "fiveDaysReturn": "-19.35%",
    "oneMonthReturn": "-28.48%",
    "threeMonthReturn": "-14.02%",
    "sixMonthReturn": "36.39%",
    "ytdReturn": "+10.00%",
    "yearReturn": "+20.00%",
    "threeYearReturn": "+30.00%",
    "fiveYearReturn": "+40.00%",
    "tenYearReturn": "2,005.31%",
    "maxReturn": "22,857.89%",
    "logo": "https://img.logo.dev/apple.com?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  }
]

# Simple data for stocks endpoint
https://finance-query.onrender.com/v1/simple-quotes?symbols=PSIX <-- the symbol should
be dynamic - no hardcode on the package 

# JSON format the endpoint returns 
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": "145.00",
    "preMarketPrice": "145.50",
    "afterHoursPrice": "145.50",
    "change": "+1.00",
    "percentChange": "+0.69%",
    "logo": "https://img.logo.dev/apple.com?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  }
]

# Similar stock quote endpoint
https://finance-query.onrender.com/v1/similar?symbol=TSLA&limit=20 <-- the symbol should
be dynamic - no hardcode on the package & the limit will be dynamic - no hardcode

# JSON format the endpoint returns 
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": "257.13",
    "change": "+1.68",
    "percentChange": "+0.66%",
    "logo": "https://img.logo.dev/ticker/AAPL?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "AMZN",
    "name": "Amazon.com, Inc.",
    "price": "222.41",
    "change": "+1.78",
    "percentChange": "+0.81%",
    "logo": "https://img.logo.dev/ticker/AMZN?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "META",
    "name": "Meta Platforms, Inc.",
    "price": "727.05",
    "change": "+9.71",
    "percentChange": "+1.35%",
    "logo": "https://img.logo.dev/ticker/META?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "GOOG",
    "name": "Alphabet Inc.",
    "price": "246.43",
    "change": "+0.89",
    "percentChange": "+0.36%",
    "logo": "https://img.logo.dev/ticker/GOOG?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "NVDA",
    "name": "NVIDIA Corporation",
    "price": "188.89",
    "change": "+1.65",
    "percentChange": "+0.88%",
    "logo": "https://img.logo.dev/ticker/NVDA?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "NFLX",
    "name": "Netflix, Inc.",
    "price": "1162.53",
    "change": "-8.37",
    "percentChange": "-0.71%",
    "logo": "https://img.logo.dev/ticker/NFLX?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "MSFT",
    "name": "Microsoft Corporation",
    "price": "515.74",
    "change": "-3.97",
    "percentChange": "-0.76%",
    "logo": "https://img.logo.dev/ticker/MSFT?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "AMD",
    "name": "Advanced Micro Devices, Inc.",
    "price": "169.73",
    "change": "+5.72",
    "percentChange": "+3.49%",
    "logo": "https://img.logo.dev/ticker/AMD?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "DIS",
    "name": "The Walt Disney Company",
    "price": "112.14",
    "change": "-0.81",
    "percentChange": "-0.72%",
    "logo": "https://img.logo.dev/ticker/DIS?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "INTC",
    "name": "Intel Corporation",
    "price": "37.30",
    "change": "+1.36",
    "percentChange": "+3.78%",
    "logo": "https://img.logo.dev/ticker/INTC?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "PLTR",
    "name": "Palantir Technologies Inc.",
    "price": "187.05",
    "change": "+2.10",
    "percentChange": "+1.14%",
    "logo": "https://img.logo.dev/ticker/PLTR?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "BA",
    "name": "The Boeing Company",
    "price": "217.43",
    "change": "+2.23",
    "percentChange": "+1.04%",
    "logo": "https://img.logo.dev/ticker/BA?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "BABA",
    "name": "Alibaba Group Holding Limited",
    "price": "189.34",
    "change": "+6.56",
    "percentChange": "+3.59%",
    "logo": "https://img.logo.dev/ticker/BABA?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "F",
    "name": "Ford Motor Company",
    "price": "12.22",
    "change": "-0.05",
    "percentChange": "-0.41%",
    "logo": "https://img.logo.dev/ticker/F?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "NIO",
    "name": "NIO Inc.",
    "price": "7.89",
    "change": "+0.24",
    "percentChange": "+3.14%",
    "logo": "https://img.logo.dev/ticker/NIO?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  },
  {
    "symbol": "JPM",
    "name": "JPMorgan Chase & Co.",
    "price": "307.55",
    "change": "-3.16",
    "percentChange": "-1.02%",
    "logo": "https://img.logo.dev/ticker/JPM?token=pk_Xd1Cdye3QYmCOXzcvxhxyw&retina=true"
  }
]


# Historical data Endpoint 
https://finance-query.onrender.com/v1/historical?symbol=TSLA&range=1d&interval=5m 
<-- The symbol will not be hardcoded on the package, it will be dynamic 
The range & Interval will not be hardcoded it will be dynamic 

Users will be able to pass in these Range & Interval 

Range 
1d 
5d
1mo
3mo
6m0

Interval 
1m
5m
15m
30m 
1h
1d
1wk
1mo

# JSON format the endpoint returns 
{
  "2025-10-02 16:00:00": {
    "open": 436,
    "high": 436,
    "low": 436,
    "close": 436,
    "adjClose": null,
    "volume": 0
  },
  "2025-10-02 15:55:00": {
    "open": 436.24,
    "high": 437.09,
    "low": 435.57,
    "close": 435.97,
    "adjClose": null,
    "volume": 3081391
  },
  "2025-10-02 15:50:00": {
    "open": 438.98,
    "high": 439.04,
    "low": 435.97,
    "close": 436.22,
    "adjClose": null,
    "volume": 2729862
  },
  "2025-10-02 15:45:00": {
    "open": 439.1,
    "high": 439.42,
    "low": 438.09,
    "close": 438.94,
    "adjClose": null,
    "volume": 1660001
  },
  "2025-10-02 15:40:00": {
    "open": 440.41,
    "high": 440.7,
    "low": 439.04,
    "close": 439.08,
    "adjClose": null,
    "volume": 1324957
  },
  "2025-10-02 15:35:00": {
    "open": 441.06,
    "high": 441.12,
    "low": 439.63,
    "close": 440.4,
    "adjClose": null,
    "volume": 1421228
  },
  "2025-10-02 15:30:00": {
    "open": 442.79,
    "high": 443.04,
    "low": 440.63,
    "close": 441.05,
    "adjClose": null,
    "volume": 1254514
  },
  "2025-10-02 15:25:00": {
    "open": 442.73,
    "high": 443.22,
    "low": 442.22,
    "close": 442.78,
    "adjClose": null,
    "volume": 786154
  },
  "2025-10-02 15:20:00": {
    "open": 442.35,
    "high": 443.37,
    "low": 442.25,
    "close": 442.73,
    "adjClose": null,
    "volume": 1544089
  },
  "2025-10-02 15:15:00": {
    "open": 442.02,
    "high": 442.45,
    "low": 441.5,
    "close": 442.36,
    "adjClose": null,
    "volume": 811555
  },
  "2025-10-02 15:10:00": {
    "open": 441.9,
    "high": 442.37,
    "low": 441.04,
    "close": 442.02,
    "adjClose": null,
    "volume": 1031321
  },
  "2025-10-02 15:05:00": {
    "open": 443.43,
    "high": 444.2,
    "low": 441.72,
    "close": 441.91,
    "adjClose": null,
    "volume": 1474270
  },
  "2025-10-02 15:00:00": {
    "open": 441.02,
    "high": 443.49,
    "low": 441,
    "close": 443.4,
    "adjClose": null,
    "volume": 1298373
  },
  "2025-10-02 14:55:00": {
    "open": 441.13,
    "high": 441.58,
    "low": 440.72,
    "close": 441.05,
    "adjClose": null,
    "volume": 713789
  },
  "2025-10-02 14:50:00": {
    "open": 441.45,
    "high": 441.49,
    "low": 440.7,
    "close": 441.13,
    "adjClose": null,
    "volume": 691400
  },
  "2025-10-02 14:45:00": {
    "open": 441.34,
    "high": 441.63,
    "low": 439.99,
    "close": 441.43,
    "adjClose": null,
    "volume": 984115
  },
  "2025-10-02 14:40:00": {
    "open": 441.17,
    "high": 441.5,
    "low": 440.69,
    "close": 441.36,
    "adjClose": null,
    "volume": 865345
  },
  "2025-10-02 14:35:00": {
    "open": 440.16,
    "high": 441.27,
    "low": 438.45,
    "close": 441.15,
    "adjClose": null,
    "volume": 1648919
  },
  "2025-10-02 14:30:00": {
    "open": 441.19,
    "high": 441.6,
    "low": 440,
    "close": 440.15,
    "adjClose": null,
    "volume": 1068659
  },
  "2025-10-02 14:25:00": {
    "open": 442.42,
    "high": 442.45,
    "low": 439.08,
    "close": 441.25,
    "adjClose": null,
    "volume": 1526459
  },
  "2025-10-02 14:20:00": {
    "open": 442.93,
    "high": 443.3,
    "low": 442.35,
    "close": 442.42,
    "adjClose": null,
    "volume": 716051
  },
  "2025-10-02 14:15:00": {
    "open": 442.76,
    "high": 443.17,
    "low": 442.1,
    "close": 442.95,
    "adjClose": null,
    "volume": 723538
  },
  "2025-10-02 14:10:00": {
    "open": 441.59,
    "high": 442.87,
    "low": 441.42,
    "close": 442.77,
    "adjClose": null,
    "volume": 837307
  },
  "2025-10-02 14:05:00": {
    "open": 441.15,
    "high": 442.32,
    "low": 441.08,
    "close": 441.58,
    "adjClose": null,
    "volume": 964972
  },
  "2025-10-02 14:00:00": {
    "open": 441.02,
    "high": 441.56,
    "low": 440.41,
    "close": 441.07,
    "adjClose": null,
    "volume": 956380
  },
  "2025-10-02 13:55:00": {
    "open": 441.17,
    "high": 441.63,
    "low": 440.65,
    "close": 441.03,
    "adjClose": null,
    "volume": 863911
  },
  "2025-10-02 13:50:00": {
    "open": 441.6,
    "high": 442,
    "low": 440.5,
    "close": 441.26,
    "adjClose": null,
    "volume": 1100435
  },
  "2025-10-02 13:45:00": {
    "open": 442.82,
    "high": 443.21,
    "low": 439.6,
    "close": 441.55,
    "adjClose": null,
    "volume": 2310018
  },
  "2025-10-02 13:40:00": {
    "open": 443.31,
    "high": 444.66,
    "low": 442.48,
    "close": 442.8,
    "adjClose": null,
    "volume": 1245149
  },
  "2025-10-02 13:35:00": {
    "open": 446.24,
    "high": 446.4,
    "low": 442.63,
    "close": 443.28,
    "adjClose": null,
    "volume": 1357012
  },
  "2025-10-02 13:30:00": {
    "open": 445.89,
    "high": 446.78,
    "low": 445.37,
    "close": 446.27,
    "adjClose": null,
    "volume": 1213159
  },
  "2025-10-02 13:25:00": {
    "open": 444.16,
    "high": 446.05,
    "low": 444.01,
    "close": 445.89,
    "adjClose": null,
    "volume": 1294973
  },
  "2025-10-02 13:20:00": {
    "open": 443.03,
    "high": 444.29,
    "low": 442.65,
    "close": 444.19,
    "adjClose": null,
    "volume": 977456
  },
  "2025-10-02 13:15:00": {
    "open": 443.48,
    "high": 443.67,
    "low": 442.2,
    "close": 443.09,
    "adjClose": null,
    "volume": 854335
  },
  "2025-10-02 13:10:00": {
    "open": 443.4,
    "high": 444.22,
    "low": 442.68,
    "close": 443.49,
    "adjClose": null,
    "volume": 821170
  },
  "2025-10-02 13:05:00": {
    "open": 443.8,
    "high": 444.75,
    "low": 443.29,
    "close": 443.45,
    "adjClose": null,
    "volume": 879423
  },
  "2025-10-02 13:00:00": {
    "open": 444.02,
    "high": 444.5,
    "low": 443.44,
    "close": 443.85,
    "adjClose": null,
    "volume": 1011776
  },
  "2025-10-02 12:55:00": {
    "open": 443.65,
    "high": 444.42,
    "low": 443.28,
    "close": 444.06,
    "adjClose": null,
    "volume": 855294
  },
  "2025-10-02 12:50:00": {
    "open": 442.6,
    "high": 444.3,
    "low": 442.52,
    "close": 443.71,
    "adjClose": null,
    "volume": 1218587
  },
  "2025-10-02 12:45:00": {
    "open": 442.9,
    "high": 443.29,
    "low": 441.46,
    "close": 442.56,
    "adjClose": null,
    "volume": 1835741
  },
  "2025-10-02 12:40:00": {
    "open": 446.16,
    "high": 446.28,
    "low": 442.9,
    "close": 442.97,
    "adjClose": null,
    "volume": 1837440
  },
  "2025-10-02 12:35:00": {
    "open": 447.16,
    "high": 447.3,
    "low": 445.33,
    "close": 446.17,
    "adjClose": null,
    "volume": 1041985
  },
  "2025-10-02 12:30:00": {
    "open": 447.37,
    "high": 447.8,
    "low": 447.01,
    "close": 447.11,
    "adjClose": null,
    "volume": 592974
  },
  "2025-10-02 12:25:00": {
    "open": 447.02,
    "high": 447.5,
    "low": 446.65,
    "close": 447.38,
    "adjClose": null,
    "volume": 584606
  },
  "2025-10-02 12:20:00": {
    "open": 448.17,
    "high": 448.2,
    "low": 446.88,
    "close": 447.02,
    "adjClose": null,
    "volume": 783953
  },
  "2025-10-02 12:15:00": {
    "open": 448.19,
    "high": 448.7,
    "low": 447.52,
    "close": 448.19,
    "adjClose": null,
    "volume": 899051
  },
  "2025-10-02 12:10:00": {
    "open": 448.1,
    "high": 448.38,
    "low": 447.49,
    "close": 448.26,
    "adjClose": null,
    "volume": 701390
  },
  "2025-10-02 12:05:00": {
    "open": 447.96,
    "high": 448.58,
    "low": 446.62,
    "close": 448.1,
    "adjClose": null,
    "volume": 1051137
  },
  "2025-10-02 12:00:00": {
    "open": 447.53,
    "high": 449.02,
    "low": 446.84,
    "close": 448.06,
    "adjClose": null,
    "volume": 1326113
  },
  "2025-10-02 11:55:00": {
    "open": 448.11,
    "high": 448.77,
    "low": 447.58,
    "close": 447.58,
    "adjClose": null,
    "volume": 1231153
  },
  "2025-10-02 11:50:00": {
    "open": 445.04,
    "high": 448.22,
    "low": 444.95,
    "close": 448.15,
    "adjClose": null,
    "volume": 1676872
  },
  "2025-10-02 11:45:00": {
    "open": 446.1,
    "high": 446.99,
    "low": 444.73,
    "close": 444.98,
    "adjClose": null,
    "volume": 2016604
  },
  "2025-10-02 11:40:00": {
    "open": 446.38,
    "high": 448.25,
    "low": 445.9,
    "close": 446.12,
    "adjClose": null,
    "volume": 1964984
  },
  "2025-10-02 11:35:00": {
    "open": 450.12,
    "high": 450.26,
    "low": 446.11,
    "close": 446.43,
    "adjClose": null,
    "volume": 2362319
  },
  "2025-10-02 11:30:00": {
    "open": 450.35,
    "high": 451.14,
    "low": 448.7,
    "close": 450.07,
    "adjClose": null,
    "volume": 1977976
  },
  "2025-10-02 11:25:00": {
    "open": 453.63,
    "high": 453.72,
    "low": 450.15,
    "close": 450.3,
    "adjClose": null,
    "volume": 1553228
  },
  "2025-10-02 11:20:00": {
    "open": 453.67,
    "high": 454.36,
    "low": 453.02,
    "close": 453.64,
    "adjClose": null,
    "volume": 1165923
  },
  "2025-10-02 11:15:00": {
    "open": 453.36,
    "high": 453.97,
    "low": 452.9,
    "close": 453.64,
    "adjClose": null,
    "volume": 951488
  },
  "2025-10-02 11:10:00": {
    "open": 452.29,
    "high": 453.61,
    "low": 452.16,
    "close": 453.33,
    "adjClose": null,
    "volume": 1394765
  },
  "2025-10-02 11:05:00": {
    "open": 449.89,
    "high": 452.58,
    "low": 449.89,
    "close": 452.28,
    "adjClose": null,
    "volume": 1591643
  },
  "2025-10-02 11:00:00": {
    "open": 452.79,
    "high": 453.68,
    "low": 449.34,
    "close": 449.85,
    "adjClose": null,
    "volume": 2540921
  },
  "2025-10-02 10:55:00": {
    "open": 453.58,
    "high": 454.24,
    "low": 452.5,
    "close": 452.8,
    "adjClose": null,
    "volume": 1088057
  },
  "2025-10-02 10:50:00": {
    "open": 454.55,
    "high": 454.98,
    "low": 453.3,
    "close": 453.58,
    "adjClose": null,
    "volume": 908603
  },
  "2025-10-02 10:45:00": {
    "open": 455.61,
    "high": 456.05,
    "low": 453,
    "close": 454.54,
    "adjClose": null,
    "volume": 1364906
  },
  "2025-10-02 10:40:00": {
    "open": 454.67,
    "high": 455.96,
    "low": 454.65,
    "close": 455.57,
    "adjClose": null,
    "volume": 1397063
  },
  "2025-10-02 10:35:00": {
    "open": 452.08,
    "high": 454.9,
    "low": 451.88,
    "close": 454.67,
    "adjClose": null,
    "volume": 1523602
  },
  "2025-10-02 10:30:00": {
    "open": 454.75,
    "high": 455.43,
    "low": 451.7,
    "close": 452.08,
    "adjClose": null,
    "volume": 2320096
  },
  "2025-10-02 10:25:00": {
    "open": 454.4,
    "high": 455.95,
    "low": 454.38,
    "close": 454.75,
    "adjClose": null,
    "volume": 1217520
  },
  "2025-10-02 10:20:00": {
    "open": 455.27,
    "high": 456.1,
    "low": 453.51,
    "close": 454.47,
    "adjClose": null,
    "volume": 1898192
  },
  "2025-10-02 10:15:00": {
    "open": 456.4,
    "high": 457.52,
    "low": 455.07,
    "close": 455.32,
    "adjClose": null,
    "volume": 1627151
  },
  "2025-10-02 10:10:00": {
    "open": 458.91,
    "high": 459.52,
    "low": 456.14,
    "close": 456.44,
    "adjClose": null,
    "volume": 1728730
  },
  "2025-10-02 10:05:00": {
    "open": 458.92,
    "high": 459.19,
    "low": 455.87,
    "close": 458.97,
    "adjClose": null,
    "volume": 1811375
  },
  "2025-10-02 10:00:00": {
    "open": 456.73,
    "high": 459.32,
    "low": 456.12,
    "close": 458.95,
    "adjClose": null,
    "volume": 2073965
  },
  "2025-10-02 09:55:00": {
    "open": 456.05,
    "high": 457.67,
    "low": 453.38,
    "close": 456.65,
    "adjClose": null,
    "volume": 2929795
  },
  "2025-10-02 09:50:00": {
    "open": 457.84,
    "high": 458.43,
    "low": 455.69,
    "close": 456.05,
    "adjClose": null,
    "volume": 2836590
  },
  "2025-10-02 09:45:00": {
    "open": 454.78,
    "high": 461.75,
    "low": 454.35,
    "close": 457.86,
    "adjClose": null,
    "volume": 4198910
  },
  "2025-10-02 09:40:00": {
    "open": 462.42,
    "high": 463.69,
    "low": 454.6,
    "close": 454.74,
    "adjClose": null,
    "volume": 4704722
  },
  "2025-10-02 09:35:00": {
    "open": 466.08,
    "high": 466.32,
    "low": 461.34,
    "close": 462.46,
    "adjClose": null,
    "volume": 3974697
  },
  "2025-10-02 09:30:00": {
    "open": 470.54,
    "high": 470.75,
    "low": 466,
    "close": 466.12,
    "adjClose": null,
    "volume": 15825523
  }
}

# Most actives endpoint
https://finance-query.onrender.com/v1/actives <-- user will be able to 
pass in the numbers of stocks they want in their request 

25, 50, & 100 

# JSON format the endppint returns
[
  {
    "symbol": "OPEN",
    "name": "Opendoor Technologies Inc.",
    "price": "8.01",
    "change": "-0.05",
    "percentChange": "-0.62%"
  },
  {
    "symbol": "INTC",
    "name": "Intel Corporation",
    "price": "37.30",
    "change": "1.36",
    "percentChange": "3.78%"
  },
  {
    "symbol": "RGTI",
    "name": "Rigetti Computing, Inc.",
    "price": "35.40",
    "change": "5.55",
    "percentChange": "18.59%"
  },
  {
    "symbol": "TSLA",
    "name": "Tesla, Inc.",
    "price": "436.00",
    "change": "-23.46",
    "percentChange": "-5.11%"
  },
  {
    "symbol": "NVDA",
    "name": "NVIDIA Corporation",
    "price": "188.89",
    "change": "1.65",
    "percentChange": "0.88%"
  },
  {
    "symbol": "PLUG",
    "name": "Plug Power Inc.",
    "price": "2.8300",
    "change": "-0.1000",
    "percentChange": "-3.41%"
  },
  {
    "symbol": "SNAP",
    "name": "Snap Inc.",
    "price": "8.22",
    "change": "0.51",
    "percentChange": "6.61%"
  },
  {
    "symbol": "ONDS",
    "name": "Ondas Holdings Inc.",
    "price": "9.21",
    "change": "1.90",
    "percentChange": "25.99%"
  },
  {
    "symbol": "PSLV",
    "name": "Sprott Physical Silver Trust",
    "price": "15.76",
    "change": "-0.18",
    "percentChange": "-1.13%"
  },
  {
    "symbol": "DNN",
    "name": "Denison Mines Corp.",
    "price": "2.7700",
    "change": "0.0000",
    "percentChange": "0.00%"
  },
  {
    "symbol": "BBAI",
    "name": "BigBear.ai Holdings, Inc.",
    "price": "7.27",
    "change": "0.29",
    "percentChange": "4.15%"
  },
  {
    "symbol": "NIO",
    "name": "NIO Inc.",
    "price": "7.89",
    "change": "0.24",
    "percentChange": "3.14%"
  },
  {
    "symbol": "SOUN",
    "name": "SoundHound AI, Inc.",
    "price": "17.84",
    "change": "1.69",
    "percentChange": "10.46%"
  },
  {
    "symbol": "RKT",
    "name": "Rocket Companies, Inc.",
    "price": "18.37",
    "change": "-1.22",
    "percentChange": "-6.23%"
  },
  {
    "symbol": "AAL",
    "name": "American Airlines Group Inc.",
    "price": "11.43",
    "change": "0.16",
    "percentChange": "1.42%"
  },
  {
    "symbol": "RIVN",
    "name": "Rivian Automotive, Inc.",
    "price": "13.53",
    "change": "-1.08",
    "percentChange": "-7.39%"
  },
  {
    "symbol": "F",
    "name": "Ford Motor Company",
    "price": "12.22",
    "change": "-0.05",
    "percentChange": "-0.41%"
  },
  {
    "symbol": "QBTS",
    "name": "D-Wave Quantum Inc.",
    "price": "29.21",
    "change": "3.58",
    "percentChange": "13.97%"
  },
  {
    "symbol": "PFE",
    "name": "Pfizer Inc.",
    "price": "27.08",
    "change": "-0.13",
    "percentChange": "-0.48%"
  },
  {
    "symbol": "ABEV",
    "name": "Ambev S.A.",
    "price": "2.1900",
    "change": "-0.0200",
    "percentChange": "-0.90%"
  },
  {
    "symbol": "QS",
    "name": "QuantumScape Corporation",
    "price": "14.30",
    "change": "-0.29",
    "percentChange": "-1.99%"
  },
  {
    "symbol": "RXRX",
    "name": "Recursion Pharmaceuticals, Inc.",
    "price": "5.52",
    "change": "0.42",
    "percentChange": "8.24%"
  },
  {
    "symbol": "SOFI",
    "name": "SoFi Technologies, Inc.",
    "price": "25.97",
    "change": "0.21",
    "percentChange": "0.82%"
  },
  {
    "symbol": "MARA",
    "name": "MARA Holdings, Inc.",
    "price": "18.79",
    "change": "0.18",
    "percentChange": "0.97%"
  },
  {
    "symbol": "CIFR",
    "name": "Cipher Mining Inc.",
    "price": "13.81",
    "change": "1.21",
    "percentChange": "9.60%"
  }
]


# Top gainers endpoint
https://finance-query.onrender.com/v1/gainers <-- user will be able to 
pass in the numbers of stocks they want in their request 

25, 50, & 100 

# JSON format  the endpoint return
[
  {
    "symbol": "ONDS",
    "name": "Ondas Holdings Inc.",
    "price": "9.21",
    "change": "1.90",
    "percentChange": "25.99%"
  },
  {
    "symbol": "RZLV",
    "name": "Rezolve AI PLC",
    "price": "6.28",
    "change": "1.22",
    "percentChange": "24.01%"
  },
  {
    "symbol": "USAR",
    "name": "USA Rare Earth, Inc.",
    "price": "22.71",
    "change": "4.30",
    "percentChange": "23.36%"
  },
  {
    "symbol": "RGTI",
    "name": "Rigetti Computing, Inc.",
    "price": "35.40",
    "change": "5.55",
    "percentChange": "18.59%"
  },
  {
    "symbol": "FICO",
    "name": "Fair Isaac Corporation",
    "price": "1,784.68",
    "change": "271.97",
    "percentChange": "17.98%"
  },
  {
    "symbol": "ASTS",
    "name": "AST SpaceMobile, Inc.",
    "price": "66.16",
    "change": "9.22",
    "percentChange": "16.19%"
  },
  {
    "symbol": "CRCL",
    "name": "Circle Internet Group",
    "price": "149.72",
    "change": "20.69",
    "percentChange": "16.03%"
  },
  {
    "symbol": "SRPT",
    "name": "Sarepta Therapeutics, Inc.",
    "price": "22.35",
    "change": "3.03",
    "percentChange": "15.68%"
  },
  {
    "symbol": "QBTS",
    "name": "D-Wave Quantum Inc.",
    "price": "29.21",
    "change": "3.58",
    "percentChange": "13.97%"
  },
  {
    "symbol": "BLSH",
    "name": "Bullish",
    "price": "67.91",
    "change": "7.10",
    "percentChange": "11.68%"
  },
  {
    "symbol": "OKLO",
    "name": "Oklo Inc.",
    "price": "128.80",
    "change": "12.87",
    "percentChange": "11.10%"
  },
  {
    "symbol": "SOUN",
    "name": "SoundHound AI, Inc.",
    "price": "17.84",
    "change": "1.69",
    "percentChange": "10.46%"
  },
  {
    "symbol": "IONQ",
    "name": "IonQ, Inc.",
    "price": "69.60",
    "change": "6.51",
    "percentChange": "10.32%"
  },
  {
    "symbol": "CRSP",
    "name": "CRISPR Therapeutics AG",
    "price": "72.82",
    "change": "6.66",
    "percentChange": "10.07%"
  },
  {
    "symbol": "JOBY",
    "name": "Joby Aviation, Inc.",
    "price": "17.80",
    "change": "1.58",
    "percentChange": "9.74%"
  },
  {
    "symbol": "CIFR",
    "name": "Cipher Mining Inc.",
    "price": "13.81",
    "change": "1.21",
    "percentChange": "9.60%"
  },
  {
    "symbol": "SYM",
    "name": "Symbotic Inc.",
    "price": "63.62",
    "change": "5.52",
    "percentChange": "9.50%"
  },
  {
    "symbol": "KLAR",
    "name": "Klarna Group plc",
    "price": "40.74",
    "change": "3.51",
    "percentChange": "9.43%"
  },
  {
    "symbol": "RKLB",
    "name": "Rocket Lab Corporation",
    "price": "52.47",
    "change": "4.50",
    "percentChange": "9.38%"
  },
  {
    "symbol": "CELC",
    "name": "Celcuity Inc.",
    "price": "49.42",
    "change": "4.20",
    "percentChange": "9.29%"
  },
  {
    "symbol": "WRD",
    "name": "WeRide Inc.",
    "price": "11.27",
    "change": "0.95",
    "percentChange": "9.21%"
  },
  {
    "symbol": "FIGR",
    "name": "Figure Technology Solutions, Inc.",
    "price": "41.28",
    "change": "3.46",
    "percentChange": "9.15%"
  },
  {
    "symbol": "NTLA",
    "name": "Intellia Therapeutics, Inc.",
    "price": "20.44",
    "change": "1.68",
    "percentChange": "8.96%"
  },
  {
    "symbol": "NBIS",
    "name": "Nebius Group N.V.",
    "price": "125.87",
    "change": "10.26",
    "percentChange": "8.87%"
  },
  {
    "symbol": "MENS",
    "name": "Jyong Biotech Ltd.",
    "price": "52.00",
    "change": "4.14",
    "percentChange": "8.65%"
  }
]



# Top loserss endpoint
https://finance-query.onrender.com/v1/losers <-- user will be able to 
pass in the numbers of stocks they want in their request 

25, 50, & 100 

# JSON format the endpoint returns 
[
  {
    "symbol": "TRU",
    "name": "TransUnion",
    "price": "73.51",
    "change": "-8.75",
    "percentChange": "-10.64%"
  },
  {
    "symbol": "EFX",
    "name": "Equifax Inc.",
    "price": "232.35",
    "change": "-21.49",
    "percentChange": "-8.47%"
  },
  {
    "symbol": "FORD",
    "name": "Forward Industries, Inc.",
    "price": "24.51",
    "change": "-2.22",
    "percentChange": "-8.31%"
  },
  {
    "symbol": "RIVN",
    "name": "Rivian Automotive, Inc.",
    "price": "13.53",
    "change": "-1.08",
    "percentChange": "-7.39%"
  },
  {
    "symbol": "OXY",
    "name": "Occidental Petroleum Corporation",
    "price": "44.23",
    "change": "-3.49",
    "percentChange": "-7.31%"
  },
  {
    "symbol": "GEO",
    "name": "The GEO Group, Inc.",
    "price": "20.09",
    "change": "-1.53",
    "percentChange": "-7.08%"
  },
  {
    "symbol": "AES",
    "name": "The AES Corporation",
    "price": "14.29",
    "change": "-1.08",
    "percentChange": "-7.03%"
  },
  {
    "symbol": "VG",
    "name": "Venture Global, Inc.",
    "price": "13.78",
    "change": "-0.94",
    "percentChange": "-6.39%"
  },
  {
    "symbol": "ERJ",
    "name": "Embraer S.A.",
    "price": "56.78",
    "change": "-3.78",
    "percentChange": "-6.24%"
  },
  {
    "symbol": "PLBL",
    "name": "Polibeli Group Ltd",
    "price": "8.25",
    "change": "-0.55",
    "percentChange": "-6.23%"
  },
  {
    "symbol": "RKT",
    "name": "Rocket Companies, Inc.",
    "price": "18.37",
    "change": "-1.22",
    "percentChange": "-6.23%"
  },
  {
    "symbol": "KGS",
    "name": "Kodiak Gas Services, Inc.",
    "price": "34.54",
    "change": "-2.18",
    "percentChange": "-5.94%"
  },
  {
    "symbol": "FUTU",
    "name": "Futu Holdings Limited",
    "price": "166.25",
    "change": "-10.18",
    "percentChange": "-5.77%"
  },
  {
    "symbol": "CXW",
    "name": "CoreCivic, Inc.",
    "price": "19.48",
    "change": "-1.07",
    "percentChange": "-5.21%"
  },
  {
    "symbol": "TSLA",
    "name": "Tesla, Inc.",
    "price": "436.00",
    "change": "-23.46",
    "percentChange": "-5.11%"
  },
  {
    "symbol": "WFRD",
    "name": "Weatherford International plc",
    "price": "66.29",
    "change": "-3.58",
    "percentChange": "-5.12%"
  },
  {
    "symbol": "CIVI",
    "name": "Civitas Resources, Inc.",
    "price": "33.68",
    "change": "-1.76",
    "percentChange": "-4.97%"
  },
  {
    "symbol": "APA",
    "name": "APA Corporation",
    "price": "23.88",
    "change": "-1.18",
    "percentChange": "-4.71%"
  },
  {
    "symbol": "NG",
    "name": "NovaGold Resources Inc.",
    "price": "9.65",
    "change": "-0.47",
    "percentChange": "-4.64%"
  },
  {
    "symbol": "WHD",
    "name": "Cactus, Inc.",
    "price": "38.22",
    "change": "-1.86",
    "percentChange": "-4.64%"
  },
  {
    "symbol": "ALHC",
    "name": "Alignment Healthcare, Inc.",
    "price": "16.05",
    "change": "-0.77",
    "percentChange": "-4.58%"
  },
  {
    "symbol": "HALO",
    "name": "Halozyme Therapeutics, Inc.",
    "price": "71.69",
    "change": "-3.25",
    "percentChange": "-4.34%"
  },
  {
    "symbol": "AR",
    "name": "Antero Resources Corporation",
    "price": "33.49",
    "change": "-1.49",
    "percentChange": "-4.26%"
  },
  {
    "symbol": "OII",
    "name": "Oceaneering International, Inc.",
    "price": "24.16",
    "change": "-1.06",
    "percentChange": "-4.20%"
  },
  {
    "symbol": "MLCO",
    "name": "Melco Resorts & Entertainment Limited",
    "price": "8.93",
    "change": "-0.39",
    "percentChange": "-4.18%"
  }
]


# Stock NEWS endpoint
https://finance-query.onrender.com/v1/news?symbol=TSLA <-- the stock symbol will
be dynamic, not hardcoded on the package - users will be able to pass
in any stocks they want 

# JSON format the endpoint returns 
[
  {
    "title": "Tesla's $1 Trillion Pay Proposal For Musk Faces Investor Pushback—What We Know",
    "link": "https://www.forbes.com/sites/siladityaray/2025/10/03/teslas-1-trillion-pay-proposal-for-musk-faces-investor-pushback-what-we-know/",
    "source": "Forbes",
    "img": "https://cdn.snapi.dev/images/v1/x/o/0/teslas-1-trillion-pay-proposal-3312599.jpg",
    "time": "40 minutes ago"
  },
  {
    "title": "Why Tesla's record Q3 is a one-time high, and what comes next?",
    "link": "https://invezz.com/news/2025/10/03/why-teslas-record-q3-is-a-one-time-high-and-what-comes-next/?utm_source=snapi",
    "source": "Invezz",
    "img": "https://cdn.snapi.dev/images/v1/0/b/h/2fre3edr-2691589-3312478.jpg",
    "time": "2 hours ago"
  },
  {
    "title": "Tesla Stock Tanked After Decent Deliveries. What to Know.",
    "link": "https://www.barrons.com/articles/tesla-stock-deliveries-musk-pay-9d256496",
    "source": "Barrons",
    "img": "https://cdn.snapi.dev/images/v1/a/p/9/tsla27-2686059-3312390.jpg",
    "time": "3 hours ago"
  },
  {
    "title": "A group of Tesla investors is urging shareholders not to confirm Elon Musk's $1 trillion pay package",
    "link": "https://www.businessinsider.com/tesla-investors-push-back-elon-musks-1-trillion-pay-package-2025-10",
    "source": "Business Insider",
    "img": "https://cdn.snapi.dev/images/v1/r/p/4/2efvd-2642824-3312383.jpg",
    "time": "3 hours ago"
  },
  {
    "title": "Tesla begins selling Cybertrucks in Qatar, company says",
    "link": "https://www.reuters.com/business/autos-transportation/tesla-begins-selling-cybertrucks-qatar-company-says-2025-10-03/",
    "source": "Reuters",
    "img": "https://cdn.snapi.dev/images/v1/8/e/g/tsla13-2688204-3312355.jpg",
    "time": "4 hours ago"
  },
  {
    "title": "Tesla's Comeback: Why Skeptics Like Me Are Becoming Believers (Upgrade)",
    "link": "https://stockanalysis.com/out/news?url=https://seekingalpha.com/article/4827623-tesla-stock-comeback-why-skeptics-like-me-are-becoming-believers-upgrade",
    "source": "Seeking Alpha",
    "img": "https://cdn.snapi.dev/images/v1/e/c/q/fe22e-2480900-3312329.jpg",
    "time": "4 hours ago"
  },
  {
    "title": "Tesla sued by family of California teenager killed in fiery Cybertruck crash",
    "link": "https://www.theguardian.com/us-news/2025/oct/02/tesla-sued-cybertruck-crash-krysta-tsukahara",
    "source": "The Guardian",
    "img": "https://cdn.snapi.dev/images/v1/u/h/d/tsla22-2686600-3312320.jpg",
    "time": "11 hours ago"
  },
  {
    "title": "Elon Musk's $1 trillion pay plan faces pushback from investors, state officials",
    "link": "https://www.reuters.com/business/autos-transportation/elon-musks-1-trillion-pay-plan-faces-pushback-investors-state-officials-2025-10-02/",
    "source": "Reuters",
    "img": "https://cdn.snapi.dev/images/v1/s/3/v/fe22e-2480900-3312211.jpg",
    "time": "14 hours ago"
  },
  {
    "title": "Tesla Is Sued by Families Who Say Faulty Cybertruck Doors Led to Two Deaths",
    "link": "https://www.nytimes.com/2025/10/02/business/tesla-cybertruck-doors-lawsuit-california.html",
    "source": "NYTimes",
    "img": "https://cdn.snapi.dev/images/v1/d/j/l/tsla39-2689556-3312073.jpg",
    "time": "15 hours ago"
  },
  {
    "title": "Tesla Stock Is 'Mooning'—Thank Elon?",
    "link": "https://www.benzinga.com/trading-ideas/movers/25/10/48006761/tesla-stock-is-mooning-thank-elon?utm_source=snapi",
    "source": "Benzinga",
    "img": "https://cdn.snapi.dev/images/v1/z/e/j/tsla38-2682801-3312048.jpg",
    "time": "16 hours ago"
  },
  {
    "title": "Tesla's Sales Surge Is A Sugar High Powered By Less Musk And Trump's EV Tax Credit Cut",
    "link": "https://www.forbes.com/sites/alanohnsman/2025/10/02/teslas-sales-surge-is-a-sugar-high-powered-by-less-musk-and-trumps-ev-tax-credit-cut/",
    "source": "Forbes",
    "img": "https://cdn.snapi.dev/images/v1/9/5/y/teslas-sales-surge-is-a-sugar--3311984.jpg",
    "time": "16 hours ago"
  },
  {
    "title": "Tesla Stock Is Down Today After Upbeat Deliveries News—And a Long Upward Run",
    "link": "https://www.investopedia.com/tesla-stock-is-down-today-after-upbeat-deliveries-news-and-a-long-upward-run-11822133",
    "source": "Investopedia",
    "img": "https://cdn.snapi.dev/images/v1/v/0/z/tsla18-2687093-3311613.jpg",
    "time": "20 hours ago"
  },
  {
    "title": "Tesla shocks Wall Street with nearly 500K deliveries as buyers rushed to lock in tax credit",
    "link": "https://nypost.com/2025/10/02/business/tesla-beats-delivery-estimates-as-ev-buyers-rush-to-secure-expiring-tax-credits/",
    "source": "New York Post",
    "img": "https://cdn.snapi.dev/images/v1/2/t/x/tsla19-2687092-3311524.jpg",
    "time": "21 hours ago"
  },
  {
    "title": "Tesla, Rivals Brace For EV Market 'Collapse'—Thanks To Trump",
    "link": "https://www.benzinga.com/markets/large-cap/25/10/47996067/tesla-rivals-brace-for-ev-market-collapse-thanks-to-trump?utm_source=snapi",
    "source": "Benzinga",
    "img": "https://cdn.snapi.dev/images/v1/v/l/v/f2d-2495697-3311572.jpg",
    "time": "22 hours ago"
  },
  {
    "title": "Tesla reports surprise increase in car sales in the third quarter",
    "link": "https://techxplore.com/news/2025-10-tesla-car-sales-quarter.html",
    "source": "TechXplore",
    "img": "https://cdn.snapi.dev/images/v1/r/y/a/tsla8-2688816-3311376.jpg",
    "time": "22 hours ago"
  }
]


# Symbol search endpoint 
https://finance-query.onrender.com/v1/search?query=TSLA&hits=2&yahoo=true 
<-- Users will be able to specify what symbols they want to searcj for,
but the hits should be hardcoded to 2 & yahoo=true 

# JSON format the endpoint returns 
[
  {
    "name": "Tesla, Inc.",
    "symbol": "TSLA",
    "exchange": "NMS",
    "type": "stock"
  },
  {
    "name": "Direxion Daily TSLA Bull 2X Sha",
    "symbol": "TSLL",
    "exchange": "NGM",
    "type": "etf"
  }
]


# Performace for all sectors endpoint 
https://finance-query.onrender.com/v1/sectors

# JSON format the endpoint returns 
[
  {
    "sector": "Technology",
    "dayReturn": "+0.02%",
    "ytdReturn": "+21.25%",
    "yearReturn": "+30.32%",
    "threeYearReturn": "+149.24%",
    "fiveYearReturn": "+163.99%"
  },
  {
    "sector": "Healthcare",
    "dayReturn": "+0.06%",
    "ytdReturn": "+5.44%",
    "yearReturn": "-3.88%",
    "threeYearReturn": "+13.62%",
    "fiveYearReturn": "+33.34%"
  },
  {
    "sector": "Financial Services",
    "dayReturn": "-0.03%",
    "ytdReturn": "+13.64%",
    "yearReturn": "+21.36%",
    "threeYearReturn": "+73.86%",
    "fiveYearReturn": "+106.44%"
  },
  {
    "sector": "Consumer Cyclical",
    "dayReturn": "+0.07%",
    "ytdReturn": "+6.61%",
    "yearReturn": "+21.08%",
    "threeYearReturn": "+68.59%",
    "fiveYearReturn": "+69.86%"
  },
  {
    "sector": "Industrials",
    "dayReturn": "+0.08%",
    "ytdReturn": "+16.93%",
    "yearReturn": "+15.53%",
    "threeYearReturn": "+66.27%",
    "fiveYearReturn": "+89.41%"
  },
  {
    "sector": "Consumer Defensive",
    "dayReturn": "-0.05%",
    "ytdReturn": "+2.18%",
    "yearReturn": "+1.86%",
    "threeYearReturn": "+27.28%",
    "fiveYearReturn": "+33.11%"
  },
  {
    "sector": "Energy",
    "dayReturn": "-0.01%",
    "ytdReturn": "+4.53%",
    "yearReturn": "-1.66%",
    "threeYearReturn": "+16.46%",
    "fiveYearReturn": "+194.60%"
  },
  {
    "sector": "Real Estate",
    "dayReturn": "-0.59%",
    "ytdReturn": "+4.09%",
    "yearReturn": "-3.21%",
    "threeYearReturn": "+23.06%",
    "fiveYearReturn": "+34.36%"
  },
  {
    "sector": "Utilities",
    "dayReturn": "-0.19%",
    "ytdReturn": "+11.21%",
    "yearReturn": "+4.63%",
    "threeYearReturn": "+33.02%",
    "fiveYearReturn": "+52.61%"
  },
  {
    "sector": "Basic Materials",
    "dayReturn": "+0.69%",
    "ytdReturn": "+28.14%",
    "yearReturn": "+14.29%",
    "threeYearReturn": "+55.38%",
    "fiveYearReturn": "+72.28%"
  },
  {
    "sector": "Communication Services",
    "dayReturn": "+0.03%",
    "ytdReturn": "+26.45%",
    "yearReturn": "+36.30%",
    "threeYearReturn": "+128.38%",
    "fiveYearReturn": "+93.29%"
  }
]


# Performance of a stock sector endpoint
https://finance-query.onrender.com/v1/sectors/symbol/{symbol} <-- users will
specify what symbols they want 

# JSON format the endpoint returns 
{
  "sector": "Consumer Cyclical",
  "dayReturn": "+0.07%",
  "ytdReturn": "+6.61%",
  "yearReturn": "+21.08%",
  "threeYearReturn": "+68.59%",
  "fiveYearReturn": "+69.86%"
}







































