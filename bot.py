from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans


API_TOKEN = '5928752976:AAGbdodODfqG1C98YrG2PWSOaredpBYlpt4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def make_photo_black_and_white(path):
    img = Image.open(path)
    BlackAndWhite = img.convert("L")
    BlackAndWhite.save('/Users/tretyakovaekaterina/Desktop/практика/blackandwhite.jpg')


def blur_photo(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    blurred = cv2.blur(image, (11, 11))
    plt.imsave('/Users/tretyakovaekaterina/Desktop/практика/blurred.png', blurred)


def rotate(path, angle):
    image = Image.open(path)
    out = image.rotate(angle)
    out.save('/Users/tretyakovaekaterina/Desktop/практика/rotated.png')


def mirror_photo(path):
    image = Image.open(path)
    mirrored = image.transpose(Image.FLIP_LEFT_RIGHT)
    mirrored.save('/Users/tretyakovaekaterina/Desktop/практика/mirrored.jpg')


def find_five_colours(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)

    def preprocess(raw):
        image = cv2.resize(raw, (900, 600), interpolation=cv2.INTER_AREA)
        image = image.reshape(image.shape[0] * image.shape[1], 3)
        return image

    def rgb_to_hex(rgb_color):
        hex_color = "#"
        for i in rgb_color:
            hex_color += ("{:02x}".format(int(i)))
        return hex_color

    def analyze(img):
        clf = KMeans(n_clusters=5)
        color_labels = clf.fit_predict(img)
        center_colors = clf.cluster_centers_
        counts = Counter(color_labels)
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]

        plt.figure(figsize=(12, 8))
        plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)

    modified_image = preprocess(image)
    analyze(modified_image)
    plt.savefig('/Users/tretyakovaekaterina/Desktop/практика/analitics.jpg')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я фотобот. Отправь мне фотографию, с которой хочешь, чтобя я поработал.")


@dp.message_handler(content_types=['photo'])
async def scan_message(message: types.InputMediaPhoto):
    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')
    path = '/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg'
    await message.photo[-1].download(path)

    bw_button = InlineKeyboardButton(text='Сделать ее черно-белой', callback_data='bw')
    blur_button = InlineKeyboardButton(text='Сделать размытие', callback_data='blur')
    rotate_button = InlineKeyboardButton(text='Развернуть фото', callback_data='rotate')
    mirror_button = InlineKeyboardButton(text='Отразить по вертикали', callback_data='mirror')
    find_colours_button = InlineKeyboardButton(text='Найти 5 доминирующих цветов', callback_data='find_colours')
    inkb = InlineKeyboardMarkup(row_width=1).add(bw_button, blur_button, rotate_button, mirror_button, find_colours_button)
    await message.reply("Что вы хотите сделать с фото?", reply_markup=inkb)


@dp.callback_query_handler(text='bw')
async def find_colours(callback: types.CallbackQuery):
    make_photo_black_and_white('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg')
    path = '/Users/tretyakovaekaterina/Desktop/практика/blackandwhite.jpg'
    bw_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.message.answer_photo(photo=bw_photo, reply_markup=keyboard)


@dp.callback_query_handler(text='blur')
async def blur(callback: types.CallbackQuery):
    blur_photo('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg')
    path = '/Users/tretyakovaekaterina/Desktop/практика/blurred.png'
    bw_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.message.answer_photo(photo=bw_photo, reply_markup=keyboard)


@dp.callback_query_handler(text='rotate')
async def find_angle(callback: types.CallbackQuery):
    kb = [
        [types.KeyboardButton(text="90")],
        [types.KeyboardButton(text="180")],
        [types.KeyboardButton(text="270")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.message.answer('На сколько градусов вы хотите развернуть фото?', reply_markup=keyboard)

@dp.message_handler(text='90')
async def rotate_90(message: types.Message):
    rotate('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg', 90)
    path = '/Users/tretyakovaekaterina/Desktop/практика/rotated.png'
    rotated_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id, photo=rotated_photo, reply_markup=keyboard)


@dp.message_handler(text='180')
async def rotate_180(message: types.Message):
    rotate('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg', 180)
    path = '/Users/tretyakovaekaterina/Desktop/практика/rotated.png'
    rotated_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id, photo=rotated_photo, reply_markup=keyboard)


@dp.message_handler(text='270')
async def rotate_270(message: types.Message):
    rotate('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg', 270)
    path = '/Users/tretyakovaekaterina/Desktop/практика/rotated.png'
    rotated_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id, photo=rotated_photo, reply_markup=keyboard)



@dp.callback_query_handler(text='mirror')
async def mirror(callback: types.CallbackQuery):
    mirror_photo('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg')
    path = '/Users/tretyakovaekaterina/Desktop/практика/mirrored.jpg'
    mirrored_photo = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.message.answer_photo(photo=mirrored_photo, reply_markup=keyboard)


@dp.callback_query_handler(text='find_colours')
async def find_colours(callback: types.CallbackQuery):
    find_five_colours('/Users/tretyakovaekaterina/Desktop/практика/photo_from_bot.jpg')
    path = '/Users/tretyakovaekaterina/Desktop/практика/analitics.jpg'
    analitics = InputFile(path)
    kb = [
        [types.KeyboardButton(text="Отправить новое фото")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.message.answer_photo(photo=analitics, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Отправить новое фото")
async def new_photo(message: types.Message):
    markup = types.ReplyKeyboardRemove()
    await message.reply("Отправь мне новую фотку, с которой хочешь, чтобы я поработал.", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
