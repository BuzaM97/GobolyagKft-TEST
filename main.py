from creat_sheet import creat_xls
from write_sheet import add_data_to_sheet
from selenium.common.exceptions import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
START_URL = "https://gombolyagkft.hu/"

chrome_driver_path = r"C:\Users\buzam\Documents\Programming\Chrome Driver\chromedriver"
driver = webdriver.Chrome(chrome_driver_path)
driver.get(START_URL)
# Get a response from url with requests modul
# response = requests.get(START_URL)

# Get the website html version
# website_html = response.text
# Scrapping the data with BeautifulSoup
# soup = BeautifulSoup(website_html)

# ---------- VISIBLE TEXT
# [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
# Get the visible text, to check typos
# visible_text = soup.getText()
# print(visible_text)
# ----------

# Check if the links leads to the correct destination
def links_check(class_name, cell_location):
    menu_links = driver.find_elements(By.CLASS_NAME, class_name)
    # Click every menu link (all 12 working 8)
    # Starting num of check link
    link_cheks = 0
    # Num of all menu links(including not workin ones)
    working_menu_link = len(menu_links)
    print(len(menu_links))
    for n in range(len(menu_links)):
        print(n)
        if class_name=="menu-link":
            # Menu link appear on every page, the test does not get back to the main page,
            # but continuously check the next main menu link
            menu_links = driver.find_elements(By.CLASS_NAME, class_name)
        # Catch the not working/appearing menu links
        try:
            link_href = menu_links[n].get_attribute('href')
            print(link_href)
            menu_links[n].click()
            current_url=driver.current_url
            # print(f"href={link_href}")
            # print(f"current={current_url}")
            if current_url==link_href:
                # Add one value to check links
                link_cheks += 1

        except ElementNotInteractableException:
            # Decrease the manu links, to get the num of working links
            working_menu_link-=1
        # If the given link does not show up in the header or footer, step back to the main page to open the next link
        if class_name=="elementor-button-link" or \
                class_name=="woocommerce-LoopProduct-link" or \
                class_name=="ast-loop-product__link":
            driver.back()
            time.sleep(5)


    add_data_to_sheet(cell_location=cell_location, test_cases=working_menu_link, successful_checks=link_cheks)
# Check if the correct value and price added to the cart
def add_to_cart_check(class_name, cell_location):
    time.sleep(5)
    # List of all wp-element buttons, these are connected to products
    items_div=driver.find_elements(By.CLASS_NAME, class_name)
    # List of all prices on the site, including the cart (prices[0]) (Selenium web element)
    prices= driver.find_elements(By.CLASS_NAME, 'woocommerce-Price-amount')
    int_prices=[]
    # From the prices selenium web element format to an int
    for p in prices:
        # Get rid of the " Ft"
        try:
            int_prices.append(int(p.text[:-2]))
        # Catch error from empty elements
        except ValueError:
            pass
    sum_prices=0
    # Add upp all the int elements to get the sum of all item's prices 
    for v in int_prices:
        sum_prices=sum_prices+v


    print(sum_prices)
    # List of the buttons of sizes
    sizes_btns= driver.find_elements(By.CLASS_NAME, 'cfvsw-swatches-option')
    # For the test we chose the s size
    s_size_btns = sizes_btns[0::5]
    # click on each ad to cart
    for click_on_btn in s_size_btns:
        click_on_btn.click()
    # Before a successful check set the num of checks to 0
    checks= 0
    # Click all add to cart button one by one
    for n in range(len(items_div)):
        items_div[n].click()
        time.sleep(5)

    prices= driver.find_elements(By.CLASS_NAME, 'woocommerce-Price-amount')
    # The cart's value after adding every item on the page
    carts_value=int(prices[0].text[:-2])
    # Comparing the cart's value and the sum of all items's prices
    if carts_value == sum_prices:
        # After a successful check add a checks num 1
        checks += 1
        # Send the num of checks and successful checks and the cell location to the write_sheet module
        add_data_to_sheet(cell_location=cell_location,test_cases=len(items_div), successful_checks=checks )

        # links_check(class_name= "menu-link", cell_location="B8")
# links_check(class_name= "elementor-button-link", cell_location="B18")
# links_check(class_name= "woocommerce-LoopProduct-link", cell_location="B26")
# links_check(class_name= "ast-loop-product__link", cell_location="B34")
add_to_cart_check(class_name= "wp-element-button", cell_location="B42")

# creat_xls(check_type="menu_links", whole_num= working_menu_link, successful_checks= link_cheks )
