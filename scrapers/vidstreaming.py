from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import json,requests
from base64 import b64encode, b64decode
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs






USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

ENCRYPT_AJAX_REQUEST_HEADERS = {
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': USER_AGENT,
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Gpc': '1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': '',
}


keys = {
    "key1": b"37911490979715163134003223491201",
    "key2": b"54674138327930866480207815084989",
    "iv": b"3134003223491201"
}



def create_remaining_params(ciphertext, key, iv):

    # Convert key and iv to bytes
   # key = key.ljust(32, b'\0')[:32]
   # iv = iv.ljust(16, b'\0')[:16]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_data.rstrip(b'\0').decode('utf-8')







def extract_vidstreaming_url(full_html):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(full_html, 'html.parser')

    # Find the div tag with the specified attributes
    play_video_tag = soup.find('div', {'class':'play-video'})

    # Extract the src attribute from the iframe
    src_content = BeautifulSoup(str(play_video_tag),'html.parser').find('iframe').get('src')

    return src_content




def extract_vidstreaming_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Get the query parameters from the URL
    query_params = parse_qs(parsed_url.query)

    # Get the value of the 'id' parameter
    id_value = query_params.get('id', [])[0] if 'id' in query_params else None

    return id_value





def extract_episode_script(full_html):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(full_html, 'html.parser')

    # Find the script tag with the specified attributes
    script_tag = soup.find('script', {'data-name': 'episode', 'type': 'text/javascript'})

    # Extract the value attribute from the script tag
    script_content = script_tag.get('data-value')

    return script_content



def create_encrypted_key(data, key, iv):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return b64encode(ciphertext).decode('utf-8')












def decrypt_encrypt_ajax_response(data, key, iv):
    # Convert the base64-encoded data to bytes
    data_bytes = b64decode(data)


    # Create an AES cipher with CBC mode and PKCS7 padding
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted = decryptor.update(data_bytes) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted) + unpadder.finalize()

    # Convert the decrypted bytes to a UTF-8 string
    decrypted_str = unpadded_data.decode('utf-8')

    # Parse the decrypted string as JSON

    return decrypted_str





'''
# Example usage:
encrypted_data = "w89bNzwCrlGHreXFIaZoZhZLmUoDYVdPoNGEznAPg8DjvgU6jYrnVtjCvxmIIODzTFHCjHwOr90Pi+t9rr7jJibVAQxwekikfDwnROf51Qi3kKC86AbQq8tiffWSF\/q3jS2\/ibpEegtHTxR\/GMrmz7eYU8ymmiIbx576NvFgduC3An9IqWlHT0uGxC5BjbBYgoTzivvmzTlcTRlvM82hG2QevRtjqqBKWe1csI9T8sIvXL81RUErexh6i5pVdkwGi0yYVJ0+qW8WQ4K7UD0f4\/m8iVcLWn0UkKOVJ7WJL6R7X7E5An2dByqGLhprSEZ\/AC5nrK072JKEU3N0YgBl6fkRyZrmdT1C4R4akA\/k3L\/m8\/2p97gBvygRbzH++prUTHUUGhJcAjDVmrRAY\/td2twgogGXA\/x9yMpfG7+peMYVwAgBHpZCpOUJOO6x3TiC5bK0abGVRh4yo0XaRdKSuJeakYZ8eXg1SC6k1z6Dnw1n+GQDjzuU4tLovM6mR\/6Swp4Vebz0zmShMqTJQFrPbD+3uIYxtF4YihM6mIhiyZaYLgZlTk6azyemZckQavMl"  # Replace with your actual encrypted data
encryption_key = b"54674138327930866480207815084989"  # Replace with your actual encryption key
iv_real = b"3134003223491201"  # Replace with your actual initialization vector

result = decrypt_encrypt_ajax_response(encrypted_data, keys["key2"],keys["iv"])

'''


'''
# Input values
data = "MjUwNTQ="
script = '6U5HfTjysX9yNBo9HikOfOO4ObGAnXfQIAMCFRTLRnyhXLoAP6scvb0OXyNsSnRCAMS0omots3H5NANiij411Xv2EVcuh5z8/c3Plpi3lcfseKZrSlQblEmJxZ0ZQlDM13f/AmHE2/yYdvA5gPq9e8vHWigsFgEYPG/b8nvD1lR7O3sIlxQqZXqWzHlViwh/QpNnBaQL+1FxL7+CMcSgkQ=='
key = b'37911490979715163134003223491201'
iv = b'3134003223491201'
'''



'''
# Encrypt the data
encrypted_key = create_encrypted_key(data, key, iv)

#print(f"Encrypted Key: {encrypted_key}")
'''


'''
# Decode base64 and decrypt the script
decoded_script = b64decode(script)
decrypted_token = create_remaining_params(decoded_script, key, iv)

#print(f"Decrypted Token: {decrypted_token}")

'''



'''

streaming_page_data=requests.get("https://goone.pro/streaming.php?id=MjUwNTQ=&title=Naruto+Episode+1&typesub=SUB").text

test_encrypted_key = create_encrypted_key(data, key, iv)

print()




t_full_partams=create_remaining_params(b64decode(extract_episode_script(streaming_page_data)), key, iv)

final_url=f"https://goone.pro/encrypt-ajax.php?id={test_encrypted_key}&alias={t_full_partams}"



headers = {
    'Host': 'goone.pro',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': USER_AGENT,
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Gpc': '1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://goone.pro/streaming.php?id=MjUwNTQ=&title=Naruto+Episode+1&typesub=SUB',
}
t_ajax_resp=requests.get(final_url,headers=headers).text

print()
dcdt=json.loads(t_ajax_resp)["data"]
print(dcdt)
result = str(decrypt_encrypt_ajax_response(dcdt, encryption_key, iv_real)).replace('\\',"")
print(result)


'''