# hkqr python

__hkqr python__ is a python package for generating the QR Code data for Hong Kong Faster Payment System (FPS) which is a standard by Hong Kong Interbank Clearing Limited. 
Standard definitions are available at https://fps.hkicl.com.hk/eng/fps/merchants/qr_code.php

The __hkqr python__ package only deals with:
- Generating the string data of the QR Code. You are free to use any QR code libraries to generate the graphics on your chosen frontends.
- Currently support the generation QR Code with your Merchant ID with ``price`` and ``reference ID``.

---

## Installation

Use pip to install:  

``pip install hkqr``

## Running hkqr in your Python program

Supposed your Merchant ID is ``999999999999``,  
and you would like to charge an amount of ``100``  
with reference ID ``QR12345``:

```
from hkqr import HKQR
hkqr = HKQR('999999999999')
qrcode = hkqr.create_hkqr_code( 100, reference_id="QR12345")
```
Printing the value of ``code`` should show the string value ``00020101021226320012hk.com.hkicl021299999999999952040000530334454031005802HK5902NA6002HK62110507QR123456304983E``.

The Merchant ID can be ``account number`` assigned by your FPS provider, ``phone number`` or ``e-mail``.

## WARNING
Make sure you test your code and do a very small amount of transaction for testing, verifying the transaction actually works before going live on production. 

---
# Terms & Conditions

Please read these terms and conditions carefully before using __hkqr python__. By using this software, you agree to be bound by these terms and conditions.

Acceptance of Terms
By using __hkqr python__, you acknowledge that you have read, understood, and agreed to be bound by these terms and conditions. If you do not agree with any part of these terms and conditions, please refrain from using the software.

No Warranty
__hkqr python__ is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. The developer(s) of [Your Open Source Python Package] make no warranty that the software will meet your requirements or that it will be error-free, reliable, or compatible with your operating system or other software.

Limitation of Liability
In no event shall the developer(s) of __hkqr python__ be liable for any damages, including but not limited to direct, indirect, special, incidental, or consequential damages or losses arising out of the use or inability to use the software, even if advised of the possibility of such damages. You assume all risks associated with the use of [Your Open Source Python Package].

Indemnification
You agree to indemnify, defend, and hold harmless the developer(s) of __hkqr python__ from and against any claims, liabilities, damages, losses, or expenses, including attorney's fees, arising out of your use or misuse of the software or violation of these terms and conditions.

Modification and Distribution
You are allowed to modify and distribute __hkqr python__ in accordance with the applicable open source licenses, provided that you include a copy of these terms and conditions with your distribution. However, you may not use the name of the developer(s) or [Your Open Source Python Package] to endorse or promote your modified version without prior written permission.

Governing Law
These terms and conditions shall be governed by and construed in accordance with the laws of Hong Kong, the United States of America and United Kingdom. Any legal action or proceeding arising out of or relating to these terms and conditions shall be exclusively brought in the courts of Hong Kong, the United States of America or United Kingdom.

Entire Agreement
These terms and conditions constitute the entire agreement between you and the developer(s) of __hkqr python__ and supersede all prior or contemporaneous communications and proposals, whether oral or written, relating to the software.

By using __hkqr python__, you acknowledge that you have read, understood, and agreed to these terms and conditions. If you do not agree with any part of these terms and conditions, please refrain from using the software.

__hkqr python__ is an open source project. For more information, please visit https://github.com/pulsely/hkqr

---

# Copyright and license

The __hkqr python__ is written by Pulsely https://www.pulsely.com/  
GPL License

Copyright 2023 Pulsely