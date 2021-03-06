# dynamic-photo-vk
Смена изображений на фото ВКонтакте 20 раз в день

Требуется Python 3 + библиотека requests  
```
pip3 install requests -U
```

Запуск:
```
python3 rollphotos.py my_profile
```

Для использования нескольких профилей можно создать в папке `photos` папку с тем же названием, что и у файла профиля из
`profiles` и переместить фото в нее. Если этого не сделать, фото будут выбираться из папки `photos`

Через какое-то время фотография может перестать обновляться, тогда нужно с ПК открыть добавление эффектов на фото и 
нажать "Восстановить оригинал"

### Требования к изображениям:

Коротко: изображениям лучше быть одного размера

Развернуто: Изображения могут быть разных размеров, но если изображение другого размера установлено как фотография 
профиля и выбранная для отображения на странице область не поместится в новом изображении (размер области вместе с 
отступом больше размера новой фотографии), то произойдет ошибка.

### Перед запуском:

В папку photos добавить изображения  
Добавить ВК одно фото из папки

В папке profiles создать файл, его название будет названием профиля  
В него с новой строки добавить данные в таком порядке:
```
photo_id (id загруженной фотографии)
p_cookie
l_cookie (id пользователя ВК)
user_agent
remixttpid (только если включено подтверждение входа ВК)
```
p_cookie нужно искать в списке куки для домена login.vk.com  
remixttpid в списке куки для домена vk.com  
Например, в chrome куки тут: chrome://settings/siteData  

user_agent нужен именно тот, с которого вы авторизированы ВК  
Посмотреть его можно так:  
1) Нажать f12  
2) Открыть вкладку Network  
3) Выбрать любой пакет  
4) Промотать к request headers  
5) Найти user-agent и скопировать его  

#### Пример файла с настройками:
```
456322547
ce0dde27d6c9d8dc8dfd63aaa50c0b5481d8b4ee8365f9861daa3
55581578
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36
410f99b22cc22a38383aa777d33df6a6aaeee83ddd
```

## Docker

```sh
# git clone https://github.com/skorpionikus/dynamic-photo-vk && cd dynamic-photo-vk
docker build -t dynamic-photo-vk .
docker run -d --name dynamic-photo-vk \
    -v <path to photos directory>:/code/photos \
    -v <path to profiles directory>:/code/profiles  \
    dynamic-photo-vk python rollphotos.py my_profile
```
