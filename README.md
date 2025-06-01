<h1 align="center">💸 Cashflow Project / Проект учёта ДДС</h1>
<p align="center">
  <b>A modern web application for managing cash flow (ДДС – движение денежных средств), built with Django and SQLite.</b><br>
  <b>Веб‑приложение для управления движением денежных средств (ДДС), созданное на Django и SQLite.</b>
</p>

<p align="center">
  <a href="#features--возможности">Возможности</a> •
  <a href="#tech-stack--технологии">Технологии</a> •
  <a href="#installation--установка">Установка</a> •
  <a href="#admin-panel--админ-панель">Админ-панель</a> •
  <a href="#screenshots--скриншоты">Скриншоты</a> •
  <a href="#author--автор">Автор</a>
</p>

---

## 🚀 Features / Возможности

- **Create, edit, delete, and view** cash flow records  
  **Создание, редактирование, удаление и просмотр** записей о движении денежных средств
- **Record fields / Поля записи:**
  - **Date** (auto‑filled, editable) / **Дата** (заполняется автоматически, редактируемая)
  - **Status** – Business, Personal, Tax (editable list)  
    **Статус** – Бизнес, Личное, Налог (редактируемый список)
  - **Type** – Income, Expense (editable list)  
    **Тип** – Пополнение, Списание (редактируемый список)
  - **Category** and **Subcategory** (hierarchical, user‑defined)  
    **Категория** и **Подкатегория** (иерархические, настраиваемые пользователем)
  - **Amount** in RUB / **Сумма** в рублях
  - Optional **Comment** / Необязательный **Комментарий**
- **Filter** records by date, status, type, category, subcategory  
  **Фильтрация** по дате, статусу, типу, категории и подкатегории
- **Manage reference lists** (status, type, category, subcategory)  
  **Управление справочниками** (статус, тип, категория, подкатегория)
- **Logical dependencies / Логические зависимости:**
  - Categories belong to specific types  
    Категории привязаны к определённым типам
  - Subcategories belong to specific categories  
    Подкатегории привязаны к категориям
- **Validation** on both client and server sides  
  **Валидация данных** на стороне клиента и сервера

---

## 🛠️ Tech Stack / Технологии

| Layer / Уровень      | Technology / Технология          |
|----------------------|----------------------------------|
| Backend / Сервер     | Django 4.x                       |
| Database / БД        | SQLite                           |
| Frontend / Фронтенд  | Django templates + Bootstrap     |
| Admin / Админка      | Django Admin (расширенная)       |

---

## ⚡ Installation / Установка

<details>
<summary><b>Step-by-step / Пошаговая инструкция</b></summary>

### 1. Clone the repository / Клонировать репозиторий
```bash
git clone https://github.com/BarGhasH17/Cashflow_project.git
cd Cashflow_project
```

### 2. Create a virtual environment / Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies / Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Apply migrations / Применить миграции
```bash
python manage.py migrate
```

### 5. (Optional) Create superuser / Создать суперпользователя (по желанию)
```bash
python manage.py createsuperuser
```

### 6. Run the server / Запустить сервер
```bash
python manage.py runserver
```

</details>

<p align="center">
  Open in browser / Открыть в браузере:<br>
  <a href="http://127.0.0.1:8000/" target="_blank"><b>http://127.0.0.1:8000/</b></a>
</p>

---

## ⚙️ Admin Panel / Админ-панель

- URL: <a href="http://127.0.0.1:8000/admin/" target="_blank">http://127.0.0.1:8000/admin/</a>
- Manage all records and reference lists  
  Управление всеми записями и справочниками

---

## 🖼️ Screenshots / Скриншоты

<p align="center">
  <img src="https://github.com/user-attachments/assets/95070ca6-613c-4c32-b473-a4faceed26e8" alt="screenshot-1" width="700"/><br>
  <img src="https://github.com/user-attachments/assets/c0bf45ae-1e2e-4865-99a9-cea7c69441bf" alt="screenshot-2" width="700"/><br>
  <img src="https://github.com/user-attachments/assets/f7fa656c-7ee2-4b64-87d8-b8237089867c" alt="screenshot-3" width="700"/><br>
  <img src="https://github.com/user-attachments/assets/9dc30e9b-2b66-487d-ada2-671a08b5fad4" alt="screenshot-4" width="700"/>
</p>

---

## 👤 Author / Автор

<p align="center">
  <b>Kipiani Edisheri Nodarovich</b>
</p>