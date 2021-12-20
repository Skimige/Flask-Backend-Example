import requests
import time

base_url = 'http://127.0.0.1:80/'


def login(user: dict):
    r = requests.get(url=base_url + 'login', params=user)
    r_data = r.json()
    return r_data['access_token']


# Login
admin = {
    'username': '__ADMIN_USERNAME__',
    'password': '__ADMIN_PASSWORD__'
}
user = {
    'username': '__USER_USERNAME__',
    'password': '__USER_PASSWORD__'
}

ak_admin = login(admin)
ak_user = login(user)

headers_admin = {
    'Authorization': 'Bearer ' + ak_admin
}
headers_user = {
    'Authorization': 'Bearer ' + ak_user
}

# Tests
print('\nAdmin: Get user list')
user_list = requests.get(url=base_url + 'users', headers=headers_admin)
print(user_list.json())

print('\nAdmin: Get per user')
user_per_from_admin = requests.get(url=base_url + 'users/1', headers=headers_admin)
print(user_per_from_admin.json())

print('\nUser: Get per user')
user_per_from_user = requests.get(url=base_url + 'users/1', headers=headers_user)
print(user_per_from_user.json())

print('\nUser: Get books')
books = requests.get(url=base_url + 'books', headers=headers_user)
print(books.json())

# print('\nAdmin: Add book')
# new_book = {
#     'name': '乔布斯传',
#     'description': '记叙史蒂夫·乔布斯的一生',
#     'status': 'available'
# }
# books = requests.post(url=base_url + 'books', headers=headers_admin, data=new_book)
# print(books.json())
#
# print('\nAdmin: Remove book')
# remove_book = requests.delete(url=base_url + 'books/2', headers=headers_admin)
# print(remove_book.json())

print('\nCheck Book')
book_borrow_query = requests.get(url=base_url + 'books/borrow/2', headers=headers_admin)
print(book_borrow_query.json())

print('\nBorrow Book')
book_borrow_action = requests.post(url=base_url + 'books/borrow/2', headers=headers_admin)
print(book_borrow_action.json())

print('\nSleep for 10s...')
time.sleep(10)

print('\nReturn Book')
book_return_action = requests.post(url=base_url + 'books/return/2', headers=headers_admin)
print(book_return_action.json())
