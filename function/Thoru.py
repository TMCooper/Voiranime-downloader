import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

chrome_driver_path = '/chemin/vers/le/chromedriver'  # Remplace par le chemin vers ton ChromeDriver
chrome_path = r'function\chrome-win64\chrome.exe'  # Chemin vers ton Chrome personnalisé

class Thoru():
    def captcha(original_url):

        # Début de l'exécution
        print(f"[DEBUG] Démarrage du navigateur pour l'URL : {original_url}")

        # Configuration de Chrome et démarrage du navigateur
        chrome_options = Options()
        chrome_options.binary_location = chrome_path  # Spécifie le chemin de l'ancienne version de Chrome
        chrome_options.add_argument("--no-sandbox")  # Désactiver la sandbox
        chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
        chrome_options.add_argument("--disable-webgl")  # Désactiver WebGL pour éviter les erreurs liées à WebGL
        chrome_options.add_argument("--enable-unsafe-swiftshader")  # Activer SwiftShader pour un fallback en mode logiciel si nécessaire
        chrome_options.add_argument("--start-maximized")  # Maximiser la fenêtre
        # chrome_options.add_argument("--headless")  # Mode sans interface (peut être retiré si besoin de voir l'interface)        
        service = Service("function\chromedriver-win64\chromedriver.exe")  # Remplace par le chemin vers ton chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Ouvre la page cible
        print(f"[DEBUG] Chargement de la page : {original_url}")
        driver.get(original_url)

        click_elements(driver)
        # video_automation = VideoAutomation(driver)
        # video_automation.run(original_url)

        # Fonction pour capturer les requêtes réseau en continu
        def capture_network_requests():
            print("[DEBUG] Capture des requêtes réseau...")
            script = """
            function captureRequests() {
                const performanceEntries = performance.getEntriesByType('resource');
                const networkRequests = performanceEntries.filter(entry =>
                    entry.name.includes('.m3u8')
                );
                return networkRequests.map(request => request.name);
            }
            return captureRequests();
            """
            return driver.execute_script(script)

        # Boucle pour surveiller les requêtes réseau
        m3u8_link = None
        print("[DEBUG] Début de la surveillance des requêtes réseau.")
        while not m3u8_link:
            network_requests = capture_network_requests()
            if network_requests:
                for request in network_requests:
                    print(f"[DEBUG] Requête .m3u8 trouvée : {request}")
                    m3u8_link = request
                    break
            else:
                print("[DEBUG] Aucune requête .m3u8 trouvée, nouvelle vérification dans 1 seconde.")
            time.sleep(1)  # On attend 1 seconde avant de vérifier de nouveau

        # Afficher le lien m3u8 si trouvé
        if m3u8_link:
            print(f"[DEBUG] Lien .m3u8 récupéré : {m3u8_link}")
        else:
            print("[DEBUG] Aucun lien .m3u8 n'a été récupéré.")

        # Ferme le navigateur
        print("[DEBUG] Fermeture du navigateur.")
        driver.quit()


def click_elements(driver):
    try:
        print("[DEBUG] Tentative de trouver le captcha...")
        # Passer à l'iframe contenant le reCAPTCHA
        iframe = driver.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]")
        driver.switch_to.frame(iframe)

        # Ensuite, essayer de cliquer sur le reCAPTCHA
        checkbox = driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
        checkbox.click()
        print("[DEBUG] Checkbox reCAPTCHA cliquée avec succès.")

        # Revenir au contexte principal de la page
        driver.switch_to.default_content()

        time.sleep(0.5)
        print("[DEBUG] Tentative de trouver et de cliquer sur le bouton 'btn'...")
        button = driver.find_element(By.CLASS_NAME, 'btn')
        button.click()
        print("[DEBUG] Le bouton 'btn' a été cliqué avec succès.")
        return True

    except NoSuchElementException as e:
        print(f"[DEBUG] Erreur : Un des éléments n'a pas été trouvé - {e}.")
        return False

    except ElementClickInterceptedException as e:
        print("[DEBUG] Erreur : Un des éléments n'a pas pu être cliqué (intercepté par un autre élément).")
        return False

