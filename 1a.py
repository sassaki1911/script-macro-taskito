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
    {"Nome": "ANA CLARA NUNES GATINI", "Login": "110443g", "Senha": "Aluno@2910"},
    {"Nome": "ALYSSOM COSTA BARBOSA", "Login": "110574b", "Senha": "Aluno@1706"},
    {"Nome": "ANA CLARA JUDITE ALVES SILVA", "Login": "111710s", "Senha": "Aluno@2506"},
    {"Nome": "ANA KLARA OLIVEIRA", "Login": "112669o", "Senha": "Aluno@3004"},
    {"Nome": "ANNA JULLYA COSTA DE SÁ", "Login": "110017s", "Senha": "Aluno@0807"},
    {"Nome": "BARBARA MILLER RAMOS", "Login": "112188r", "Senha": "Aluno@0802"},
    {"Nome": "BRYAN ALVES", "Login": "110184a", "Senha": "Aluno@0607"},
    {"Nome": "DANIELA NOBERTO DE LIMA", "Login": "111608l", "Senha": "Aluno@2209"},
    {"Nome": "DENILSON MARINI FEDOSSI", "Login": "110761f", "Senha": "Aluno@1911"},
    {"Nome": "DOUGLAS WALLYSON VINICIUS MENEZES MASSOLA", "Login": "109684m", "Senha": "Aluno@2402"},
    {"Nome": "ENZO RODRIGO DOS SANTOS PINTO", "Login": "113368p", "Senha": "Aluno@1809"},
    {"Nome": "FLÁVIA EDUARDA MACHADO", "Login": "112768m", "Senha": "Aluno@1512"},
    {"Nome": "GABRIEL LIMA GONÇALVES", "Login": "111608g", "Senha": "Aluno@3007"},
    {"Nome": "GUSTAVO TEIXEIRA AMÉNDOLA", "Login": "113368a", "Senha": "Aluno@0305"},
    {"Nome": "HELENA DOS SANTOS COLEONI", "Login": "113367c", "Senha": "Aluno@0203"},
    {"Nome": "HELOÃ YSABELLE DIAS", "Login": "113366d", "Senha": "Aluno@0906"},
    {"Nome": "HOMERO DE MELLO ALVES", "Login": "111142a", "Senha": "Aluno@2303"},
    {"Nome": "JOANA DE LUCAS PEIXE BARBOSA ALVES", "Login": "112668a", "Senha": "Aluno@0810"},
    {"Nome": "JOÃO LUCAS SOARES CARDOSO", "Login": "113374c", "Senha": "Aluno@0605"},
    {"Nome": "JOÃO PAULO DOS SANTOS MARTINS", "Login": "113374m", "Senha": "Aluno@2912"},
    {"Nome": "JOÃO PEDRO BARCELLOS", "Login": "112659b", "Senha": "Aluno@0604"},
    {"Nome": "JOÃO VITOR DOS REIS", "Login": "110898r", "Senha": "Aluno@2606"},
    {"Nome": "JONATAS PEREIRA DOS SANTOS", "Login": "113193s", "Senha": "Aluno@1503"},
    {"Nome": "JÚLIA CALIXTO", "Login": "113370c", "Senha": "Aluno@1512"},
    {"Nome": "JÚLIA COMPARETTO ALVES", "Login": "109843a", "Senha": "Aluno@1007"},
    {"Nome": "KAUÊ EDUARDO PREVIATO DE ALMEIDA", "Login": "110273a", "Senha": "Aluno@2508"},
    {"Nome": "LUIGI GABRIEL ORLANDO CARDOSO", "Login": "111178c", "Senha": "Aluno@1806"},
    {"Nome": "LURIANY CASTILHO GODOY", "Login": "113370g", "Senha": "Aluno@2412"},
    {"Nome": "MANASSÉS GONÇALVES ANTONIO", "Login": "110462a", "Senha": "Aluno@1304"},
    {"Nome": "MAYTÉ FRANCISCO DAS CHAGAS", "Login": "109649c", "Senha": "Aluno@2607"},
    {"Nome": "MARYANE VICTÓRIA VIEIRA", "Login": "113374v", "Senha": "Aluno@0303"},
    {"Nome": "ANA CECÍLIA SAMPIETRO DA SILVA", "Login": "109896s", "Senha": "Aluno@0208"},
    {"Nome": "MIGUEL DE SOUZA CAMPREGHER", "Login": "113367c", "Senha": "Aluno@2903"},
    {"Nome": "MIGUEL LEITE PEREIRA", "Login": "111628p", "Senha": "Aluno@0205"},
    {"Nome": "NATACHA FAUSTINO DIAS MAZOCHO", "Login": "114616m", "Senha": "Aluno@2106"},
    {"Nome": "RICARDO FERNANDES SOUSA", "Login": "110898s", "Senha": "Aluno@3108"},
    {"Nome": "RICHARD DO CARMO SANTI", "Login": "113374s", "Senha": "Aluno@1211"},
    {"Nome": "THALYA GABRIELA GOMES FRANCISCO", "Login": "109561f", "Senha": "Aluno@1607"},
    {"Nome": "THAMILLY VICTÓRIA DUARTE DE AMORIM", "Login": "110867a", "Senha": "Aluno@1601"},
    {"Nome": "VIKTOR GABRIEL EVANGELISTA VIEIRA", "Login": "111575v", "Senha": "Aluno@1107"},
    {"Nome": "VINICIUS LUIZ OLIVEIRA DE ALMEIDA", "Login": "113367a", "Senha": "Aluno@0604"},
    {"Nome": "VINICIUS ROBERTO RODRIGUES AMBROZIO", "Login": "112070a", "Senha": "Aluno@1505"},
    {"Nome": "YASMIN DA SILVA ALEXANDRE", "Login": "110704a", "Senha": "Aluno@2411"},
    {"Nome": "VITÓRIA APARECIDA DA COSTA", "Login": "113370c", "Senha": "Aluno@1908"},
    {"Nome": "JULIANO DO CARMO MILLER", "Login": "113366m", "Senha": "Aluno@0707"},
    {"Nome": "KAIO HENRICK NALIN RAMOS", "Login": "110635r", "Senha": "Aluno@1003"}
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