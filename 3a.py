import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Configurações
URL = "https://taskitos.cupiditys.lol/"
HEADLESS = False  # True para rodar sem abrir janela, False para visível
TIMEOUT = 30  # tempo máximo para espera explícita

# Dados dos alunos em formato JSON (numerados)
STUDENTS_DATA = [
    {"Número": 1, "Nome": "MELISSA CAROLINE ARISTIDES GONÇALVES", "Login": "1120489039sp", "Senha": "Mcc@mc29"},
    {"Número": 2, "Nome": "GUSTAVO DEZANETTI BASTOS NETO", "Login": "1113801062sp", "Senha": "Mcc@gd25"},
    {"Número": 3, "Nome": "FLÁVIO DE OLIVEIRA IZIQUE MENDES", "Login": "111431206xsp", "Senha": "Mcc@fo02"},
    {"Número": 4, "Nome": "SUELEN JULIÃO CAVALCANTE", "Login": "1113574562sp", "Senha": "Mcc@sj04"},
    {"Número": 5, "Nome": "THÉO POMPÉO MAZZUCCA", "Login": "1099634799sp", "Senha": "Mcc@tp14"},
    {"Número": 6, "Nome": "THIAGO DA SILVA MENEZES FELTRIN", "Login": "1075579715sp", "Senha": "Mcc@ts16"},
    {"Número": 7, "Nome": "TOMMASO RENZETTI", "Login": "1109484392sp", "Senha": "Mcc@tr27"},
    {"Número": 8, "Nome": "VICTOR HUGO DE SOUZA", "Login": "1113800732sp", "Senha": "Mcc@vh27"},
    {"Número": 9, "Nome": "VICTÓRIA BOCUTO PREVIATO", "Login": "111431156xsp", "Senha": "Mcc@vb11"},
    {"Número": 10, "Nome": "VINICIUS ANDERSON VITORINO", "Login": "1115902234sp", "Senha": "Mcc@va26"},
    {"Número": 11, "Nome": "YALEN CASTRO FONSECA", "Login": "1212995260sp", "Senha": "Mcc@yc16"},
    {"Número": 12, "Nome": "YURI TETSUO MIRANDA SITANAKA", "Login": "1106720189sp", "Senha": "Mcc@yt06"},
    {"Número": 13, "Nome": "MIGUEL HENRIQUE ROMÃO BRUNHETTI", "Login": "1060068138sp", "Senha": "Mcc@mh20"},
    {"Número": 14, "Nome": "RAAJLA IAKAIKA DE MENEZES MONTEDORI CARVALHO", "Login": "1111121497sp", "Senha": "Mcc@ri02"},
    {"Número": 15, "Nome": "RENATO GABRIEL ROCHA SANTOS DE OLIVEIRA", "Login": "1107728939sp", "Senha": "Mcc@rg18"},
    {"Número": 16, "Nome": "ROBSON RODRIGUES MURÇA", "Login": "1107054345sp", "Senha": "Mcc@rr19w"},
    {"Número": 17, "Nome": "ALICE PRIMANI MILANI", "Login": "1113801104sp", "Senha": "Mcc@ap31"},
    {"Número": 18, "Nome": "ANA BEATRYS MASSONI DOS REIS", "Login": "1100175453sp", "Senha": "Mcc@ab15"},
    {"Número": 19, "Nome": "DAIRO DA SILVA GUERRA BIANCONI", "Login": "1088121767sp", "Senha": "Mcc@ds17"},
    {"Número": 20, "Nome": "DAVI MATHEUS DA SILVA LIMA", "Login": "1084488620sp", "Senha": "Mcc@dm30"},
    {"Número": 21, "Nome": "EDUARDA VITÓRIA DE OLIVEIRA", "Login": "1085699432sp", "Senha": "Mcc@ev28"},
    {"Número": 22, "Nome": "EMILLY FERREIRA ALVES", "Login": "1130327073sp", "Senha": "Mcc@ef28"},
    {"Número": 23, "Nome": "ENZO RYU LIMA SASSAKI", "Login": "1104544519sp", "Senha": "Mcc@er19"},
    {"Número": 24, "Nome": "ESTER DA SILVA", "Login": "1119480139sp", "Senha": "Mcc@es23"},
    {"Número": 25, "Nome": "GIOVANNI PENAROTI CARDOSO", "Login": "1088593288sp", "Senha": "Mcc@gp03"},
    {"Número": 26, "Nome": "FELIPE CAETANO DE ALMEIDA", "Login": "1113800975sp", "Senha": "Mcc@fc04"},
    {"Número": 27, "Nome": "GEOVANA MARÇAL LIBORIO DA ROCHA", "Login": "122908759xsp", "Senha": "Mcc@gm14"},
    {"Número": 28, "Nome": "GUILHERME FERREIRA DE MELO", "Login": "1085032772sp", "Senha": "Mcc@gf08"},
    {"Número": 29, "Nome": "ISAQUE FERNANDO DIAS PIMENTA", "Login": "1101849010sp", "Senha": "Mcc@if07"},
    {"Número": 30, "Nome": "JELDYS FERNANDO ANTONIO PEREIRA", "Login": "1096664641sp", "Senha": "Mcc@jf27"},
    {"Número": 31, "Nome": "KAUAN ALVES DOS SANTOS", "Login": "1136374474sp", "Senha": "Mcc@ka05"},
    {"Número": 32, "Nome": "LARA LEANI DA CONCEIÇÃO", "Login": "1081730195sp", "Senha": "Mcc@ll01"},
    {"Número": 33, "Nome": "MARIA CLARA PARRA DE OLIVEIRA", "Login": "1113800938sp", "Senha": "Mcc@mc03"},
    {"Número": 34, "Nome": "MARIANY JULIA GOMES", "Login": "1086341922sp", "Senha": "Mcc@mj02"},
    {"Número": 35, "Nome": "MARIANA LEITE GOMES", "Login": "1113800744sp", "Senha": "Mcc@ml12"},
    {"Número": 36, "Nome": "MATTEUS FERNANDO BUSO", "Login": "1091346100sp", "Senha": "Mcc@mf07"},
    {"Número": 37, "Nome": "MAYKON SANTOS DE ALMEIDA", "Login": "1115047863sp", "Senha": "Mcc@ms28"},
    {"Número": 38, "Nome": "MICAEL HENRIQUE PAZ DA SILVA", "Login": "1121697379sp", "Senha": "Mcc@mh26"},
]

