// pages/addOrEditUser/addOrEditUser.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    info:{
      name:"黄鑫霆",
      id:17363032,
      password:1234567,
      cellphone:13223332333,
      email:"23333333@qq.com"
    },
    titleInfo: "我的信息",
    password: "",
    password_check: "",
    password_show: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
  addUser: function(){
    var that = this;
    var password = that.data.password;
    var password_check = that.data.password_check;
    if(password == password_check){
      
    }else{
      wx.showModal({
        title: '提示',
        content: '对不起！您输入的两次密码不同！',
        success(res) {
          if (res.confirm) {
            that.setData({
              password_show: true
            });
          } else if (res.cancel) {
            that.setData({
              password_show: false
            });
          }
        }
      })
    }
  },
  passwordInput: function (e) {
    this.setData({
      password: e.detail.value
    });
  },
  passwordCheckInput: function (e) {
    this.setData({
      password_check: e.detail.value
    });
  } 
})