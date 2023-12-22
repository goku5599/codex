import asyncio
import random
import requests
from faker import Faker
from telegram import Bot

BINLIST_API_URL = "https://binlist.io/lookup/"
country_emojis = {
  "Canada": "🇨🇦",
  "United States": "🇺🇸",
  "United Kingdom": "🇬🇧",
  "Spain": "🇪🇸",
  "France": "🇫🇷",
  "Germany": "🇩🇪",
  "Italy": "🇮🇹",
  "Australia": "🇦🇺",
  "Japan": "🇯🇵",
  "Russia": "🇷🇺",
  "Brazil": "🇧🇷",
  "India": "🇮🇳",
  "China": "🇨🇳",
  "South Korea": "🇰🇷",
  "Mexico": "🇲🇽",
  "South Africa": "🇿🇦",
  "Egypt": "🇪🇬",
  "Turkey": "🇹🇷",
  "Argentina": "🇦🇷",
  "New Zealand": "🇳🇿",
  "Greece": "🇬🇷",
  "Nigeria": "🇳🇬",
  "Kenya": "🇰🇪",
  "Sweden": "🇸🇪",
  "Norway": "🇳🇴",
  "Denmark": "🇩🇰",
  "Finland": "🇫🇮",
  "Netherlands": "🇳🇱",
  "Belgium": "🇧🇪",
  "Austria": "🇦🇹",
  "Switzerland": "🇨🇭",
  "Portugal": "🇵🇹",
  "Ireland": "🇮🇪",
  "Poland": "🇵🇱",
  "Hungary": "🇭🇺",
  "Czech Republic": "🇨🇿",
  "Slovakia": "🇸🇰",
  "Croatia": "🇭🇷",
  "Serbia": "🇷🇸",
  "Bulgaria": "🇧🇬",
  "Romania": "🇷🇴",
  "Ukraine": "🇺🇦",
  "Belarus": "🇧🇾",
  "Estonia": "🇪🇪",
  "Latvia": "🇱🇻",
  "Lithuania": "🇱🇹",
  "Slovenia": "🇸🇮",
  "Bosnia and Herzegovina": "🇧🇦",
  "Montenegro": "🇲🇪",
  "Macedonia": "🇲🇰",
  "Albania": "🇦🇱",
  "Kosovo": "🇽🇰",
  "Moldova": "🇲🇩",
  "Georgia": "🇬🇪",
  "Armenia": "🇦🇲",
  "Azerbaijan": "🇦🇿",
  "Kazakhstan": "🇰🇿",
  "Turkmenistan": "🇹🇲",
  "Uzbekistan": "🇺🇿",
  "Tajikistan": "🇹🇯",
  "Kyrgyzstan": "🇰🇬",
  "Afghanistan": "🇦🇫",
  "Pakistan": "🇵🇰",
  "Nepal": "🇳🇵",
  "Bhutan": "🇧🇹",
  "Sri Lanka": "🇱🇰",
  "Bangladesh": "🇧🇩",
  "Myanmar": "🇲🇲",
  "Thailand": "🇹🇭",
  "Cambodia": "🇰🇭",
  "Vietnam": "🇻🇳",
  "Laos": "🇱🇦",
  "Malaysia": "🇲🇾",
  "Singapore": "🇸🇬",
  "Indonesia": "🇮🇩",
  "Brunei": "🇧🇳",
  "Philippines": "🇵🇭",
  "Timor-Leste": "🇹🇱",
  "Papua New Guinea": "🇵🇬",
  "Solomon Islands": "🇸🇧",
  "Vanuatu": "🇻🇺",
  "Fiji": "🇫🇯",
  "Tuvalu": "🇹🇻",
  "Kiribati": "🇰🇮",
  "Marshall Islands": "🇲🇭",
  "Micronesia": "🇫🇲",
  "Palau": "🇵🇼",
  "Nauru": "🇳🇷",
  "Tonga": "🇹🇴",
  "Samoa": "🇼🇸",
  "Haiti": "🇭🇹",
  "Jamaica": "🇯🇲",
  "Cuba": "🇨🇺",
  "Dominican Republic": "🇩🇴",
  "Puerto Rico": "🇵🇷",
  "The Bahamas": "🇧🇸",
  "Barbados": "🇧🇧",
  "Trinidad and Tobago": "🇹🇹",
  "Grenada": "🇬🇩",
  "Saint Vincent and the Grenadines": "🇻🇨",
  "Saint Lucia": "🇱🇨",
  "Antigua and Barbuda": "🇦🇬",
  "Saint Kitts and Nevis": "🇰🇳",
  "Belize": "🇧🇿",
  "Guatemala": "🇬🇹",
  "El Salvador": "🇸🇻",
  "Honduras": "🇭🇳",
  "Nicaragua": "🇳🇮",
  "Costa Rica": "🇨🇷",
  "Panama": "🇵🇦",
  "Colombia": "🇨🇴",
  "Ecuador": "🇪🇨",
  "Peru": "🇵🇪",
  "Bolivia": "🇧🇴",
  "Chile": "🇨🇱",
  "Paraguay": "🇵🇾",
  "Uruguay": "🇺🇾",
  "Venezuela": "🇻🇪",
  "Guyana": "🇬🇾",
  "Suriname": "🇸🇷",
  "Mauritania": "🇲🇷",
  "Senegal": "🇸🇳",
  "Gambia": "🇬🇲",
  "Guinea-Bissau": "🇬🇼",
  "Guinea": "🇬🇳",
  "Sierra Leone": "🇸🇱",
  "Liberia": "🇱🇷",
  "Ivory Coast": "🇨🇮",
  "Ghana": "🇬🇭",
  "Togo": "🇹🇬",
  "Benin": "🇧🇯",
  "Niger": "🇳🇪",
  "Mali": "🇲🇱",
  "Burkina Faso": "🇧🇫",
  "Niger": "🇳🇪",
  "Mali": "🇲🇱",
  "Burkina Faso": "🇧🇫",
  "Mauritania": "🇲🇷",
  "Senegal": "🇸🇳",
  "Gambia": "🇬🇲",
  "Guinea-Bissau": "🇬🇼",
  "Guinea": "🇬🇳",
  "Sierra Leone": "🇸🇱",
  "Liberia": "🇱🇷",
  "Ivory Coast": "🇨🇮",
  "Ghana": "🇬🇭",
  "Togo": "🇹🇬",
  "Benin": "🇧🇯",
  "Niger": "🇳🇪",
  "Mali": "🇲🇱",
  "Burkina Faso": "🇧🇫",
  "Guinea": "🇬🇳",
  "Sierra Leone": "🇸🇱",
  "Liberia": "🇱🇷",
  "Ivory Coast": "🇨🇮",
  "Ghana": "🇬🇭",
  "Togo": "🇹🇬",
  "Benin": "🇧🇯",
  "Niger": "🇳🇪",
  "Mali": "🇲🇱",
  "Burkina Faso": "🇧🇫",
  "Nigeria": "🇳🇬",
  "Cameroon": "🇨🇲",
  "Chad": "🇹🇩",
  "Central African Republic": "🇨🇫",
  "Sudan": "🇸🇩",
  "South Sudan": "🇸🇸",
  "Uganda": "🇺🇬",
  "Rwanda": "🇷🇼",
  "Burundi": "🇧🇮",
  "Democratic Republic of the Congo": "🇨🇩",
  "Republic of the Congo": "🇨🇬",
  "Gabon": "🇬🇦",
  "Equatorial Guinea": "🇬🇶",
  "Sao Tome and Principe": "🇸🇹",
  "Morocco": "🇲🇦",
  "Western Sahara": "🇪🇭",
  "Algeria": "🇩🇿",
  "Tunisia": "🇹🇳",
  "Libya": "🇱🇾",
  "Egypt": "🇪🇬",
  "Sudan": "🇸🇩",
  "South Sudan": "🇸🇸",
  "Uganda": "🇺🇬",
  "Rwanda": "🇷🇼",
  "Burundi": "🇧🇮",
  "Democratic Republic of the Congo": "🇨🇩",
  "Republic of the Congo": "🇨🇬",
  "Gabon": "🇬🇦",
  "Equatorial Guinea": "🇬🇶",
  "Sao Tome and Principe": "🇸🇹",
  "Morocco": "🇲🇦",
  "Western Sahara": "🇪🇭",
  "Algeria": "🇩🇿",
  "Tunisia": "🇹🇳",
  "Libya": "🇱🇾",
  "Egypt": "🇪🇬",
  "Western Sahara": "🇪🇭",
  "Algeria": "🇩🇿",
  "Tunisia": "🇹🇳",
  "Libya": "🇱🇾",
  "Mauritania": "🇲🇷",
  "Western Sahara": "🇪🇭",
  "Algeria": "🇩🇿",
  "Tunisia": "🇹🇳",
  "Libya": "🇱🇾",
  "Mauritania": "🇲🇷",
  "Senegal": "🇸🇳",
  "Gambia": "🇬🇲",
  "Guinea-Bissau": "🇬🇼",
  "Guinea": "🇬🇳",
  "Sierra Leone": "🇸🇱",
  "Liberia": "🇱🇷",
  "Ivory Coast": "🇨🇮",
  "Ghana": "🇬🇭",
  "Togo": "🇹🇬",
  "Benin": "🇧🇯",
  "Niger": "🇳🇪",
  "Mali": "🇲🇱",
  "Burkina Faso": "🇧🇫",
  "Nigeria": "🇳🇬",
  "Cameroon": "🇨🇲",
  "Chad": "🇹🇩",
  "Central African Republic": "🇨🇫",
}


