# Huong dan su dung

# Setup moi truong (Lan dau tien)

- Cai dat thu vien 

``` batch
    pip install -r requirements.txt
```

- Setup moi truong database

``` python
    python init_database.py 
```

# Setup account va link offer

- Them tai khoan Affilitest (Chi chay lai khi bo sung them tai khoan), tai khoan chua trong file `account/total.txt`

``` python
    python load_account_to_database.py 
```

- Cap nhat link offer (Chi chay moi khi co update them link moi), cap nhat link o file `offer.txt` theo mau sau:
  
```txt
    offer_id,offer_network,offer_link,offer_name,country,device
```

device: iphone, android

``` python
    python update_offer.py 
```

# Run he thong

- Chay auto test link:

```python
    python auto_affilitest.py
```

- Mo them cmd khac va chay trinh quan ly:
  
```python
    python app.py
```
