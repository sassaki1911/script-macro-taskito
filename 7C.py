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
    {"Número": 1, "Nome": "ABNER MIGUEL DE SOUZA GUERRA", "Login": "114311145xsp", "Senha": "Mcc@am27"},
    {"Número": 2, "Nome": "ANTONELLA CAMILO DA SILVA", "Login": "1160460279sp", "Senha": "Mcc@ac09"},
    {"Número": 3, "Nome": "ARTHUR VIDESCHI KREPSKER", "Login": "114251156xsp", "Senha": "Mcc@av11"},
    {"Número": 4, "Nome": "EDUARDO BORGES DA SILVA ELLEBROKE", "Login": "1160432776sp", "Senha": "Mcc@eb25"},
    {"Número": 5, "Nome": "FERNANDA HELENA DA SILVA MELO", "Login": "1160103628sp", "Senha": "Mcc@fh24"},
    {"Número": 6, "Nome": "GUILHERME PORTO DE FRANÇA", "Login": "1145792200sp", "Senha": "Mcc@gp22"},
    {"Número": 7, "Nome": "HIAGO DO CARMO BARBOSA", "Login": "1141950790sp", "Senha": "Mcc@hc22"},
    {"Número": 8, "Nome": "KAUANY YASMIN MARQUES LIMA", "Login": "1158608123sp", "Senha": "Mcc@ky25"},
    {"Número": 9, "Nome": "LAÚNA SANCHES VIEIRA", "Login": "1150482941sp", "Senha": "Mcc@ls15"},
    {"Número": 10, "Nome": "LAURA DE SOLZA BRITO", "Login": "116107269xsp", "Senha": "Mcc@ls01"},
    {"Número": 11, "Nome": "LORENZO GABRIEL MULLER BERTOLLO", "Login": "1133603269sp", "Senha": "Mcc@lg27"},
    {"Número": 12, "Nome": "LUAN FELIPE MIRANDA RILKO", "Login": "1132524118sp", "Senha": "Mcc@lf22"},
    {"Número": 13, "Nome": "LUCAS MIGUEL SULATI", "Login": "1165383160sp", "Senha": "Mcc@ls03"},
    {"Número": 14, "Nome": "LUIS MIGUEL LEME DE MATOS", "Login": "1161072676sp", "Senha": "Mcc@lm03"},
    {"Número": 15, "Nome": "LUIZ ANTÓNIO SANTOS ORLANDO", "Login": "114014067xsp", "Senha": "Mcc@la11"},
    {"Número": 16, "Nome": "MARIA PAULA SANTOS ORLANDO", "Login": "1140140437sp", "Senha": "Mcc@mp11"},
    {"Número": 17, "Nome": "MIGUEL POLTRONIERI SOBRAL", "Login": "1214813902sp", "Senha": "Mcc@mp27"},
    {"Número": 18, "Nome": "NICOLY VITÓRIA FRANCISCO DO NASCIMENTO", "Login": "1145312871sp", "Senha": "Mcc@nv22"},
    {"Número": 19, "Nome": "OTÁVIO DE OLIVEIRA COSTA", "Login": "1151690004sp", "Senha": "Mcc@oc16"},
    {"Número": 20, "Nome": "PEDRO AUGUSTO OLICERIO DE AGUIAR", "Login": "1125356510sp", "Senha": "Mcc@pa23"},
    {"Número": 21, "Nome": "THIAGO MARQUES CLEMENTINO", "Login": "1163624883sp", "Senha": "Mcc@tm27"},
    {"Número": 22, "Nome": "VITÓRIA DOMINGUES DA SILVA", "Login": "1162768630sp", "Senha": "Mcc@vd01"},
    {"Número": 23, "Nome": "YURI TREVIZAN GUERBAS", "Login": "1159495841sp", "Senha": "Mcc@yg14"},
    {"Número": 24, "Nome": "MARIA CLARA GRANZOTTI SILVA FUMIS", "Login": "1139964393sp", "Senha": "Mcc@mc03"},
    {"Número": 25, "Nome": "ALYCIA EVELLY SILVA BATISTA", "Login": "1260835420sp", "Senha": "Mcc@ae17"},
    {"Número": 26, "Nome": "ISAQUE CAMARA", "Login": "1260959140sp", "Senha": "Mcc@ic17"}
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
