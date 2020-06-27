// pages/devices.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    cateItems: [
      {
        cate_id: 1,
        cate_name: "tutlebot",
        ishaveChild: true,
        children:
        [
          {
            type_id: 1,
            name: 'turtlebot2',
            image: "../../images/turtlebot2.png",
          },
          {
            type_id: 2,
            name: 'turtlebot3',
            image: "../../images/turtlebot3.png",
          }
        ]
      },
      {
        cate_id: 2,
        cate_name: "无人机",
        ishaveChild: true,
        children:
        [
          {
            type_id: 3,
            name: 'F550',
            image: "../../images/F550.png"
          }
        ]
      },
      {
        cate_id: 3,
        cate_name: "单片机",
        ishaveChild: true,
        children:
        [
          {
            type_id: 4,
            name: 'STM32f103vct6',
            image: "../../images/stm32f103vct6.png"
          },
          {
            type_id: 5,
            name: 'STM32f103zet6',
            image: "../../images/stm32f103zet6.png"
          }
        ]
      },
      {
        cate_id: 4,
        cate_name: "智能小车",
        ishaveChild: false,
        children: []
      }
    ],
    curNav: 1,
    curIndex: 0
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
  
  gotoDetail:function(e){
    var id=null;
    wx.navigateTo({
      url: "../devicesDetail/devicesDetail?item="+ JSON.stringify(e.currentTarget.dataset.item.type_id),
    })
  },
 
  //事件处理函数 
  switchRightTab: function (e) {
    // 获取item项的id，和数组的下标值 
    let id = e.target.dataset.id,
      index = parseInt(e.target.dataset.index);
    // 把点击到的某一项，设为当前index 
    this.setData({
      curNav: id,
      curIndex: index
    })
  }
})