def setup_driver(headless: bool) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")  # erro somente, sem info ou warning
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver

def wait_for_verificado_checkbox(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    try:
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "label.altcha-label"),
                "Verificado"
            )
        )
    except:
        pass

def wait_for_notification(driver, timeout=10, poll_frequency=0.5):
    """
    Espera até `timeout` segundos por uma notificação visível.
    Retorna:
    - 'no_activities' se detectar notificação "Nenhuma atividades encontrada"
    - 'login_fail' se detectar notificação "Falha no login"
    - 'none' se nenhuma notificação aparecer no tempo
    """
    elapsed = 0
    while elapsed < timeout:
        try:
            notif_div = driver.find_element(By.CSS_SELECTOR, "div.notification.show > div.notification-content > p")
            text = notif_div.text.strip()
            if "Nenhuma atividades encontrada" in text:
                return "no_activities"
            if "Falha no login" in text:
                return "login_fail"
        except NoSuchElementException:
            pass
        time.sleep(poll_frequency)
        elapsed += poll_frequency
    return "none"

def wait_for_activities_modal(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-content.large"))
    )

def wait_for_processing_to_finish(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    try:
        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div#progressStatus strong")
            )
        )
        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.progress-content"))
        )
    except:
        pass

def process_student(driver, login: str, password: str) -> bool:
    driver.get(URL)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Preenche login
        student_id_input = wait.until(EC.presence_of_element_located((By.ID, "studentId")))
        student_id_input.clear()
        student_id_input.send_keys(login)

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)

        # Espera o "Verificado"
        wait_for_verificado_checkbox(driver)

        # Clica em Atividades Pendentes
        btn_atividades = driver.find_element(By.ID, "loginNormal")
        btn_atividades.click()

        # Aguarda notificações por até 10 segundos
        notif = wait_for_notification(driver, timeout=10)
        if notif == "login_fail":
            print(f"❌ Falha no login: {login}")
            return False

        if notif == "no_activities":
            print(f"✅ Login OK, mas sem atividades para: {login}")
            return True

        # Se não teve notificação, espera modal aparecer
        wait_for_activities_modal(driver)

        # Clica em Fazer Lições Todas
        btn_fazer_todas = driver.find_element(By.ID, "startAllActivities")
        btn_fazer_todas.click()

        # Aguarda 20 segundos + espera fim processamento
        time.sleep(20)
        wait_for_processing_to_finish(driver)

        # Atualiza página antes de ir para próximo login
        driver.refresh()
        time.sleep(5)

        print(f"✅ Atividades concluídas para: {login}")
        return True

    except Exception as e:
        print(f"❌ Erro ao processar {login}: {e}")
        return False

def main():
    driver = setup_driver(HEADLESS)

    total = len(STUDENTS_DATA)  # Total de alunos
    success = 0
    failure = 0

    try:
        for student in STUDENTS_DATA:
            login = student["Login"]
            password = student["Senha"]
            current_num = student["Número"]  # Pega o número do aluno atual
            
            print(f"\n➡️ Processando {login} ({current_num}/{total})...")
            result = process_student(driver, login, password)
            if result:
                success += 1
            else:
                failure += 1

    finally:
        driver.quit()

    print("\n==== Resultado Final ====")
    print(f"Total de alunos: {total}")
    print(f"Sucesso: {success}")
    print(f"Falhas: {failure}")

if __name__ == "__main__":
    main()
