import  requests , tkinter as tk , urllib , os , webbrowser , re
from  bs4    import BeautifulSoup
from  tkinter  import ttk
from  tkinter  import Label
from  tkinter  import LabelFrame
from  tkinter  import Button
from  tkinter  import messagebox
from  tkinter  import Canvas
from  PIL   import Image , ImageTk

#==================================================================================

def Request_url(url):
	try:
		r = requests.get(url)
		r.raise_for_status() #判斷http回應的狀態碼是否為200
		r.encoding = 'utf-8' #改變編碼方式避免出現亂碼
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		pass
	return soup


def Show_Movie_Img(url):

	soup = Request_url(url)
	img_url    = soup.find('div', class_= 'movie_intro_foto').img.get('src')#圖片網址
	movie_name = soup.find('h1').get_text()   #電影名稱
	img_name  = movie_name + '.png'     #圖片名稱
	file_path = "img"
	img_path  = file_path  + '/' + img_name   #圖片的路徑

	if not os.path.exists(file_path):  #資料夾不存在就建立
		os.mkdir(file_path)

	if not os.path.exists(img_path):   #圖片  不存在就建立
		urllib.request.urlretrieve(img_url , img_path)

	try:
		img = Image.open(img_path)  #打開圖片
		img.thumbnail((250,300))   #改變大小
		img.save(img_path)     #儲存圖片
		photo = ImageTk.PhotoImage(img) #讀取圖片
		CV.create_image(0 , 0 , anchor = 'nw', image = photo )#放置圖片
	except(OSError):
		messagebox.showerror(title = 'OS Error' , message = '儲存格式錯誤')

	UI.mainloop()


def Show_Movie_Text(url):

	detail = []
	soup = Request_url(url)

	movie_name  = soup.find('h1').get_text() #得到電影名稱
	detail.append('片　　名：' + movie_name)    #添加電影名稱

	detail_tag  = soup.find('div' , class_ = 'movie_intro_info_r').find_all('span')
	for d in detail_tag:
		detail.append(d.get_text())

	director  = soup.select('div.movie_intro_list')[0].get_text() #導演
	actor  = soup.select('div.movie_intro_list')[1].get_text() #演員
	director  = re.sub("[' ','\n']" , '' , director) #將空白.換行符號刪除
	actor  = re.sub("[' ','\n']" , '' , actor)
	d1 = detail.index('導演：')  #紀錄位置
	a1 = detail.index('演員：')
	detail.remove('導演：')   #刪除
	detail.remove('演員：')
	d2 = '導　　演：' + director     #合併
	a2 = '演　　員：\n' + actor
	detail.insert(d1,d2)     #重新插入
	detail.insert(a1,a2)

	if '官方連結：' in detail:  #有就刪除
		detail.remove('官方連結：')


	#--------------------------------

	if len(detail) == 6 :    #無IMDb分數
		t1.config(text = detail[0])
		t2.config(text = detail[1])
		t3.config(text = detail[2])
		t4.config(text = detail[3])
		t5.config(text = '')
		t6.config(text = detail[4])
		t7.config(text = detail[5])

	elif len(detail) == 7 :    #有IMDb分數
		for i in range(len(detail)):
			globals()['t' + str(i+1)].config(text = detail[i])

	elif len(detail) > 7:
		del detail[7:]
		for i in range(len(detail)):
			globals()['t' + str(i+1)].config(text = detail[i])


def Show_Movie_Data(event):

	CV.delete("all")#清除畫布
	for i in range(7):
		globals()['t' + str(i+1)].config(text = '')#清除內容

	option_movie = tree.item(tree.selection()).get('text')#提取key(text)的value(電影介紹連結)


	if not option_movie == '':
		intr_link_but.config(command = lambda:  webbrowser.open(option_movie) , state = 'normal')

		Show_Movie_Text(option_movie) #顯示電影資料
		Show_Movie_Img(option_movie) #顯示電影圖片

	elif option_movie == '': #沒有連結就跳出錯誤
		intr_link_but.config(state = 'disabled')
		messagebox.showerror(title = 'url Error' , message = 'Not Found url')


#==================================================

def Clear():  #清空  畫布/文字/表格/選單/按鈕
	global CV  #使用變數
	CV.delete("all")
	for i in range(7):
		globals()['t' + str(i+1)].config(text = '')
	range_label.config(text = '')
	time_label.config(text = '')
	tree.destroy()
	Down_Menu.place_forget()
	intr_link_but.config(state = 'disabled')

