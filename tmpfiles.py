import os
import requests

def upload_data():
    image_list = os.listdir("outputs/edit_results")
    res = {}
    for i in range(len(image_list)):
        if image_list[i][-3:] == "png":
            path = "outputs/edit_results/" + image_list[i]
            files = {
                'file': open(path, 'rb'),
            }
            
            response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
            res['image'] = response.json()['data']['url']

    sample_name_list = os.listdir('outputs/edit_results/samples/images')
    sample_url_list = []

    for i in range(len(sample_name_list)):
        
        path = 'outputs/edit_results/samples/images/' + sample_name_list[i]
        files = {
            'file': open(path, 'rb'),
        }
        
        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)

        sample_url_list.append(response.json()['data']['url'])

    res['samples'] = sample_url_list

    return res