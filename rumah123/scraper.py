from functions import *

def main():
    start = 360
    end = 370
    while True:
        start_time = time.time()
        # Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # Create a SafeItemList instance
            safe_item_list = SafeItemList()

            # List of items to be processed
            items_to_process = load_json('OUTPUT/agents_page.json')[start:end]

            # Submit tasks to the ThreadPoolExecutor
            futures = [executor.submit(process_item, item) for item in items_to_process]
            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
            results = [future.result() for future in futures]
            flattened_results = [item for sublist in results for item in sublist]
            safe_item_list.add_item(flattened_results)
            
            processed_items = safe_item_list.items
            to_json(f'OUTPUT/prod/agents_listing{start}-{end}.json', processed_items)
            end_time = time.time()
            elapsed_time = end_time - start_time
        
        print(f"Elapsed time: {elapsed_time} seconds. from {start}-{end}")
        start += 50
        end += 50




def main2():
    page = 1

    while True:
        try:
            start_time = time.time()
            # Create a ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                # Create a SafeItemList instance
                safe_item_list = SafeItemList()

                # List of items to be processed
                # items_to_process = load_json('OUTPUT/agents_page.json')[start:end]
                items_to_process = get_agent_page(page)
                # Submit tasks to the ThreadPoolExecutor
                futures = [executor.submit(process_item, item) for item in items_to_process]
                # Wait for all tasks to complete
                concurrent.futures.wait(futures)
                results = [future.result() for future in futures]
                flattened_results = [item for sublist in results for item in sublist]
                safe_item_list.add_item(flattened_results)
                
                processed_items = safe_item_list.items
                to_json(f'OUTPUT/prod_update2/agents_listing_{page}.json', processed_items)
                end_time = time.time()
                elapsed_time = end_time - start_time
            
            print(f"Elapsed time: {elapsed_time} seconds. Agents page : {page}")
            page += 1
        except:
            print(f"FAIL PAGE {page}")
            page += 1
        

if __name__ == "__main__":
    main()
    # main2()