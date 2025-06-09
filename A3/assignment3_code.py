books = [
    {"ISBN": "9781785150289", "Title": "Go Set a Watchman", "Author": "Harper Lee", "Price": 9.89},
    {"ISBN": "9780744016697", "Title": "The Legend of Zelda: Tri Force Heroes", "Author": "Prima Games", "Price": 14.99},
    {"ISBN": "9780099529126", "Title": "Catch-22", "Author": "Joseph Heller", "Price": 6.29},
    {"ISBN": "9780007447831", "Title": "A Clash of Kings", "Author": "George R. R. Martin", "Price": 4.95},
    {"ISBN": "9781853260001", "Title": "Pride and Prejudice", "Author": "Jane Austin", "Price": 1.99},
    {"ISBN": "9780099576853", "Title": "Casino Royale", "Author": "Ian Fleming", "Price": 6.79},
    {"ISBN": "9780099549482", "Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Price": 4.99},
    {"ISBN": "9780333998667", "Title": "Fundamentals of Computer Architecture", "Author": "Mark Burrell", "Price": 41.10},
    {"ISBN": "9780701189358", "Title": "Simply Nigella: Feel Good Food", "Author": "Nigella Lawson", "Price": 12.50},
]

import urllib.request  
import json
import random
from datetime import time, date, datetime, timedelta


