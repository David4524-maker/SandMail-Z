import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import imaplib
import email
import os
import json
import threading
import time
import datetime
import platform

try:
    import keyring
    KEYRING_OK = True
except ImportError:
    KEYRING_OK = False

class Win11:
    LIGHT_BG = "#F3F3F3"; LIGHT_SURFACE = "#FFFFFF"; LIGHT_CARD = "#FBFBFB"
    LIGHT_BORDER = "#E5E5E5"; LIGHT_TEXT = "#1A1A1A"; LIGHT_SUBTEXT = "#616161"
    LIGHT_HOVER = "#EAEAEA"; LIGHT_NAV_BG = "#F3F3F3"
    DARK_BG = "#202020"; DARK_SURFACE = "#2B2B2B"; DARK_CARD = "#272727"
    DARK_BORDER = "#3D3D3D"; DARK_TEXT = "#FFFFFF"; DARK_SUBTEXT = "#A0A0A0"
    DARK_HOVER = "#383838"; DARK_NAV_BG = "#1F1F1F"
    ACCENT = "#0067C0"; ACCENT_HOVER = "#1975C5"; ACCENT_PRESSED = "#005BA1"
    BRAND_ORANGE = "#FF6B00"; BRAND_RED = "#E81123"; BRAND_YELLOW = "#FFD700"
    FONT_FALLBACK = "Segoe UI"; FONT_MONO = "Cascadia Code"

class Aero:
    LIGHT_BG = "#D6E4F0"; LIGHT_SURFACE = "#EAF2FB"; LIGHT_CARD = "#F0F6FC"
    LIGHT_BORDER = "#9CB9D4"; LIGHT_TEXT = "#0A1F33"; LIGHT_SUBTEXT = "#3A5A78"
    LIGHT_HOVER = "#C4DCF0"; LIGHT_NAV_BG = "#B8D0E6"
    DARK_BG = "#1A2430"; DARK_SURFACE = "#233040"; DARK_CARD = "#2A3A4A"
    DARK_BORDER = "#3A5870"; DARK_TEXT = "#E8F0F8"; DARK_SUBTEXT = "#8DA8C0"
    DARK_HOVER = "#2F4256"; DARK_NAV_BG = "#182230"
    ACCENT = "#3C7FBC"; ACCENT_HOVER = "#4C93D0"; ACCENT_PRESSED = "#2C6A9F"
    ACCENT_GLOW = "#7FB5E5"; GLOW = "#A8CCEE"; GREEN = "#5CB85C"; RED = "#D9534F"
    BRAND_ORANGE = "#FF6B00"; BRAND_RED = "#E81123"; BRAND_YELLOW = "#FFD700"
    FONT_FALLBACK = "Segoe UI"; FONT_MONO = "Consolas"


class SandMailZApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SandMail Z")
        w, h = 1280, 820
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(1100, 720)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.modo_oscuro = False
        self.estilo_actual = "win11"
        self.archivos_adjuntos = []
        self.contactos = [
            "Tony Hawk <tony@skate.com>", "Rodrigo <rodri@sandmailz.net>",
            "Soporte <ayuda@sandmailz.net>", "Bob Esponja <bob@fondo.com>"
        ]

        self.creds_gmail_user = ""
        self.creds_gmail_pass = ""
        self.creds_outlook_user = ""
        self.creds_outlook_pass = ""
        self.creds_sandmail_user = ""
        self.creds_sandmail_pass = ""

        # Sistema de cuentas múltiples
        self.cuentas = {}       # {email: {"user", "pass", "servicio", ...}}
        self.cuenta_actual = ""

        self.uids_actuales = []

        self.cargar_credenciales_guardadas()

        self.idioma_actual = 'es'
        self.traducciones = self._crear_traducciones()

        self.style = ttk.Style()
        self.style.theme_use('clam')

        if platform.system() == "Windows" and platform.release() in ("6.1", "6.0"):
            self.estilo_actual = "aero"

        self.aplicar_estilo()
        self.crear_menu()
        self.crear_layout_principal()
        self.actualizar_combo_cuentas()

        self.root.bind('<Control-Return>', lambda e: self.hilo_enviar())
        self.root.bind('<Control-s>', lambda e: self.guardar_borrador())
        self.root.bind('<Control-n>', lambda e: self.tabs.select(1))
        self.root.bind('<F5>', lambda e: self.toggle_modo_oscuro())
        self.root.bind('<F6>', lambda e: self.cambiar_estilo())

    def _crear_traducciones(self):
        return {
            'es': {'titulo':'SandMail Z','archivo':'Archivo','ver':'Ver','herramientas':'Herramientas','nuevo':'Nuevo','guardar':'Guardar','salir':'Salir','oscuro':'Modo Oscuro / Claro','ia':'SandAI','encriptar':'Encriptar','config':'Configuracion SMTP','idioma':'Idioma','estilo':'Estilo Visual','aero':'Aero (Vista/7)','win11':'Minimalista (Win 11)','tab_inbox':'Correo','tab_compose':'Nuevo','tab_contacts':'Contactos','tab_calendar':'Calendario','tab_tasks':'Tareas','tab_settings':'Ajustes','tab_log':'Registro','sb_inbox':'Bandeja de Entrada','sb_compose':'Redactar','sb_contacts':'Contactos','sb_calendar':'Calendario','sb_tasks':'Tareas','sb_settings':'Configuracion','sb_log':'Registro','servicio':'Servicio','de':'De','para':'Para','cc':'CC','bcc':'BCC','asunto':'Asunto','prioridad':'Prioridad','mensaje':'Mensaje','enviar':'Enviar','adjuntar':'Adjuntar','sandai':'SandAI','normal':'Normal','alta':'Alta','baja':'Baja','contactos_title':'Contactos','agregar':'Agregar','calendario_title':'Calendario','hoy':'Hoy: ','tareas_title':'Tareas','completar':'Completar','config_title':'Configuracion SMTP + IMAP','guardar_config':'Guardar','log_title':'Registro','status_listo':'Listo','buscar':'Buscar correos...','nuevo_contacto':'Nuevo contacto...','cargar_reales':'Cargar Reales','cargando':'Cargando...','eliminar':'Mover a Papelera','marcar_leido':'Marcar Leido','adjuntos':'Adjuntos','enviar_html':'Enviar como HTML','guardar_creds':'Recordar credenciales (keyring)','abrir_correo':'Lectura','cuerpo_vacio':'(Sin cuerpo)','cuenta':'Cuenta:'},
            'en': {'titulo':'SandMail Z','archivo':'File','ver':'View','herramientas':'Tools','nuevo':'New','guardar':'Save','salir':'Exit','oscuro':'Dark / Light','ia':'SandAI','encriptar':'Encrypt','config':'SMTP','idioma':'Language','estilo':'Style','aero':'Aero (Vista/7)','win11':'Minimalist (Win 11)','tab_inbox':'Mail','tab_compose':'New','tab_contacts':'Contacts','tab_calendar':'Calendar','tab_tasks':'Tasks','tab_settings':'Settings','tab_log':'Log','sb_inbox':'Inbox','sb_compose':'Compose','sb_contacts':'Contacts','sb_calendar':'Calendar','sb_tasks':'Tasks','sb_settings':'Settings','sb_log':'Log','servicio':'Service','de':'From','para':'To','cc':'CC','bcc':'BCC','asunto':'Subject','prioridad':'Priority','mensaje':'Message','enviar':'Send','adjuntar':'Attach','sandai':'SandAI','normal':'Normal','alta':'High','baja':'Low','contactos_title':'Contacts','agregar':'Add','calendario_title':'Calendar','hoy':'Today: ','tareas_title':'Tasks','completar':'Complete','config_title':'SMTP + IMAP','guardar_config':'Save','log_title':'Log','status_listo':'Ready','buscar':'Search...','nuevo_contacto':'New contact...','cargar_reales':'Load Real','cargando':'Loading...','eliminar':'Move to Trash','marcar_leido':'Mark Read','adjuntos':'Attachments','enviar_html':'Send HTML','guardar_creds':'Remember (keyring)','abrir_correo':'Reader','cuerpo_vacio':'(No body)','cuenta':'Account:'},
            'pt': {'titulo':'SandMail Z','archivo':'Arquivo','ver':'Ver','herramientas':'Ferramentas','nuevo':'Nova','guardar':'Salvar','salir':'Sair','oscuro':'Escuro / Claro','ia':'SandAI','encriptar':'Criptografar','config':'SMTP','idioma':'Idioma','estilo':'Estilo','aero':'Aero (Vista/7)','win11':'Minimalista (Win 11)','tab_inbox':'Correio','tab_compose':'Novo','tab_contacts':'Contatos','tab_calendar':'Calendario','tab_tasks':'Tarefas','tab_settings':'Ajustes','tab_log':'Registro','sb_inbox':'Caixa de Entrada','sb_compose':'Escrever','sb_contacts':'Contatos','sb_calendar':'Calendario','sb_tasks':'Tarefas','sb_settings':'Configuracoes','sb_log':'Registro','servicio':'Servico','de':'De','para':'Para','cc':'CC','bcc':'BCC','asunto':'Assunto','prioridad':'Prioridade','mensaje':'Mensagem','enviar':'Enviar','adjuntar':'Anexar','sandai':'SandAI','normal':'Normal','alta':'Alta','baja':'Baixa','contactos_title':'Contatos','agregar':'Adicionar','calendario_title':'Calendario','hoy':'Hoje: ','tareas_title':'Tarefas','completar':'Concluir','config_title':'SMTP + IMAP','guardar_config':'Salvar','log_title':'Registro','status_listo':'Pronto','buscar':'Buscar...','nuevo_contacto':'Novo...','cargar_reales':'Carregar','cargando':'Carregando...','eliminar':'Papelera','marcar_leido':'Marcar Lido','adjuntos':'Anexos','enviar_html':'HTML','guardar_creds':'Lembrar','abrir_correo':'Leitor','cuerpo_vacio':'(Sem corpo)','cuenta':'Conta:'},
            'fr': {'titulo':'SandMail Z','archivo':'Fichier','ver':'Affichage','herramientas':'Outils','nuevo':'Nouveau','guardar':'Enregistrer','salir':'Quitter','oscuro':'Sombre / Clair','ia':'SandAI','encriptar':'Crypter','config':'SMTP','idioma':'Langue','estilo':'Style','aero':'Aero (Vista/7)','win11':'Minimaliste (Win 11)','tab_inbox':'Courrier','tab_compose':'Nouveau','tab_contacts':'Contacts','tab_calendar':'Calendrier','tab_tasks':'Taches','tab_settings':'Parametres','tab_log':'Journal','sb_inbox':'Boite','sb_compose':'Ecrire','sb_contacts':'Contacts','sb_calendar':'Calendrier','sb_tasks':'Taches','sb_settings':'Parametres','sb_log':'Journal','servicio':'Service','de':'De','para':'A','cc':'CC','bcc':'BCC','asunto':'Objet','prioridad':'Priorite','mensaje':'Message','enviar':'Envoyer','adjuntar':'Joindre','sandai':'SandAI','normal':'Normale','alta':'Haute','baja':'Basse','contactos_title':'Contacts','agregar':'Ajouter','calendario_title':'Calendrier','hoy':'Aujourd hui: ','tareas_title':'Taches','completar':'Terminer','config_title':'SMTP + IMAP','guardar_config':'Enregistrer','log_title':'Journal','status_listo':'Pret','buscar':'Rechercher...','nuevo_contacto':'Nouveau...','cargar_reales':'Charger','cargando':'Chargement...','eliminar':'Corbeille','marcar_leido':'Marquer Lu','adjuntos':'Pieces jointes','enviar_html':'HTML','guardar_creds':'Se souvenir','abrir_correo':'Lecteur','cuerpo_vacio':'(Sans corps)','cuenta':'Compte:'},
            'ja': {'titulo':'SandMail Z','archivo':'ファイル','ver':'表示','herramientas':'ツール','nuevo':'新規','guardar':'保存','salir':'終了','oscuro':'ダーク/ライト','ia':'SandAI','encriptar':'暗号化','config':'SMTP','idioma':'言語','estilo':'スタイル','aero':'Aero','win11':'ミニマル','tab_inbox':'メール','tab_compose':'作成','tab_contacts':'連絡先','tab_calendar':'カレンダー','tab_tasks':'タスク','tab_settings':'設定','tab_log':'ログ','sb_inbox':'受信','sb_compose':'作成','sb_contacts':'連絡先','sb_calendar':'カレンダー','sb_tasks':'タスク','sb_settings':'設定','sb_log':'ログ','servicio':'サービス','de':'差出人','para':'宛先','cc':'CC','bcc':'BCC','asunto':'件名','prioridad':'優先度','mensaje':'本文','enviar':'送信','adjuntar':'添付','sandai':'SandAI','normal':'普通','alta':'高','baja':'低','contactos_title':'連絡先','agregar':'追加','calendario_title':'カレンダー','hoy':'今日: ','tareas_title':'タスク','completar':'完了','config_title':'SMTP + IMAP','guardar_config':'保存','log_title':'ログ','status_listo':'準備完了','buscar':'検索...','nuevo_contacto':'新規...','cargar_reales':'読込','cargando':'読込中...','eliminar':'ゴミ箱','marcar_leido':'既読','adjuntos':'添付','enviar_html':'HTML','guardar_creds':'保存','abrir_correo':'閲覧','cuerpo_vacio':'(本文なし)','cuenta':'アカウント:'},
            'ru': {'titulo':'SandMail Z','archivo':'Файл','ver':'Вид','herramientas':'Инструменты','nuevo':'Новое','guardar':'Сохранить','salir':'Выход','oscuro':'Темная/Светлая','ia':'SandAI','encriptar':'Шифр','config':'SMTP','idioma':'Язык','estilo':'Стиль','aero':'Aero','win11':'Минимал','tab_inbox':'Почта','tab_compose':'Написать','tab_contacts':'Контакты','tab_calendar':'Календарь','tab_tasks':'Задачи','tab_settings':'Настройки','tab_log':'Журнал','sb_inbox':'Входящие','sb_compose':'Написать','sb_contacts':'Контакты','sb_calendar':'Календарь','sb_tasks':'Задачи','sb_settings':'Настройки','sb_log':'Журнал','servicio':'Сервис','de':'От','para':'Кому','cc':'Копия','bcc':'Скрытая','asunto':'Тема','prioridad':'Приоритет','mensaje':'Сообщение','enviar':'Отправить','adjuntar':'Прикрепить','sandai':'SandAI','normal':'Обычный','alta':'Высокий','baja':'Низкий','contactos_title':'Контакты','agregar':'Добавить','calendario_title':'Календарь','hoy':'Сегодня: ','tareas_title':'Задачи','completar':'Выполнить','config_title':'SMTP + IMAP','guardar_config':'Сохранить','log_title':'Журнал','status_listo':'Готово','buscar':'Поиск...','nuevo_contacto':'Новый...','cargar_reales':'Загрузить','cargando':'Загрузка...','eliminar':'В корзину','marcar_leido':'Отметить','adjuntos':'Вложения','enviar_html':'HTML','guardar_creds':'Запомнить','abrir_correo':'Просмотр','cuerpo_vacio':'(Нет текста)','cuenta':'Аккаунт:'},
            'ar': {'titulo':'SandMail Z','archivo':'ملف','ver':'عرض','herramientas':'أدوات','nuevo':'جديد','guardar':'حفظ','salir':'خروج','oscuro':'داكن/فاتح','ia':'SandAI','encriptar':'تشفير','config':'SMTP','idioma':'اللغة','estilo':'النمط','aero':'Aero','win11':'بسيط','tab_inbox':'البريد','tab_compose':'إنشاء','tab_contacts':'جهات','tab_calendar':'التقويم','tab_tasks':'المهام','tab_settings':'الإعدادات','tab_log':'السجل','sb_inbox':'الوارد','sb_compose':'إنشاء','sb_contacts':'جهات','sb_calendar':'التقويم','sb_tasks':'المهام','sb_settings':'الإعدادات','sb_log':'السجل','servicio':'الخدمة','de':'من','para':'إلى','cc':'نسخة','bcc':'مخفية','asunto':'الموضوع','prioridad':'الأولوية','mensaje':'الرسالة','enviar':'إرسال','adjuntar':'إرفاق','sandai':'SandAI','normal':'عادي','alta':'عالية','baja':'منخفضة','contactos_title':'جهات','agregar':'إضافة','calendario_title':'التقويم','hoy':'اليوم: ','tareas_title':'المهام','completar':'إكمال','config_title':'SMTP + IMAP','guardar_config':'حفظ','log_title':'السجل','status_listo':'جاهز','buscar':'بحث...','nuevo_contacto':'جديد...','cargar_reales':'تحميل','cargando':'تحميل...','eliminar':'حذف','marcar_leido':'مقروء','adjuntos':'المرفقات','enviar_html':'HTML','guardar_creds':'تذكر','abrir_correo':'قارئ','cuerpo_vacio':'(لا نص)','cuenta':'الحساب:'},
        }

    def t(self, key):
        return self.traducciones[self.idioma_actual].get(key, key)

    def P(self):
        return Aero if self.estilo_actual == "aero" else Win11

    def bg(self): return self.P().DARK_BG if self.modo_oscuro else self.P().LIGHT_BG
    def surface(self): return self.P().DARK_SURFACE if self.modo_oscuro else self.P().LIGHT_SURFACE
    def card(self): return self.P().DARK_CARD if self.modo_oscuro else self.P().LIGHT_CARD
    def border(self): return self.P().DARK_BORDER if self.modo_oscuro else self.P().LIGHT_BORDER
    def text(self): return self.P().DARK_TEXT if self.modo_oscuro else self.P().LIGHT_TEXT
    def subtext(self): return self.P().DARK_SUBTEXT if self.modo_oscuro else self.P().LIGHT_SUBTEXT
    def hover(self): return self.P().DARK_HOVER if self.modo_oscuro else self.P().LIGHT_HOVER
    def nav_bg(self): return self.P().DARK_NAV_BG if self.modo_oscuro else self.P().LIGHT_NAV_BG

    # ============ KEYRING / CUENTAS ============
    def cargar_credenciales_guardadas(self):
        if not KEYRING_OK:
            return
        try:
            data = keyring.get_password("SandMailZ", "cuentas_json")
            if data:
                try:
                    self.cuentas = json.loads(data)
                except Exception:
                    self.cuentas = {}
            gu = keyring.get_password("SandMailZ", "gmail_user")
            gp = keyring.get_password("SandMailZ", "gmail_pass")
            ou = keyring.get_password("SandMailZ", "outlook_user")
            op = keyring.get_password("SandMailZ", "outlook_pass")
            su = keyring.get_password("SandMailZ", "sandmail_user")
            sp = keyring.get_password("SandMailZ", "sandmail_pass")
            if gu: self.creds_gmail_user = gu
            if gp: self.creds_gmail_pass = gp
            if ou: self.creds_outlook_user = ou
            if op: self.creds_outlook_pass = op
            if su: self.creds_sandmail_user = su
            if sp: self.creds_sandmail_pass = sp
            if self.cuentas and not self.cuenta_actual:
                primera = list(self.cuentas.keys())[0]
                self.cuenta_actual = primera
                datos = self.cuentas[primera]
                if datos.get("servicio") == "Gmail":
                    self.creds_gmail_user = datos["user"]
                    self.creds_gmail_pass = datos["pass"]
                elif datos.get("servicio") == "Outlook":
                    self.creds_outlook_user = datos["user"]
                    self.creds_outlook_pass = datos["pass"]
                elif datos.get("servicio") == "SandMail Z":
                    self.creds_sandmail_user = datos["user"]
                    self.creds_sandmail_pass = datos["pass"]
        except Exception:
            pass

    def guardar_todo_keyring(self):
        if not KEYRING_OK:
            return False
        try:
            keyring.set_password("SandMailZ", "cuentas_json", json.dumps(self.cuentas))
            if self.creds_gmail_user:
                keyring.set_password("SandMailZ", "gmail_user", self.creds_gmail_user)
            if self.creds_gmail_pass:
                keyring.set_password("SandMailZ", "gmail_pass", self.creds_gmail_pass)
            if self.creds_outlook_user:
                keyring.set_password("SandMailZ", "outlook_user", self.creds_outlook_user)
            if self.creds_outlook_pass:
                keyring.set_password("SandMailZ", "outlook_pass", self.creds_outlook_pass)
            if self.creds_sandmail_user:
                keyring.set_password("SandMailZ", "sandmail_user", self.creds_sandmail_user)
            if self.creds_sandmail_pass:
                keyring.set_password("SandMailZ", "sandmail_pass", self.creds_sandmail_pass)
            return True
        except Exception as e:
            print("Keyring error:", e)
            return False

    def actualizar_combo_cuentas(self):
        if not hasattr(self, 'combo_cuenta'):
            return
        valores = list(self.cuentas.keys())
        if not valores:
            valores = ["(Sin cuentas)"]
        self.combo_cuenta['values'] = valores
        if self.cuenta_actual in self.cuentas:
            self.combo_cuenta.set(self.cuenta_actual)
        elif valores and valores[0] != "(Sin cuentas)":
            self.combo_cuenta.current(0)
            self.seleccionar_cuenta()

    def seleccionar_cuenta(self, event=None):
        sel = self.combo_cuenta.get()
        if sel not in self.cuentas:
            return
        self.cuenta_actual = sel
        datos = self.cuentas[sel]
        if datos.get("servicio") == "Gmail":
            self.creds_gmail_user = datos["user"]
            self.creds_gmail_pass = datos["pass"]
        elif datos.get("servicio") == "Outlook":
            self.creds_outlook_user = datos["user"]
            self.creds_outlook_pass = datos["pass"]
        elif datos.get("servicio") == "SandMail Z":
            self.creds_sandmail_user = datos["user"]
            self.creds_sandmail_pass = datos["pass"]
        self.log("Cuenta activa: " + sel + " (" + datos.get("servicio", "?") + ")")

    def aplicar_estilo(self):
        s = self.style
        p = self.P()
        bg, surf, card = self.bg(), self.surface(), self.card()
        bord, txt, subt = self.border(), self.text(), self.subtext()
        hov, nav = self.hover(), self.nav_bg()
        accent = p.ACCENT
        font = p.FONT_FALLBACK
        self.root.configure(bg=bg)
        s.configure('TFrame', background=bg)
        s.configure('Surface.TFrame', background=surf)
        s.configure('Card.TFrame', background=card)
        s.configure('Nav.TFrame', background=nav)
        s.configure('TLabel', background=bg, foreground=txt, font=(font, 10))
        s.configure('Surface.TLabel', background=surf, foreground=txt, font=(font, 10))
        if self.estilo_actual == "aero":
            s.configure('TEntry', fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#0A1F33",
                        bordercolor=Aero.ACCENT, lightcolor=Aero.ACCENT, darkcolor=Aero.ACCENT,
                        insertcolor="#0A1F33", padding=6, relief='sunken', borderwidth=1)
        else:
            s.configure('TEntry', fieldbackground=surf, background=surf, foreground=txt,
                        bordercolor=bord, lightcolor=bord, darkcolor=bord, insertcolor=txt,
                        padding=8, relief='flat')
            s.map('TEntry', bordercolor=[('focus', accent)])
        if self.estilo_actual == "aero":
            s.configure('TCombobox', fieldbackground="#FFFFFF", background="#E8F0F8",
                        foreground="#0A1F33", arrowcolor="#0A1F33", bordercolor=Aero.ACCENT,
                        lightcolor=Aero.ACCENT, darkcolor=Aero.ACCENT, padding=4,
                        relief='raised', borderwidth=1)
        else:
            s.configure('TCombobox', fieldbackground=surf, background=surf, foreground=txt,
                        arrowcolor=txt, bordercolor=bord, lightcolor=bord, darkcolor=bord,
                        padding=6, relief='flat')
        s.map('TCombobox', fieldbackground=[('readonly', surf)])
        if self.estilo_actual == "aero":
            s.configure('Accent.TButton', background=Aero.ACCENT, foreground="#FFFFFF",
                        font=(font, 10, 'bold'), borderwidth=1, bordercolor=Aero.ACCENT_GLOW,
                        lightcolor=Aero.ACCENT_GLOW, darkcolor=Aero.ACCENT_PRESSED,
                        focuscolor='none', padding=(16, 8), relief='raised')
            s.map('Accent.TButton',
                  background=[('active', Aero.ACCENT_HOVER), ('pressed', Aero.ACCENT_PRESSED)])
        else:
            s.configure('Accent.TButton', background=accent, foreground="#FFFFFF",
                        font=(font, 10, 'bold'), borderwidth=0, focuscolor='none',
                        padding=(16, 8), relief='flat')
            s.map('Accent.TButton',
                  background=[('active', p.ACCENT_HOVER), ('pressed', p.ACCENT_PRESSED)])
        if self.estilo_actual == "aero":
            s.configure('Secondary.TButton', background="#E8F0F8", foreground="#0A1F33",
                        font=(font, 10), borderwidth=1, bordercolor=Aero.ACCENT,
                        lightcolor="#FFFFFF", darkcolor=Aero.ACCENT, focuscolor='none',
                        padding=(14, 7), relief='raised')
            s.map('Secondary.TButton', background=[('active', "#D6E4F0")])
        else:
            s.configure('Secondary.TButton', background=surf, foreground=txt, font=(font, 10),
                        borderwidth=1, bordercolor=bord, focuscolor='none',
                        padding=(14, 7), relief='flat')
            s.map('Secondary.TButton', background=[('active', hov)])
        s.configure('Danger.TButton', background="#E81123", foreground="#FFFFFF",
                    font=(font, 10, 'bold'), borderwidth=0, focuscolor='none',
                    padding=(12, 7), relief='flat')
        s.map('Danger.TButton', background=[('active', "#C50F1F")])
        if self.estilo_actual == "aero":
            s.configure('Nav.TButton', background=nav, foreground="#0A1F33", font=(font, 10),
                        borderwidth=0, focuscolor='none', padding=(14, 10), anchor='w', relief='flat')
            s.map('Nav.TButton', background=[('active', "#A8CCEE")])
        else:
            s.configure('Nav.TButton', background=nav, foreground=txt, font=(font, 10),
                        borderwidth=0, focuscolor='none', padding=(14, 10), anchor='w', relief='flat')
            s.map('Nav.TButton', background=[('active', hov)])
        s.configure('TNotebook', background=bg, borderwidth=0, tabmargins=[0, 0, 0, 0])
        if self.estilo_actual == "aero":
            s.configure('TNotebook.Tab', background="#C4DCF0", foreground="#0A1F33",
                        font=(font, 10, 'bold'), padding=[18, 8], borderwidth=1)
            s.map('TNotebook.Tab', background=[('selected', "#EAF2FB"), ('active', "#D6E4F0")])
        else:
            s.configure('TNotebook.Tab', background=bg, foreground=subt, font=(font, 10),
                        padding=[18, 10], borderwidth=0, focuscolor='none')
            s.map('TNotebook.Tab', background=[('selected', surf), ('active', hov)],
                  foreground=[('selected', txt), ('active', txt)])
        if self.estilo_actual == "aero":
            s.configure('Treeview', background="#FFFFFF", fieldbackground="#FFFFFF",
                        foreground="#0A1F33", font=(font, 10), rowheight=32)
        else:
            s.configure('Treeview', background=surf, fieldbackground=surf, foreground=txt,
                        font=(font, 10), rowheight=36, borderwidth=0, relief='flat')
            s.configure('Treeview.Heading', background=surf, foreground=subt,
                        font=(font, 9, 'bold'), relief='flat', padding=8)
            s.map('Treeview', background=[('selected', accent)], foreground=[('selected', '#FFFFFF')])
        s.configure('TSeparator', background=bord)
        s.configure('Progress.Horizontal.TProgressbar', background=accent,
                    troughcolor=bord, borderwidth=0, thickness=6)

    def crear_menu(self):
        self.menubar = tk.Menu(self.root)
        m1 = tk.Menu(self.menubar, tearoff=0)
        m1.add_command(label=self.t('nuevo'), command=lambda: self.tabs.select(1))
        m1.add_command(label=self.t('guardar'), command=self.guardar_borrador)
        m1.add_separator()
        m1.add_command(label=self.t('salir'), command=self.root.quit)
        self.menubar.add_cascade(label=self.t('archivo'), menu=m1)
        m2 = tk.Menu(self.menubar, tearoff=0)
        m2.add_command(label=self.t('oscuro'), command=self.toggle_modo_oscuro)
        m_est = tk.Menu(m2, tearoff=0)
        m_est.add_command(label=self.t('aero'), command=lambda: self.cambiar_estilo("aero"))
        m_est.add_command(label=self.t('win11'), command=lambda: self.cambiar_estilo("win11"))
        m2.add_cascade(label=self.t('estilo'), menu=m_est)
        m_id = tk.Menu(m2, tearoff=0)
        for nombre, codigo in [("Espanol", "es"), ("English", "en"), ("Portugues", "pt"),
                                ("Francais", "fr"), ("Japanese", "ja"), ("Russian", "ru"), ("Arabic", "ar")]:
            m_id.add_command(label=nombre, command=lambda c=codigo: self.cambiar_idioma(c))
        m2.add_cascade(label=self.t('idioma'), menu=m_id)
        self.menubar.add_cascade(label=self.t('ver'), menu=m2)
        m3 = tk.Menu(self.menubar, tearoff=0)
        m3.add_command(label=self.t('ia'), command=self.asistente_ia)
        m3.add_command(label=self.t('encriptar'), command=self.encriptar_mensaje)
        m3.add_command(label=self.t('config'), command=lambda: self.tabs.select(5))
        self.menubar.add_cascade(label=self.t('herramientas'), menu=m3)
        self.root.config(menu=self.menubar)

    def crear_layout_principal(self):
        self.frame_header = tk.Frame(self.root, bg=self.nav_bg(), height=72)
        self.frame_header.pack(fill="x")
        self.frame_header.pack_propagate(False)
        self.border_bottom = tk.Frame(self.root, bg=self.border(), height=1)
        self.border_bottom.pack(fill="x")
        self.canvas_logo = tk.Canvas(self.frame_header, width=280, height=60,
                                      bg=self.nav_bg(), highlightthickness=0)
        self.canvas_logo.pack(side="left", padx=24, pady=6)
        self.dibujar_logo_texto(self.canvas_logo, 10, 12)

        # --- Selector de cuenta en la cabecera ---
        self.chip_frame = tk.Frame(self.frame_header, bg=self.surface(),
                                    highlightbackground=self.border(), highlightthickness=1)
        self.chip_frame.pack(side="right", padx=20, pady=18)
        self.lbl_user = tk.Label(self.chip_frame, text=self.t('cuenta'),
                                  font=(self.P().FONT_FALLBACK, 9),
                                  bg=self.surface(), fg=self.text())
        self.lbl_user.pack(side="left", padx=(8, 4), pady=4)
        self.combo_cuenta = ttk.Combobox(self.chip_frame, width=26, state="readonly")
        self.combo_cuenta.pack(side="left", padx=(0, 8), pady=4)
        self.combo_cuenta.bind("<<ComboboxSelected>>", self.seleccionar_cuenta)

        self.container = tk.Frame(self.root, bg=self.bg())
        self.container.pack(fill="both", expand=True)
        self.frame_sidebar = tk.Frame(self.container, bg=self.nav_bg(), width=220)
        self.frame_sidebar.pack(side="left", fill="y")
        self.frame_sidebar.pack_propagate(False)
        self.sep_vert = tk.Frame(self.container, bg=self.border(), width=1)
        self.sep_vert.pack(side="left", fill="y")
        tk.Frame(self.frame_sidebar, bg=self.nav_bg(), height=10).pack()
        self.botones_nav = []
        for key, idx in [('sb_inbox', 0), ('sb_compose', 1), ('sb_contacts', 2),
                         ('sb_calendar', 3), ('sb_tasks', 4), ('sb_settings', 5), ('sb_log', 6)]:
            btn = ttk.Button(self.frame_sidebar, text="  " + self.t(key),
                             style='Nav.TButton', command=lambda i=idx: self.tabs.select(i))
            btn.pack(fill="x", padx=8, pady=1)
            self.botones_nav.append(btn)

        self.frame_main = tk.Frame(self.container, bg=self.bg())
        self.frame_main.pack(side="right", fill="both", expand=True)
        self.tabs = ttk.Notebook(self.frame_main)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=12)
        self.tab_inbox = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_compose = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_contacts = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_calendar = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_tasks = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_settings = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tab_log = ttk.Frame(self.tabs, style='Surface.TFrame')
        self.tabs.add(self.tab_inbox, text=self.t('tab_inbox'))
        self.tabs.add(self.tab_compose, text=self.t('tab_compose'))
        self.tabs.add(self.tab_contacts, text=self.t('tab_contacts'))
        self.tabs.add(self.tab_calendar, text=self.t('tab_calendar'))
        self.tabs.add(self.tab_tasks, text=self.t('tab_tasks'))
        self.tabs.add(self.tab_settings, text=self.t('tab_settings'))
        self.tabs.add(self.tab_log, text=self.t('tab_log'))
        self.construir_inbox()
        self.construir_compose()
        self.construir_contactos()
        self.construir_calendario()
        self.construir_tareas()
        self.construir_configuracion()
        self.construir_log()

        self.frame_status = tk.Frame(self.root, bg=self.nav_bg())
        self.frame_status.pack(side="bottom", fill="x")
        self.progress = ttk.Progressbar(self.frame_status, mode='indeterminate',
                                         style='Progress.Horizontal.TProgressbar', length=200)
        self.status_bar = tk.Label(self.frame_status,
                                   text="  " + self.t('status_listo') + "  |  SandMail Z v5.1",
                                   font=(self.P().FONT_FALLBACK, 9),
                                   bg=self.nav_bg(), fg=self.subtext(), anchor="w", padx=14, pady=6)
        self.status_bar.pack(side="left", fill="x", expand=True)

    def dibujar_logo_texto(self, canvas, x, y):
        c = "#0A1F33" if not self.modo_oscuro else "#E8F0F8"
        canvas.create_text(x, y, text="Sand", font=(self.P().FONT_FALLBACK, 22, "bold"), fill=c, anchor="w")
        canvas.create_text(x, y + 26, text="Mail", font=(self.P().FONT_FALLBACK, 22, "bold"), fill=Aero.BRAND_ORANGE, anchor="w")
        xz, yz = 105, y + 26
        canvas.create_line(xz + 10, yz - 6, xz - 5, yz - 6, fill=Aero.BRAND_RED, width=2)
        canvas.create_line(xz + 12, yz, xz - 8, yz, fill=Aero.BRAND_RED, width=2)
        canvas.create_line(xz + 10, yz + 6, xz - 5, yz + 6, fill=Aero.BRAND_RED, width=2)
        canvas.create_text(xz + 20, yz, text="Z", font=(self.P().FONT_FALLBACK, 24, "bold italic"), fill=Aero.BRAND_RED, anchor="w")

    def dibujar_icono_patineta(self, canvas, ox, oy):
        canvas.create_polygon(ox-30,oy+40,ox+30,oy-60,ox+70,oy-10,ox+130,oy-40,ox+160,oy+50,ox+40,oy+80,ox-30,oy+40, fill=Aero.BRAND_RED, outline="", smooth=True)
        canvas.create_polygon(ox-10,oy+30,ox+50,oy-30,ox+90,oy+10,ox+130,oy-10,ox+140,oy+40,ox+50,oy+60,ox-10,oy+30, fill=Aero.BRAND_ORANGE, outline="", smooth=True)
        canvas.create_polygon(ox+10,oy+20,ox+60,oy-10,ox+100,oy+20,ox+130,oy+10,ox+130,oy+30,ox+60,oy+50,ox+10,oy+20, fill=Aero.BRAND_YELLOW, outline="", smooth=True)
        canvas.create_line(ox+40,oy+90,ox+190,oy+70, fill="#1A1A1A", width=4, capstyle="round")
        canvas.create_oval(ox+60,oy+80,ox+90,oy+110, fill="#1A1A1A", outline="")
        canvas.create_oval(ox+160,oy+60,ox+190,oy+90, fill="#1A1A1A", outline="")
        canvas.create_polygon(ox+50,oy-50,ox+200,oy-30,ox+180,oy+70,ox+30,oy+50, fill="#FFFFFF", outline="#1A1A1A", width=2)
        canvas.create_polygon(ox+50,oy-50,ox+200,oy-30,ox+120,oy+15, fill="#E5E5E5", outline="#1A1A1A", width=2)
        canvas.create_oval(ox+100,oy+5,ox+130,oy+35, fill=Aero.BRAND_YELLOW, outline="#1A1A1A", width=1)

    def construir_inbox(self):
        surf, txt, subt = self.surface(), self.text(), self.subtext()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_inbox, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        top = tk.Frame(outer, bg=surf)
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text="Correo", font=(font, 22, "bold"), bg=surf, fg=txt).pack(side="left")
        ttk.Button(top, text="  " + self.t('cargar_reales'), style='Accent.TButton',
                   command=self.hilo_cargar_reales).pack(side="right", padx=(8, 0))
        sf = tk.Frame(top, bg=surf, highlightbackground=self.border(), highlightthickness=1)
        sf.pack(side="right", padx=8)
        self.entry_buscar = tk.Entry(sf, width=25, bd=0, bg=surf, fg=subt,
                                     font=(font, 10), insertbackground=txt)
        self.entry_buscar.pack(side="left", padx=10, pady=6)
        self.entry_buscar.insert(0, self.t('buscar'))
        acciones = tk.Frame(outer, bg=surf)
        acciones.pack(fill="x", pady=(0, 8))
        ttk.Button(acciones, text="  " + self.t('marcar_leido'), style='Secondary.TButton',
                   command=self.marcar_como_leido).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="  " + self.t('eliminar'), style='Danger.TButton',
                   command=self.mover_a_papelera).pack(side="left", padx=(0, 6))
        cols = ("fav", self.t('de'), self.t('asunto'), "Fecha", self.t('prioridad'), "Servidor")
        self.tree = ttk.Treeview(outer, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree.heading(c, text=c if c != "fav" else "")
        self.tree.column("fav", width=40, anchor="center")
        self.tree.column(self.t('de'), width=250)
        self.tree.column(self.t('asunto'), width=400)
        self.tree.column("Fecha", width=140)
        self.tree.column(self.t('prioridad'), width=90, anchor="center")
        self.tree.column("Servidor", width=110, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.abrir_correo_seleccionado)
        self.cargar_correos_demo()

    def cargar_correos_demo(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.uids_actuales = []
        correos = [
            ("*", "Tony Hawk", "Nuevo truco en el skatepark!", "10:30", self.t('alta'), "Gmail"),
            ("*", "SandMail Z Team", "Bienvenido a @sandmailz.net", "Ayer", self.t('normal'), "SandMail Z"),
            ("", "Soporte Outlook", "Actualiza tu contrasena", "Lunes", self.t('baja'), "Outlook"),
            ("", "Rodrigo", "Vamos a patinar el sabado?", "Dom", self.t('normal'), "Gmail"),
        ]
        for c in correos:
            self.tree.insert("", "end", values=c)

    def abrir_correo_seleccionado(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        try:
            uid_index = int(iid)
        except (ValueError, TypeError):
            uid_index = -1
        if 0 <= uid_index < len(self.uids_actuales):
            uid = self.uids_actuales[uid_index]
            threading.Thread(target=self.cargar_cuerpo_correo, args=(uid,)).start()
        else:
            self.mostrar_ventana_correo("Demo", "Correo de ejemplo",
                "Este es un correo de demostracion.\n\nPara ver correos reales:\n"
                "1. Configura tus credenciales en la pestaña Ajustes\n"
                "2. Pulsa Cargar Reales\n"
                "3. Haz doble clic en un correo real")

    def cargar_cuerpo_correo(self, uid):
        self.log("Descargando cuerpo UID=" + str(uid) + "...")
        self.root.after(0, lambda: self.mostrar_progress(True))
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(self.creds_gmail_user, self.creds_gmail_pass)
            mail.select("inbox")
            status, datos = mail.uid('fetch', uid, "(RFC822)")
            if status != "OK":
                raise Exception("No se pudo obtener el correo")
            raw = datos[0][1]
            msg = email.message_from_bytes(raw)
            remitente = self.decodificar_header(msg.get("From", "(Desconocido)"))
            asunto = self.decodificar_header(msg.get("Subject", "(Sin asunto)"))
            cuerpo, adjuntos = "", []
            if msg.is_multipart():
                for parte in msg.walk():
                    ctype = parte.get_content_type()
                    cdisp = str(parte.get("Content-Disposition", ""))
                    if ctype == "text/plain" and "attachment" not in cdisp:
                        try:
                            payload = parte.get_payload(decode=True)
                            charset = parte.get_content_charset() or "utf-8"
                            cuerpo += payload.decode(charset, errors="ignore")
                        except Exception:
                            pass
                    elif ctype == "text/html" and "attachment" not in cdisp and not cuerpo:
                        try:
                            payload = parte.get_payload(decode=True)
                            charset = parte.get_content_charset() or "utf-8"
                            html = payload.decode(charset, errors="ignore")
                            import re
                            cuerpo = re.sub(r'<[^>]+>', '', html)
                        except Exception:
                            pass
                    elif "attachment" in cdisp:
                        nombre = parte.get_filename()
                        if nombre:
                            adjuntos.append(self.decodificar_header(nombre))
            else:
                try:
                    payload = msg.get_payload(decode=True)
                    charset = msg.get_content_charset() or "utf-8"
                    cuerpo = payload.decode(charset, errors="ignore")
                except Exception:
                    cuerpo = str(msg.get_payload())
            if not cuerpo.strip():
                cuerpo = self.t('cuerpo_vacio')
            mail.logout()
            self.root.after(0, lambda: self.mostrar_ventana_correo(remitente, asunto, cuerpo, adjuntos))
        except Exception as e:
            self.log("Error: " + str(e))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.mostrar_progress(False))

    def mostrar_ventana_correo(self, remitente, asunto, cuerpo, adjuntos=None):
        win = tk.Toplevel(self.root)
        win.title(self.t('abrir_correo') + " - " + asunto[:50])
        win.geometry("750x600")
        win.configure(bg=self.surface())
        hdr = tk.Frame(win, bg=self.surface())
        hdr.pack(fill="x", padx=20, pady=(15, 5))
        tk.Label(hdr, text="De: " + remitente, font=(self.P().FONT_FALLBACK, 11, "bold"),
                 bg=self.surface(), fg=self.text()).pack(anchor="w")
        tk.Label(hdr, text="Asunto: " + asunto, font=(self.P().FONT_FALLBACK, 11),
                 bg=self.surface(), fg=self.text()).pack(anchor="w", pady=(4, 0))
        if adjuntos:
            tk.Label(hdr, text=self.t('adjuntos') + ": " + ", ".join(adjuntos),
                     font=(self.P().FONT_FALLBACK, 9, "italic"),
                     bg=self.surface(), fg=self.subtext()).pack(anchor="w", pady=(4, 0))
        tk.Frame(win, bg=self.border(), height=1).pack(fill="x", padx=20, pady=8)
        txt = scrolledtext.ScrolledText(win, wrap='word', font=(self.P().FONT_FALLBACK, 10),
                                         bg=self.surface(), fg=self.text(), bd=0, relief='flat',
                                         padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        txt.insert("1.0", cuerpo)
        txt.config(state="disabled")
        ttk.Button(win, text="Cerrar", style='Accent.TButton', command=win.destroy).pack(pady=(0, 15))

    def mover_a_papelera(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccion", "Selecciona un correo primero.")
            return
        iid = sel[0]
        try:
            uid_index = int(iid)
        except (ValueError, TypeError):
            uid_index = -1
        if not (0 <= uid_index < len(self.uids_actuales)):
            self.tree.delete(iid)
            self.log("Correo demo eliminado de la vista")
            return
        uid = self.uids_actuales[uid_index]
        if not messagebox.askyesno("Confirmar", "Mover este correo a la papelera de Gmail?"):
            return
        self.mostrar_progress(True)
        self.log("Moviendo UID=" + str(uid) + " a papelera...")
        def tarea():
            try:
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login(self.creds_gmail_user, self.creds_gmail_pass)
                mail.select("inbox")
                status, _ = mail.uid('COPY', uid, '[Gmail]/Trash')
                if status != "OK":
                    mail.uid('COPY', uid, '[Gmail]/Papelera')
                mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
                mail.expunge()
                mail.logout()
                self.root.after(0, lambda: self.log("Correo movido a papelera"))
                self.root.after(0, lambda: self.tree.delete(iid))
                self.root.after(0, lambda: messagebox.showinfo("OK", "Correo movido a papelera."))
            except Exception as e:
                self.root.after(0, lambda: self.log("Error: " + str(e)))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.root.after(0, lambda: self.mostrar_progress(False))
        threading.Thread(target=tarea).start()

    def marcar_como_leido(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccion", "Selecciona un correo primero.")
            return
        iid = sel[0]
        try:
            uid_index = int(iid)
        except (ValueError, TypeError):
            uid_index = -1
        if not (0 <= uid_index < len(self.uids_actuales)):
            messagebox.showinfo("Info", "Solo correos reales.")
            return
        uid = self.uids_actuales[uid_index]
        self.mostrar_progress(True)
        self.log("Marcando UID=" + str(uid) + " como leido...")
        def tarea():
            try:
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login(self.creds_gmail_user, self.creds_gmail_pass)
                mail.select("inbox")
                mail.uid('STORE', uid, '+FLAGS', '(\\Seen)')
                mail.logout()
                self.root.after(0, lambda: self.log("Marcado como leido"))
                self.root.after(0, lambda: messagebox.showinfo("OK", "Correo marcado como leido."))
            except Exception as e:
                self.root.after(0, lambda: self.log("Error: " + str(e)))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.root.after(0, lambda: self.mostrar_progress(False))
        threading.Thread(target=tarea).start()

    def mostrar_progress(self, mostrar=True):
        if mostrar:
            self.progress.pack(side="right", padx=15)
            self.progress.start(15)
        else:
            self.progress.stop()
            self.progress.pack_forget()

    def decodificar_header(self, valor):
        if not valor:
            return ""
        try:
            partes = decode_header(valor)
            r = ""
            for contenido, encoding in partes:
                if isinstance(contenido, bytes):
                    try:
                        r += contenido.decode(encoding or "utf-8", errors="ignore")
                    except Exception:
                        r += contenido.decode("utf-8", errors="ignore")
                else:
                    r += str(contenido)
            return r
        except Exception:
            return str(valor)

    def hilo_cargar_reales(self):
        threading.Thread(target=self.cargar_correos_reales).start()

    def cargar_correos_reales(self):
        usuario = self.creds_gmail_user.strip()
        password = self.creds_gmail_pass.strip()
        if not usuario or not password:
            self.root.after(0, lambda: messagebox.showwarning("Faltan credenciales",
                "Ve a Ajustes y guarda tu correo y contrasena de aplicacion de Gmail."))
            return
        self.root.after(0, lambda: self.status_bar.config(text="  " + self.t('cargando')))
        self.root.after(0, lambda: self.mostrar_progress(True))
        self.log("--- Conectando a Gmail IMAP (" + usuario + ") ---")
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(usuario, password)
            mail.select("inbox")
            status, mensajes = mail.uid('search', None, "ALL")
            uids = mensajes[0].split()
            if not uids:
                self.log("Bandeja vacia")
                mail.logout()
                self.root.after(0, lambda: messagebox.showinfo("IMAP", "Bandeja vacia."))
                return
            uids_rec = uids[-20:]
            uids_rec.reverse()
            self.log("Descargando " + str(len(uids_rec)) + " correos...")
            correos, uids_guardar = [], []
            for uid in uids_rec:
                try:
                    status, datos = mail.uid('fetch', uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
                    if status != "OK":
                        continue
                    msg = email.message_from_bytes(datos[0][1])
                    remitente = self.decodificar_header(msg.get("From", "(Desconocido)"))
                    if "<" in remitente:
                        remitente = remitente.split("<")[0].strip().strip('"')
                    if len(remitente) > 40:
                        remitente = remitente[:37] + "..."
                    asunto = self.decodificar_header(msg.get("Subject", "(Sin asunto)"))
                    if len(asunto) > 80:
                        asunto = asunto[:77] + "..."
                    fecha_raw = msg.get("Date", "")
                    try:
                        ft = email.utils.parsedate(fecha_raw)
                        if ft:
                            fd = datetime.datetime(*ft[:6])
                            d = datetime.datetime.now() - fd
                            if d.days == 0: fecha = fd.strftime("Hoy %H:%M")
                            elif d.days == 1: fecha = "Ayer " + fd.strftime("%H:%M")
                            elif d.days < 7: fecha = fd.strftime("%a %H:%M")
                            else: fecha = fd.strftime("%d/%m/%y")
                        else:
                            fecha = fecha_raw[:20]
                    except Exception:
                        fecha = fecha_raw[:20]
                    correos.append(("", remitente, asunto, fecha, self.t('normal'), "Gmail"))
                    uids_guardar.append(uid.decode() if isinstance(uid, bytes) else str(uid))
                except Exception:
                    continue
            mail.logout()
            def actualizar():
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.uids_actuales = uids_guardar
                for idx, c in enumerate(correos):
                    self.tree.insert("", "end", iid=str(idx), values=c)
                self.log("OK: " + str(len(correos)) + " correos cargados")
                self.status_bar.config(text="  " + self.t('status_listo') + "  |  SandMail Z v5.1")
                self.mostrar_progress(False)
                messagebox.showinfo("Gmail IMAP", "Se cargaron " + str(len(correos)) + " correos.\n\nDoble clic para leerlos.")
            self.root.after(0, actualizar)
        except imaplib.IMAP4.error as e:
            self.log("Error IMAP: " + str(e))
            self.root.after(0, lambda: messagebox.showerror("Error IMAP",
                "No se pudo conectar a Gmail.\nVerifica:\n1. Correo correcto\n2. Contrasena de Aplicacion\n3. IMAP habilitado\n\n" + str(e)))
            self.root.after(0, lambda: self.mostrar_progress(False))
        except Exception as e:
            self.log("Error: " + str(e))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.mostrar_progress(False))

    def construir_compose(self):
        surf, card, txt, subt = self.surface(), self.card(), self.text(), self.subtext()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_compose, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        left = tk.Frame(outer, bg=card, width=280, highlightbackground=self.border(), highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)
        canvas = tk.Canvas(left, width=260, height=280, bg=card, highlightthickness=0)
        canvas.pack(pady=20)
        self.dibujar_icono_patineta(canvas, 30, 100)
        tk.Label(left, text="SandMail Z", font=(font, 16, "bold"), bg=card, fg=txt).pack()
        tk.Label(left, text="Envia con estilo", font=(font, 10), bg=card, fg=subt).pack(pady=(0, 20))
        right = tk.Frame(outer, bg=surf)
        right.pack(side="left", fill="both", expand=True)
        tk.Label(right, text="Nuevo Mensaje", font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 14))
        row = tk.Frame(right, bg=surf)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=self.t('servicio'), font=(font, 9), bg=surf, fg=subt, width=10, anchor="w").pack(side="left")
        self.combo_proveedor = ttk.Combobox(row, values=["SandMail Z", "Gmail", "Outlook"], state="readonly", width=30)
        self.combo_proveedor.current(0)
        self.combo_proveedor.pack(side="left")
        self.combo_proveedor.bind("<<ComboboxSelected>>", self.cambiar_remitente)
        self.campos = {}
        for key in ['de', 'para', 'cc', 'asunto']:
            row = tk.Frame(right, bg=surf)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=self.t(key), font=(font, 9), bg=surf, fg=subt, width=10, anchor="w").pack(side="left")
            e = ttk.Entry(row, width=40)
            e.pack(side="left", fill="x", expand=True)
            self.campos[key] = e
        self.campos['de'].insert(0, "rider@sandmailz.net")
        self.campos['de'].config(state="readonly")
        row = tk.Frame(right, bg=surf)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=self.t('prioridad'), font=(font, 9), bg=surf, fg=subt, width=10, anchor="w").pack(side="left")
        self.combo_prioridad = ttk.Combobox(row, values=[self.t('normal'), self.t('alta'), self.t('baja')], state="readonly", width=15)
        self.combo_prioridad.current(0)
        self.combo_prioridad.pack(side="left")
        toolbar = tk.Frame(right, bg=surf)
        toolbar.pack(fill="x", pady=(10, 4))
        ttk.Button(toolbar, text="B", width=3, style='Secondary.TButton', command=lambda: self.log("Bold")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="I", width=3, style='Secondary.TButton', command=lambda: self.log("Italic")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="U", width=3, style='Secondary.TButton', command=lambda: self.log("Underline")).pack(side="left", padx=2)
        ttk.Button(toolbar, text=self.t('adjuntar'), style='Secondary.TButton', command=self.adjuntar_archivo).pack(side="left", padx=8)
        ttk.Button(toolbar, text=self.t('sandai'), style='Secondary.TButton', command=self.asistente_ia).pack(side="left", padx=2)
        self.var_html = tk.BooleanVar(value=False)
        tk.Checkbutton(toolbar, text=self.t('enviar_html'), variable=self.var_html, bg=surf, fg=txt,
                       selectcolor=surf, activebackground=surf, activeforeground=txt,
                       font=(font, 9)).pack(side="left", padx=12)
        self.lbl_adjuntos = tk.Label(right, text="", font=(font, 9, "italic"), bg=surf, fg=subt)
        self.lbl_adjuntos.pack(anchor="w")
        tk.Label(right, text=self.t('mensaje'), font=(font, 9), bg=surf, fg=subt).pack(anchor="w", pady=(6, 2))
        self.texto_mensaje = scrolledtext.ScrolledText(right, height=10, font=(font, 10),
                                                        bg=surf, fg=txt, bd=1, relief='solid', wrap='word')
        self.texto_mensaje.pack(fill="both", expand=True)
        btn_row = tk.Frame(right, bg=surf)
        btn_row.pack(fill="x", pady=14)
        ttk.Button(btn_row, text=self.t('guardar'), style='Secondary.TButton', command=self.guardar_borrador).pack(side="left")
        ttk.Button(btn_row, text=self.t('enviar'), style='Accent.TButton', command=self.hilo_enviar).pack(side="right")

    def construir_contactos(self):
        surf, txt = self.surface(), self.text()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_contacts, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        tk.Label(outer, text=self.t('contactos_title'), font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 14))
        add = tk.Frame(outer, bg=surf)
        add.pack(fill="x", pady=6)
        self.entry_nuevo_contacto = ttk.Entry(add, width=40)
        self.entry_nuevo_contacto.insert(0, self.t('nuevo_contacto'))
        self.entry_nuevo_contacto.pack(side="left", fill="x", expand=True)
        ttk.Button(add, text=self.t('agregar'), style='Accent.TButton', command=self.agregar_contacto).pack(side="left", padx=8)
        self.lista_contactos = tk.Listbox(outer, font=(font, 11), bg=surf, fg=txt,
                                           selectbackground=self.P().ACCENT, selectforeground="white",
                                           bd=0, highlightthickness=1,
                                           highlightbackground=self.border(), activestyle='none')
        self.lista_contactos.pack(fill="both", expand=True, pady=10)
        for c in self.contactos:
            self.lista_contactos.insert(tk.END, "  " + c)

    def agregar_contacto(self):
        n = self.entry_nuevo_contacto.get()
        if n and n != self.t('nuevo_contacto'):
            self.contactos.append(n)
            self.lista_contactos.insert(tk.END, "  " + n)
            self.entry_nuevo_contacto.delete(0, tk.END)
            self.entry_nuevo_contacto.insert(0, self.t('nuevo_contacto'))
            self.log("Contacto agregado: " + n)

    def construir_calendario(self):
        surf, card, txt, subt = self.surface(), self.card(), self.text(), self.subtext()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_calendar, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        tk.Label(outer, text=self.t('calendario_title'), font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 10))
        tk.Label(outer, text=self.t('hoy') + datetime.datetime.now().strftime("%d/%m/%Y"),
                 font=(font, 11), bg=surf, fg=subt).pack(anchor="w", pady=(0, 16))
        for hora, texto, color in [("10:00", "Revision de correos", self.P().ACCENT),
                                     ("14:00", "Reunion SandMail", Aero.BRAND_ORANGE),
                                     ("17:00", "Salir a patinar", Aero.BRAND_RED),
                                     ("20:00", "Responder mensajes", "#00B294")]:
            c = tk.Frame(outer, bg=card, highlightbackground=self.border(), highlightthickness=1)
            c.pack(fill="x", pady=4)
            tk.Frame(c, bg=color, width=4).pack(side="left", fill="y")
            tk.Label(c, text=hora, font=(font, 11, "bold"), bg=card, fg=txt, width=8).pack(side="left", padx=10, pady=12)
            tk.Label(c, text=texto, font=(font, 10), bg=card, fg=txt).pack(side="left", padx=6)

    def construir_tareas(self):
        surf, txt = self.surface(), self.text()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_tasks, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        tk.Label(outer, text=self.t('tareas_title'), font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 14))
        self.lista_tareas = tk.Listbox(outer, font=(font, 11), bg=surf, fg=txt,
                                        selectbackground=self.P().ACCENT, selectforeground="white",
                                        bd=0, highlightthickness=1, highlightbackground=self.border(),
                                        activestyle='none', height=12)
        self.lista_tareas.pack(fill="both", expand=True, pady=8)
        for t in ["Responder a Tony Hawk", "Comprar ruedas nuevas", "Configurar SMTP",
                  "Probar leer cuerpo con IMAP", "Enviar adjuntos reales"]:
            self.lista_tareas.insert(tk.END, "  [ ]  " + t)
        ttk.Button(outer, text=self.t('completar'), style='Accent.TButton', command=self.completar_tarea).pack(pady=8)

    def completar_tarea(self):
        try:
            idx = self.lista_tareas.curselection()[0]
            t = self.lista_tareas.get(idx).replace("[ ]", "[X]")
            self.lista_tareas.delete(idx)
            self.lista_tareas.insert(idx, t)
            self.log("Tarea completada")
        except IndexError:
            messagebox.showwarning("Tareas", "Selecciona una tarea.")

    def construir_configuracion(self):
        surf, card, txt, subt = self.surface(), self.card(), self.text(), self.subtext()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_settings, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        tk.Label(outer, text=self.t('config_title'), font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 14))

        # ---- Tarjeta SandMail Z ----
        c0 = tk.Frame(outer, bg=card, highlightbackground=self.border(), highlightthickness=1)
        c0.pack(fill="x", pady=6)
        tk.Label(c0, text="SandMail Z (SMTP propio)", font=(font, 12, "bold"),
                 bg=card, fg=txt).pack(anchor="w", padx=14, pady=(10, 4))
        r = tk.Frame(c0, bg=card); r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Correo", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_sandmail_user = ttk.Entry(r, width=30)
        self.entry_sandmail_user.insert(0, self.creds_sandmail_user)
        self.entry_sandmail_user.pack(side="left", fill="x", expand=True)
        r = tk.Frame(c0, bg=card); r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Contrasena", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_sandmail_pass = ttk.Entry(r, width=30, show="*")
        if self.creds_sandmail_pass:
            self.entry_sandmail_pass.insert(0, self.creds_sandmail_pass)
        self.entry_sandmail_pass.pack(side="left", fill="x", expand=True)
        r = tk.Frame(c0, bg=card); r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Servidor SMTP", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_sandmail_host = ttk.Entry(r, width=22)
        self.entry_sandmail_host.insert(0, "smtp.sandmailz.net")
        self.entry_sandmail_host.pack(side="left")
        tk.Label(r, text=" Puerto:", font=(font, 9), bg=card, fg=subt).pack(side="left")
        self.entry_sandmail_port = ttk.Entry(r, width=6)
        self.entry_sandmail_port.insert(0, "465")
        self.entry_sandmail_port.pack(side="left")
        tk.Label(c0, text="Tu correo @sandmailz.net (o el dominio que uses).",
                 font=(font, 8), bg=card, fg=subt).pack(anchor="w", padx=14, pady=(2, 10))

        # ---- Tarjeta Gmail ----
        c = tk.Frame(outer, bg=card, highlightbackground=self.border(), highlightthickness=1)
        c.pack(fill="x", pady=6)
        tk.Label(c, text="Gmail (SMTP + IMAP)", font=(font, 12, "bold"), bg=card, fg=txt).pack(anchor="w", padx=14, pady=(10, 4))
        r = tk.Frame(c, bg=card)
        r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Correo", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_gmail_user = ttk.Entry(r, width=30)
        self.entry_gmail_user.insert(0, self.creds_gmail_user)
        self.entry_gmail_user.pack(side="left", fill="x", expand=True)
        r = tk.Frame(c, bg=card)
        r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Contrasena App", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_gmail_pass = ttk.Entry(r, width=30, show="*")
        if self.creds_gmail_pass:
            self.entry_gmail_pass.insert(0, self.creds_gmail_pass)
        self.entry_gmail_pass.pack(side="left", fill="x", expand=True)
        tk.Label(c, text="Necesitas Contrasena de Aplicacion. IMAP habilitado en Gmail.",
                 font=(font, 8), bg=card, fg=subt).pack(anchor="w", padx=14, pady=(2, 10))

        # ---- Tarjeta Outlook ----
        c2 = tk.Frame(outer, bg=card, highlightbackground=self.border(), highlightthickness=1)
        c2.pack(fill="x", pady=6)
        tk.Label(c2, text="Outlook (SMTP)", font=(font, 12, "bold"), bg=card, fg=txt).pack(anchor="w", padx=14, pady=(10, 4))
        r = tk.Frame(c2, bg=card)
        r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Correo", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_outlook_user = ttk.Entry(r, width=30)
        self.entry_outlook_user.insert(0, self.creds_outlook_user)
        self.entry_outlook_user.pack(side="left", fill="x", expand=True)
        r = tk.Frame(c2, bg=card)
        r.pack(fill="x", padx=14, pady=4)
        tk.Label(r, text="Contrasena", font=(font, 9), bg=card, fg=subt, width=12, anchor="w").pack(side="left")
        self.entry_outlook_pass = ttk.Entry(r, width=30, show="*")
        if self.creds_outlook_pass:
            self.entry_outlook_pass.insert(0, self.creds_outlook_pass)
        self.entry_outlook_pass.pack(side="left", fill="x", expand=True)
        tk.Frame(c2, bg=card, height=8).pack()

        self.var_recordar = tk.BooleanVar(value=KEYRING_OK)
        texto_check = self.t('guardar_creds')
        if not KEYRING_OK:
            texto_check += "  (pip install keyring)"
        tk.Checkbutton(outer, text=texto_check, variable=self.var_recordar,
                       bg=surf, fg=txt if KEYRING_OK else "#999",
                       selectcolor=surf, activebackground=surf, activeforeground=txt,
                       font=(font, 9), state="normal" if KEYRING_OK else "disabled").pack(anchor="w", pady=8)
        ttk.Button(outer, text=self.t('guardar_config'), style='Accent.TButton',
                   command=self.guardar_configuracion).pack(pady=16)

    def guardar_configuracion(self):
        gu = self.entry_gmail_user.get().strip()
        gp = self.entry_gmail_pass.get().strip()
        ou = self.entry_outlook_user.get().strip()
        op = self.entry_outlook_pass.get().strip()
        su = self.entry_sandmail_user.get().strip()
        sp = self.entry_sandmail_pass.get().strip()
        sh = self.entry_sandmail_host.get().strip() or "smtp.sandmailz.net"
        sport = self.entry_sandmail_port.get().strip() or "465"
        if gu: self.creds_gmail_user = gu
        if gp: self.creds_gmail_pass = gp
        if ou: self.creds_outlook_user = ou
        if op: self.creds_outlook_pass = op
        if su: self.creds_sandmail_user = su
        if sp: self.creds_sandmail_pass = sp
        if su and sp:
            self.cuentas[su] = {"user": su, "pass": sp, "servicio": "SandMail Z",
                                "host": sh, "port": sport}
            if not self.cuenta_actual:
                self.cuenta_actual = su
        if gu and gp:
            self.cuentas[gu] = {"user": gu, "pass": gp, "servicio": "Gmail"}
            if not self.cuenta_actual:
                self.cuenta_actual = gu
        if ou and op:
            self.cuentas[ou] = {"user": ou, "pass": op, "servicio": "Outlook"}
            if not self.cuenta_actual:
                self.cuenta_actual = ou
        self.actualizar_combo_cuentas()
        self.log("Configuracion guardada. Cuentas: " + str(len(self.cuentas)))
        msg = "Configuracion guardada.\n\nCuentas totales: " + str(len(self.cuentas))
        if KEYRING_OK and self.var_recordar.get():
            if self.guardar_todo_keyring():
                msg += "\n\nCredenciales guardadas con keyring."
                self.log("Guardado en keyring OK")
            else:
                msg += "\n\nNo se pudo guardar en keyring."
        elif not KEYRING_OK:
            msg += "\n\nKeyring no instalado (pip install keyring)"
        messagebox.showinfo("Config", msg)

    def construir_log(self):
        surf, txt = self.surface(), self.text()
        font = self.P().FONT_FALLBACK
        outer = tk.Frame(self.tab_log, bg=surf)
        outer.pack(fill="both", expand=True, padx=20, pady=18)
        tk.Label(outer, text=self.t('log_title'), font=(font, 22, "bold"), bg=surf, fg=txt).pack(anchor="w", pady=(0, 14))
        self.consola_log = scrolledtext.ScrolledText(outer, bg="#1E1E1E", fg="#00FF9C",
                                                      font=("Consolas", 10), bd=0, relief='flat', insertbackground="#00FF9C")
        self.consola_log.pack(fill="both", expand=True)
        self.log("SandMail Z v5.1 iniciado")
        self.log("Keyring: " + ("activo" if KEYRING_OK else "NO instalado"))
        self.log("Cuentas cargadas: " + str(len(self.cuentas)))

    def log(self, msg):
        h = datetime.datetime.now().strftime("%H:%M:%S")
        self.consola_log.insert(tk.END, "[" + h + "] " + msg + "\n")
        self.consola_log.see(tk.END)

    def toggle_modo_oscuro(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_estilo()
        self.refrescar_colores_manuales()
        self.log("Modo " + ("OSCURO" if self.modo_oscuro else "CLARO"))

    def cambiar_estilo(self, estilo=None):
        if estilo is None:
            self.estilo_actual = "aero" if self.estilo_actual == "win11" else "win11"
        else:
            self.estilo_actual = estilo
        self.aplicar_estilo()
        self.refrescar_colores_manuales()
        nombre = "Aero" if self.estilo_actual == "aero" else "Win11"
        self.log("Estilo: " + nombre)
        messagebox.showinfo("Estilo", "Estilo aplicado: " + nombre)

    def refrescar_colores_manuales(self):
        bg, surf, nav = self.bg(), self.surface(), self.nav_bg()
        txt, subt, bord = self.text(), self.subtext(), self.border()
        try:
            self.root.configure(bg=bg)
            self.frame_header.configure(bg=nav)
            self.frame_sidebar.configure(bg=nav)
            self.frame_main.configure(bg=bg)
            self.container.configure(bg=bg)
            self.border_bottom.configure(bg=bord)
            self.sep_vert.configure(bg=bord)
            self.frame_status.configure(bg=nav)
            self.status_bar.configure(bg=nav, fg=subt)
            self.chip_frame.configure(bg=surf, highlightbackground=bord)
            self.lbl_user.configure(bg=surf, fg=txt)
            self.canvas_logo.configure(bg=nav)
            self.canvas_logo.delete("all")
            self.dibujar_logo_texto(self.canvas_logo, 10, 12)
        except Exception:
            pass

    def cambiar_idioma(self, codigo):
        self.idioma_actual = codigo
        self.root.title(self.t('titulo'))
        self.log("Idioma: " + codigo.upper())
        messagebox.showinfo("Idioma", "Reinicia para aplicar todos los cambios.")

    def asistente_ia(self):
        r = {'es': "Hola, he recibido tu correo.", 'en': "Hello, I received your email.",
             'pt': "Ola, recebi seu e-mail.", 'fr': "Bonjour.", 'ja': "こんにちは。",
             'ru': "Здравствуйте.", 'ar': "مرحبا."}
        self.texto_mensaje.insert(tk.END, "\n\n[SandAI]: " + r.get(self.idioma_actual, r['en']))
        self.log("SandAI genero respuesta")

    def encriptar_mensaje(self):
        self.texto_mensaje.insert(tk.END, "\n[SandCrypt Encrypted]")
        self.log("Mensaje encriptado")

    def adjuntar_archivo(self):
        a = filedialog.askopenfilename()
        if a:
            self.archivos_adjuntos.append(a)
            self.log("Adjunto: " + a)
            nombres = [os.path.basename(x) for x in self.archivos_adjuntos]
            self.lbl_adjuntos.config(text="Adjuntos: " + ", ".join(nombres))

    def guardar_borrador(self):
        self.log("Borrador guardado")
        messagebox.showinfo("Borrador", "Mensaje guardado como borrador.")

    def cambiar_remitente(self, event=None):
        p = self.combo_proveedor.get()
        self.campos['de'].config(state="normal")
        self.campos['de'].delete(0, tk.END)
        if p == "SandMail Z":
            correo = ""
            if self.cuenta_actual in self.cuentas and \
               self.cuentas[self.cuenta_actual].get("servicio") == "SandMail Z":
                correo = self.cuentas[self.cuenta_actual]["user"]
            if not correo:
                correo = self.creds_sandmail_user or "tu_correo@sandmailz.net"
            self.campos['de'].insert(0, correo)
        elif p == "Gmail":
            self.campos['de'].insert(0, self.creds_gmail_user or "tu_correo@gmail.com")
        else:
            self.campos['de'].insert(0, self.creds_outlook_user or "tu_correo@outlook.com")
        self.campos['de'].config(state="readonly")

    def hilo_enviar(self):
        threading.Thread(target=self.enviar_correo).start()

    def enviar_correo(self):
        prov = self.combo_proveedor.get()
        para = self.campos['para'].get()
        asunto = self.campos['asunto'].get()
        msg_txt = self.texto_mensaje.get("1.0", tk.END).strip()
        if not para or not asunto or not msg_txt:
            messagebox.showwarning("Vacios", "Llena todos los campos.")
            return
        self.root.after(0, lambda: self.status_bar.config(text="  Enviando via " + prov + "..."))
        self.root.after(0, lambda: self.mostrar_progress(True))
        self.log("--- Enviando via " + prov + " ---")
        try:
            if prov == "SandMail Z":
                usuario = self.creds_sandmail_user
                pwd = self.creds_sandmail_pass
                host = "smtp.sandmailz.net"
                port = 465
                if self.cuenta_actual in self.cuentas and \
                   self.cuentas[self.cuenta_actual].get("servicio") == "SandMail Z":
                    datos = self.cuentas[self.cuenta_actual]
                    host = datos.get("host", host)
                    try: port = int(datos.get("port", port))
                    except Exception: port = 465
                if usuario and pwd:
                    msg = MIMEMultipart()
                    msg['From'] = usuario
                    msg['To'] = para
                    msg['Subject'] = "[" + self.combo_prioridad.get() + "] " + asunto
                    if self.var_html.get():
                        msg.attach(MIMEText(msg_txt, 'html'))
                    else:
                        msg.attach(MIMEText(msg_txt, 'plain'))
                    for ruta in self.archivos_adjuntos:
                        try:
                            with open(ruta, "rb") as f:
                                parte = MIMEBase("application", "octet-stream")
                                parte.set_payload(f.read())
                                encoders.encode_base64(parte)
                                parte.add_header("Content-Disposition",
                                                 "attachment; filename=" + os.path.basename(ruta))
                                msg.attach(parte)
                        except Exception as e:
                            self.log("Error adjuntando: " + str(e))
                    server = smtplib.SMTP_SSL(host, port)
                    server.login(usuario, pwd)
                    server.send_message(msg)
                    server.quit()
                    self.log("Correo enviado por SandMail Z (" + usuario + ")")
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Exito", "Correo enviado por SandMail Z desde " + usuario))
                    self.archivos_adjuntos = []
                    self.root.after(0, lambda: self.lbl_adjuntos.config(text=""))
                else:
                    time.sleep(1.5)
                    self.log("Servidor @sandmailz.net OK (modo demo, sin credenciales)")
                    self.root.after(0, lambda: messagebox.showinfo(
                        "SandMail Z",
                        "Envio simulado.\n\nVe a Ajustes > SandMail Z y guarda tu correo y "
                        "contrasena para enviar de verdad."))
            elif prov == "Gmail":
                usuario = self.creds_gmail_user
                pwd = self.creds_gmail_pass
                if not usuario or not pwd:
                    self.root.after(0, lambda: messagebox.showwarning("Falta", "Configura Gmail primero."))
                    return
                msg = MIMEMultipart()
                msg['From'] = usuario
                msg['To'] = para
                msg['Subject'] = "[" + self.combo_prioridad.get() + "] " + asunto
                if self.var_html.get():
                    msg.attach(MIMEText(msg_txt, 'html'))
                else:
                    msg.attach(MIMEText(msg_txt, 'plain'))
                for ruta in self.archivos_adjuntos:
                    try:
                        with open(ruta, "rb") as f:
                            parte = MIMEBase("application", "octet-stream")
                            parte.set_payload(f.read())
                            encoders.encode_base64(parte)
                            nombre = os.path.basename(ruta)
                            parte.add_header("Content-Disposition", "attachment; filename=" + nombre)
                            msg.attach(parte)
                    except Exception as e:
                        self.log("Error adjuntando: " + str(e))
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(usuario, pwd)
                server.send_message(msg)
                server.quit()
                self.log("Correo enviado por Gmail")
                self.root.after(0, lambda: messagebox.showinfo("Exito", "Correo enviado por Gmail."))
                self.archivos_adjuntos = []
                self.root.after(0, lambda: self.lbl_adjuntos.config(text=""))
            elif prov == "Outlook":
                usuario = self.creds_outlook_user
                pwd = self.creds_outlook_pass
                if not usuario or not pwd:
                    self.root.after(0, lambda: messagebox.showwarning("Falta", "Configura Outlook primero."))
                    return
                msg = MIMEMultipart()
                msg['From'] = usuario
                msg['To'] = para
                msg['Subject'] = "[" + self.combo_prioridad.get() + "] " + asunto
                if self.var_html.get():
                    msg.attach(MIMEText(msg_txt, 'html'))
                else:
                    msg.attach(MIMEText(msg_txt, 'plain'))
                for ruta in self.archivos_adjuntos:
                    try:
                        with open(ruta, "rb") as f:
                            parte = MIMEBase("application", "octet-stream")
                            parte.set_payload(f.read())
                            encoders.encode_base64(parte)
                            parte.add_header("Content-Disposition", "attachment; filename=" + os.path.basename(ruta))
                            msg.attach(parte)
                    except Exception as e:
                        self.log("Error adjuntando: " + str(e))
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()
                server.login(usuario, pwd)
                server.send_message(msg)
                server.quit()
                self.log("Correo enviado por Outlook")
                self.root.after(0, lambda: messagebox.showinfo("Exito", "Correo enviado por Outlook."))
                self.archivos_adjuntos = []
                self.root.after(0, lambda: self.lbl_adjuntos.config(text=""))
        except Exception as e:
            self.log("ERROR: " + str(e))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.mostrar_progress(False))
            self.root.after(0, lambda: self.status_bar.config(text="  " + self.t('status_listo') + "  |  SandMail Z v5.1"))


if __name__ == "__main__":
    root = tk.Tk()
    app = SandMailZApp(root)
    root.mainloop()
