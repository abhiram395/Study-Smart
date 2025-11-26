from googlesearch import search
import requests
import os
import tempfile

class WebScraper:
    def __init__(self):
        pass

    def find_papers(self, subject_name, university="", num_results=3):
        """
        Searches for question papers for the given subject.
        Returns a list of local paths to downloaded PDFs.
        """
        # Improved query with filetype:pdf
        if university:
            query = f"{university} {subject_name} question paper filetype:pdf post 2020"
        else:
            query = f"{subject_name} question paper filetype:pdf post 2020"
        print(f"Searching for: {query}")
        
        downloaded_files = []
        
        try:
            # Search for PDFs
            urls = []
            # Increase num_results to scan more candidates
            for url in search(query, num_results=15, advanced=True):
                # advanced=True returns SearchResult objects, but basic returns strings
                # Let's stick to basic for now, but handle the iterator carefully
                pass 
            
            # Re-implementing loop to be safer with the generator
            count = 0
            for url in search(query, num_results=20):
                if url.lower().endswith('.pdf'):
                    urls.append(url)
                    count += 1
                    if count >= num_results:
                        break
            
            if not urls:
                print("No direct PDF links found. Trying broader search...")
                # Fallback: Try without filetype:pdf but look for 'pdf' in url
                query_fallback = f"{subject_name} previous year question paper pdf"
                for url in search(query_fallback, num_results=15):
                    if url.lower().endswith('.pdf'):
                        urls.append(url)
                        if len(urls) >= num_results:
                            break

            if not urls:
                print("Still no PDF URLs found.")
                return []

            print(f"Found {len(urls)} potential PDFs. Downloading...")

            # Download files
            for i, url in enumerate(urls):
                try:
                    print(f"Downloading {url}...")
                    # User-Agent is often required to avoid 403 Forbidden
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                        # Save to temp file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(response.content)
                            downloaded_files.append(tmp.name)
                            print(f"Successfully downloaded: {tmp.name}")
                    else:
                        print(f"Skipping {url}: Not a valid PDF (Status: {response.status_code}, Type: {response.headers.get('Content-Type')})")
                        
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
                    
        except Exception as e:
            print(f"Search failed: {e}")
            return []
            
        return downloaded_files

    def find_study_material(self, topic, num_results=2):
        """
        Searches for study material/tutorials for a specific topic.
        Returns a list of tuples: (Title, URL)
        """
        # Targeted search for tutorials
        query = f"{topic} tutorial geeksforgeeks javatpoint tutorialspoint"
        print(f"Finding resources for: {topic}")
        
        resources = []
        try:
            for url in search(query, num_results=num_results):
                # Simple heuristic to get a readable title from URL
                # e.g. https://www.geeksforgeeks.org/compiler-design-tutorials/ -> Compiler Design Tutorials
                domain = url.split('//')[-1].split('/')[0].replace('www.', '')
                resources.append((f"Tutorial ({domain})", url))
                
        except Exception as e:
            print(f"Resource search failed for {topic}: {e}")
            
        return resources
