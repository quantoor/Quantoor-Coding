class Crypto_Breakout_Bot:
    def __init__(self, token, chat_id):
        import telegram
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.foundSymbols = {}  # maps found symbols to the timestamp when they are found. Used to avoid signaling the same symbol again before some time has passed
    def Start(self):
        import util
        import strategy
        allSymbols = util.get_all_symbols()
        print(allSymbols)
        import time
        while (True):
            for fsym in allSymbols:
                # ignore if already found this symbol
                if self.Already_Found(fsym):
                    continue
                # isConsolidating, isPumping = strategy.check_status(fsym)
                # print(fsym + " is consolidating: " + isConsolidating + ", is breaking out: " + isPumping)
                isConsolidating, isPumping = strategy.check_status_now(fsym)
                print(fsym + " is consolidating: " + isConsolidating + ", is breaking out: " + isPumping)
                if isConsolidating:
                    if isPumping:
                        self.bot.sendMessage(chat_id=self.chat_id, text=fsym + " is breaking out")
                        self.foundSymbols[fsym] = time.time()  # add the symbol to the found dict with the corresponding timestamp



    def Already_Found_Old(self, fsym):
        found = False
        for s in self.foundSymbols:
            if s == fsym:
                found = True
                break
        if found == False:
            return False
        First_timestamp = self.foundSymbols[fsym]
        SecondTimestamp = datetime.timestamp(datetime.now())
        dt = SecondTimestamp - First_timestamp
        less = dt < 3600
        return less


    # def Already_Found_New(self, fsym):
    #     found = False
    #     for s in self.foundSymbols:
    #         if s == fsym:
    #             found = True
    #             break
    #     if found == False:
    #         return False
    #     lastTimestamp = self.foundSymbols[fsym]  # last time this symbol was found
    #     timestampNow = time.time()
    #     dt = timestampNow - lastTimestamp  # seconds that have passed since this symbol was found
    #     return dt < 3600  # do not notify if already found in the last hour
    def Already_Found(self, fsym):
        found = False
        for s in self.foundSymbols:
            if s == fsym:
                found = True
                break
        if found == False:
            return False
        lastTimestamp = self.foundSymbols[fsym]  # last time this symbol was found
        timestampNow = time.time()
        dt = timestampNow - lastTimestamp  # seconds that have passed since this symbol was found
        less = dt < 3600  # do not notify if already found in the last hour
        return less




with open("private.txt", 'r') as f:
    token = f.readline().strip()
    chat_id = f.readline()



bot = CryptoBreakoutBot(token, chat_id)
    # bot.Start_1()
# bot.Start_2()

bot.Start()