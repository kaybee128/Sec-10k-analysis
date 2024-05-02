from flask import Flask, request
from sec10_process import find_insights
app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML template
    return app.send_static_file('index.html')

@app.route('/process_button1', methods=['GET'])
def process_button1():
    # Get the ticker symbol from the query parameters
    ticker_symbol = request.args.get('tickerSymbol')
    ans= find_insights(ticker_symbol,1)
    # Process the ticker symbol (you can perform any required operations here)
    # For demonstration, we simply print the ticker symbol
    print(f"Ticker Symbol: {ticker_symbol}")
    
    # Return a response to the frontend
    return f"{ans}"

@app.route('/process_button2', methods=['GET'])
def process_button2():
    # Get the ticker symbol from the query parameters
    ticker_symbol = request.args.get('tickerSymbol')
    ans= find_insights(ticker_symbol,2)
    # Process the ticker symbol (you can perform any required operations here)
    # For demonstration, we simply print the ticker symbol
    print(f"Ticker Symbol: {ticker_symbol}")
    
    # Return a response to the frontend
    return f"{ans}"

@app.route('/process_button3', methods=['GET'])
def process_button3():
    # Get the ticker symbol from the query parameters
    ticker_symbol = request.args.get('tickerSymbol')
    ans= find_insights(ticker_symbol,3)
    # Process the ticker symbol (you can perform any required operations here)
    # For demonstration, we simply print the ticker symbol
    print(f"Ticker Symbol: {ticker_symbol}")
    
    # Return a response to the frontend
    return f"{ans}"




if __name__ == '__main__':
    app.run(debug=True)
