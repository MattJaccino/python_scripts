#!/usr/bin/python3

import os
from yahoo_fin import stock_info
from datetime import datetime


class stock:
    def __init__(self, ticker, buy_price, q):
        self.name = ticker
        self.q = q
        self.bp = buy_price
        self.cp = stock_info.get_live_price(ticker)
        # info relative to entire stock purchase
        self.bval = self.q * self.bp
        self.cval = self.q * self.cp
        self.netval = net(self.bval, self.cval)
    def output_str(self):
        # For individual stock changes, not entire purchase
        return f"{self.name}\t\t"\
               f"{self.q}\t\t"\
               f"{self.bp} ({self.bval:.2f})\t\t"\
               f"{self.cp:.2f} ({self.cval:.2f})\t\t"\
               f"{net(self.bp,self.cp)} ({self.netval})"


def net(buy, curr):
    return f"{curr-buy:.2f}" if curr-buy < 0 else "+"+f"{curr-buy:.2f}"


def check_ticker(ticker):
    try:
        stock_info.get_data(ticker)
        valid = True
    except:
        valid = False
    return valid


def check_price(price):
    try:
        float(price)
        valid = True
    except ValueError:
        valid = False
    return valid


def check_quan(q):
    try:
        int(q)
        valid = True
    except ValueError:
        valid = False
    return valid


def make_list():
    stock_list = []
    uin = input("Enter the ticker of the stock you purchased, or press ENTER to continue.\n")
    while uin:
        ticker = uin.upper()
        while not check_ticker(ticker): 
            print(f"'{ticker}' is invalid.  Please try again.")
            ticker = input("Enter the ticker of the stock you purchased.\n")

        buy_price = input(f"At what price did you purchase {ticker}?\n")
        while not check_price(buy_price):
            print(f"'{buy_price}' is an invalid price.  Please try again.")
            buy_price = input(f"At what price did you purchase {ticker}?\n")
        # Convert to float after verification
        buy_price = float(buy_price)

        quan = input(f"How many shares of {ticker} did you purchase?\n")
        while not check_quan(quan):
            print(f"'{quan}' is an invalid quantity.  Please try again.")
            quan = input(f"How many shares of {ticker} did you purchase?\n")
        # Convert to int after verification
        quan = int(quan)

        stock_list.append((ticker, buy_price, quan))
        uin = input("Enter the ticker of the stock you purchased, or press ENTER to continue.\n")
    return stock_list


def ask_for_changes():
    uin = input("Would you like to:\n"
                "(1) use the data saved in 'stocks.csv', or\n"
                "(2) create a new file?\n\n"
                "Enter '1' or '2'\n")
    while uin != '1' and uin != '2':
        uin = input("Please enter '1' or '2'.\n")
    # Essentially its asking 'Do you want to use the saved data?'
    return True if uin == '1' else False

def ask_for_updates():
    uin = input("Would you like to:\n"
                "(1) use data as-is, or\n"
                "(2) add new items?\n\n"
                "Enter '1' or '2'\n")
    while uin != '1' and uin != '2':
        uin = input("Please enter '1' or '2'.\n")
    # Essentially its asking 'Do you want to add to the data?'
    return False if uin == '1' else True



#*****************************************************************************




# Keep list as truple of ([TICKER], [PRICE WHEN BOUGHT], [QUANTITY BOUGHT])



def main():   
    # Check if data is already stored
    if os.path.isfile("./stocks.csv"):
        if ask_for_changes():
            use_new = False
            stock_list = []
            stock_doc_r = open("./stocks.csv", "r")
            for line in stock_doc_r:
                t,p,q = line.split(',')
                ticker = t[2:-1]
                bp = p[1:]
                quan = q[1:-2]
                stock_list.append((ticker, float(bp), int(quan)))
            stock_doc_r.close()
            if ask_for_updates():
                stock_doc_a = open("./stocks.csv", "a")
                new_stock_list = make_list()
                for s in new_stock_list:
                    stock_doc_a.write(str(s)+'\n')
                stock_list += new_stock_list
                stock_doc_a.close()
        else:
            use_new = True
    else:
        use_new = True

    if use_new:
        stock_list = make_list()
        stock_doc = open("./stocks.csv", "w")
        for s in stock_list:
            stock_doc.write(str(s)+'\n')
        stock_doc.close()
    sd = {} # Stock dict
    # Create objects for each stock to hold info
    for s in stock_list:
        sd[s] = stock(s[0], s[1], s[2])



    output = "Stock\t\tQuantity\tBought\t\t\tCurrent\t\t\tNet\n"
    now = datetime.today().strftime("%m/%d/%y  %H:%M")
    print(f"\nSTOCK UPDATE FOR {now}:\n","*"*96,sep='')
    print(output)

    tbv = 0
    tcv = 0
    for s in sorted(sd.keys()):
        tbv += sd[s].bval
        tcv += sd[s].cval
        print(sd[s].output_str())

    print("*"*96)
    totals = f"TOTAL BUY VALUE: {tbv:.2f}\tTOTAL CURRENT VALUE: {tcv:.2f}\tTOTAL NET CHANGE: {net(tbv, tcv)}\n"
    print(totals)

main()

