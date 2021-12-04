from selenium import webdriver
import matplotlib.pyplot as plt
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path="geckodriver")

#aller sur la page de trade SAND/USDT
driver.get("https://www.binance.com/fr/trade/ADA_EUR?layout=pro")

time.sleep(60)

#cliquer sur market (pour acheter et vendre pile au prix du marché)
market = driver.find_element_by_css_selector("span.item.css-1knxu4r")
market.click()
#cliquer sur 15Minutes
#temps = driver.find_element_by_id("15m")
#temps.click()

time.sleep(1)


trade=1
t=0
tprime=0
achat=0
vente=0
prix=[]
temps=[]
#ma7=[]
#ma25=[]
#ma3=[]
rsi=[]
date=[]
ema3=[]
ema7=[]
macd=[]

jachete=0
jevends=0

while trade:

    indicators = driver.find_elements_by_css_selector("span.default-label-box")
    heure = float(indicators[0].text[14:16])
    date.append(heure)
    plt.pause(0.5)

    if tprime>0:
        if date[tprime-1]!=date[tprime]:

            #recuperer le prix de la crypto choisie
            chaine = driver.find_element_by_class_name("nowPrice")
            val=chaine.text[0:7]
            price=float(val)
            prix.append(price)

            #MA7=float(indicators[14].text)
            #ma7.append(MA7)
            #MA25=float(indicators[16].text)
            #ma25.append(MA25)
            #MA3=float(indicators[18].text)
            #ma3.append(MA3)
            EMA7=float(indicators[34].text)
            ema7.append(EMA7)
            EMA3=float(indicators[38].text)
            ema3.append(EMA3)
            MACD = float(indicators[56].text)
            macd.append(MACD)
            RSI=float(indicators[58].text)
            rsi.append(RSI)
            temps.append(t)

            if t>1:
                if (ema3[t-1]<ema3[t] and rsi[t-1]<30 and rsi[t-1]<rsi[t] and achat==0) or (rsi[t-1]<20 and rsi[t]>rsi[t-1] and achat==0):
                    print("j'achète à",price,"t=", t)
                    jachete=1
                if ema3[t-1]>ema3[t] and rsi[t-1]>70 and rsi[t-1]>rsi[t] and achat==1:
                    print("je vends à",price,"t=", t)
                    jevends=1

            #si pas de crypto achetee, il faut en acheter
            if achat==0 and jachete==1 and vente==0:

                usdt = driver.find_elements_by_css_selector("span.css-k4h8bj")[0]

                case = driver.find_element_by_id("FormRow-BUY-total")
                case.click()
                case.send_keys(usdt.text[0:6])

                #case ACHETER
                ACHETER = driver.find_element_by_id("orderformBuyBtn")
                ACHETER.click()

                achat=1
                jachete=0

            #si crypto achetee et pas vendue, il faut la vendre
            if achat==1 and vente==0 and jevends==1:

                vendre = driver.find_element_by_css_selector("div.css-b2gwzx")
                vendre.click()
                time.sleep(2)
                eth = driver.find_elements_by_css_selector("span.css-k4h8bj")[1]
                #case 100%
                case1 = driver.find_element_by_id("FormRow-SELL-quantity")
                case1.click()
                case1.send_keys(eth.text[0:6])
                #case VENDRE
                VENDRE = driver.find_element_by_id("orderformSellBtn")
                VENDRE.click()

                vente=1
                achat=0
                jevends=0

            #si crypto vendue, il faut en racheter
            if vente==1 and achat==0 and jachete==1:

                acheter = driver.find_element_by_css_selector("div.css-b2gwzx")
                acheter.click()
                time.sleep(2)
                usdt = driver.find_elements_by_css_selector("span.css-k4h8bj")[0]

                case = driver.find_element_by_id("FormRow-BUY-total")
                case.click()
                case.send_keys(Keys.ARROW_RIGHT, Keys.ARROW_RIGHT, Keys.ARROW_RIGHT, Keys.ARROW_RIGHT, Keys.ARROW_RIGHT, Keys.ARROW_RIGHT,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, usdt.text[0:6])
                #case ACHETER
                ACHETER = driver.find_element_by_id("orderformBuyBtn")
                ACHETER.click()

                vente=0
                achat=1
                jachete=0

            #tracer le prix de la crypto choisie à chaque intervalle de temps choisi
            #plt.subplot(221)
            #plt.plot(temps, ma7, color="b")
            #plt.plot(temps, ma25, color="g")
            #plt.plot(temps, rsi, ".",color="g")
            #plt.title("RSI")

            #plt.subplot(222)
            #plt.plot(temps, macd, ".",color="r")
            #plt.title("MACD")

            #plt.subplot(212)
            #plt.plot(temps, ema7, ".",color="b")
            #plt.plot(temps, prix, ".",color="r")
            #plt.plot(temps, pourcentage, color="g")
            #plt.title("EMA(7)")

            t+=1

    tprime+=1

#plt.show()