def Taipei(url):

	Clear()

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	global tree

	soup = Request_url(url)

	column_tag  = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr top"]' )
	row_tag     = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr"]' )    #class(屬性)tr(值)
	column_name =  list(column_tag.pop(0).stripped_strings)

	time_label_tag = soup.find('div' , class_ = 'rank_time').get_text()
	time_label.config(text = time_label_tag)

	ERL  = []
	TRL = []
	
	MIL = soup.select("div.rank_list.table.rankstyle1 div.tr div[class = 'td'] a")
	MIU = [ ]
	for m in range( len(MIL) ):
		MIU.append(MIL[m].get("href"))

	for rt in range(len(row_tag)):

		ERL = list(row_tag.pop(0).stripped_strings) #列表中的第一個元素開始移除

		if not ERL[1].isdigit():
			ERL.insert(1, str('') )
		if rt == 0:
			del ERL[3]
			del ERL[3]

		if ERL[3] == "未定" and len(ERL) == 4:
			ERL.append("")
			MIU.insert(rt, "")

		if ERL[4] != '預告片':
			ERL.insert(4, str('無'))

		TRL.append(ERL)


	tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = "headings") #第一列(垂直)不顯示
	ttk.Style().configure('Treeview', rowheight = 26)

	for cn  in range(len(column_name)):
		tree.heading(cn , text = column_name[cn] )
	for row in range(len(TRL)):
		tree.insert('', 'end', values=TRL[row], text=MIU[row])


	tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' )#本週
	tree.column('1' , width = 35  , minwidth = 35  , anchor = 'center' )#上週
	tree.column('2' , width = 260 , minwidth = 260 , anchor = 'center' )#片名
	tree.column('3' , width = 90 , minwidth = 90 , anchor = 'center' ) #上映日期
	tree.column('4' , width = 60 , minwidth = 60 , anchor = 'center' ) #預告片
	tree.column('5' , width = 70 , minwidth = 70 , anchor = 'center' ) #網友滿意度
	tree.pack(padx = 10 ,pady = 10 )

	tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)

def USA(url):


	Clear()

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	global tree

	soup = Request_url(url)
	#------------------------------
	MIL = soup.select( 'div.rank_list.table.rankstyle1 div.tr div[class = "td"] a' )
	MIU = []
	for m in range( len(MIL) ):
		MIU.append( MIL[m].get("href") )
	#------------------------------
	row_tag = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr"]' )

	time_label_tag = soup.find('div' ,class_ = 'rank_time').get_text()
	time_label.config(text = time_label_tag)

	ERL  = []
	TRL  = []

	count = -1
	record_row = 0  #沒有連結

	for rt in range(len(row_tag)):
		count +=1
		ERL = list(row_tag.pop(0).stripped_strings) #列表中的第一個元素開始移除

		if not ERL[1].isdigit():  #如果上週無排名就添加空元素
			ERL.insert(1, str('') )

		if rt == 0:    #本週排名為1
			del ERL[3:5]  #刪除第3個跟第4個元素(英文名稱跟電影介紹)

		if len(ERL) == 6:
			if ERL[4] != '預告片':
				ERL.insert(4, str('無') )

		if len(ERL) < 6:
			record_row = count
			MIU.insert(record_row,'')
			for i in range(6-len(ERL)):
				ERL.append('')

		TRL.append( ERL )

	#------------------------------

	column_tag  = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr top"]' )  #
	column_name =  list(column_tag.pop().stripped_strings)

	#------------------------------

	tree = ttk.Treeview(frame_rank , columns = column_name , height = 10 , show = 'headings')
	ttk.Style().configure('Treeview', rowheight = 26)

	for cn in range(len(column_name)):
		tree.heading(cn , text = column_name[cn])
	for row in range(len(TRL)):
		tree.insert('' , 'end' , values = TRL[row], text = MIU[row])

	tree.column('0' , width = 35 , minwidth = 35 , anchor = 'center' )#本週
	tree.column('1' , width = 35 , minwidth = 35 , anchor = 'center' )#上週
	tree.column('2' , width = 260 , minwidth = 260 , anchor = 'center')#片名
	tree.column('3' , width = 90 , minwidth = 90 , anchor = 'center' ) #上映日期
	tree.column('4' , width = 60 , minwidth = 60 , anchor = 'center' ) #預告片
	tree.column('5' , width = 70 , minwidth = 70 , anchor = 'center' ) #網友滿意度

	tree.pack(padx = 10 , pady = 10 )
	tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)

