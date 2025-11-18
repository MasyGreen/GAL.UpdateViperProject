# Назначение
Обновление проекта(ов) Viper Галактика ERP + очистка от мусора.

* Ожидается, что все файлы проектов в подкаталогах обработки - **_project.vpr**
* Предыдущая версия **_project.vpr** сохраняются как **_project_save.vpr** 
* Функционал преобразовывает **_project.vpr** в соответствии указанных параметров дополнительно очищая от 'мусора' 

# Параметры

Файл параметров **config.json** создается при первом запуске 

| Параметр         |                    Назначение |
|:-----------------|------------------------------:|
| folder_process   | Каталог верхнего уровня *.vpr |
| folder_galaktika |                    Путь к Gal |
| folder_viper     |        Путь к компилятору Vip |
| folder_hwkey     |                          Ключ |
| path_lic_support |     Лицензионный файл Support |
| sql_database     |               База сборки SQL |
| sql_server       |     Соединение с сервером SQL |

Например:

```json
{
  "folder_galaktika": "C:\\Galaktika",
  "folder_hwkey": "192.168.X.x:55555",
  "folder_process": "C:\\ClientProjects",
  "folder_viper": "c:\\Program Files (x86)\\Galaktika Corp\\Viper 5.5\\bin\\5.5.41.0",
  "path_lic_support": "C:\\Galaktika\\Support\\sup_sql.lic",
  "sql_database": "DBName",
  "sql_server": "ncacn_ip_tcp:192.168.X.X[1997]"
}
```