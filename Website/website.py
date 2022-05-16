from prettytable import PrettyTable
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import Website.xPaths as x
from selenium.common.exceptions import *
from selenium.webdriver import Keys
import Website.url as u
from Selenium.elements import Elements


class McGraw(Elements):
    def __init__(self, **kwargs):
        self.questionL = None
        self.fixedQuestion = None
        self.connectTab = None
        self.fixedAnswer = None
        self.answer = None
        self.key_word_3 = None
        self.key_word_2 = None
        self.key_word_1 = None
        self.googleTab = None
        self.question = None
        super().__init__(**kwargs)

    def quizletLogin(self, email, password, timeout=2):
        self.get("https://quizlet.com/login")
        try:
            self.ele(x.quizletEmail, ECType="click", keys=f"{email}", timeout=timeout)
            self.ele(x.quizletPass, ECType="click", keys=f"{password}" + Keys.ENTER, timeout=timeout)
            self.urlChange("https://quizlet.com/login")
        except TimeoutException:
            print("Already logged in!")

    def mcGrawLogin(self, email, password, timeout=2):
        self.get(u.BASE_URL)
        self.get(u.LOGIN_URL)
        try:
            self.ele("login-email", locaTy="id", keys=email, timeout=timeout, keysSlow=False)
            self.ele("login-password", locaTy="id", keys=password + Keys.ENTER, keysSlow=False)
        except TimeoutException:
            print("Already logged in!")

    def startAssignment(self):
        self.ele(x.assignmentFrame, ECType='frame')
        try:
            self.ele(x.findAssignment, ECType="click").click()
            print('Assignments found, starting first one!')
        except TimeoutException:
            print('No Assignments found!')
        self.ele("launchRHP", ECType="click", locaTy="id").click()

    def startQuestions(self, timeout):
        self.switchDC()
        try:
            self.ele(x.startQues, ECType="click", timeout=timeout).click()
            print("Starting questions...")
        except TimeoutException:
            pass
        try:
            self.ele(x.startQues2, ECType="click", timeout=timeout).click()
            print("Starting questions...")
        except TimeoutException:
            pass
        try:
            self.ele(x.continueQues, ECType="click", timeout=timeout).click()
            print("Continuing questions...")
        except:
            pass

    def closePopup(self, timeout):
        try:
            self.ele("action-button", ECType="click", locaTy="class", timeout=timeout).click()
        except TimeoutException:
            print("No prompts!")

    @property
    def currentQuestion(self):
        return self.ele(x.currentQuestion, getText=True)

    @property
    def questionsDone(self):
        return int(self.currentQuestion.split()[1])

    @property
    def questionsLeft(self):
        return int(self.currentQuestion.split()[3])

    def questionFind(self):
        self.connectTab = self.current_window_handle
        self.log(self.connectTab)
        print(f"Working on {self.currentQuestion}...")
        self.questionL = []
        self.question = self.ele("question", locaTy="class", getText=True)
        self.questionL.append(self.question)
        translator = (str.maketrans('', '', '"?!.,'))
        almost_fixed_question = (self.question.translate(translator))
        self.fixedQuestion = almost_fixed_question.replace("'s", "")
        self.question = almost_fixed_question.replace("'s", "")

        self.key_word_1 = sorted((x for x in self.fixedQuestion.split() if "___" not in x), key=len)[-1]
        self.key_word_2 = sorted((x for x in self.fixedQuestion.split() if "___" not in x), key=len)[-2]
        self.key_word_3 = sorted((x for x in self.fixedQuestion.split() if "___" not in x), key=len)[-3]
        self.key_word_4 = sorted((x for x in self.fixedQuestion.split() if "___" not in x), key=len)[-4]

    def printKeywords(self):
        print(f"Keywords = {self.key_word_1}, {self.key_word_2}, {self.key_word_3}, {self.key_word_4}")

    def searchOnGoogle(self):
        self.switch_to.new_window()
        self.googleTab = self.current_window_handle
        self.get(u.GOOGLE_URL)
        self.ele("q", locaTy="name", keys=f'{self.question} + site:quizlet.com' +
                                          Keys.ENTER, keysSlow=False)

    def removeGoogleElement(self):
        try:
            self.execute_script("""var people_also_ask = arguments[0];
                            people_also_ask.parentNode.removeChild(people_also_ask);""",
                                self.ele(x.googleElement, timeout=1))
        except TimeoutException:
            self.log('No People Ask Me Section found!')

    def googleResultClick(self, searchNum):
        self.ele(f"(//div[@id='search']//following::h3)[{searchNum}]", ECType="click", timeout=5).click()
        try:
            self.ele(x.quizletPopup, ECType='click').click()
        except:
            pass

    def getAnswer(self):
        self.printKeywords()
        searchNum = 1
        keepSearching = True
        while keepSearching:
            try:
                self.googleResultClick(searchNum)
            except WebDriverException as e:
                print(e)
            quesNum = 2
            while True:
                try:
                    self.answer = self.ele(
                        f"(//*[contains(text(),'{self.key_word_1}') and contains(text(),'{self.key_word_2}') and contains(text(),'{self.key_word_3}')])[{quesNum}]/following::span[1]",
                        getTextP=True, wait=False)
                    self.switch_to.window(self.connectTab)
                    acceptAnswer = int(input("Press 1 to try different answer or 2 to move on: "))
                    if acceptAnswer == 1:
                        quesNum += 1
                        self.switch_to.window(self.googleTab)
                        continue
                    elif acceptAnswer == 2:
                        self.close()
                        self.switch_to.window(self.connectTab)
                        keepSearching = False
                        break
                    else:
                        print("Enter 1 or 2 only!")
                except NoSuchElementException:
                    searchNum += 1
                    self.execute_script("window.history.go(-1)")
                    break

    def getAnswer2(self):
        ansReq = 5
        while True:
            self.switchDC()
            searchNum = 1
            answers = []
            NoMoreResults = False
            print(f"Working on question = {self.question}")
            print(f"Looking for first {ansReq} answers...")
            while len(answers) != ansReq and NoMoreResults is False:
                while True:
                    try:
                        self.removeGoogleElement()
                        self.ele(f"(//div[@id='search']//following::h3)[{searchNum}]", ECType="click",
                                 timeout=2).click()
                        break
                    except ElementClickInterceptedException:
                        self.log("error: ElementClickInterceptedException. Waiting and trying again...")
                        self.switchDC()
                        self.makeEleVisible()
                        continue
                    except TimeoutException:
                        print("No more google results!")
                        self.execute_script("window.history.go(+1)")
                        NoMoreResults = True
                        break
                quesNum = 1
                while len(answers) != ansReq and NoMoreResults is False:
                    try:
                        self.makeEleVisible()
                        while True:
                            try:
                                self.answer = self.ele(
                                    f"(//*[contains(text(),'{self.key_word_1}') and contains(text(),'{self.key_word_2}') "
                                    f"and contains(text(),'{self.key_word_3}') and contains(text(),'{self.key_word_4}')])[{quesNum}]/following::span[1]",
                                    getText=True, wait=False)
                                break
                            except StaleElementReferenceException:
                                self.log("StaleElementReferenceException error, trying again after 0.5s...")
                                sleep(0.5)
                                continue
                        if self.answer == '':
                            quesNum += 1
                            continue
                        else:
                            answers.append(self.answer)
                            quesNum += 1
                            continue
                    except NoSuchElementException:
                        searchNum += 1
                        self.execute_script("window.history.go(-1)")
                        break
            self.printTable(answers)
            self.key_word_4 = sorted(self.fixedQuestion.split(), key=len)[-4]
            if 0 < len(answers) < ansReq:
                self.close()
                self.switch_to.window(self.connectTab)
                input("These are all the answers I could find, enter 1 once on next question..")
                break
            else:
                self.switch_to.window(self.connectTab)
                more = input(
                    "Enter 1 to move on, 2 to look for more answers or if the answers are too random, enter an exact word from the question to include in the search: ")
                if more == '1':
                    self.switch_to.window(self.googleTab)
                    self.close()
                    self.switch_to.window(self.connectTab)
                    self.switchDC()
                    newQuestionL = []
                    newQuestion = self.ele("question", locaTy="class", getText=True)
                    newQuestionL.append(newQuestion)
                    while newQuestionL[0] == self.questionL[0]:
                        newQuestionL.pop(0)
                        newQuestion = self.ele("question", locaTy="class", getText=True)
                        newQuestionL.append(newQuestion)
                        sleep(1.5)
                        print("Same question, click on next...")
                    print("Found new question!")
                    self.questionL.pop(0)
                    break
                elif more == '2':
                    ansReq += 3
                    self.switch_to.window(self.googleTab)
                    self.execute_script("window.history.go(-1)")
                    continue
                else:
                    print(f"Using '{more}' instead of '{self.key_word_4}' as the new 4th key word...")
                    self.key_word_4 = more
                    self.switch_to.window(self.googleTab)
                    self.execute_script("window.history.go(-1)")
                    continue

    def fixAnswerText(self):
        translator1 = (str.maketrans('', '', '?!.-,'))
        almost_fixed_answer_text = (self.answer.translate(translator1))
        self.fixedAnswer = almost_fixed_answer_text.replace("'s", "")
        print(self.fixedAnswer)

    def clickAnswer(self):
        if len(self.fixedAnswer.split()) == 1:
            self.execute_script("arguments[0].click();",
                                WebDriverWait(self, 2).until(EC.element_to_be_clickable((
                                    By.XPATH,
                                    f"//label[contains(., '{self.fixedAnswer}')]/child::input"))))

        answer_word_1 = sorted(self.fixedAnswer.split(), key=len)[-1]
        print(f'Word 1 = {answer_word_1}')
        answer_word_2 = sorted(self.fixedAnswer.split(), key=len)[-2]
        print(f'Word 2 = {answer_word_2}')
        answer_word_3 = sorted(self.fixedAnswer.split(), key=len)[-3]
        print(f'Word 3 = {answer_word_3}')
        try:
            self.execute_script("arguments[0].click();",
                                WebDriverWait(self, 2).until(EC.element_to_be_clickable((
                                    By.XPATH,
                                    f"//label[contains(., '{answer_word_1}') and contains(., '{answer_word_2}') and contains(., '{answer_word_3}')]/child::input")))
                                )
        except TimeoutException:
            input("do it yourself")

    def nextQuestion(self):
        while True:
            nextQues = int(input("If on new question, enter 1: "))
            if nextQues == 1:
                print("Working on this question...")
                break
            else:
                print("Enter 1 only or terminate me!")
                continue

    def printTable(self, answers):
        pT = PrettyTable()
        pT.title = f"Keywords = {self.key_word_1}, {self.key_word_2}, {self.key_word_3}, {self.key_word_4}"
        pT.field_names = [f"{self.question}"]
        for index, item in enumerate(answers, 1):
            pT.add_row([f"Answer {index}: {item}"])
        pT.align = "l"
        print(pT)