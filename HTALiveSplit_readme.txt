HTALiveSplit v1.0

Автосплиттер для спидранов Ex Machina/Hard Truck Apocalypse с LiveSplit на Python с json. В папке `HTALiveSplitLOG` создает логи всех событий.

- Запускает ран по началу новой игры;
- Ставит таймер на паузу во время загрузок;
- Переключает сплиты по выполненным квестам определенной категории.

Использование:
1. Проверьте комплектацию файлов. В папке `HTALiveSplits` находятся доступные категории рана:
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

2. Убедитесь, что в `HTALiveSplit_config.json` корректно указаны данные:
    2.1 `GLOBALPATH_EXMACHINA_LOG`  - Полный путь к exmachina.log, с обратными слешами "\\";
    2.2 `GLOBALPATH_SPLITS`         - Полный путь к .json файлу нужной категории рана, с обратными слешами "\\";
    2.3 `LIVESPLIT_HOST`            - IP-адрес локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, строкой. Не меняйте, если указан по умолчанию;
    2.4 `LIVESPLIT_PORT`            - Порт IP-адреса локального TCP-сервера LiveSplit для отправки команд HTALiveSplit, числом. Не меняйте, если указан по умолчанию;
    2.5 Настройки паузы:
        2.5.1 `LIVESPLIT_PAUSE_WhenLevelLoading` - Таймер ставится на паузу при загрузке карты, если true;
        2.5.2 `LIVESPLIT_PAUSE_WhenSaveLoading`  - Таймер ставится на паузу при загрузке сохранения, если true;
        2.5.3 `LIVESPLIT_PAUSE_WhenGameSaving`   - Таймер ставится на паузу при сохранении игры, если true.
    2.6 `LIVESPLIT_TCP_COMMAND_...` - Набор корректных команд TCP-сервера LiveSplit для отправки HTALiveSplit, строкой. Изменяйте, если ваш LiveSplit не реагирует на текущие версии команд;
    2.7 `MATCH_...`                 - Набор корректных событий .log файла игры для контроля HTALiveSplit, строкой. Не меняйте, если указаны по умолчанию.

3. Запустите LiveSplit;

4. Выберите и укажите желаемую категорию рана:
    3.1 `HTALiveSplits_Original_LisaRoute`        - Ран оригинальной игры по ветке с оказанием помощи Лисе в начале игры;
    3.2 `HTALiveSplits_Original_WithoutLisaRoute` - Ран оригинальной игры по ветке с отказом в помощи Лисе в начале игры;
    3.3 `...`                                     - Могут быть любые ваши категории и настройки.
    - Файл настроек .json укажите в config HTALiveSplit.
    - Файл сплитов .lss откройте в LiveSplit.

5. В LiveSplit запустите TCP Server: ПКМ -> `Control` -> `Start TCP Server`;

6. Запустите `HTALiveSplit.exe`, отслеживайте его работу по открывшемуся терминалу Windows, сообщайте об ошибках;

7. Ставьте рекорды!
