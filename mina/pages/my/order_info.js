var app = getApp();
Page({
    data: {},
    onLoad: function (e) {
        var that = this;
    },
    onShow: function () {
        var that = this;
        that.setData({
            info: {
                order_sn:"123123",
                status: -8,
                status_desc: "待支付",
                deadline:"2018-07-31 12:00",
                pay_price: "85.00",
                yun_price: 0.00,
                total_price: "85.00",
                address: {},
                goods: []
            }
        });
    }
});