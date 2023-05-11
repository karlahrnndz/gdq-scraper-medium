from bs4 import BeautifulSoup
import scrapy
import re
from ..items import BidItem
from unidecode import unidecode

class Bids(scrapy.Spider):
    name = "bids"
    start_urls = ['https://gamesdonequick.com/tracker/bids/']

    def parse(self, response):
        """Find links to event bid pages and run "parse_event" on each."""
        
        event_bidspge_lst = response.css('div.list-group a')
        yield from response.follow_all(event_bidspge_lst, self.parse_event)

    def parse_event(self, response):
        """Extract bids data for one event."""

        # Extract rows
        soup = BeautifulSoup(response.text, "lxml")  # Pass response from an event's bids site to bs
        event = unidecode(soup.title.text.split('—')[-1].strip().lower())  # Get and clean event name
        header = self.clean_header([ele.text for ele in soup.find('thead').find_all('th')])  # Get and clean table header
        table = soup.find('table')  # Find first table
        rows = table.find_all('tr', {'class': 'small'})  # Find all table rows of class "small"
        
        # Parse row
        for row in rows:
            bid_id = row.a['href'].split('/')[-1]  # Each row has a link with more bid details. Using last part of link as bid_id
            cols = self.clean_row([col.text for col in row.find_all('td')])  # Apply custom "clean_row" method to each row (see below)
            no_cols = len(cols)  # Get number of columns in scraped row

            if no_cols == 5:  # Regular or parent bid
                parent_bid_id = bid_id   # The bid_id for parent bids or rows with no children is itself
                is_child = False
            
            elif no_cols == 4:  # Child bid
                cols.append('')  # Goal (last column) is not available in child bids
                is_child = True

            else:
                continue

            # Construct dict with metadata (the 4 additional attributes)
            meta_dict = {'bid_id': bid_id,
                        'parent_bid_id': parent_bid_id,
                        'is_child': is_child,
                        'event': event}

            # Create instance of BidItem with scraped row data + metadata
            item = BidItem(**dict(zip(header, cols)), **meta_dict)

            # If the yielded item is not an instance of BidIdem, the pipeline
            # we defined will ignore this scraped item entirely.
            # In other words, if item does not contain exactly the same attributes
            # Defined in the BidItem class, the item will not be saved.
            # This is why the header is being converted to lower case with spaces
            # replaced by "_" in the clean_header() method below.
            yield(item)

    def clean_row(self, row):
        """Simple method for cleaning text in row data."""

        row = [re.sub(' +', ' ', unidecode(ele)
                    .replace('Show Options', '')
                    .replace('Hide Options', '')
                    .replace('\n', '')
                    .replace('\r', '')
                    .replace('--', '')
                    .strip()
                    .lower())
                    for ele in row]
        
        return row

    def clean_header(self, header):
        """
        Simple method for cleaning text in header data.
        """

        header = [re.sub(' +', ' ', unidecode(ele)
                        .replace('AscDsc', '')
                        .replace('\n', '')
                        .replace('\r', '')
                        .strip()
                        .lower()).replace(' ', '_')
                        for ele in header]
        
        return header