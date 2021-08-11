#!/usr/bin/env python
import pandas as pd
import requests
from bs4 import BeautifulSoup



BASE_URL = "https://etherscan.io/address/"

headers = {
    'user-agent' :  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36'
    }



def main():
    filename = 'example.csv'
    df = pd.read_csv(filename)
   
    bin = []
    for index, row in df.iterrows():
        
        address = row['address']

        while True:
            try:
                
                url = BASE_URL + address + "#code"
                page = requests.get(url, headers=headers)
                print(page)
                
                if (page.status_code != 200):
                    print("page status code is: ", page.status_code)
                    
                else :
                    print("Interaction ", index)
                    soup = BeautifulSoup(page.text, "html.parser")

                    if soup.find("div", { "id": "verifiedbytecode2" }) is None:
                        print("No verified bytecode")
                        print(address)

                        if soup.find("pre", { "class": "wordwrap" }) is None:
                            print("No bytecode")
                            # break
                             
                        else:
                            bin.append( soup.find("pre", { "class": "wordwrap" }).text )
                            break

                    else: 
                        print("Verified bytecode")
                        bin.append(soup.find("div", { "id": "verifiedbytecode2" }).text)
                        break
                print("_____________________________________________________________________________")
                
            except Exception: continue
    dataframe = pd.DataFrame(bin) 
    dataframe.to_csv('new_csv2.csv')


if __name__ == "__main__":
    main()