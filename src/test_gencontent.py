import unittest

from gencontent import extract_title


class TestGenContent(unittest.TestCase):
    def test_easy_header(self):
        md = """# Hello """
        test_1 = extract_title(md)
        test_2 = "Hello"
        self.assertEqual(test_1, test_2)

    def test_practical_header(self):
        md = """
# This is a heading 

``` 
This is a code block beep boop 
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

> This is a quote

- This is an unordered list
- with items

1. This is an ordered list
2. with items 
"""
        test_1 = extract_title(md)
        test_2 = "This is a heading"
        self.assertEqual(test_1, test_2)

    def test_no_header(self):
        with self.assertRaisesRegex(Exception, "No valid header found"):
            md = """
This is a heading 

``` 
This is a code block beep boop 
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
            return extract_title(md)

    def test_invalid_header_format(self):
        with self.assertRaisesRegex(Exception, "No valid header found"):
            md = """
#This is a heading 

``` 
This is a code block beep boop 
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
            return extract_title(md)
