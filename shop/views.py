from django.shortcuts import render
from django.views.generic import TemplateView

from config.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, BASE_DIR

import stripe
import time
import os

stripe.api_key = STRIPE_SECRET_KEY


#############################
#商品を売る人のstripeアカウント
#############################

def create_custom_account():
    """
    #アカウント作成 account
    
    return example

        "id": "acct_1F6KiGB3268k39y4",        
        ...
        "type": "custom"
    """

    #token-account: https://stripe.com/docs/connect/account-tokens
    account = stripe.Account.create(
        type="custom",
        country="JP",
        email="test@test.com", #user email
        business_type="individual",
    )
    return account

def create_account_person(user_id):
    #pserson tokenについて
    #https://stripe.com/docs/connect/account-tokens

    token = "token-person" #request.form['token-person] 上の情報を参照
    person = stripe.Account.create_person(
        user_id,

    )

def get_custom_account(acct_id):
    account = stripe.Account.retrieve(acct_id)
    return account


def update_custom_account(acct_id):
    account = get_custom_account(acct_id)
    print(account)

    #アカウント情報の更新
    res = stripe.Account.modify(
        acct_id,
        individual ={
            'first_name':'田中',
            'last_name':"太郎",
            'first_name_kana':"ﾀﾅｶ",
            'last_name_kana':"ﾀﾛｳ",
            'first_name_kanji':"田中",
            'last_name_kanji':"太郎",
            'phone':"+8109001020993",
            'gender':"male", #male or female
            'address_kanji':{
                "country":"JP",
                "state":"東京都",
                "city":"渋谷区",
                "town":"神宮前　1丁目",
                "line1":"5-8",
                "line2":"神宮前タワービルディング 22F",
                "postal_code":"1500001",
            },
            'address_kana':{
                "country": "JP", # 2-letter country code
                "postal_code": "1500001", # Zip/Postal Code
                "state": "ﾄｳｷﾖｳﾄ", # Prefecture
                "city": "ｼﾌﾞﾔ", # City/Ward
                "town": "ｼﾞﾝｸﾞｳﾏｴ 1-", # Town/cho-me
                "line1": "5-8", # Block/Building number
                "line2": "ｼﾞﾝｸﾞｳﾏｴﾀﾜｰﾋﾞﾙﾃﾞｨﾝｸﾞ22F", # Building details (optional)
            },
            'dob':{
                "day":"01",
                "month":"01",
                "year":"1900"
            },
            
        },
        tos_acceptance = {
            "date":int(time.time()),  #=> 1399605420   # 経過秒数を整数で取得
            "ip":"8.8.8.8"            #グローバルIPアドレスを入力
        }
    )

def create_bank_account(acct_id):
    #銀行講座登録
    account = stripe.Account.create_external_account(
        acct_id,
        external_account = {
            "object":"bank_account",
            "account_number":"00012345",
            "routing_number":"1100000", #銀行コード + 支店
            "account_holder_name":"タナカタロウ",
            "account_holder_type":"individual",
            "currency":"jpy",
            "country":"JP"
        }
    )

def update_payouts_schedule(acct_id):
    account = get_custom_account(acct_id)

    #入金のスケジュールを更新
    res = stripe.Account.modify(
        acct_id,
        settings = {"payouts": {"schedule":{
                "delay_days": 4,
                "interval":"weekly",
                "weekly_anchor": "friday"
            },
        }}
    )

def upload_identity_verification_file(acct_id, img_path):
    #https://stripe.com/docs/connect/identity-verification-api
    with open(img_path, "rb") as fp:
        res = stripe.FileUpload.create(
            purpose='identity_document',
            file=fp,
            stripe_account=acct_id
        )
        verification_id = res["id"]

        res = stripe.Account.modify(
            acct_id,
            individual ={ "verification" :{
                "document":{
                    "front": verification_id
                }
            }})

        print(res)



#############################
#商品を買う人のstripeアカウント
#############################

def create_user_account(user):
    """
    "id":"cus_FbYcVYlQhY5Yzv"
    """
    strip_customer = stripe.Customer.create(
        description = user.username,
        email = user.email
    )
    return strip_customer

def charge_user(acct_id, amount, application_fee):
    #https://stripe.com/docs/connect/direct-charges#collecting-fees
    charge = stripe.Charge.create(
        amount=amount,
        currency='jpy',
        description='charge',
        source="tok_visa",  #request.POST['stripeToken']
        application_fee_amount=application_fee,
        stripe_account=acct_id
    )
    print(charge)
    
    



class ShopView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        
        #https://stripe.com/docs/api/errors/handling #エラーハンドリング

        ####################################
        # 2. Customアカウント作成
        ####################################

        #account = create_custom_account()
        

        ####################################
        # 3. アカウント情報の取得
        ####################################
    
        CONNECTED_STRIPE_ACCOUNT_ID = "acct_1F6KiGB3268k39y4"
        
        #update_custom_account(CONNECTED_STRIPE_ACCOUNT_ID)
        
        ####################################
        # 4. 銀行口座の登録
        ####################################

        #create_bank_account(CONNECTED_STRIPE_ACCOUNT_ID)
        #update_payouts_schedule(CONNECTED_STRIPE_ACCOUNT_ID)

        ####################################
        # 5. 本人証明
        ####################################
        
        #image_path = os.path.join(BASE_DIR, "static", "identify.png")
        
        #upload_identity_verification_file(CONNECTED_STRIPE_ACCOUNT_ID, image_path)

        #charge_user(CONNECTED_STRIPE_ACCOUNT_ID, 5000, 500)
        return context
    