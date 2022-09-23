import cv2
from photoshop import Session
import photoshop.api as phs


def fr_auto():
    # Копирование пути открытого в PS документа
    with Session() as ps:
        doc = ps.active_document
        path = str(doc.path)
        filename = doc.name
        path = path + '\\' + filename

    # Распознание лица на открытом в PS документе
    photo_r = cv2.imread(path)
    photo_g = cv2.cvtColor(photo_r, cv2.COLOR_RGB2GRAY)

    face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face.detectMultiScale(photo_g, 1.1, 19)
    print(faces)

    frame2 = cv2.rectangle(photo_r, (faces[0][0], faces[0][1]), (faces[0][2] + faces[0][0], faces[0][3] + faces[0][1]),
                           (0, 255, 0), 2)

    # Определение размера лица в процентах относительно размера всего изображения
    s_photo = frame2.shape[0] * frame2.shape[1]
    s_frame = (faces[0][2]) * (faces[0][3])
    proc = (s_frame / s_photo) * 100
    print(s_photo)
    print(s_frame)
    print(proc)

    # Создание слоёв частнотного разложения
    i = 1
    doc.selection.selectAll()
    doc.selection.copy()
    layer_set = doc.layerSets.add()
    while i <= 3:
        layer = doc.artLayers.add()
        doc.paste()
        layer.move(layer_set, ps.ElementPlacement.PlaceInside)
        i += 1
    layer_set.name = 'Fr'

    # Присваивание значений фильтру в зависимости от размера лица

    if proc <= 1.5:
        x = 2
    elif 1.5 < proc <= 3:
        x = 3
    elif 3 < proc <= 5:
        x = 4
    elif 5 < proc <= 10:
        x = 5
    elif 10 < proc <= 20:
        x = 7
    else:
        x = 10
    y = 3 * x

    # Применение фильтров к слоям
    gr_layer = layer_set.layers.item
    gr_layer(1).applyHighPass(x)
    gr_layer(1).adjustBrightnessContrast(0, -50)
    gr_layer(1).blendMode = phs.BlendMode.LinearLight
    gr_layer(1).name = 'X = {}'.format(x)
    gr_layer(2).applyHighPass(y)
    gr_layer(2).applyGaussianBlur(x)
    gr_layer(2).adjustBrightnessContrast(0, -50)
    gr_layer(2).blendMode = phs.BlendMode.LinearLight
    gr_layer(2).name = 'X = {0} Y = {1}'.format(x, y)
    gr_layer(3).applyGaussianBlur(y)
    gr_layer(3).name = 'X = {}'.format(y)

    ps.alert('Готово!')


fr_auto()
