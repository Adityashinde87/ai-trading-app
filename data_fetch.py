from SmartApi import SmartConnect
import pyotp
import pandas as pd
import config

def get_data():
    try:
        totp = pyotp.TOTP(config.TOTP_SECRET).now()
        smartApi = SmartConnect(api_key=config.API_KEY)

        smartApi.generateSession(
            config.CLIENT_ID,
            config.PASSWORD,
            totp
        )

        ltp = smartApi.ltpData("NSE", "RELIANCE-EQ", "2885")
        price = ltp["data"]["ltp"]

        df = pd.DataFrame({
            "close": [price]
        })

        return df

    except Exception as e:
        print("Error in API:", e)
        return None