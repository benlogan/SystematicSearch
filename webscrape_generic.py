import json
import re
import time
import requests

from bibtexparser.model import Field
from bs4 import BeautifulSoup

from parser import parse_file, create_new_lib, save_file

FIELD_DOI = 'doi'
FIELD_ABSTRACT = 'abstract'
FIELD_KEYWORDS = 'keywords'
FIELD_TITLE = 'title'


# use something like https://curlconverter.com/
# to build the cookies and headers, to enable authentication (to IEEE)

cookies = {
    'TS013304a6': '01c1c020dd9c0d3353512ba0b66274673e31000345b919425ceda02047af0d9b9141b8155a33ace1662596bf4df0e4074f79e82e01',
    'TS011ecef4': '01c1c020dd9c0d3353512ba0b66274673e31000345b919425ceda02047af0d9b9141b8155a33ace1662596bf4df0e4074f79e82e01',
    'PF': 'BZGmovWVJldcNPCGQay9zrWmf7XkgxJq8JAtdkk7KbPw',
    'TS01f293bb': '012f350623824afb050395cba78ecac7fe27e8cbedac1041dc2ae7f0b3425f2f628eabb81b288c588bbe50692cd370f349259ea8efd700ef81a918894359cc3684d7b7e9cd',
    'tempuid': '',
    'ieeeUserInfoCookie': '%7B%22userInfoId%22%3A%2299624278%22%2C%22cartItemQty%22%3A0%2C%22name%22%3A%22BEN%20LOGAN%22%2C%22authStatus%22%3A%22success%22%2C%22lastUpdated%22%3A-661872397479518334%2C%22env%22%3A%22pr%22%7D',
    'ieeeSSO': 'ZlEtommRo2JpGWSicZFvM5B4Wf35YTwSWxpfGymsBQfNXbLVldBNRA==',
    'opentoken': 'T1RLAQJ8kXkw1kYYVRitDqB5aAnRWDsJghCjcIavpPkdnNO8SdsQVAXTAACAFhzksuRjdRh-oAAVoz5wUuLCBAB8Q9oSiJ634qvtsd960qu6xfHGbgfERJ6QdwfNEeZ_ZHEk0YlLwSvghBkF5yS2S9lPf_jDBjU4PGfxQQxNouGUG8hM-IYC7BgWCJYqQ5VBjUzQVHHWooiVoQ7meJzRfa48sxyAN5jowWxidi8*',
    'PA.Global_Websession': 'eyJ6aXAiOiJERUYiLCJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2Iiwia2lkIjoiY2ciLCJwaS5zcmkiOiJJTjlqWjgteGRLdno2ejhaR2s5OGRfN1lKSDQuVGtvIn0..i_3jW8sJcW4kflQNwttL9w.jxIX8lBUXHg_oc_J0hEmZV8AtNyP5Cfz5YuThtYHVaLDaKjAZpmqbC50dGj1o3iDtkL3fGpzeCbuoHo45J6b9EYL91cP8pxouZrlEiKxRTU5nmPXsAheSkb_VFyk0ou7nWhfzupddkKBoWZPwMstjcADWzMPw_njEQpBaOi4u7-Hq9CkqsLw13aGC8KzVvMA7GdH9jDuLXAWmYomn3bA07_Y1MtJ4Ea00zRDRglvMdy7TcSHwzjM4sc_GgNnqadZdVOO7PTbMkxGaJKm8M2STFIqpxZoM2-bym2uZOEFVnHVm4L7GdR7vrO_D6TDCR-lHfkYrj79-oLWyFiOASuxemc12vfAq3pZ2yQd7qIl8JL_4wLR74TTNbbEeKKIHljB7mNlUl64jL6-Y0XOMoOHkR6NxfM4527o3-hUwUkAHcQUxRgqEhJrZ7W9WUBAQzU3KmWIsm_w3U_W2at0VmngtQ.blEXmVGJ4qayxpErTdKYYA',
    'TS01797c2d': '012f3506231b7bd60b003ab9a7eb6aa5ce13bafaaae1b31e6bf20659152c5375f58ac17ba70ff8d04022de9a5c31a3fd4c35cdef3d',
    's_ecid': 'MCMID%7C41119512348153149430961847830110833947',
    'AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1',
    's_cc': 'true',
    'osano_consentmanager_uuid': '22e2eecc-45b3-4779-bb9e-c369cc8a5bd4',
    'osano_consentmanager': 'UdrhNX28-wiqdQuhvvt1HCDXDK0uaNAl2JN6ETOC2QO6rDDIzTxQcpc6oMPhBVu0gGey6g8gY8sGk-drOcLsfjRkGyIXrzex3XgV7QBdp-e1eSg3jGWGBGPLwbo8zVORGR3D6pcIOdqI2fhdxwP9C4TCd_nykGU8-dIQCg74f-N-9XuLFpfXlrNJGqRXQ4uxaCoK4ODkxCjA0XCa1szvLoFNbAS_si1LaMlj4Vfz6sV-dvuqsaXkyVY9hlkxypPM3eO5k8Sdox7ouaJfZdgXh-IoXxNUzcteorxyRw==',
    'TS01b03060': '012f350623c8ceaa3d3ea41814ccc28c63d59febbe5871662e26829fd566c2e7270aad933c3b46b18f052320d014a41b3a9eeaafc3',
    'TSaeeec342027': '080f8ceb8aab2000338d9500da429fffe24840ddd37eeced23055926821f3be1fa17b731f482bd1f08a63be1fe113000f0ca6437a29ac0f7b8ca10e6c056dcd08513b1392a6efdd4f336086b0e23b26b119cc43368c1385d092c13abb5959f45',
    'TS0118b72b': '01f15fc87c6ae56813c69e9a258e602ec3207408f6907948b712f8255586de2c87d5fd7185276b95f0f06307f1e257f47520ba00b8',
    'TS010fc0bf': '01f15fc87cbc88d8e71fcaff9c0f800e43033510ac92a3bc218fe1de9331db278790ea141d6e2ecfaf7fa337d3322015dff4d2171b',
    'TS01c3e3fe': '01f15fc87cbc88d8e71fcaff9c0f800e43033510ac92a3bc218fe1de9331db278790ea141d6e2ecfaf7fa337d3322015dff4d2171b',
    's_sq': '%5B%5BB%5D%5D',
    'ipCheck': '134.83.3.184',
    'CloudFront-Key-Pair-Id': 'KBLQQ1K30MUFK',
    'AWSALBAPP-1': '_remove_',
    'AWSALBAPP-2': '_remove_',
    'AWSALBAPP-3': '_remove_',
    'ipList': '"37.205.58.148,82.132.229.201,134.83.3.184"',
    'usbls': '1',
    'hum_ieee_visitor': '88822cce-654a-47ba-8c60-bbdd1633085a',
    'hum_ieee_visitor_matched': 'true',
    'JSESSIONID': '4C4BB54C0914B50B35CFFA8689F31A29',
    'ERIGHTS': 'kW3kLHEqciW1WG9ULrzr0ANDFHmqwHTD*ACpmxxFx2BJDnpktuRV3YNvVAx3Dx3D-18x2dsHfyx2BKdx2FcPlxxCitNDM7HnQx3Dx3DMcsQG2Mt9jdCyoFx2Bff7VGQx3Dx3D-mEjGbp7x2FDleWTLnGjuY1KAx3Dx3D-5f6yx2F5lFOeakMmsg8x2FRRtgx3Dx3D',
    'WLSESSION': '3758191114.47873.0000',
    'TS0154b67f': '012f35062348f6f3c376cd553b86607e78246395d0488eb86d60e13b441c7e6bd53cd2c3f6079f42a5ee45d29145db55bda6868575',
    '_zitok': 'd725a74b342f92c79eea1718098533',
    'TS016349ac': '01f15fc87cdf610c994c69334cbda06de892c3b18df39d76cde73e927076a33956cc167137f4164b4cc1a7e56be7d6a5677e98a6a9',
    'utag_main': 'v_id:018fe3dc2cff002b0908fa126b2c05075003506d00b78',
    'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '359503849%7CMCMID%7C41119512348153149430961847830110833947%7CMCIDTS%7C19886%7CMCAID%7CNONE%7CMCOPTOUT-1718106156s%7CNONE%7CvVersion%7C5.0.1',
    'CloudFront-Policy': 'eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vaWVlZXhwbG9yZS5pZWVlLm9yZy9tZWRpYXN0b3JlL0lFRUUvY29udGVudC9tZWRpYS82NzIwMjI1LzY3MzUwMzIvNjczNTA0OC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzE4MTAwNzU5fSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjEzNC44My4zLjE4NCJ9fX1dfQ__',
    'CloudFront-Signature': 'nx7VUZvinA-lZ-27H4--BVj4JCpHJumT88WXK6875VhhA0Zg-lokG0eEMC~4vfMY29I7I9tw2IozXNWjlVyF0W~3TznKSYC5FLlIkvjiQ84FSx3R-FL2SeOU1z8KsuXGI7thEdnwsbA5RRSePyTpSEX1-S1uFOasO9rvupC5wTTx2pa-58iCEzrAyKzqoPLdU5GPWvyF6-8Sar1aF5YOV~8UaJtEbdj73vekf28wiB~FHSv-tGTX4txg8M1w1IfRhvTgg2brp6pNTBjXnLbrxuwkXyq0iqKeT5QXRjU9XqlMIuVGf-w9HpQVDffJnWoASq0S25hopE1eizm-96ADxQ__',
    'xpluserinfo': 'eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCcnVuZWwgVW5pdmVyc2l0eSIsInByb2R1Y3RzIjoiRUJPT0tTOjE5NzQ6MjAyM3xNSVRQOjE5NDM6MjAyM3xOT1dDU0VDOjIwMTg6MjAxOHxXSUxFWVRFTEVDT006MjAxOToyMDE5fElCTToxODcyOjIwMjB8Tk9XQ1NFQzoyMDE5OjIwMTl8Tk9XQ1NFQzoyMDIwOjIwMjB8QVJURUNIOjIwMjE6MjAyM3xXSUxFWVRFTEVDT006MjAxNToyMDE2fE5PS0lBIEJFTEwgTEFCU3xJU09MNTV8TUNDSVM1fE1DQ0lTNnxNQ0NJUzd8SVNPTDg1fE1DQ0lTOHxNQ0NJUzl8TUlUUF9ESVNDT05USU5VRUR8TUNDSVM0fE1DQ0lTNXxJRUx8VkRFfCJ9',
    'seqId': '17129',
    'AWSALBAPP-0': 'AAAAAAAAAADhK/ywGpQtNZVPsIZ5bArEOS6PTgtO3nI54a0HtTH2O5A/rcHa9utyZ6m9A+MyAwMu/gMdT4kCIYpGOBlXJZX2QdSL1OZ0nhJbEJHLEI8QzGB/W48vAyTzjoYyoF2QEAtPjv+BhRqiycX6lICC+IS2U0iDZuy2U5j3vhayKdvQY41yxB3o7zAjyTonabVBYT4TTBF7tN0rQQ==',
    'TS8b476361027': '0807dc117eab2000bfd9a4df131b406988bbb3fd6a74ee2f640eb5de2a0f861172bccd9cc384b3f808daf00ab6113000ad3cf8ccf982583be7187d86449ae77a2fc94df5d04575748f69fe7f573e8ac8b94aadd4642b16baa05de474cc023b9c',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'TS013304a6=01c1c020dd9c0d3353512ba0b66274673e31000345b919425ceda02047af0d9b9141b8155a33ace1662596bf4df0e4074f79e82e01; TS011ecef4=01c1c020dd9c0d3353512ba0b66274673e31000345b919425ceda02047af0d9b9141b8155a33ace1662596bf4df0e4074f79e82e01; PF=BZGmovWVJldcNPCGQay9zrWmf7XkgxJq8JAtdkk7KbPw; TS01f293bb=012f350623824afb050395cba78ecac7fe27e8cbedac1041dc2ae7f0b3425f2f628eabb81b288c588bbe50692cd370f349259ea8efd700ef81a918894359cc3684d7b7e9cd; tempuid=; ieeeUserInfoCookie=%7B%22userInfoId%22%3A%2299624278%22%2C%22cartItemQty%22%3A0%2C%22name%22%3A%22BEN%20LOGAN%22%2C%22authStatus%22%3A%22success%22%2C%22lastUpdated%22%3A-661872397479518334%2C%22env%22%3A%22pr%22%7D; ieeeSSO=ZlEtommRo2JpGWSicZFvM5B4Wf35YTwSWxpfGymsBQfNXbLVldBNRA==; opentoken=T1RLAQJ8kXkw1kYYVRitDqB5aAnRWDsJghCjcIavpPkdnNO8SdsQVAXTAACAFhzksuRjdRh-oAAVoz5wUuLCBAB8Q9oSiJ634qvtsd960qu6xfHGbgfERJ6QdwfNEeZ_ZHEk0YlLwSvghBkF5yS2S9lPf_jDBjU4PGfxQQxNouGUG8hM-IYC7BgWCJYqQ5VBjUzQVHHWooiVoQ7meJzRfa48sxyAN5jowWxidi8*; PA.Global_Websession=eyJ6aXAiOiJERUYiLCJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2Iiwia2lkIjoiY2ciLCJwaS5zcmkiOiJJTjlqWjgteGRLdno2ejhaR2s5OGRfN1lKSDQuVGtvIn0..i_3jW8sJcW4kflQNwttL9w.jxIX8lBUXHg_oc_J0hEmZV8AtNyP5Cfz5YuThtYHVaLDaKjAZpmqbC50dGj1o3iDtkL3fGpzeCbuoHo45J6b9EYL91cP8pxouZrlEiKxRTU5nmPXsAheSkb_VFyk0ou7nWhfzupddkKBoWZPwMstjcADWzMPw_njEQpBaOi4u7-Hq9CkqsLw13aGC8KzVvMA7GdH9jDuLXAWmYomn3bA07_Y1MtJ4Ea00zRDRglvMdy7TcSHwzjM4sc_GgNnqadZdVOO7PTbMkxGaJKm8M2STFIqpxZoM2-bym2uZOEFVnHVm4L7GdR7vrO_D6TDCR-lHfkYrj79-oLWyFiOASuxemc12vfAq3pZ2yQd7qIl8JL_4wLR74TTNbbEeKKIHljB7mNlUl64jL6-Y0XOMoOHkR6NxfM4527o3-hUwUkAHcQUxRgqEhJrZ7W9WUBAQzU3KmWIsm_w3U_W2at0VmngtQ.blEXmVGJ4qayxpErTdKYYA; TS01797c2d=012f3506231b7bd60b003ab9a7eb6aa5ce13bafaaae1b31e6bf20659152c5375f58ac17ba70ff8d04022de9a5c31a3fd4c35cdef3d; s_ecid=MCMID%7C41119512348153149430961847830110833947; AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1; s_cc=true; osano_consentmanager_uuid=22e2eecc-45b3-4779-bb9e-c369cc8a5bd4; osano_consentmanager=UdrhNX28-wiqdQuhvvt1HCDXDK0uaNAl2JN6ETOC2QO6rDDIzTxQcpc6oMPhBVu0gGey6g8gY8sGk-drOcLsfjRkGyIXrzex3XgV7QBdp-e1eSg3jGWGBGPLwbo8zVORGR3D6pcIOdqI2fhdxwP9C4TCd_nykGU8-dIQCg74f-N-9XuLFpfXlrNJGqRXQ4uxaCoK4ODkxCjA0XCa1szvLoFNbAS_si1LaMlj4Vfz6sV-dvuqsaXkyVY9hlkxypPM3eO5k8Sdox7ouaJfZdgXh-IoXxNUzcteorxyRw==; TS01b03060=012f350623c8ceaa3d3ea41814ccc28c63d59febbe5871662e26829fd566c2e7270aad933c3b46b18f052320d014a41b3a9eeaafc3; TSaeeec342027=080f8ceb8aab2000338d9500da429fffe24840ddd37eeced23055926821f3be1fa17b731f482bd1f08a63be1fe113000f0ca6437a29ac0f7b8ca10e6c056dcd08513b1392a6efdd4f336086b0e23b26b119cc43368c1385d092c13abb5959f45; TS0118b72b=01f15fc87c6ae56813c69e9a258e602ec3207408f6907948b712f8255586de2c87d5fd7185276b95f0f06307f1e257f47520ba00b8; TS010fc0bf=01f15fc87cbc88d8e71fcaff9c0f800e43033510ac92a3bc218fe1de9331db278790ea141d6e2ecfaf7fa337d3322015dff4d2171b; TS01c3e3fe=01f15fc87cbc88d8e71fcaff9c0f800e43033510ac92a3bc218fe1de9331db278790ea141d6e2ecfaf7fa337d3322015dff4d2171b; s_sq=%5B%5BB%5D%5D; ipCheck=134.83.3.184; CloudFront-Key-Pair-Id=KBLQQ1K30MUFK; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; ipList="37.205.58.148,82.132.229.201,134.83.3.184"; usbls=1; hum_ieee_visitor=88822cce-654a-47ba-8c60-bbdd1633085a; hum_ieee_visitor_matched=true; JSESSIONID=4C4BB54C0914B50B35CFFA8689F31A29; ERIGHTS=kW3kLHEqciW1WG9ULrzr0ANDFHmqwHTD*ACpmxxFx2BJDnpktuRV3YNvVAx3Dx3D-18x2dsHfyx2BKdx2FcPlxxCitNDM7HnQx3Dx3DMcsQG2Mt9jdCyoFx2Bff7VGQx3Dx3D-mEjGbp7x2FDleWTLnGjuY1KAx3Dx3D-5f6yx2F5lFOeakMmsg8x2FRRtgx3Dx3D; WLSESSION=3758191114.47873.0000; TS0154b67f=012f35062348f6f3c376cd553b86607e78246395d0488eb86d60e13b441c7e6bd53cd2c3f6079f42a5ee45d29145db55bda6868575; _zitok=d725a74b342f92c79eea1718098533; TS016349ac=01f15fc87cdf610c994c69334cbda06de892c3b18df39d76cde73e927076a33956cc167137f4164b4cc1a7e56be7d6a5677e98a6a9; utag_main=v_id:018fe3dc2cff002b0908fa126b2c05075003506d00b78; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=359503849%7CMCMID%7C41119512348153149430961847830110833947%7CMCIDTS%7C19886%7CMCAID%7CNONE%7CMCOPTOUT-1718106156s%7CNONE%7CvVersion%7C5.0.1; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vaWVlZXhwbG9yZS5pZWVlLm9yZy9tZWRpYXN0b3JlL0lFRUUvY29udGVudC9tZWRpYS82NzIwMjI1LzY3MzUwMzIvNjczNTA0OC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzE4MTAwNzU5fSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjEzNC44My4zLjE4NCJ9fX1dfQ__; CloudFront-Signature=nx7VUZvinA-lZ-27H4--BVj4JCpHJumT88WXK6875VhhA0Zg-lokG0eEMC~4vfMY29I7I9tw2IozXNWjlVyF0W~3TznKSYC5FLlIkvjiQ84FSx3R-FL2SeOU1z8KsuXGI7thEdnwsbA5RRSePyTpSEX1-S1uFOasO9rvupC5wTTx2pa-58iCEzrAyKzqoPLdU5GPWvyF6-8Sar1aF5YOV~8UaJtEbdj73vekf28wiB~FHSv-tGTX4txg8M1w1IfRhvTgg2brp6pNTBjXnLbrxuwkXyq0iqKeT5QXRjU9XqlMIuVGf-w9HpQVDffJnWoASq0S25hopE1eizm-96ADxQ__; xpluserinfo=eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJCcnVuZWwgVW5pdmVyc2l0eSIsInByb2R1Y3RzIjoiRUJPT0tTOjE5NzQ6MjAyM3xNSVRQOjE5NDM6MjAyM3xOT1dDU0VDOjIwMTg6MjAxOHxXSUxFWVRFTEVDT006MjAxOToyMDE5fElCTToxODcyOjIwMjB8Tk9XQ1NFQzoyMDE5OjIwMTl8Tk9XQ1NFQzoyMDIwOjIwMjB8QVJURUNIOjIwMjE6MjAyM3xXSUxFWVRFTEVDT006MjAxNToyMDE2fE5PS0lBIEJFTEwgTEFCU3xJU09MNTV8TUNDSVM1fE1DQ0lTNnxNQ0NJUzd8SVNPTDg1fE1DQ0lTOHxNQ0NJUzl8TUlUUF9ESVNDT05USU5VRUR8TUNDSVM0fE1DQ0lTNXxJRUx8VkRFfCJ9; seqId=17129; AWSALBAPP-0=AAAAAAAAAADhK/ywGpQtNZVPsIZ5bArEOS6PTgtO3nI54a0HtTH2O5A/rcHa9utyZ6m9A+MyAwMu/gMdT4kCIYpGOBlXJZX2QdSL1OZ0nhJbEJHLEI8QzGB/W48vAyTzjoYyoF2QEAtPjv+BhRqiycX6lICC+IS2U0iDZuy2U5j3vhayKdvQY41yxB3o7zAjyTonabVBYT4TTBF7tN0rQQ==; TS8b476361027=0807dc117eab2000bfd9a4df131b406988bbb3fd6a74ee2f640eb5de2a0f861172bccd9cc384b3f808daf00ab6113000ad3cf8ccf982583be7187d86449ae77a2fc94df5d04575748f69fe7f573e8ac8b94aadd4642b16baa05de474cc023b9c',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

data = parse_file('data/enrichment/slr_enriched_11_06_2024_12_21_07.bib')

# Define the URL
#url = "https://ieeexplore.ieee.org/document/6735048/keywords#keywords"

# follow the DOI url instead - this approach should work for all IEEE papers in my dataset
#url = "https://doi.org/" + '10.1109/ICOS.2013.6735048'
url = "https://doi.org/"

# this is scraping the source of the article, as redirected to via the DOI url
# this is preferred over the GS approach (see webscrape_doi), as it;
# a, is less susceptible to anti-webscraping strategies employed by Google Scholar
# b, means we can source additional metadata fields (like keywords)


def scrape_springer(soup):
    abstract_scraped = soup.find(id='Abs1-content')

    print(abstract_scraped.get_text())

    return {'abstract': abstract_scraped.get_text(), 'keywords': None}


def scrape_ieee(soup):
    # IEEE keywords & abstract...

    script_tags = soup.find_all('script')

    json_text = None
    for script in script_tags:
        if script.string and 'xplGlobal.document.metadata' in script.string:
            match = re.search(r'xplGlobal\.document\.metadata\s*=\s*(\{.*?\});', script.string, re.DOTALL)
            if match:
                json_text = match.group(1)
                break

    if json_text:
        try:
            json_data = json.loads(json_text)
            # print(json.dumps(data, indent=2))  # Pretty print the JSON data
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print('JSON data not found in any script tag.')


def scrape(scrape_url):
    print(scrape_url)

    response = requests.get(scrape_url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        scraped_data = None
        if 'ieeexplore.ieee.org' in response.request.url:
            print('IEEE article')
            scraped_data = scrape_ieee(soup)
        elif 'link.springer.com' in response.request.url:
            print('springer article')
            scraped_data = scrape_springer(soup)
        else:
            print('non-IEEE article')
            print(response.request.url)
        print('-----------------------------------------')
        return scraped_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response)
        return None


new_data = []

for entry in data.entries:
    if FIELD_DOI in entry.fields_dict:
        doi = entry.fields_dict[FIELD_DOI].value
        doi = doi.replace('\\', '')

        if FIELD_ABSTRACT not in entry.fields_dict or FIELD_KEYWORDS not in entry.fields_dict:
            print(entry.fields_dict[FIELD_TITLE].value)
            data = scrape(url + doi)

            if data is not None:
                if FIELD_ABSTRACT not in entry.fields_dict:
                    abstract = data.get('abstract')
                    print('INSERTING THIS ABSTRACT INTO EMPTY ABSTRACT:')
                    print(abstract)
                    print("")

                    if abstract is not None:
                        entry.fields.append(Field(FIELD_ABSTRACT, abstract))

                if FIELD_KEYWORDS not in entry.fields_dict:
                    keywords = data.get('keywords', [])

                    # a bunch of dictionaries...
                    if keywords is not None:
                        for item in keywords:
                            if item['type'] == 'Author Keywords':
                                authorKeywords = item['kwd']
                                print('INSERTING THESE KEYWORDS INTO EMPTY KEYWORDS:')
                                print(authorKeywords)
                                print("")

                        if authorKeywords is not None:
                            entry.fields.append(Field(FIELD_KEYWORDS, authorKeywords))

            time.sleep(10)  # or you may be booted!
    new_data.append(entry)

lib = create_new_lib(new_data)
timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
cleaned_filename = 'data/enrichment/slr_enriched_' + timestamp + '.bib'
save_file(lib, cleaned_filename)
