from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import JobListing
from datetime import date
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings

# Fetch jobs from indeed
def scrape_indeed():
    # Open browser
    driver = webdriver.Chrome()

    # Go to Indeed search
    driver.get("https://www.linkedin.com/")

    # Find the search box and type query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python Developer")
    search_box.send_keys(Keys.RETURN)

    # Wait untill job results appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "jobTitle"))
    )

    print(driver.page_source[:2000])
    
    # Grab job titles (limit to first 5)
    jobs = driver.find_elements(By.CLASS_NAME, "jobTitle")[:5]
    
    print(driver.page_source[:2000])

    print("Top 5 job title:")
    for job in jobs:
        print("-", job.text)
        JobListing.objects.get_or_create(
            title=job.text,
            company="Unknow",
            location="Unknow",
            defaults={ "url": "https://indeed.com", 'date_posted': date.today()}
        )
        

    # Close browser
    driver.quit()
    
def save_logo_from_url(job, image_url):
    if not image_url:
        return None
    
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            filename = f"{job.company}_{os.path.basename(image_url.split("?")[0])}"
            job.image.save(filename, ContentFile(response.content), save=True)
    except Exception as e:
        print("Could not download logo:", e)
    
    
def scrape_jobs_linkedin(keyword):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    # --- Login ---
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys("murio87@gmail.com")
    password_input.send_keys("kogi@murio87")
    password_input.send_keys(Keys.RETURN)


    print(f"\n🔎 Search for: {keyword}")
    driver.get("https://www.linkedin.com/jobs/search/")

    # --- Search box ---
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
        )
    )
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # --- Retry loop for job cards ---
    jobs = []
    for i in range(5):
        try:
            jobs = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.job-card-container"))
            )
            if jobs:
                break
        except:
            print(f"⚠️ No jobs yet, scrolling... (try {i+1})")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

    if not jobs:
        print(f"❌ No jobs for {keyword}")
        driver.quit()
        return

    print("Top 5 LinkedIn job titles:")
    seen = set()
    for idx in range(min(10, len(jobs))):
        try:
            job = driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")[idx]
            
            title_el = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link")
            company_el = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle span")
            location_el = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption li span")
            
            try:
                image_el = job.find_element(By.CSS_SELECTOR, "div.job-card-list__logo img")
                image = image_el.get_attribute("src").strip() if image_el else None
            except:
                image = None

            title = title_el.text.strip()
            company = company_el.text.strip() if company_el else 'Unknown'
            location = location_el.text.strip() if location_el else 'Unknown'
            url = title_el.get_attribute("href")
            
            if url in seen: # skip duplicates
                continue
            seen.add(url)

            # Optional filter
            if keyword.lower() not in title.lower():
                continue

            print("-", title, "|", company, "|", location, "|", image, "|", url)

            job, created = JobListing.objects.get_or_create(
                title=title,
                company=company,
                location=location,
                defaults={"url": url, "date_posted": date.today()},
            )
            
            if created and image:
                save_logo_from_url(job, image)
        except Exception as e:
            print("⚠️ Skipped one card:", e)

    driver.quit()

