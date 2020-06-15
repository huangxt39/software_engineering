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
            image: ["../../images/turtlebot2.png","../../images/turtlebot2.0.png","../../images/turtlebot2.1.png",],
            description:"技术参数\n3个保险杠（碰撞传感器）：左，前，右\n1个悬崖感应器（防止从5cm以上高处跌落）\n1个车轮下降传感器（每个车轮一个）\n4个连接器：5V @ 1A Molex PN：43650-0218 - 用于定制电路板\n12V@1.5A：Molex PN：43045-0224 - 特别支持kinect\n12V @ 5A：Molex PN：5566-02B2 - 用于高功率配件（例如机械臂）\n19V @ 2A：Molex PN：3928-9068 - 用于上网本充电",
            components:[{name:'turtlebot2机体[型号xxx]', quantity:1 },{name:'充电器[型号xxx]', quantity:1 },{name:'笔记本电脑[型号]', quantity:1 }],
            total_amount: 100,
            left_amount: 3
          },
          {
            type_id: 2,
            name: 'turtlebot3',
            image: ["../../images/turtlebot3.png","../../images/turtlebot3.0.png",],
            description: "技术参数\n3个保险杠（碰撞传感器）：左，前，右\n1个悬崖感应器（防止从5cm以上高处跌落）\n1个车轮下降传感器（每个车轮一个）\n4个连接器：5V @ 1A Molex PN：43650-0218 - 用于定制电路板\n12V@1.5A：Molex PN：43045-0224 - 特别支持kinect\n12V @ 5A：Molex PN：5566-02B2 - 用于高功率配件（例如机械臂）\n19V @ 2A：Molex PN：3928-9068 - 用于上网本充电",
            components:[{name:'turtlebot3机体[型号xxx]', quantity:1 },{name:'充电器[型号xxx]', quantity:1 },{name:'笔记本电脑[型号]', quantity:1 }],
            total_amount: 100,
            left_amount: 2
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
            image: ["../../images/F550.png"],
            description: "[技术参数]",
            components:[{name:'F550机体[型号xxx]', quantity:1 },{name:'充电器[型号xxx]', quantity:1 },{name:'遥控[型号]', quantity:1 }],
            total_amount: 10,
            left_amount: 1
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
            image: ["../../images/stm32f103vct6.png"],
            description: "72 MHz CPU，具有高达1MB的Flash、电机控制、USB和CAN",
            components:[{name:'F550机体[型号xxx]', quantity:1 },{name:'充电器[型号xxx]', quantity:1 },{name:'遥控[型号]', quantity:1 }],
            total_amount: 10,
            left_amount: 1
          },
          {
            type_id: 5,
            name: 'STM32f103zet6',
            image: ["../../images/stm32f103zet6.png"],
            description: "[技术参数]",
            components:[{name:'F550机体[型号xxx]', quantity:1 },{name:'充电器[型号xxx]', quantity:1 },{name:'遥控[型号]', quantity:1 }],
            total_amount: 10,
            left_amount: 1
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
      url: "../devicesDetail/devicesDetail?item="+ JSON.stringify(e.currentTarget.dataset.item),
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