def Week(url):

	Clear()

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	global tree

	soup = Request_url(url)
	row_tag     = soup.select( 'div.rank_list.table.rankstyle2 div[class="tr"]' )

	time_label_tag = soup.find('div' ,class_ = 'rank_time').get_text()
	time_label.config(text = time_label_tag)

	ERL  = []
	TRL  = []

	for rt in range(len(row_tag)):

		ERL = list(row_tag.pop(0).stripped_strings)

		if ERL[3] != '預告片':
			ERL.insert(3, str('無') )

		TRL.append(ERL)

	#------------------------------

	column_tag  = soup.select( 'div.rank_list.table.rankstyle2 div[class="tr top"]' )
	column_name =  list(column_tag.pop(0).stripped_strings)

	#------------------------------

	MIL = soup.select( 'div.rank_list.table.rankstyle2 div.tr div[class = "td"] a' )
	MIU = []
	for m in range( len(MIL) ):
		MIU.append( MIL[m].get("href") )

	#------------------------------

	tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = "headings")
	ttk.Style().configure('Treeview', rowheight = 26)

	for cn  in range(len(column_name)):
		tree.heading(cn , text = column_name[cn] )
	for row in range(len(TRL)):
		tree.insert('' , 'end' , values = TRL[row] ,text = MIU[row])

	tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' )#週次
	tree.column('1' , width = 260 , minwidth = 260 , anchor = 'center' )#片名
	tree.column('2' , width = 125 , minwidth = 125 , anchor = 'center' )#統計時間
	tree.column('3' , width = 60  , minwidth = 60  , anchor = 'center' )#預告片
	tree.column('4' , width = 70  , minwidth = 70  , anchor = 'center' )#網友滿意度

	tree.pack(padx = 10 , pady = 10)
	tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)

def Year(url):

	Clear()

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	global tree

	soup = Request_url(url)
	row_tag     = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr"]' )

	time_label_tag = soup.find('div' ,class_ = 'rank_time').get_text()
	time_label.config(text = time_label_tag)

	MIL = soup.select('div.rank_list.table.rankstyle1 div.tr div[class = "td"] a')
	MIU = []
	for m in range(len(MIL)):
		MIU.append(MIL[m].get("href"))

	ERL  = []
	TRL  = []

	for rt in range(len(row_tag)):

		ERL = list(row_tag.pop(0).stripped_strings)

		if rt == 0:
			del ERL[3:5]

		if not ERL[1].isdigit():
			ERL.insert(1, str('') )
		if ERL[3] == "未定" and len(ERL) == 4:
			ERL.append("")
			MIU.insert(rt, "")

		if ERL[4] != '預告片':
			ERL.insert(4, str('無') )

		TRL.append(ERL)

	#------------------------------

	column_tag  = soup.select( 'div.rank_list.table.rankstyle1 div[class="tr top"]' )
	column_name =  list(column_tag.pop(0).stripped_strings)

	#------------------------------


	
	#------------------------------

	tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = "headings")
	ttk.Style().configure('Treeview', rowheight = 26)

	for cn  in range(len(column_name)):
		tree.heading(cn , text = column_name[cn] )
	for row in range(len(TRL)):
		tree.insert('' , 'end' , values = TRL[row] ,text = MIU[row])

	tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' )#本週
	tree.column('1' , width = 35  , minwidth = 35  , anchor = 'center' )#上週
	tree.column('2' , width = 260 , minwidth = 260 , anchor = 'center' )#片名
	tree.column('3' , width = 90 , minwidth = 90 , anchor = 'center' ) #上映日期
	tree.column('4' , width = 60 , minwidth = 60 , anchor = 'center' ) #預告片
	tree.column('5' , width = 70 , minwidth = 70 , anchor = 'center' ) #網友滿意度

	tree.pack(padx = 10 , pady = 10 )
	tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)

