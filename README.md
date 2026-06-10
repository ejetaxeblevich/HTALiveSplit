# HTALiveSplit
Автосплиттер для спидранов оригинальной Ex Machina, других ее частей, а также любых ее модов вместе с [таймером LiveSplit](https://github.com/LiveSplit/LiveSplit).

### Note: Please translate this text, if it necessary.

## Возможности
- Запускает ран по началу новой игры;
- Ставит таймер на паузу во время загрузок;
- Переключает сплиты по выполненным квестам определенной категории;
- Пользователь может легко менять существующие и создавать новые настройки категории конкретного мода.

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
╠═ HTALiveSplit_readme.txt
╠═ HTALiveSplit_config.json
╚═ HTALiveSplit.exe
```
2. Убедитесь, что в `HTALiveSplit_config.json` корректно указаны данные:
- `GLOBALPATH_EXMACHINA_LOG`  - Полный путь к `exmachina.log`, с обратными слешами `\\`;
- `GLOBALPATH_SPLITS`         - Полный путь к `.json` файлу нужной категории рана, с обратными слешами `\\`;
- `LIVESPLIT_HOST`            - IP-адрес локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, строкой. *Не меняйте, если указан по умолчанию*;
- `LIVESPLIT_PORT`            - Порт IP-адреса локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, числом. *Не меняйте, если указан по умолчанию*;
- `LIVESPLIT_TCP_COMMAND_...` - Набор корректных команд TCP-сервера LiveSplit для отправки HTALiveSplit, строкой. *Изменяйте, если ваш LiveSplit не реагирует на текущие версии команд*;
- `MATCH_...`                 - Набор корректных событий `.log` файла игры для контроля HTALiveSplit, строкой. *Не меняйте, если работают правильно*.
Настройки паузы:
- `LIVESPLIT_PAUSE_WhenLevelLoading` - Таймер ставится на паузу при загрузке карты, если `true`;
- `LIVESPLIT_PAUSE_WhenSaveLoading`  - Таймер ставится на паузу при загрузке сохранения, если `true`;
- `LIVESPLIT_PAUSE_WhenGameSaving`   - Таймер ставится на паузу при сохранении игры, если `true`.
   
3. Запустите LiveSplit;

4. Выберите и укажите желаемую категорию рана:
- `HTALiveSplits_Original_LisaRoute`        - Ран оригинальной игры по ветке с оказанием помощи Лисе в начале игры;
- `HTALiveSplits_Original_WithoutLisaRoute` - Ран оригинальной игры по ветке с отказом в помощи Лисе в начале игры;
- `...`                                     - Могут быть любые ваши категории и настройки.
- - **Файл настроек** `.json` укажите в config HTALiveSplit.
- - **Файл сплитов** `.lss` откройте в LiveSplit.

5. В LiveSplit запустите TCP Server: `ПКМ по LiveSplit` -> `Control` -> `Start TCP Server`;

6. Запустите `HTALiveSplit.exe` или python-код, отслеживайте его работу по открывшемуся терминалу или логу, сообщайте об ошибках <3;

7. Ставьте рекорды!

### Использовано:
- Visual Studio Code
- Python v3.12.4
- Flet v0.24.1

### Компиляция:
cd C:\Users\axeble\Desktop\HTALiveSplit
```powershell
python -m nuitka --onefile HTALiveSplit.py --windows-company-name="E Jet a.k.a. axeble" --windows-product-name="HTALiveSplit" --windows-file-version=0.1 --windows-file-description="Autosplitter HTALiveSplit" --windows-console-mode=enable
```
