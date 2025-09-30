# Yahoo Finance Module (stonksapi)

A comprehensive, type-safe Python wrapper for the `yfinance` library with Pydantic models.

**Part of the `stonksapi` package.**

## Features

- ✅ **Strongly Typed**: Full Pydantic model support for `yfinance` responses.
- ✅ **Easy to Use**: Clean, intuitive API with excellent IDE autocomplete.
- ✅ **No API Key Required**: Access Yahoo Finance data freely.
- ✅ **Well Documented**: Extensive docstrings and examples.

## Installation

This package is part of the `stonksapi` project. The `yfinance` library is a dependency.

```bash
uv add yfinance pydantic
```

## Quick Start

```python
from stonksapi.yfinance import YFinanceClient

# Initialize client (no API key needed)
client = YFinanceClient()

# Get company profile information for Apple Inc.
info = client.get_ticker_info("AAPL")

print(f"Company: {info.long_name}")
print(f"Sector: {info.sector}")
print(f"Industry: {info.industry}")
print(f"Market Cap: ${info.market_cap:,}")
print(f"Website: {info.website}")
```

## Type Safety

All responses are fully typed with Pydantic models, giving you:

- **IDE Autocomplete**: Your IDE knows all available fields.
- **Type Checking**: Catch errors before runtime.
- **Validation**: Automatic data validation from API responses.
- **Documentation**: Inline documentation for all fields.

```python
# Your IDE will show you all available fields!
info = client.get_ticker_info("MSFT")

market_cap = info.market_cap  # int type
long_name = info.long_name    # str type
website = info.website      # pydantic.HttpUrl type
```

## Contributing

This package is part of the larger `stonksapi` project. See the main README for contribution guidelines.

## License

This package follows the license of the parent `stonksapi` project.