class VideoAutomation():
    def __init__(self, driver):
        self.driver = driver
        self.keep_running = True

    def remove_popups(self):
        main_window = self.driver.current_window_handle
        time.sleep(1)  # Pause pour laisser le temps aux onglets de se charger

        # Vérifier si des onglets supplémentaires sont ouverts
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            for window in all_windows:
                if window != main_window:
                    # Passer à l'onglet popup et le fermer
                    self.driver.switch_to.window(window)
                    time.sleep(1)  # Pause pour laisser le temps à l'onglet de se charger
                    self.driver.close()
                    print(f"[DEBUG] Onglet popup fermé: {window}")

            # Revenir à l'onglet principal
            self.driver.switch_to.window(main_window)
            time.sleep(2)  # Pause après retour à l'onglet principal

        # Vérifier les pop-ups sur la page principale
        try:
            # Attendre que le pop-up apparaisse (ajuster le SELECTEUR selon la structure HTML)
            popup_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'popup')]"))  # Remplacez avec la classe ou l'ID corrects
            )
            if popup_element:
                popup_element.click()  # Cliquez pour fermer le pop-up si possible
                print("[DEBUG] Pop-up détecté et fermé.")
        except TimeoutException:
            print("[DEBUG] Aucun pop-up détecté sur la page principale.")
        
    def check_and_close_fraudulent_tab(self):
        main_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles

        for window in all_windows:
            if window != main_window:
                self.driver.switch_to.window(window)
                time.sleep(1)  # Attendre que la page se charge

                current_url = self.driver.current_url
                print(f"[DEBUG] Onglet détecté avec l'URL : {current_url}")

                # Vérifier si l'URL de l'onglet est frauduleux
                if "diessity.com" in current_url or "click.php" in current_url:
                    print("[DEBUG] Onglet frauduleux détecté.")
                    self.driver.close()  # Fermer l'onglet frauduleux
                    print("[DEBUG] Onglet frauduleux fermé.")
                    self.driver.switch_to.window(main_window)
                    return True

        # Revenir à l'onglet principal
        self.driver.switch_to.window(main_window)
        print("[DEBUG] Aucun onglet frauduleux détecté.")
        return False
    
    def monitor_popups_and_tabs(self):
        while self.keep_running:  # Continue tant que keep_running est True
            self.remove_popups()  # Vérifie les popups
            self.check_and_close_fraudulent_tab()  # Vérifie les onglets frauduleux
            time.sleep(1)  # Attendre 1 seconde avant de vérifier à nouveau

    def start_monitoring(self):
        # Démarre le monitoring dans un nouveau thread
        monitoring_thread = threading.Thread(target=self.monitor_popups_and_tabs)
        monitoring_thread.daemon = True  # Finit le thread quand le programme principal se termine
        monitoring_thread.start()

    def click_video_player(self, btn_location):
        try:
            video_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'jw-icon-display'))
            )
            video_button.click()
            print("[DEBUG] Le lecteur vidéo a été cliqué avec succès.")
            return True

        except (NoSuchElementException, TimeoutException):
            print("[DEBUG] Le lecteur vidéo avec la classe 'jw-icon-display' n'a pas été trouvé.")
            if btn_location:
                ActionChains(self.driver).move_by_offset(btn_location['x'], btn_location['y']).click().perform()
                print(f"[DEBUG] Clic effectué à la position ({btn_location['x']}, {btn_location['y']}) du bouton 'btn'.")
                return True
            return False
        
    def run(self, original_url):
        while True:  # Boucle continue jusqu'à ce que l'on sorte
            print(f"[DEBUG] Chargement de la page : {original_url}")
            self.driver.get(original_url)
            time.sleep(2)  # Pause après le chargement de la page

            self.start_monitoring()
            # 1. Supprimer les popups s'ils existent
            self.remove_popups()
            self.monitor_popups_and_tabs()
            self.click_video_player()



    def stop_monitoring(self):
        self.keep_running = False  # Arrête le monitoring