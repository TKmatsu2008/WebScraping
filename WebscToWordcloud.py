import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer #品詞解析、形態素解析
from PIL import Image
import numpy as np
 
def scraping():
    reading_url= "https://hentai-matome.net/I0000802"
    html=requests.get(reading_url)#htmlにはそのresponseがhtml.textにはhtmlファイルそのものが入っている
    parse=BeautifulSoup(html.text,'html.parser')#beautiflSoupの引数は(解析対象,解析器)
    parse_tag=parse.find_all("h2")#どのhtmlタグをスクレイピングするか
    topics=[]
    for text_data in parse_tag:
        topics.append(text_data.getText())#text_dataは<p>うんこ</p>みたいなかんじであるのでそこからオブジェクト(うんこ)だけを抜き取るのがgetText
    return topics
 
def purse():
    tokenizer=Tokenizer()
    words=[]
    topics=scraping()
    # #画像読み込み(白黒のみ)
    # mask = np.array(Image.open('heart0509.jpg'))
    
    #画像を円にする
    mask_ary = np.zeros(shape=(400,400))
    for i in range(400):
        for j in range(400):
            if (i-200)**2+(j-200)**2>180**2:
                mask_ary[i,j]=255
    mask_ary=mask_ary.astype(int)
    
    for word in topics:
        tokens=tokenizer.tokenize(word)#tokenは形態素解析した二重配列
        for token in tokens:
            pos=token.part_of_speech.split(',')[0]#品詞の形態素解析配列の,で区切ったときの品詞の分類部分を抜き取る( 東京 名詞,固有名詞,地域,一般,*,*,東京,トウキョウ,トーキョー)
            if pos in ['名詞']:
                words.append(token.base_form)
    text=' '.join(words)
    

    wordcloud=WordCloud(
        mask = mask_ary,
        background_color='white',
        contour_width=1,
        contour_color='green',
        font_path='./BIZ-UDGothicR.ttc',
        ).generate(text)
    wordcloud.to_file('./result.png')
 
purse()