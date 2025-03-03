country_codes = [
    "IN",  # India
    "US",  # United States
    "UAE",  # United Arab Emirates
]

timezone = {
    "IN": "Asia/Kolkata",  # Indian Standard Time (IST)
    "US": "America/New_York",  # Eastern Standard Time (EST)
    "UAE": "Asia/Dubai",  # Gulf Standard Time (GST)
}

currency_codes = [
    "INR",  # Indian Rupee
    "USD",  # United States Dollar
    "AED",  # United Arab Emirates Dirham
]

currency_symbols = {
    "INR": "₹",
    "USD": "$",
    "AED": "د.إ",
}

language_codes = [
    "ar",  # Arabic (Dubai language)
    "en",  # English
    "hi",  # Hindi
    "ta",  # Tamil
]

date_format = [
    "dd-MM-yyyy",
    "dd/MM/yyyy",
    "MM-dd-yyyy",
    "MM/dd/yyyy",
]

time_format = [
    "HH:mm",  # 24-hour time format
    "hh:mm a",  # 12-hour time format with AM/PM
]

country_config = {
    "IN": {
        "time_zone": "Asia/Kolkata",
        "date_format": "dd-MM-yyyy",
        "time_format": "hh:mm a",
        "language": "en",
        "currency": "INR",
        "login_via": [
            "email",
            "mobile_no",
        ],
        "sms": {
            "is_enabled": True,
            "provider": "msg91",
        },
        "payment_gateway": [
            "razorpay",
        ],
    },
    "US": {
        "time_zone": "America/New_York",
        "date_format": "MM/dd/yyyy",
        "time_format": "HH:mm",
        "language": "en",
        "currency": "USD",
        "login_via": [
            "email",
        ],
        "sms": {
            "is_enabled": False,
            "provider": "",
        },
        "payment_gateway": [
            "stripe",
        ],
    },
    "UAE": {
        "time_zone": "Asia/Dubai",
        "date_format": "dd/MM/yyyy",
        "time_format": "HH:mm",
        "language": "en",
        "currency": "AED",
        "login_via": [
            "email",
        ],
        "sms": {
            "is_enabled": False,
            "provider": "",
        },
        "payment_gateway": [
            "stripe",
        ],
    },
    "default": {
        "time_zone": "America/New_York",
        "date_format": "MM/dd/yyyy",
        "time_format": "HH:mm",
        "language": "en",
        "currency": "USD",
        "login_via": [
            "email",
        ],
        "sms": {
            "is_enabled": False,
            "provider": "",
        },
        "payment_gateway": [
            "stripe",
        ],
    },
}
