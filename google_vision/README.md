# Google APIs for Vision, Translation and Geocoding 
[Colab notebook](https://drive.google.com/file/d/1CO9k589Mbwqz3sBMBSutoSXIarYH4NCP/view?usp=sharing)

Haverford College Digital Scholarship has an account with Google Cloud.  If you would like to manage this account and the API keys, go to [console.cloud.google.com](console.cloud.google.com).

With the DS API key, you can access any of the enabled APIs, including
- Google Translate API
- Google Cloud Vision API
- Google Natural Language API
- Google Cloud Speech API

## Here is a sample function for extracting text from jpg files.  
```python
def vision_ocr(path, filename, language):
    '''A function to send a single jpg (<4mb) to the Vision API for text extraction.  
    param: path, the location of the file
           filename, the name of the file
           language of the text ('es', 'en'...), can be detected automatically, but is often incorrect. 
           API_KEY is the Google API key from console.cloud.google.com
    returns: full text from the images.  Note that the results also include each word, paragraph and text block identified with    
    coordinates for a bounding box. 
    '''
    
    service = googleapiclient.discovery.build('vision', 'v1', developerKey=API_KEY)
        language = language
        with open(path + filename, 'rb') as image:
                image_content = base64.b64encode(image.read())
                service_request = service.images().annotate(body={
                        'requests': [{
                                       'image': {
                                       'content': image_content.decode('UTF-8')
                                        },
                                       
                                       'imageContext': {
                                           'languageHints': [language]},
                                       'features': [{
                                           'type': 'TEXT_DETECTION'
                                        }]
                                    }]
                })
                response = service_request.execute()

                if 'error' in response['responses'][0]:
                        print('[*] error %s' % file)
                        pass

                else:
                        try:
                            text = response['responses'][0]['textAnnotations'][0]['description']
                            text = text.encode('utf-8')
                        except:
                            text = ''
                            text = text.encode('utf-8')
                        return text
 ```
 
 Please note that the files need to be less than 4mb.  If your files are too large, here is an effective solution.
 
 
 ```python
 #https://stackoverflow.com/questions/13407717/python-image-library-pil-how-to-compress-image-into-desired-file-size
class file_counter(object):
    def __init__(self):
        self.position = self.size = 0

    def seek(self, offset, whence=0):
        if whence == 1:
            offset += self.position
        elif whence == 2:
            offset += self.size
        self.position = min(offset, self.size)

    def tell(self):
        return self.position

    def write(self, string):
        self.position += len(string)
        self.size = max(self.size, self.position)

def smaller_than(im, size, guess=70, subsampling=1, low=1, high=100):
    while low < high:
        counter = file_counter()
        im.save(counter, format='JPEG', subsampling=subsampling, quality=guess)
        if counter.size < size:
            low = guess
        else:
            high = guess - 1
        guess = (low + high + 1) // 2
    return low

def change_size_if_needed(file):
    if os.path.getsize(file) > 4000000:
        im = Image.open(file)
        size = smaller_than(im,4000000)
        im.save(file, 'JPEG', quality=size)```
