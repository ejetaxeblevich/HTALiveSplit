# HTALiveSplit
Автосплиттер для спидранов оригинальной Ex Machina, других ее частей, а также любых ее модов вместе с [таймером LiveSplit](https://github.com/LiveSplit/LiveSplit).

> [!NOTE]
> 🇬🇧 ***English description [here](README_en.md)***.

<div align="center">
    
![LiveSplitScreenshot.png](LiveSplitScreenshot.png)

</div>

## Возможности
- Запускает ран по началу новой игры;
- Ставит таймер на паузу во время загрузок;
- Переключает сплиты по выполненным квестам определенной категории;
- Пользователь может легко менять существующие и создавать новые настройки категории конкретного мода.

> [!WARNING]
> *Читает события из `.log` файла игры, что может вызывать неточное время.*
> > Всяко лучше, чем вручную нажимать кнопку сплита.

## [Видео с демонстрацией работы](https://youtu.be/oVrpQL6um7E)

## Использование
1. Проверьте комплектацию файлов. В папке `HTALiveSplits` находятся доступные категории рана:
```
\HTALiveSplit\
╠═ \HTALiveSplitLOG\
╠═ \HTALiveSplits\
    ╠═ HTALiveSplits_Original_LisaRoute.json
    ╠═ HTALiveSplits_Original_LisaRoute.lss
    ╠═ HTALiveSplits_Original_WithoutLisaRoute.json
    ╠═ HTALiveSplits_Original_WithoutLisaRoute.lss
    ╚═ ...
╠═ HTALiveSplit_Layout_by_E_Jet.lsl
╠═ HTALiveSplit_config.json
╚═ HTALiveSplit.exe
```
2. Убедитесь, что в `HTALiveSplit_config.json` корректно указаны данные:

| Ключ | Значение |
|-----------|-----------|
| `GLOBALPATH_EXMACHINA_LOG` | Полный путь к `exmachina.log`, с обратными слешами `\\` |
| `GLOBALPATH_SPLITS` | Полный путь к `.json` файлу нужной категории рана, с обратными слешами `\\` |
| `LIVESPLIT_HOST` | IP-адрес локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, строкой. *Не меняйте, если указан по умолчанию* |
| `LIVESPLIT_PORT` | Порт IP-адреса локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, числом. *Не меняйте, если указан по умолчанию* |
| `LIVESPLIT_TCP_COMMAND_...` | Набор корректных команд TCP-сервера LiveSplit для отправки HTALiveSplit, строкой. *Изменяйте, если ваш LiveSplit не реагирует на текущие версии команд* |
| `MATCH_...` | Набор корректных событий `.log` файла игры для контроля HTALiveSplit, строкой. *Не меняйте, если работают правильно* |

Настройки паузы:

| Ключ | Значение |
|-----------|-----------|
| `LIVESPLIT_PAUSE_WhenLevelLoading` | Таймер ставится на паузу при загрузке карты, если `true` |
| `LIVESPLIT_PAUSE_WhenSaveLoading` | Таймер ставится на паузу при загрузке сохранения, если `true` |
| `LIVESPLIT_PAUSE_WhenGameSaving` | Таймер ставится на паузу при сохранении игры, если `true` |
   
3. Запустите LiveSplit;

4. Выберите и укажите желаемую категорию рана:

| Ключ | Значение |
|-----------|-----------|
| `HTALiveSplits_Original_LisaRoute` | Ран оригинальной игры по ветке с оказанием помощи Лисе в начале игры |
| `HTALiveSplits_Original_WithoutLisaRoute` | Ран оригинальной игры по ветке с отказом в помощи Лисе в начале игры |
| `...` | Могут быть любые ваши категории и настройки |
- **Файл настроек** `.json` укажите в config HTALiveSplit.
- **Файл сплитов** `.lss` откройте в LiveSplit.

5. В LiveSplit запустите TCP Server: `ПКМ по LiveSplit` -> `Control` -> `Start TCP Server`;
   
6. В LiveSplit включите Game Time: `ПКМ по LiveSplit` -> `Compare Against` -> `Game Time`;

7. Запустите `HTALiveSplit.exe` или python-код, отслеживайте его работу по открывшемуся терминалу или логу, сообщайте об ошибках❤️;

8. Ставьте рекорды!

## Как редактировать категории
Вы можете самостоятельно сделать сплиты для своего мода!

1. Откройте образец конфигурации `HTALiveSplits_Original_LisaRoute.json` для HTALiveSplit:

| Ключ | Значение |
|-----------|-----------|
| `LOCALPATH_EXMACHINA_MAINMENULEVEL` | Локальный путь внутри папки игры (там где лежит `.exe` файл) до имени карты `.ssl` ***главного меню***. Автосплиттер поймет, когда вы вышли в главное меню |
| `LOCALPATH_EXMACHINA_FIRSTLEVEL` | Локальный путь внутри папки игры (там где лежит `.exe` файл) до имени карты `.ssl` ***начала игры***. Автосплиттер поймет, когда вы начали новую игру |
| `SPLIT_QUESTS` | Список технических имен ключевых квестов вашего мода/игры. Когда один из этих квестов будет `is complete` *(или чо там в его `MATCH`)*, автосплиттер сделает сплит сегмента таймера |
| `SPLIT_LEVELS` | Список технических имен карт вашего мода/игры *(как в `LOCALPATH_...`)*. Когда будет переход на одну из этих карт впервые, автосплиттер сделает сплит сегмента таймера |
| `SPLIT_CUSTOM` | Список любых других LOG-строк вашего мода/игры. Когда в логе будет одно из этих совпадений, автосплиттер сделает сплит сегмента таймера |

2. Создайте свой `.json` файл с нужными настройками под ваш мод. Вспомните, как идут сюжетные квесты и добавьте нужные из них в `SPLIT_QUESTS`;

3. В LiveSplit откройте редактор сплитов: `ПКМ по LiveSplit` -> `Edit Splits...`;

4. В редакторе сплитов LiveSplit очистите все сегменты и добавьте свои, называя ключевыми словами. Используйте кнопки слева. **Важно!** Количество квестов в `SPLIT_QUESTS` должно быть равным или больше, чем количество сегментов в LiveSplit;

5. Когда заполните, нажмите `ОК`;

6. Сохраните получившиеся сегменты в редакторе сплитов LiveSplit: `ПКМ по LiveSplit` -> `Save Splits As...`;

7. Протестируйте работоспособность таймера;

8. Соревнуйтесь с другими, кому интересен ваш мод!


### Использовано:
- Visual Studio Code
- Python v3.12.4

### Компиляция:

[comment]: <> (cd C:\Users\axeble\Desktop\HTALiveSplit)

```powershell
python -m nuitka --onefile HTALiveSplit.py --windows-company-name="E Jet a.k.a. axeble" --windows-product-name="HTALiveSplit" --windows-file-version=1.2 --windows-file-description="Autosplitter HTALiveSplit" --windows-console-mode=force
```
