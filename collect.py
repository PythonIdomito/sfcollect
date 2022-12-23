import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait, expected_conditions as ec
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import bs4
from bs4 import BeautifulSoup
from models import *

def get_date_from_comment(string):
    date=string.replace(",", "").split()
    date=f"{date[2]} {date[0]} {date[1]} {date[3]}"
    return datetime.strptime(date, "%Y %b %d %X")

def get_comments(driver : uc.Chrome, waitObj: wait.WebDriverWait, pagenumber, sess:Session):
    driver.get(f"http://forum.sodika.org/?pageNo={pagenumber}")
    page=BeautifulSoup(driver.page_source, features="html.parser")
    comments=page.find_all(attrs={"class":"comment"})

    c:bs4.element.Tag # annotate type
    for c in comments:
        comment=Comment(
            id=int(c["rel"]),
            name=c.find("strong").get_text(),
            date=get_date_from_comment(c.find(class_="date").get_text()),
            comment_text=c.find(class_="innerDiv").decode_contents().replace("\t",""),
            points=int(c.find(class_="buttons").find("b").get_text()),
            is_registered=("verified" in c.find("strong")["class"]),
            page_number=pagenumber
        )
        sess.merge(comment)
    print(pagenumber)

driver = uc.Chrome()
driver.get("http://forum.sodika.org")

wait=wait.WebDriverWait(driver, 20)
wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "comment")))

last_page_num=int(driver.find_element(By.CLASS_NAME, "paginator")\
    .find_elements(By.TAG_NAME, "a")[-1].text)

older_than3days_page=1

sess=Session(engine)
last_stored_comment=sess.query(Comment).order_by(Comment.id.desc()).first()

if last_stored_comment!=None:
    olddate=(last_stored_comment.date-timedelta(days=3))
    older_than3days=sess.query(Comment).filter(Comment.date < olddate).order_by(Comment.date.desc()).first()
    if older_than3days!=None:
        older_than3days_page=older_than3days.page_number
        print(f"last saved comment date - 3 days = {older_than3days.date}")
sess.close()

sess=Session(engine)
for i in range(older_than3days_page, last_page_num+1, 1):
    get_comments(driver, wait, i, sess)
    if i%50==0 or i==last_page_num:
        sess.commit()
        print("COMMIT")
sess.close()


