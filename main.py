import requests, filetype, os
if not os.path.exists('viruses'):
    os.mkdir('viruses')
api_key = '<KEY>'
viruses = []
print('Getting samples ...')
for virus in requests.get(f'https://malshare.com/api.php?api_key={api_key}&action=getlist').json():
    viruses.append(virus['sha256'])
for virus in viruses:
    with open(f'viruses/{viruses.index(virus)}', 'wb') as file:
        connection = requests.get(f'https://malshare.com/api.php?api_key={api_key}&action=getfile&hash={virus}', stream=True)
        connection.raise_for_status()
        for chunk in connection.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)
    type = filetype.guess(f'viruses/{viruses.index(virus)}')
    if type:
        os.rename(f'viruses/{viruses.index(virus)}', f'viruses/{viruses.index(virus)}.{type.extension}')
    print(f'№{viruses.index(virus)} - Downloaded!')
