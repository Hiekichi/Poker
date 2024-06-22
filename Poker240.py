import pyxel

D = [[0,1],[0,-1],[1,0],[-1,0]]  ## 下、上、右、左
LAXIS = [pyxel.GAMEPAD1_AXIS_LEFTY,pyxel.GAMEPAD1_AXIS_LEFTY,
         pyxel.GAMEPAD1_AXIS_LEFTX,pyxel.GAMEPAD1_AXIS_LEFTX]
LAXIS_RANGE = [[10000,36000],[-36000,-10000],[10000,36000],[-36000,-10000]]
GPAD = [pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]

STATE_WAIT_GAMESTART = 0
STATE_WAIT_CHANGE = 1
STATE_WAIT_NEXTGAME = 2

state = STATE_WAIT_GAMESTART
mycard = []

YAKU_ROYAL_FLUSH   = 0
YAKU_STAIGHT_FLUSH = 1
YAKU_FOUR_CARD     = 2
YAKU_FULLHOUSE     = 3
YAKU_FLUSH         = 4
YAKU_STRAIGHT      = 5
YAKU_THREE_CARD    = 6
YAKU_TWO_PAIRS     = 7
YAKU_ONE_PAIR      = 8
YAKU_HIGHCARD      = 9
YAKU_GETMONEY = [10000,5000,2500,900,600,400,300,200,100,0]
yaku = YAKU_HIGHCARD