def Trailer(url):

	Clear()

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	global tree

	soup = Request_url(url)
	row_tag  = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr"]' )

	ERL  = []
	TRL  = []

	for rt in range(len(row_tag)):

		ERL = list(row_tag.pop(0).stripped_strings)

		if rt == 0 :
			del ERL[2:4]

		if ERL[3] != '預告片':
			ERL.insert(3, str('無') )
		TRL.append( ERL )

	#------------------------------

	column_tag  = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr top"]' )
	column_name =  list(column_tag.pop(0).stripped_strings)

	#------------------------------

	MIL = soup.select( 'div.rank_list.table.rankstyle3 div.tr div[class = "td"] a' )
	MIU = []
	for m in range( len(MIL) ):
		MIU.append( MIL[m].get("href") )

	#------------------------------

	tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = "headings")
	ttk.Style().configure('Treeview', rowheight = 26)

	for cn  in range(len(column_name)):
		tree.heading(cn , text = column_name[cn] )
	for row in range(len(TRL)):
		tree.insert('' , 'end' , values = TRL[row] , text = MIU[row])

	tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' ) #排名
	tree.column('1' , width = 295 , minwidth = 295 , anchor = 'center' ) #片名
	tree.column('2' , width = 90 , minwidth = 90 , anchor = 'center' )  #上映日期
	tree.column('3' , width = 60 , minwidth = 60 , anchor = 'center' )  #預告片
	tree.column('4' , width = 70 , minwidth = 70 , anchor = 'center' )  #網友滿意度

	tree.pack(padx = 10 ,pady = 10)
	tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)

def Expects(url):

	Clear()

	def SHOW_Tree(url):

		global tree

		soup = Request_url(url)
		row_tag     = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr"]' )

		ERL = []
		TRL = []

		for rt in range(len(row_tag)):

			ERL = list(row_tag.pop(0).stripped_strings)

			if rt == 0:
				del ERL[2]

			ERL.remove('人想看')

			if ERL[3] != '預告片':
				ERL.insert(3 ,'無')

			join = ''.join(ERL[5]) #提取第6個元素 合併到join這個字串

			str1 = ''     #投票人數

			for st in join:
				if st.isdigit():
					str1+=st

			del ERL[5]

			ERL.append(str1)
			TRL.append(ERL)

		#------------------------------

		column_tag  = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr top"]' )
		column_name = list(column_tag.pop(0).stripped_strings)
		del column_name[len(column_name)-1]    #把期待度刪掉
		column_name.extend(['想看人數','投票人數'])   #在最後面插入多個元素

		#------------------------------

		MIL = soup.select( 'div.rank_list.table.rankstyle3 div.tr div[class = "td"] a' )
		MIU = [ ]
		for m in range( len(MIL) ):
			MIU.append( MIL[m].get("href") )

		#------------------------------

		tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = "headings")
		ttk.Style().configure('Treeview', rowheight = 26)

		for cn in range(len(column_name)):
			tree.heading(cn , text = column_name[cn])
		for row in range(len(TRL)):
			tree.insert('' , 'end', values = TRL[row] ,text =  MIU[row] )

		tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' ) #排名
		tree.column('1' , width = 255 , minwidth = 255 , anchor = 'center' ) #片名
		tree.column('2' , width = 80 , minwidth = 80  , anchor = 'center' )  #上映日期
		tree.column('3' , width = 60 , minwidth = 60 , anchor = 'center' )  #預告片
		tree.column('4' , width = 60 , minwidth = 60 , anchor = 'center' )  #想看人數
		tree.column('5' , width = 60 , minwidth = 60 , anchor = 'center' )  #投票人數

		tree.pack(padx = 10 ,pady = 10)
		tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)


	#=======================
	def Select_Item(event):

		global record  #使用record

		Item = Down_Menu.get()
		if Item == '30天內即將上映':
			now = 30
		else:
			now = 365
		if now != record:  #避免發生重複選取
			url = 'https://movies.yahoo.com.tw/chart.html?cate=exp_30&search_date=' + str(now)
			tree.destroy()
			SHOW_Tree(url)
			rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')
			intr_link_but.config(state = 'disabled')
			record  = now
			CV.delete("all")
			for i in range(7):
				globals()['t' + str(i+1)].config(text = '')
	#=======================
	global record
	record = 30   #上次所選(預設是30)

	SHOW_Tree(url)

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	year_tag = Request_url(url).select('select[name = "search_date"] option')
	year_list = []
	for y in year_tag:
		year_list.append(y.get_text())

	range_label.config(text = '請選擇查詢範圍：')


	Down_Menu.config(values = year_list )
	Down_Menu.place( x = 120 , y = 80 )
	Down_Menu.current(0)  #預設選項
	Down_Menu.bind("<<ComboboxSelected>>", Select_Item)

