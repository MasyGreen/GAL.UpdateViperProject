@ECHO OFF
CHCP 65001
CLS
@ECHO =====================Attention!!!============================
@ECHO Запуск всех _DelTempRename.bat в подкаталгах от текущего (скопровать в корень проекта Заказчика)
@ECHO =====================Attention!!!============================

powershell write-host -back Green START %username% at: %date% - %time% Удаление временных файлов


rem Сохраняем исходный каталог для возврата после выполнения
pushd "%~dp0"

rem Начинаем рекурсивный поиск файлов
for /r %%f in (_DelTempRename.bat) do (
    rem Проверяем, существует ли файл
    if exist "%%f" (
        rem Получаем путь к папке с найденным файлом
        for %%d in ("%%~dpf") do (
            rem Меняем каталог напрямую
            cd /d "%%~fd"
            
            rem Проверяем успешность смены каталога
            if errorlevel 1 (
                echo Ошибка при смене каталога: %%~fd
                continue
            )
            
            rem Выводим путь к найденному файлу
            powershell -Command "Write-Host -ForegroundColor Blue 'Запуск файла: %%f'"
			
            rem Запускаем найденный файл с правильным рабочим каталогом
            call "%%f"
            
            rem Возвращаемся в исходный каталог
            popd
            
            rem Переходим обратно в корневой каталог для поиска
            pushd "%~dp0"
        )
    )
)

popd
powershell write-host -back Green END %username% at: %date% - %time%
pause