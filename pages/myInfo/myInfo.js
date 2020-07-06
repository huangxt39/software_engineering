// pages/addOrEditUser/addOrEditUser.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    info:{},
  },

  delete_account() {
    console.log(app.globalData.userInfo.user_id)
    wx.request({
      url:'https://reck.sakurasou.life/wx_login/delete_account', //后端数据接口
      // url:'http://127.0.0.1:5000/login/login.msg', //必填，其他的都可以不填
      header:{  
        'content-type':'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'application/json'
      },
      method:'POST',  
      //dataType:"json",
      data:{user_id: app.globalData.userInfo.user_id},
      success: function (res){ //调用成功之后获得的数据在res
        console.log(res.data)
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    let user_info=JSON.parse(options.item);
    this.setData({
      info:user_info
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  
})