def Feel(url):

	Clear()

	def SHOW_Tree(url):

		global tree

		soup = Request_url(url)
		row_tag = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr"]' )

		ERL = []
		TRL = []

		for rt in range(len(row_tag)):

			ERL = list(row_tag.pop(0).stripped_strings)

			if rt == 0:
				del ERL[2]

			if ERL[3] != '預告片':
				ERL.insert(3,'無')

			str1 = ''  #投票人數

			for st in ERL[5]:
				if st.isdigit():
					str1+=st
			del ERL[5]

			ERL.append(str1)
			TRL.append(ERL)

		#------------------------------

		column_tag  = soup.select( 'div.rank_list.table.rankstyle3 div[class="tr top"]' )
		column_name =  list(column_tag.pop(0).stripped_strings)
		column_name.append('投票人數')
		#------------------------------

		MIL = soup.select( 'div.rank_list.table.rankstyle3 div.tr div[class = "td"] a' )
		MIU = [ ]
		for m in range( len(MIL) ):
			MIU.append( MIL[m].get("href") )
		#------------------------------

		global tree

		tree = ttk.Treeview(frame_rank, columns = column_name , height = 10 , show = 'headings')
		ttk.Style().configure('Treeview', rowheight = 26)

		for cn in range(len(column_name)):
			tree.heading(cn , text = column_name[cn])
		for row in range(len(TRL)):
			tree.insert('' , 'end' , values = TRL[row] , text = MIU[row])

		tree.column('0' , width = 35  , minwidth = 35  , anchor = 'center' )#排名
		tree.column('1' , width = 245 , minwidth = 245 , anchor = 'center' )#片名
		tree.column('2' , width = 80 , minwidth = 80 , anchor = 'center' ) #上映日期
		tree.column('3' , width = 60 , minwidth = 60 , anchor = 'center' ) #預告片
		tree.column('4' , width = 70 , minwidth = 70 , anchor = 'center' ) #網友滿意度
		tree.column('5' , width = 60 , minwidth = 60 , anchor = 'center' ) #投票人數

		tree.pack(padx = 10 ,pady = 10)
		tree.bind("<<TreeviewSelect>>" , Show_Movie_Data)
	#=======================
	def Select_Item(event):

		global record

		Item = Down_Menu.get()

		now = ''
		for i in Item:  #對字串當中的每個字元做判斷如果是數字就加到sr裡
			if i.isdigit():
				now += i
		now = int(now)  #轉換成整數
		if now != record:
			tree.destroy()
			CV.delete("all")
			for i in range(7):
				globals()['t' + str(i+1)].config(text = '')

			url = 'https://movies.yahoo.com.tw/chart.html?cate=rating&search_year=' + str(now)
			SHOW_Tree(url)
			rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')
			intr_link_but.config(state = 'disabled')
			record  = now
	#=======================

	global record
	record = 30   #上次所選(預設是30)

	SHOW_Tree(url)

	rank_link_but.config(command = lambda: webbrowser.open(url) , state = 'normal')


	year_tag = Request_url(url).select('select[name = "search_year"] option')

	year_list = []

	for y in year_tag:
		year_list.append(y.get_text())

	range_label.config(text = '請選擇查詢範圍：')

	Down_Menu.config(values = year_list )
	Down_Menu.place( x = 120 , y = 80 )
	Down_Menu.current(0)  #預設選項
	Down_Menu.bind("<<ComboboxSelected>>", Select_Item)

