import streamlit as st
import pandas as pd
from stock_info import StockInfo as si
from manage_bgcolor import ManageBgColor as bg


@st.cache_data
def create_dataframe(stock_df):
    stocks = []
    # 値の取得と表示
    values = stock_df[0].tolist()
    for value in values:
        stocks.append(value)

    # データフレームの作成
    data = {
        "銘柄コード": [],
        "銘柄名": [],
        "株価": [],
        "時価総額(億円)": [],
        "流通株式数": [],
        "流通株式時価総額(億円)": [],
        "流通株式比率": [],
        "収益基盤": [],
        "スコア": [],
    }
    df = pd.DataFrame(data, index=[])

    progress_text = "Operation in progress. Please wait. total count:" + str(
        len(stocks)
    )
    percent_complete = 0.0
    my_bar = st.progress(0, text=progress_text)

    for stock in stocks:
        percent_complete += 1 / len(stocks)
        if percent_complete < 1:
            my_bar.progress(percent_complete, text=progress_text)
        try:
            stock_info = si(stock)
            stock_info.score_minus()

            new_stock = pd.DataFrame(
                {
                    "銘柄コード": [str(stock_info.ticker)],
                    "銘柄名": [stock_info.name],
                    "株価": [stock_info.regularMarketPreviousClose],
                    "時価総額(億円)": [format(stock_info.market_cap / 100000000, ".2f")],
                    "流通株式数": [stock_info.float_shares],
                    "流通株式時価総額(億円)": [
                        format(
                            stock_info.float_shares_value / 100000000,
                            ".2f",
                        )
                    ],
                    "流通株式比率": [format(stock_info.float_ratio, ".2f")],
                    "収益基盤": stock_info.is_revenue_market_cap(),
                    "スコア": [str(stock_info.score)],
                }
            )
            df = pd.concat([df, new_stock], ignore_index=True)

        except Exception as e:
            print(e)
            # pass

        my_bar.empty()

    return df


st.set_page_config(
    layout="wide",
)

# CSVファイルの読み込み
stock_df = pd.read_csv("stock.csv", header=None)
df = create_dataframe(stock_df)
df["時価総額(億円)"] = pd.to_numeric(df["時価総額(億円)"])
data_f = df
# データフレームの表示
data_f = df.style.apply(bg.highlight_ner_row, axis=1)
st.dataframe(data_f)
st.download_button(
    label="Download data as CSV",
    data=df.to_csv().encode("shift-jis"),
    file_name="stock_data.csv",
    mime="text/csv",
)
