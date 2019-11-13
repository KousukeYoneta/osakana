#"ウィンドウ表示"
import sys, pygame, random, time, pygame.mixer
from pygame.locals import QUIT, KEYDOWN

pygame.mixer.pre_init(44100, -16, 2, 2048) # なぜこうするのかは誰にもわからない笑
pygame.mixer.init()
pygame.init()                                               # pygameモジュールを初期化する関数、pygameを使うアプリでは最初に呼び出す必要があります（p.79）

SURFACE = pygame.display.set_mode((1000,600))
FPSCLOCK = pygame.time.Clock()


class sakana:
    def __init__(self, yomi, kanji, hiragana, yomi2, keyalpha):
        self.yomi = yomi
        self.kanji  = kanji
        self.hiragana = hiragana
        self.yomi2 = yomi2
        self.keyalpha = keyalpha
#  オブジェクト生成→それをリスト何文字目までいったらもうyomi2に変わらないかプロパティ作ったほうがいいかね。
obj1 = sakana("sawara", "鰆", "さわら","",100)
obj2 = sakana("kajika", "鮖", "かじか","kazika",100)
obj3 = sakana("sake", "鮭", "さけ","",100) 
obj4 = sakana("aji", "鯵", "あじ","azi",100) 
obj5 = sakana("sannma", "秋刀魚", "さんま", "sanma",100) 
obj6 = sakana("yamame", "山女魚", "やまめ","",100) 
obj7 = sakana("hirame", "鮃", "ひらめ","",100)
obj8 = sakana("dozyou", "鰌", "どじょう","dojou",3)
obj9 = sakana("ica", "烏賊", "いか","ika",100)
obj10 = sakana("funa", "鮒", "ふな","huna",100)

obj_list = [obj1,obj2,obj3,obj4,obj5,obj6,obj7,obj8,obj9,obj10]
random.shuffle(obj_list)
time_sta = time.time()
time_end = 0
tim = 0

# 効果音
se1 = pygame.mixer.Sound("seikai.ogg")

# 文字を生成する関数
def moji(font,size,text,hutoji,color,iti):
    font = pygame.font.Font(font, size)
    hyouji = font.render(text, hutoji, color)     
    hyouji_rect = hyouji.get_rect()
    hyouji_rect.center = iti          
    SURFACE.blit(hyouji,hyouji_rect)

 # 正しいアルファベットを打てば次のアルファベットへ、そして効果音をならす
def maru():
    global alphabet
    alphabet += 1
    se1.play()
  

def main():
    
    global alphabet
    alphabet = 0  
    index = 0
    enterindex = 0
    yomi2index = 0
    
    # クリアしたら
    def ending():
    # 時間計測終了
        global time_end,tim    # これがないと、「宣言される前に参照されています」的なエラーに
        # globalって「中から書き換えられますよ」って意味と思ってたけど「書き換えられる」＝「外の変数を使いますよ」的な意味なんじゃないかな。
        # やからあとからtim = があっても新たなローカル変数の宣言じゃなくて、「外のグローバル変数timを「書き換える」」とインタプリタが解釈してくれるのかな。
        if bool(time_end) == False:
            time_end = time.time()
            tim = time_end - time_sta    
        
        SURFACE.fill((255,255,255))
        if tim < 30:
            moji("IPAexfont00401/ipaexg.ttf",  72, "もしかして製作者？", True, (200,10,10),  (500,200)) 
        elif tim < 60:
            moji("IPAexfont00401/ipaexg.ttf",  72, "まあまあやるやん", True, (200,10,10),  (500,200))    
        else :
            moji("IPAexfont00401/ipaexg.ttf",  72, "まだまだやな", True, (200,10,10),  (500,200))
        # クリア時間の表示
        moji("IPAexfont00401/ipaexg.ttf",  72,  "所要時間："+ str(round(tim, 1)) + "秒",  True,  (200,10,10),  (500,400) )
        pygame.display.update()
    
    
    """main routine"""    
    while True:
        
        # クリアしたら
        if index == len(obj_list):
            ending()
            
        else:
            SURFACE.fill((255,255,255))
            # まず漢字を表示
            moji("IPAexfont00401/ipaexg.ttf",120,obj_list[index].kanji,True,(0,128,128),(500,150) )
            
            # 経過時間を表示
            global time_end,tim   
            time_end = time.time()
            tim = time_end - time_sta
            moji("IPAexfont00401/ipaexg.ttf",54,"経過時間",True,(0,128,128),(300,450) )
            moji("IPAexfont00401/ipaexg.ttf",54,str(round(tim, 1)),True,(0,128,128),(300,500) )
                

            #右下に正解したものを表示したい
            if index != 0:
                moji("IPAexfont00401/ipaexg.ttf",  42, "前の問題の答え",  True,  (128,128,128),   (800,380))
                moji("IPAexfont00401/ipaexg.ttf",  72, obj_list[index-1].kanji,  True,  (128,128,128),   (800,450))   # 漢字
                moji("IPAexfont00401/ipaexg.ttf",  42, obj_list[index-1].hiragana, True, (128,128,128),    (800,520) ) # よみ

            # 正解のアルファベットは表示していく
            if alphabet != 0:
                alphahyoujis = []                                   
                for i in range(alphabet):
                    font = pygame.font.Font("IPAexfont00401/ipaexg.ttf", 72)
                    if yomi2index == 0:
                        alphahyouji = font.render(obj_list[index].yomi[i], True, (0,128,128))      # pythonはリストをこんなふうに使えるんか・・・     
                        alphahyouji_rect = alphahyouji.get_rect()
                        alphahyouji_rect.center = (550-len(obj_list[index].yomi)*35 + i*70,  300)   
                        alphahyoujis.append(alphahyouji)      # この部分があるから関数は使わんことにした
                        SURFACE.blit(alphahyoujis[i],alphahyouji_rect)
            # enterが押されていれば答えを表示
            if enterindex == 1:
                moji("IPAexfont00401/ipaexg.ttf",  42, obj_list[index].hiragana,  True,  (128,128,128),   (500,70) )
            pygame.display.update() 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:  
  
                if chr(event.key) == obj_list[index].yomi[alphabet] :                  #　もし表示されている漢字の次のアルファベットと一致したら
                    maru()
                elif event.key == 13: # エンターは１３らしい
                    enterindex = 1   
                # nnの処理とjiとzi 
                elif len(obj_list[index].yomi2) != 0 and alphabet < obj_list[index].keyalpha:# keyalphaがないと、鰌で、dozを打ってoを打てばyomi2になっちゃう 
                    if chr(event.key) == obj_list[index].yomi2[alphabet]:
                        maru()
                        obj_list[index].yomi = obj_list[index].yomi2 
                if alphabet == len(obj_list[index].yomi):           #　これここの階層にないとうまくいかん
                    index += 1    
                    alphabet = 0                                                          
                    enterindex = 0
        FPSCLOCK.tick(200)         # 多分これはwhileTrue内第１インデントにないと                                       

if __name__ == "__main__":
    main()