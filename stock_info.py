import yfinance as yf


class StockInfo:
    # 銘柄情報を取得
    def __init__(self, ticker):
        self.ticker = ticker
        stock = yf.Ticker(str(ticker) + ".T")
        self.name = stock.info.get("longName")
        self.score = 5

        try:
            # 株価を取得
            self.regularMarketPreviousClose = stock.info.get("regularMarketPreviousClose")
        except:
            self.regularMarketPreviousClose = 0

        # 流通株式数を取得
        try:
            self.float_shares = stock.info.get("floatShares")
            if self.float_shares == None:
                self.float_shares = 0
        except:
            self.float_shares = 0

        # 流通株式時価総額
        try:
            self.float_shares_value = self.regularMarketPreviousClose * self.float_shares
        except:
            self.float_shares_value = 0

        # 発行済株式総数を取得        
        try:
            self.outstanding_shares = stock.info.get("sharesOutstanding")
        except:
            self.outstanding_shares = 0

        # 流通株式比率を計算
        try:
            self.float_ratio = self.float_shares / self.outstanding_shares
        except:
            self.float_ratio = 0

        # 売買高を取得
        try:
            self.regular_market_volume = stock.info.get("regularMarketVolume")
        except:
            self.regular_market_volume = 0

        # 売買代金を取得
        try:
            self.trading_value = (
            self.regular_market_volume * self.regularMarketPreviousClose
        )
        except:
            self.trading_value = 0
            
        # 売上高を取得
        try:
            self.revenue = stock.info.get("totalRevenue")
        except:
            self.revenue = 0

        # 時価総額を取得
        try:
            self.market_cap = stock.info.get("marketCap")
        except:
            self.market_cap = 0

        # 純資産額を取得
        try:
            self.total_assets = stock.info.get("TotalAssets")
        except:
            self.total_assets = 0

    def score_minus(self):
        # 流通株式数２０，０００単位以上
        if self.float_shares < 2000000:
            self.score -= 1

        # 流通株式時価総額１００億円以上
        if self.float_shares_value < 10000000000:
            self.score -= 1

        # 時価総額２５０億円以上
        if self.market_cap < 25000000000:
            self.score -= 1

        # ３５％以上
        if round(self.float_ratio,2) < 0.35:
            self.score -= 1

        # 売上⾼１００億円以上かつ時価総額１，０００億円以上
        if self.revenue < 10000000000 or self.market_cap < 100000000000:
            self.score -= 1

        return self.score

    # 売上⾼１００億円以上かつ時価総額１，０００億円以上
    def is_revenue_market_cap(self):
        flg = ""
        if self.revenue > 10000000000 and self.market_cap > 100000000000:
            flg = "○"
        return flg
