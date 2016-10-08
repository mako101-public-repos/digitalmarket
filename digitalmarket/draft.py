from mimetypes import guess_type

url1 = 'https://s3.amazonaws.com/digital-market-1/media/44/office365.png'

print(guess_type(url1))

url2 = 'http://s3.amazonaws.com/digital-market-1/media/43/Horarios_Malaga-Marbella_est.pdf'

print(guess_type(url2))