def is_valid_bin(bin_number):
    if len(bin_number) > 0:
        return True
    else:
        return False

def get_bin_info(bin_number):
    url = f"{BINLIST_API_URL}{bin_number}/"
    response = requests.get(url)
    if response.status_code == 200:
        bin_info = response.json()
        return bin_info
    return None

def generate_credit_card():
    while True:
        bin_number = random.randint(400000, 599999)
        bin_number_str = str(bin_number)
        if is_valid_bin(bin_number_str):
            fake = Faker()
            expiration_date = fake.credit_card_expire()
            cvv = random.randint(000, 999)
            credit_card_number = f"{bin_number_str}{''.join(random.choice('0123456789') for _ in range(10))}"
            bin_info = get_bin_info(bin_number_str)
            if bin_info:
                country_emoji = bin_info.get('country', {}).get('emoji', '🌍')
                return bin_number_str, credit_card_number, expiration_date, cvv, bin_info, country_emoji

async def send_message_to_telegram(message, token, chat_id):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

async def send_credit_card_info(bot_token, channel_username):
    valid_bin, credit_card, expiration_date, cvv, bin_info, country_emoji = generate_credit_card()
    country = bin_info.get('country', {}).get('name', 'N/A')
    bank_name = bin_info.get('bank', {}).get('name', 'N/A')

    message = f"{country_emoji}|{credit_card} {expiration_date} {cvv} - {valid_bin}\n"
    message += f"{country} {bank_name}"

    await send_message_to_telegram(message, bot_token, channel_username)

async def main():
    bot_token = "6856406658:AAHIR-yCgZvbGqiOxoygKHCLqhDkXPnQf-4"
    channel_username = "@DARKMETHORDSCRAPPER"

    print("*+++++++++ WELCOME TO MY SCRIPT GUYS ONE PIECE IS HERE! ++++++++++*\n")
    print("*++++++++++++++++ HEY BABY WE ARE LIVE ++++++++++++++++*")
    while True:
        await send_credit_card_info(bot_token, channel_username)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
