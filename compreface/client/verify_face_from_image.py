"""
    Copyright(c) 2021 the original author or authors

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https: // www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
    or implied. See the License for the specific language governing
    permissions and limitations under the License.
 """

from compreface.common.multipart_constructor import multipart_constructor_with_two_images
import requests
from compreface.config.api_list import VERIFICATION_API
from compreface.common.typed_dict import ExpandedOptionsDict, check_fields_by_name
from compreface.common.client import ClientRequest


class VerifyFaceFromImageClient(ClientRequest):
    """
        Verify face in image. It uses source and target images for encode and send to CompreFace 
        server with validation by image id.
    """

    def __init__(self, api_key: str, domain: str, port: str):
        super().__init__()
        self.client_url: str = VERIFICATION_API
        self.api_key: str = api_key
        self.url: str = domain + ':' + port + self.client_url

    def get(self):
        pass

    """
        POST request for verify face in image using source and target images. 
        
        :param source_image: Path to source image in file system.
        :param target_image: Path to target image in file system.
        :param image_id: subject id from previously added image. 
        :param options: dictionary with options for server.
        
        :return: json from server.
    """

    def post(self,
             source_image: str = '' or bytes,
             target_image: str = '' or bytes,
             options: ExpandedOptionsDict = {}) -> dict:

        url: str = self.url + '/verify?'
        # Validation loop and adding fields to the url.
        for key in options.keys():
            # Checks fields with necessary rules.
            # key - key field by options.
            check_fields_by_name(key, options[key])
            url += '&' + key + "=" + str(options[key])

        # Encoding image from path and encode in multipart for sending to the server.
        m = multipart_constructor_with_two_images(source_image, target_image)

        # Sending encode image for verify face.
        result = requests.post(url, data=m, headers={'Content-Type': m.content_type,
                                                     'x-api-key': self.api_key})
        return result.json()

    def put(self):
        pass

    def delete(self):
        pass