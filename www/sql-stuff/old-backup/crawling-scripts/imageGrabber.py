import requests
item = ['https://m.media-amazon.com/images/I/71JFT44OhnL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/61YciR5MYmL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1fEooigMCL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/91Xe8LC3hSL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/917OTaZsNhL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1hvK1Mi7dL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71dIfJyz+9L._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81obuKhRAsL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/61HrF-Z7ChL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81xc6+rPyOL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71vwVWYC8NL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81bKGD4wY5L._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1r8wvZcibL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81mirmwnASL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/61Wnc3mJyqL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/91+4nHGV4NL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/61oBBtrcUzL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1BR0wUbEZL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/916CpEniqUL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/918uEKIaCXL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/51Vnd4g0MXL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1W9YmeDKmL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71+QwShxzbL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/51KfiPiQvwL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/7191oE5luUL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81IqTEbQpQL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/61mnFaK4LfL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71bnFMEYbKL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1apLbwJSgL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/91efsGAg2hL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/615wihaQq2L._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/91FL1fgnJAL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/51qRpHymdkL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71Ai3X7IbJL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81xoFYlxx-L._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/A1t05PQW0WL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81i8bINKoaL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/71D5TRDWCwL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81A3AHe1PfL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/91j47E0mMKL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/81m9q59YeRL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/716xYSST0LL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/810hDJsW+rL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/516Fds4dqLL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/51qqLBPhcDL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/817eqfF4IIL._AC_UL320_ML3_.jpg', 'https://m.media-amazon.com/images/I/412S1EMkPgL._AC_UL320_ML3_.jpg']

















currentNumber = 1780
for x in range(1, len(item)):
    with open(str(currentNumber+x)+'.jpg', 'wb') as f:
        f.write(requests.get(item[x]).content)