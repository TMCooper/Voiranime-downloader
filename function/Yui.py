import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class Yui:

    @staticmethod
    def requesting_anime(original_url):

        # Début de l'exécution
        print(f"[DEBUG] Démarrage du navigateur pour l'URL : {original_url}")

        # Configuration de Chrome et démarrage du navigateur
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans interface (peut être retiré si besoin de voir l'interface)        
        service = Service("function\chromedriver-win64\chromedriver.exe")  # Remplace par le chemin vers ton chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Ouvre la page cible
        print(f"[DEBUG] Chargement de la page : {original_url}")
        driver.get(original_url)

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

        # Cliquer au centre du reCAPTCHA et recapturer la position pour cliquer à nouveau
        try:
            print("[DEBUG] Tentative de clic sur le reCAPTCHA.")
            captcha = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")
            
            # Récupère les coordonnées de l'élément
            location = captcha.location
            size = captcha.size

            # Calcule les coordonnées du centre
            center_x = location['x'] + size['width'] / 2
            center_y = location['y'] + size['height'] / 2

            # Crée une action pour cliquer à ces coordonnées
            actions = ActionChains(driver)
            actions.move_by_offset(center_x, center_y).click().perform()
            print(f"[DEBUG] Premier clic au centre du reCAPTCHA aux coordonnées : ({center_x}, {center_y})")

            # Attendre 2 secondes
            time.sleep(2)

            # Refaire le même clic au même endroit
            actions.move_by_offset(-center_x, -center_y)  # Remet la souris à l'origine avant de recliquer
            actions.move_by_offset(center_x, center_y).click().perform()
            print(f"[DEBUG] Deuxième clic au même endroit après 2 secondes.")

        except NoSuchElementException:
            print("[DEBUG] reCAPTCHA non trouvé, tentative ignorée.")

        # Attendre 1 seconde
        time.sleep(1)

        # Cliquer sur le bouton avec la classe "btn"
        try:
            print("[DEBUG] Tentative de clic sur le bouton avec la classe 'btn'.")
            button = driver.find_element(By.CLASS_NAME, "btn")
            button.click()
            print("[DEBUG] Bouton cliqué.")
        except NoSuchElementException:
            print("[DEBUG] Bouton 'btn' non trouvé, tentative ignorée.")

        # Attendre 1 seconde
        time.sleep(1)

        # Chercher le <div> avec la classe spécifique
        try:
            print("[DEBUG] Recherche du <div> avec la classe spécifique.")
            div = driver.find_element(By.CSS_SELECTOR, 'div.psvg9akfoyq[style*="background-image"]')
            print("[DEBUG] Le <div> avec l'image de fond a été trouvé.")
        except NoSuchElementException:
            print("[DEBUG] Le <div> avec l'image de fond n'a pas été trouvé.")

        # Afficher le lien m3u8 si trouvé
        if m3u8_link:
            print(f"[DEBUG] Lien .m3u8 récupéré : {m3u8_link}")
        else:
            print("[DEBUG] Aucun lien .m3u8 n'a été récupéré.")

        # Ferme le navigateur
        print("[DEBUG] Fermeture du navigateur.")
        driver.quit()
