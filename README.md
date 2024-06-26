# Auto-Calendar

A python script which can help you automatically parse the names and times of some algorithm competitions matches ad import them into your outlook emails.

## supported websites

- [codeforces](https://codeforces.com/)
- [atcoder](https://atcoder.jp/home)
- [nowcoder](https://ac.nowcoder.com/acm/contest/vip-index)
- [luogu](https://www.luogu.com.cn/training/list)

## running locally

This project relies on tesseract to implement image recognition functions. You need to install [tesseract](https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D). Don't use **VPN** as this slow down downloads.
![alt text](image/three.png)
Click the arrow pointing to the button in the picture to make it appear as **Last modified** and downloads the latest version. Don't forget to add environment variables.

To install the necessary dependencies, make sure you have Python and pip installed, then run the following command in the project root directory:

```bash
pip install -r requirements.txt
```

After the above preparations are completed you need to log in Outlook on your default browser and set the display **week number** in the calendar and the start of each week as **Monday**.

Then run the **get_position.py** and press **CTRL** and click screen in the order of the pictures.
![alt text](image/one.png)
![alt text](image/two.png)

Then you can run the **main.py**.
