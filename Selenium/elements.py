import os
import pickle
import random
from traceback import print_stack
from prettytable import PrettyTable
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Selenium.driversSet import Selenium
from time import sleep

class Elements(Selenium):
    def __init__(self, **kwargs):
        self.pT = PrettyTable()
        super().__init__(**kwargs)

    def getByType(self, locaTy):
        locaTy = locaTy.lower()
        if locaTy == "id":
            return By.ID
        elif locaTy == "name":
            return By.NAME
        elif locaTy == "tag":
            return By.TAG_NAME
        elif locaTy == "xpath":
            return By.XPATH
        elif locaTy == "css":
            return By.CSS_SELECTOR
        elif locaTy == "class":
            return By.CLASS_NAME
        elif locaTy == "link":
            return By.LINK_TEXT
        else:
            self.log(f"Locator type {locaTy} incorrect! Choose between id, name, xpath, css, name, class or link")
            print_stack()

    def waitElementType(self, ECType="present"):
        ECType = ECType.lower()
        if ECType == "click":
            return EC.element_to_be_clickable
        elif ECType == "visible":
            return EC.visibility_of_element_located
        elif ECType == "present":
            return EC.presence_of_element_located
        elif ECType == "frame":
            return EC.frame_to_be_available_and_switch_to_it
        else:
            self.log(f"EC type {ECType} incorrect! Choose between clickable, frame, present or visible")
            print_stack()

    def getEle(self, element, eleName, click=False, getText=False, keys=None, keysSlow=True, clear=False,
               getAttribute=None, kD1=0.05, kD2=0.1, ECType="present", wait=True, timeout=5, eleOnly=None):
        # element = self.ele(locaTy=locaTy, loca=loca, eleName=eleName, ECType=ECType, wait=wait, timeout=timeout)
        if clear:
            try:
                element.clear()
                self.log(f"Cleared '{eleName}' field box!")
            except:
                self.debug(f"Could not clear '{eleName}' field box")
                print_stack()
        if click:
            try:
                element.click()
                self.log(f"Clicked on '{eleName}'!")
            except:
                self.debug(f"Could not click on '{eleName}'")
                print_stack()
        if getText:
            try:
                self.log(f"Returning '{eleName}' text which happens to be '{element.text}'")
                return element.text
            except:
                self.debug(f"Could not return '{eleName}' text")
                print_stack()
        if keys is not None and keysSlow is False:
            try:
                element.send_keys(keys)
                self.log(f"Typed in {keys} in '{eleName}' with no delay!")
            except:
                self.debug(f"Could not type in {keys} in '{eleName}' with no delay")
                print_stack()
        if keys is not None and keysSlow:
            try:
                for x in keys:
                    element.send_keys(x)
                    sleep(random.uniform(kD1, kD2))
                self.log(f"Typed in {keys} in '{eleName}' with delay!")
            except:
                self.debug(f"Could not type in {keys} in '{eleName}' with delay")
                print_stack()
        if getAttribute is not None:
            try:
                self.log(
                    f"Returning '{eleName}' attribute '{getAttribute}' which happens to be '{element.get_attribute(getAttribute)}'")
                return element.get_attribute(getAttribute)
            except:
                self.debug(
                    f"Could not return '{eleName}' attribute '{getAttribute}'")
        if eleOnly:
            try:
                self.log(f"Returning element '{eleName}' which happens to be '{element}'!")
                return element
            except:
                self.debug(f"Could not return element '{eleName}'")
                print_stack()

    def ele(self, loca, locaTy="xpath", ECType="present", wait=True, timeout=5, keysSlow=True, keys=None,
            kD1=0.05, kD2=0.09, getText=False, getTextP=False, getAttr=False, getAttrP=False, Attr=None):
        getByType = self.getByType(locaTy)
        waitElementType = self.waitElementType(ECType)
        waitDriver = WebDriverWait(self, timeout=timeout)
        if wait is False:
            element = self.find_element(getByType, loca)
            self.log(f"Element with type '{locaTy}' and loca '{loca}' found with no wait!")
            if keys is not None and keysSlow is False:
                element.send_keys(keys)
                self.log(f"Typed in {keys} with no delay!")
            if keys is not None and keysSlow:
                for x in keys:
                    element.send_keys(x)
                    sleep(random.uniform(kD1, kD2))
                self.log(f"Typed in {keys} with delay!")
            if getText:
                self.log(f"Returning '{loca}' text '{element.text}'")
                return element.text
            if getTextP:
                self.log(f"Returning '{loca}' text '{element.text}'")
                print(element.text)
            if getAttr:
                return element.get_attribute(Attr)
            if getAttr and Attr is None:
                raise ValueError(Attr, "cannot be none")
            if getAttrP:
                print(element.get_attribute(Attr))
            if getAttrP and Attr is None:
                raise ValueError(Attr, "cannot be none")
            return element
        if wait:
            element = waitDriver.until(waitElementType((getByType, loca)))
            self.log(f"Element with type '{locaTy}' and loca '{loca}' found with {timeout} seconds wait!")
            if keys is not None and keysSlow is False:
                element.send_keys(keys)
                self.log(f"Typed in {keys} with no delay!")
            if keys is not None and keysSlow:
                for x in keys:
                    element.send_keys(x)
                    sleep(random.uniform(kD1, kD2))
                self.log(f"Typed in {keys} with delay!")
            if getText:
                self.log(f"Returning '{loca}' text '{element.text}'")
                return element.text
            if getTextP:
                self.log(f"Returning '{loca}' text '{element.text}'")
                print(element.text)
            if getAttr:
                return element.get_attribute(Attr)
            if getAttr and Attr is None:
                raise ValueError(Attr, "cannot be none")
            if getAttrP:
                print(element.get_attribute(Attr))
            if getAttrP and Attr is None:
                raise ValueError(Attr, "cannot be none")
            return element

    def eleLoop(self, element, equal='', delay=0.5):
        while element.text == equal:
            element.text
            self.debug("Text not found, looking again after 0.5s..")
            sleep(delay)
        self.log("Text found..")
        return element

    def urlChange(self, url, timeout=5):
        try:
            WebDriverWait(self, timeout).until(EC.url_changes(url))
        except Exception as e:
            print(f"Url did not change even after waiting for {timeout} seconds. {str(e)}")

    def sleep(self, t1=0.3, t2=0.8):
        sleep(random.uniform(t1, t2))
        self.log(f"Sleeping for {t1 + t2} seconds")

    def switchDC(self):
        self.switch_to.default_content()
        self.log(f"Switching to default content")

    def tabForthBack(self):
        ActionChains(self).send_keys(Keys.TAB).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(
            Keys.SHIFT).perform()
        self.log(f"Tabbing forth and back...")

    def loadCookies(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.add_cookie(cookie)
            print('Cookies loaded!')
        except InvalidCookieDomainException:
            print('Could not load cookies!')

    def saveCookies(self):
        pickle.dump(self.get_cookies(), open("cookies.pkl", "wb"))
        print('Cookies saved for next time!')

    def maximize(self):
        self.switch_to.window(self.window_handles[-1])

    def urlChange(self, url, timeout=5):
        try:
            WebDriverWait(self, timeout).until(EC.url_changes(url))
            self.log("URL changed!")
        except:
            self.log("URL did not change")
            print_stack()

    def newest(self, path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files if basename.endswith('.py')]
        return max(paths, key=os.path.getctime)

    def filesEndingInPyOnly(self, path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files if basename.endswith('.py')]
        return paths

    def orderInfo(self, path, alwaysLatest=False):
        global orderInfo
        try:
            if alwaysLatest:
                orderInfo = self.newest(path)
            else:
                print(f"Latest order info found: {self.newest(path)}")
                whatUse = int(input(f"Click 1 to use latest or 2 to use another: "))
                if whatUse == 1:
                    orderInfo = self.newest(path)
                elif whatUse == 2:
                    for index, eachOrderInfo in enumerate(self.filesEndingInPyOnly(path)):
                        print(index, eachOrderInfo)
                    orderInfoOption = int(input("Select one: "))
                    orderInfo = (self.filesEndingInPyOnly(path)[orderInfoOption])
                print(f"Using {orderInfo}")
        except FileNotFoundError:
            print("No order infos found, run ebay bot to create one")
        return orderInfo.replace("/", ".").replace(".py", "")

    def eleLoopIndex(self, loca, locaTy="xpath", ECType="present", getText=False,
                     getTextP=False, index=1, timeout=5, printTotal=False, returnTotal=False, list=None, getAttr=False, getAttrP=False, Attr=None):
        while True:
            try:
                x = self.ele(f"({loca})[{index}]", locaTy=locaTy, timeout=timeout,
                         getText=getText, getTextP=getTextP, ECType=ECType, getAttr=getAttr, getAttrP=getAttrP, Attr=Attr)
                if list is not None:
                    list.append(x)
                index += 1
                timeout = 0
                continue
            except TimeoutException:
                index -= 1
                break
        if printTotal:
            print(f"Total elements found: {index}")
        if returnTotal:
            return index

    def eleInLinkLoop(self, loca, *args, linkEnd=None, printTotal=False, timeout=2):
        index = 1
        links = []
        for x in args:
            while True:
                try:
                    newLink = f"{x}{linkEnd}{index}"
                    print(newLink)
                    self.get(newLink)
                    self.ele(loca, timeout=timeout)
                    links.append(newLink)
                    index += 1
                    continue
                except TimeoutException:
                    index = 1
                    break
        if printTotal:
            print(f"Found {len(links)} links!")
        return links

    def removeDuplicates(self, toRemove, dirtyList):
        new = {k: v for v, k in enumerate(toRemove)}
        remove = list(new.values())
        lol = []
        for x, y in enumerate(toRemove):
            if x not in remove:
                lol.append(x)
        cleanList = []
        for a, b in enumerate(dirtyList):
            if a not in lol:
                cleanList.append(b)
        return cleanList

    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            # sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def makeEleVisible(self):
        self.scroll_down()
        self.maximize()
        self.ele("body", locaTy="tag", keys=Keys.HOME)