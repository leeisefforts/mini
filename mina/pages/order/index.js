//获取应用实例
var app = getApp();

Page({
    data: {
        goods_list: [],
        default_address: {},
        yun_price: "1.00",
        pay_price: "85.00",
        total_price: "86.00",
        params: null
    },
    onShow: function () {
        var that = this;
        that.getOrderInfo()
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
          params: JSON.parse(e.data)
        });
        
    },
    createOrder: function (e) {
        wx.showLoading();
        var me = this;

      var data = {
        type: me.data.params.type,
        goods: JSON.stringify(me.data.params.goods)
      };

      wx.request({
        url: app.buildUrl("/order/create"),
        method: 'POST',
        header: app.getRequestHeader(),
        data: data,
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert({ "content": resp.msg });
            return;
          };

          wx.navigateTo({
            url: "/pages/my/order_list"
          });
        }
      });
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },

    getOrderInfo: function(){
      var me = this;
      var data = {
        type: me.data.params.type,
        goods: JSON.stringify(me.data.params.goods)
      }
      wx.request({
          url: app.buildUrl("/order/info"),
          method: 'POST',
          header: app.getRequestHeader(),
          data:data,
          success: function(res){
            var resp = res.data;
            if (resp.code != 200) {
              app.alert({ "content": resp.msg });
              return;
            }

            me.setData({
              goods_list: resp.data.food_list,
              default_address: resp.data.default_address,
              yun_price: resp.data.yun_price,
              pay_price: resp.data.pay_price,
              total_price: resp.data.total_price
            })
          }
      });
    }

});