class helperClass:
    
    @staticmethod
    def maxLength(data, key):

        """
        This method finds the maximum length of values for a given key in a list of dictionaries.

        Parameters:
            key (int): The key in a dictionary whose values' lengths should be calculated.

        Returns:
            max_length (int): The maximum length of a value in corresponding to the given key. 

        Raises:
            KeyError: If the given key does not exist in any dictionary. 

        Example:
            >>> demo = bookData()
            >>> demo.maxLength('Title')
                25
        """

        # Initialise flags
        max_length = 0
        found_key = False

        # Compare lengths
        for item in data:
            if key in item:
                found_key = True
                length = len(str(item[key]))
                max_length = max(max_length, length)

        if not found_key:
            raise ValueError(f"The given key '{key}' does not exist in any dictionary in the list.")
             
        return max_length

    @staticmethod
    def add_hyphen(to_string, index):
        """
        This method adds a hypen at a specified index within a string.

        The method first converts the number string to a string and then slices the it into two parts:
            1. 'string[:index]' gives everything before the index.
            2. string[index:]' gives everything after the index. 
        A hypen is then inserted in between these two slices.

        Parameters:
            to_string (int): The input to be modified.
            index (int): The position at which to insert a hyphen. 

        Returns:
            str: A new string with the hyphen inserted at the specified index.

        Raises:
            TypeError: If the given index is not an integer. 
            ValueError: If the index is out of bounds (less than 0 or greater than the length of the string. 

        Example:
            >>> demo = bookData()
            >>> demo.add_hyphen("14254235", 3)
            '142-54235'
        """
        string = str(to_string)

        # Validation
        if not isinstance(index, int):
            raise TypeError(f"'{index}' must be an integer.")
            
        if index < 0 or index >= len(string):
            raise ValueError("Index is out of bounds.")

        # Insert hyphen at given index
        return string[:index] + '-' + string[index:]

    
    @staticmethod
    def wrap_text(text, width):
        """
        This method wraps text, splitting long words to fit within a given width.

        The method replaces new line characters with space characters and splits the text 
        string into a list. For each word in the list, the method checks if the length of 
        the word is greater than the given width. If it is, the word is split into multiple 
        parts using slicing at the specified width. The parts are added to a list called 'lines'.
        Words that fit within the width are combined into lines, ensuring that each line does 
        not exceed the given width. 

        Parameters:
            text (str): Text to be wrapped according to a specific width. 
            width (int): The width to restrict some text to. 

        Raises:
            TypeError: If 'text' is not a string, or 'width' is not an integer. 

        Returns:
            lines (list): A list of strings, with each element being a line of wrapped text.  

        Example:
            >>> helperClass.wrap_text("This is a demo of how to wrap text.", 10)
            ['This is a', 'demo of h', 'ow to wra', 'p text.']

        """

        if not isinstance(text, str) or not isinstance(width, int):
            raise TypeError(f"'{text}' must be a string, and '{width}' must be an integer.")
            
        # Remove new line characters
        text = text.replace('\n', ' ')  
    
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # If the current word exceeds the width by itself
            while len(word) > width:
                lines.append(word[:width])  
                word = word[width:]  
    
            # If the current line plus the next word fits within the width
            if len(current_line) + len(word) + 1 <= width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)  
                current_line = word

        # Add the last line if there's leftover content
        if current_line:
            lines.append(current_line)

        return lines


    @staticmethod
    def preview_limit(text, max_length=50):
        
        """
        This method limits a given text to a specified maximum length, 
        appending with "...".

        This method checks if the input text exceeds `max_length`. If it does, 
        the text is shortened to the `max_length` of characters, followed by "...". 
        Otherwise, the original text is returned.

        Parameters:
            text (str): The input string to be truncated.
            max_length (int, optional): The maximum allowed length for the output string. 
                Defaults to `50`.

        Raises:
            None

        Returns:
            text (str) : The truncated text if it exceeds `max_length`; otherwise, the
            original text.

        Example:
            >>> preview_limit("This is a long sentence that needs to be cut off.", max_length=20)
                'This is a long sente...'

        """
        # Truncate at given length
        if len(text) > max_length:
            previewed_text = text[:max_length] + "..."
            return previewed_text
        else:
            return text
        
            

    @staticmethod
    def get_url(url):
        """
        This method fetches JSON data from a specified URL.

        This method uses the .request.urlopen() method from the standard Python library to open
        a specified URL. If there was no error opening the URL, the raw data is read and decoded,
        before being returned. If the server did not contain any valid JSON data a 
        JSONDecodeError is raised.
        
        Parameters:
             URL (str): The URL of the JSON data.

        Raises:
             ValueError: If the URL does not return valid JSON data. 
             
        Returns:
            data (list or dict): Parsed JSON data.
    
        """
        try:
            with urllib.request.urlopen(url) as response:

                # Check for a valid HTTP response
                if response.status != 200:
        
                    raise ValueError(f"Failed to access data. HTTP Status: {response.status}")

                # Read and decode JSON
                raw_data = response.read().decode("utf-8")
        
                return json.loads(raw_data)
            
        except json.JSONDecodeError:
            raise ValueError("The server did not contain valid JSON data.")


    @staticmethod
    def encode_json(data):
        """
        This method encodes Python data into a JSON-formatted string.

        This method takes a Python object and encodes it into a JSON string. 

        Parameters:
            data: The python object to be encoded (e.g. dict, list, str)

        Raises:
            None

        Returns:
            json_data (str): A JSON formatted string representing the given
            input data. 

        Example:
            >>> encode_json({"animal": "dog", "age": 10})
                '{"animal": "dog", "age": 10}'

        """
        # Encode data
        json_data = json.dumps(data)

        return json_data


    @staticmethod
    def gen_rand_time():
        """
        This method generates a random time, using the 24 hour clock.

        This method randomly selects an hour, minute, and second. It then creates a time object
        from these random time parameters. 

        Parameters:
            None

        Raises:
            None

        Returns:
            str_random_time (str): A formatted string representation of the randomly
            generated time. 

        Example:
            >>> gen_rand_time()
                '15:39:15'

        """

        # Select time components randomly
        hour = random.randint(0,23)
        minute = random.randint(0,59)
        second = random.randint(0,59)

        random_time = time(hour, minute, second)

        str_random_time = random_time.strftime("%H:%M:%S")
        
        return str_random_time

    @staticmethod
    def gen_rand_date():
        """
        This method generates a random date.

        This method selects a random date between 01/01/2020 and yesterdays date, this 
        prevents future dates being generated. 

        Parameters:
            None

        Raises:
            None

        Returns:
            str_random_date (str): A string representation of the generated date.

        Example:
            >>> gen_rand_date()
            '2016:02:10'
        """
        # Set a start and end date
        start_date = datetime(2010, 1, 1)
        start_date = start_date.date()
        
        # Set to yesterday's date to prevent comments being posted in the future
        end_date = date.today() - timedelta(days=1)

        # Difference 
        difference = end_date - start_date
        day_difference = difference.days

        # Set random amount of days from start
        random_days = random.randint(0, day_difference)

        # Add to start
        random_date = start_date + timedelta(days=random_days)

        str_random_date = random_date.strftime("%Y:%m:%d")
        
        # Convert to date type
        return str_random_date


    @staticmethod
    def gen_rand_ip():
        """
        This method generates a random IP address.

        An IP address is made up of four digits between 0 and 255. The method randomly 
        generates these numbers and concatenates them together.

        Parameters:
            None

        Raises:
            None

        Returns: 
            ip (str): A string representation of the ip address.

        Example:
            >>> gen_rand_ip()
                '05.16.141.200'

        """

        # Generate four random numbers
        num_1 = random.randint(0, 255)
        num_2 = random.randint(0, 255)
        num_3 = random.randint(0, 255)
        num_4 = random.randint(0, 255)

        # Format together
        ip = f"{num_1}.{num_2}.{num_3}.{num_4}"

        return ip



