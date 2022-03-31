from logging import error
from platform import system
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pyautogui import screenshot
from os import getenv, kill, getpid, remove, listdir
from signal import SIGINT
from sys import exit
from datetime import datetime
if system() == 'Windows':
    from win32gui import SendMessage
    from win32con import HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER
elif system() == 'Linux':
    pass
else:
    error("System not supported")

from subprocess import Popen
from random import randint
from time import sleep
from cv2 import imwrite, VideoCapture, destroyAllWindows, CAP_DSHOW

# show heading
print("  _____    _                                 ______       _    ")
print(" |_   _|  | |                                | ___ \     | |   ")
print("   | | ___| | ___  __ _ _ __ __ _ _ __ ___   | |_/ / ___ | |_  ")
print("   | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \  | ___ \/ _ \| __| ")
print("   | |  __/ |  __/ (_| | | | (_| | | | | | | | |_/ / (_) | |_  ")
print("   \_/\___|_|\___|\__, |_|  \__,_|_| |_| |_| \____/ \___/ \__| ")
print("                   __/ |                                       ")
print("                  |___/                                        ")
print(" ")

#Create local log file
old_print = print
log_file = open("logfile.log", "a")
print = lambda *args, **kw: old_print(*args, **kw) or old_print(*args, file=log_file, **kw)
log = ''
def myprint(mystr):
    global log
    print(mystr)
    log =log + '\n' + mystr

#Get bot token
myprint("Uploading the bot token file...")

try:
    botTokenFile = open(r"./token.txt")
    botToken = botTokenFile.readline()
    myprint("Bot token uploaded successfully")
except:
    myprint("Bot token not found, please create a .txt file named 'token.txt' with your bot token in the first line")
    input('Press [OK] to exit from the program...')
    exit()
    
#list of commands
ask_commands =  'What would you like to do?\n\n' + \
                ' - /screen to take a screenshot\n\n' + \
                ' - /snapshot to take a snapshot\n\n' + \
                ' - /turnoff to turn off the PC monitor\n\n' + \
                ' - /turnon to turn on the PC monitor\n\n' + \
                ' - /lock to lock the PC\n\n' + \
                ' - /unlock <password> to unlock the PC\n\n' + \
                ' - /logout to logout the PC and stop the bot\n\n' + \
                ' - /standby to put the PC on standby and stop the bot\n\n' + \
                ' - /hibernate to hibernate the PC and stop the bot\n\n' + \
                ' - /shutdown to shutdown the PC and stop the bot\n\n' + \
                ' - /restart to restart the PC and stop the bot\n\n' + \
                ' - /stop to stop the bot\n\n'
                
after_command = 'Type /commands to see the list of all commands'
easter_dir = './.easter_egg/'


# Def  
   
