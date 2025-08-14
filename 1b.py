import json
import time
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # pyright: ignore[reportMissingImports]
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore

# Configurações
URL = "https://taskitos.cupiditys.lol/"
HEADLESS = False  # True para rodar sem abrir janela, False para visível
TIMEOUT = 30  # tempo máximo para espera explícita

# Dados dos alunos em formato JSON
STUDENTS_DATA = [
    {"Nome": "ALYSSOM COSTA BARBOSA", "Login": "1105748674sp", "Senha": "Mcc@ac17"},
    {"Nome": "ANA CLARA JUDITE ALVES SILVA", "Login": "1117104679sp", "Senha": "Mcc@ac25"},
    {"Nome": "ANA CECÍLIA SAMPIETRO DA SILVA", "Login": "1098965000sp", "Senha": "Mcc@ac02"},
    {"Nome": "ANA CLARA NUNES GATINI", "Login": "1104434891sp", "Senha": "Mcc@ac29"},
    {"Nome": "ANTHONY BERNARDO BRANDÃO MACHADO DA SILVA", "Login": "1115061471sp", "Senha": "Mcc@ab06"},
    {"Nome": "BERNARDO PRIMANI OLIVEIRA", "Login": "1109839443sp", "Senha": "Mcc@bp28"},
    {"Nome": "DHÁFINE TAÍS DOMINGUES", "Login": "1128747583sp", "Senha": "Mcc@dt18"},
    {"Nome": "EDUARDO TERZIAN DA MOTA", "Login": "1135641250sp", "Senha": "Mcc@et30"},
    {"Nome": "EDUARDO VIDESCHI FRANCISCO", "Login": "1133664702sp", "Senha": "Mcc@ev03"},
    {"Nome": "ELOÁ MARIA DA SILVA", "Login": "113405838xsp", "Senha": "Mcc@em16"},
    {"Nome": "EMANUELY VITÓRIA CUSTÓDIO", "Login": "1130842708sp", "Senha": "Mcc@ev30"},
    {"Nome": "ENZO RODRIGO DOS SANTOS PINTO", "Login": "1133687647sp", "Senha": "Mcc@er18"},
    {"Nome": "GABRIEL BORGES PRATES", "Login": "1113429380sp", "Senha": "Mcc@gb15"},
    {"Nome": "GABRIELLI GUEDES COLEONI", "Login": "1133703136sp", "Senha": "Mcc@gg15"},
    {"Nome": "GABRIELLY GENNARI CAMPANELLA", "Login": "1123564334sp", "Senha": "Mcc@gg22"},
    {"Nome": "GUSTAVO LEME GORNI", "Login": "1133684427sp", "Senha": "Mcc@gl21"},
    {"Nome": "GUSTAVO TARSITANO LEME", "Login": "1135642382sp", "Senha": "Mcc@gt09"},
    {"Nome": "HELENA PEREIRA DE CAMARGO", "Login": "1133702909sp", "Senha": "Mcc@hp11"},
    {"Nome": "HENRIQUE GABRIEL CAMARGO DA SILVA", "Login": "1108520212sp", "Senha": "Mcc@hg09"},
    {"Nome": "IVAN ALVES DE MELO JUNIOR", "Login": "1145519660sp", "Senha": "Mcc@ia28"},
    {"Nome": "JONATAS PEREIRA DOS SANTOS", "Login": "1131934313sp", "Senha": "Mcc@jp15"},
    {"Nome": "JULIANO DO CARMO MILLER", "Login": "1133663667sp", "Senha": "Mcc@jc07"},
    {"Nome": "KAUAN FERREIRA CORREA", "Login": "1133674720sp", "Senha": "Mcc@kf30"},
    {"Nome": "LAURA PRADO ROSSI", "Login": "1127283935sp", "Senha": "Mcc@lp05"},
    {"Nome": "LUÍS FELIPE ALVES BARBOSA LIMA", "Login": "113366345xsp", "Senha": "Mcc@lf08"},
    {"Nome": "LUÍS OTÁVIO PILOTO DOS REIS", "Login": "113366278xsp", "Senha": "Mcc@lo06"},
    {"Nome": "MANUELE YASMIN LUIZ BENVINDO", "Login": "1126639825sp", "Senha": "Mcc@my23"},
    {"Nome": "MÁRCIO JOSÉ DE OLIVEIRA JÚNIOR", "Login": "1092635130sp", "Senha": "Mcc@mj10"},
    {"Nome": "MARCOS VINÍCIUS COLEONI", "Login": "1133699583sp", "Senha": "Mcc@mv30"},
    {"Nome": "MARIA CECÍLIA DA SILVA COSTA", "Login": "1106358697sp", "Senha": "Mcc@mc29"},
    {"Nome": "MARIA CLARA THEODORO BEDIN", "Login": "1133747991sp", "Senha": "Mcc@mc01"},
    {"Nome": "MARIA JÚLIA DE OLIVEIRA DA SILVA", "Login": "1098433294sp", "Senha": "Mcc@mj16"},
    {"Nome": "RICHARD DO CARMO SANTI", "Login": "1133748387sp", "Senha": "Mcc@rc12"},
    {"Nome": "MATHEUS CASTRO DE ANDRADE", "Login": "1133688810sp", "Senha": "Mcc@ma22"},
    {"Nome": "NATHALLY BLEINAT DA SILVA RODRIGUES", "Login": "1133657187sp", "Senha": "Mcc@nb07"},
    {"Nome": "NICOLAS MAURIELI DOS SANTOS", "Login": "1135071895sp", "Senha": "Mcc@nm19"},
    {"Nome": "PEDRO CAMPREGUER CARDOSO", "Login": "1112312183sp", "Senha": "Mcc@pc21"},
    {"Nome": "PEDRO HENRIQUE CARVALHO DA COSTA", "Login": "111218675xsp", "Senha": "Mcc@ph19"},
    {"Nome": "SAMUEL RODRIGO OFMAN REZENDE", "Login": "1111787049sp", "Senha": "Mcc@sr16"},
    {"Nome": "SOFIA SANTOS DE MELLO", "Login": "1122537359sp", "Senha": "Mcc@ss23"},
    {"Nome": "TIAGO LUIS CIRIACO DA SILVA JUNIOR", "Login": "1143376481sp", "Senha": "Mcc@tl15"},
    {"Nome": "VITÓRIA APARECIDA DA COSTA", "Login": "1133700603sp", "Senha": "Mcc@va19"},
    {"Nome": "VITÓRIA DE SOUZA SYLVESTRIN", "Login": "1134412241sp", "Senha": "Mcc@vs01"},
    {"Nome": "VITÓRIA ISABELA SILVA", "Login": "1101848042sp", "Senha": "Mcc@vi19"},
    {"Nome": "WENDER AUGUSTO DA SILVA", "Login": "1122763426sp", "Senha": "Mcc@wa24"},
    {"Nome": "ANNA JULLYA COSTA DE SÁ", "Login": "1100174436sp", "Senha": "Mcc@aj08"},
    {"Nome": "YASMIN DA SILVA ALEXANDRE", "Login": "1107046658sp", "Senha": "Mcc@ya24"},
    {"Nome": "LUIZ GUSTAVO FRANCISCHINI PINHEIRO", "Login": "111505563xsp", "Senha": "Mcc@lg08"},
    {"Nome": "JOÃO PEDRO BARCELLOS", "Login": "1126596218sp", "Senha": "Mcc@jp06"}
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

    total = 0
    success = 0
    failure = 0

    try:
        for student in STUDENTS_DATA:
            total += 1
            login = student["Login"]
            password = student["Senha"]
            print(f"\n➡️ Processando {login} ({total})...")
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