#  SandMail Z

Cliente de correo de escritorio escrito **100% en Python con Tkinter**, pensado para funcionar en PCs modestas (2 GB de RAM) y sin dependencias pesadas.

Envío real por SMTP, recepción por IMAP, múltiples cuentas, adjuntos, modo oscuro y 7 idiomas.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

##  Tabla de contenidos

- [Características](#-características)
- [Capturas](#-capturas)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Configuración de cuentas](#-configuración-de-cuentas)
- [Atajos de teclado](#-atajos-de-teclado)
- [Solución de problemas](#-solución-de-problemas)
- [Aviso sobre servidores SMTP propios](#-aviso-sobre-servidores-smtp-propios)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

---

##  Características

| Función | Descripción |
|---|---|
| **Múltiples cuentas** | Gmail, Outlook y SandMail Z en un solo selector de la cabecera. |
| **Envío real** | SMTP con SSL/TLS para Gmail (465), Outlook (587) y cualquier servidor propio. |
| **Recepción IMAP** | Lectura de la bandeja de entrada de Gmail con doble clic para abrir el correo. |
| **Adjuntos** | Envía archivos de cualquier tipo. |
| **HTML o texto plano** | Checkbox para elegir el formato del cuerpo. |
| **Prioridad** | Marca el asunto con `[Normal]`, `[Alta]` o `[Baja]`. |
| **Keyring** | Guarda las credenciales de forma segura en el llavero del sistema. |
| **Modo oscuro / claro** | Cambio instantáneo con `F5`. |
| **Dos estilos visuales** | *Aero* (Vista/7) y *Minimalista* (Win 11), con `F6`. |
| **7 idiomas** | ES, EN, PT, FR, JA, RU y AR. |
| **SandAI** | Asistente que sugiere respuestas rápidas. |
| **Mover a papelera / Marcar leído** | Acciones IMAP directas sobre los correos reales. |
| **Pestañas extra** | Contactos, Calendario y Tareas (vista previa). |

---

##  Capturas

<img width="1275" height="788" alt="Captura de pantalla 2026-10-06 211653" src="https://github.com/user-attachments/assets/129b4f2c-ea32-4ad0-8359-d0447c6908d0" />

---

##  Requisitos

- **Python 3.10 o superior** (probado en 3.14).
- **Tkinter** — normalmente viene incluido con Python. En Linux puede requerir:
  ```bash
  sudo apt install python3-tk
  ```
- **Opcional pero recomendado:**
  ```bash
  pip install keyring
  ```
  Solo necesario para guardar credenciales de forma segura. Sin keyring, la app funciona igual pero no recuerda las contraseñas.

No hay más dependencias. Todo lo demás es **librería estándar**.

---

##  Instalación


1. Clona el repositorio:
   ```bash
   git clone https://github.com/David4524-maker/sandmail-z.git
   cd sandmail-z
   ```

2. (Opcional) Instala keyring:
   ```bash
   pip install keyring
   ```

3. Ejecuta:
   ```bash
   python sendmail_z.py
   ```

También puedes descargar el `.py` suelto y ejecutarlo con doble clic si tienes Python asociado.

---

##  Uso

1. Abre la pestaña **Ajustes** y configura tu cuenta (Gmail, Outlook o SandMail Z).
2. Pulsa **Guardar**.
3. Verás tu cuenta en el desplegable **Cuenta:** de la esquina superior derecha.
4. Ve a la pestaña **Nuevo** para redactar, o **Correo** → **Cargar Reales** para descargar los últimos 20 correos de Gmail.
5. Doble clic sobre un correo para leerlo.

---

##  Configuración de cuentas

### Gmail

1. Activa la **verificación en dos pasos** en tu cuenta de Google.
2. Genera una **Contraseña de Aplicación** en <https://myaccount.google.com/apppasswords>.
3. Activa **IMAP** en Gmail → Configuración → Reenvío y correo POP/IMAP.
4. En SandMail Z, pestaña **Ajustes**, pon:
   - Correo: Tu correo de Gmail
   - Contraseña: la **Contraseña de Aplicación** (16 letras, no tu contraseña normal).

### Outlook

- Correo y contraseña normales de tu cuenta Microsoft.
- Requiere que tu organización permita SMTP con autenticación básica.

### SandMail Z (SMTP propio)

- Sirve para cualquier proveedor con SMTP (Brevo, Zoho, Mailcow, tu VPS…).
- Rellena **Correo**, **Contraseña**, **Servidor SMTP** y **Puerto**.
- Si dejas el correo o la contraseña vacíos, la app entra en **modo demo** (envío simulado).

---

##  Atajos de teclado

| Tecla | Acción |
|---|---|
| `Ctrl + Enter` | Enviar el correo |
| `Ctrl + S` | Guardar borrador |
| `Ctrl + N` | Nueva pestaña de redacción |
| `F5` | Alternar modo oscuro / claro |
| `F6` | Cambiar entre estilo Aero y Minimalista |

---

##  Solución de problemas

**"No se pudo conectar a Gmail"**
- Verifica que la contraseña sea una **Contraseña de Aplicación**, no la normal.
- Asegúrate de que IMAP esté habilitado en Gmail.
- Comprueba que el correo esté escrito completo (`tu@gmail.com`).

**"Name or service not known" al enviar por SandMail Z**
- El servidor SMTP configurado no existe. Si no tienes servidor propio, **deja las credenciales vacías** para usar el modo demo, o usa Gmail/Outlook.

**Error de autenticación en Outlook**
- Microsoft bloquea la autenticación básica en muchas cuentas personales. Usa Gmail o un SMTP propio si te pasa esto.

**La app no recuerda las credenciales**
- Instala keyring: `pip install keyring`.

**El correo llega a spam**
- Es normal si envías desde un servidor propio sin **SPF, DKIM, DMARC** configurados. Usa un proveedor serio (Gmail, Brevo, Zoho) para evitarlo.

---

##  Aviso sobre servidores SMTP propios

SandMail Z puede enviar a través de **cualquier servidor SMTP**, pero si quieres usar tu propio dominio (ej. `@tudominio.com`) **no basta con levantar un servidor en Python**. Necesitas:

1. Un dominio real registrado.
2. Registros DNS: **SPF**, **DKIM** y **DMARC**.
3. IP pública con **PTR** apuntando a tu dominio.
4. Puerto 25 abierto (la mayoría de ISPs lo bloquean en conexiones domésticas).

Por eso se recomienda usar un **proveedor SMTP profesional** (Brevo, Zoho, Resend, Mailgun) o un VPS con **Mailcow / Mailu / iRedMail** en lugar de montar el servidor desde cero.

> Un servidor **HTTP** (tipo `http.server`) no sirve para esto: HTTP y SMTP son protocolos distintos.

---

##  Estructura del proyecto

```
sandmail-z/
├── sendmail_z.py      # Aplicación completa (un solo archivo)
├── README.md
├── LICENSE
└── requirements.txt   # Opcional: solo keyring
```

Todo el código está en un único archivo por simplicidad y portabilidad.

---

## Otras alternativas

[Google Gmail](https://mail.google.com/mail/u/0/)

[Apple Mail](https://www.icloud.com/es-mx/mail)

[Outlook](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=9199bf20-a13f-4107-85dc-02114787ef48&scope=https%3A%2F%2Foutlook.office.com%2F.default%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Foutlook.cloud.microsoft%2Fmail%2F&client-request-id=f317623e-ba6f-4097-14d3-b4da9c3412a1&response_mode=fragment&client_info=1&clidata=1&prompt=select_account&nonce=01a11498-2e62-7a6d-8179-5400569d6d36&state=eyJpZCI6IjAxYTExNDk4LTJlNjItN2UxOS1hZWQ4LWM4ZmMyN2RhMGVlMiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D%7CaHR0cHM6Ly9vdXRsb29rLmNsb3VkLm1pY3Jvc29mdC9tYWlsLw&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22CP1%22%5D%7D%7D%7D&x-client-SKU=msal.js.browser&x-client-VER=5.12.0&response_type=code&code_challenge=WyNe9mnfl7JdcWdKesN39rTFT43F97x_f7UqjKIFETI&code_challenge_method=S256&sso_reload=true)

[Samsung Email](https://galaxystore.samsung.com/detail/com.samsung.android.email.provider)

[Yahoo Mail](https://login.yahoo.com/?.src=ym&pspid=&activity=mail-direct&.lang=en-US&.intl=us&tsid=t2qy3yfm6henm7&.done=https%3A%2F%2Fmail.yahoo.com%2Fn%2F%3Ftsid%3Dt2qy3yfm6henm7)

---

##  Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Puedes usarlo, modificarlo y compartirlo libremente, siempre que conserves el aviso de copyright.

---

> ¿Sugerencias, bugs o ideas? Abre un **issue** o manda un **PR**
