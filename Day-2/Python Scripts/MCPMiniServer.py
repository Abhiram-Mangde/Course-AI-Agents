from mcp.server import Server, tool

server = Server("stock-server")

@tool
def lookup_stock(symbol: str):
    """
    Fetch stock price.
    """
    price = 178.32  # placeholder
    return {"symbol": symbol, "price": price}

if __name__ == "__main__":
    server.run()
