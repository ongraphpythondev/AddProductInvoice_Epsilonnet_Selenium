import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class Product:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def login(self):
        """This Method is for login on the website"""
        self.driver.get("https://myaccount.epsilonnet.gr/identity/account/login")
        self.driver.find_element(by=By.NAME, value="Input.Email").send_keys(
            self.username
        )
        self.driver.find_element(by=By.NAME, value="Input.Password").send_keys(
            self.password
        )
        self.driver.find_element(by=By.TAG_NAME, value="form").submit()

    def clickcancelbutton(self, locatorname):
        """This Method is for close popup

        Args:
            locatorname (str): it takes the locator name
        """
        CancelClientButton = self.driver.find_elements(By.CLASS_NAME, locatorname)[-1]
        CancelClientButton.click()
        time.sleep(2)

    def addProduct(self, parameter, name):
        """This Method is to add product in the invoice

        Args:
            onoma (_type_): _description_
            kwdikos (_type_): _description_


        """
        kwdikos = parameter.get("ScanCode")

        # ItemPrintDescr, ScanCode
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, "mastersMenuItem"))
        ).click()
        time.sleep(6)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, "itemsMenuItem"))
        ).click()
        time.sleep(6)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, "CreateNew"))
        ).click()

        self.driver.find_element(
            by=By.CSS_SELECTOR, value="label[for=Name] ~ input"
        ).send_keys(name)
        time.sleep(1)
        self.driver.find_element(by=By.CSS_SELECTOR, value=".k-last").click()
        time.sleep(1)
        self.driver.find_element(
            by=By.CSS_SELECTOR, value="label[for=UserDefText01] ~ input"
        ).send_keys(kwdikos)
        time.sleep(2)
        self.driver.find_element(
            by=By.CSS_SELECTOR, value=".k-tabstrip-items li ~ li"
        ).click()
        self.driver.find_element(
            by=By.CSS_SELECTOR, value="label[for=VTScanCode] ~ input"
        ).send_keys(kwdikos)
        time.sleep(1)
        self.driver.find_element(by=By.ID, value="SaveAndNew").click()

        print(
            f"product {name} has been added successfully.now it will add in the invoice!"
        )

    def getalloption(self):
        WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/span/button",
                )
            )
        ).click()

        time.sleep(4)

        options_list = self.driver.find_element(By.CLASS_NAME, "k-list-ul")
        options = options_list.find_elements(By.CLASS_NAME, "k-list-item")

        return options

    def previousitem(self):
        WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[1]/ul/li[1]",
                )
            )
        ).click()
        time.sleep(2)

    def selectchoicevat(self, value):
        WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[1]/ul/li[2]",
                )
            )
        ).click()
        if value:
            options = self.getalloption()
            action = ActionChains(self.driver)
            option_found = False
            for option in options:
                option_text = option.find_element(
                    By.CLASS_NAME, "k-list-item-text"
                ).text.strip()
                print(option_text, 22222222)
                if option_text == value.strip():
                    print(option_text, "condition meet 33333333333")
                    action.click(on_element=option)
                    action.perform()
                    option_found = True
                    time.sleep(3)

                    break
            if not option_found:
                options[-1].click()
            self.previousitem()

        else:
            options = self.getalloption()
            options[-1].click()
            self.previousitem()
            
            
    def set_hmerominia(self, hmerominia, i=1):
        try:
            print('\nset_hmerominia....')
            time.sleep(5)
            d = hmerominia.split('/')
            # date = d[2] + '/' + d[1] + '/' + d[0]
            time.sleep(1)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(
            d[0]
            )
            time.sleep(1)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(Keys.LEFT)
            time.sleep(1)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(
            d[1]
            )
            time.sleep(1)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(Keys.LEFT)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(Keys.LEFT)
            time.sleep(2)
            self.driver.find_element(by=By.CSS_SELECTOR, value="label[for=Date] ~ span input").send_keys(
            d[2]
            )
            m = 'Hmerominia has been added successfully to invoice (method: set_hmerominia)'
            return True, m
        except Exception as e:
            # traceback.print_exc()
            m = 'Date has been failed to be added to invoice (method: set_hmerominia)'
            return False, m
    

    def additems(self, itemslist):
        """This Method is for to add the items in the invoice

        Args:
            items (dict): Its take dict
        """
        items = itemslist["items"]
        parameters = itemslist.get("parameter")

        new_items = list()
        transactions_menu_found = True

        if items:
            for item in range(len(items)):
                time.sleep(2)
                if transactions_menu_found:
                    WebDriverWait(self.driver, 200).until(
                        EC.presence_of_element_located((By.ID, "transactionsMenuItem"))
                    ).click()
                    time.sleep(5)
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.ID, "salesEntriesMenuItem"))
                    ).click()
                    time.sleep(5)

                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.ID, "CreateNew"))
                    ).click()
                time.sleep(3)
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[2]/div/div[1]/button[2]",
                        )
                    )
                ).click()

                InputBox_ = WebDriverWait(self.driver, 80).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/span/input",
                        )
                    )
                )
                InputBox_.send_keys(items[item])
                time.sleep(2)

                InputBox_.send_keys(Keys.RETURN)
                time.sleep(2)

                TableBody = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/table/tbody",
                )
                try:
                    AllRows = TableBody.find_elements(By.TAG_NAME, "tr")
                    for row in AllRows:
                        columns = row.find_elements(By.TAG_NAME, "td")

                        ItemName = columns[2].text
                        # action = ActionChains(self.driver)
                        if items[item].strip() == ItemName.strip():
                            new_items.append(items[item])
                            transactions_menu_found = False
                            self.clickcancelbutton("pull-right")
                            time.sleep(2)
                            break
                        else:
                            raise Exception
                except Exception as e:
                    print(f"Item: {items[item]} Records does not exist.. ")
                    self.clickcancelbutton("pull-right")
                    new_items.append(items[item])
                    transactions_menu_found = True
                    self.addProduct(parameters[item], items[item])

            datetime = True
            choice = True
            for val in range(len(new_items)):
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.ID, "salesEntriesMenuItem")
                        )
                    )
                    el = element.text
                except Exception:
                    self.driver.find_element(By.ID, "transactionsMenuItem").click()
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.ID, "salesEntriesMenuItem"))
                    ).click()
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.ID, "CreateNew"))
                    ).click()

                if choice:
                    vatvalue = itemslist.get("VATStatus")
                    self.selectchoicevat(value=vatvalue)
                    choice = False
                if datetime:
                    print("dateeeee")
                    date = itemslist.get("date")
                    
                    self.set_hmerominia(hmerominia=date)
                    datetime = False

                WebDriverWait(self.driver, 120).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[2]/div/div[1]/button[2]",
                        )
                    )
                ).click()

                InputBox__ = WebDriverWait(self.driver, 80).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/span/input",
                        )
                    )
                )
                InputBox__.send_keys(new_items[val])
                time.sleep(4)

                InputBox__.send_keys(Keys.RETURN)
                time.sleep(3)

                TableBody_ = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/table/tbody",
                )
                action_ = ActionChains(self.driver)

                try:
                    AllRows_ = TableBody_.find_elements(By.TAG_NAME, "tr")
                    for row_ in AllRows_:
                        columns_ = row_.find_elements(By.TAG_NAME, "td")

                        ItemName_ = columns_[2].text
                        if new_items[val].strip() == ItemName_.strip():
                            print(f"Item {new_items[val].strip()} exist and added...")
                            action_.double_click(on_element=row_)
                            action_.perform()
                            self.clickcancelbutton("pull-right")
                            break

                except Exception as e:
                    pass

                GridContent = WebDriverWait(self.driver, 40).until(
                    EC.presence_of_element_located((By.TAG_NAME, "tbody"))
                )

                ContentRows = GridContent.find_elements(By.TAG_NAME, "tr")
                if ContentRows:
                    last_row = ContentRows[-1]

                    GridContentCol = last_row.find_elements(By.TAG_NAME, "td")
                    time.sleep(2)
                    if len(GridContentCol) >= 3:
                        GridContentCol[4].click()
                        time.sleep(3)
                        QtyInputEelement = self.driver.find_element(
                            By.XPATH,
                            "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td[5]/span/span/input",
                        )
                        Qty = parameters[val].get("Qty")

                        self.driver.execute_script(
                            "arguments[0].focus();", QtyInputEelement
                        )
                        self.driver.execute_script(
                            "arguments[0].value = arguments[1];", QtyInputEelement, Qty
                        )
                        self.driver.execute_script(
                            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                            QtyInputEelement,
                        )

                        QtyInputEelement.send_keys(Keys.ENTER)
                        GridContent_ = WebDriverWait(self.driver, 40).until(
                            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
                        )

                    ContentRows_ = GridContent_.find_elements(By.TAG_NAME, "tr")
                    if ContentRows_:
                        last_row_ = ContentRows_[-1]

                        GridContentCol_ = last_row_.find_elements(By.TAG_NAME, "td")

                    if len(GridContentCol_) >= 7:
                        time.sleep(3)
                        GridContentCol_[6].click()
                        time.sleep(3)
                        PriceInputEelement = self.driver.find_element(
                            By.XPATH,
                            "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td[7]/span/span/input",
                        )
                        Price = parameters[val].get("Price")

                        self.driver.execute_script(
                            "arguments[0].focus();", PriceInputEelement
                        )
                        self.driver.execute_script(
                            "arguments[0].value = arguments[1];",
                            PriceInputEelement,
                            Price,
                        )
                        self.driver.execute_script(
                            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                            PriceInputEelement,
                        )
                        PriceInputEelement.send_keys(Keys.ENTER)

                time.sleep(5)
            #document number
            WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[1]/div[4]/div/span/span/span/button[1]",
                    )
                )
            ).click()
          
        else:
            print("please provide the items.")

    def addclient(self, client):
        """This Method is to add the client

        Args:
            client (str): it's a string value
        """
        if client:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div/button",
                    )
                )
            ).click()
            time.sleep(3)
            InputBox = WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/span/input",
                    )
                )
            )
            InputBox.send_keys(client)
            time.sleep(3)
            InputBox.send_keys(Keys.RETURN)
            time.sleep(5)
            TableBody = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/table/tbody",
            )
            try:
                AllRows = TableBody.find_elements(By.TAG_NAME, "tr")
                for row in AllRows:
                    columns = row.find_elements(By.TAG_NAME, "td")

                    ItemName = columns[2].text
                    action = ActionChains(self.driver)
                    if client.strip() == ItemName.strip():
                        print(f"Client {client.strip()} exist and has been added...")
                        action.double_click(on_element=row)
                        action.perform()
                        break
                time.sleep(4)
                
                #create invoice
                WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[1]/div[2]/div/div/button[3]",
                    )
                )
            ).click()
            except:
                print(f"{client} client does not exists.......")
                self.clickcancelbutton("pull-right")

        else:
            print("please provide the Cusomer.")

    def close_browser(self):
        """This Method is to close the browser"""
        self.driver.quit()


ListOfitems = {
    "items": ["test002", "SAAFCARB 25 KG/BAG"],
    "date": "06/10/2023",
    # "VATStatus":"Μειω",
    "parameter": [
        {
            "ScanCode": "tes002",
            "ItemPrintDescr": "AMERKLEEN M80 PAD 24X24X4 MM",
            "VATPercent": 0.0,
            "Qty": 260.0,
            "Price": 4.5,
            "IsGift": 0,
            "NetVal": 1170.0,
        },
        {
            "ScanCode": "2161400065",
            "ItemPrintDescr": 'DURACEL XL-90D 24"X24"X12"',
            "VATPercent": 0.0,
            "Qty": 250.0,
            "Price": 140.0,
            "IsGift": 0,
            "NetVal": 35000.0,
        },
    ],
}

Username = "kostas.david@aaf.gr"
Password = "YHfAt3misKtBh25"
VatNumber = "094262988"

p = Product(Username, Password)
p.login()
time.sleep(10)
p.additems(ListOfitems)
time.sleep(3)
p.addclient(VatNumber)
time.sleep(8)
p.close_browser()
