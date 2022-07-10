# -- coding: utf-8 --
"""
@Time : 2022/7/9 9:41
@Author : Zijie.XIANG
@Description : Extract the images from some external sources
"""
import os

import requests
import zipfile


def main():
    if not os.path.exists('./pipeline_data'):
        os.mkdir('./pipeline_data')
    if not os.path.exists('./pipeline_data/images.zip'):
        # mock the request, info obtained from F12 -> network
        dataset_url = 'https://storage.googleapis.com/kaggle-data-sets/739747/1281826/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com@kaggle-161607.iam.gserviceaccount.com/20220710/auto/storage/goog4_request&X-Goog-Date=20220710T111520Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=3b18850fbd7a82bd95d920a55c625d3d7230fa5f59680016eb7afa251e590654f8c1f3349d100acfce4d1ad742536e4da46e05859cb28cbd2a381a084d71ea9a0b60b5ae17abcb15f6eee00e4692c66aa506d7975e509b4d75828b64c72296edef61b0408153f22d2c8ae669c86c94666bd4489ed6a3a0b689366bdb8728bbb77db3b97580578853e8692712d6b4eb89f8575bc1cd2e7804299959fbed815aeda6031dbfd1a28b784949bb8efdfb44e638c9d7e91009464f25b8fd7a18c57d176301fa2209fba2b200e15e7766153a4c3cd8b9459581d74e73de892b67c56090be3556232fa5df9c9c0b8c47443c201c272a8454c6fa034761ba1183691d87f8'
        HEADERS = {
            'authority': 'storage.googleapis.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en-AU;q=0.8,en;q=0.7',
            'referer': 'https://www.kaggle.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"103.0.5060.114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-client-data': 'CJC2yQEIprbJAQjEtskBCKmdygEIpNPKAQiWocsBCIO7zAEIg7zMAQjvvMwB'
        }
        resp = requests.get(dataset_url, headers=HEADERS, stream=True)
        with open('./pipeline_data/images.zip', 'wb') as file:
            for idx, chunk in enumerate(resp.iter_content(chunk_size=128)):
                file.write(chunk)

        # Unzip the data
        zip_file = zipfile.ZipFile('./pipeline_data/images.zip', 'r')
        for inner in zip_file.namelist():
            zip_file.extract(inner, './pipeline_data/images')


if __name__ == '__main__':
    main()