#==================================================
def v1(url):
	
	Taipei(url)
	B1.config(state= 'disabled' )
	for i in [2,3,4,5,6,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v2(url):
	USA(url)
	B2.config(state= 'disabled' )
	for i in [1,3,4,5,6,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v3(url):
	Week(url)
	B3.config(state= 'disabled' )
	for i in [1,2,4,5,6,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v4(url):
	Year(url)
	B4.config(state= 'disabled' )
	for i in [1,2,3,5,6,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v5(url):
	Trailer(url)
	B5.config(state= 'disabled' )
	for i in [1,2,3,4,6,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v6(url):
	Expects(url)
	B6.config(state= 'disabled' )
	for i in [1,2,3,4,5,7]:
		globals()['B' + str(i)].config(state = 'normal')

def v7(url):
	Feel(url)
	B7.config(state= 'disabled' )
	for i in [1,2,3,4,5,6]:
		globals()['B' + str(i)].config(state = 'normal')
#=================================================================================================
#使用者介面

#======================
#  		  框架
#======================

UI = tk.Tk() #建GUI

UI.title('yahoo奇摩電影排行榜')

UI.geometry('865x705')

UI.resizable(0,0)  #用戶不可改變大小

frame_rank = LabelFrame( UI , bd = 2 , text = '電影排行榜' , font = ('微軟正黑體', 13)  , fg = 'red')
frame_img  = LabelFrame( UI , bd = 2 , text = '電影圖片'   , font = ('微軟正黑體', 13)  , fg = 'green')
frame_text = LabelFrame( UI , bd = 2 , text = '電影詳情'   , font = ('微軟正黑體', 13)  , fg = 'blue')

frame_rank.place( x = 20 , width = 580 , y = 120 , height = 335 )
frame_img.place( x = 620 , width = 225 , y = 120 , height = 335 )
frame_text.place( x = 20 , width = 825 , y = 465 , height = 220 )

#======================
#  	 按鈕的文字跟連結
#======================

but_list = Request_url('https://movies.yahoo.com.tw/chart.html').select('div.rank_list_bottombtn ul li a')

but_title = []
but_link  = []

for but in range(len(but_list)):
	but_title.append(but_list[but].get_text())
	but_link. append(but_list[but].get('href'))

#======================
#  	   建立按鈕&事件
#======================

rank_link_but = Button(UI , text = '電影排行榜' , bd = 1 , relief = 'solid' , height = 2 , activebackground = '#a8ff24' , cursor = "hand2" , state = 'disabled')
rank_link_but.place(x = 740 , y = 78 , width = 100)

intr_link_but = Button(UI , text = '電影介紹'   , bd = 1 , relief = 'solid' , height = 2 , activebackground = '#a8ff24' , cursor = "hand2" , state = 'disabled')
intr_link_but.place(x = 620 , y = 78 , width = 100)

for i in range(len(but_title)):
	globals()['B' + str(i+1)] = Button(UI , height = 2 , text = but_title[i] , bd = 1 , relief = 'solid' , activebackground = '#a8ff24' , cursor = "hand2" )
	globals()['B' + str(i+1)].place(x = 20 + (i * 120) , y = 20 , width = 100)

B1.config(command = lambda: v1(but_link[0]))
B2.config(command = lambda: v2(but_link[1]))
B3.config(command = lambda: v3(but_link[2]))
B4.config(command = lambda: v4(but_link[3]))
B5.config(command = lambda: v5(but_link[4]))
B6.config(command = lambda: v6(but_link[5]))
B7.config(command = lambda: v7(but_link[6]))

#======================
#  		  電影圖片
#======================

CV = Canvas(frame_img , height = 300 , width = 210  ) #建立畫布
CV.pack( padx = 5 , pady = 5 )

#======================
#    電影詳細介紹文字
#======================

loca_y1 = 5  #初始位置
loca_y2 = 5

for left in range(1,6):  #1-5  片名,上映日期,片長,發行公司,IMDb分數
	globals()['t' + str(left)] = Label( frame_text , fg = 'black' , font = ('微軟正黑體', 10) )
	globals()['t' + str(left)].place(x = 30 , y = loca_y1)
	loca_y1 += 40 #間距

for right in range(6,8): #6-7  導演,演員
	globals()['t' + str(right)] = Label( frame_text , fg = 'black' , font = ('微軟正黑體', 10) , wraplength = 380 , justify = 'left' )
	globals()['t' + str(right)].place(x = 410 , y = loca_y2)
	loca_y2 += 40

#======================
#  		初始畫面
#======================

range_label = Label( UI )
range_label.place( x = 20 , y = 80 )

time_label = Label( UI , font = ('微軟正黑體',12))
time_label.place( x = 20 , y = 80 )

Down_Menu = ttk.Combobox(UI , width = 15 , state = 'readonly')#不能自行輸入值
Down_Menu.place()

tree = ttk.Treeview(UI) #建立空treeview 防止Clear()抓不到而發生錯誤

#======================
#		維持視窗
#======================
UI.mainloop()
