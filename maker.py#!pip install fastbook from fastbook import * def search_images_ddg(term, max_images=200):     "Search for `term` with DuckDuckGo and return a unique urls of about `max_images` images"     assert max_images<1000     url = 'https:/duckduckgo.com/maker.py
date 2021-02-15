!pip install fastbook
from fastbook import *
def search_images_ddg(term, max_images=200):
    "Search for `term` with DuckDuckGo and return a unique urls of about `max_images` images"
    assert max_images<1000
    url = 'https://duckduckgo.com/'
    res = urlread(url,data={'q':term})
    searchObj = re.search(r'vqd=([\d-]+)\&', res)
    assert searchObj
    requestUrl = url + 'i.js'
    params = dict(l='us-en', o='json', q=term, vqd=searchObj.group(1), f=',,,', p='1', v7exp='a')
    urls,data = set(),{'next':1}
    while len(urls)<max_images and 'next' in data:
        try:
            data = urljson(requestUrl,data=params)
            urls.update(L(data['results']).itemgot('image'))
            requestUrl = url + data['next']
        except (URLError,HTTPError): pass
        time.sleep(0.2)
    return L(urls)
   
def dataset_maker(sort_data,path):
  bear_types = sort_data
  path = Path(path)
  if not path.exists():
      path.mkdir()
      for o in bear_types:
          dest = (path/o)
          dest.mkdir(exist_ok=True)
          results = search_images_ddg(f'{o}')
          download_images(dest, urls=results)
  fns = get_image_files(path)
  failed = verify_images(fns)
  failed.map(Path.unlink)
  list_not_found = [file  for child in path.iterdir() for file in child.iterdir()]
  list_to_unlink = [set(list_not_found)-set(fns)]
  for file in list_to_unlink:
    Path.unlink(file)
  fns = get_image_files(path)
  for file in fns:
    file.rename(file.with_suffix('.jpg'))
  print('Your dataset did')   
