import matplotlib.pyplot as plt
import pandas as pd
from sec_api import XbrlApi

from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings


def show_plot(ticker):
    # print("in function")
    #find the url of the 10k filing using sec-downloader 
    #extract income statements from it using SEC API
    #Plot the income statements
    
    dl=Downloader("mycompanyname", "xyz@email.com")
    metadatas= dl.get_filing_metadatas(RequestedFilings(ticker,"10-K",limit=1))
    for filings in metadatas:
        url=filings.primary_doc_url
    API_KEY="3ee5738d347017fcd92864dd4aa3cc1264fd42d0ba976a0c2d7a28f953e313b1"
    # print(url)
    xbrlApi = XbrlApi(API_KEY)
    xbrl_json = xbrlApi.xbrl_to_json(htm_url=url)
    # print(xbrl_json["StatementsOfIncome"])
    income_statement = get_income_statement(xbrl_json)


    indices_to_include = [0,1,2,6,10]  # 1st, 4th, and 5th entries
    # Filter the DataFrame based on the indices
    filtered_df = income_statement.iloc[indices_to_include]
    ax = filtered_df.plot(kind='bar', figsize=(10, 6))
    ax.set_xlabel(f"10-K Filing Data For {ticker}")
    ax.set_ylabel('Amount')
    ax.set_title('Income Statement')
    # plt.xticks(rotation=0,)
    plt.xticks([0, 1, 2,3,4], ['Total net sales', 'Total cost of sales', 'Gross margin','Operating income','Net income'],   rotation=20)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.savefig(f"static/Image/{ticker}.jpeg")


def get_income_statement(xbrl_json):
    income_statement_store = {}

    # iterate over each US GAAP item in the income statement
    for usGaapItem in xbrl_json['StatementsOfIncome']:
        values = []
        indicies = []

        for fact in xbrl_json['StatementsOfIncome'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact:
                index = fact['period']['startDate'] + '-' + fact['period']['endDate']
                # ensure no index duplicates are created
                if index not in indicies:
                    # Convert value to numeric
                    value = pd.to_numeric(fact['value'])
                    values.append(value)
                    indicies.append(index)

        income_statement_store[usGaapItem] = pd.Series(values, index=indicies)

    income_statement = pd.DataFrame(income_statement_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date range
    return income_statement.T

