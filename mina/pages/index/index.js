//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {}
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/food/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    })
  },
  onShow:function(){

  },
  onReady: function(){
    var that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
    
  login: function (e) {
        if(!e.detail.userInfo){
          app.alert({'content': '授权失败'});
          return;
        }

        var data = e.detail.userInfo;

        wx.login({
          success:function(res){
            if(!res.code){
              app.alert({ 'content': '授权失败' });
              return;
            }


            data['code'] = res.code
            wx.request({
              url: 'http://127.0.0.1:5000/api/member/login',
              method: 'POST',
              header: app.getRequestHeader(),
              data: data,
              success: function (res) {

              }
            })
          }
        })
  }
});