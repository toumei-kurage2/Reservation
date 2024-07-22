from django import forms
from django.contrib.auth.models import User
from .models import Account,RoomType,Reservation,Reservation_detail
import re
from django.core.validators import MinLengthValidator
from datetime import date,datetime

# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'6文字以上、半角英数字'}),
        label="パスワード",
        validators=[MinLengthValidator(6,"6文字以上で入力してください")]
    )
    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','password')
        # フィールド名指定
        labels = {'username':"ユーザーID"}

class AddAccountForm(forms.ModelForm):
    phone_number=forms.CharField(
        max_length=30,
        widget= forms.TextInput(attrs={'placeholder':'例)090-1234-5678'}),label="電話番号"
    )
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('last_name','first_name','phone_number','address',)
        labels = {'last_name':"苗字",'first_name':"名前",'phone_number':"電話番号","address":"住所"}
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if  not re.match(r'[(]?\d{2,4}[-)]?\d{2,4}-\d{3,4}',str(phone_number)):
            raise forms.ValidationError("電話番号の形式で入力してください")
        return phone_number

class ChecklistForm(forms.Form):
    room_type=forms.ModelChoiceField(RoomType.objects.all(),label="部屋種別")
    check_in = forms.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y'],
                               widget=forms.DateInput(attrs={'type': 'date'}),
                               initial=date.today,
                               label="チェックイン日付")
    check_out = forms.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y'],
                               widget=forms.DateInput(attrs={'type': 'date'}),
                               initial=date.today,
                               label="チェックアウト日付")
    room_sum = forms.IntegerField(label="部屋数")
    type_persons = forms.IntegerField(label="宿泊人数")
    def clean_type_persons(self):
        type_persons=self.cleaned_data.get("type_persons")
        room_type=self.cleaned_data.get("room_type")
        capacity=room_type.capacity
        if type_persons>capacity:
            raise forms.ValidationError("宿泊可能な人数を超えています")
        return type_persons

    def clean_check_out(self):
        check_in=self.cleaned_data.get("check_in")
        check_out=self.cleaned_data.get("check_out")
        check_in = datetime.strptime(str(check_in), '%Y-%m-%d')
        check_out= datetime.strptime(str(check_out),'%Y-%m-%d')
        check_in=date(check_in.year,check_in.month,check_in.day)
        check_out=date(check_out.year,check_out.month,check_out.day)
        if check_in >= check_out:
            raise forms.ValidationError("チェックアウト日付がチェックイン日付と同じか前に指定されています")
        return check_out
    
            
    
    