class App():
    def __init__(self) -> None:
        pyxel.init(240,240,"Poker",fps=24)
        pyxel.load("card.pyxres")
        self.score = 500
        self.init_game()
        pyxel.run(self.update,self.draw)
    
    def init_game(self):
        self.yubi_x = 0
        self.yubi_y = 0
        self.kubarichuu_cnt = 0
        self.koukanchuu_cnt = 0
        self.gameover_cnt = 0
        self.init_cards()

    def init_cards(self):
        self.usednumber_flags = [0] * 52
        self.nums = [0,0,0,0,0]   # A:1  2~10:2~10  J:11 Q:12 K:13
        self.suits = [0,0,0,0,0]  # スペード:0  ハート:1  クラブ:2  ダイヤ:3
        self.change_flags = [0,0,0,0,0]
        for i in range(5):
            self.nums[i]  = pyxel.rndi(1,13)
            self.suits[i] = pyxel.rndi(0,3)
            while self.usednumber_flags[self.suits[i]*13+(self.nums[i]-1)]!=0:
                self.nums[i]  = pyxel.rndi(1,13)
                self.suits[i] = pyxel.rndi(0,3)
            self.usednumber_flags[self.suits[i]*13+(self.nums[i]-1)] = 1

    def card_change(self):
        for i in range(5):
            if self.change_flags[i] == 1:
                self.nums[i]  = pyxel.rndi(1,13)
                self.suits[i] = pyxel.rndi(0,3)
                while self.usednumber_flags[self.suits[i]*13+(self.nums[i]-1)]!=0:
                    self.nums[i]  = pyxel.rndi(1,13)
                    self.suits[i] = pyxel.rndi(0,3)
                self.usednumber_flags[self.suits[i]*13+(self.nums[i]-1)] = 1


    def update(self):
        global state

        ### ゲームオーバー中
        if self.gameover_cnt > 0:
            self.gameover_cnt -= 1
            if self.gameover_cnt == 0:
                self.score = 500
                self.init_game()
                state = STATE_WAIT_CHANGE
                self.score -= 100
                self.kubarichuu_cnt = 25
            return
        ### ゲームオーバーの判定
        if self.score < 0:
            self.score = 0
            self.gameover_y = pyxel.rndi(0,8)
            self.gameover_cnt = 100
            pyxel.play(2,7)
            return

        ### ゲーム開始時のカード配り中の処理
        if self.kubarichuu_cnt > 0:
            if self.kubarichuu_cnt%5==0:
                pyxel.play(1,1)
            self.kubarichuu_cnt -= 1
            return
                
        ### カード交換中の処理
        if self.koukanchuu_cnt > 0:
            self.koukanchuu_cnt -= 1
            if self.koukanchuu_cnt == 0:
                self.card_change()
                self.yakuhantei()
                self.change_flags = [0,0,0,0,0]
                self.yubi_x = 0
                self.yubi_y = 0
                state = STATE_WAIT_NEXTGAME
            return
        
        ### ゲーム開始待ち
        if state == STATE_WAIT_GAMESTART:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                state = STATE_WAIT_CHANGE
                self.score -= 100
                self.kubarichuu_cnt = 25
            return

        ### ゲーム中（交換するカードを選んでるとき）のイベント処理
        if state == STATE_WAIT_CHANGE:
            ### 指の移動
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnp(pyxel.KEY_LEFT):
                self.yubi_x = max(self.yubi_x-1,0)
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.yubi_x = min(4,self.yubi_x+1)
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.KEY_UP):
                self.yubi_y = max(self.yubi_y-1,0)
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnp(pyxel.KEY_DOWN):
                self.yubi_y = min(1,self.yubi_y+1)
            ### Aボタン押下し
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE):
                ### 交換するカードを選ぶ
                if self.yubi_y == 0:
                    self.change_flags[self.yubi_x] = 1 - self.change_flags[self.yubi_x]
                    pyxel.play(0,0)
                ## カードを交換する
                else:
                    self.koukanchuu_cnt = 24
                    pyxel.play(0,6)
        ### ゲーム中（次のゲームを開始するボタンの押し待ち）のイベント処理
        elif state == STATE_WAIT_NEXTGAME:
            ### 指の移動
            ### Aボタン押下し
            if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE):
                self.init_game()
                state = STATE_WAIT_CHANGE
                self.score -= 100
                self.kubarichuu_cnt = 25


    def draw(self):
        pyxel.cls(6)
        ### 背景
        pyxel.blt(0,0, 1, 0,192, 240,64)
        pyxel.blt(0,64, 2, 0,192, 240,64)
        pyxel.blt(10,20,2,192,144,64,48,0)
        ### 持ち点数
        pyxel.blt(206,12, 0, 16,56, 23,5, 0)
        pyxel.blt(200+6*4,20, 0, 16,48, 3,5, 0)
        for i in range(1,6):
            n = self.score//(10**i)
            if n > 0:
                pyxel.blt(200+(6-i)*4,20, 0, 16+(n%10)*4,48, 3,5, 0)

        ### ゲームオーバー中の描画
        if self.gameover_cnt > 0:
            pyxel.bltm(64,152, 0, 0,576+64*self.gameover_y, 128,56, 8)
            return

        ### ゲーム開始待ちの描画
        if state == STATE_WAIT_GAMESTART:
            #pyxel.blt(80,140,2,192,144,64,48,0)
            #pyxel.text(80,160,"Push A-Button to Start!",pyxel.frame_count//2%15+1)
            pyxel.bltm(4,152, 0, 0,512, 232,56, 8)
            return

        ### ゲーム開始時のカード配り中の描画
        if self.kubarichuu_cnt > 0:
            ### カードの描画
            for i in range(min(5, 5 - self.kubarichuu_cnt//5)):
                    pyxel.blt(40+i*32,
                            148,
                            1,
                            192,
                            48,
                            32,
                            48)
            return

        ### カード交換中の描画
        if self.koukanchuu_cnt > 0:
            ### カードの描画
            for i in range(5):
                if self.change_flags[i] == 0:
                    pyxel.blt(40+i*32,
                            148,
                            self.suits[i]//2+1,
                            (self.nums[i]-1)%7*32,
                            self.suits[i]%2*96 + (self.nums[i]-1)//7*48,
                            32,
                            48)
                else:
                    pyxel.blt(40+i*32,
                            130,
                            1,
                            192,
                            48,
                            32,
                            48)
            ### ボタンの描画
            #pyxel.blt(90,210,0,0,64,64,16,8)
            return

        ### ゲーム中（交換するカードを選んでいる）の描画
        if state == STATE_WAIT_CHANGE:
            ### カードの描画
            for i in range(5):
                pyxel.blt(40+i*32,
                        148-self.change_flags[i]*18,
                        self.suits[i]//2+1,
                        (self.nums[i]-1)%7*32,
                        self.suits[i]%2*96 + (self.nums[i]-1)//7*48,
                        32,
                        48)
            ### ボタンの描画
            if sum(self.change_flags) == 0:
                pyxel.blt(90,210,0,0,112,64,16,8)
            else:
                pyxel.blt(90,210,0,0,64,64,16,8)
            ### 指の描画
            if self.yubi_y == 0:
                pyxel.blt(50+self.yubi_x*32,
                        190-self.change_flags[self.yubi_x]*18,
                        0,0,48,16,16,8)
            else:
                pyxel.blt(120,220,0,0,48,16,16,8)
        ### ゲーム中（次のゲームを開始するボタンの押し待ち）の描画
        elif state == STATE_WAIT_NEXTGAME:
            ### カードの描画
            for i in range(5):
                pyxel.blt(40+i*32,
                        148-self.change_flags[i]*18,
                        self.suits[i]//2+1,
                        (self.nums[i]-1)%7*32,
                        self.suits[i]%2*96 + (self.nums[i]-1)//7*48,
                        32,
                        48)
            ### 役とNEXTボタンの描画
            pyxel.bltm(28,200, 0, 0,yaku*24, 192,24, 8)
            ### 指の描画
            pyxel.blt(206,218,0,0,48,16,16,8)
        

    def yakuhantei(self):
        global mycard,yaku
        mycard = []
        ### 並び替えながらグルーバル変数に代入
        mycard.insert(0,[self.nums[0],self.suits[0]])
        for i in range(1,5):
            for pos in range(len(mycard)):
                break_flag = False
                if self.nums[i] < mycard[pos][0]:
                    break_flag = True
                    break
            if break_flag:
                mycard.insert(pos,[self.nums[i],self.suits[i]])
            else:
                mycard.append([self.nums[i],self.suits[i]])
        #print(mycard)
        ### 役の判定
        ### すべてのスーツが同じか？　※フラッシュの系統
        if mycard[0][1]==mycard[1][1] and mycard[1][1]==mycard[2][1] and \
            mycard[2][1]==mycard[3][1] and mycard[3][1]==mycard[4][1]:
            yaku = YAKU_FLUSH
            ### 更にA,10,J,Q,Kで構成されているか？
            if mycard[0][0]==1 and mycard[1][0]==10 and mycard[2][0]==11 and \
                mycard[3][0]==12 and mycard[4][0]==13:
                yaku = YAKU_ROYAL_FLUSH
            ### 若しくは一個づつ離れた数で並んでいるか？
            elif mycard[0][0]==mycard[1][0]-1 and mycard[1][0]==mycard[2][0]-1 and \
                  mycard[2][0]==mycard[3][0]-1 and mycard[3][0]==mycard[4][0]-1:
                yaku = YAKU_STAIGHT_FLUSH
        ### 4つのカードが同じ数か？　※フォーカード
        elif mycard[0][0]==mycard[3][0] or mycard[1][0]==mycard[4][0]:
            yaku = YAKU_FOUR_CARD
        ### 3つのカードと2つのカードがそれぞれ同じ数か？　※フルハウス
        elif (mycard[0][0]==mycard[2][0] and  mycard[3][0]==mycard[4][0]) or \
             (mycard[0][0]==mycard[1][0] and  mycard[2][0]==mycard[4][0]):
            yaku = YAKU_FULLHOUSE
        ### 一個づつ離れた数で並んでいるか？　※ストレート
        elif mycard[0][0]==mycard[1][0]-1 and mycard[1][0]==mycard[2][0]-1 and \
              mycard[2][0]==mycard[3][0]-1 and mycard[3][0]==mycard[4][0]-1:
                yaku = YAKU_STRAIGHT
        ### 3つのカードが同じ数か？　※スリーカード
        elif mycard[0][0]==mycard[2][0] or mycard[1][0]==mycard[3][0] or \
              mycard[2][0]==mycard[4][0]:
            yaku = YAKU_THREE_CARD
        ### 2つのカードが同じ数という組があるか？　※ワンペアかツーペアかペア無し（役無し）
        else:
            num = 0
            for i in range(4):
                if mycard[i][0]==mycard[i+1][0]:
                    num += 1
            if num == 2:
                yaku = YAKU_TWO_PAIRS
            elif num == 1:
                yaku = YAKU_ONE_PAIR
            else:
                yaku = YAKU_HIGHCARD

        #print(yaku)
        self.score += YAKU_GETMONEY[yaku]
        if yaku == YAKU_HIGHCARD:
            pyxel.play(1,3)
        elif yaku == YAKU_ONE_PAIR:
            pyxel.play(1,4)
        else:
            pyxel.play(1,2)
            
App()