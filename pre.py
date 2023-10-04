from senior import*

'''pictures'''
pic_1=picture("1.png")
pic_2=picture("2.png")
pic_3=picture("3.png")
pic_4=picture("4.png")
pic_5=picture("5.png")
pic_6=picture("6.png")
pic_9=picture("9.png")
pic_10=picture("10.png")
pic_close=picture("close.png")
pic_min=picture("min.png")
pic_start=scp((1280, 60), WHITE)
pic_start.set_alpha(128)
pic_one=picture("one.png")
pic_ten=picture("ten.png")
pic_prl=picture("parallelogram.png")
pic_archive=picture("archive.png")
pic_select=picture("gatherbottom.png")
pic_selectstu=picture("selectstu.png")
pic_stone=picture("stone.png")
pic_stu=picture("stu.png")
pic_qui=picture("qui.png")

START_PIC=[pic_3, pic_2, pic_4, pic_6, pic_9]

'''buttons'''
BUTTON_ASSURE=Button(scp((120, 60), GREEN), (0, 0), Text("确认", font=font("SimHei", 24)))
BUTTON_YES=Button(scp((120, 60), GREEN), (0, 0), Text("是", font=font("SimHei", 24)))
BUTTON_NO=Button(scp((120, 60), RED), (0, 0), Text("否", font=font("SimHei", 24)))
BUTTON_BACK=Button(scp((120, 60), RED), (0, 0), Text("返回", font=font("SimHei", 24)))
BUTTON_CLOSE=Button(pic_close, (0, 0))
BUTTON_MIN=Button(pic_min, (0, -24))
BUTTON_START=Button(pic_start, (0, 480), Text("Press To Start", font=font("ConsolasI", 28)))

BUTTON_ONE=Button(pic_one, (0, 0))
BUTTON_TEN=Button(pic_ten, (0, 0))
BUTTON_SELECT=Button(pic_selectstu, (-8, -8))
BUTTON_STU=Button(pic_stu, (0, 0))

'''number'''
ONE_STONE=120
TEN_STONE=1200
GUARANTEE=200
gUARANTEE=100
SMALLHEIGHT=200
MINIHEIGHT=100
psb=[0, 0.785, 0.185, 0.03]
fes_psb=[0, 0.5, 0.03, 0.007]
CALLING=Text("当你想抽卡时，打开这个游戏，直到你冷静下来", (0, 0), font=font("SimHeiB", 50))
CALLINGPAGE=Page(scp((W, H), AZURE), (0, 0))
CALLINGPAGE.add_text(CALLING, -3)
BLACKSUITPAGE=Page(pic_10, (0, 0))