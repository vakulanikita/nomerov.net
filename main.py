import matplotlib.pyplot as plt
import pytesseract
import cv2
import urllib.request
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'

from skimage import io

def open_img(img_path):
    req = urllib.request.urlopen(img_path)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    carplate_img = cv2.imdecode(arr, -1)  # 'Load it as it is'

    # cv2.imshow('random_title', img)
    # if cv2.waitKey() & 0xff == 27: quit()

    # carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(carplate_img)
    # plt.show()

    return carplate_img

def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)

    for x, y, w, h in carplate_rects:
        try:
            carplate_img = image[y+15:y+h-10, x+15:x+w-20]
        except:
            print("An exception occurred")
            carplate_img = 0

    return carplate_img


def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return resized_image


def main(url):
    carplate_img_rgb = open_img(img_path=url)
    carplate_haar_cascade = cv2.CascadeClassifier('C:/Users/haarcascade_russian_plate_number.xml')
    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)
    # plt.show()

    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    plt.axis('off')
    plt.imshow(carplate_extract_img_gray, cmap='gray')
    plt.show()

    message1 = 'Номер авто: ', pytesseract.image_to_string(
         carplate_extract_img_gray,
         config='--psm 6 --oem 3 -c tessedit_char_whitelist=QWERTYUIOPASDFGHJKLZXCVBNM0123456789')

    print(message1)
    return pytesseract.image_to_string(
         carplate_extract_img_gray,
         config='--psm 6 --oem 3 -c tessedit_char_whitelist=QWERTYUIOPASDFGHJKLZXCVBNM0123456789')
    # bot.reply_to(message, "I support the following commands: \n /start \n /info \n /help \n /status !!!")


# if __name__ == '__main__':
#     main()

import telebot

API_KEY = "6591955432:AAH6Pzw8KR_cG6LazXFZ_kbtlQ7Y2DeLz2E"

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Я ИИ телеграм бот по распознаванию автомобильных номеров. Пришли изображение")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Я поддерживаю команды: \n /start \n /info \n /help \n /status")


@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, "Я ИИ телеграм бот по распознаванию автомобильных номеров. Пришли изображение.")


@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "Работаю.")

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    # 'C:/Users/nikva/PycharmProjects/pythonProject/image.jpg'
    # https://api.telegram.org/file/bot6591955432:AAH6Pzw8KR_cG6LazXFZ_kbtlQ7Y2DeLz2E/photos/file_1.jpg
    # 'C:/Users/lada.jpg'
    url = 'https://api.telegram.org/file/bot6591955432:AAH6Pzw8KR_cG6LazXFZ_kbtlQ7Y2DeLz2E/' + file_info.file_path
    print(url)
    result = main(url)
    print(result)
    bot.reply_to(message, "Номер авто: {}".format(result))

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

print("Hey, I am up....")
bot.polling()