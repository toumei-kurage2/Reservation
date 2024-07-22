from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView #テンプレートタグ
from .forms import (AccountForm, AddAccountForm,ChecklistForm)
from .models import Facility,Room,Reservation,Reservation_detail,RoomType,Account
from django.contrib.auth.models import User
from datetime import date,datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('facility_select'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'ReservationApp/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))




#新規登録
class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"ReservationApp/register.html",context=self.params)

    #Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"ReservationApp/register.html",context=self.params)
#施設選択画面
@login_required    
def facility_select(request):
    facilities = Facility.objects.all()
    facility_list = []
    for facility in facilities:
        facility_list.append(Facility(facility_name=facility.facility_name,picture_url=facility.picture_url))
    return render(request,"ReservationApp/facility_select.html",context={
        "facility_list":facility_list,
    }) 
          
@login_required 
def checklist(request,facility_name):
    reservation_tb = Reservation()
    if request.method=="POST":
        form=ChecklistForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]
            user = User.objects.get(username=request.user)
            account=Account.objects.get(user=user)
            re1=Reservation.objects.filter(Q(check_in__range=[check_in,check_out])|Q(check_out__range=[check_in,check_out]),account=account)
            de=Reservation_detail.objects.filter(reservation=re1[0])
            older_facility_name=de[0].room.facility.facility_name
            older_room_type=de[0].room.room_type
            room_type = RoomType.objects.get(pk=form.cleaned_data["room_type"].pk)
            older_reservation1=Reservation.objects.filter(account=account,check_in__range=[check_in,check_out])
            older_reservation2=Reservation.objects.filter(account=account,check_out__range=[check_in,check_out])
            if older_reservation1 or older_reservation2:
                if facility_name != older_facility_name:
                    return HttpResponse("同じ日に別の予約がございます。予定一覧をご覧ください")
                elif room_type == older_room_type:
                    return HttpResponse("同じ日に同じ部屋種別の予約がございます。予定詳細一覧をご覧ください")
            type_persons=form.cleaned_data["type_persons"]
            facility = Facility.objects.get(facility_name=facility_name)
            facility_id = facility.pk
            room_type_id = room_type.pk
            rooms = Room.objects.filter(facility_id=facility_id,room_type_id=room_type_id,)
            room_sum = form.cleaned_data["room_sum"]
            empty_rooms=[]
            for room in rooms :
                details = Reservation_detail.objects.filter(
                    date__range=[check_in,check_out],
                    room = room
                )
                if not details:
                    empty_rooms.append(room)
            if len(empty_rooms) < room_sum:
                print(len(empty_rooms),room_sum)
                return HttpResponse("部屋の数が足りませんでした。条件を変更の上再度ご入力ください")
            reservation_tb.account=account
            reservation_tb.check_in=check_in
            reservation_tb.check_out=check_out
            reservation_tb.save() 
            for i in range(check_out.day-check_in.day):
                reservation=Reservation.objects.get(account=account,check_in=check_in,check_out=check_out)
                for j in range(room_sum):
                    detail=Reservation_detail()
                    print("ここまで")
                    room=Room.objects.get(pk=empty_rooms[j].pk)
                    detail.date=check_in+timedelta(days=i)
                    detail.type_persons=type_persons
                    detail.reservation=reservation
                    detail.room=room
                    detail.save()
            return redirect('reservationlist')
    else:
        form = ChecklistForm()
    return render(request,"ReservationApp/checklist.html",context={
        "form":form,
        "facility_name":facility_name
    })
  
        
@login_required 
def reservationlist(request):
    user = request.user
    account=Account.objects.get(user=user)
    reservations = Reservation.objects.filter(account=account)
    reservationlist=[]
    for reservation in reservations:
        detaillist=Reservation_detail.objects.filter(reservation=reservation)
        reservationlist.append([reservation,detaillist[0].room.facility.facility_name])
    return render(request,"ReservationApp/reservationlist.html",context={
        "reservationlist":reservationlist,
    })

@login_required 
def detaillist(request,reservation_id):
    details=Reservation_detail.objects.filter(reservation=Reservation.objects.get(pk=reservation_id))
    return render(request,"ReservationApp/detaillist.html",context={
        "details":details
    })
    
@login_required    
def delete(request,reservation_id):
    reservation=Reservation.objects.get(pk=reservation_id)
    reservation.delete()
    return redirect('reservationlist')

@login_required 
def update(request,reservation_id):
    detail=Reservation_detail.objects.filter(reservation=reservation_id)
    facility=detail[0].room.facility
    form=ChecklistForm()
    reservation_tb = Reservation()
    if request.method=="POST":
        form=ChecklistForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]
            account=Account.objects.get(user=request.user)
            user = User.objects.get(username=request.user)
            account=Account.objects.get(user=user)
            older_reservationlist1=Reservation.objects.exclude(pk=reservation_id).filter(account=account,check_in__range=[check_in,check_out])
            older_reservationlist2=Reservation.objects.exclude(pk=reservation_id).filter(account=account,check_out__range=[check_in,check_out])
            if older_reservationlist1 or older_reservationlist2:
                return HttpResponse("同じ日に別の予約がございます。予定一覧をご覧ください")
            type_persons=form.cleaned_data["type_persons"]
            room_type = RoomType.objects.get(pk=form.cleaned_data["room_type"].pk)
            facility_id = facility.pk
            room_type_id = room_type.pk
            rooms = Room.objects.filter(facility_id=facility_id,room_type_id=room_type_id,)
            room_sum = form.cleaned_data["room_sum"]
            empty_rooms=[]
            for room in rooms :
                details=Reservation_detail.objects.exclude(reservation=reservation_id).filter(
                    date__range=[check_in,check_out],
                    room = room
                )
                if not details:
                    empty_rooms.append(room)
            if len(empty_rooms) < room_sum:
                print(len(empty_rooms),room_sum)
                return HttpResponse("部屋の数が足りませんでした。条件を変更の上再度ご入力ください")
            olderreservation=Reservation.objects.get(pk=reservation_id)
            olderreservation.delete()
            reservation_tb.account=account
            reservation_tb.check_in=check_in
            reservation_tb.check_out=check_out
            reservation_tb.save() 
            for i in range(check_out.day-check_in.day):
                reservation=Reservation.objects.get(account=account,check_in=check_in,check_out=check_out)
                for j in range(room_sum):
                    detail=Reservation_detail()
                    room=Room.objects.get(pk=empty_rooms[j].pk)
                    detail.date=check_in+timedelta(days=i)
                    detail.type_persons=type_persons
                    detail.reservation=reservation
                    detail.room=room
                    detail.save()
            return redirect('reservationlist')

    return render(request,"ReservationApp/checklist.html",context={"form":form,"facility_name":facility.facility_name})

 