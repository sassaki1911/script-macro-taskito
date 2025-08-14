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
    {"Número": 1, "Nome": "ANA CLARA NUNES GATINI", "Login": "1104434891sp", "Senha": "Mcc@ac29"},  
    {"Número": 2, "Nome": "ALYSSOM COSTA BARBOSA", "Login": "1105748674sp", "Senha": "Mcc@ac17"},    
    {"Número": 3, "Nome": "ANA CLARA JUDITE ALVES SILVA", "Login": "1117104679sp", "Senha": "Mcc@ac25"},  
    {"Número": 4, "Nome": "ANA KLARA OLIVEIRA", "Login": "1126699998sp", "Senha": "Mcc@ak30"},      
    {"Número": 5, "Nome": "ANNA JULLYA COSTA DE SÁ", "Login": "1100174436sp", "Senha": "Mcc@aj08"},  
    {"Número": 6, "Nome": "BARBARA MILLER RAMOS", "Login": "1121888343sp", "Senha": "Mcc@bm08"},    
    {"Número": 7, "Nome": "BRYAN ALVES", "Login": "1101848200sp", "Senha": "Mcc@ba06"},           
    {"Número": 8, "Nome": "DANIELA NOBERTO DE LIMA", "Login": "1116083978sp", "Senha": "Mcc@dn22"}, 
    {"Número": 9, "Nome": "DENILSON MARINI FEDOSSI", "Login": "1107617716sp", "Senha": "Mcc@dm19"}, 
    {"Número": 10, "Nome": "DOUGLAS WALLYSON VINICIUS MENEZES MASSOLA", "Login": "1096843213sp", "Senha": "Mcc@dw24"},  
    {"Número": 11, "Nome": "ENZO RODRIGO DOS SANTOS PINTO", "Login": "1133687647sp", "Senha": "Mcc@er18"},
    {"Número": 12, "Nome": "FLÁVIA EDUARDA MACHADO", "Login": "1127687451sp", "Senha": "Mcc@fe15"},  
    {"Número": 13, "Nome": "GABRIEL LIMA GONÇALVES", "Login": "1116081787sp", "Senha": "Mcc@gl30"},  
    {"Número": 14, "Nome": "GUSTAVO TEIXEIRA AMÉNDOLA", "Login": "1133686862sp", "Senha": "Mcc@gt03"},  
    {"Número": 15, "Nome": "HELENA DOS SANTOS COLEONI", "Login": "1133673314sp", "Senha": "Mcc@hs02"},  
    {"Número": 16, "Nome": "HELOÃ YSABELLE DIAS", "Login": "1133661348sp", "Senha": "Mcc@hy09"},    
    {"Número": 17, "Nome": "HOMERO DE MELLO ALVES", "Login": "1111423854sp", "Senha": "Mcc@hm23"},  
    {"Número": 18, "Nome": "JOANA DE LUCAS PEIXE BARBOSA ALVES", "Login": "1126685690sp", "Senha": "Mcc@jl08"},  
    {"Número": 19, "Nome": "JOÃO LUCAS SOARES CARDOSO", "Login": "113374929Xsp", "Senha": "Mcc@jl06"},  
    {"Número": 20, "Nome": "JOÃO PAULO DOS SANTOS MARTINS", "Login": "1133748867sp", "Senha": "Mcc@jp29"},  
    {"Número": 21, "Nome": "JOÃO PEDRO BARCELLOS", "Login": "1126596218sp", "Senha": "Mcc@jp06"},     # J (JOÃO) + P (PEDRO)
    {"Número": 22, "Nome": "JOÃO VITOR DOS REIS", "Login": "1108987187sp", "Senha": "Mcc@jv26"},      # J (JOÃO) + V (VITOR)
    {"Número": 23, "Nome": "JONATAS PEREIRA DOS SANTOS", "Login": "1131934313sp", "Senha": "Mcc@jp15"},  # J (JONATAS) + P (PEREIRA)
    {"Número": 24, "Nome": "JÚLIA CALIXTO", "Login": "113370248Xsp", "Senha": "Mcc@jc15"},           # J (JÚLIA) + C (CALIXTO)
    {"Número": 25, "Nome": "JÚLIA COMPARETTO ALVES", "Login": "1098432940sp", "Senha": "Mcc@jc10"},  # J (JÚLIA) + C (COMPARETTO)
    {"Número": 26, "Nome": "KAUÉ EDUARDO PREVIATO DE ALMEIDA", "Login": "110273715Xsp", "Senha": "Mcc@ke25"},  # K (KAUÉ) + E (EDUARDO)
    {"Número": 27, "Nome": "LUIGI GABRIEL ORLANDO CARDOSO", "Login": "1111786963sp", "Senha": "Mcc@lg18"},  # L (LUIGI) + G (GABRIEL)
    {"Número": 28, "Nome": "LURIANY CASTILHO GODOY", "Login": "1133701139sp", "Senha": "Mcc@lc24"},  # L (LURIANY) + C (CASTILHO)
    {"Número": 29, "Nome": "MANASSÉS GONÇALVES ANTONIO", "Login": "1104625258sp", "Senha": "Mcc@mg13"},  # M (MANASSÉS) + G (GONÇALVES)
    {"Número": 30, "Nome": "MAYTÉ FRANCISCO DAS CHAGAS", "Login": "1096493913sp", "Senha": "Mcc@mf26"},  # M (MAYTÉ) + F (FRANCISCO)
    {"Número": 31, "Nome": "MARYANE VICTÓRIA VIEIRA", "Login": "1133747784sp", "Senha": "Mcc@mv03"},  # M (MARYANE) + V (VICTÓRIA)
    {"Número": 32, "Nome": "MIGUEL DE SOUZA CAMPREGHER", "Login": "1133674033sp", "Senha": "Mcc@ms29"},  # M (MIGUEL) + S (SOUZA)
    {"Número": 33, "Nome": "MIGUEL LEITE PEREIRA", "Login": "1116285800sp", "Senha": "Mcc@ml02"},     # M (MIGUEL) + L (LEITE)
    {"Número": 34, "Nome": "NATACHA FAUSTINO DIAS MAZOCHO", "Login": "1146165900sp", "Senha": "Mcc@nf21"},  # N (NATACHA) + F (FAUSTINO)
    {"Número": 35, "Nome": "RICARDO FERNANDES SOUSA", "Login": "1108980429sp", "Senha": "Mcc@rf31"},  # R (RICARDO) + F (FERNANDES)
    {"Número": 36, "Nome": "RICHARD DO CARMO SANTI", "Login": "1133748387sp", "Senha": "Mcc@rc12"},  # R (RICHARD) + C (CARMO)
    {"Número": 37, "Nome": "THALYA GABRIELA GOMES FRANCISCO", "Login": "1095619603sp", "Senha": "Mcc@tg16"},  # T (THALYA) + G (GABRIELA)
    {"Número": 38, "Nome": "THAMILLY VICTÓRIA DUARTE DE AMORIM", "Login": "1108679626sp", "Senha": "Mcc@tv16"},  # T (THAMILLY) + V (VICTÓRIA)
    {"Número": 39, "Nome": "VIKTOR GABRIEL EVANGELISTA VIERA", "Login": "1115758470sp", "Senha": "Mcc@vg11"},  # V (VIKTOR) + G (GABRIEL)
    {"Número": 40, "Nome": "VINICIUS LUIZ OLIVEIRA DE ALMEIDA", "Login": "1133673624sp", "Senha": "Mcc@vl06"},  # V (VINICIUS) + L (LUIZ)
    {"Número": 41, "Nome": "VINICIUS ROBERTO RODRIGUES AMBROZIO", "Login": "1120706919sp", "Senha": "Mcc@vr15"},  # V (VINICIUS) + R (ROBERTO)
    {"Número": 42, "Nome": "YASMIN DA SILVA ALEXANDRE", "Login": "1107046658sp", "Senha": "Mcc@yd24"},  # Y (YASMIN) + D (DA)
    {"Número": 43, "Nome": "JULIANO DO CARMO MILLER", "Login": "1133663667sp", "Senha": "Mcc@jc07"},   # J (JULIANO) + C (CARMO)
    {"Número": 44, "Nome": "KAIO HENRICK NALIN RAMOS", "Login": "1106358922sp", "Senha": "Mcc@kh10"}   # K (KAIO) + H (HENRICK)
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
