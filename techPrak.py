# Импорт библиотек
import cv2 as cv


# Создаем ядра для морфологических операций
erode_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
dilate_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))

# Открываем видеофайл для чтения
cap = cv.VideoCapture('IMG_1337.MOV')

# Задаем глобальные координаты области интереса (ROI)
global_w = 10000
global_h = 10000
global_x = 0
global_y = 0

# Функция для объединения ROI из нескольких кадров
def merge_roi(frame, x, y, w, h):
    return frame[y:y + h, x:x + w, :]


# Чтение первого кадра
for i in range(1):
    success, frame = cap.read()
    print(frame.shape[0], frame.shape[1])
    frame_w_px = frame.shape[1]
if not success:
    exit(1123)

# Вычисляем время между кадрами и ширину пикселя в метрах
time_between_frames = 1/30
real_w = 411/100
real_w_px = real_w/frame_w_px

# Конвертируем фоновый кадр в оттенки серого
gray_background = cv.cvtColor(merge_roi(frame, global_x, global_y, global_w, global_h), cv.COLOR_BGR2GRAY)

cx = 0
cy = 0

success, frame = cap.read()
print(success)
while success:
    cnt += 1
    if cnt == 300:
        break
    frame = merge_roi(frame, global_x, global_y, global_w, global_h)
    gray_frame = cv.cvtColor(merge_roi(frame, global_x, global_y, global_w, global_h), cv.COLOR_BGR2GRAY)

    # Вычисляем разницу между текущим кадром и фоновым
    diff = cv.absdiff(gray_background, gray_frame)
    # Применяем пороговое значение для получения двоичной карты
    _, thresh = cv.threshold(diff, 40, 255, cv.THRESH_BINARY)
    # Применяем морфологические операторы
    cv.erode(thresh, erode_kernel, thresh, iterations=2)
    cv.dilate(thresh, dilate_kernel, thresh, iterations=2)

    # Находим контуры
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Проходим по найденным контурам
    for c in contours:
        # Если площадь контура больше определенного значения, рисуем прямоугольник вокруг него
        if cv.contourArea(c) > 4000:
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            # Вычисляем центр масс контура
            M = cv.moments(c)
            lastcx = cx
            lastcy = cy
            cx = x
            cy = y
            # Вычисляем скорость в км/ч
            print('speed in km/h:', (((lastcx-cx)*real_w_px)/time_between_frames)*3.6)

    # Показываем результаты на экране
    cv.imshow('diff', diff)
    cv.imshow('thresh', thresh)
    cv.imshow('detection', frame)

    # Ожидаем нажатия клавиши Escape для выхода из цикла
    while cv.waitKey(1)!= 27:
        continue
    success, frame = cap.read()