class bookData:

    """This class implements functions that print information about a book.

    Attributes
    ----------
    books (list of dictionaries): The book store data.

    """


    def __init__(self, books):
        """
        Initialise the class with a list of dictionaries (books).
        """
        self.books = books


    def toISBN(self, isbn):
        """
        This method adds formatting to an ISBN number.

        The input is first validated using the 'valid()' method. Indices are 
        specified and stored in a list, 'indices'. These are all the points where
        a hyphen is to be added to the given isbn number. The method loops through the 
        elements in the 'indices' list, adding a hyphen to the isbn number where required, using
        the 'add_hyphen()' method from the helperClass. 

        Parameters:
            isbn (int): A number to be converted to isbn formatting. 

        Raises:
            --

        Returns:
            new_isbn (string): An ISBN number with hyphens inserted at the required indices.  

        Example: 
            >>> demo = bookData()
            >>> demo.toISBN("9780099529126")
            978-00099352912-6
        """

        str_isbn = str(isbn)

        # Set indices for hyphens
        indices = [3, 5, 9, 15]
        new_isbn = str_isbn

        for index in indices:
            new_isbn = helperClass.add_hyphen(new_isbn, index)

        return new_isbn

    def valid(self, isbn):
        """
        This method checks if an ISBN number is valid.

        The method first converts the given isbn number to a string and checks each element 
        of the string is a digit, and has length 13. Each element of the isbn number is added
        to a list, 'digits' and converted to be an integer. For the first 12 digits in the list,
        if the digit is odd it is multiplied by 3 and if it is even it is multiplied by one. The 
        results are stored in a new list. If 10 minus the cumulative sum modulo 10 of the 
        multiplied digits does not equal the final digit in the isbn number, then it is invalid. 

        Parameters:
            isbn (str or int): an isbn number to be validated. 

        Raises:
            ValueError: If isbn is not a 13 digit number. 

        Returns:
            Boolean: True if the digit check is correct and False otherwise. 

        Example:
            >>> demo = bookData()
            >>> demo.valid(9780099529126)
            True
            
        """
        str_isbn = str(isbn)

        # Validation checks
        if not str_isbn.isdigit() or len(str_isbn) != 13:
            raise ValueError(f"'{isbn}' must be a 13 digit number.")
            
        digits = [int(d) for d in str_isbn]
        products = []
        cumulative_sum = 0

        # Apply ISBN validation rules
        for i in range(12):
            if i % 2 == 1:
                products.append(digits[i] * 3)
                cumulative_sum += products[i]
            else:
                products.append(digits[i])
                cumulative_sum += products[i]

        check_digit = 10 - (cumulative_sum % 10)

        if digits[-1] != check_digit:
            return False
        else:
            return True

        
    def validateISBNs(self):
        """
        This method checks removes books with invalid ISBNs from a database.

        The method loops through each book in 'self.books', calling the 'valid()' method, if the 
        ISBN number is valid, the book is added the a list. If not, it is removed from the
        database and an explanatory note is printed on screen. self.books is updated in place as 
        the valid list of books. This method assumes self.books is a list of dictionaries with
        at least an 'ISBN' and 'Title' key. 

        Returns:
            The updated books database. 

        Example:
            >>> demo = bookData()
            >>> demo.validateISBNs()
                All books in database have valid ISBN numbers.
        """

        valid = []

        for book in self.books:
            if self.valid(book['ISBN']):
                valid.append(book)
            else:
                print(f"Removing book: '{book['Title']}' from the database.")

        if len(valid) == len(self.books):
            print(f"All books in database have valid ISBN numbers.")

        self.books = valid

        return self

    def printAllBooks(self, limit=None):

        """
        This method prints all books in a user-friendly, formatted table.

        The method uses the helperClass method 'maxLength()' to determine the maximum 
        length of values in the 'Title', 'Author', and 'Price' fields. These lengths 
        are used to dynamically adjust column widths for a formatted table. The ISBN is
        formatted using the 'toISBN()' method, and printed in a row of the table.
        If no books are found, a message is printed.

        Returns:
            self: Returns the instance of the object to allow method chaining.

        Example:
            >>> demo = bookData()
            >>> demo.printAllBooks()
            -----------------------------------------------------------------
            | ISBN             | Title              | Author    | Price (£) |
            -----------------------------------------------------------------
            | 978-009952912-6  |  Book Title        | A. Writer |     12.99 |
            -----------------------------------------------------------------

        """
        
        books = self.books
        if not books:
            print("No books found.")
            return self

        # This can be set depending on preference
        wrap_width = 18

        len_title = wrap_width
        len_author = max(helperClass.maxLength(self.books, 'Author'), len("Author"))
        len_price = max(helperClass.maxLength(self.books, 'Price'), len("Price (£)"))
        total_width = 19 + len_title + len_author + len_price 

        # Print header row
        print("-" * (total_width + 13))
        print(f"| {'ISBN':<19} | {'Title':<{len_title}} | {'Author':<{len_author}} | {'Price (£)':>{len_price}} |")
        print("-" * (total_width + 13))

        if limit is not None:
            books = books[:limit]

        for book in books:
            title_lines = helperClass.wrap_text(book['Title'], wrap_width)
            author_lines = [book['Author']]
            price_lines = [f"{book['Price']:.2f}"]
            isbn_lines = [self.toISBN(book['ISBN'])]

            # Pad other columns to match title's wrapped lines
            max_lines = len(title_lines)
            author_lines += [""] * (max_lines - len(author_lines))
            price_lines += [""] * (max_lines - len(price_lines))
            isbn_lines += [""] * (max_lines - len(isbn_lines))

            # Print each line of the wrapped row
            for i in range(max_lines):
                print(f"| {isbn_lines[i]:<19} | {title_lines[i]:<{len_title}} | {author_lines[i]:<{len_author}} | {price_lines[i]:>{len_price}} |")

        print("-" * (total_width + 13))
        return self
    
    def printByTitle(self, title, show=True):

        """
        This method prints the details of a book with a specified title.

        The method filters 'self.books' by the name of a given title by looping through each 
        book in the database and checking if the given title matches the 'Title' value in 
        the dictionary. The search is case insensitive as it converts the given title, and 
        the 'Title' for each book to lower case, which makes the function more robust. A
        new bookData object is initialised using the filtered data to preserve the original 
        book store data. 

        Parameters: 
            title (str): The title of a book being searched for. 
            show (boolean): A flag specifying whether the filtered results should be printed.

        Raises:
            TypeError: If the given title is not a string. 

        Returns:
            new_obj: bookData object for the filtered data, to allow method chaining.

        Example:
            >>> demo = bookData()
            >>> demo.printByTitle("Lost")
            --------------------------------------------------------------
            | ISBN                | Title    | Author        | Price (£) |
            --------------------------------------------------------------
            | 978-0-099-50012-6   | Lost     |  Michael Ro   |      6.29 |
            --------------------------------------------------------------
            
        """

        if not isinstance(title, str):
            raise TypeError(f"'{title}' must be of type string.")

        # Filter using lower case version of title
        filtered_books = [book for book in self.books if title.lower() in book['Title'].lower()]

        # Create a new object to allow chaining
        new_obj = bookData(filtered_books)
        if show:
            new_obj.printAllBooks()
        return new_obj
        

    def printByAuthor(self, author, show=True):

        """
        This method prints the details of a book with a specified author.

        The method filters 'self.books' by the name of a given author by looping through each 
        book in the database and checking if the given author matches the 'Author' value in 
        the dictionary. The search is case insensitive as it converts the given author, and 
        the 'Author' for each book to lower case, which makes the function robust. A
        new bookData object is initialised using the filtered data to preserve the original 
        book store data. 

        Parameters:
            author (str): The author of a book being searched for. 
            show (boolean): A flag specifying whether the filtered results should be printed.

        Raises: 
            TypeError: If the given 'author' is not a string. 

        Returns: 
            new_obj: bookData object for the filtered data, to allow method chaining. 
    
        Example:
            >>> demo = bookData()
            >>> demo.printByTitle("Joseph Heller")
            --------------------------------------------------------------
            | ISBN                | Title    | Author        | Price (£) |
            --------------------------------------------------------------
            | 853-0-099-50012-6   | Catch-22 | Joseph Heller |      8.90 |
            --------------------------------------------------------------
        
        """

        if not isinstance(author, str):
            raise TypeError(f"'{author}' must be of type string.")

        # Filter using lower case author name
        filtered_books = [book for book in self.books if author.lower() in book['Author'].lower()]

        # Create a new object to allow chaining
        new_obj = bookData(filtered_books)
        if show:
            new_obj.printAllBooks()
        return new_obj
        

    def printOverPrice(self, price, show=True):

        """
        This method prints the details of a book that cost more than a specified price.

        The method filters 'self.books' by looping through each book in 'self.books' 
        checking if the 'Price' value in each book's dictionary is greater than the given 
        price. A new 'bookData' object is initialised with the filtered books to preserve 
        the original database. If 'show' is True, the filtered books are printed in a 
        formatted table using the 'printAllBooks()' method.

        Parameters:
            price (numeric): The price threshold used to filter books by.
            show (boolean): A flag specifying whether the filtered results should be printed.

        Raises:
            TypeError: If 'price' is not an integer or float.

        Returns:
            new_obj: bookData object for the filtered data, to allow method chaining. 

        Example:
            >>> demo = bookData()
            >>> demo.printOverPrice(15.99)
            --------------------------------------------------------------
            | ISBN                | Title    | Author        | Price (£) |
            --------------------------------------------------------------
            | 853-0-099-54321-6   | Demo-01  | Author A      |     16.00 |
            | 853-0-099-12345-6   | Demo-02  | Author B      |     25.00 |
            --------------------------------------------------------------

        """

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        filtered_books = [book for book in self.books if book['Price'] > price]
        
        new_obj = bookData(filtered_books)
        
        if show:
            new_obj.printAllBooks()
        return new_obj


    def printAllBooksSorted(self, sortedBy, reverse_param=False, show=True, limit=None):

        """
        This method prints all books in the database, sorted by the given parameter.

        The method sorts 'self.books' by the specified parameter ('Price', 'Title', 
        or 'Author'), using Python's built-in 'sorted()' function. The method is case 
        insensitive as it converts the given 'sortedBy' value to lower case. It creates a new 
        'bookData' object with the sorted books to preserve the original order in 'self.books'.
        If 'show' is True, the sorted books are printed using the 'printAllBooks()' method.

        Parameters:
            sortedBy (str): The paramter to sort by ('Price', 'Title', or 'Author').
            reverse_param (bool): Whether to sort in ascending or descending order, default
            is ascending.
            show (bool): Whether to print the sorted books, default is to print. 

        Raises:
            ValueError: If the given 'sortedBy' value is not one of 'title', 'price', 'author'. 

        Returns:
            new_obj: bookData object containing the sorted books, to allow method chaining.

        Example:
            >>> demo = bookData()
            >>> demo.printAllBooksSorted('Price', limit=2)
            --------------------------------------------------------------
            | ISBN                | Title    | Author        | Price (£) |
            --------------------------------------------------------------
            | 853-0-099-54321-6   | Demo-01  | Author A      |     16.00 |
            | 853-0-099-12345-6   | Demo-02  | Author B      |     45.00 |
            --------------------------------------------------------------
            
        """

        sortedBy_lower = sortedBy.lower()
        if sortedBy_lower not in ['price', 'title', 'author']:
            raise ValueError(f"'{sortedBy}' must be one of 'Price', 'Title', or 'Author'.")

        sorted_books = sorted(self.books, key=lambda x: x[sortedBy], reverse=reverse_param)

        if limit is not None:
            sorted_books = sorted_books[:limit]

        new_obj = bookData(sorted_books)
        if show:
            new_obj.printAllBooks()
        return new_obj



