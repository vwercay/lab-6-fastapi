from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Мой сайт</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f7fa;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }

            h1 {
                color: #2c3e50;
            }

            .btn {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                border-radius: 6px;
                cursor: pointer;
                margin: 10px;
            }
            .btn:hover {
                background: #2980b9;
            }

            /* Модальное окно */
            .modal {
                display: none;
                position: fixed;
                z-index: 100;
                left: 0; top: 0;
                width: 100%; height: 100%;
                background-color: rgba(0,0,0,0.5);
                justify-content: center;
                align-items: center;
            }

            .modal-content {
                background: white;
                padding: 30px;
                border-radius: 10px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                position: relative;
            }

            .close {
                position: absolute;
                top: 15px; right: 20px;
                font-size: 24px;
                cursor: pointer;
                color: #aaa;
            }
            .close:hover { color: #333; }

            .tabs {
                display: flex;
                margin-bottom: 20px;
            }
            .tab-btn {
                flex: 1;
                padding: 10px;
                background: #eee;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }
            .tab-btn.active {
                background: #3498db;
                color: white;
            }

            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }

            input {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }

            .message {
                padding: 12px;
                margin: 15px 0;
                border-radius: 4px;
                display: none;
            }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }

            .divider {
                margin: 20px 0;
                text-align: center;
                position: relative;
            }
            .divider::before {
                content: "";
                position: absolute;
                top: 50%; left: 0; right: 0;
                height: 1px;
                background: #eee;
                z-index: 0;
            }
            .divider span {
                background: white;
                padding: 0 10px;
                position: relative;
                z-index: 1;
            }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать!</h1>
        <p>Это главная страница. Нажмите кнопку ниже, чтобы войти или зарегистрироваться.</p>
        <button class="btn" onclick="openModal()">Войти / Зарегистрироваться</button>

        <!-- Модальное окно -->
        <div id="authModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>

                <div class="tabs">
                    <button class="tab-btn active" onclick="switchTab('login')">Вход</button>
                    <button class="tab-btn" onclick="switchTab('register')">Регистрация</button>
                </div>

                <div id="login-tab" class="tab-content active">
                    <h3>Вход в аккаунт</h3>
                    <form id="loginForm">
                        <input type="text" name="username" placeholder="Имя пользователя" required>
                        <input type="password" name="password" placeholder="Пароль" required>
                        <button type="submit" class="btn">Войти</button>
                    </form>
                </div>

                <div id="register-tab" class="tab-content">
                    <h3>Регистрация</h3>
                    <form id="registerForm">
                        <input type="text" name="username" placeholder="Имя пользователя" required>
                        <input type="email" name="email" placeholder="Email" required>
                        <input type="password" name="password" placeholder="Пароль" required>
                        <button type="submit" class="btn">Зарегистрироваться</button>
                    </form>
                </div>

                <div id="message" class="message"></div>
            </div>
        </div>

        <script>
            function openModal() {
                document.getElementById('authModal').style.display = 'flex';
            }
            function closeModal() {
                document.getElementById('authModal').style.display = 'none';
                document.getElementById('message').style.display = 'none';
            }

            function switchTab(tabName) {
                // переключаем кнопки
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelector(`.tab-btn[onclick="switchTab('${tabName}')"]`).classList.add('active');

                // переключаем контент
                document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                document.getElementById(tabName + '-tab').classList.add('active');
            }

            // AJAX отправка форм
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const res = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                showMessage(result.detail || 'Ошибка', result.success ? 'success' : 'error');
            });

            document.getElementById('registerForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const res = await fetch('/register', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                if (result.success) {
                    showMessage('Вы успешно зарегистрированы!', 'success');
                    // через 2 секунды закроем окно
                    setTimeout(() => {
                        closeModal();
                    }, 2000);
                } else {
                    showMessage(result.detail || 'Ошибка регистрации', 'error');
                }
            });

            function showMessage(text, type) {
                const msg = document.getElementById('message');
                msg.textContent = text;
                msg.className = 'message ' + type;
                msg.style.display = 'block';
            }

            // Закрытие по клику вне окна
            window.onclick = function(event) {
                const modal = document.getElementById('authModal');
                if (event.target === modal) closeModal();
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Просто логируем (в реальном проекте — проверка в БД)
    with open("logins.txt", "a", encoding="utf-8") as f:
        f.write(f"[LOGIN] {username}\n")
    return JSONResponse({"success": True, "detail": "Вход выполнен"})


@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    with open("registrations.txt", "a", encoding="utf-8") as f:
        f.write(f"[REGISTER] {username}, {email}\n")
    return JSONResponse({"success": True, "detail": "Регистрация успешна"})