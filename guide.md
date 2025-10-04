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


# Income stateme endpoint 
https://finance-query.onrender.com/v1/financials/AAPL?statement=income&frequency=annual <-- users will specify what frequency they want - 'quarterly' or 'annual' for any stock

# JSON format the endpoint returns 
{
  "symbol":"AAPL",
  "statement_type":"income",
  "frequency":"quarterly",
  "statement":{"0":
  {"Breakdown":"Total Revenue","TTM":"408625000000.0","2025-06-30":"94036000000.0","2025-03-31":"95359000000.0","2024-12-31":"124300000000.0","2024-09-30":"94930000000.0","2024-06-30":"85777000000.0","2024-03-31":"90753000000.0","2023-12-31":"119575000000.0","2023-09-30":"89498000000.0","2023-06-30":"81797000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"82959000000.0"},"1":{"Breakdown":"Operating Revenue","TTM":"408625000000.0","2025-06-30":"94036000000.0","2025-03-31":"95359000000.0","2024-12-31":"124300000000.0","2024-09-30":"94930000000.0","2024-06-30":"85777000000.0","2024-03-31":"90753000000.0","2023-12-31":"119575000000.0","2023-09-30":"89498000000.0","2023-06-30":"81797000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"82959000000.0"},"2":{"Breakdown":"Cost of Revenue","TTM":"217886000000.0","2025-06-30":"50318000000.0","2025-03-31":"50492000000.0","2024-12-31":"66025000000.0","2024-09-30":"51051000000.0","2024-06-30":"46099000000.0","2024-03-31":"48482000000.0","2023-12-31":"64720000000.0","2023-09-30":"49071000000.0","2023-06-30":"45384000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"47074000000.0"},"3":{"Breakdown":"Gross Profit","TTM":"190739000000.0","2025-06-30":"43718000000.0","2025-03-31":"44867000000.0","2024-12-31":"58275000000.0","2024-09-30":"43879000000.0","2024-06-30":"39678000000.0","2024-03-31":"42271000000.0","2023-12-31":"54855000000.0","2023-09-30":"40427000000.0","2023-06-30":"36413000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"35885000000.0"},"4":{"Breakdown":"Operating Expense","TTM":"60525000000.0","2025-06-30":"15516000000.0","2025-03-31":"15278000000.0","2024-12-31":"15443000000.0","2024-09-30":"14288000000.0","2024-06-30":"14326000000.0","2024-03-31":"14371000000.0","2023-12-31":"14482000000.0","2023-09-30":"13458000000.0","2023-06-30":"13415000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"12809000000.0"},"5":{"Breakdown":"Selling General and Administrative","TTM":"27076000000.0","2025-06-30":"6650000000.0","2025-03-31":"6728000000.0","2024-12-31":"7175000000.0","2024-09-30":"6523000000.0","2024-06-30":"6320000000.0","2024-03-31":"6468000000.0","2023-12-31":"6786000000.0","2023-09-30":"6151000000.0","2023-06-30":"5973000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"6012000000.0"},"6":{"Breakdown":"Research & Development","TTM":"33449000000.0","2025-06-30":"8866000000.0","2025-03-31":"8550000000.0","2024-12-31":"8268000000.0","2024-09-30":"7765000000.0","2024-06-30":"8006000000.0","2024-03-31":"7903000000.0","2023-12-31":"7696000000.0","2023-09-30":"7307000000.0","2023-06-30":"7442000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"6797000000.0"},"7":{"Breakdown":"Operating Income","TTM":"130214000000.0","2025-06-30":"28202000000.0","2025-03-31":"29589000000.0","2024-12-31":"42832000000.0","2024-09-30":"29591000000.0","2024-06-30":"25352000000.0","2024-03-31":"27900000000.0","2023-12-31":"40373000000.0","2023-09-30":"26969000000.0","2023-06-30":"22998000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"23076000000.0"},"8":{"Breakdown":"Net Non-Operating Interest Income Expense","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"-18000000.0","2023-06-30":"-18000000.0","2023-03-31":"-12000000.0","2022-12-31":"-135000000.0","2022-09-30":"-74000000.0","2022-06-30":"3000000.0"},"9":{"Breakdown":"Non-Operating Interest Income","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"984000000.0","2023-06-30":"980000000.0","2023-03-31":"918000000.0","2022-12-31":"868000000.0","2022-09-30":"753000000.0","2022-06-30":"722000000.0"},"10":{"Breakdown":"Non-Operating Interest Expense","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"1002000000.0","2023-06-30":"998000000.0","2023-03-31":"930000000.0","2022-12-31":"1003000000.0","2022-09-30":"827000000.0","2022-06-30":"719000000.0"},"11":{"Breakdown":"Other Income Expense","TTM":"-679000000.0","2025-06-30":"-171000000.0","2025-03-31":"-279000000.0","2024-12-31":"-248000000.0","2024-09-30":"19000000.0","2024-06-30":"142000000.0","2024-03-31":"158000000.0","2023-12-31":"-50000000.0","2023-09-30":"47000000.0","2023-06-30":"-265000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"-10000000.0"},"12":{"Breakdown":"Other Non Operating Income Expenses","TTM":"-679000000.0","2025-06-30":"-171000000.0","2025-03-31":"-279000000.0","2024-12-31":"-248000000.0","2024-09-30":"19000000.0","2024-06-30":"142000000.0","2024-03-31":"158000000.0","2023-12-31":"-50000000.0","2023-09-30":"47000000.0","2023-06-30":"-265000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"-10000000.0"},"13":{"Breakdown":"Pretax Income","TTM":"129535000000.0","2025-06-30":"28031000000.0","2025-03-31":"29310000000.0","2024-12-31":"42584000000.0","2024-09-30":"29610000000.0","2024-06-30":"25494000000.0","2024-03-31":"28058000000.0","2023-12-31":"40323000000.0","2023-09-30":"26998000000.0","2023-06-30":"22733000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"23066000000.0"},"14":{"Breakdown":"Tax Provision","TTM":"30255000000.0","2025-06-30":"4597000000.0","2025-03-31":"4530000000.0","2024-12-31":"6254000000.0","2024-09-30":"14874000000.0","2024-06-30":"4046000000.0","2024-03-31":"4422000000.0","2023-12-31":"6407000000.0","2023-09-30":"4042000000.0","2023-06-30":"2852000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"3624000000.0"},"15":{"Breakdown":"Net Income Common Stockholders","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"16":{"Breakdown":"Net Income(Attributable to Parent Company Shareholders)","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"17":{"Breakdown":"Net Income Including Non-Controlling Interests","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"18":{"Breakdown":"Net Income Continuous Operations","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"19":{"Breakdown":"Diluted NI Available to Com Stockholders","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"20":{"Breakdown":"Basic EPS","TTM":"6.16","2025-06-30":"1.57","2025-03-31":"1.65","2024-12-31":"2.41","2024-09-30":"0.97","2024-06-30":"1.4","2024-03-31":"1.53","2023-12-31":"2.19","2023-09-30":"1.47","2023-06-30":"1.27","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"1.2"},"21":{"Breakdown":"Diluted EPS","TTM":"6.13","2025-06-30":"1.57","2025-03-31":"1.65","2024-12-31":"2.4","2024-09-30":"0.97","2024-06-30":"1.4","2024-03-31":"1.53","2023-12-31":"2.18","2023-09-30":"1.46","2023-06-30":"1.26","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"1.2"},"22":{"Breakdown":"Basic Average Shares","TTM":"15744231000.0","2025-06-30":"14902886000.0","2025-03-31":"14994082000.0","2024-12-31":"15081724000.0","2024-09-30":"15171990000.0","2024-06-30":"15287521000.0","2024-03-31":"15405856000.0","2023-12-31":"15509763000.0","2023-09-30":"15599434000.0","2023-06-30":"15697614000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"16162945000.0"},"23":{"Breakdown":"Diluted Average Shares","TTM":"15812547000.0","2025-06-30":"14948179000.0","2025-03-31":"15056133000.0","2024-12-31":"15150865000.0","2024-09-30":"15242853000.0","2024-06-30":"15348175000.0","2024-03-31":"15464709000.0","2023-12-31":"15576641000.0","2023-09-30":"15672400000.0","2023-06-30":"15775021000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"16262203000.0"},"24":{"Breakdown":"Total Operating Income as Reported","TTM":"130214000000.0","2025-06-30":"28202000000.0","2025-03-31":"29589000000.0","2024-12-31":"42832000000.0","2024-09-30":"29591000000.0","2024-06-30":"25352000000.0","2024-03-31":"27900000000.0","2023-12-31":"40373000000.0","2023-09-30":"26969000000.0","2023-06-30":"22998000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"23076000000.0"},"25":{"Breakdown":"Total Expenses","TTM":"278411000000.0","2025-06-30":"65834000000.0","2025-03-31":"65770000000.0","2024-12-31":"81468000000.0","2024-09-30":"65339000000.0","2024-06-30":"60425000000.0","2024-03-31":"62853000000.0","2023-12-31":"79202000000.0","2023-09-30":"62529000000.0","2023-06-30":"58799000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"59883000000.0"},"26":{"Breakdown":"Net Income from Continuing & Discontinued Operation","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"27":{"Breakdown":"Normalized Income","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"28":{"Breakdown":"Interest Income","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"984000000.0","2023-06-30":"980000000.0","2023-03-31":"918000000.0","2022-12-31":"868000000.0","2022-09-30":"753000000.0","2022-06-30":"722000000.0"},"29":{"Breakdown":"Interest Expense","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"1002000000.0","2023-06-30":"998000000.0","2023-03-31":"930000000.0","2022-12-31":"1003000000.0","2022-09-30":"827000000.0","2022-06-30":"719000000.0"},"30":{"Breakdown":"Net Interest Income","TTM":"*","2025-06-30":"*","2025-03-31":"*","2024-12-31":"*","2024-09-30":"*","2024-06-30":"*","2024-03-31":"*","2023-12-31":"*","2023-09-30":"-18000000.0","2023-06-30":"-18000000.0","2023-03-31":"-12000000.0","2022-12-31":"-135000000.0","2022-09-30":"-74000000.0","2022-06-30":"3000000.0"},"31":{"Breakdown":"EBIT","TTM":"130214000000.0","2025-06-30":"28202000000.0","2025-03-31":"29589000000.0","2024-12-31":"42832000000.0","2024-09-30":"29591000000.0","2024-06-30":"25352000000.0","2024-03-31":"27900000000.0","2023-12-31":"40373000000.0","2023-09-30":"28000000000.0","2023-06-30":"22998000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"23076000000.0"},"32":{"Breakdown":"EBITDA","TTM":"141696000000.0","2025-06-30":"31032000000.0","2025-03-31":"32250000000.0","2024-12-31":"45912000000.0","2024-09-30":"32502000000.0","2024-06-30":"28202000000.0","2024-03-31":"30736000000.0","2023-12-31":"43221000000.0","2023-09-30":"30653000000.0","2023-06-30":"26050000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"*"},"33":{"Breakdown":"Reconciled Cost of Revenue","TTM":"217886000000.0","2025-06-30":"50318000000.0","2025-03-31":"50492000000.0","2024-12-31":"66025000000.0","2024-09-30":"51051000000.0","2024-06-30":"46099000000.0","2024-03-31":"48482000000.0","2023-12-31":"64720000000.0","2023-09-30":"49071000000.0","2023-06-30":"45384000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"47074000000.0"},"34":{"Breakdown":"Reconciled Depreciation","TTM":"11482000000.0","2025-06-30":"2830000000.0","2025-03-31":"2661000000.0","2024-12-31":"3080000000.0","2024-09-30":"2911000000.0","2024-06-30":"2850000000.0","2024-03-31":"2836000000.0","2023-12-31":"2848000000.0","2023-09-30":"2653000000.0","2023-06-30":"3052000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"2805000000.0"},"35":{"Breakdown":"Net Income from Continuing Operation Net Minority Interest","TTM":"99280000000.0","2025-06-30":"23434000000.0","2025-03-31":"24780000000.0","2024-12-31":"36330000000.0","2024-09-30":"14736000000.0","2024-06-30":"21448000000.0","2024-03-31":"23636000000.0","2023-12-31":"33916000000.0","2023-09-30":"22956000000.0","2023-06-30":"19881000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"19442000000.0"},"36":{"Breakdown":"Normalized EBITDA","TTM":"141696000000.0","2025-06-30":"31032000000.0","2025-03-31":"32250000000.0","2024-12-31":"45912000000.0","2024-09-30":"32502000000.0","2024-06-30":"28202000000.0","2024-03-31":"30736000000.0","2023-12-31":"43221000000.0","2023-09-30":"30653000000.0","2023-06-30":"26050000000.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"25881000000.0"},"37":{"Breakdown":"Tax Rate for Calcs","TTM":"0.23","2025-06-30":"0.16","2025-03-31":"0.16","2024-12-31":"0.15","2024-09-30":"0.21","2024-06-30":"0.16","2024-03-31":"0.16","2023-12-31":"0.21","2023-09-30":"0.15","2023-06-30":"0.13","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"0.16"},"38":{"Breakdown":"Tax Effect of Unusual Items","TTM":"0.0","2025-06-30":"0.0","2025-03-31":"0.0","2024-12-31":"0.0","2024-09-30":"0.0","2024-06-30":"0.0","2024-03-31":"0.0","2023-12-31":"0.0","2023-09-30":"0.0","2023-06-30":"0.0","2023-03-31":"*","2022-12-31":"*","2022-09-30":"*","2022-06-30":"0.0"}}}


# Balance sheet endpoint 
https://finance-query.onrender.com/v1/financials/AAPL?statement=income&frequency=annual <--
users will specify what frequency they want - 'quarterly' or 'annual' for any stock 

# JSON format the endpoint returns 
{
  "symbol":"AAPL",
"statement_type":"balance",
"frequency":"annual",
"statement":{"0":{"Breakdown":"Total Assets","2024-09-30":"364980000000.0","2023-09-30":"352583000000.0","2022-09-30":"352755000000.0","2021-09-30":"351002000000.0","2020-09-30":"323888000000.0","2019-09-30":"*"},"1":{"Breakdown":"Total Current Assets","2024-09-30":"152987000000.0","2023-09-30":"143566000000.0","2022-09-30":"135405000000.0","2021-09-30":"134836000000.0","2020-09-30":"143713000000.0","2019-09-30":"*"},"2":{"Breakdown":"Cash, Cash Equivalents & Short Term Investments","2024-09-30":"65171000000.0","2023-09-30":"61555000000.0","2022-09-30":"48304000000.0","2021-09-30":"62639000000.0","2020-09-30":"90943000000.0","2019-09-30":"*"},"3":{"Breakdown":"Cash And Cash Equivalents","2024-09-30":"29943000000.0","2023-09-30":"29965000000.0","2022-09-30":"23646000000.0","2021-09-30":"34940000000.0","2020-09-30":"38016000000.0","2019-09-30":"*"},"4":{"Breakdown":"Cash","2024-09-30":"27199000000.0","2023-09-30":"28359000000.0","2022-09-30":"18546000000.0","2021-09-30":"17305000000.0","2020-09-30":"17773000000.0","2019-09-30":"*"},"5":{"Breakdown":"Cash Equivalents","2024-09-30":"2744000000.0","2023-09-30":"1606000000.0","2022-09-30":"5100000000.0","2021-09-30":"17635000000.0","2020-09-30":"20243000000.0","2019-09-30":"*"},"6":{"Breakdown":"Other Short Term Investments","2024-09-30":"35228000000.0","2023-09-30":"31590000000.0","2022-09-30":"24658000000.0","2021-09-30":"27699000000.0","2020-09-30":"52927000000.0","2019-09-30":"*"},"7":{"Breakdown":"Receivables","2024-09-30":"66243000000.0","2023-09-30":"60985000000.0","2022-09-30":"60932000000.0","2021-09-30":"51506000000.0","2020-09-30":"37445000000.0","2019-09-30":"*"},"8":{"Breakdown":"Accounts receivable","2024-09-30":"33410000000.0","2023-09-30":"29508000000.0","2022-09-30":"28184000000.0","2021-09-30":"26278000000.0","2020-09-30":"16120000000.0","2019-09-30":"*"},"9":{"Breakdown":"Other Receivables","2024-09-30":"32833000000.0","2023-09-30":"31477000000.0","2022-09-30":"32748000000.0","2021-09-30":"25228000000.0","2020-09-30":"21325000000.0","2019-09-30":"*"},"10":{"Breakdown":"Inventory","2024-09-30":"7286000000.0","2023-09-30":"6331000000.0","2022-09-30":"4946000000.0","2021-09-30":"6580000000.0","2020-09-30":"4061000000.0","2019-09-30":"*"},"11":{"Breakdown":"Other Current Assets","2024-09-30":"14287000000.0","2023-09-30":"14695000000.0","2022-09-30":"21223000000.0","2021-09-30":"14111000000.0","2020-09-30":"11264000000.0","2019-09-30":"*"},"12":{"Breakdown":"Total non-current assets","2024-09-30":"211993000000.0","2023-09-30":"209017000000.0","2022-09-30":"217350000000.0","2021-09-30":"216166000000.0","2020-09-30":"180175000000.0","2019-09-30":"*"},"13":{"Breakdown":"Net PPE","2024-09-30":"45680000000.0","2023-09-30":"43715000000.0","2022-09-30":"42117000000.0","2021-09-30":"49527000000.0","2020-09-30":"45336000000.0","2019-09-30":"*"},"14":{"Breakdown":"Gross PPE","2024-09-30":"119128000000.0","2023-09-30":"114599000000.0","2022-09-30":"114457000000.0","2021-09-30":"119810000000.0","2020-09-30":"112096000000.0","2019-09-30":"*"},"15":{"Breakdown":"Properties","2024-09-30":"0.0","2023-09-30":"0.0","2022-09-30":"0.0","2021-09-30":"0.0","2020-09-30":"0.0","2019-09-30":"*"},"16":{"Breakdown":"Land And Improvements","2024-09-30":"24690000000.0","2023-09-30":"23446000000.0","2022-09-30":"22126000000.0","2021-09-30":"20041000000.0","2020-09-30":"17952000000.0","2019-09-30":"*"},"17":{"Breakdown":"Machinery Furniture Equipment","2024-09-30":"80205000000.0","2023-09-30":"78314000000.0","2022-09-30":"81060000000.0","2021-09-30":"78659000000.0","2020-09-30":"75291000000.0","2019-09-30":"*"},"18":{"Breakdown":"Other Properties","2024-09-30":"*","2023-09-30":"10661000000.0","2022-09-30":"10417000000.0","2021-09-30":"10087000000.0","2020-09-30":"8570000000.0","2019-09-30":"*"},"19":{"Breakdown":"Leases","2024-09-30":"14233000000.0","2023-09-30":"12839000000.0","2022-09-30":"11271000000.0","2021-09-30":"11023000000.0","2020-09-30":"10283000000.0","2019-09-30":"*"},"20":{"Breakdown":"Accumulated Depreciation","2024-09-30":"-73448000000.0","2023-09-30":"-70884000000.0","2022-09-30":"-72340000000.0","2021-09-30":"-70283000000.0","2020-09-30":"-66760000000.0","2019-09-30":"*"},"21":{"Breakdown":"Investments And Advances","2024-09-30":"91479000000.0","2023-09-30":"100544000000.0","2022-09-30":"120805000000.0","2021-09-30":"127877000000.0","2020-09-30":"100887000000.0","2019-09-30":"*"},"22":{"Breakdown":"Investment in Financial Assets","2024-09-30":"91479000000.0","2023-09-30":"100544000000.0","2022-09-30":"120805000000.0","2021-09-30":"127877000000.0","2020-09-30":"100887000000.0","2019-09-30":"*"},"23":{"Breakdown":"Available for Sale Securities","2024-09-30":"91479000000.0","2023-09-30":"100544000000.0","2022-09-30":"120805000000.0","2021-09-30":"127877000000.0","2020-09-30":"100887000000.0","2019-09-30":"*"},"24":{"Breakdown":"Other Investments","2024-09-30":"*","2023-09-30":"*","2022-09-30":"120805000000.0","2021-09-30":"127877000000.0","2020-09-30":"100887000000.0","2019-09-30":"105341000000.0"},"25":{"Breakdown":"Non Current Deferred Assets","2024-09-30":"19499000000.0","2023-09-30":"17852000000.0","2022-09-30":"15375000000.0","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"},"26":{"Breakdown":"Non Current Deferred Taxes Assets","2024-09-30":"19499000000.0","2023-09-30":"17852000000.0","2022-09-30":"15375000000.0","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"},"27":{"Breakdown":"Other Non Current Assets","2024-09-30":"55335000000.0","2023-09-30":"46906000000.0","2022-09-30":"39053000000.0","2021-09-30":"38762000000.0","2020-09-30":"33952000000.0","2019-09-30":"*"},"28":{"Breakdown":"Total Liabilities","2024-09-30":"308030000000.0","2023-09-30":"290437000000.0","2022-09-30":"302083000000.0","2021-09-30":"287912000000.0","2020-09-30":"258549000000.0","2019-09-30":"*"},"29":{"Breakdown":"Total Current Liabilities","2024-09-30":"176392000000.0","2023-09-30":"145308000000.0","2022-09-30":"153982000000.0","2021-09-30":"125481000000.0","2020-09-30":"105392000000.0","2019-09-30":"*"},"30":{"Breakdown":"Payables And Accrued Expenses","2024-09-30":"95561000000.0","2023-09-30":"71430000000.0","2022-09-30":"70667000000.0","2021-09-30":"54763000000.0","2020-09-30":"42296000000.0","2019-09-30":"*"},"31":{"Breakdown":"Payables","2024-09-30":"95561000000.0","2023-09-30":"71430000000.0","2022-09-30":"70667000000.0","2021-09-30":"54763000000.0","2020-09-30":"42296000000.0","2019-09-30":"*"},"32":{"Breakdown":"Accounts Payable","2024-09-30":"68960000000.0","2023-09-30":"62611000000.0","2022-09-30":"64115000000.0","2021-09-30":"54763000000.0","2020-09-30":"42296000000.0","2019-09-30":"*"},"33":{"Breakdown":"Total Tax Payable","2024-09-30":"26601000000.0","2023-09-30":"8819000000.0","2022-09-30":"6552000000.0","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"},"34":{"Breakdown":"Income Tax Payable","2024-09-30":"26601000000.0","2023-09-30":"8819000000.0","2022-09-30":"6552000000.0","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"},"35":{"Breakdown":"Current Debt And Capital Lease Obligation","2024-09-30":"20879000000.0","2023-09-30":"15807000000.0","2022-09-30":"22773000000.0","2021-09-30":"17141000000.0","2020-09-30":"15229000000.0","2019-09-30":"*"},"36":{"Breakdown":"Current Debt","2024-09-30":"20879000000.0","2023-09-30":"15807000000.0","2022-09-30":"21110000000.0","2021-09-30":"15613000000.0","2020-09-30":"13769000000.0","2019-09-30":"*"},"37":{"Breakdown":"Commercial Paper","2024-09-30":"9967000000.0","2023-09-30":"5985000000.0","2022-09-30":"9982000000.0","2021-09-30":"6000000000.0","2020-09-30":"4996000000.0","2019-09-30":"*"},"38":{"Breakdown":"Other Current Borrowings","2024-09-30":"10912000000.0","2023-09-30":"9822000000.0","2022-09-30":"11128000000.0","2021-09-30":"9613000000.0","2020-09-30":"8773000000.0","2019-09-30":"*"},"39":{"Breakdown":"Current Capital Lease Obligation","2024-09-30":"*","2023-09-30":"1575000000.0","2022-09-30":"1663000000.0","2021-09-30":"1528000000.0","2020-09-30":"1460000000.0","2019-09-30":"*"},"40":{"Breakdown":"Current Deferred Liabilities","2024-09-30":"8249000000.0","2023-09-30":"8061000000.0","2022-09-30":"7912000000.0","2021-09-30":"7612000000.0","2020-09-30":"6643000000.0","2019-09-30":"*"},"41":{"Breakdown":"Current Deferred Revenue","2024-09-30":"8249000000.0","2023-09-30":"8061000000.0","2022-09-30":"7912000000.0","2021-09-30":"7612000000.0","2020-09-30":"6643000000.0","2019-09-30":"*"},"42":{"Breakdown":"Other Current Liabilities","2024-09-30":"51703000000.0","2023-09-30":"50010000000.0","2022-09-30":"52630000000.0","2021-09-30":"45965000000.0","2020-09-30":"41224000000.0","2019-09-30":"*"},"43":{"Breakdown":"Total Non Current Liabilities","2024-09-30":"131638000000.0","2023-09-30":"145129000000.0","2022-09-30":"148101000000.0","2021-09-30":"162431000000.0","2020-09-30":"153157000000.0","2019-09-30":"*"},"44":{"Breakdown":"Long Term Debt And Capital Lease Obligation","2024-09-30":"85750000000.0","2023-09-30":"95281000000.0","2022-09-30":"109707000000.0","2021-09-30":"119381000000.0","2020-09-30":"107049000000.0","2019-09-30":"*"},"45":{"Breakdown":"Long Term Debt","2024-09-30":"85750000000.0","2023-09-30":"95281000000.0","2022-09-30":"98959000000.0","2021-09-30":"109106000000.0","2020-09-30":"98667000000.0","2019-09-30":"*"},"46":{"Breakdown":"Long Term Capital Lease Obligation","2024-09-30":"*","2023-09-30":"11267000000.0","2022-09-30":"10748000000.0","2021-09-30":"10275000000.0","2020-09-30":"8382000000.0","2019-09-30":"*"},"47":{"Breakdown":"Trade and Other Payables Non Current","2024-09-30":"9254000000.0","2023-09-30":"15457000000.0","2022-09-30":"16657000000.0","2021-09-30":"24689000000.0","2020-09-30":"28170000000.0","2019-09-30":"*"},"48":{"Breakdown":"Other Non Current Liabilities","2024-09-30":"36634000000.0","2023-09-30":"34391000000.0","2022-09-30":"21737000000.0","2021-09-30":"18361000000.0","2020-09-30":"17938000000.0","2019-09-30":"*"},"49":{"Breakdown":"Total Equity","2024-09-30":"56950000000.0","2023-09-30":"62146000000.0","2022-09-30":"50672000000.0","2021-09-30":"63090000000.0","2020-09-30":"65339000000.0","2019-09-30":"*"},"50":{"Breakdown":"Stockholders' Equity","2024-09-30":"56950000000.0","2023-09-30":"62146000000.0","2022-09-30":"50672000000.0","2021-09-30":"63090000000.0","2020-09-30":"65339000000.0","2019-09-30":"*"},"51":{"Breakdown":"Capital Stock","2024-09-30":"83276000000.0","2023-09-30":"73812000000.0","2022-09-30":"64849000000.0","2021-09-30":"57365000000.0","2020-09-30":"50779000000.0","2019-09-30":"*"},"52":{"Breakdown":"Common Stock","2024-09-30":"83276000000.0","2023-09-30":"73812000000.0","2022-09-30":"64849000000.0","2021-09-30":"57365000000.0","2020-09-30":"50779000000.0","2019-09-30":"*"},"53":{"Breakdown":"Retained Earnings","2024-09-30":"-19154000000.0","2023-09-30":"-214000000.0","2022-09-30":"-3068000000.0","2021-09-30":"5562000000.0","2020-09-30":"14966000000.0","2019-09-30":"*"},"54":{"Breakdown":"Gains Losses Not Affecting Retained Earnings","2024-09-30":"-7172000000.0","2023-09-30":"-11452000000.0","2022-09-30":"-11109000000.0","2021-09-30":"163000000.0","2020-09-30":"-406000000.0","2019-09-30":"*"},"55":{"Breakdown":"Other Equity Adjustments","2024-09-30":"-7172000000.0","2023-09-30":"-11452000000.0","2022-09-30":"-11109000000.0","2021-09-30":"163000000.0","2020-09-30":"-406000000.0","2019-09-30":"*"},"56":{"Breakdown":"Total Capitalization","2024-09-30":"142700000000.0","2023-09-30":"157427000000.0","2022-09-30":"149631000000.0","2021-09-30":"172196000000.0","2020-09-30":"164006000000.0","2019-09-30":"*"},"57":{"Breakdown":"Common Stock Equity","2024-09-30":"56950000000.0","2023-09-30":"62146000000.0","2022-09-30":"50672000000.0","2021-09-30":"63090000000.0","2020-09-30":"65339000000.0","2019-09-30":"*"},"58":{"Breakdown":"Capital Lease Obligations","2024-09-30":"*","2023-09-30":"12842000000.0","2022-09-30":"12411000000.0","2021-09-30":"11803000000.0","2020-09-30":"9842000000.0","2019-09-30":"*"},"59":{"Breakdown":"Net Tangible Assets","2024-09-30":"56950000000.0","2023-09-30":"62146000000.0","2022-09-30":"50672000000.0","2021-09-30":"63090000000.0","2020-09-30":"65339000000.0","2019-09-30":"*"},"60":{"Breakdown":"Working Capital","2024-09-30":"-23405000000.0","2023-09-30":"-1742000000.0","2022-09-30":"-18577000000.0","2021-09-30":"9355000000.0","2020-09-30":"38321000000.0","2019-09-30":"*"},"61":{"Breakdown":"Invested Capital","2024-09-30":"163579000000.0","2023-09-30":"173234000000.0","2022-09-30":"170741000000.0","2021-09-30":"187809000000.0","2020-09-30":"177775000000.0","2019-09-30":"*"},"62":{"Breakdown":"Tangible Book Value","2024-09-30":"56950000000.0","2023-09-30":"62146000000.0","2022-09-30":"50672000000.0","2021-09-30":"63090000000.0","2020-09-30":"65339000000.0","2019-09-30":"*"},"63":{"Breakdown":"Total Debt","2024-09-30":"106629000000.0","2023-09-30":"111088000000.0","2022-09-30":"132480000000.0","2021-09-30":"136522000000.0","2020-09-30":"122278000000.0","2019-09-30":"*"},"64":{"Breakdown":"Net Debt","2024-09-30":"76686000000.0","2023-09-30":"81123000000.0","2022-09-30":"96423000000.0","2021-09-30":"89779000000.0","2020-09-30":"74420000000.0","2019-09-30":"*"},"65":{"Breakdown":"Share Issued","2024-09-30":"15116786000.0","2023-09-30":"15550061000.0","2022-09-30":"15943425000.0","2021-09-30":"16426786000.0","2020-09-30":"16976763000.0","2019-09-30":"*"},"66":{"Breakdown":"Ordinary Shares Number","2024-09-30":"15116786000.0","2023-09-30":"15550061000.0","2022-09-30":"15943425000.0","2021-09-30":"16426786000.0","2020-09-30":"16976763000.0","2019-09-30":"*"},"67":{"Breakdown":"Treasury Shares Number","2024-09-30":"*","2023-09-30":"0.0","2022-09-30":"*","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"}}}


# Cash flow endpoint 
https://finance-query.onrender.com/v1/financials/AAPL?statement=cashflow&frequency=annual
users will specify what frequency they want - 'quarterly' or 'annual' for any stock 

# JSON format the endpoint returns 
{
  "symbol":"AAPL",
  "statement_type":"cashflow",
  "frequency":"annual",
  "statement":{"0":{"Breakdown":"Operating Cash Flow","2024-09-30":"118254000000.0","2023-09-30":"110543000000.0","2022-09-30":"122151000000.0","2021-09-30":"104038000000.0","2020-09-30":"80674000000.0","2019-09-30":"*"},"1":{"Breakdown":"Cash Flow from Continuing Operating Activities","2024-09-30":"118254000000.0","2023-09-30":"110543000000.0","2022-09-30":"122151000000.0","2021-09-30":"104038000000.0","2020-09-30":"80674000000.0","2019-09-30":"*"},"2":{"Breakdown":"Net Income from Continuing Operations","2024-09-30":"93736000000.0","2023-09-30":"96995000000.0","2022-09-30":"99803000000.0","2021-09-30":"94680000000.0","2020-09-30":"57411000000.0","2019-09-30":"*"},"3":{"Breakdown":"Depreciation Amortization Depletion","2024-09-30":"11445000000.0","2023-09-30":"11519000000.0","2022-09-30":"11104000000.0","2021-09-30":"11284000000.0","2020-09-30":"11056000000.0","2019-09-30":"*"},"4":{"Breakdown":"Depreciation & Amortization","2024-09-30":"11445000000.0","2023-09-30":"11519000000.0","2022-09-30":"11104000000.0","2021-09-30":"11284000000.0","2020-09-30":"11056000000.0","2019-09-30":"*"},"5":{"Breakdown":"Deferred Tax","2024-09-30":"*","2023-09-30":"*","2022-09-30":"895000000.0","2021-09-30":"-4774000000.0","2020-09-30":"-215000000.0","2019-09-30":"-340000000.0"},"6":{"Breakdown":"Deferred Income Tax","2024-09-30":"*","2023-09-30":"*","2022-09-30":"895000000.0","2021-09-30":"-4774000000.0","2020-09-30":"-215000000.0","2019-09-30":"-340000000.0"},"7":{"Breakdown":"Other Non-Cash Items","2024-09-30":"-2266000000.0","2023-09-30":"-2227000000.0","2022-09-30":"1006000000.0","2021-09-30":"-4921000000.0","2020-09-30":"-97000000.0","2019-09-30":"*"},"8":{"Breakdown":"Stock Based Compensation","2024-09-30":"11688000000.0","2023-09-30":"10833000000.0","2022-09-30":"9038000000.0","2021-09-30":"7906000000.0","2020-09-30":"6829000000.0","2019-09-30":"*"},"9":{"Breakdown":"Change In Working Capital","2024-09-30":"3651000000.0","2023-09-30":"-6577000000.0","2022-09-30":"1200000000.0","2021-09-30":"-4911000000.0","2020-09-30":"5690000000.0","2019-09-30":"*"},"10":{"Breakdown":"Change in Receivables","2024-09-30":"-5144000000.0","2023-09-30":"-417000000.0","2022-09-30":"-9343000000.0","2021-09-30":"-14028000000.0","2020-09-30":"8470000000.0","2019-09-30":"*"},"11":{"Breakdown":"Changes in Account Receivables","2024-09-30":"-3788000000.0","2023-09-30":"-1688000000.0","2022-09-30":"-1823000000.0","2021-09-30":"-10125000000.0","2020-09-30":"6917000000.0","2019-09-30":"*"},"12":{"Breakdown":"Change in Inventory","2024-09-30":"-1046000000.0","2023-09-30":"-1618000000.0","2022-09-30":"1484000000.0","2021-09-30":"-2642000000.0","2020-09-30":"-127000000.0","2019-09-30":"*"},"13":{"Breakdown":"Change in Payables And Accrued Expense","2024-09-30":"6020000000.0","2023-09-30":"-1889000000.0","2022-09-30":"9448000000.0","2021-09-30":"12326000000.0","2020-09-30":"-4062000000.0","2019-09-30":"*"},"14":{"Breakdown":"Change in Payable","2024-09-30":"6020000000.0","2023-09-30":"-1889000000.0","2022-09-30":"9448000000.0","2021-09-30":"12326000000.0","2020-09-30":"-4062000000.0","2019-09-30":"*"},"15":{"Breakdown":"Change in Account Payable","2024-09-30":"6020000000.0","2023-09-30":"-1889000000.0","2022-09-30":"9448000000.0","2021-09-30":"12326000000.0","2020-09-30":"-4062000000.0","2019-09-30":"*"},"16":{"Breakdown":"Change in Other Current Assets","2024-09-30":"-11731000000.0","2023-09-30":"-5684000000.0","2022-09-30":"-6499000000.0","2021-09-30":"-8042000000.0","2020-09-30":"-9588000000.0","2019-09-30":"*"},"17":{"Breakdown":"Change in Other Current Liabilities","2024-09-30":"15552000000.0","2023-09-30":"3031000000.0","2022-09-30":"6110000000.0","2021-09-30":"7475000000.0","2020-09-30":"8916000000.0","2019-09-30":"*"},"18":{"Breakdown":"Change in Other Working Capital","2024-09-30":"*","2023-09-30":"*","2022-09-30":"478000000.0","2021-09-30":"1676000000.0","2020-09-30":"2081000000.0","2019-09-30":"-625000000.0"},"19":{"Breakdown":"Investing Cash Flow","2024-09-30":"2935000000.0","2023-09-30":"3705000000.0","2022-09-30":"-22354000000.0","2021-09-30":"-14545000000.0","2020-09-30":"-4289000000.0","2019-09-30":"*"},"20":{"Breakdown":"Cash Flow from Continuing Investing Activities","2024-09-30":"2935000000.0","2023-09-30":"3705000000.0","2022-09-30":"-22354000000.0","2021-09-30":"-14545000000.0","2020-09-30":"-4289000000.0","2019-09-30":"*"},"21":{"Breakdown":"Net Investment Purchase And Sale","2024-09-30":"13690000000.0","2023-09-30":"16001000000.0","2022-09-30":"-9560000000.0","2021-09-30":"-3075000000.0","2020-09-30":"5453000000.0","2019-09-30":"*"},"22":{"Breakdown":"Purchase of Investment","2024-09-30":"-48656000000.0","2023-09-30":"-29513000000.0","2022-09-30":"-76923000000.0","2021-09-30":"-109558000000.0","2020-09-30":"-114938000000.0","2019-09-30":"*"},"23":{"Breakdown":"Sale of Investment","2024-09-30":"62346000000.0","2023-09-30":"45514000000.0","2022-09-30":"67363000000.0","2021-09-30":"106483000000.0","2020-09-30":"120391000000.0","2019-09-30":"*"},"24":{"Breakdown":"Net PPE Purchase And Sale","2024-09-30":"-9447000000.0","2023-09-30":"-10959000000.0","2022-09-30":"-10708000000.0","2021-09-30":"-11085000000.0","2020-09-30":"-7309000000.0","2019-09-30":"*"},"25":{"Breakdown":"Purchase of PPE","2024-09-30":"-9447000000.0","2023-09-30":"-10959000000.0","2022-09-30":"-10708000000.0","2021-09-30":"-11085000000.0","2020-09-30":"-7309000000.0","2019-09-30":"*"},"26":{"Breakdown":"Net Business Purchase And Sale","2024-09-30":"*","2023-09-30":"*","2022-09-30":"-306000000.0","2021-09-30":"-33000000.0","2020-09-30":"-1524000000.0","2019-09-30":"-624000000.0"},"27":{"Breakdown":"Purchase of Business","2024-09-30":"*","2023-09-30":"*","2022-09-30":"-306000000.0","2021-09-30":"-33000000.0","2020-09-30":"-1524000000.0","2019-09-30":"-624000000.0"},"28":{"Breakdown":"Net Other Investing Changes","2024-09-30":"-1308000000.0","2023-09-30":"-1337000000.0","2022-09-30":"-2086000000.0","2021-09-30":"-385000000.0","2020-09-30":"-909000000.0","2019-09-30":"*"},"29":{"Breakdown":"Financing Cash Flow","2024-09-30":"-121983000000.0","2023-09-30":"-108488000000.0","2022-09-30":"-110749000000.0","2021-09-30":"-93353000000.0","2020-09-30":"-86820000000.0","2019-09-30":"*"},"30":{"Breakdown":"Cash Flow from Continuing Financing Activities","2024-09-30":"-121983000000.0","2023-09-30":"-108488000000.0","2022-09-30":"-110749000000.0","2021-09-30":"-93353000000.0","2020-09-30":"-86820000000.0","2019-09-30":"*"},"31":{"Breakdown":"Net Issuance Payments of Debt","2024-09-30":"-5998000000.0","2023-09-30":"-9901000000.0","2022-09-30":"-123000000.0","2021-09-30":"12665000000.0","2020-09-30":"2499000000.0","2019-09-30":"*"},"32":{"Breakdown":"Net Long Term Debt Issuance","2024-09-30":"-9958000000.0","2023-09-30":"-5923000000.0","2022-09-30":"-4078000000.0","2021-09-30":"11643000000.0","2020-09-30":"3462000000.0","2019-09-30":"*"},"33":{"Breakdown":"Long Term Debt Issuance","2024-09-30":"0.0","2023-09-30":"5228000000.0","2022-09-30":"5465000000.0","2021-09-30":"20393000000.0","2020-09-30":"16091000000.0","2019-09-30":"*"},"34":{"Breakdown":"Long Term Debt Payments","2024-09-30":"-9958000000.0","2023-09-30":"-11151000000.0","2022-09-30":"-9543000000.0","2021-09-30":"-8750000000.0","2020-09-30":"-12629000000.0","2019-09-30":"*"},"35":{"Breakdown":"Net Short Term Debt Issuance","2024-09-30":"3960000000.0","2023-09-30":"-3978000000.0","2022-09-30":"3955000000.0","2021-09-30":"1022000000.0","2020-09-30":"-963000000.0","2019-09-30":"*"},"36":{"Breakdown":"Short Term Debt Issuance","2024-09-30":"*","2023-09-30":"*","2022-09-30":"3955000000.0","2021-09-30":"*","2020-09-30":"*","2019-09-30":"*"},"37":{"Breakdown":"Short Term Debt Payments","2024-09-30":"*","2023-09-30":"*","2022-09-30":"*","2021-09-30":"*","2020-09-30":"-963000000.0","2019-09-30":"*"},"38":{"Breakdown":"Net Common Stock Issuance","2024-09-30":"-94949000000.0","2023-09-30":"-77550000000.0","2022-09-30":"-89402000000.0","2021-09-30":"-85971000000.0","2020-09-30":"-72358000000.0","2019-09-30":"*"},"39":{"Breakdown":"Common Stock Issuance","2024-09-30":"*","2023-09-30":"*","2022-09-30":"*","2021-09-30":"1105000000.0","2020-09-30":"880000000.0","2019-09-30":"781000000.0"},"40":{"Breakdown":"Common Stock Payments","2024-09-30":"-94949000000.0","2023-09-30":"-77550000000.0","2022-09-30":"-89402000000.0","2021-09-30":"-85971000000.0","2020-09-30":"-72358000000.0","2019-09-30":"*"},"41":{"Breakdown":"Cash Dividends Paid","2024-09-30":"-15234000000.0","2023-09-30":"-15025000000.0","2022-09-30":"-14841000000.0","2021-09-30":"-14467000000.0","2020-09-30":"-14081000000.0","2019-09-30":"*"},"42":{"Breakdown":"Common Stock Dividend Paid","2024-09-30":"-15234000000.0","2023-09-30":"-15025000000.0","2022-09-30":"-14841000000.0","2021-09-30":"-14467000000.0","2020-09-30":"-14081000000.0","2019-09-30":"*"},"43":{"Breakdown":"Net Other Financing Charges","2024-09-30":"-5802000000.0","2023-09-30":"-6012000000.0","2022-09-30":"-6383000000.0","2021-09-30":"-5580000000.0","2020-09-30":"-2880000000.0","2019-09-30":"*"},"44":{"Breakdown":"End Cash Position","2024-09-30":"29943000000.0","2023-09-30":"30737000000.0","2022-09-30":"24977000000.0","2021-09-30":"35929000000.0","2020-09-30":"39789000000.0","2019-09-30":"*"},"45":{"Breakdown":"Changes in Cash","2024-09-30":"-794000000.0","2023-09-30":"5760000000.0","2022-09-30":"-10952000000.0","2021-09-30":"-3860000000.0","2020-09-30":"-10435000000.0","2019-09-30":"*"},"46":{"Breakdown":"Beginning Cash Position","2024-09-30":"30737000000.0","2023-09-30":"24977000000.0","2022-09-30":"35929000000.0","2021-09-30":"39789000000.0","2020-09-30":"50224000000.0","2019-09-30":"*"},"47":{"Breakdown":"Income Tax Paid Supplemental Data","2024-09-30":"26102000000.0","2023-09-30":"18679000000.0","2022-09-30":"19573000000.0","2021-09-30":"25385000000.0","2020-09-30":"9501000000.0","2019-09-30":"*"},"48":{"Breakdown":"Interest Paid Supplemental Data","2024-09-30":"*","2023-09-30":"3803000000.0","2022-09-30":"2865000000.0","2021-09-30":"2687000000.0","2020-09-30":"3002000000.0","2019-09-30":"*"},"49":{"Breakdown":"Capital Expenditure (CapEx)","2024-09-30":"-9447000000.0","2023-09-30":"-10959000000.0","2022-09-30":"-10708000000.0","2021-09-30":"-11085000000.0","2020-09-30":"-7309000000.0","2019-09-30":"*"},"50":{"Breakdown":"Issuance of Capital Stock","2024-09-30":"*","2023-09-30":"*","2022-09-30":"*","2021-09-30":"1105000000.0","2020-09-30":"880000000.0","2019-09-30":"781000000.0"},"51":{"Breakdown":"Issuance of Debt","2024-09-30":"0.0","2023-09-30":"5228000000.0","2022-09-30":"5465000000.0","2021-09-30":"20393000000.0","2020-09-30":"16091000000.0","2019-09-30":"*"},"52":{"Breakdown":"Repayment of Debt","2024-09-30":"-9958000000.0","2023-09-30":"-11151000000.0","2022-09-30":"-9543000000.0","2021-09-30":"-8750000000.0","2020-09-30":"-12629000000.0","2019-09-30":"*"},"53":{"Breakdown":"Repurchase of Capital Stock","2024-09-30":"-94949000000.0","2023-09-30":"-77550000000.0","2022-09-30":"-89402000000.0","2021-09-30":"-85971000000.0","2020-09-30":"-72358000000.0","2019-09-30":"*"},"54":{"Breakdown":"Free Cash Flow","2024-09-30":"108807000000.0","2023-09-30":"99584000000.0","2022-09-30":"111443000000.0","2021-09-30":"92953000000.0","2020-09-30":"73365000000.0","2019-09-30":"*"}}}


# Earnings Transcript endpoint 
https://finance-query.onrender.com/v1/earnings-transcript/TSLA?quarter=Q3&year=2024 <-- users will specify the stock they want,
'quarter' or 'annual', & the year 

# JSON format the endpoint returns 
{
  "symbol":"TSLA",
  "transcripts":
  [{"symbol":"TSLA","quarter":"Q3","year":2024,"date":"2024-09-15T00:00:00",
  "transcript":"Travis Axelrod: Good afternoon, everyone, and welcome to Tesla's Third Quarter 2024 Q&A webcast. My name is Travis Axelrod, Head of Investor Relations, and I am joined today by Elon Musk, Vaibhav Taneja and a number of other executives. Our Q3 results were announced at about 3 P.M. Central Time in the update deck we published at the same link as this webcast. During this call, we will discuss our business outlook and make forward-looking statements. These comments are based on our predictions and expectations as of today. Actual events or results could differ materially due to a number of risks and uncertainties, including those mentioned in our most recent filings with the SEC. During the question-and-answer portion of today's call, please limit yourself to one question and one follow-up. Please use the raise hand button to join the question queue. Before we jump into Q&A, Elon has some opening remarks. Elon?\n\nElon Musk: Thank you. So to recap, something that [Indiscernible] the industry I've seen year-over-year declines in order volumes in Q3. Tesla at the same time has achieved record deliveries. In fact, I think if you look at EV companies worldwide to the best of my knowledge, no EV company is even profitable. And I'm not - to the best of my knowledge, there was no EV division of any company, of any existing auto company that is profitable. So it is notable that Tesla is profitable despite a very challenging automotive environment. And this quarter actually is a record Q3 for us. So we produced our 7-millionth vehicle actually just yesterday. So congratulations to the teams that made it happen in Tesla. That's staggeringly immense amount of work to make 7million cars. So, let's see. And we also have the energy storage business is growing like wildfire, with strong demand for both Megapack and Powerwall. And as people know, on October 10th, we laid out a vision for an autonomous future that I think is very compelling. So, the Tesla team did a phenomenal job there with actually giving people an opportunity to experience the future, where you have humanoid robots walking among the crowd, not with a canned video presentation or anything, but literally walking among the crowd, serving drinks and whatnot. And we had 50 autonomous vehicles. There were 20 Cybercabs, but there were an additional 30 Model Ys operating fully autonomously the entire night, carrying thousands of peoples [Indiscernible] with no incidents, the entire night. So -- and for those who went there that -- it's worth emphasizing that these the Cybercab had no steering wheel or brake or accelerator pedals. Meaning, there was no -- there's no -- there was no way for anyone to intervene manually even if they wanted to. And the whole night went very smoothly. So, regarding the vehicle business, we are still on-track to deliver more affordable models starting in the first half of 2025. This is I think probably people are wondering what should they assume for vehicle sales growth next year. And at the risk of - to take a bit of risk here, I do want to give some rough estimate, which is I think it's 20% to 30% vehicle growth next year. Notwithstanding negative external events, like if there's some force majeure events, like some big war breaks out or interest rates go sky high or something like that, then we can't overcome massive force majeure events. But I think with our lower cost vehicles with the advent of autonomy something like a 20% to 30% growth next year is my best guess. And then Cybercab reaching volume production in ’26. I do feel confident of Cybercab reaching volume production in ‘26. So just starting production, reaching volume production in ‘26. And that's -- that should be substantial. And we're aiming for at least 2 million units a year of Cybercab. That'll be in more than one factory, but I think it's at least 2 million units a year, maybe 4 million ultimately. So, yeah, these are just my best guesses, but if you ask me my best guesses, that those are my best guesses. The cell 4680 lines, the team is actually doing great work there. The 4680 is rapidly approaching the point where it is the most competitive set. So when you consider the fully landed - the cost of a battery pack, fully landed in the U.S. net of incentives and duties, the 4680 is tracking to be the most competitive. Meaning lower cost [Indiscernible] considered than any other alternative. We're not quite there yet, but we're close to being there, which I think is, extremely exciting. And we've got several - a lot of ideas to go well beyond that. So if I think there's -- if we execute well, the 4680 will have the -- Tesla internally produced cell will be the most cost competitive cell in North America, a testament to a tremendous amount of hard work there by the team. So that's - we'll continue to buy a lot of cells from our competitors. Our intent is not to make to provide to make cells just internally. So I don't want to set off any alarm bells here. We're also increasing substantially our vehicle output and our stationary storage output. So we need a lot of cells. And most of them will still come from suppliers, but I think it is some good news that the Tesla internal cell is likely - is tracking to be the most competitive in the U.S. So with respect to autonomy, as people are experiencing in the cars, really from week-to-week, there are significant improvements in the miles between interventions. So with the new version 12.5, release of full self-driving in Cybertruck, combining the code into a single stack so that the, city driving and the entering the highway driving are one stack, which is a bigger burden for the highway driving. So it's just all neural nets. And the release of Actually Smart Summon. We're trying to have a sense of humor here. And we're also -- so that that's 12.5. Version 13 of FSD is going out soon. Ashok will elaborate more on that later in the call. We expect to see some roughly a 5 or 6 fold improvement in miles between interventions compared to 12.5. And looking at the year as a whole, the improvement in miles between interventions, we think will be at least three orders of magnitude. So that's a very dramatic improvement in the course of the year. And we expect that trend to continue next year. So, the current internal expectation for the Tesla FSD having longer miles between intervention than human is the second quarter of next year, which means it may end up being the third quarter, but it's next - it seems extremely likely to be next year. Ashok. Do you want to add anything?\n\nAshok Elluswamy: Yeah. miles between critical interventions, yep, like you mentioned, Elon, we already made a 100x improvement with 12.5 from starting of this year. And then with v13 release, we expect to be a 1000x from the beginning - from January of this year on production [Indiscernible] software. And this came in because technology improvements going to end-to-end, having higher frame rate, partly also helped by hardware force, more capabilities, so on. And we hope that we continue to scale the neural network, the data, the training compute, et cetera. By Q2 next year, we should cross over the average human miles per critical intervention, call it collision in that case.\n\nElon Musk: I mean, that that's just unvarnishing our internal estimate.\n\nAshok Elluswamy: Yes. Yeah.\n\nElon Musk: So, that's not sandbagging or anything else. Our internal estimate is Q2 of next year to be safer than human and then to continue with rapid improvements, thereafter. So, a vast majority of humanity has no idea that Teslas drive themselves. So especially for something like a Model 3 or Model Y, it looks like a normal car. So you don't expect normal car to be able to be intelligent enough to drive itself. The Cybercab looks different. Cybertruck looks different. But Model Y and Model 3 look, they're good looking cars, but look, I think, look fairly normal. You don't expect a fairly normal looking car to have the intelligence enough AI to be able to drive itself, but it does. So we do want to expose that to more people. And so we're doing every time we have, a significant improvement in the software, we'll roll out another sort of 30 day trial. So to encourage people to try it again. And we are seeing a significant improvement in adoption. So the take rate for FSD has improved substantially especially after the 10/10 event. So there's no need to wait for a robo-taxi or Cybercab to experience full autonomy. We expect to achieve that next year with the -- with our existing vehicle line.\n\nAshok Elluswamy: One point Actually Smart Summon gives a small taste of what it's going to look like, the car able to drive itself to the user within private parking lots. Currently, it's speed limited, but then it's going to quickly be increased. And we already had more than 1 million usage [Indiscernible] of Smart Summon.\n\nElon Musk: Yep. So, and we actually we have, for Tesla employees in the Bay Area, we already are offering a ride-hailing capability. So you can actually with the development app, you can request a ride, and it'll take you anywhere in the Bay Area. We do have a safety driver for now, but the software required to do that, we've developed and I mean, David, do you want to elaborate on that?\n\nUnidentified Company Representative: Yeah. Sure. David, we showed some screenshots of this in the Q1 shareholder deck. And, yeah, this is real. We've been testing it for the better part of the year and, the building blocks that we needed in order to build this functionality and deliver it to production, we've been thinking about working on for years. It just so happens that we've used those building blocks to deliver great features for our customers in the meantime, such as sharing your profile, synchronizing it across cars, so that every single car that you jump into, whether it's another car that you own or a car that somebody's loaned to you or a rental car that you jump into, it looks exactly like yours. Everything's synchronized, seat mirror positions, media navigation, everything is the same. Just what you would expect from, one of our robotaxis. But we gave that functionality to our customers right now because we built it intending for it to be used in the future. We’re releasing that functionality now. All the -- and then cybersecurity that we knew we were going to need to deliver that functionality, sending a navigation to destination from your phone to the vehicle, and so we’re doing that now with the ride-hailing app, but it's something that we've made available to customers for years. Seeing the progress on route in the mobile app, that's something you'll need for the ride-hailing app. But again, we released it in the meantime. So it's not like we're just starting to think about this stuff right now while we're building out the early stages of our ride-hailing network. We've been thinking about this for quite a long time, and we're excited to get the functionality out there.\n\nElon Musk: Yeah. And we do expect to roll out ride-hailing in California, Texas next year to the public. But not the California is somewhat there's quite a long regulatory approval process. I think we should get approval next year, but it's contingent upon regulatory approval. Texas is a lot faster. So it's, I'd say, like, we're -- we'll definitely have available at Texas, and probably have it available in California subject to regulatory approval. And then -- and maybe some other states actually, next year as well, but at least California and Texas. So that'd be very exciting. There's really a profound change. Tesla becomes more than a sort of vehicle and battery manufacturing company, at that point. So we published our Q3 vehicle safety report, which shows one impact for every 7 million miles of autopilot, that compares to the U.S. average of one crash roughly every 700,000 miles. So it's currently showing a 10x safety improvement relative to the U.S. average. And we continue to expand our AI training capacity to accommodate the needs of both FSD and Optimus. We're currently not a training compute constraint. That's probably the biggest factors that the FSD is actually getting so good that it takes us a while to actually find mistakes. And when you start getting to where it could take 10,000 miles to find a mistake, it takes a while to actually figure out which it is -- is this soccer ball better than -- is soccer ball A better than soccer ball B? It actually takes a while to figure it out because neither one of them are making mistakes, or takes take a long time to make mistakes. So that's actually the single [Indiscernible] based on many factors. How long does it take us to figure out which version is better? So that’s sort of high class problem. Obviously, having a giant fleet is very helpful for breaking this out. And then with Optimus, we show a massive improvement in Optimus's dexterity movement on October 10. And our next-gen, hand and forearm, which has 22 degrees of freedom double - which is double the prior hand and forearm, it's extremely human like. And also it's much better tactile sensing. It's really - I feel confident in saying that we have most advanced humanoid robot by long shot. And we're moreover the only company that really has all of the ingredients necessary to scale humanoid robots. Because the things that what other companies are missing is that they're missing the AI brain, and they're missing the ability to really scale to very high volume production. So some have seen some impressive video demos, but what but they’re [lacking is] (ph) localized AI and the [going] (ph) to scale volume to very high numbers. As I've said on a few occasions before, I think Optimus will ultimately be the most valuable product. So I think it has a good chance of being the most valuable product ever made. For the energy business, that's doing extremely well. And there's the opportunity ahead is gigantic. The Lathrop Megapack factory, reached 200 Megapacks a week, which is now a 40 gigawatt hour a year run rate. And, we have a second factory in Shanghai that will begin with a 20 gigawatt hour a year run rate in Q1 next year, so next quarter. And, that will also scale up. It won't be long before, we're shipping a 100 gigawatt hours a year, stationary storage at Tesla. And that'll ultimately grow I think to multiple terawatt hours per year. It has to actually in order to have a sustainable energy future. If you're not at the terawatt scale, you're not really moving the needle. So if you look at our admittedly very complicated last master plan, which I think actually is too much detail. I'll -- maybe I'll ask [Vaibhav] (ph) to analyze it.\n\nUnidentified Company Representative: Sure Elon.\n\nElon Musk: Can give us the TLDR on the last master plan. But we showed in that last plan that it is possible to take all of us to a fully sustainable energy situation, using sustainable energy power generation and batteries and electric transport. And there are no fundamental material limitations. Like, there's not some very rare material that we don't have enough of on earth. We actually have enough of raw materials to, yeah, take all of human civilization make it fully sustainable. And even if civilization dramatically increased its electricity usage, it would still be fully sustainable. One way to think of the progress of a civilization, it's based out a little esoteric, but is percentage completion of Kardashev scale. So Kardashev Scale 1 would be you're using all the power of a planet. We were we're currently less than 1% on Kardashev Level 1. Level 2 would be using all the power of the sun. And level 3, all the power of the galaxy. So we have a long way to go. Long way to go. When you think in Kardashev terms, it becomes obvious that by far the biggest source of energy is the sun. Everything else is in the noise. So in conclusion, Tesla is focused on building the future of energy, transport, robotics, and AI. And this is a time when others are just focused on managing around near term trends. We think what we're doing is the right approach. And, if we execute on our objectives, then I think we will. Tesla my prediction is Tesla will become the most valuable company in the world and probably by a long by a long shot. I want to thank the Tesla team once again for strong execution in a tough operating environment, and we're looking forward to building, an incredibly exciting future. Thank you.\n\nTravis Axelrod: Great. Thank you very much, Elon. And I'll let Vaibhav pass some more big remarks as well.\n\nVaibhav Taneja: Yeah. Thanks. Our Q3 results were positive and once again, demonstrate the scale to which businesses evolved. What they use with the generation of record operating cash flows of $6.3 billion. Our automotive revenues grew both quarter-on-quarter, year-on-year. While we had unit volume growth, we did experience reduction in ASPs, primarily due to the impact of financing incentives. As a reminder, we are providing these incentives primarily using third-party banks and financial institution and recognize the cost of these incentives as an upfront reduction to them. We released FSD for Cybertruck and other features like Actually Smart Summon, like Elon talked about in North America, which contributed $326 million of revenues in the quarter. We continue to see elevated levels of regular 2 week credit sales with over $2 billion of revenues so far this year. To expand on this at an industrial level, China continues to outperform U.S. and Europe by a factor of three. And if there is something to be learned from that, this gives a signal of what is to come in other regions. As customers’ acceptance of EV growth. And we feel that is the right strategy to build affordable and more compelling leads. Our focus remains on growing unit volume, while avoiding a build-up of inventory. To support this strategy, we're continuing to offer extremely compelling vehicle financing options in every market. When you compare any vehicle in our lineup with other OEMs, believe our vehicles provide much better value, particularly when you consider the safety features, performance, and unparalleled software functionalities, like David also talked about, include also what, Ashok talked about around autonomy, music options, parental controls, and much more. While every vehicle in our lineup comes up with these capabilities, there is an awareness gap, not just with buyers, but at times, even with existing owners. We plan on making these more visible in our interactions with both existing and future customers. Automotive margins improved quarter over quarter as a result of a 50 features released discussed before. Increase in our overall production and delivery volume, albeit benefit from the marketing pricing, and more localized deliveries in region, which resulted in lower freight and duties. Sustaining these margins in Q4, however, will be challenging given the current economic environment. Note that we are focused on the cost per vehicle, and there are numerous work streams within the company to squeeze that cost without compromising on customer experience.\n\nElon Musk: Yes. I'm assuming that's a helpful -- hopefully, a helpful macro trend is if there's a decline in in interest rates, this has a massive effect on the, automotive demand. The vast majority of people is or the demand is driven by the monthly payment. Can they put monthly payment? So, like, most likely, we'll see continue to decline interest rates, which helps with affordability vehicles.\n\nVaibhav Taneja: Yeah. I mean, that is one trend which we observed in the industry that, because of affordability being impacted because of interest rates, People are willing to take cars longer, especially in the U.S. And that is actually having an impact on all our industry too. As we discussed, earlier, as we discussed impact orders, energy deployments fluctuate quarter over quarter due to customer readiness, location of orders being fulfilled, and not necessarily an indicator of demand or production within the quarter. While we did see a decline in Q3, we expect to grow our deployment sequentially in Q4 to end the year with more than doubled of last year. Energy margins in Q3 were a record at more than 30%. This is a function of mix of projects being deployed in the quarter. Note that there will be fluctuation in margins as we manage through deployments and our inventory. Our pipeline and backlog continue to grow quarter over quarter as we fill our 2025 production slots, and we're doing our little best to keep up with the demand. Just coming back on automotive margins, I talked about -- sorry. I talked about what is happening. One other thing which I want to also share is that we're -- that we will continue to keep whatever we can to squeeze like I said before about squeezing out the cost. But this is something which we also are very capable of. I mean, just in Q3, we reached our lowest cost per micro. And that is a trend which we will keep focus on. Then going on to service and other, we continue to show improvements in Q3. This was a result of better performance, both in our service business, which includes collision part sales and merchandise, and continued growth in supercharging. These field based revenues will continue to grow as the overall fleet size increases. Our operating expenses declined quarter over quarter in a year on year basis. This is partially due to the restructuring we undertook in Q2. Cost savings from these initiatives were partially offset by increase in costs related to our AI efforts. We've started using the GPU cluster based out of our factory house and ahead of schedule, and are on track to get 50k GPUs deployed in Texas by the end of this month. One thing which I'd like to elaborate is that we're being very judicious on our AI compute spend too and saying how best we can utilize the existing infrastructure before making further investments. On the CapEx front, we had about $3.5 billion in the quarter. This was a sequential increase largely because of investments in AI compute. We now expect our CapEx for the year to be in excess of $11 billion. We shared our vision for the future at the real world event at the beginning of the month. The Tesla team is hyper focused on delivering on that version, and all efforts are underway to make it a reality. While we've achieved significant progress this year, it will take time to get this as we find a new and incredibly complex technologies and navigate a fragmented regulatory landscape. Future is incredibly bright, and I want to thank the Tesla team once again for all their help.\n\nA - Travis Axelrod: Great. Thank you very much, Vaibhav. Now we'll go to investor questions. The first one is, is Tesla still on track to deliver the more affordable model next year as mentioned by Elon earlier? And how does it align with your AI product roadmap?\n\nLars Moravy: Sure. I mean, as Elon and Vaibhav both said, you are in plan, to meet that in the first half of next year. Our mission has always been to lower the cost of our vehicles to increase the adoption of sustainable energy and transport. Part of that is lowering the cost for current vehicles, which is where, all of the personally owned vehicles that we sell today come in. But the next stage in that really is it fits into AI roadmap is when we bring in robotaxis, which lowers the initial cost of getting into an EV. And those -- that's really where we see the marriage of EV road map and the AI road map.\n\nElon Musk: Yeah. It'll be with incentive sub-30k, which is kind of a key threshold.\n\nTravis Axelrod: Great. Thank you very much. Similar, question next. When can we expect Tesla to give us the $25,000 non-robotaxi regular car model?\n\nElon Musk: We're not breaking it on.\n\nLars Moravy: Yeah. All our vehicles today are road jets.\n\nElon Musk: I think we've made very clear that, we're the future is autonomous. It I mean, I it's going to be you know, I've actually said this many years ago, but that, in my strong belief, and I believe that is panning out to be true. So and I'll be very obvious in retrospect, is that the future is autonomous electric vehicles, and, non-autonomous gasoline vehicles in the future will be like riding a horse and using a foot bone. It's not that there are no horses. Yeah. There are some horses, but they're unusual. They're niche. And so it just everything's going to be electric autonomous. I think this is like it should be frankly blindingly obvious at this point that that is the future. So a lot of automotive companies or most automotive companies have not internalized this, which is surprising, because we've been shouting this from the rooftops for such a long time, and it will accrue to their detriment in the future. But all of our vehicles in the future will be autonomous. Yes. So all the vehicles that we've really made, all the 7 million vehicles, vast majority are capable of autonomy. And, we're currently making on the order of 35,000 autonomous vehicles a week. Compare that to, say, Waymo's entire fleet is less than – they’ve have less than a 1,000 cars. We make 35,000 a week.\n\nLars Moravy: Yeah. And our cars look normal.\n\nElon Musk: Yeah. They mostly look normal. The Cybertruck looks abnormal. And the, Cybercab/robotaxi. We wanted to have something futuristic working. I think it does look futuristic. And it's worth noting with respect to the Cybercab. It's not it's especially not just a revolutionary vehicle design, but a revolution in vehicle manufacturing that is also coming with the Cybercab. The cycle time, like, the, the units per hour of the Cybercab line it is -- like, this is just really something special. I mean, this is probably a yeah. Half order of magnitude better than other car manufacturing lines. Like not in the same league is what I'm saying. Not in the same league. So it's -- and I said, like, several years ago that the -- maybe the most I mean, the hottest Tesla product to copy will be the factory. Just like buy a factory.\n\nLars Moravy: Yeah. In camera versus near a factory, that's up to my --\n\nElon Musk: Yeah. It's like things yeah. So the and as we so we're rapidly evolving and manufacturing technology. So anyway, there's, like, basically, I think having a regular $25,000 model is pointless. Yeah. It would be silly. Like, it'll be completely at odds with what we believe.\n\nLars Moravy: In autonomous world. But matters as well as cost per mile of efficiency of that vehicle. And that's what we've done with the robotaxi.\n\nElon Musk: Exactly. Autonomous, it it's fully considered cost per mile, is what matters. And if you try to make a car that is, essentially, a hybrid manual automatic cars. It's not going to be as good as a dedicated autonomous car. So, yeah -- Cybercab is just not going to have steering wheels and pads. It's only designed to optimize for autonomy. But now it'll cost on the order of cost roughly $25,000. So it is a $25,000 car. And you can -- you will be able to buy one on an exclusive exclusively if you want. So just what happens to your mobile phones. You don't need it.\n\nTravis Axelrod: Great. Thank you very much. The next question is, what is Tesla doing to alleviate long wait times at service centers?\n\nUnidentified Company Representative: So we aim on solving problems at the source, so at the factory before they can even affect our customers. We believe the best service is no service and our heads don't even have them.\n\nElon Musk: If the car doesn't break, yeah. That's the best thing.\n\nUnidentified Company Representative: Exactly. Don't see any with the test. You either do it remote, yeah fix the issue upstream or do it remotely, do it through software, maybe being at work or at home and car can be parked. And we've addressed fixed the issue, and we've partnered the field with service to make sure we're looking at the same issues. And additionally, just in Q3 Q4 of this year alone, we have opened and will open in total at nearly 70 locations. And in North America, we've significantly expand the size of each location and have doubled the size last year compared to this year.\n\nElon Musk: Yeah. I think it's, like, actually a lot of merit to having large service centers because you can have specialization of labor. Okay. You can start to approach. Yeah. It should be more factory like, where you can have dedicated lanes for particular types of service. And people and it's way easier for somebody to come expert in a few different types of repairs than in every repair.\n\nUnidentified Company Representative: Exactly. This has helped us with the base set, these heavy repairs clogging up the lane. They've dedicated lanes for different type of repairs. And so it's through a bit massively treating it like a factory.\n\nElon Musk: Yes. This is where a Tesla structure, I think, a strong advantage relative to the rest of the auto industry because we make the cars and we service the cars, whereas I think there's a bit of a conflict of interest with the dealer model and the traditional OEM and dealer model where the dealerships make most of their money on service. And so they don't -- they obviously assistance to reduce the servicing cost, whereas in our case, we are incented to reduce the service and cost because we carry that servicing cost. And we've got a good feedback with our cars.\n\nUnidentified Company Representative: Exactly. If you were with the factory, with the service leaders together, and send back people from the factories that field to the factory to see it firsthand. Suggestions for manufacturing as well as for engineering on design.\n\nElon Musk: Yeah. So I view this as a structural -- fundamental structural advantage of Tesla versus the rest of the auto industry.\n\nUnidentified Company Representative: Also do a bunch of work on the software side, not only to automate diagnostics so identifying what needs to be done to a car before it comes into service, but also automating all of the preparation work and aligning all the resources that are necessary in order for the car to be very efficiently worked on once it arrives. So the parts are there, like, the lift is scheduled, the technician's schedule, like, everything that's what I'm saying. This is what's wrong with me, and tells us tell the service center.\n\nUnidentified Company Representative: The car everything ready in the van.\n\nElon Musk: Yeah. Please fix me and this is what's wrong.\n\nUnidentified Company Representative: This is what I'm trying to do now. This is what I'm trying to do. Yeah.\n\nUnidentified Company Representative: Instead of customer trying to translate the car, it's telling us directly and we're pulling that. Yeah.\n\nElon Musk: Yeah. You don't need most of the time, you don't need to diagnose the car when it arrives. The car yeah -- this is like, again, a fundamental technology advantage and structural advantage compared to the rest of the auto industry.\n\nVaibhav Taneja: I think it's underappreciated as to what all we are able to do. And that's why because like you said before, most of our cars, except for Cybertruck, look the same. So people don't realize that it has so much capability.\n\nElon Musk: Yeah. But, like, that's better than other cars. But they don't, like, obviously, like, super futuristic. Yes.\n\nTravis Axelrod: So yeah. Great. Thank you very much. The next question is, please provide an update on the semi. What will the next stage of growth look like, and when will FSD be ready?\n\nLars Moravy: Sure. So as you we posted in earnings back, we're progressing swiftly on the build of the semi factory in there, in our data factory in Reno. We've released all our major capital expenditures for that program, and we're on track to start, pilot builds in the second half of next year with production starting in the first half of 2026 and ramping really throughout the year to full production. Semi, growth will largely depend on our customers' adoption of the product.\n\nElon Musk: Well, I don't think we're going to be demand limited, honestly.\n\nLars Moravy: Yeah. Which I was going to say, which is like a brainer for the semi because it's really a commodity of total cost of ownership.\n\nElon Musk: Yes. Exactly. It's good. We have kind of ridiculous demand for the semi.\n\nUnidentified Company Representative: In that world where it's about how much do I spend to go to excess lanes per mile, it's a no brainer.\n\nLars Moravy: Yeah. Fundamentally, if you've got a semi where the fully considered cost per mile or per ton of transport, is better than, say, diesel truck, any company that doesn't adopt an electric semi will lose. It's not -- it's not it's not a subjective thing. It's like whether do you like just a competitive I mean, we like, we want the start we want we want to have a good old semi-truck, but frankly, if we made an oxy semi-truck, it wouldn't matter.\n\nLars Moravy: And this is proving so in our fleets, in in Pepsi's Partner. In fact, the Pepsi actually said last week, they're having nobody want their drivers don't want to go back.\n\nElon Musk: Yeah. Yeah. As soon as we give anyone the electric semi, it it's like -- that's like the choice.\n\nLars Moravy: It's the, what they want to drive.\n\nElon Musk: Yeah. That's like so the -- like the most, like their top drivers will, they get to drive the Tesla Semi. It's, it's, it's the, it's the thing they want to drive.\n\nLars Moravy: It's super fun to drive. It's also very easy to drive.\n\nElon Musk: It's easy to drive and it holds ass. It's like fast.\n\nLars Moravy: Superfast. Maybe too fast.\n\nElon Musk: Well, but I mean, like, like, ring like this. Like, you've seen, like, the videos of where, like, I think, like, Tesla Electric Semi, like, can go uphill Just pass. Speed speeding past, like, the diesel truck or even cars. So, like, it's responsive. It it's you floor it and that that truck actually hurt.\n\nLars Moravy: And that's a benefit not only for the driver and for the goods, but also for safety in terms of other drivers on the road. You don't get stuck behind the semi. You're not, like in a slowdown situation in an on ramp. I mean, how that plays into, you know, FSD, which is the second part of the question. All of the semis have been since the couple hundred we've deployed already, and the ones that we'll be building next year and throughout, the future have all the hardware and the cameras necessary to, deploy FSD, and we're currently training with that small fleet that we have. And as soon as the fleet is trained and the neural nets are up, we'll get FSD onto that platform.\n\nElon Musk: Yeah. I mean, it'd be a massive improvement in, driver fatigue, because, driver safety, we've got sort of the anti-jack knifing software. You don't have to worry about your brakes overheating if you go down a down a steep hill because the -- we use regenerative, like, that that energy goes back into the pack. It's just like it's like radically better than it is in some way. It's what the drivers love it.\n\nTravis Axelrod: Great, guys. Thank you very much. Our next question is, when will Tesla incorporate X and Grok in all of the Tesla vehicles?\n\nElon Musk: Well, I mean, these are relatively small things. But, yeah, with the -- I think, we'll keep expanding, what is available in the car on the on screen and also improving the browser. So, just generally, you can access anything you want in the car. In fact, for the Tesla we're scheduled for autonomy. You actually want fully a system that is can do anything. Like, if you want to browse the Internet, if you want to ask AI questions, if you want to watch a movie, if you want to play a video game, if you want to do some productivity thing, you can do anything you want in an autonomous vehicle because you don't need to drive. So that's why the Cybercab got a nice big screen and a great sound system. So you can watch it -- watch a great movie with, it's like being in a Personal movie theater?\n\nUnidentified Company Representative: This is why we've been building this functionality, adding gaming to the car, adding movies and other, you know, all sorts of different media applications of the car because the cars, that's what you're going to -- that's the cars will be built today.\n\nElon Musk: There's some fun games, by the way. People haven't tried it. There's Castle Doombad and Polytopia and a bunch of really fun games in the car.\n\nUnidentified Company Representative: Yes. We're constantly looking at what features to add next and we're paying attention to what's most commonly requested by our customers.\n\nElon Musk: Yes. Play Castle, Doombad. You want --\n\nTravis Axelrod: Great. Thank you guys very much. The next question is, Elon mentioned unsupervised FSD in California and Texas next year. Does that mean regulators have agreed to it in the entire state for existing Model 3 and 4 vehicles?\n\nElon Musk: No. As I said earlier, California lost regulation. But they have a pathway? Yeah. I mean, there's a pathway. Obviously, Waymo operates in California. So there's just a lot of forms but a lot of approvals that are required. I mean, I'd be shocked if we don't get approval next year, but it's just not something we totally control. But I think we will get approval next year, in California and Texas. And for the end of the year, it will branch out be beyond California and Texas.\n\nLars Moravy: I mean, I think it's important to reiterate this. Like, homogeneity or certifying a vehicle at the federal level in the U.S. is done by meeting FMVSS regulations. All our vehicles today that are produced that are autonomous capable meet all those regulations, cybertruck need those regulations. And so the deployment of the vehicle to the road is not a limitation. What is a limitation is what you said at the state level where they control autonomous vehicle deployment. Some states are relatively easy as you mentioned for Texas. Yeah. And so other ones have in place like California that may take a little longer. Other ones haven't set up anything yet, and so we will work through those state by state.\n\nElon Musk: I do think we should have a federal, I agree. Like, autonomous vehicles should be approved. They just should be -- it should be possible to.\n\nLars Moravy: Congress, if you're listening, let's say the federal AV --\n\nElon Musk: There should -- there should be a federal approval process for autonomous vehicles. I mean, that's how the FMVSS is worked. Federal Motor Vehicle. The FMBSS is federal.\n\nUnidentified Company Representative: Yeah. So, I mean, in 2017 and ‘18, they we know it's when regulators started looking at it. And it's really kind of stalled since then, but we would appreciate and would support helping out with those regulators.\n\nElon Musk: It really needs to be a national approval is important. There's department of government efficiency. I'll try to help make that happen. And you said for everyone, not just Tesla, obviously. But just, like some things in the U.S. are state by state regulated for example, insurance. And it's incredibly painful to do it state by state for 50 states. And, I think we should have there should be a natural approval process for autonomy.\n\nTravis Axelrod: Great. Thanks, guys. The next question is, what is the plan for 2025?\n\nElon Musk: I mean, who we just talked?\n\nAshok Elluswamy: Yeah. Just. We I mean, basically, we talked through this. There's a lot going on. Elon already mentioned that we're working on cheaper models to come out. I mean, there are work which the team is doing to get the factories ready today to try and make that happen on --\n\nElon Musk: And by the way, the amount of work required to make a lower cost car is insanely high. But, like, it is harder to get, like, 20% of the cost out of a car than it is to design the car and build the entire factory in the first place. Yeah. It's, like, excruciating. And it's -- and there's not a lot of movies made about the heroes who got 20% of the cost out of a car. But let me tell you, there should be.\n\nUnidentified Company Representative: He's a little changes. And I it's not like a silver.\n\nElon Musk: Yeah. It's like there should be you the heroes who got 20% cost out of a car is like, damn, I have a lot of respect to them. It was like movie. It's like, I think you probably could make a compelling movie, but I it just no. No. Like, if you actually saw how hard it if people actually saw how hard it was to do that, you'd be like, wow. That's damn hard.\n\nUnidentified Company Representative: Just yesterday we were talking about party.\n\nElon Musk: Yeah. I mean, honestly, like, literally yeah. I mean, they've been there's a lot of but I do call it sort of like getting cost out of things. It's kind of like it's -- like game of pennies. So it's like game of thrones but pennies. First approximation, if you've got if you've got 10,000 items, in a car, very rough approximation, and each of them cost $4, then you have a $40,000 car. So if you want to make a $35,000 car, you're going to get $0.50 on average out of the 10,000 items.\n\nUnidentified Company Representative: Every part.\n\nElon Musk: Yeah. And it's like yeah. And then, obviously, the best is you delete some parts. In fact, we've done we have to delete a lot of parts.\n\nUnidentified Company Representative: I'm very excited about the Cybercab design and the well, how we're rethinking the design of a car for the Cybercab, designing it all for high volume production, and then designing machine that builds the machine, that is that I think is also revolutionary. And it's just there's no other car company that's even trying to do what we're doing. Like, I've even heard of it, actually. In fact, I'm certain there is someone like I'm I think this this the new machine that pulls the machine, like, it's inherent it's like the it's put it's designed to be, like, 5x better than a traditional factory. Like, cycle time –\n\nUnidentified Company Representative: Cycle time and, like, part deletion and shipment. I don't think any other car company has the same level of, like, integration of thought that we have when it comes to, like, when you design a part from a white sheet of paper, who's going to make it? Where is it going to be made? How is it going be shipped? How is it going to be assembled into the vehicle? And, like, at any one point, if something is done in a silo, it becomes a bottleneck of either cost or time or efficiency. But with the robotaxi, the development, like, we've done a good job on the like, combining all that and then, like, blowing up how it's made and saying it should be made this way and rethinking it also. It's the most efficient factory possible. That shows in our -- it will show in our CapEx efficiency when we deploy it. It shows in the number of parts. It shows in the simplicity of the vehicle, but also how it performs in in terms of, like, end user, state.\n\nVaibhav Taneja: Just to close-up, just on the energy front also in ‘25, we will have started with flashing up mega factory Shanghai. We'll continue to increase our storage deployments with Powerwall 3. We plan to continue expanding our supercharging network, getting more OEMs on our network. 4680 that as Elon talked about. That would keep going. And then, there's we're also we'll have our lithium refinery starting to produce. So there's a lot which is going on.\n\nElon Musk: Yes, so many things. Like crazy thing is like Tesla is winning basically on almost every single thing we're doing. If we're not running now, we're in a where their entire large companies, that's the only thing they do.\n\nVaibhav Taneja: Yeah. I mean, it's a company -- there are multiple companies within the company.\n\nElon Musk: Yeah. Tesla's like many companies in one.\n\nTravis Axelrod: Yeah. Guys, just a few more. What is going on with the Tesla Roadster?\n\nElon Musk: Some things. Well, I just thought to go back to our long-suffering deposit holders of the Tesla Roadster. The reason it hasn't come out yet is because it is -- Roadster is not just icing on the cake, it's the cherry on the icing on the cake. And so our larger mission is to accelerate the progress towards a sustainable energy future, trying to do things that maximize probably the future is good for humanity and for Earth. And so that necessarily means that like the things like that are deserved. We'd like -- we'd all love to work on the Tesla -- next-gen -- it is super fun. And we are working on it, but it has to come behind the more things that have a more serious impact on the -- of the world. So just thank you to all our long-suffering Tesla Roadster deposit holders. And we are actually finally making progress on that. And we're close to finalizing the design on it. It's really going to be something spectacular, mind and some like [Peter Telaria] we're really good friends. Peter was lamenting how the future doesn't have flying cars. Well, we'll see. More to come.\n\nTravis Axelrod: Yeah. Thanks very much. The next one is quite similar to other questions you've had. So when I combine it with the final question. So briefly, could you just detail how robotaxi will roll out? Will it start with a Tesla deployed fleet and then allow customers to add theirs on the subscription model, and then we'll Hardware 3 capable of this.\n\nAshok Elluswamy: Regarding the Hardware 3, what we saw with was, it was easier to make a progress with starting with Hardware 4 and on the solution and backporting to Hardware 3 instead of directly working on Hardware 3 given that Hardware 4 was more like fundamental hardware capabilities. I think that trend will continue into the next few quarters as well by the first solution rapidly with Hardware 4 and then backwardate and it just takes longer to those things because it's not fundamentally supported in the hardware and it's emulated. But yeah, initially working on Hardware 4, backwarding it to Hardware 3.\n\nElon Musk: Yes. So answer is we're not 100% sure, but as Ashok mentioned, because by some measure, Hardware 4 has really several times the capability of Hardware 3. It's easier to get things to work with then it takes a lot of effort to sort of squeeze that box analyst hat Hardware 3. And there is some chance that Hardware 3 is -- does not achieve the safety level that allows for unsupervised FSD. There was some chance of that. And if that turns out to be the case, we will upgrade those who bought hardware 3 FSD for free. And we have designed the system to be upgradable. So it's and it's really it's really what just to switch sort of switch out the computer type thing. Like, the camera the cameras are yeah. They're capable. But, anyway, we don't we don't actually know the answers to that. But if it does turn out, we will take we'll make sure we take care of those who are bored FSD on Hardware 3.\n\nTravis Axelrod: Great. In the last few minutes that we have left, we will try to get in some analyst questions. The first question will be coming from, Pierre Ferragu at New Street. Pierre, please feel free to unmute yourself.\n\nFerragu Pierre: Thanks a lot, guys, for taking my question. I was wondering about, like, the compute you're, you're ramping up. So you gave, like, interesting statistics on how much you have, and you said you don't feel your compute's constrained. And I was wondering, how you are putting to work this additional compute. Is that a game for you of creating, like, larger and larger models, like next generation of models that are larger the way OpenAI go from GPT-3 to GPT-4, or is that more like you're set on your model and you need to throw more and more compute to accelerate the pace of learning to improve reliability. And then I had a quick follow-up really quick on your rollout in Texas and in California next year. The plan as you see today, is it to roll out, like, a fleet or two, with, cars that will start with, like, a supervisory, like, some soup onboard supervision, someone, sitting at the wheel just in case and removing the supervisors progressively, or are you aiming for going, free fledged without even a human super supervisor when you get started?\n\nElon Musk: Okay. Well, I guess we're going to I'll answer, yeah, the first part of the question. The nature of real world AI is, different from, say, an LLM in that, you have a massive amount of context. So that, like, the you've got, case of Tesla 7 or 8 cameras, that, 9 up to 9 if you include the internal camera that that that so you got gigabytes of context, and that that is then distilled down into a small number of control outputs. Whereas it's like you don't really it's very rare to have in fact, I'm not sure any LLM out there who can do gigabytes of context. And then you've got to then process that in the car with a very small amount of compute power. So, it's all doable and it's happening, but it is a different problem than what, say, a Gemini or OpenAI is doing. And now part of the way you can make up for the fact that the inference computer is quite small is by spending a lot of effort on training. And just like a human, like, you the more you train on something, the less mental workload it takes when you try to -- when you do it, like when the first time like a driving it absolves your whole mind. But then as you train more and more on driving different than the driving becomes a background task. It doesn't -- it only solves a small amount of your mental capacity because you have a lot of training. So we can make up for the fact that the insurance computers -- it's tiny compared to a 10-kilowatt bank of GPUs because you've got a few hundred watts of inference compute. We can make up that with heavy training. So yeah, that's -- and then there's also vast amounts to the actual petabytes of data coming in tremendous. And then sorting out what training is important of the vast amounts of video training video data coming complete what is actually most important for trading. That's quite difficult. But as I said, we're not currently training compute constraint. -- had you want levering\n\nAshok Elluswamy: Like you mentioned, the training has both an large models, also the trend quicker. But in the end, we still got to take which models are performing better. So the validation network to picking the models because as mentioned this pretty large. We had to drive a lot of miles going close to. We do have simulation and other ways to get those metrics. Those two help, but in the end, that's a big bottleneck. That's why we're not trying to compete constraint alone. And there's other access of scaling as well, which is a data figuring office as more useful. That is an important as focusing on that.\n\nUnidentified Company Representative: Yeah. So as it relates to the second part of your question, Pierre, about safety drivers and rolling it out. Each state has different requirements in terms of how many miles and how much time you need to have a safety driver and not have a safety driver. We're going to follow all those were not regulations are out there. But safety is a priority. But the goal is obviously at when we're ready and safety is there, we'll address from the --\n\nElon Musk: Yeah. I mean, I guess like we think that we'll be able to have driverless Teslas during paid rides next year, sometime next year.\n\nTravis Axelrod: All right. Thank you. And our next question comes from Adam Jonas at Morgan Stanley. Adam, please feel free to unmute yourself.\n\nAdam Jonas: Okay, thanks, everybody. I just had a question about the relationship between Tesla and xAI. Many investors are still not clear how the work at xAI is truly beneficial to Tesla. Some even take the view that the two companies may even be in competition with each other in terms of talent and tech and even your time, Elon. So what's your message to investors on that relationship between Tesla and xAI? And where do you see it going over time?\n\nElon Musk: Well, I should say that xAI has been helpful to Tesla AI quite a few times in terms of things like scaling it, bought it, like training, just even like recently in the last week or so, improvements in training, where if you're doing a big training one and it fails, be able to continue training and is to recover from a training on has been pretty helpful. But it but there are different problems. xAI is working on artificial general intelligence or artificial super intelligence. Tesla's trying to make autonomous cars and autonomous robots. They're different problems. So, yeah. I mean --\n\nAshok Elluswamy: I think we've said this before also. Like, all not all AI is equal. Right? I mean, there's AI is a broad spectrum. And we have our own swim lanes. Here, there are certain things which we can collaborate on if needed, but for the most part, we're solving different issues.\n\nElon Musk: Yeah. Tesla’s focus on real world data. And like I said, saying it is quite a bit different from an element. Because, like, you have you have massive context in the form of video and some other audio, that's going to be distilled very like, with extremely efficient advanced compute. I do think Tesla's the most efficient, in the world in terms of inference compute. Like, because out of necessity, we have to we have to be very good at in in efficient inference. We can't pretend 10 kilowatts of GPUs in a car. We've got a couple 100 watts. So, it's pretty well designed Tesla AI chip, but it's still a couple 100 ones. But there are different problems. I mean, this is, like, the stuff that I said is, like, we're going to running in burns. I mean, it's it is running in burns. Like, answering persons, answering questions on a 10 kilowatt rack. It's like, yeah. Put that in the car. It's a different file. No. Exactly. So, xAI is because I felt there wasn't there wasn't a truth seeking digital super intelligence company out there. Like, that's what it came down to. Like, they needed to be a truth seeking like, an AI company that is very rigorous about, being truthful. So I'm not saying xAI is perfect, but that is but that is at least the explosive aspiration. Even if something is politically incorrect, it should still be truthful. I think this is very important for AI safety. So anyway, I think AI, xAI will it has been helpful to Tesla and will continue to be helpful to Tesla, but they are very different problems. Great. And, I mean, like, if you it also thinking like, what is like, what other car company has that -- has a world class trip design team? Like 0. What other car company has a world class AI team like Tesla does? 0. Those were all startups. They're created from scratch.\n\nTravis Axelrod: Great. Thank you, Elon. And I think that's unfortunately all the time that we have for today. We appreciate all of your questions, and we look forward to hearing you next quarter. Thank you very much and goodbye.","participants":["Travis Axelrod","Elon Musk","Ashok Elluswamy","Unidentified Company Representative","Vaibhav Taneja","A - Travis Axelrod","Lars Moravy","Ferragu Pierre","Adam Jonas"],
  "metadata":{"source":"defeatbeta-api","retrieved_at":"2025-10-04T20:27:46.439631","transcripts_id":303380}}],
  "metadata":{"total_transcripts":1,"filters_applied":{"quarter":"Q3","year":2024},"retrieved_at":"2025-10-04T20:27:46.439742"}}

  



























