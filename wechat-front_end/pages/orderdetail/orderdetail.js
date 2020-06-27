// pages/orderdetail/orderdetail.js
import util from './../../utils/util.js';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    manager:[
      "张三",
      "李四"
    ],
    device_img:{
      "turtlebot":"../../images/turtlebot2.png",
      "F550":'../../images/F550.png'
    },
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let data=JSON.parse(options.item);
    console.log(data);
      this.setData({
        item:data,
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

  }
})