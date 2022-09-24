# Library management

The Webapp is built using Python Framework Django which contains various functionalities like add book, borrow book, return book etc.
## Introduction
The project uses Django as a backend framework and also uses Html, Css and bootstrap for styling of web pages.
## Installation and Running

To run this project first make a virtual enviroment , activate it and install requirement libraries present in requirement.txt file

creating and acitvating virtual environment
```bash
  python3 -m venv env
  source venv/bin/activate
```
change directory
```bash
  cd backend
```
Installing required libraries for the project
```bash
  pip install -r requirement.txt
```
To run the server
```bash
  python manage.py runserver
```
To open page 
```bash
  cd frontend
```
Then open login.html page.
## Functionalites

- Anyone (include anonymous), can check what book is in the library, and if they are available for borrowing
- Student: a. Check what books he/she has borrowed, If a book hasn't been renewed yet, the student can renew it see a history of borrowed books 
- Librarian: a. Can see which student borrowed which book, history of borrowing, etc b. Can mark a student borrowed a book c. Can mark a student returned a book 