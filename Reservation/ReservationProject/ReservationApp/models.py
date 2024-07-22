from django.db import models
# ユーザー認証
from django.contrib.auth.models import User
# ユーザーアカウントのモデルクラス
class Account(models.Model):
    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 追加フィールド
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number=models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.user

class Facility(models.Model):
    facility_name=models.CharField(max_length=50)
    picture_url = models.URLField()
    class Meta:
        db_table="facility"

class RoomType(models.Model):
    type_name = models.CharField(max_length=30)
    capacity=models.IntegerField()
    type_fee = models.IntegerField()
    def __str__(self):
        return self.type_name
    class Meta:
        db_table = "roomtype" 

class Reservation(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    account = models.ForeignKey(
        Account,on_delete=models.CASCADE
    )
    class Meta:
        db_table="reseravtion"

class Room(models.Model):
    room_number= models.IntegerField()
    facility = models.ForeignKey(
        Facility,on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType,on_delete=models.CASCADE
    )
    class Meta:
        db_table = "room"

class Reservation_detail(models.Model):
    date = models.DateField()
    type_persons = models.IntegerField()
    reservation = models.ForeignKey(
        Reservation,on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room,on_delete = models.CASCADE
    )
    class Meta:
        db_table = "reservation_detail"
        unique_together = [["room","date"]]
