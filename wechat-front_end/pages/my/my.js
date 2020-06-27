// pages/my/my.js
Page({

  /**
   * 页面的初始数据
   */
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {avatar: "../../images/turtlebot3.png"},
    user_info: '',
    edit_icon: "../../images/edit-icon.png"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //用户登录 获取头像 获取id等等
    this.setData({
      user_info: {id:"wx-sieusiaon", type: '学生', name:'黄鑫霆',stu_fac_id:'1736363636',bor_now:'2',bor_history:'100',money:'300',violate:'2',
      email:'1710019999@qq.com', phone:'15170829361',description:'我是中山大学2017级智能科学与技术专业本科生'}
    })
  },

  goDetail()  {
    wx.navigateTo({
      url: "../myInfo/myInfo?item="+JSON.stringify(this.data.user_info)
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