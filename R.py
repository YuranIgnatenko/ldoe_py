import os, shutil, time,sys
from androidhelper import Android

# os.system('pwd')

path = "/storage/emulated/0/Android/"
pref_data = "data/" 
pref_obb = "obb/"
namefile_origin = "zombie.survival.craft.z"
namefile_copy = "zombie.survival.craft.z_copy"
title="кэш - это ваш прогресс в игре"

msg_cache_copy='''

✅ КЭШ сохранён! 🧐

Сейчас можно удалять игру.
Скачайте игру на телефон,
в которую хотите перенести 
свой игровой прогресс и
прочие достижения
(любую - мод или официальную)
и после установки игры на телефон,
(без разницы - запускать ли игру или нет)
вернитесь сюда в меню
и нажмите "Использовать кэш".

'''
msg_cache_origin='''

🟩 КЭШ игры найден! 🙂

Можно запускать. Приятной игры.

Нажмите "Сохранить кэш", 
если вышло обновление,
если игра не запускается,
если хотите перенести 
ваш текущий прогресс
из официальной версии в мод-версию
или наоборот.
после сохранения кэша, скачайте и 
установите игру 
откуда угодно и
вернитесь сюда в меню,
что бы применить ваш кэш
с игровым прогрессом к игре.

'''

msg_cache_not_found='''

🟥 КЭШ не найден! 😧

Он появится автоматически 
после входа в игру,
установите официальную игру 
из плей маркета
и запустите её, а потом
вернитесь сюда в меню
для сохранения вашего прогресса.

'''

droid = Android()
run = True

def dialog_list():
    
    
 # копия кэша
 res = check_copy_islive()

 if res == True:
     droid.dialogCreateAlert(title,msg_cache_copy)
 else:
 # если копии нет, проверяем есть ли
 # оригинальный кэш
     res = check_origin_islive()
     if res == True:
         droid.dialogCreateAlert(title,msg_cache_origin)
     else:
         droid.dialogCreateAlert(title,msg_cache_not_found)
    
    
    
    
 #if check_copy_islive() == True:
 #    droid.dialogCreateAlert("КЭШ"+status_copy_yes)
 #else:
 #    droid.dialogCreateAlert("КЭШ"+status_copy_no)
 droid.dialogSetPositiveButtonText("Сохр.кэш")
 droid.dialogSetNegativeButtonText("Выход")
 droid.dialogSetNeutralButtonText("Использ.кэш")
 droid.dialogShow()
 return droid.dialogGetResponse()[1]

# true if yes file
def check_copy_islive():
 r1 = os.path.exists(path+pref_data+namefile_copy)
 r2 = os.path.exists(path+pref_obb+namefile_copy)
 if r1 == True and r2 == True:
     return True
 else:
     return False

# true if yes file
def check_origin_islive():
 r1 = os.path.exists(path+pref_data+namefile_origin)
 r2 = os.path.exists(path+pref_obb+namefile_origin)
 if r1 == True and r2 == True:
     return True
 else:
     return False

def remove_dir(path):
 shutil.rmtree(path)

def rename_origin_to_copy():
 os.rename(path+pref_data+namefile_origin, path+pref_data+namefile_copy)
 os.rename(path+pref_obb+namefile_origin, path+pref_obb+namefile_copy)

def rename_copy_to_origin():
 os.rename(path+pref_data+namefile_copy, path+pref_data+namefile_origin)
 os.rename(path+pref_obb+namefile_copy, path+pref_obb+namefile_origin)

def info(text):
 droid.makeToast(text)
 droid.vibrate(300)

# сохранение наигранного кэша
def save():
 # проверка - существует ли 
 # копия кэша
 res = check_copy_islive()

 if res == True:
     info("кэш уже сохранён !")
 else:
 # если копии нет, проверяем есть ли
 # оригинальный кэш
     res = check_origin_islive()
     if res == False:
         info("кэш не найден !")
     else:
         # создание копии кэша
         rename_origin_to_copy()
         progress("Сохранение кэша")
         info("кэш сохранён !")

# применение кэша подключение к игре
def upload():
 # проверка - существует ли 
 # копия кэша
 res = check_copy_islive()
 if res == True:
 # удалить дефолтный кэш
 # если он есть
     if check_origin_islive() == True:
         try:
             remove_dir(path+pref_data+namefile_origin)
             progress("Замена кеша в Android/data")
             info("заменен кэш в Android/data")
         except:
             pass
         try:
             remove_dir(path+pref_obb+namefile_origin)
             progress("Замена кеша в Android/obb")
             info("заменен кэш в Android/obb")
         except:
             pass
 
 # применение кэша
     rename_copy_to_origin()
     progress("Применение кэша")
     info("кэш применён !")
 else:
 # если копии нет
     info("кэш-копия не найден !")

def progress(m):
  title = 'Автоматическая настройка'
  message = m
  droid.dialogCreateHorizontalProgress(title, message, 50)
  droid.dialogShow()
  for x in range(0, 50):
    time.sleep(0.1)
    droid.dialogSetCurrentProgress(x)
  droid.dialogDismiss()


while run:
 resp = dialog_list()
 print(resp)

 #exit
 if resp["which"] == "negative":
     droid.vibrate(200)
     run = False
 #save
 if resp["which"] == "positive":
     save()

 #upload
 if resp["which"] == "neutral":
     upload()
     
     
#droid.launch(namefile_origin)
#droid.makeIntent()
#print(droid.getLaunchableApplications())
#droid.launch("re.sova.five.Sova")
#droid.launch("ru")
#sys.exit()
