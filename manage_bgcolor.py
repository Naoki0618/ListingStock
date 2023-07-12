class ManageBgColor():
    

    def highlight_ner_row(x):
        color = [""] * len(x)  # 初期化
        tmp = float(x['時価総額(億円)'])
        if tmp >= 250:
            color[3] = "background-color: moccasin;"
            
        tmp = float(x['流通株式数'])
        if tmp >= 2000000:
            color[4] = "background-color: moccasin;"
            
        tmp = float(x['流通株式時価総額(億円)'])
        if tmp >= 100:
            color[5] = "background-color: moccasin;"
            
        tmp = float(x['流通株式比率'])
        if tmp >= 0.35:
            color[6] = "background-color: moccasin;"

        if x['収益基盤'] == "○":
            color[7] = "background-color: moccasin;"
        return color