class commentData:

    """This class implements functions that get information about comments.

    Attributes
    ----------
    comments (list of dictionaries): The comments data loaded from a url.

    """
    
    def __init__(self, comments):
        """
        Initialise the class with a the JSON data.
        """
        self.comments = comments
        

    def printAllComments(self, wrap_width=24, preview_only=False, limit=None):
        """
        Prints all comments in a neatly formatted table with wrapped text, ensuring all 
        table borders are consistent.

        This method sets column widths, allowing the 'Comment' column width to be specified
        by the user. The table header is set using formatted strings, left aligning text and
        separating columns with '|' characters. A separator line ('-' characters)is used to
        separate the header and contents. The helperClass method 'wrap_text()' is called on 
        each column to ensure the text is wrapped for each row. If a comment's contents spans 
        multiple lines, the method ensures that all rows stay aligned by padding shorter 
        contents with empty strings.

        In order for this method to print comments out in a neatly formatted table, a minimum
        screen width is needed. The screen must be able to display at least 91 character spaces 
        horizontally. If the pane is less than this width, the formatting will be messy. 

        Parameters:
            wrap_width (int): The width to wrap the contents of the 'Comment' column by, default
            is 32.

        Raises:
            TypeError: If 'wrap_width' is not an integer. 

        Returns:
            None.

        Example:
            >>> demo = commentData()
            >>> demo.printAllComments(wrap_width=40)
            ------------------------------------------------------------------------------------
            | ID  | Post ID | Name           | Email          | Comment                        |
            ------------------------------------------------------------------------------------
            | 1   | 1       | Some User      | user@email.com | This is a comments will wrap   |
            |     |         |                |                | when this function is called.  | 
            ------------------------------------------------------------------------------------
        
        """
        # Check the keys in the data
        comment_vars = self.comments[0].keys()

        post_info_flag = False

        if len(comment_vars) > 5:
            post_info_width = 16
            post_info_flag = True

        if not isinstance(wrap_width, int):
            raise TypeError(f"'{wrap_width}' must be an integer.")
    
        # Set column widths
        id_width = 3
        post_id_width = 7
        name_width = 10
        email_width = 12
        body_width = wrap_width

        # Table header
        header = (
            f"| {'ID':<{id_width}} | {'Post ID':<{post_id_width}} | "
            f"{'Name':<{name_width}} | {'Email':<{email_width}} | {'Body':<{body_width}} |"
        )
        if post_info_flag:
            header += f" {'Post Info':<{post_info_width}} |" 
        separator = "-" * len(header)

        print(separator)
        print(header)
        print(separator)

        # Reduce number of comments if a limit is given
        comments_to_process = self.comments[:limit] if limit else self.comments
        
        for comment in comments_to_process:
            # Use .get to handle cases with missing data
            email_lines = helperClass.wrap_text(comment.get('email', ''), email_width)

            # Check if preview is specified
            if preview_only:
                name_text = helperClass.preview_limit(comment.get('name', ''), max_length=16)
                body_text = helperClass.preview_limit(comment.get('body', ''), max_length=26)
            else:
                name_text = comment.get('name', '')
                body_text = comment.get('body', '')

            name_lines = helperClass.wrap_text(name_text, name_width)
            body_lines = helperClass.wrap_text(body_text, body_width)

            post_info_lines = helperClass.wrap_text(comment.get('post_info', ''), post_info_width) if post_info_flag else []

            # Find column with the most rows (elements from respective list)
            max_lines = max(len(name_lines), len(email_lines), len(body_lines), len(post_info_lines))

            # Add empty lines to columns with less lines per comment to ensure they align
            name_lines += [""] * (max_lines - len(name_lines))
            email_lines += [""] * (max_lines - len(email_lines))
            body_lines += [""] * (max_lines - len(body_lines))
            post_info_lines += [""] * (max_lines - len(post_info_lines))

            # Print table rows
            for i in range(max_lines):
                # For first rows per comment set value, else print empty lines
                id_col = f"{comment['id']:<{id_width}}" if i == 0 else " " * id_width
                post_id_col = f"{comment['postId']:<{post_id_width}}" if i == 0 else " " * post_id_width
                # Set each line from line lists
                name_col = name_lines[i]
                email_col = email_lines[i]
                body_col = body_lines[i]
                post_info_col = post_info_lines[i] if post_info_flag else ""

                # Print results for all comments
                row = f"| {id_col} | {post_id_col} | {name_col:<{name_width}} | {email_col:<{email_width}} | {body_col:<{body_width}} |"
                if post_info_flag:
                    row += f" {post_info_col:<{post_info_width}} |"
                print(row)
            print(separator)


    def printByVar(self, var, value, show=True, preview_only=False):

        """
        This method prints the details of a comment matching with a value matching the
        chosen variable.

        The method loops through all comments in the database, checking if the comment
        value, from the specified variable, 'var', matches the 'value' given as input. 
        Different logic is applied for string values and integer values, allowing 
        users to search across all variables in a given dictionary with one method. If any matches
        are found between the values in the database and the given 'value', they are added to a
        list, which will be used to initialise a new commentData object. The 'printAllComments'
        method is then used to print the filtered comments.
        
        Parameters:
            var (int or string): The variable to search within.
            value (int or string): The value to be searched for, within the given variable.
            show (bool, optional): A boolean specifying whether to print results or not,
            default=True.

        Raises:
            ValueError: If 'var' is not a variable that can be searched, i.e. not a valid key.

        Returns:
            new_obj or self: A commentData object. 

        Example:
            >>> demo = commentData(demo_data)
            >>> demo.printByVar('postId', 10)
            ------------------------------------------------------------------------------------
            | ID  | Post ID | Name           | Email          | Comment                        |
            ------------------------------------------------------------------------------------
            | 1   | 10      | Some User      | user@email.com | This comment will wrap when    |
            |     |         |                |                | this function is called.       | 
            ------------------------------------------------------------------------------------
        
        """

        # Find the keys from the comment dictionaries
        comment_vars = self.comments[0].keys()

        # Join for a more readable ValueError message
        valid_vars = ", ".join(comment_vars)

        # Validation check
        if var not in comment_vars: 
            raise ValueError(f"'{var}' is not a variable that can be searched, expected one of '{valid_vars}'.")

        filtered_comments = []

        # Find the value corresponding to given var
        for comment in self.comments:
            comment_value = comment.get(var)

            # Check if value matches for string or integer
            if isinstance(comment_value, str) and value.lower() in comment_value.lower(): 
                filtered_comments.append(comment)
            elif isinstance(comment_value, (int, float)) and comment_value == value:  
                filtered_comments.append(comment)

        # Create new object if any matches found
        if filtered_comments:
            new_obj = commentData(filtered_comments)
            if show:
                if preview_only:
                    new_obj.printAllComments(preview_only=True)
                else:
                    new_obj.printAllComments()
            return new_obj
            
        else:
            print(f"No comments found with '{var}' matching '{value}'.")
            return self

            
    def printOverVar(self, var, value, show=True, preview_only=False, limit=None):

        """
        This method filters and prints comments where a given numeric variable is greater than
        a  value in the dataset.
        
        This method checks that the specified variable is numeric (e.g., 'id', 'postId'), and 
        filters the comment list to include only those where the variable's value is greater than
        the given threshold. If 'show' is True, the results are printed using 'printAllComments'. 
        If no comments meet the criteria, a message is printed instead.

        Parameters:
            var (str): The name of the variable to filter by. Must be a number.
            value (int or float): The threshold value to compare against.
            show (bool): Whether to print the filtered results. Default is True.

        Raises:
            ValueError: If 'var' is not a numeric variable that can be used for comparison.

        Returns:
            commentData: A new commentData object containing only the filtered comments 
            (if any), enabling method chaining or further analysis. If no comments match, 
            nothing is returned.

        Example:
            >>> demo = commentData(comments)
            >>> demo.printOverVar('postId', 50)
            -------------------------------------------------------------------------------
            | ID | Post ID | Name         | Email        | Comment                        |
            -------------------------------------------------------------------------------
            |  7 |     51  | Jane Doe     | jane@...     | Ut enim ad minim veniam...     |
            
        """
        
        # Extract the keys that contain numeric values
        num_vars = [num for num in self.comments[0].keys()
        if isinstance(self.comments[0][num], (int, float))]

        valid_vars = ", ".join(num_vars)

        if var not in num_vars:
            raise ValueError(f"'{var}' is not a variable that can be used, expected one of {valid_vars}.")

        filtered_comments = []

        for comment in self.comments:
            comment_value = comment.get(var)

            if comment_value > value:
                filtered_comments.append(comment)

        if limit is not None:
            filtered_comments = filtered_comments[:limit]
                
        if filtered_comments:
            new_obj = commentData(filtered_comments)
            if show:
                if preview_only:
                    new_obj.printAllComments(preview_only=True)
                else:
                    new_obj.printAllComments()
            return new_obj

        else:
            print(f"No comments found with {var} greater than {value}.")

            

    def printCommentsSorted(self, sortVar, reverse_param=False, show=True, preview_only=False, limit=None):
        """
        This method sorts comments by a specified variable.

        This method sorts the list of comment dictionaries by the value of the given variable 
        (excluding 'body', which is often too long for useful sorting). The sort can be in 
        ascending or descending order depending on 'reverse_param'. If 'show' is True, the 
        sorted comments are displayed in a formatted table using the 'printAllComments' method.

        Parameters:
            sortVar (str): The variable to sort by (e.g., 'id', 'postId', 'name', or 'email').
            reverse_param (bool): Whether to sort in descending order. Default is False (ascending).
            show (bool): Whether to print the sorted comments. Default is True.

        Raises:
            ValueError: If 'sortVar' is not a valid field for sorting.

        Returns:
            new_obj (commentData): A new commentData object containing the sorted comments, 
            allowing for method chaining.

        Example:
            >>> demo = commentData(comments)
            >>> demo.printCommentsSorted('name')
            -------------------------------------------------------------------------------
            | ID | Post ID | Name         | Email        | Comment                        |
            -------------------------------------------------------------------------------
            |  1 |    101  | Alice Smith  | alice@...    | Lorem ipsum dolor sit amet... |
            |  2 |    102  | Bob Johnson  | bob@...      | Consectetur adipiscing elit... |
        """

        sort_vars = [var for var in self.comments[0].keys() if var != 'body']

        valid_vars = ", ".join(sort_vars)

        if sortVar not in sort_vars:
            raise ValueError(f"'{sortVar}' is not a variable that can be used for sorting, expected one of {valid_vars}.")

        # Apply sorting function
        sorted_comments = sorted(self.comments, key=lambda x: x[sortVar], reverse=reverse_param)

        if limit is not None:
            sorted_comments = sorted_comments[:limit]

        new_obj = commentData(sorted_comments)
        if show:
            if preview_only:
                new_obj.printAllComments(preview_only=True)
            else:
                new_obj.printAllComments() 
        return new_obj
        

    def add_field(self, show=False, preview_only=True, limit_field=None):
        """
        This method adds a new field 'post_info' to each comment in the existing data.

        This method cehcks whether the field 'post_info' already exists. If not, it 
        generates and appends formatted timestamp and IP address information to each 
        comment in 'self.comments'. It uses the helper methods 'gen_rand_time', 
        'gen_rand_date', and 'gen_rand_ip' to do so. 

        Parameters:
            show (bool, optional): Whether to display the updated comments on screen.
                Default is not to print results. 
            preview_only (bool, optional): If 'True' the data that is printed is shortened 
                give a preview rather than full printed data set. Default is to preview the data.
            limit_field (int, optional): This restricts the number of commments displayed
                to the user when 'show=True'. Default is no restriction. 

        Raises:
            None

        Returns:
            self: The updated instance of the class with the modified, updated comment data. 

        Example:
             >>> instance.add_field(show=False, preview_only=True, limit_field=5)
        """
        
        # Find the keys from the comment dictionaries
        comment_vars = self.comments[0].keys()
        post_info = 'post_info'

        # Check if post info col already exists
        if post_info in comment_vars:
            pass
        else:
            for item in self.comments:
    
                # Generate info
                time = helperClass.gen_rand_time()
                date = helperClass.gen_rand_date()
                ip = helperClass.gen_rand_ip()

                # Add new field
                item['post_info'] = f"Time: {time}\nDate: {date}\nIP address: {ip}"
            
            if show:
                if preview_only:
                    self.printAllComments(wrap_width=11, preview_only=True, limit=limit_field)
                else:
                    self.printAllComments(limit=limit_field)
            return self




    




                

        
          
                






        
