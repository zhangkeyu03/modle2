# WebData Crawler

This project collects data from:
- **Web1.0** sources (e.g., official university websites like MSU, SPbGU)
- **Web2.0** platforms (e.g., VK, Telegram)

## Folders

- `web1.0/` – Scripts for parsing university websites (e.g., `msu_parser.py`)
- `web2.0/` – VK parser that fetches posts from groups using the VK API

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/zhangkeyu03/modle2.git
   cd modle2


## How to Get a VK Service Token

To run the VK data crawler (`web2.0/vk_parser.py`), follow these steps to get a **Service Token**:

1. Visit https://dev.vk.com/.
2. Log in with your VK account.
3. Go to the "Apps" section.
4. Click "Create app", and select the app type "Мини-приложение" (Mini Application).
5. Fill in:
   - **App name**: e.g., `web2research`
   - **Category**: e.g., `Образ жизни` (Lifestyle)
6. Once created, go to the app’s settings.
7. Copy the **Service Token** listed under **"Access Tokens"**.

Then, in your script (`vk_parser.py`), replace this line:

```python
SERVICE_TOKEN = "your_actual_token_here"
