var app = getApp();
Page({
    data: {
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成","已关闭"],
        status:[ "-8","-7","-6","-5","1","0" ],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        this.onShow();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;

      this.getPayOrder();
        that.setData({
            order_list: [          ]
        });
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },

    getPayOrder: function(){
      var me = this;

      wx.request({
        url: app.buildUrl("/my/order"),
        header: app.getRequestHeader(),
        data: {
          status: me.data.status[me.data.currentType]
        },
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert({ "content": resp.msg });
            return;
          }

          me.setData({
           order_list : resp.data.pay_order_list
          })
        }
      });
    },

    toPay: function(e){
      var me = this;

      wx.request({
        url: app.buildUrl("/order/pay"),
        method: 'POST',
        header: app.getRequestHeader(),
        data: {
          order_sn: e.currentTarget.dataset.id
        },
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert({ "content": resp.msg });
            return;
          }

          var pay_info = resp.data.pay_info
          wx.requestPayment({
            'timeStamp': pay_info.timeStamp,
            'nonceStr': pay_info.nonceStr,
            'package': pay_info.package,
            'signType': 'MD5',
            'paySign': pay_info.paySign,
            'success': function (res) { },
            'fail': function (res) { },
            'complete': function (res) { }
          })
        }
      });
    }
})