def start(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    update.message.reply_text('Hi ' + userName + ' \U0001F604 ' + 
                            ask_commands +
                            'Make sure the bot is running on your PC!')
    
def commands(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(ask_commands)
    
def screen(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    chat_id = update.message.chat_id
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Screenshot requested by " + userName + " at " + date_time)
    update.message.reply_text('Taking a screenshot of your PC \U0001F60B ')
    myScreenshot = screenshot()
    if system() == 'Windows':
        fileName = getenv('APPDATA') + '\\telegram-bot-screen.png'
    elif system() == 'Linux':
        fileName = getenv('HOME') + '/.cache/telegram-bot-screen.png'
    else:
        error("OS not supported")
    
    try:
        myScreenshot.save(fileName)
    except:
        update.message.reply_text('Fatal error occured while saving the screenshot \U0001F624') 
        myprint("Fatal error occured while saving the screenshot")
        return
    try:
        myphoto = open(fileName, 'rb')
        context.bot.sendPhoto(chat_id=chat_id,photo=myphoto, caption='Here your screenshot \U0001F60E',timeout=500)
        myphoto.close()
    except:
        update.message.reply_text('Fatal error occured while sending the screenshot \U0001F62D')
        myprint("Fatal error occured while sending the screenshot")
        return
    update.message.reply_text('Screenshot sent \U0001F607 ' + after_command)
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Screenshot successfully sent to " + userName + " at " + date_time)
    remove(fileName)
    
def snapshot(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    chat_id = update.message.chat_id
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Snapshot requested by " + userName + " at " + date_time)
    update.message.reply_text('Taking a snapshot from your PC \U0001F60B ')
    if system() == 'Windows':
        fileName = getenv('APPDATA') + '\\telegram-bot-snapshot.png'
    elif system() == 'Linux':
        fileName = getenv('HOME') + '/.cache/telegram-bot-snapshot.png'
    else:
        error("OS not supported")
    try:
        cam = VideoCapture(0,CAP_DSHOW)
        s, img = cam.read()
        imwrite(fileName,img)
        cam.release()
        destroyAllWindows()
    except:
        update.message.reply_text('Fatal error occured while saving the snapshot \U0001F624') 
        myprint("Fatal error occured while saving the snapshot")
        return
    try:
        myphoto = open(fileName, 'rb')
        context.bot.sendPhoto(chat_id=chat_id,photo=myphoto, caption='Here your snapshot \U0001F60E',timeout=500)
        myphoto.close()
    except:
        update.message.reply_text('Fatal error occured while sending the snapshot \U0001F62D')
        myprint("Fatal error occured while sending the snapshot")
        return
    update.message.reply_text('Snapshot sent \U0001F607 ' + after_command)
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Snapshot successfully sent to " + userName + " at " + date_time)
    remove(fileName)
    
    
def stop(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    update.message.reply_text('Stopping the bot on your PC \U0001F634 Bye Bye ' + userName + ' \U0001F618')
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Bot stopped by " + userName + " at " + date_time)
    sleep(0.5)
    log_file.close()
    kill(getpid(), SIGINT)
    
def turnoff(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Monitor turned off by " + userName + " at " + date_time)
    update.message.reply_text('Turning off the monitor of your PC \U0001F634')
    if system() == 'Windows':
        SendMessage(HWND_BROADCAST,WM_SYSCOMMAND, SC_MONITORPOWER, 2)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    update.message.reply_text('Monitor turned off \U0001F607 ' + after_command)

    
def turnon(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Monitor turned on by " + userName + " at " + date_time)
    update.message.reply_text('Turning on the monitor of your PC \U0001F604')
    if system() == 'Windows':
        SendMessage(HWND_BROADCAST,WM_SYSCOMMAND, SC_MONITORPOWER, -1)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    update.message.reply_text('Monitor turned on \U0001F607 ' + after_command)
    
def lock(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC locked by " + userName + " at " + date_time)
    update.message.reply_text('Locking your PC \U0001F634')
    if system() == 'Windows':
        Popen("rundll32.exe user32.dll, LockWorkStation",shell=True)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    update.message.reply_text('PC locked \U0001F607 ' + after_command)
        
def unlock(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Sorry, this feature has not been implemented in my code yet \U0001F616 ' + after_command)
    # global countAcces, unlocked
    # if not unlocked:
    #     userName = update.message.from_user.first_name;
    #     now = datetime.now() # current date and time
    #     date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    #     max_attempts = 3
    #     if len(context.args)==0:
    #         userPassword = ''
    #     else:
    #         userPassword = context.args[0]
            
    #     if ctypes.windll.advapi32.LogonUserW(userPCName,".", userPassword, 3, 0, ctypes.byref(token)) == 0:
    #         print("Login attempt by " + userName + " at " + date_time)
    #         countAcces = countAcces + 1
    #         if countAcces<max_attempts:
    #             print("Login attempt failed by " + userName + " at " + date_time)
    #             update.message.reply_text('Wrong password, ' + str(max_attempts-countAcces) + ' attempt(s) remaining \U0001F635 ' + after_command)
    #         else:
    #             print("Login locked after" + str(max_attempts) + " failed logins by " + userName + " at " + date_time)
    #             update.message.reply_text('Login locked, please unlock the PC directly and restart the bot \U00011F631 ' + after_command)
    #     else:
    #         countAcces = 0
            
    #         #TODO
            
    #         print("PC successfully unlocked by " + userName + " at " + date_time)
    #         update.message.reply_text('PC successfully unlocked \U0001F60D ' + after_command)
    #         unlocked = True
            
    # else:
    #     update.message.reply_text('PC already unlocked \U0001F605 ' + after_command)
    
def shutdown(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC shutted down by " + userName + " at " + date_time)
    update.message.reply_text('Shutting down your PC \U0001F634 The bot will be stopped')
    if system() == 'Windows':
        Popen("shutdown /s /t 1",shell=True)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    stop(update,context)
    
def restart(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC restarted by " + userName + " at " + date_time)
    update.message.reply_text('Restarting your PC \U0001F635 The bot will be stopped')
    if system() == 'Windows':
        Popen("shutdown /r /t 1",shell=True)   
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    stop(update,context)
    
def hibernate(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC hibernated down by " + userName + " at " + date_time)
    update.message.reply_text('Hibernating your PC \U0001F634 The bot will be stopped')
    if system() == 'Windows':
        Popen("shutdown /h /f",shell=True)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    stop(update,context)
    
def standby(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC put on standby by " + userName + " at " + date_time)
    update.message.reply_text('Putting your PC on standby \U0001F634 The bot will be stopped')
    if system() == 'Windows':
        Popen("rundll32.exe powrprof.dll,SetSuspendState Sleep",shell=True)
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    stop(update,context)
    
def logout(update: Update, context: CallbackContext) -> None:
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("PC logged out by " + userName + " at " + date_time)
    update.message.reply_text('Logging out your PC \U0001F634 The bot will be stopped')
    if system() == 'Windows':
        Popen("shutdown /l",shell=True)   
    elif system() == 'Linux':
        pass
    else:
        error("OS not supported")
    stop(update,context)  

def oscar(update: Update, context: CallbackContext) -> None:
    files = listdir(easter_dir)
    chat_id = update.message.chat_id
    n = randint(0,len(files)-1) #generate random (int) value in a given range
    fileName = easter_dir + files[n]
    photo = open(fileName, 'rb')
    context.bot.send_sticker(chat_id,photo,timeout=500)
    photo.close()

def getlog(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(log)
    userName = update.message.from_user.first_name;
    now = datetime.now() # current date and time
    date_time = now.strftime("%H:%M:%S, %m/%d/%Y")
    myprint("Log requested by " + userName + " at " + date_time)
        

def main():
    myprint("Running the bot...")
    myprint("Type /start or /commands on the Telegram bot to see the list of all commands")
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(botToken)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("commands", commands))
    dispatcher.add_handler(CommandHandler("screen", screen))
    dispatcher.add_handler(CommandHandler("snapshot", snapshot))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("turnoff", turnoff))
    dispatcher.add_handler(CommandHandler("turnon", turnon))
    dispatcher.add_handler(CommandHandler("shutdown", shutdown))
    dispatcher.add_handler(CommandHandler("hibernate", hibernate))
    dispatcher.add_handler(CommandHandler("standby", standby))
    dispatcher.add_handler(CommandHandler("lock", lock))
    dispatcher.add_handler(CommandHandler("unlock", unlock))
    dispatcher.add_handler(CommandHandler("logout", logout))
    dispatcher.add_handler(CommandHandler("restart", restart))
    dispatcher.add_handler(CommandHandler("getlog", getlog))
    
    
    # easter egg
    dispatcher.add_handler(CommandHandler("oscar", oscar))
    
    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()
    
    
if __name__ == '__main__':
    main()