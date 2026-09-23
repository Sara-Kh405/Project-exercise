from playwright.sync_api import Page
import re
import pandas as pd
import time

class Scroll:
    def __init__(self, page:Page):
        self.page = page

    def select_name_price_score(self):
        print("\nScrolling to load more hotels...")
        time.sleep(3)
        
        all_hotels_data = []
        seen_hotels = set()
        
        MAX_HOTELS = 15
        MAX_SCROLLS = 20
        MAX_NO_NEW = 5
        
        scroll_count = 0
        no_new_hotels_count = 0
        
        while scroll_count < MAX_SCROLLS and no_new_hotels_count < MAX_NO_NEW:
            try:
                self.page.evaluate("window.scrollBy(0, 600)")
                time.sleep(2)
                
                hotel_elements = self.page.locator('li[data-selenium="hotel-item"]')
                current_count = hotel_elements.count()
                
                new_hotels_found = False
                
                for i in range(current_count):
                    try:
                        if len(all_hotels_data) >= MAX_HOTELS:
                            print(f"\nReached {MAX_HOTELS} hotels limit!")
                            break
    
    
                        hotel_item = hotel_elements.nth(i)
                        
                        try:
                            hotel_name = hotel_item.locator('a[data-selenium="hotel-name"]').text_content(timeout=3000)
                            if not hotel_name or hotel_name.strip() == "":
                                continue
                            hotel_name = hotel_name.strip()
                        except:
                            continue
                        
                        if hotel_name in seen_hotels:
                            continue
    
                #****************************
                #****************************
                         
                        try:
                            hotel_price = hotel_item.locator('span[data-selenium="display-price"]').text_content(timeout=3000)
                            if not hotel_price or hotel_price.strip() == "":
                                hotel_price = "N/A"
                            else:
                                hotel_price = hotel_price.strip()
                        except:
                            hotel_price = "N/A"
    
                #****************************
                #****************************
            
                        hotel_score = "N/A"
                        try:
                            review_box = hotel_item.locator('div[data-element-name="property-card-review"]')
                            if review_box.count() > 0:
                                sr_text = review_box.locator('span[class*="ScreenReaderOnly"]').first.text_content(timeout=3000)
                                # sr_text مثل: "Average rating Very good 7.8 out of 10 with 43 reviews"
                                match = re.search(r'Average rating (.+?) (\d+\.\d+) out of', sr_text)
                                if match:
                                    rating_text = match.group(1).strip()   # "Very good"
                                    score = match.group(2).strip()          # "7.8"
                                    hotel_score = f"{score} {rating_text}"
                        except Exception as e:
                            print(f"Score extraction error: {e}")
    
                #***************************
                #***************************
                        
                        all_hotels_data.append([hotel_name, hotel_price, hotel_score])
                        seen_hotels.add(hotel_name)
                        new_hotels_found = True
                        print(f"Hotel {len(all_hotels_data)}: {hotel_name} - Price: {hotel_price} - Score: {hotel_score}")
                        
                    except Exception as e:
                        if "closed" in str(e).lower():
                            break
                        continue
                
                if len(all_hotels_data) >= MAX_HOTELS:
                    break
                
                if not new_hotels_found:
                    no_new_hotels_count += 1
                else:
                    no_new_hotels_count = 0
                
                scroll_count += 1
                
            except Exception as e:
                if "closed" in str(e).lower():
                    break
                break
        
        print(f"\nTotal hotels extracted: {len(all_hotels_data)}")
        
        if all_hotels_data:
            try:
                df = pd.DataFrame(all_hotels_data, columns=['Hotel Name', 'Hotel Price', 'Hotel Score'])
                df.to_csv('hotel_results.csv', index=False, encoding='utf-8-sig')
                print(f"\nCSV file saved with {len(all_hotels_data)} hotels")
                
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print("No hotels extracted!")
        
        print("\nClosing browser...")
        time.sleep(2)
        print("Done!")